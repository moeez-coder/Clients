"""Doc 2 sizing step 1: company + people + job-posting counts (Blitz, max_results: 1 per count).
Writes 2026-11-18-doc-2-blitz-counts.json. Pre-DNC = no client/DNC name exclusion; post-DNC = EXCL_PHARMA / EXCL_DEVICE names excluded."""
import json
from doc2_common import *

out, used = {"companies": {}, "people": {}, "jobs": {}, "samples": {}}, 0
def go(key, path, body, bucket):
    global used
    r = call(path, body); used += r.get("fair_usage", {}).get("records_used", 0)
    bucket[key] = {"body": body, "total_results": r.get("total_results"), "error": r.get("_body")}
    print(key, r.get("total_results"), r.get("_body") or "", flush=True)
    return r

C = out["companies"]
go("pharma_raw_no_excl", "/v2/search/companies", {"company": pharma_co(False, False), "max_results": 1}, C)
go("pharma_kw_excl_pre_dnc", "/v2/search/companies", {"company": pharma_co(False, True), "max_results": 1}, C)
go("pharma_post_dnc", "/v2/search/companies", {"company": pharma_co(True, True), "max_results": 1}, C)
for s in PHARMA_SIZES:
    go(f"pharma_post_dnc_{s}", "/v2/search/companies", {"company": pharma_co(True, True, [s]), "max_results": 1}, C)
go("pharma_dnc_hits", "/v2/search/companies", {"company": dict(pharma_co(False, True), name={"include": EXCL_PHARMA}), "max_results": 50}, C)
go("device_c7_pre_dnc", "/v2/search/companies", {"company": device_co(False), "max_results": 1}, C)
go("device_c7_post_dnc", "/v2/search/companies", {"company": device_co(True), "max_results": 1}, C)
go("device_large_10001", "/v2/search/companies", {"company": device_co(False, ["10001+"]), "max_results": 1}, C)

# fit samples (20 rows each)
r = call("/v2/search/companies", {"company": pharma_co(True, True), "max_results": 20}); used += r["fair_usage"]["records_used"]
out["samples"]["pharma"] = r.get("results", [])
r = call("/v2/search/companies", {"company": device_co(True), "max_results": 20}); used += r["fair_usage"]["records_used"]
out["samples"]["device"] = r.get("results", [])
r = out["companies"]  # keep dnc hit names
P = out["people"]
for camp, cells in PHARMA_CELLS.items():
    for lv, (inc, exc) in cells.items():
        go(f"{camp}/{lv}/pre_dnc", "/v2/search/people", people_body(pharma_co(False, True), inc, exc, LV[lv]), P)
        go(f"{camp}/{lv}/post_dnc", "/v2/search/people", people_body(pharma_co(True, True), inc, exc, LV[lv]), P)
for lv, (inc, exc) in DEVICE_CELLS.items():
    go(f"c7_device/{lv}/pre_dnc", "/v2/search/people", people_body(device_co(False), inc, exc, LV[lv]), P)
    go(f"c7_device/{lv}/post_dnc", "/v2/search/people", people_body(device_co(True), inc, exc, LV[lv]), P)

J = out["jobs"]
for camp, titles in JOB_TITLES.items():
    ind, sizes = (DEVICE_IND, DEVICE_SIZES_C7) if camp == "c7_device" else (PHARMA_IND, PHARMA_SIZES)
    for d in (30, 90):
        b = {"job": {"title": {"include": titles, "exclude": JOB_EXCL}, "location": {"country_code": {"include": ["US"]}},
                     "date_posted": {"last_days": d}}, "company": jobs_company(ind, sizes), "max_results": 1}
        go(f"{camp}/{d}d", "/v2/jobs/search", b, J)
out["records_used"] = used; print("records_used", used)
json.dump(out, open("2026-11-18-doc-2-blitz-counts.json", "w"), indent=1)
