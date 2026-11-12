"""CLI orchestrating the cheapest-first, exclusion-aware list build.

Commands:
  probe               capability probe for every provider (free)
  seed                ingest prior CSVs into the exclusion table
  sweep-blitz         plan shards and drain them (free)
  sweep-clay          people (or companies) sweep (free, quota-bound); use --ledger for a side ledger
  merge-ledger        fold a side ledger (e.g. the Clay one) into the main ledger with full dedupe
  join-domains        fill missing company domains from the companies table (+ --enrich via Blitz, free)
  estimate-discolike  free counts + tiny overlap sample, prints the cost estimate and STOPS
  fetch-discolike     paid fetch up to an approved USD cap (blind or thin-company targeted)
  consolidate         title guard, region checks, stats
  export              CSV chunks + cost report
  report              stats and spend
"""
import argparse
import csv
import json
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from .config import WORKSPACE, load_icp, load_keys, load_providers, workspace_out
from .identity import normalize_domain, normalize_linkedin_url
from .ledger import Ledger
from .seniority import classify_title
from .sharding import plan_shards
from .providers import blitz as B
from .providers import clay as C
from .providers import discolike as D



def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Ctx:
    def __init__(self, args, ledger_path=None):
        self.args = args
        self.icp = load_icp(args.icp)
        self.prov = load_providers()
        self.keys = load_keys()
        self.out = workspace_out() / self.icp["name"]   # one folder per ICP inside the workspace: ledger, logs, CSVs
        self.out.mkdir(parents=True, exist_ok=True)
        self.ledger = Ledger(ledger_path or args.ledger or self.out / "ledger.sqlite")

    def with_ledger(self, path):
        return Ctx(self.args, ledger_path=path)

    def blitz(self):
        return B.BlitzClient(self.keys["blitz"], self.prov["blitz"]["base_url"], rps=min(40, self.prov["blitz"].get("rps", 40)))

    def clay(self):
        return C.ClayClient(self.keys["clay"], self.prov["clay"]["base_url"])

    def discolike(self):
        return D.DiscoLikeClient(self.keys["discolike"], self.prov["discolike"]["base_url"])


def _notice(lg, text):
    """Append a provider-limit notice that `run` prints at the end."""
    notices = lg.get_kv("run_notices", [])
    if text not in notices:
        notices.append(text)
    lg.set_kv("run_notices", notices)


def _tag(rows):
    for r in rows:
        r["title_check"] = classify_title(r.get("job_title"))
    return rows


# ----------------------------------------------------------------------------- probe
def cmd_probe(ctx, args):
    icp, lg = ctx.icp, ctx.ledger
    results = {}

    bz = ctx.blitz()
    ki = bz.key_info()
    results["blitz_key"] = {"valid": ki.get("valid"), "records_remaining": ki.get("records_remaining"),
                            "rps": ki.get("max_requests_per_seconds"), "plan": [p.get("name") for p in ki.get("active_plans", [])]}
    small = {"country": "NZ"}
    page = bz.search_people(B.build_people_body(icp, small, page_size=50))
    rows = [B.parse_person(r, small) for r in page.get("results", [])]
    results["blitz_page"] = {"rows": len(rows), "with_domain": sum(1 for r in rows if r["company_domain"]),
                             "with_linkedin": sum(1 for r in rows if r["linkedin_url"]), "total_results_NZ": page.get("total_results"),
                             "records_used": (page.get("fair_usage") or {}).get("records_used")}
    log(f"Blitz: {results['blitz_key']} | NZ page: {results['blitz_page']}")

    cl = ctx.clay()
    me = cl.me()
    results["clay_me"] = {"user": me.get("user", {}).get("email"), "workspace": me.get("workspace", {}).get("name")}
    sid, _ = cl.create_search(C.build_people_query(icp, {"location_country": "NZ"}))
    t0 = time.time()
    run1 = cl.run(sid, ctx.prov["clay"]["page_size"])
    data = run1.get("data") or []
    sample = data[0] if data else {}
    results["clay_run"] = {"rows": len(data), "seconds": round(time.time() - t0, 1), "has_more": run1.get("has_more"),
                           "exhaustion_reason": run1.get("exhaustion_reason"), "period_quota": run1.get("period_quota"),
                           "sample_keys": sorted(sample.keys()) if sample else []}
    log(f"Clay: {results['clay_me']} | run: {results['clay_run']}")

    dl = ctx.discolike()
    usage = dl.usage()
    results["discolike_usage"] = {k: usage.get(k) for k in ("account_status", "month_to_date_spend", "max_spend", "total_available_spend")}
    day = now_iso()[:10]
    results["discolike_billed_today"] = D.DiscoLikeClient.billing_since(usage, day)
    base = D.build_contact_params(icp, employee_floor=icp.get("discolike_employee_floor"))
    results["discolike_count_A"] = dl.count(base)
    results["discolike_note"] = "exclusion_query_id verified non-functional on 2026-09-22; not used"
    log(f"DiscoLike: {results['discolike_usage']} billed today {results['discolike_billed_today']} count {results['discolike_count_A']}")

    results["ts"] = now_iso()
    lg.set_kv("probe", results)
    (ctx.out / "probe.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


# ----------------------------------------------------------------------------- seed
def _pick(header, *cands):
    hl = [h.lower().strip() for h in header]
    for cand in cands:
        for i, h in enumerate(hl):
            if cand in h:
                return header[i]
    return None


def cmd_seed(ctx, args):
    from .seeds import iter_seed_rows
    lg = ctx.ledger
    total, batch = 0, []
    for r in iter_seed_rows(args.csv):
        if args.origin:
            r["origin"] = args.origin
        batch.append(r)
        if len(batch) >= 5000:
            total += lg.add_excluded(batch)
            batch = []
    total += lg.add_excluded(batch)
    log(f"seeded {total:,} rows from {len(args.csv)} file(s); excluded table now has {lg.count_excluded():,} keys")


# ----------------------------------------------------------------------------- blitz
def cmd_sweep_blitz(ctx, args):
    icp, lg, cfg = ctx.icp, ctx.ledger, ctx.prov["blitz"]
    bz = ctx.blitz()
    base = {"country": args.only_country} if args.only_country else {}
    dims = B.SHARD_DIMS(icp)
    if args.only_country:
        dims = [d for d in dims if d[0] != "country"]

    pending = [s for s in lg.pending_shards("blitz") if all(s["filters"].get(k) == v for k, v in base.items())]
    if not pending or args.replan:
        log("planning shards (each count costs 1 record)...")
        gaps = []

        def on_split(parent, ptotal, ctotal):
            gap = (ctotal - ptotal) / ptotal if ptotal else 0
            gaps.append({"parent": parent, "parent_total": ptotal, "children_total": ctotal, "gap_pct": round(100 * gap, 1)})
            if abs(gap) > 0.10:
                log(f"  partition gap {100*gap:+.1f}% at {parent}: parent {ptotal} vs children {ctotal}")

        # always split down to country x job_level so every row carries a seniority value, then adapt below that
        fixed = [d for d in dims if d[0] in ("country", "job_level")]
        adaptive = [d for d in dims if d[0] not in ("country", "job_level")]
        seeds = [dict(base)]
        for name, values in fixed:
            seeds = [{**s, name: v} for s in seeds for v in values]
        shards = []
        for seed in seeds:
            shards += plan_shards(seed, adaptive, lambda f: bz.count(icp, f), cap=cfg["shard_cap"], on_split=on_split)
        for s in shards:
            lg.save_shard("blitz", s.filters, s.expected_total, note="oversized" if s.oversized else None)
        lg.set_kv("blitz_partition_log", gaps)
        log(f"planned {len(shards)} shards, expected {sum(s.expected_total for s in shards):,} rows, "
            f"{sum(1 for s in shards if s.oversized)} oversized, {bz.records_used} records used planning")
        pending = [s for s in lg.pending_shards("blitz") if all(s["filters"].get(k) == v for k, v in base.items())]
    if args.plan_only:
        return

    log(f"sweeping {len(pending)} shards with {cfg['workers']} workers")
    progress = {"rows": 0, "inserted": 0, "merged": 0, "excluded": 0, "pages": 0}
    plock = threading.Lock()
    t0 = time.time()

    def run_shard(shard):
        filters = shard["filters"]
        cursor, fetched = shard.get("cursor"), shard.get("fetched") or 0
        while True:
            data = bz.search_people(B.build_people_body(icp, filters, cfg["page_size"], cursor))
            rows = _tag([B.parse_person(r, filters) for r in data.get("results", [])])
            out = lg.upsert_many(rows)
            fetched += len(rows)
            cursor = data.get("cursor")
            lg.update_shard("blitz", filters, fetched=fetched, cursor=cursor, status="running")
            with plock:
                progress["rows"] += len(rows)
                progress["pages"] += 1
                for k in ("inserted", "merged", "excluded"):
                    progress[k] += out[k]
                if progress["pages"] % 100 == 0:
                    el = time.time() - t0
                    log(f"  {progress['rows']:,} rows / {progress['pages']} pages in {el/60:.1f} min "
                        f"({progress['rows']/max(el,1):.0f} rows/s) inserted={progress['inserted']:,} merged={progress['merged']:,} excluded={progress['excluded']:,}")
            if not cursor or not rows:
                break
        lg.update_shard("blitz", filters, status="done", fetched=fetched, cursor=None)
        return fetched

    with ThreadPoolExecutor(max_workers=cfg["workers"]) as ex:
        futs = {ex.submit(run_shard, s): s for s in pending}
        for f in as_completed(futs):
            s = futs[f]
            try:
                f.result()
            except Exception as e:  # noqa: BLE001
                log(f"shard {s['filters']} failed: {e}")
                lg.update_shard("blitz", s["filters"], status="error", note=str(e)[:200])
    el = time.time() - t0
    log(f"Blitz sweep finished: {progress} in {el/60:.1f} min; summary {lg.shard_summary('blitz')}; records used {bz.records_used:,}")


# ----------------------------------------------------------------------------- blitz companies (industry labels + keyword gate)
def cmd_sweep_blitz_companies(ctx, args):
    """Enumerate ICP companies via Blitz company search (free). --keywords restricts to the keyword-gated industries
    plus marketing keywords and flags matches; without it, every ICP company gets its authoritative industry label."""
    icp, lg, cfg = ctx.icp, ctx.ledger, ctx.prov["blitz"]
    bz = ctx.blitz()
    fit = icp["fit"]
    industries = list(fit["keyword_gated_industries"]) if args.keywords else list(icp["industries"]["blitz"])
    keywords = list(fit["keywords"]) if args.keywords else None
    provider = "blitz_companies_kw" if args.keywords else "blitz_companies"
    dims = B.COMPANY_SHARD_DIMS(icp, industries)

    pending = lg.pending_shards(provider)
    if not pending or args.replan:
        log(f"planning {provider} shards...")
        fixed = [d for d in dims if d[0] in ("country", "industry")]
        adaptive = [d for d in dims if d[0] not in ("country", "industry")]
        seeds = [{}]
        for name, values in fixed:
            seeds = [{**s, name: v} for s in seeds for v in values]
        shards = []
        for seed in seeds:
            shards += plan_shards(seed, adaptive, lambda f: bz.count_companies(icp, f, industries, keywords), cap=cfg["shard_cap"])
        for s in shards:
            lg.save_shard(provider, s.filters, s.expected_total, note="oversized" if s.oversized else None)
        log(f"planned {len(shards)} shards, expected {sum(s.expected_total for s in shards):,} companies")
        pending = lg.pending_shards(provider)

    progress = {"rows": 0, "with_domain": 0, "pages": 0}
    plock = threading.Lock()
    matched_domains = set()
    t0 = time.time()

    def run_shard(shard):
        filters = shard["filters"]
        cursor, fetched = shard.get("cursor"), shard.get("fetched") or 0
        while True:
            data = bz.search_companies(B.build_company_body(icp, filters, cfg["page_size"], cursor, industries, keywords))
            results = data.get("results", [])
            comps = [B.parse_company(r) for r in results]
            with lg.lock:
                for c in comps:
                    if c["domain"]:
                        lg.upsert_company(c, commit=False)
                        if keywords:
                            matched_domains.add(c["domain"])
                    # contacts that only know the company LinkedIn URL: give them the domain and/or industry
                    if c["linkedin_url"]:
                        if c["domain"]:
                            lg.conn.execute("UPDATE contacts SET company_domain = ? WHERE company_domain IS NULL AND company_linkedin_url = ?", (c["domain"], c["linkedin_url"]))
                        if c["industry"] and not keywords:
                            lg.conn.execute("UPDATE contacts SET industry = ? WHERE industry IS NULL AND company_linkedin_url = ?", (c["industry"], c["linkedin_url"]))
                lg.conn.commit()
            fetched += len(results)
            cursor = data.get("cursor")
            lg.update_shard(provider, filters, fetched=fetched, cursor=cursor, status="running")
            with plock:
                progress["rows"] += len(results)
                progress["with_domain"] += sum(1 for c in comps if c["domain"])
                progress["pages"] += 1
                if progress["pages"] % 200 == 0:
                    log(f"  {provider}: {progress['rows']:,} companies / {progress['pages']} pages in {(time.time()-t0)/60:.1f} min")
            if not cursor or not results:
                break
        lg.update_shard(provider, filters, status="done", fetched=fetched, cursor=None)

    with ThreadPoolExecutor(max_workers=cfg["workers"]) as ex:
        futs = {ex.submit(run_shard, s): s for s in pending}
        for f in as_completed(futs):
            s = futs[f]
            try:
                f.result()
            except Exception as e:  # noqa: BLE001
                log(f"shard {s['filters']} failed: {e}")
                lg.update_shard(provider, s["filters"], status="error", note=str(e)[:200])
    if keywords:
        gated = [r[0] for r in lg.conn.execute(
            f"SELECT domain FROM companies WHERE industry IN ({','.join('?'*len(industries))})", industries).fetchall()]
        lg.set_keyword_fit(matched_domains, checked_domains=gated)
        log(f"keyword gate: {len(matched_domains):,} consulting-bucket companies match marketing keywords; {len(gated):,} gated companies checked")
    log(f"{provider} finished: {progress} in {(time.time()-t0)/60:.1f} min; summary {lg.shard_summary(provider)}; records used {bz.records_used:,}")


def cmd_apply_fit(ctx, args):
    lg = ctx.ledger
    gated = list(ctx.icp["fit"]["keyword_gated_industries"])
    kw = lg.shard_summary("blitz_companies_kw")
    if kw["n"] and kw["done"] == kw["n"]:
        # keyword sweep is complete: any gated company still unflagged did not match the keywords
        with lg.lock:
            cur = lg.conn.execute(
                f"UPDATE companies SET keyword_fit = 0 WHERE keyword_fit IS NULL AND industry IN ({','.join('?'*len(gated))})", gated)
            lg.conn.commit()
        log(f"keyword sweep complete; marked {cur.rowcount:,} further gated companies as not matching")
    else:
        log("WARNING: keyword sweep incomplete; gated companies without a flag stay 'unknown'")
    counts = lg.apply_fit(ctx.icp)
    reasons = lg.conn.execute("SELECT icp_fit, fit_reason, COUNT(*) FROM contacts WHERE title_check != 'fail' GROUP BY 1, 2 ORDER BY 3 DESC").fetchall()
    log(f"ICP fit over all contacts: {counts}")
    for r in reasons:
        print(f"  {r[0]:8s} {r[1]:40s} {r[2]:>9,}")
    for d in (args.check or []):
        r = lg.conn.execute("SELECT icp_fit, fit_reason, COUNT(*) FROM contacts WHERE company_domain = ? GROUP BY 1, 2", (d,)).fetchall()
        print(f"  check {d}: {[tuple(x) for x in r]}")


# ----------------------------------------------------------------------------- clay
def _clay_children(dims, filters):
    depth = len(filters)
    if depth >= len(dims):
        return []
    name, values = dims[depth]
    return [{**filters, name: v} for v in values]


def cmd_sweep_clay(ctx, args):
    icp, lg, cfg = ctx.icp, ctx.ledger, ctx.prov["clay"]
    cl = ctx.clay()
    mode = args.mode
    provider = f"clay_{mode}"
    dims = C.CLAY_PEOPLE_DIMS(icp) if mode == "people" else C.CLAY_COMPANY_DIMS(icp)
    initial_depth = 2 if mode == "people" else 1

    if not lg.pending_shards(provider) and not lg.shard_summary(provider)["n"]:
        seeds = [{}]
        for _ in range(initial_depth):
            seeds = [c for s in seeds for c in _clay_children(dims, s)]
        for s in seeds:
            lg.save_shard(provider, s, expected_total=None)
        log(f"seeded {len(seeds)} initial {mode} shards")

    stop = threading.Event()
    progress = {"rows": 0, "pages": 0, "inserted": 0, "merged": 0, "excluded": 0}
    plock = threading.Lock()
    t0 = time.time()

    def run_shard(shard):
        filters = shard["filters"]
        search_id, fetched = shard.get("cursor"), shard.get("fetched") or 0
        if not search_id:
            q = C.build_people_query(icp, filters) if mode == "people" else C.build_companies_query(icp, filters)
            search_id, _ = cl.create_search(q)
            lg.update_shard(provider, filters, cursor=search_id, status="running")
        reason = None
        while not stop.is_set():
            try:
                data = cl.run(search_id, cfg["page_size"])
            except C.QuotaExceeded as e:
                log(f"NOTICE: Clay quota exhausted; the Clay layer stops here and the run continues with the other providers ({str(e)[:80]})")
                _notice(lg, f"Clay: search quota exhausted during the {mode} sweep ({fetched:,} rows fetched in this shard). Rerun `run --force --stages clay merge domains consolidate-final export` after the quota resets.")
                stop.set()
                lg.update_shard(provider, filters, status="quota", fetched=fetched)
                return
            batch = data.get("data") or []
            if mode == "people":
                rows = _tag([C.parse_person(r, filters, icp) for r in batch])
                out = lg.upsert_many(rows)
            else:
                for r in batch:
                    lg.upsert_company(C.parse_company(r, icp), commit=False)
                lg.conn.commit()
                out = {"inserted": len(batch), "merged": 0, "excluded": 0}
            fetched += len(batch)
            lg.update_shard(provider, filters, fetched=fetched, status="running")
            with plock:
                progress["rows"] += len(batch)
                progress["pages"] += 1
                for k in ("inserted", "merged", "excluded"):
                    progress[k] += out.get(k, 0)
                if progress["pages"] % 20 == 0:
                    el = time.time() - t0
                    q = cl.last_quota or {}
                    log(f"  clay {mode}: {progress['rows']:,} rows / {progress['pages']} pages in {el/60:.1f} min; "
                        f"inserted={progress['inserted']:,} merged={progress['merged']:,}; quota remaining={q.get('remaining')}")
            q = cl.last_quota or {}
            if q.get("remaining") is not None and q["remaining"] < cfg["quota_reserve"] and mode == "people":
                log(f"NOTICE: Clay quota reserve reached ({q['remaining']:,} remaining, reserve {cfg['quota_reserve']:,}); the Clay people layer stops here and the run continues")
                _notice(lg, f"Clay: people sweep stopped at the quota reserve ({q['remaining']:,} results remaining, resets {str(q.get('resets_at'))[:10]}). The list is missing Clay's remaining contribution; rerun the clay stage after the reset.")
                stop.set()
            if not data.get("has_more"):
                reason = data.get("exhaustion_reason")
                break
        if stop.is_set() and reason is None:
            lg.update_shard(provider, filters, status="paused", fetched=fetched)
            return
        if reason == "query_limit":
            children = _clay_children(dims, filters)
            for c in children:
                lg.save_shard(provider, c, expected_total=None, note=f"split from {json.dumps(filters)}")
            lg.update_shard(provider, filters, status="done", fetched=fetched, note=f"query_limit -> {len(children)} children")
            log(f"  shard {filters} hit query_limit after {fetched} rows; split into {len(children)} children")
        else:
            lg.update_shard(provider, filters, status="done", fetched=fetched, cursor=None)

    while not stop.is_set():
        pending = [s for s in lg.pending_shards(provider) if s["status"] in ("pending", "running", "paused", "error")]
        if not pending:
            break
        with ThreadPoolExecutor(max_workers=cfg["workers"]) as ex:
            futs = {ex.submit(run_shard, s): s for s in pending}
            for f in as_completed(futs):
                s = futs[f]
                try:
                    f.result()
                except Exception as e:  # noqa: BLE001
                    log(f"clay shard {s['filters']} failed: {e}")
                    lg.update_shard(provider, s["filters"], status="error", note=str(e)[:200])
    el = time.time() - t0
    log(f"Clay {mode} sweep finished: {progress} in {el/60:.1f} min; summary {lg.shard_summary(provider)}; quota {cl.last_quota}")


# ----------------------------------------------------------------------------- merge
def cmd_merge_ledger(ctx, args):
    lg = ctx.ledger
    src = Ledger(args.src)
    out = {"inserted": 0, "merged": 0, "excluded": 0, "skipped": 0}
    batch = []
    for row in src.iter_contacts():
        row = dict(row)
        row["source"] = row.get("first_source") or "unknown"
        batch.append(row)
        if len(batch) >= 2000:
            r = lg.upsert_many(batch)
            for k in out:
                out[k] += r[k]
            batch = []
    if batch:
        r = lg.upsert_many(batch)
        for k in out:
            out[k] += r[k]
    n_comp = 0
    for c in src.conn.execute("SELECT domain, name, linkedin_url, country, industry, first_source FROM companies"):
        lg.upsert_company({"domain": c[0], "name": c[1], "linkedin_url": c[2], "country": c[3], "industry": c[4], "source": c[5]}, commit=False)
        n_comp += 1
    lg.conn.commit()
    for s in src.conn.execute("SELECT provider, filters, expected_total, fetched, status, note FROM shards"):
        f = json.loads(s[1])
        lg.save_shard(s[0], f, s[2], note=s[5])
        lg.update_shard(s[0], f, fetched=s[3], status=s[4])
    log(f"merged {args.src}: contacts {out}; companies {n_comp}; stats now {lg.stats()}")


# ----------------------------------------------------------------------------- join
def cmd_join_domains(ctx, args):
    lg = ctx.ledger
    conn = lg.conn
    before = conn.execute("SELECT COUNT(*) FROM contacts WHERE company_domain IS NULL").fetchone()[0]
    with lg.lock:
        conn.execute("""
            UPDATE contacts SET company_domain = (
                SELECT c.domain FROM companies c WHERE c.linkedin_url IS NOT NULL AND c.linkedin_url = contacts.company_linkedin_url LIMIT 1)
            WHERE company_domain IS NULL AND company_linkedin_url IS NOT NULL""")
        rows = conn.execute("SELECT key, company_name FROM contacts WHERE company_domain IS NULL AND company_name IS NOT NULL").fetchall()
        hits = 0
        for r in rows:
            d = lg.domain_for_company_name(r["company_name"])
            if d:
                conn.execute("UPDATE contacts SET company_domain = ? WHERE key = ?", (d, r["key"]))
                hits += 1
        conn.commit()
    mid = conn.execute("SELECT COUNT(*) FROM contacts WHERE company_domain IS NULL").fetchone()[0]
    log(f"domain join: {before:,} lacked a domain; {hits:,} matched by normalised name; {mid:,} still missing")

    if args.enrich:
        known_misses = set(lg.get_kv("enrich_misses", []))
        urls = [r[0] for r in conn.execute(
            "SELECT DISTINCT company_linkedin_url FROM contacts WHERE company_domain IS NULL AND company_linkedin_url IS NOT NULL").fetchall()]
        urls = [u for u in urls if u not in known_misses]
        if args.limit:
            urls = urls[: args.limit]
        log(f"Blitz company enrichment for {len(urls):,} company LinkedIn URLs (1 record each, flat plan; {len(known_misses):,} known misses skipped)")
        bz = ctx.blitz()
        resolved, misses, done, t0 = 0, [], 0, time.time()
        lock = threading.Lock()

        def one(u):
            resp = bz.http.request("POST", "/v2/enrichment/company", json={"company_linkedin_url": u})
            data = resp.get("company") or {}
            return u, normalize_domain(data.get("domain") or data.get("website")), data

        def flush_misses():
            lg.set_kv("enrich_misses", sorted(known_misses | set(misses)))

        with ThreadPoolExecutor(max_workers=10) as ex:
            for fut in as_completed([ex.submit(one, u) for u in urls]):
                done += 1
                try:
                    u, dom, data = fut.result()
                except Exception as e:  # noqa: BLE001
                    continue  # transient failure: retry on next run
                if dom:
                    # commit immediately so a killed run keeps its progress
                    lg.upsert_company({"domain": dom, "name": data.get("name"), "linkedin_url": u, "country": (data.get("hq") or {}).get("country_code"),
                                       "industry": data.get("industry"), "source": "blitz_enrich"}, commit=False)
                    with lg.lock:
                        conn.execute("UPDATE contacts SET company_domain = ? WHERE company_domain IS NULL AND company_linkedin_url = ?", (dom, u))
                        conn.commit()
                    resolved += 1
                else:
                    misses.append(u)
                if done % 500 == 0:
                    flush_misses()
                    log(f"  enrichment {done:,}/{len(urls):,} in {(time.time()-t0)/60:.1f} min; resolved {resolved:,}, no-website {len(misses):,}")
        flush_misses()
        after = conn.execute("SELECT COUNT(*) FROM contacts WHERE company_domain IS NULL").fetchone()[0]
        log(f"enrichment resolved {resolved:,} companies ({len(misses):,} have no website on record); {after:,} contacts still without domain")


# ----------------------------------------------------------------------------- discolike
def _known_key(lg, row):
    li = normalize_linkedin_url(row.get("linkedin_url"))
    return lg.get_contact(f"li:{li}") is not None if li else False


def cmd_estimate_discolike(ctx, args):
    """Exclusion is non-functional on DiscoLike, so this prices two honest options:
    BLIND  - pull the filtered bucket and pay for overlap (overlap measured on a random sample)
    THIN   - domain-targeted pulls at known companies where we hold <= N director-plus contacts
    """
    icp, lg, cfg = ctx.icp, ctx.ledger, ctx.prov["discolike"]
    dl = ctx.discolike()
    rate = cfg["cost_per_contact_usd"]
    usage0 = dl.usage()
    since = usage0["billing_events"][0]["created_at"] if usage0.get("billing_events") else ""
    floor = icp.get("discolike_employee_floor")
    est = {"rate": rate, "ts": now_iso(), "exclusion": "non-functional (verified); not used"}

    variants = {
        "A_floor": dict(employee_floor=floor, include_optional_industries=False),
        "B_nofloor": dict(employee_floor=None, include_optional_industries=False),
        "C_floor_plus_consulting": dict(employee_floor=floor, include_optional_industries=True),
    }
    est["variants"] = {}
    for name, kw in variants.items():
        n = dl.count(D.build_contact_params(icp, **kw))
        est["variants"][name] = {"count_total": n, "gross_cost_usd": round(n * rate, 2)}
        log(f"  {name}: {n:,} contacts, gross ${n*rate:,.2f}")

    # random-offset sample of the blind pull to measure overlap and revenue precision
    n_a = est["variants"]["A_floor"]["count_total"]
    params = D.build_contact_params(icp, **variants["A_floor"])
    sample_rows = []
    for _ in range(args.sample_pages):
        off = random.randint(0, max(0, min(10000, n_a - 20)))  # DiscoLike caps offset at 10,000
        recs, _ = dl.contacts(params, max_records=20, offset=off)
        sample_rows += [D.parse_contact(r) for r in recs]
    known = lg.known_domains()
    held = sum(1 for r in sample_rows if _known_key(lg, r))
    at_known = sum(1 for r in sample_rows if normalize_domain(r["company_domain"]) in known)
    qual = [D.revenue_qualifies(r["revenue_hint"], icp["revenue_min_usd"]) for r in sample_rows]
    n_s = len(sample_rows) or 1
    share_new_person = 1 - held / n_s
    share_new_company = 1 - at_known / n_s
    share_q = (qual.count(True) + 0.5 * qual.count(None)) / n_s
    est["blind_sample"] = {"rows": len(sample_rows), "already_held_person": held, "at_known_company": at_known,
                           "revenue_qualified": qual.count(True), "revenue_below": qual.count(False), "revenue_unknown": qual.count(None),
                           "share_net_new_person": round(share_new_person, 3), "share_net_new_company": round(share_new_company, 3),
                           "share_revenue_qualified_est": round(share_q, 3)}
    eff = rate / max(share_new_person * share_q, 1e-6)
    est["blind"] = {"variant": "A_floor", "count": n_a, "expected_net_new_qualified": int(n_a * share_new_person * share_q),
                    "effective_cost_per_net_new_qualified_usd": round(eff, 4), "gross_cost_full_pull_usd": round(n_a * rate, 2)}

    # THIN option: known companies where we hold <= thin_max contacts
    thin = [r[0] for r in lg.conn.execute(
        "SELECT company_domain FROM contacts WHERE company_domain IS NOT NULL GROUP BY company_domain HAVING COUNT(*) <= ?", (args.thin_max,)).fetchall()]
    random.shuffle(thin)
    batches = [thin[i:i + 40] for i in range(0, min(len(thin), 40 * args.thin_probe_batches), 40)]
    probed_domains, probed_contacts = 0, 0
    for b in batches:
        probed_contacts += dl.count(D.build_contact_params(icp, employee_floor=None, extra=[("domain", d) for d in b]))
        probed_domains += len(b)
    per_domain = probed_contacts / probed_domains if probed_domains else 0
    thin_total = int(per_domain * len(thin))
    est["thin"] = {"thin_max": args.thin_max, "thin_domains": len(thin), "probed_domains": probed_domains, "probed_contacts": probed_contacts,
                   "contacts_per_domain": round(per_domain, 3), "estimated_contacts": thin_total, "gross_cost_usd": round(thin_total * rate, 2),
                   "note": "people at these companies are almost all net-new persons (we hold <= thin_max there); revenue filter already satisfied by the free providers"}

    time.sleep(3)
    usage1 = dl.usage()
    cost, nb, cb = D.DiscoLikeClient.billing_since(usage1, since)
    lg.record_spend("discolike", "sample", units=nb, cost_usd=cost, note=f"estimate sample {len(sample_rows)} rows")
    est["sample_billed_usd"] = cost
    today = now_iso()[:10]
    est["account"] = {"billed_today_usd": D.DiscoLikeClient.billing_since(usage1, today)[0], **{k: usage1.get(k) for k in ("month_to_date_spend", "max_spend", "total_available_spend")}}
    lg.set_kv("discolike_estimate", est)
    (ctx.out / "discolike_estimate.json").write_text(json.dumps(est, indent=2), encoding="utf-8")

    print("\n================ DISCOLIKE ESTIMATE (nothing bulk-fetched yet) ================")
    for name, v in est["variants"].items():
        print(f"  {name:26s} total={v['count_total']:>9,}  gross=${v['gross_cost_usd']:,.2f}")
    print(f"BLIND sample: {est['blind_sample']}")
    print(f"BLIND: expected net-new qualified {est['blind']['expected_net_new_qualified']:,} of {n_a:,}; "
          f"effective ${eff:.4f} per net-new qualified contact; full pull ${n_a*rate:,.2f}")
    print(f"THIN : {est['thin']}")
    print(f"account: {est['account']}  | this estimate billed ${cost:.2f} | budget ceiling ${args.budget}")
    print("Approve with: fetch-discolike --mode blind|thin --cap-usd <amount>")


def _bill(dl, since):
    return D.DiscoLikeClient.billing_since(dl.usage(), since)


def cmd_fetch_discolike(ctx, args):
    icp, lg, cfg = ctx.icp, ctx.ledger, ctx.prov["discolike"]
    est = lg.get_kv("discolike_estimate")
    if not est:
        sys.exit("run estimate-discolike first")
    dl = ctx.discolike()
    rate = cfg["cost_per_contact_usd"]
    usage0 = dl.usage()
    since = usage0["billing_events"][0]["created_at"] if usage0.get("billing_events") else ""
    stats = {"received": 0, "inserted": 0, "merged": 0, "excluded": 0, "unqualified": 0, "no_linkedin": 0, "pages": 0}

    def ingest(recs):
        rows = []
        for rec in recs:
            row = D.parse_contact(rec)
            row["cost_usd"] = rate
            if not row["linkedin_url"]:
                stats["no_linkedin"] += 1
            # thin mode targets companies the free providers already revenue-qualified; only the blind pull post-filters
            if args.mode == "blind" and D.revenue_qualifies(row["revenue_hint"], icp["revenue_min_usd"]) is False:
                stats["unqualified"] += 1
                lg.add_paid_unqualified(f"persona:{row.get('persona_id')}", "discolike", rec, f"revenue {row['revenue_hint']}", rate)
                continue
            rows.append(row)
        out = lg.upsert_many(_tag(rows))
        stats["received"] += len(recs)
        stats["pages"] += 1
        for k in ("inserted", "merged", "excluded"):
            stats[k] += out[k]

    def over_cap():
        cost, nb, cb = _bill(dl, since)
        log(f"  billed so far ${cost:.2f} ({nb} contacts, {cb} companies) | {stats}")
        return cost >= args.cap_usd

    if args.mode == "blind":
        floor = icp.get("discolike_employee_floor") if "floor" in args.variant else None
        params = D.build_contact_params(icp, employee_floor=floor, include_optional_industries="consulting" in args.variant)
        # offset is capped at 10,000 by the API, so each (country x seniority) sub-filter yields at most 20k rows
        page = min(cfg["max_records"], max(20, int(args.cap_usd / rate) // 4))  # 4 checkpoints inside the cap
        done_subs = set(lg.get_kv("discolike_blind_done", []))
        stop_all = False
        for country in icp["company_hq_countries"]:
            for sen in icp["seniority_map"]["discolike"]:
                sub = f"{country}:{sen}"
                if sub in done_subs or stop_all:
                    continue
                sub_params = [(k, v) for k, v in params if k not in ("filter_country", "seniority")] + [("filter_country", country), ("seniority", sen)]
                offset = 0
                while offset <= 10000:
                    recs, _ = dl.contacts(sub_params, max_records=page, offset=offset)
                    if not recs:
                        break
                    ingest(recs)
                    offset += len(recs)
                    if over_cap():
                        stop_all = True
                        break
                    if len(recs) < page:
                        break
                done_subs.add(sub)
                lg.set_kv("discolike_blind_done", sorted(done_subs))
    else:  # thin
        done = set(lg.get_kv("discolike_thin_done", []))
        thin = [r[0] for r in lg.conn.execute(
            "SELECT company_domain FROM contacts WHERE company_domain IS NOT NULL GROUP BY company_domain HAVING COUNT(*) <= ?", (args.thin_max,)).fetchall()]
        thin = [d for d in thin if d not in done]
        bs = 80
        for i in range(0, len(thin), bs):
            batch = thin[i:i + bs]
            recs, _ = dl.contacts(D.build_contact_params(icp, employee_floor=None, extra=[("domain", d) for d in batch]), max_records=2000, offset=0)
            ingest(recs)
            done.update(batch)
            lg.set_kv("discolike_thin_done", sorted(done))
            if (i // bs) % 5 == 4 and over_cap():
                break
    cost, nb, cb = _bill(dl, since)
    if cost < args.cap_usd * 0.9:
        _notice(lg, f"DiscoLike: fetch ended at ${cost:.2f} of the ${args.cap_usd:.2f} cap (records exhausted or account balance/limit reached). Check the balance before rerunning `run --force --stages discolike-fetch fit consolidate-final export`.")
    lg.record_spend("discolike", "contacts", units=nb, cost_usd=cost, note=f"fetch mode={args.mode}")
    log(f"DiscoLike fetch done: billed ${cost:.2f} ({nb} contacts, {cb} companies) | {stats} | ledger spend ${lg.total_spend('discolike')}")


# ----------------------------------------------------------------------------- consolidate / export / report
def cmd_consolidate(ctx, args):
    icp, lg = ctx.icp, ctx.ledger
    conn = lg.conn
    refreshed = lg.refresh_alt_keys()
    log(f"refreshed {refreshed:,} name+domain keys after domain back-fill")
    purged = lg.purge_excluded()
    log(f"purged {purged:,} contacts that match exclusion seeds (LinkedIn key or first+last+domain)")
    collapsed = lg.dedupe_similar_slugs()
    log(f"collapsed {collapsed:,} same-person rows whose LinkedIn slugs differ only in form")
    with lg.lock:
        rows = conn.execute("SELECT key, job_title FROM contacts").fetchall()
        for r in rows:
            conn.execute("UPDATE contacts SET title_check = ? WHERE key = ?", (classify_title(r["job_title"]), r["key"]))
        conn.commit()
    geo = list(icp["person_countries"])
    q = conn.execute
    checks = {
        "total": lg.count_contacts(),
        "purged_as_excluded": purged,
        "collapsed_similar_slugs": collapsed,
        "title_pass": q("SELECT COUNT(*) FROM contacts WHERE title_check='pass'").fetchone()[0],
        "title_unknown": q("SELECT COUNT(*) FROM contacts WHERE title_check='unknown'").fetchone()[0],
        "title_fail_dropped": q("SELECT COUNT(*) FROM contacts WHERE title_check='fail'").fetchone()[0],
        "person_country_outside_geo": q(f"SELECT COUNT(*) FROM contacts WHERE person_country IS NOT NULL AND person_country NOT IN ({','.join('?'*len(geo))})", geo).fetchone()[0],
        "person_country_null": q("SELECT COUNT(*) FROM contacts WHERE person_country IS NULL").fetchone()[0],
        "missing_domain": q("SELECT COUNT(*) FROM contacts WHERE company_domain IS NULL").fetchone()[0],
        "missing_linkedin": q("SELECT COUNT(*) FROM contacts WHERE linkedin_url IS NULL").fetchone()[0],
        "distinct_keys": q("SELECT COUNT(DISTINCT key) FROM contacts").fetchone()[0],
        "by_source": lg.stats()["by_source"],
        "multi_source": q("SELECT COUNT(*) FROM contacts WHERE all_sources LIKE '%,%'").fetchone()[0],
    }
    lg.set_kv("consolidate", checks)
    print(json.dumps(checks, indent=2))
    sample = q("SELECT job_title FROM contacts WHERE title_check='pass' ORDER BY RANDOM() LIMIT 50").fetchall()
    print("50 random passing titles:", [s[0] for s in sample])
    sample = q("SELECT job_title FROM contacts WHERE title_check='fail' ORDER BY RANDOM() LIMIT 30").fetchall()
    print("30 random failing titles:", [s[0] for s in sample])


EXPORT_COLS = ["first_name", "last_name", "full_name", "job_title", "seniority", "company_name", "company_domain",
               "company_linkedin_url", "industry", "revenue_hint", "person_country", "company_country", "linkedin_url",
               "first_source", "all_sources", "title_check", "icp_fit", "fit_reason"]


def _write_chunks(ctx, where, suffix, chunk):
    lg = ctx.ledger
    n, idx, writer, fh = 0, 0, None, None
    stamp = datetime.now().strftime("%Y%m%d")
    for row in lg.iter_contacts(where):
        if n % chunk == 0:
            if fh:
                fh.close()
            idx += 1
            fh = (ctx.out / f"{ctx.icp['name']}_{stamp}{suffix}_part{idx:02d}.csv").open("w", encoding="utf-8", newline="")
            writer = csv.DictWriter(fh, fieldnames=EXPORT_COLS, extrasaction="ignore")
            writer.writeheader()
        writer.writerow(row)
        n += 1
    if fh:
        fh.close()
    return n, idx


def cmd_export(ctx, args):
    base = "title_check != 'fail'" if not args.include_failed else "1=1"
    if args.require_domain:
        base += " AND company_domain IS NOT NULL"
    has_fit = ctx.ledger.conn.execute("SELECT COUNT(*) FROM contacts WHERE icp_fit IS NOT NULL").fetchone()[0] > 0
    if has_fit:
        n, idx = _write_chunks(ctx, base + " AND icp_fit = 'fit'", "", args.chunk)
        log(f"exported {n:,} ICP-fit rows in {idx} file(s)")
        nc, idxc = _write_chunks(ctx, base + " AND icp_fit = 'candidate'", "_consulting_candidates", args.chunk)
        log(f"exported {nc:,} consulting-bucket rows with marketing keywords for review in {idxc} file(s) (suffix _consulting_candidates)")
        n2, idx2 = _write_chunks(ctx, base + " AND icp_fit = 'unknown'", "_unverified", args.chunk)
        log(f"exported {n2:,} rows whose company industry could not be verified in {idx2} file(s) (suffix _unverified)")
        n3 = ctx.ledger.conn.execute(f"SELECT COUNT(*) FROM contacts WHERE {base} AND icp_fit = 'unfit'").fetchone()[0]
        log(f"held back {n3:,} rows at companies outside the ICP (not exported)")
    else:
        n, idx = _write_chunks(ctx, base, "", args.chunk)
        log(f"exported {n:,} rows in {idx} file(s) to {ctx.out}")
    cmd_report(ctx, args)


def cmd_report(ctx, args):
    lg = ctx.ledger
    st = lg.stats()
    spend = {p: lg.total_spend(p) for p in ("blitz", "clay", "discolike")}
    by_src = st["by_source"]
    lines = [f"# Cost report {now_iso()}", "", f"Contacts: {st['contacts']:,}  Companies: {st['companies']:,}  Excluded seeds: {st['excluded']:,}",
             f"Contacts without domain: {st['contacts_without_domain']:,}", "", "| provider | net-new contacts (first source) | spend USD | USD per net-new |", "|---|---|---|---|"]
    for p in ("blitz", "clay", "discolike"):
        n = by_src.get(p, 0)
        lines.append(f"| {p} | {n:,} | {spend[p]:.2f} | {spend[p]/n if n else 0:.5f} |")
    lines.append(f"| total | {st['contacts']:,} | {sum(spend.values()):.2f} | {sum(spend.values())/st['contacts'] if st['contacts'] else 0:.5f} |")
    for prov in ("blitz", "clay_people", "clay_companies"):
        s = lg.shard_summary(prov)
        if s["n"]:
            lines.append(f"\n{prov} shards: {s}")
    txt = "\n".join(lines)
    (ctx.out / "cost_report.md").write_text(txt, encoding="utf-8")
    print(txt)


# ----------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(prog="listbuild")
    ap.add_argument("--icp", default=None, help="path to icp.yaml (default config/icp.yaml)")
    ap.add_argument("--ledger", default=None)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe")
    p = sub.add_parser("new-icp", help="write config/<name>.yaml from industries, countries, revenue floor and seniority")
    p.add_argument("--name", required=True); p.add_argument("--industries", nargs="+", required=True, help="LinkedIn/Clay industry labels")
    p.add_argument("--countries", nargs="+", required=True, help="ISO-2 HQ countries"); p.add_argument("--person-countries", nargs="*")
    p.add_argument("--revenue-min", type=int, default=0); p.add_argument("--seniority", default="director_plus", choices=["director_plus", "vp_plus", "manager_plus"])
    p.add_argument("--keywords", nargs="*", help="override marketing keywords for the catch-all candidates layer")
    p = sub.add_parser("preview", help="free sizing + sample contacts before the full run"); p.add_argument("--sample", type=int, default=60, help="Blitz sample rows in total (plus up to 20 Clay rows)")
    p.add_argument("--seeds", nargs="*", default=[], help="prior-contact CSVs; sample rows already prospected are flagged")
    p = sub.add_parser("run", help="full pipeline, resumable"); p.add_argument("--seeds", nargs="*", default=[], help="prior-contact CSVs to exclude")
    p.add_argument("--discolike-cap-usd", type=float, default=0.0, help="0 = estimate only, no paid pull"); p.add_argument("--skip-clay", action="store_true")
    p.add_argument("--stages", nargs="*", help="run only these stages"); p.add_argument("--force", action="store_true", help="re-run stages already marked done")
    p = sub.add_parser("seed"); p.add_argument("--csv", nargs="+", required=True); p.add_argument("--origin")
    p = sub.add_parser("sweep-blitz"); p.add_argument("--only-country"); p.add_argument("--plan-only", action="store_true"); p.add_argument("--replan", action="store_true")
    p = sub.add_parser("sweep-clay"); p.add_argument("--mode", choices=["people", "companies"], default="people")
    p = sub.add_parser("sweep-blitz-companies"); p.add_argument("--keywords", action="store_true"); p.add_argument("--replan", action="store_true")
    p = sub.add_parser("apply-fit"); p.add_argument("--check", nargs="*")
    p = sub.add_parser("merge-ledger"); p.add_argument("--src", required=True)
    p = sub.add_parser("join-domains"); p.add_argument("--enrich", action="store_true"); p.add_argument("--limit", type=int)
    p = sub.add_parser("estimate-discolike"); p.add_argument("--budget", type=float, default=250.0); p.add_argument("--sample-pages", type=int, default=2)
    p.add_argument("--thin-max", type=int, default=1); p.add_argument("--thin-probe-batches", type=int, default=25)
    p = sub.add_parser("fetch-discolike"); p.add_argument("--cap-usd", type=float, required=True); p.add_argument("--mode", choices=["blind", "thin"], default="thin")
    p.add_argument("--variant", default="A_floor"); p.add_argument("--thin-max", type=int, default=1)
    sub.add_parser("consolidate")
    p = sub.add_parser("export"); p.add_argument("--chunk", type=int, default=50000); p.add_argument("--include-failed", action="store_true"); p.add_argument("--require-domain", action="store_true")
    sub.add_parser("report")
    args = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    from . import orchestrate
    if args.cmd == "new-icp":          # no config exists yet
        return orchestrate.cmd_new_icp(None, args)
    ctx = Ctx(args)
    {"probe": cmd_probe, "seed": cmd_seed, "sweep-blitz": cmd_sweep_blitz, "sweep-clay": cmd_sweep_clay, "merge-ledger": cmd_merge_ledger,
     "new-icp": orchestrate.cmd_new_icp, "preview": orchestrate.cmd_preview, "run": orchestrate.cmd_run,
     "sweep-blitz-companies": cmd_sweep_blitz_companies, "apply-fit": cmd_apply_fit,
     "join-domains": cmd_join_domains, "estimate-discolike": cmd_estimate_discolike, "fetch-discolike": cmd_fetch_discolike,
     "consolidate": cmd_consolidate, "export": cmd_export, "report": cmd_report}[args.cmd](ctx, args)


if __name__ == "__main__":
    main()
