"""Prospeo API POST /search-company: full pull of both review slices. 1 credit per page of 25 (plan credits).
Industry labels: the 68 Blitz MFG labels (';' -> ','); labels Prospeo rejects are dropped and logged.
Output: raw/prospeo.json"""
import json, os, re
from common import *
K = {"X-KEY": os.environ["PROSPEO_API_KEY"]}
U = "https://api.prospeo.io/search-company"

def run(filters, tag, max_pages=60):
    rows, page, total, dropped = [], 1, None, []
    while page <= max_pages:
        st, r = http("POST", U, K, {"filters": filters, "page": page})
        if "_error" in r:
            try: r = json.loads(r["_error"])
            except Exception: pass
        if r.get("error"):
            fe = r.get("filter_error") or ""
            m = re.search(r"Invalid industry\(s\) in include list: \[(.*)\]", fe)
            if m and page == 1:
                bad = re.findall(r"'([^']+)'", m.group(1))
                dropped += bad
                filters["company_industry"]["include"] = [i for i in filters["company_industry"]["include"] if i not in bad]
                continue
            print(tag, "error", st, r); break
        rows += r.get("results") or []
        pg = r.get("pagination") or {}; total = pg.get("total_count")
        if page >= (pg.get("total_page") or 0): break
        page += 1
    print(tag, "total_count", total, "pulled", len(rows), "dropped labels", dropped, flush=True)
    return {"filters": filters, "total_count": total, "dropped_labels": dropped, "results": rows}

out = {}
out["mfg"] = run({"company_industry": {"include": [m.replace(";", ",") for m in MFG]},
                  "company_location_search": {"include": [f"{s}, United States" for s in MFG_STATES]},
                  "company_headcount_range": ["201-500", "501-1000"]}, "mfg")
out_fls = None
if False: run({"company_keywords": {"include": FLS_KW},
                     "company_location_search": {"include": [f"{s}, United States" for s in ET_CT_STATES]},
                     "company_headcount_range": ["201-500", "501-1000"]}, "fls-kw")
old = json.load(open(os.path.join(HERE, "raw", "prospeo.json")))
out["fls-kw"] = old["fls-kw"]  # pulled in the first run (449 rows, 18 credits); not re-pulled
json.dump(out, open(os.path.join(HERE, "raw", "prospeo.json"), "w"))
