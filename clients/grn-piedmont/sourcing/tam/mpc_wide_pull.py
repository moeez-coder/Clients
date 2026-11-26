"""MPC company expansion for GRN Piedmont (2026-11-26, Moe: "We need to expand the companies aswell ... around 1000 atleast",
then "add 51 - 5000"). Same pull as mpc_segments_pull.py (same 68 MFG labels in 10 verticals, same title chunks, same
120-day window, US HQ outside Mountain/Pacific/AK/HI, is_agency false, FULL_TIME, same noise/DNC gates and one-family-per-
posting rule), but for the two NEW size bands only: 51-200 and 1001-5000. 201-1000 was pulled on 2026-11-24, so the bands
are disjoint and nothing here re-pulls a company already covered. F&LS is not pulled (folded into 730732).

Blitz API POST /v2/jobs/search, cursor-paged at 50. Raw pages go to $RAW (scratchpad, not committed). Writes
2026-11-26-mpc-wide-jobs.csv and 2026-11-26-mpc-wide-pull.json (request bodies, first-page totals, records used).
Resumable via .done markers.  Usage: RAW=/path python3 mpc_wide_pull.py
"""
import csv, json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "recruitment-specific-open-roles"))
from tam_counts import jobs_body, post
from mpc_segments_pull import VERT, CHUNKS, family, norm
from spec import TITLE_NOISE, COMPANY_NOISE, DNC

RAW = os.environ["RAW"]; os.makedirs(RAW, exist_ok=True)
DATE = "2026-11-26"; DAYS = 120; BANDS = ["51-200", "1001-5000"]
LOG = os.path.join(HERE, f"{DATE}-mpc-wide-pull.json")

if __name__ == "__main__":
    log = json.load(open(LOG)) if os.path.exists(LOG) else {"queries": {}, "records_used": 0}
    for band in BANDS:
        for g, labels in VERT.items():
            for ci, titles in enumerate(CHUNKS):
                key = f"{band}/{g}/chunk{ci}"; out = os.path.join(RAW, key.replace("/", "__") + ".jsonl")
                if os.path.exists(out + ".done"): continue
                b = jobs_body(titles, DAYS, labels, sizes=[band]); b["max_results"] = 50; cur = None; n = 0; tot = None
                with open(out, "w") as f:
                    while True:
                        b["cursor"] = cur; r = post("/v2/jobs/search", b)
                        if r.get("_error"): raise SystemExit(f"{key}: {r}")
                        if tot is None: tot = r.get("total_results")
                        log["records_used"] += (r.get("fair_usage") or {}).get("records_used", 0)
                        for x in r.get("results") or []: f.write(json.dumps({**x, "_vertical": g, "_band": band}) + "\n"); n += 1
                        cur = r.get("cursor")
                        if not cur or not r.get("results"): break
                b.pop("cursor", None)
                log["queries"][key] = {"total_results_first_page": tot, "pulled": n, "body": b}
                open(out + ".done", "w").write(str(n)); print(key, tot, n, flush=True)
                json.dump(log, open(LOG, "w"), indent=1)

    rows, seen = [], {}
    for p in sorted(os.listdir(RAW)):
        if not p.endswith(".jsonl"): continue
        for line in open(os.path.join(RAW, p)):
            x = json.loads(line); t = (x.get("title") or "").strip(); c = x.get("company_name") or ""
            u = norm(x.get("company_linkedin_url")); why = "kept"
            if not u or "/company/" not in u: why = "removed: no company LinkedIn page"
            elif DNC.search(c): why = "removed: client DNC list"
            elif COMPANY_NOISE.search(c): why = "removed: company outside ICP (name)"
            elif TITLE_NOISE.search(t): why = "removed: title not a placed role"
            k = (x.get("url") or "") or (u, t.lower(), (x.get("date_posted") or "")[:10])
            k2 = (u, t.lower(), (x.get("date_posted") or "")[:10])
            if k in seen or k2 in seen: continue
            seen[k] = seen[k2] = 1
            loc = x.get("location") or {}
            rows.append({"size_band": x["_band"], "segment_vertical": x["_vertical"], "role_family": family(t), "title": t or "-",
                         "company_name": c or "-", "company_linkedin_url": u or "-",
                         "job_city": (loc.get("city") if isinstance(loc, dict) else None) or "-",
                         "date_posted": (x.get("date_posted") or "-")[:10], "job_url": x.get("url") or "-",
                         "jd_summary": re.sub(r"\s+", " ", x.get("ai_summary") or "-"), "status": why})
    rows.sort(key=lambda r: r["date_posted"]); first = {}
    for r in rows:
        if r["status"] != "kept": continue
        k = (r["company_linkedin_url"], r["title"].lower())
        if k in first: r["status"] = f"removed: repost (first seen {first[k]})"
        else: first[k] = r["date_posted"]
    with open(os.path.join(HERE, f"{DATE}-mpc-wide-jobs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(len(rows), "postings;", collections.Counter(r["status"].split(" (")[0] for r in rows).most_common())
    print("records used:", log["records_used"])
