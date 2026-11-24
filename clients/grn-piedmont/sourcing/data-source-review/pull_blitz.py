"""Blitz API POST /v2/search/companies: full pull of both review slices (see common.py).
MFG labels (68) are sent in two halves (Blitz caps industry.include at 50). Pages of 25 until cursor is null.
Output: raw/blitz-<slice>.json  (1 Blitz record per company returned)."""
import json, os
from common import *
K = {"x-api-key": os.environ["BLITZ_API_KEY"]}
os.makedirs(os.path.join(HERE, "raw"), exist_ok=True)

def pull(company, tag):
    rows, cur, total = [], None, None
    while True:
        st, r = http("POST", "https://api.blitz-api.ai/v2/search/companies", K,
                     {"company": company, "max_results": 25, "cursor": cur})
        if st != 200: print(tag, st, r); break
        total = r.get("total_results"); rows += r.get("results") or []
        cur = r.get("cursor")
        if not cur: break
    print(tag, "total_results", total, "pulled", len(rows), flush=True)
    return {"body": company, "total_results": total, "results": rows}

out = {}
for i, half in enumerate((MFG[:35], MFG[35:])):
    out[f"mfg-h{i}"] = pull({"industry": {"include": half}, "employee_range": SIZES,
                             "hq": {"country_code": ["US"], "state": {"include": MFG_STATES}}}, f"mfg-h{i}")
json.dump(out, open(os.path.join(HERE, "raw", "blitz-mfg.json"), "w"))
fls = {"fls-kw": pull({"industry": {"include": FLS_IND}, "keywords": {"include": FLS_KW}, "employee_range": SIZES,
                       "hq": {"country_code": ["US"], "state": {"exclude": NON_ET_CT}}}, "fls-kw"),
       "fls-label": pull({"industry": {"include": ["Fire Protection"]}, "employee_range": SIZES,
                          "hq": {"country_code": ["US"], "state": {"exclude": NON_ET_CT}}}, "fls-label"),
       "fls-kw-anyind": pull({"keywords": {"include": FLS_KW}, "employee_range": SIZES,
                              "hq": {"country_code": ["US"], "state": {"exclude": NON_ET_CT}}}, "fls-kw-anyind")}
json.dump(fls, open(os.path.join(HERE, "raw", "blitz-fls.json"), "w"))
