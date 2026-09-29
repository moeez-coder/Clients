"""SQLite ledger: the single source of truth for what we hold, what we exclude, and what we spent."""
import json
import sqlite3
import threading
from datetime import datetime, timezone

from .identity import alt_key, contact_key, normalize_domain, normalize_linkedin_url

CONTACT_COLUMNS = [
    "linkedin_url", "first_name", "last_name", "full_name", "job_title", "seniority",
    "company_name", "company_domain", "company_linkedin_url", "industry", "revenue_hint",
    "person_country", "company_country",
]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS contacts(
  key TEXT PRIMARY KEY, linkedin_url TEXT, alt_key TEXT,
  first_name TEXT, last_name TEXT, full_name TEXT, job_title TEXT, seniority TEXT,
  company_name TEXT, company_domain TEXT, company_linkedin_url TEXT, industry TEXT, revenue_hint TEXT,
  person_country TEXT, company_country TEXT,
  first_source TEXT, all_sources TEXT, cost_usd REAL DEFAULT 0, title_check TEXT, fetched_at TEXT);
CREATE INDEX IF NOT EXISTS idx_contacts_alt ON contacts(alt_key);
CREATE INDEX IF NOT EXISTS idx_contacts_domain ON contacts(company_domain);
CREATE TABLE IF NOT EXISTS companies(
  domain TEXT PRIMARY KEY, name TEXT, name_norm TEXT, linkedin_url TEXT, country TEXT, industry TEXT, first_source TEXT);
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name_norm);
CREATE INDEX IF NOT EXISTS idx_companies_linkedin ON companies(linkedin_url);
CREATE INDEX IF NOT EXISTS idx_contacts_company_li ON contacts(company_linkedin_url);
CREATE TABLE IF NOT EXISTS excluded(
  key TEXT PRIMARY KEY, linkedin_url TEXT, alt_key TEXT, company_domain TEXT, origin TEXT);
CREATE INDEX IF NOT EXISTS idx_excluded_alt ON excluded(alt_key);
CREATE TABLE IF NOT EXISTS shards(
  id TEXT PRIMARY KEY, provider TEXT, filters TEXT, expected_total INTEGER, fetched INTEGER DEFAULT 0,
  status TEXT DEFAULT 'pending', cursor TEXT, note TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS spend(
  id INTEGER PRIMARY KEY AUTOINCREMENT, provider TEXT, action TEXT, units INTEGER, cost_usd REAL, note TEXT, ts TEXT);
CREATE TABLE IF NOT EXISTS paid_unqualified(
  key TEXT PRIMARY KEY, provider TEXT, payload TEXT, reason TEXT, cost_usd REAL, ts TEXT);
CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY, v TEXT);
"""


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Ledger:
    def __init__(self, path):
        self.path = str(path)
        self.conn = sqlite3.connect(self.path, check_same_thread=False, timeout=60)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.lock = threading.RLock()
        with self.lock:
            self.conn.executescript(_SCHEMA)
            self._add_column_if_missing("companies", "keyword_fit", "INTEGER")
            self._add_column_if_missing("companies", "size", "TEXT")
            self._add_column_if_missing("contacts", "icp_fit", "TEXT")
            self._add_column_if_missing("contacts", "fit_reason", "TEXT")

    def _add_column_if_missing(self, table, column, decl):
        cols = {r[1] for r in self.conn.execute(f"PRAGMA table_info({table})").fetchall()}
        if column not in cols:
            self.conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {decl}")
            self.conn.commit()

    # ---------- ICP fit ----------
    def set_keyword_fit(self, fit_domains, checked_domains):
        """Mark companies that matched the keyword search (1) and those checked but not matching (0)."""
        fit = {normalize_domain(d) for d in fit_domains if normalize_domain(d)}
        checked = {normalize_domain(d) for d in checked_domains if normalize_domain(d)}
        with self.lock:
            for d in checked - fit:
                self.conn.execute("UPDATE companies SET keyword_fit = 0 WHERE domain = ? AND keyword_fit IS NULL", (d,))
            for d in fit:
                self.conn.execute("UPDATE companies SET keyword_fit = 1 WHERE domain = ?", (d,))
            self.conn.commit()

    def apply_fit(self, icp):
        """Classify every contact from its company's industry (companies table first, contact row second)."""
        from .icp_fit import classify_company_fit
        counts = {"fit": 0, "candidate": 0, "unfit": 0, "unknown": 0}
        with self.lock:
            rows = self.conn.execute(
                "SELECT ct.key, ct.industry AS c_ind, co.industry AS co_ind, co.keyword_fit AS kw "
                "FROM contacts ct LEFT JOIN companies co ON co.domain = ct.company_domain").fetchall()
            for r in rows:
                kw = None if r["kw"] is None else bool(r["kw"])
                status, reason = classify_company_fit(icp, r["co_ind"] or r["c_ind"], kw)
                counts[status] += 1
                if r["co_ind"]:
                    self.conn.execute("UPDATE contacts SET icp_fit = ?, fit_reason = ?, industry = ? WHERE key = ?", (status, reason, r["co_ind"], r["key"]))
                else:
                    self.conn.execute("UPDATE contacts SET icp_fit = ?, fit_reason = ? WHERE key = ?", (status, reason, r["key"]))
            self.conn.commit()
        return counts

    # ---------- contacts ----------
    def _keys(self, row):
        key = contact_key(row.get("linkedin_url"), row.get("first_name"), row.get("last_name"), row.get("company_domain"))
        ak = alt_key(row.get("first_name"), row.get("last_name"), row.get("company_domain"))
        return key, ak

    def is_excluded(self, key, ak):
        """Excluded if the LinkedIn key matches, or if the name+domain key matches and either side lacks a LinkedIn URL."""
        if key.startswith("li:"):
            cur = self.conn.execute(
                "SELECT 1 FROM excluded WHERE key = ? OR (? IS NOT NULL AND linkedin_url IS NULL AND alt_key = ?) LIMIT 1", (key, ak, ak))
        else:
            cur = self.conn.execute("SELECT 1 FROM excluded WHERE key = ? OR (? IS NOT NULL AND alt_key = ?) LIMIT 1", (key, ak, ak))
        return cur.fetchone() is not None

    def _find_existing(self, key, ak):
        """A LinkedIn-keyed row matches only on LinkedIn; a row without LinkedIn may match on name+domain."""
        if key.startswith("li:"):
            return self.conn.execute("SELECT * FROM contacts WHERE key = ? LIMIT 1", (key,)).fetchone()
        return self.conn.execute(
            "SELECT * FROM contacts WHERE key = ? OR (? IS NOT NULL AND alt_key = ?) LIMIT 1", (key, ak, ak)).fetchone()

    def upsert_contact(self, row, commit=True):
        """Insert or merge one contact. Returns 'inserted' | 'merged' | 'excluded' | 'skipped'."""
        key, ak = self._keys(row)
        if not key:
            return "skipped"
        with self.lock:
            if self.is_excluded(key, ak):
                return "excluded"
            existing = self._find_existing(key, ak)
            source = row.get("source") or "unknown"
            domain = normalize_domain(row.get("company_domain"))
            if existing:
                sources = existing["all_sources"].split(",") if existing["all_sources"] else []
                if source not in sources:
                    sources.append(source)
                fills = {c: row.get(c) for c in CONTACT_COLUMNS if existing[c] in (None, "") and row.get(c) not in (None, "")}
                if "company_domain" in fills:
                    fills["company_domain"] = domain
                sets = ", ".join([f"{c} = ?" for c in fills] + ["all_sources = ?"])
                self.conn.execute(f"UPDATE contacts SET {sets} WHERE key = ?", [*fills.values(), ",".join(sources), existing["key"]])
                result = "merged"
            else:
                vals = {c: row.get(c) for c in CONTACT_COLUMNS}
                vals["company_domain"] = domain
                vals["linkedin_url"] = normalize_linkedin_url(row.get("linkedin_url")) or row.get("linkedin_url")
                self.conn.execute(
                    f"INSERT INTO contacts(key, alt_key, {', '.join(CONTACT_COLUMNS)}, first_source, all_sources, cost_usd, title_check, fetched_at) "
                    f"VALUES (?, ?, {', '.join('?' * len(CONTACT_COLUMNS))}, ?, ?, ?, ?, ?)",
                    [key, ak, *vals.values(), source, source, float(row.get("cost_usd") or 0), row.get("title_check"), _now()])
                result = "inserted"
            if domain:
                self.upsert_company({"domain": domain, "name": row.get("company_name"), "linkedin_url": row.get("company_linkedin_url"),
                                     "country": row.get("company_country"), "industry": row.get("industry"), "source": source}, commit=False)
            if commit:
                self.conn.commit()
            return result

    def upsert_many(self, rows):
        """Insert a page of rows in one transaction. Returns counts per outcome."""
        out = {"inserted": 0, "merged": 0, "excluded": 0, "skipped": 0}
        with self.lock:
            for r in rows:
                out[self.upsert_contact(r, commit=False)] += 1
            self.conn.commit()
        return out

    def get_contact(self, key):
        r = self.conn.execute("SELECT * FROM contacts WHERE key = ?", (key,)).fetchone()
        return dict(r) if r else None

    def count_contacts(self):
        return self.conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]

    def iter_contacts(self, where="1=1", params=()):
        cur = self.conn.execute(f"SELECT * FROM contacts WHERE {where} ORDER BY key", params)
        for r in cur:
            yield dict(r)

    # ---------- companies ----------
    def upsert_company(self, c, commit=True):
        from .identity import normalize_company_name
        domain = normalize_domain(c.get("domain"))
        if not domain:
            return
        with self.lock:
            self.conn.execute(
                "INSERT INTO companies(domain, name, name_norm, linkedin_url, country, industry, first_source, size) VALUES (?,?,?,?,?,?,?,?) "
                "ON CONFLICT(domain) DO UPDATE SET name = COALESCE(companies.name, excluded.name), "
                "name_norm = COALESCE(companies.name_norm, excluded.name_norm), linkedin_url = COALESCE(companies.linkedin_url, excluded.linkedin_url), "
                "country = COALESCE(companies.country, excluded.country), industry = COALESCE(excluded.industry, companies.industry), "
                "size = COALESCE(companies.size, excluded.size)",
                (domain, c.get("name"), normalize_company_name(c.get("name")) or None, c.get("linkedin_url"), c.get("country"), c.get("industry"),
                 c.get("source"), c.get("size")))
            if commit:
                self.conn.commit()

    def known_domains(self):
        """Domains where we already hold or exclude people. Never includes company-only domains."""
        rows = self.conn.execute(
            "SELECT company_domain FROM contacts WHERE company_domain IS NOT NULL "
            "UNION SELECT company_domain FROM excluded WHERE company_domain IS NOT NULL").fetchall()
        return {r[0] for r in rows}

    def company_only_domains(self):
        rows = self.conn.execute(
            "SELECT domain FROM companies WHERE domain NOT IN (SELECT company_domain FROM contacts WHERE company_domain IS NOT NULL) "
            "AND domain NOT IN (SELECT company_domain FROM excluded WHERE company_domain IS NOT NULL)").fetchall()
        return {r[0] for r in rows}

    def domain_for_company_name(self, name):
        from .identity import normalize_company_name
        n = normalize_company_name(name)
        if not n:
            return None
        r = self.conn.execute("SELECT domain FROM companies WHERE name_norm = ? LIMIT 1", (n,)).fetchone()
        return r[0] if r else None

    # ---------- exclusions ----------
    def add_excluded(self, rows, origin=None):
        n = 0
        with self.lock:
            for r in rows:
                key, ak = self._keys(r)
                if not key:
                    continue
                li = normalize_linkedin_url(r.get("linkedin_url"))
                dom = normalize_domain(r.get("company_domain"))
                self.conn.execute(
                    "INSERT OR IGNORE INTO excluded(key, linkedin_url, alt_key, company_domain, origin) VALUES (?,?,?,?,?)",
                    (key, li, ak, dom, r.get("origin") or origin))
                if ak and key != "alt:" + ak:
                    # keep every name variant seen for this LinkedIn URL (e.g. surname changes) so name+domain purges still match
                    self.conn.execute(
                        "INSERT OR IGNORE INTO excluded(key, linkedin_url, alt_key, company_domain, origin) VALUES (?,?,?,?,?)",
                        ("alt:" + ak, li, ak, dom, r.get("origin") or origin))
                n += 1
            self.conn.commit()
        return n

    def purge_excluded(self):
        """Remove contacts that match an exclusion by LinkedIn key OR by first+last+domain.

        The name+domain match is deliberately applied even when both sides carry (different) LinkedIn
        URLs: people change their LinkedIn slug, and re-contacting a prior prospect costs more than
        losing the rare same-name colleague. Returns rows removed.
        """
        with self.lock:
            cur = self.conn.execute(
                "DELETE FROM contacts WHERE key IN (SELECT key FROM excluded) "
                "OR alt_key IN (SELECT alt_key FROM excluded WHERE alt_key IS NOT NULL)")
            self.conn.commit()
            return cur.rowcount

    def refresh_alt_keys(self):
        """Recompute first+last+domain keys for rows whose domain was back-filled after insertion. Returns rows changed."""
        changed = 0
        with self.lock:
            rows = self.conn.execute(
                "SELECT key, alt_key, first_name, last_name, company_domain FROM contacts WHERE company_domain IS NOT NULL").fetchall()
            for r in rows:
                ak = alt_key(r["first_name"], r["last_name"], r["company_domain"])
                if ak and ak != r["alt_key"]:
                    self.conn.execute("UPDATE contacts SET alt_key = ? WHERE key = ?", (ak, r["key"]))
                    changed += 1
            self.conn.commit()
        return changed

    @staticmethod
    def _slug_root(linkedin_url):
        import re
        n = normalize_linkedin_url(linkedin_url) or ""
        return re.sub(r"[^a-z]", "", n.split("/in/")[-1])

    @classmethod
    def _slugs_alike(cls, a, b, first=None, last=None):
        """Same person if the slugs share a root, or if both are just the person's name plus a short suffix."""
        import re
        ra, rb = cls._slug_root(a), cls._slug_root(b)
        if not ra or not rb:
            return False
        if ra[:6] == rb[:6] or ra in rb or rb in ra:
            return True
        names = [re.sub(r"[^a-z]", "", (n or "").lower()) for n in (first, last)]
        names = [n for n in names if len(n) >= 2]

        def residual(root):
            for n in sorted(names, key=len, reverse=True):
                root = root.replace(n, "")
            return root
        return len(residual(ra)) <= 5 and len(residual(rb)) <= 5

    def dedupe_similar_slugs(self):
        """Collapse rows that share first+last+domain and whose LinkedIn slugs resemble each other (same person,
        old vs new custom URL). Rows with unlike slugs are kept as distinct people. Returns rows removed."""
        removed = 0
        with self.lock:
            groups = self.conn.execute(
                "SELECT alt_key FROM contacts WHERE alt_key IS NOT NULL GROUP BY alt_key HAVING COUNT(*) > 1").fetchall()
            for (ak,) in groups:
                rows = self.conn.execute(
                    "SELECT key, linkedin_url, all_sources, first_name, last_name FROM contacts WHERE alt_key = ? ORDER BY fetched_at, key", (ak,)).fetchall()
                kept = []
                for r in rows:
                    match = next((k for k in kept if self._slugs_alike(k["linkedin_url"], r["linkedin_url"], r["first_name"], r["last_name"])), None)
                    if match is None:
                        kept.append(r)
                        continue
                    sources = match["all_sources"].split(",") if match["all_sources"] else []
                    for s in (r["all_sources"] or "").split(","):
                        if s and s not in sources:
                            sources.append(s)
                    self.conn.execute("UPDATE contacts SET all_sources = ? WHERE key = ?", (",".join(sources), match["key"]))
                    self.conn.execute("DELETE FROM contacts WHERE key = ?", (r["key"],))
                    match = dict(match)
                    match["all_sources"] = ",".join(sources)
                    kept[kept.index(next(k for k in kept if k["key"] == match["key"]))] = match
                    removed += 1
            self.conn.commit()
        return removed

    def count_excluded(self):
        return self.conn.execute("SELECT COUNT(*) FROM excluded").fetchone()[0]

    # ---------- shards ----------
    @staticmethod
    def _shard_id(provider, filters):
        return provider + ":" + json.dumps(filters, sort_keys=True)

    def save_shard(self, provider, filters, expected_total, note=None):
        with self.lock:
            self.conn.execute(
                "INSERT INTO shards(id, provider, filters, expected_total, note, updated_at) VALUES (?,?,?,?,?,?) "
                "ON CONFLICT(id) DO UPDATE SET expected_total = excluded.expected_total, updated_at = excluded.updated_at",
                (self._shard_id(provider, filters), provider, json.dumps(filters, sort_keys=True), expected_total, note, _now()))
            self.conn.commit()

    def update_shard(self, provider, filters, **fields):
        allowed = {k: v for k, v in fields.items() if k in ("fetched", "status", "cursor", "note", "expected_total")}
        sets = ", ".join(f"{k} = ?" for k in allowed) + ", updated_at = ?"
        with self.lock:
            self.conn.execute(f"UPDATE shards SET {sets} WHERE id = ?", [*allowed.values(), _now(), self._shard_id(provider, filters)])
            self.conn.commit()

    def get_shard(self, provider, filters):
        r = self.conn.execute("SELECT * FROM shards WHERE id = ?", (self._shard_id(provider, filters),)).fetchone()
        if not r:
            return None
        d = dict(r)
        d["filters"] = json.loads(d["filters"])
        return d

    def pending_shards(self, provider):
        rows = self.conn.execute("SELECT * FROM shards WHERE provider = ? AND status != 'done' ORDER BY id", (provider,)).fetchall()
        out = []
        for r in rows:
            d = dict(r)
            d["filters"] = json.loads(d["filters"])
            out.append(d)
        return out

    def shard_summary(self, provider):
        r = self.conn.execute(
            "SELECT COUNT(*) n, SUM(expected_total) expected, SUM(fetched) fetched, "
            "SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) done FROM shards WHERE provider = ?", (provider,)).fetchone()
        return dict(r)

    # ---------- spend ----------
    def record_spend(self, provider, action, units, cost_usd, note=None):
        with self.lock:
            self.conn.execute("INSERT INTO spend(provider, action, units, cost_usd, note, ts) VALUES (?,?,?,?,?,?)",
                              (provider, action, units, cost_usd, note, _now()))
            self.conn.commit()

    def total_spend(self, provider=None):
        if provider:
            r = self.conn.execute("SELECT COALESCE(SUM(cost_usd), 0) FROM spend WHERE provider = ?", (provider,)).fetchone()
        else:
            r = self.conn.execute("SELECT COALESCE(SUM(cost_usd), 0) FROM spend").fetchone()
        return round(r[0], 6)

    def add_paid_unqualified(self, key, provider, payload, reason, cost_usd):
        with self.lock:
            self.conn.execute("INSERT OR IGNORE INTO paid_unqualified(key, provider, payload, reason, cost_usd, ts) VALUES (?,?,?,?,?,?)",
                              (key, provider, json.dumps(payload), reason, cost_usd, _now()))
            self.conn.commit()

    # ---------- kv ----------
    def set_kv(self, k, v):
        with self.lock:
            self.conn.execute("INSERT INTO kv(k, v) VALUES (?, ?) ON CONFLICT(k) DO UPDATE SET v = excluded.v", (k, json.dumps(v)))
            self.conn.commit()

    def get_kv(self, k, default=None):
        r = self.conn.execute("SELECT v FROM kv WHERE k = ?", (k,)).fetchone()
        return json.loads(r[0]) if r else default

    def stats(self):
        q = self.conn.execute
        return {
            "contacts": self.count_contacts(),
            "companies": q("SELECT COUNT(*) FROM companies").fetchone()[0],
            "excluded": self.count_excluded(),
            "contacts_without_domain": q("SELECT COUNT(*) FROM contacts WHERE company_domain IS NULL").fetchone()[0],
            "by_source": {r[0]: r[1] for r in q("SELECT first_source, COUNT(*) FROM contacts GROUP BY first_source")},
            "spend_usd": self.total_spend(),
        }
