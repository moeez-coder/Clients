"""Shared lead-file helpers for this repo, built on listbuild's identity + title-guard code.

Run from the repo root:
  python tools/leads.py normalize IN.csv OUT.csv [--source blitz]   canonical schema, linkedin_url first, in-file dedupe
  python tools/leads.py overlap NEW.csv --client <slug>              rule 3a: overlap vs the client's other lead files
  python tools/leads.py titles FILE.csv [--column job_title]         title-guard tally + most common failing titles
  python tools/leads.py from-listbuild --client <slug> --icp <name> --config-slug <slug>
                                                                     land a listbuild export as sourcing snapshots
"""
import argparse
import csv
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / ".claude" / "skills" / "listbuild"))
from listbuild.identity import alt_key, normalize_domain, normalize_linkedin_url  # noqa: E402
from listbuild.seniority import classify_title  # noqa: E402

# listbuild's export columns with linkedin_url moved first (CLAUDE.md rule 3b).
CANON_COLS = ["linkedin_url", "first_name", "last_name", "full_name", "job_title", "seniority", "company_name",
              "company_domain", "company_linkedin_url", "industry", "revenue_hint", "person_country", "company_country",
              "first_source", "all_sources", "title_check", "icp_fit", "fit_reason"]

ALIASES = {
    "linkedin_url": ["linkedin_url", "linkedin", "person_linkedin_url", "profile_url", "linkedin_profile_url", "li_url"],
    "first_name": ["first_name", "firstname", "first"],
    "last_name": ["last_name", "lastname", "last"],
    "full_name": ["full_name", "name", "fullname"],
    "job_title": ["job_title", "title", "position", "current_title"],
    "company_name": ["company_name", "company", "organization", "account_name"],
    "company_domain": ["company_domain", "domain", "company_url", "website", "company_website"],
    "company_linkedin_url": ["company_linkedin_url", "company_linkedin"],
    "person_country": ["person_country", "country", "country_code"],
}
EMPTY = {"", "-", "none", "null", "n/a"}


def blank(v):
    return v is None or str(v).strip().lower() in EMPTY


def clean(v):
    return None if blank(v) else str(v).strip()


def canonical_linkedin(url):
    """Full profile URL form required by rule 3b, or None."""
    n = normalize_linkedin_url(url)
    return f"https://www.{n}" if n else None


def row_keys(row):
    """Both identity keys listbuild uses: LinkedIn URL, and first+last+domain (catches changed slugs)."""
    keys = set()
    li = normalize_linkedin_url(clean(row.get("linkedin_url")))
    if li:
        keys.add("li:" + li)
    ak = alt_key(clean(row.get("first_name")), clean(row.get("last_name")), clean(row.get("company_domain")))
    if ak:
        keys.add("alt:" + ak)
    return keys


def read_rows(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def map_row(raw, source=None):
    lower = {k.strip().lower(): v for k, v in raw.items() if k is not None}
    out = {}
    for canon, names in ALIASES.items():
        out[canon] = next((clean(lower[n]) for n in names if n in lower and not blank(lower[n])), None)
    for c in CANON_COLS:
        out.setdefault(c, clean(lower.get(c)))
    if not out["full_name"] and (out["first_name"] or out["last_name"]):
        out["full_name"] = " ".join(x for x in (out["first_name"], out["last_name"]) if x)
    if out["full_name"] and not (out["first_name"] or out["last_name"]):
        bits = out["full_name"].split(" ", 1)
        out["first_name"], out["last_name"] = bits[0], (bits[1] if len(bits) > 1 else None)
    out["linkedin_url"] = canonical_linkedin(out["linkedin_url"])
    out["company_domain"] = normalize_domain(out["company_domain"])
    if source:
        out["first_source"] = out["first_source"] or source
        out["all_sources"] = out["all_sources"] or source
    out["title_check"] = classify_title(out["job_title"])
    extras = {k: v for k, v in raw.items() if k is not None and k.strip().lower() not in CANON_COLS
              and k.strip().lower() not in {n for ns in ALIASES.values() for n in ns}}
    return out, extras


def normalize_rows(raw_rows, source=None):
    """Map to the canonical schema and collapse rows sharing either identity key. Returns (rows, extra_cols, stats)."""
    kept, index, extra_cols, stats = [], {}, [], Counter(rows_in=len(raw_rows))
    for raw in raw_rows:
        row, extras = map_row(raw, source)
        for k in extras:
            if k not in extra_cols:
                extra_cols.append(k)
        row.update(extras)
        keys = row_keys(row)
        if not row["linkedin_url"]:
            stats["missing_linkedin"] += 1
        hit = next((index[k] for k in keys if k in index), None)
        if hit is not None:
            prev = kept[hit]
            srcs = [s for s in (prev.get("all_sources") or "").split(",") + (row.get("all_sources") or "").split(",") if s]
            prev["all_sources"] = ",".join(dict.fromkeys(srcs)) or None
            for c in CANON_COLS:
                if blank(prev.get(c)) and not blank(row.get(c)):
                    prev[c] = row[c]
            for k in row_keys(prev):
                index[k] = hit
            stats["collapsed_duplicates"] += 1
            continue
        kept.append(row)
        for k in keys:
            index[k] = len(kept) - 1
    stats["rows_out"] = len(kept)
    stats.update({f"title_{k}": v for k, v in Counter(r["title_check"] for r in kept).items()})
    return kept, extra_cols, stats


def write_rows(path, rows, extra_cols=()):
    cols = CANON_COLS + [c for c in extra_cols if c not in CANON_COLS]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("-" if blank(r.get(c)) else r.get(c)) for c in cols})  # rule 4: no silent blanks


def next_free(path):
    """Append-only (rule 3): never overwrite a dated snapshot; add -2, -3, ... instead."""
    if not path.exists():
        return path
    stem, n = path.name[: -len(".csv")], 2
    while (path.parent / f"{stem}-{n}.csv").exists():
        n += 1
    return path.parent / f"{stem}-{n}.csv"


def overlap_report(new_path, client):
    new_path = Path(new_path).resolve()
    new_keys = [row_keys(r) for r in normalize_rows(read_rows(new_path))[0]]
    report = []
    for other in sorted((REPO / "clients" / client / "sourcing").rglob("*leads*.csv")):
        if other.resolve() == new_path:
            continue
        held = set()
        for r in read_rows(other):
            held |= row_keys(map_row(r)[0])
        hits = sum(1 for ks in new_keys if ks & held)
        if hits:
            report.append((other.relative_to(REPO / "clients" / client).as_posix(), hits))
    return len(new_keys), report


# ----------------------------------------------------------------------------- commands
def cmd_normalize(a):
    rows, extra, stats = normalize_rows(read_rows(a.input), a.source)
    write_rows(Path(a.output), rows, extra)
    print(f"wrote {a.output}: {dict(stats)}")


def cmd_overlap(a):
    total, report = overlap_report(a.new, a.client)
    if not report:
        print(f"no overlap: none of the {total} people in {a.new} appear in {a.client}'s other lead files")
        return
    print(f"{total} people checked against {a.client}'s other lead files (LinkedIn URL or first+last+domain):")
    for f, n in report:
        print(f"  {n:6} also in {f}")
    print("History line: " + "; ".join(f"{n} of these also appear in `{f}`" for f, n in report))


def cmd_titles(a):
    rows = read_rows(a.file)
    col = a.column or next((c for c in ("job_title", "title", "position", "headline") if rows and c in rows[0]), None)
    if not col:
        sys.exit(f"no title column found; pass --column (have: {list(rows[0]) if rows else []})")
    checks = [(classify_title(r.get(col)), r.get(col)) for r in rows]
    print(f"{a.file} [{col}]: {dict(Counter(c for c, _ in checks))}")
    fails = Counter(t for c, t in checks if c == "fail")
    if fails:
        print("most common failing titles (sub-director by listbuild's guard; may be intended if the ICP includes managers):")
        for t, n in fails.most_common(a.top):
            print(f"  {n:5}  {t}")


def cmd_from_listbuild(a):
    ws = REPO / "clients" / a.client / "listbuild"
    out = ws / "out" / a.icp
    parts = sorted(out.glob(f"{a.icp}_*_part*.csv"))
    if not parts:
        sys.exit(f"no listbuild export in {out}; run `listbuild ... run` (export stage) first")
    stamp = max(re.match(rf"{re.escape(a.icp)}_(\d{{8}})", p.name).group(1) for p in parts)
    day = a.date or date.today().isoformat()
    dest = REPO / "clients" / a.client / "sourcing" / a.config_slug
    written = []
    for suffix, name in (("", "leads"), ("_consulting_candidates", "leads-candidates"), ("_unverified", "leads-unverified")):
        files = sorted(out.glob(f"{a.icp}_{stamp}{suffix}_part*.csv"))
        raw = [r for f in files for r in read_rows(f)]
        if not raw:
            continue
        rows, extra, stats = normalize_rows(raw)
        path = next_free(dest / f"{day}-{name}.csv")
        write_rows(path, rows, extra)
        written.append((path, stats))
        print(f"wrote {path.relative_to(REPO)}: {dict(stats)}")
    main = written[0][0] if written else None
    qa = {}
    ledger = out / "ledger.sqlite"
    if ledger.exists():
        row = sqlite3.connect(ledger).execute("SELECT v FROM kv WHERE k = 'consolidate'").fetchone()
        qa = json.dumps(json.loads(row[0]), indent=2) if row else {}
    cost = (out / "cost_report.md").read_text(encoding="utf-8") if (out / "cost_report.md").exists() else "(no cost_report.md)"
    if main:
        q = main.with_name(main.name[: -len(".csv")] + ".query.md")
        q.write_text(
            f"# Query — {main.name} (listbuild)\n\n"
            f"**Tool:** listbuild skill (`.claude/skills/listbuild/`), export stamp `{stamp}`\n"
            f"**Config (the query itself):** `clients/{a.client}/listbuild/config/{a.icp}.yaml`\n"
            f"**Files:** " + ", ".join(f"`{p.name}` ({s['rows_out']} rows)" for p, s in written) + "\n\n"
            "**Purpose / scope / seniority choice:** TODO — say why this build was run, General vs Campaign-specific, "
            "and why this seniority tier (CLAUDE.md requires it).\n\n"
            f"## consolidate QA counts\n\n```\n{qa or '(ledger not found)'}\n```\n\n## cost_report.md\n\n{cost}\n",
            encoding="utf-8")
        print(f"wrote {q.relative_to(REPO)} (fill in the TODO purpose line)")
        print(f"next: python tools/leads.py overlap {main.relative_to(REPO)} --client {a.client}  -> README History entry")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="leads", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("normalize"); p.add_argument("input"); p.add_argument("output"); p.add_argument("--source")
    p = sub.add_parser("overlap"); p.add_argument("new"); p.add_argument("--client", required=True)
    p = sub.add_parser("titles"); p.add_argument("file"); p.add_argument("--column"); p.add_argument("--top", type=int, default=20)
    p = sub.add_parser("from-listbuild"); p.add_argument("--client", required=True); p.add_argument("--icp", required=True)
    p.add_argument("--config-slug", required=True); p.add_argument("--date")
    a = ap.parse_args(argv)
    {"normalize": cmd_normalize, "overlap": cmd_overlap, "titles": cmd_titles, "from-listbuild": cmd_from_listbuild}[a.cmd](a)


if __name__ == "__main__":
    main()
