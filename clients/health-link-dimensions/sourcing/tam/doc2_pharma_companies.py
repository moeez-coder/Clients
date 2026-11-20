"""Doc 2 step 5: distinct companies with at least one persona person (all 3 levels), pharma campaigns 1-5 and device 7.
Blitz POST /v2/company/tam-by-people, post-DNC company filter, paged, cap 900 records per persona. 1 record per company.
Writes 2026-11-18-doc-2-pharma-companies.json (name, linkedin_url, size, matched_people)."""
import json
from doc2_common import *
out, used = {}, 0
jobs = {k: v for k, v in PHARMA_CELLS.items()}
jobs["c7_device"] = DEVICE_CELLS
for camp, cells in jobs.items():
    comp = device_co(True) if camp == "c7_device" else pharma_co(True, True)
    inc = sorted({t for lv in cells for t in cells[lv][0]})
    exc = cells["decision_makers"][1]
    rows, cursor, n = [], None, 0
    while n < 900:
        b = {"company": comp, "people": {"job_title": {"include": inc, "exclude": exc}, "job_level": ["C-Team", "VP", "Director", "Manager"],
             "location": {"country_code": ["US"]}}, "max_results": 50}
        if cursor: b["cursor"] = cursor
        r = call("/v2/company/tam-by-people", b); u = r.get("fair_usage", {}).get("records_used", 0); used += u; n += u
        if r.get("_error"): print("ERR", r.get("_body")); break
        for x in r.get("results", []):
            c = x.get("company") or {}
            rows.append({"name": c.get("name"), "linkedin_url": c.get("linkedin_url"), "size": c.get("size"), "matched_people": x.get("matched_people")})
        cursor = r.get("cursor")
        if not cursor: break
    b.pop("cursor", None)
    out[camp] = {"body": b, "companies": len(rows), "capped": bool(cursor), "rows": rows}
    print(camp, len(rows), "capped" if cursor else "", "used", used, flush=True)
out["records_used"] = used
json.dump(out, open("2026-11-18-doc-2-pharma-companies.json", "w"), indent=1)
