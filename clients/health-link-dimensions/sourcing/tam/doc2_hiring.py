"""Doc 2 sizing step 3: hiring pool. Distinct companies with a matching US job posted in the last 30 / 90 days.
Blitz POST /v2/company/tam-by-jobs (1 record per company returned), paged to the end, cap 450 records per run.
tam-by-jobs has no name filter, so DNC/clients/noise names are removed from the returned rows afterwards (dnc.py matcher).
Writes 2026-11-18-doc-2-hiring.json."""
import json
from doc2_common import *
out, used = {}, 0
for camp, titles in JOB_TITLES.items():
    ind, sizes = (DEVICE_IND, DEVICE_SIZES_C7) if camp == "c7_device" else (PHARMA_IND, PHARMA_SIZES)
    for d in (30, 90):
        body = {"job": {"title": {"include": titles, "exclude": JOB_EXCL}, "location": {"country_code": {"include": ["US"]}},
                        "date_posted": {"last_days": d}}, "company": jobs_company(ind, sizes), "max_results": 50}
        rows, cursor, n = [], None, 0
        while n < 450:
            b = dict(body, cursor=cursor) if cursor else body
            r = call("/v2/company/tam-by-jobs", b); u = r.get("fair_usage", {}).get("records_used", 0); used += u; n += u
            if r.get("_error"): print("ERR", r.get("_body")); break
            for x in r.get("results", []):
                c = x.get("company") or x
                rows.append({"name": c.get("name"), "linkedin_url": c.get("linkedin_url"), "size": c.get("size"),
                             "matched_jobs": x.get("matched_jobs_count") or x.get("jobs_count") or x.get("count")})
            cursor = r.get("cursor")
            if not cursor: break
        out[f"{camp}/{d}d"] = {"body": body, "companies": len(rows), "capped": bool(cursor), "rows": rows}
        print(camp, d, len(rows), "capped" if cursor else "", "used", used, flush=True)
out["records_used"] = used
json.dump(out, open("2026-11-18-doc-2-hiring.json", "w"), indent=1)
