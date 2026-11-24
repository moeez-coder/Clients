"""Step 1 of the Recruitment Specific pull (GRN Piedmont, 2026-11-16): every matching job posting, last 120 days.

Blitz API POST /v2/jobs/search, cursor-paged at 50, same filters as ../tam/tam_counts.py with last_days=120.
Manufacturing industries are sent as two halves (50-label cap). Output: raw/jobs-<family>.jsonl + raw/usage.json.
Resumable: a family with a .done marker is skipped.  Usage: python3 pull_jobs.py
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tam"))
from tam_counts import ROLES, FLS_ROLES, MFG, FLS_IND, FLS_KW, jobs_body, post

HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw"); DAYS = 120
fams = {k: (v, MFG, None) for k, v in ROLES.items()}
fams["fire-life-safety"] = (FLS_ROLES, FLS_IND, FLS_KW)
usage = json.load(open(os.path.join(RAW, "usage.json"))) if os.path.exists(os.path.join(RAW, "usage.json")) else {}
bodies = {}
for fam, (titles, inds, kw) in fams.items():
    out = os.path.join(RAW, f"jobs-{fam}.jsonl")
    b = jobs_body(titles, DAYS, inds, kw); b["max_results"] = 50; bodies[fam] = b
    if os.path.exists(out + ".done"): continue
    n = 0
    with open(out, "w") as f:
        for half in ([inds] if len(inds) <= 50 else [inds[:35], inds[35:]]):
            bb = json.loads(json.dumps(b)); bb["company"]["industry"]["include"] = half; cur = None
            while True:
                bb["cursor"] = cur
                r = post("/v2/jobs/search", bb)
                if r.get("_error"): raise SystemExit(f"{fam}: {r}")
                usage["/v2/jobs/search"] = usage.get("/v2/jobs/search", 0) + (r.get("fair_usage") or {}).get("records_used", 0)
                for x in r.get("results") or []: f.write(json.dumps(x) + "\n"); n += 1
                cur = r.get("cursor")
                if not cur or not r.get("results"): break
    open(out + ".done", "w").write(str(n)); print(fam, n, flush=True)
    json.dump(usage, open(os.path.join(RAW, "usage.json"), "w"))
json.dump(bodies, open(os.path.join(HERE, "jobs_request_bodies.json"), "w"), indent=1)
print(usage)
