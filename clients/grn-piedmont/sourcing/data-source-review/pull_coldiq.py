"""ColdIQ POST /v1/companies/search, provider pinned to "ai-ark-companies" (AI Ark's company DB at ColdIQ's
price). Approved by Moe 2026-11-24, cap 100 credits. Output: raw/coldiq.json (+ credits before/after)."""
import json, os
from common import *
K = {"Authorization": "Bearer " + os.environ["COLDIQ_API_KEY"]}
bal = lambda: http("GET", "https://api.coldiq.com/v1/me/credits", K)[1]["balance"]
b0 = bal()
import sys

def run(inp, tag, pages=12, limit=100):
    rows = []
    for p in range(pages):
        st, r = http("POST", "https://api.coldiq.com/v1/companies/search", K,
                     {"input": dict(inp, limit=limit, page=p), "provider": "ai-ark-companies"})
        if st != 200: print(tag, st, str(r)[:400]); break
        got = ((r.get("data") or {}).get("companies")) or []
        rows += got
        if p == 0: print(tag, "meta", {k: v for k, v in r.items() if k != "data"}, flush=True)
        if len(got) < limit: break
        if b0 - bal() > 95: print("cap reached"); break
    print(tag, "pulled", len(rows), flush=True)
    return {"input": inp, "results": rows}

if not os.environ.get("COLDIQ_PASS2"):
  out = {"mfg": run({"industries": ["manufacturing"], "industries_mode": "SMART", "countries": ["US"],
                   "locations": MFG_STATES, "min_employees": 201, "max_employees": 1000}, "mfg"),
         "fls-kw": run({"keywords": FLS_KW, "keyword_mode": "WORD", "countries": ["US"], "locations": ET_CT_STATES,
                      "min_employees": 201, "max_employees": 1000}, "fls-kw")}
  out["credits_spent"] = b0 - bal()
  print("credits spent", out["credits_spent"])
  json.dump(out, open(os.path.join(HERE, "raw", "coldiq.json"), "w"))

# --- Second pass (same day). The first MFG pass ignored geography: `countries` + bare state names in
# `locations` returned US-wide companies (California top). `locations` as "<State>, United States" with no
# `countries` constrains HQ correctly (1-page test: 25/25 NC/SC). The FLS pass returned 98 < limit, so it is
# the exhaustive US-wide keyword set and is filtered to ET/CT client-side instead of re-pulled.
# Budget left under Moe's 100-credit cap allows 3 pages (300 rows) of the corrected MFG query.
if __name__ == "__main__" and os.environ.get("COLDIQ_PASS2"):
    b1 = bal()
    out = json.load(open(os.path.join(HERE, "raw", "coldiq.json")))
    out["mfg-v2"] = run({"industries": ["manufacturing"], "industries_mode": "SMART",
                         "locations": [f"{s}, United States" for s in MFG_STATES],
                         "min_employees": 201, "max_employees": 1000}, "mfg-v2", pages=3)
    out["credits_spent_pass2"] = b1 - bal()
    print("pass2 credits", out["credits_spent_pass2"])
    json.dump(out, open(os.path.join(HERE, "raw", "coldiq.json"), "w"))
