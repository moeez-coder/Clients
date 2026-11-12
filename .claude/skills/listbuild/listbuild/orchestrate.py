"""Teammate-facing commands: new-icp (config from four inputs), preview (free sizing + sample), run (whole pipeline)."""
import argparse
import csv
import json
import math
import time
from datetime import datetime

import yaml

from . import pipeline as P
from .config import WORKSPACE
from .icp_gen import build_icp
from .http import HttpError
from .providers import blitz as B
from .providers import clay as C
from .providers import discolike as D
from .seniority import classify_title
from .seeds import load_seed_keys, is_seeded
from .icp_gen import RELATED_LABELS

log = P.log


def _cli():
    """How to invoke the CLI in the user's shell: the skill launcher if we were started through it, else the module."""
    import os
    launcher = os.environ.get("LISTBUILD_LAUNCHER")
    return f'python "{launcher}"' if launcher else "python -m listbuild"


# ----------------------------------------------------------------------------- new-icp
def cmd_new_icp(ctx, args):
    cfg = build_icp(name=args.name, industries=args.industries, countries=args.countries, revenue_min_usd=args.revenue_min,
                    seniority=args.seniority, person_countries=args.person_countries or None, keywords=args.keywords)
    notes = cfg.pop("_mapping_notes")
    path = WORKSPACE / "config" / f"{args.name}.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"wrote {path}")
    print(f"  Clay industries     : {cfg['industries']['clay']}")
    print(f"  Blitz industries    : {cfg['industries']['blitz']}")
    print(f"  DiscoLike buckets   : {cfg['industries']['discolike'] or 'none maps to these industries -> DiscoLike cannot run for this ICP; tell the requester'}")
    print(f"  Core (main list)    : {cfg['fit']['core_industries']}")
    if notes["catch_all_labels"]:
        print(f"  Catch-all labels    : {notes['catch_all_labels']} -> exported as *_consulting_candidates, never in the main list")
    if notes["unmapped_labels"]:
        print(f"  WARNING unmapped    : {notes['unmapped_labels']} (used verbatim on Clay/Blitz; check spelling against LinkedIn labels)")
    related = [r for l in args.industries for r in RELATED_LABELS.get(l, []) if r not in args.industries]
    if related:
        print(f"  Related labels you may want to add: {related}")
    print(f"next: {_cli()} --icp {path.relative_to(WORKSPACE).as_posix()} preview [--seeds prior.csv ...]")


# ----------------------------------------------------------------------------- preview
def cmd_preview(ctx, args):
    icp, out = ctx.icp, ctx.out
    bz = ctx.blitz()
    ki = bz.key_info()
    lines = [f"# Preview: {icp['name']}  ({datetime.now():%Y-%m-%d %H:%M})", ""]
    # --- Blitz sizing (1 record per count). Main list = core industries only; catch-all labels are a separate candidates layer.
    core_labels = [i for i in icp["industries"]["blitz"] if i in icp.get("fit", {}).get("core_industries", icp["industries"]["blitz"])]
    core_icp = {**icp, "industries": {**icp["industries"], "blitz": core_labels or icp["industries"]["blitz"]}}
    total_all = bz.count(icp, {})
    total_core = bz.count(core_icp, {}) if core_labels and core_labels != icp["industries"]["blitz"] else total_all
    per_country = {c: bz.count(core_icp, {"country": c}) for c in icp["company_hq_countries"]}
    lines += [f"Blitz (free, plan {[p.get('name') for p in ki.get('active_plans', [])]}, {ki.get('records_remaining'):,} records left this cycle):",
              f"  main-list contacts (core industries {core_labels}): ~{total_core:,}  by HQ country: " + ", ".join(f"{c} {n:,}" for c, n in per_country.items()),
              (f"  plus ~{total_all - total_core:,} in catch-all industries -> candidates file" if total_all != total_core else ""),
              f"  estimated sweep time: ~{max(2, total_all / 600 / 60):.0f} min"]
    # --- Blitz sample
    n_countries = max(1, len(icp["company_hq_countries"]))
    per = max(5, math.ceil(args.sample / n_countries))   # --sample = Blitz rows in total, spread over HQ countries
    sample = []
    for c in icp["company_hq_countries"]:
        page = bz.search_people(B.build_people_body(core_icp, {"country": c}, page_size=min(50, per)))
        for r in page.get("results", []):
            row = B.parse_person(r, {"country": c})
            row["title_check"] = classify_title(row["job_title"])
            row["source"] = "blitz"
            sample.append(row)
    # --- Clay
    try:
        cl = ctx.clay()
        sid, _ = cl.create_search(C.build_people_query(icp, {}))
        run = cl.run(sid, 50)
        q = run.get("period_quota") or {}
        lines.append(f"Clay (free): first page returned {len(run.get('data') or [])} rows; quota remaining {q.get('remaining'):,} of {q.get('limit'):,} (resets {q.get('resets_at', '?')[:10]})")
        if q.get("remaining") is not None and q["remaining"] < total_all:
            lines.append(f"  WARNING: the Clay layer needs roughly {total_all:,} results but only {q['remaining']:,} remain. The run will still "
                         f"attempt Clay, stop when the quota runs out, and continue with the other providers. Tell the requester before starting.")
        for r in (run.get("data") or [])[:20]:
            row = C.parse_person(r, {}, icp)
            row["title_check"] = classify_title(row["job_title"])
            sample.append(row)
    except C.QuotaExceeded as e:
        lines.append(f"Clay: WARNING quota exhausted right now ({str(e)[:100]}). The run will still attempt Clay, report the stop, "
                     f"and continue with the other providers. Tell the requester before starting.")
    except HttpError as e:
        lines.append(f"Clay: error {e.status}; the Clay stage may fail ({str(e)[:120]})")
    # --- DiscoLike
    if icp["industries"].get("discolike"):
        dl = ctx.discolike()
        usage = dl.usage()
        rate = ctx.prov["discolike"]["cost_per_contact_usd"]
        n = dl.count(D.build_contact_params(icp, employee_floor=icp.get("discolike_employee_floor")))
        avail = (usage.get("total_available_spend") or 0) - (usage.get("month_to_date_spend") or 0)
        bal = f"~${avail:,.0f}" if avail >= 0 else f"WARNING overdrawn by ${-avail:,.0f} (any paid pull will fail until topped up; tell the requester)"
        lines.append(f"DiscoLike (paid, ${rate}/contact): ~{n:,} contacts in bucket {icp['industries']['discolike']} = ${n*rate:,.0f} gross; "
                     f"~60% net-new after the free layers. Balance left on account: {bal}. Paid pull only happens with --discolike-cap-usd.")
    else:
        lines.append("DiscoLike: no bucket maps to these industries -> stage skipped")
    # --- fit notes
    gated = icp.get("fit", {}).get("keyword_gated_industries") or []
    if gated:
        lines.append(f"Catch-all industries {gated}: exported separately as *_consulting_candidates (keyword gate is ~30% precise), never in the main list")
    # --- prior-list overlap on the sample
    seeded = 0
    if args.seeds:
        li, alt = load_seed_keys(args.seeds)
        for r in sample:
            r["in_prior_list"] = is_seeded(r, li, alt)
            seeded += r["in_prior_list"]
        lines.append(f"Prior lists ({len(args.seeds)} file(s), {len(li):,} LinkedIn URLs): {seeded} of {len(sample)} sampled contacts already prospected; the run excludes them")
    # --- write sample
    cols = ["source", "full_name", "job_title", "title_check", "in_prior_list", "company_name", "company_domain", "person_country", "company_country", "linkedin_url"]
    path = out / "preview.csv"
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in sample:
            w.writerow(r)
    lines = [l for l in lines if l]
    print("\n".join(lines))
    n_b = sum(1 for r in sample if r["source"] == "blitz")
    print(f"\nSample of {len(sample)} contacts ({n_b} Blitz + {len(sample) - n_b} Clay) written to {path}. First 25:")
    for r in sample[:25]:
        flag = "" if r["title_check"] == "pass" else f"  [{r['title_check']}]"
        if r.get("in_prior_list"):
            flag += "  [already prospected]"
        print(f"  {str(r.get('full_name'))[:24]:24} | {str(r.get('job_title'))[:34]:34} | {str(r.get('company_name'))[:28]:28} | {str(r.get('company_domain'))[:24]:24} | {r.get('person_country')}{flag}")
    fails = sum(1 for r in sample if r["title_check"] == "fail")
    cfg_path = ctx.args.icp or "config/icp.yaml"
    seeds_hint = " ".join(f'"{x}"' for x in args.seeds) if args.seeds else "<prior_lists.csv ...>"
    print(f"\ntitle guard would drop {fails} of {len(sample)} sampled rows. Adjust {cfg_path} and re-run preview, or start the build:")
    print(f"  {_cli()} --icp {cfg_path} run --seeds {seeds_hint} --discolike-cap-usd 0")
    (out / "preview.md").write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------------------------- run
def _preflight(ctx, args):
    """Report every provider's quota/balance before starting. Nothing is disabled here: the run always attempts all
    providers and reports if one stops early."""
    icp = ctx.icp
    print("=== pre-flight: provider quotas and balances (all providers will be attempted) ===")
    try:
        ki = ctx.blitz().key_info()
        print(f"  Blitz    : {ki.get('records_remaining'):,} records left this cycle")
    except Exception as e:  # noqa: BLE001
        print(f"  Blitz    : WARNING key check failed ({str(e)[:100]})")
    if args.skip_clay:
        print("  Clay     : skipped by --skip-clay (requester's choice)")
    else:
        try:
            cl = ctx.clay()
            sid, _ = cl.create_search(C.build_people_query(icp, {"location_country": icp["person_countries"][0]}))
            run = cl.run(sid, 1)
            q = run.get("period_quota") or {}
            msg = f"  Clay     : {q.get('remaining'):,} results left of {q.get('limit'):,} (resets {str(q.get('resets_at'))[:10]})"
            if q.get("remaining") is not None and q["remaining"] < ctx.prov["clay"]["quota_reserve"]:
                msg += "  WARNING: below the reserve; the Clay layer will stop early and the run will continue without it"
            print(msg)
        except C.QuotaExceeded:
            print("  Clay     : WARNING quota exhausted; the Clay layer will stop immediately and the run will continue without it")
        except Exception as e:  # noqa: BLE001
            print(f"  Clay     : WARNING check failed ({str(e)[:100]}); the run will still attempt it")
    if icp["industries"].get("discolike"):
        try:
            u = ctx.discolike().usage()
            left = (u.get("total_available_spend") or 0) - (u.get("month_to_date_spend") or 0)
            msg = f"  DiscoLike: ${left:,.0f} left to spend; cap for this run ${args.discolike_cap_usd:,.0f}"
            if left < 0:
                msg += f"  WARNING: account overdrawn by ${-left:,.0f}; no paid pull is possible until it is topped up"
            elif args.discolike_cap_usd > left:
                msg += "  WARNING: cap exceeds the balance; the paid pull will stop when the balance runs out"
            print(msg)
        except Exception as e:  # noqa: BLE001
            print(f"  DiscoLike: WARNING check failed ({str(e)[:100]})")
    else:
        print("  DiscoLike: no bucket for these industries")
    print("")


def _ns(**kw):
    return argparse.Namespace(**kw)


def cmd_run(ctx, args):
    """Whole pipeline in cost order. Every stage is idempotent/resumable; completed stages are skipped unless --force."""
    lg = ctx.ledger
    done = set(lg.get_kv("run_done", []))
    want = set(args.stages) if args.stages else None
    side = ctx.out / "ledger_clay.sqlite"
    has_disco = bool(ctx.icp["industries"].get("discolike"))

    stages = [
        ("seed", lambda: P.cmd_seed(ctx, _ns(csv=args.seeds, origin=None)) if args.seeds else log("no --seeds given; nothing excluded up front")),
        ("blitz", lambda: P.cmd_sweep_blitz(ctx, _ns(only_country=None, plan_only=False, replan=False))),
        ("clay", lambda: log("Clay skipped (--skip-clay)") if args.skip_clay else P.cmd_sweep_clay(ctx.with_ledger(side), _ns(mode="people"))),
        ("merge", lambda: P.cmd_merge_ledger(ctx, _ns(src=str(side))) if side.exists() else log("no Clay ledger to merge")),
        ("companies", lambda: P.cmd_sweep_blitz_companies(ctx, _ns(keywords=False, replan=False))),
        ("companies-kw", lambda: P.cmd_sweep_blitz_companies(ctx, _ns(keywords=True, replan=False)) if ctx.icp["fit"]["keyword_gated_industries"] else log("no catch-all industries; keyword sweep skipped")),
        ("domains", lambda: P.cmd_join_domains(ctx, _ns(enrich=True, limit=None))),
        ("consolidate", lambda: P.cmd_consolidate(ctx, _ns())),
        ("discolike-estimate", lambda: P.cmd_estimate_discolike(ctx, _ns(budget=args.discolike_cap_usd or 0, sample_pages=2, thin_max=1, thin_probe_batches=0)) if has_disco else log("DiscoLike skipped: no bucket")),
        ("discolike-fetch", lambda: P.cmd_fetch_discolike(ctx, _ns(cap_usd=args.discolike_cap_usd, mode="blind", variant="A_floor", thin_max=1)) if (has_disco and args.discolike_cap_usd > 0) else log("DiscoLike paid pull skipped (cap 0)")),
        ("fit", lambda: P.cmd_apply_fit(ctx, _ns(check=[]))),
        ("consolidate-final", lambda: P.cmd_consolidate(ctx, _ns())),
        ("export", lambda: P.cmd_export(ctx, _ns(chunk=50000, include_failed=False, require_domain=False))),
    ]
    t0 = time.time()
    lg.set_kv("run_notices", [])
    _preflight(ctx, args)
    for name, fn in stages:
        if want and name not in want:
            continue
        if name in done and not args.force and name not in ("export", "consolidate-final", "fit"):
            log(f"=== {name}: already done, skipping (use --force to redo)")
            continue
        log(f"=== stage {name} ===")
        try:
            fn()
        except C.QuotaExceeded as e:
            log(f"stage {name}: Clay quota exhausted, continuing without it ({str(e)[:100]})")
        done.add(name)
        lg.set_kv("run_done", sorted(done))
    notices = lg.get_kv("run_notices", [])
    log(f"run finished in {(time.time()-t0)/60:.1f} min; outputs in {ctx.out}")
    if notices:
        print("\n=== PROVIDER LIMITS HIT DURING THIS RUN (tell the requester) ===")
        for n in notices:
            print(f"  - {n}")
        print("Rerun the affected stages once the limit clears, e.g. `run --force --stages clay merge domains consolidate-final export`.")
    else:
        print("\nNo provider limits were hit; all layers ran in full.")
