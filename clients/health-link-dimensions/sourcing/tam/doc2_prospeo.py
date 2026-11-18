"""Doc 2 cross-check: Prospeo POST /search-company and /search-person totals (pagination.total_count, page 1 only = 1 credit each).
Writes 2026-11-18-doc-2-prospeo.json."""
import json
from prospeo_probe import post
US = {"include": ["United States #US"]}
SZ = ["201-500", "501-1000", "1001-2000", "2001-5000", "5001-10000", "10000+"]
PH_IND = ["Pharmaceutical Manufacturing", "Biotechnology Research"]
DEV_IND = ["Medical Equipment Manufacturing"]
DEV_SZ = ["51-100", "101-200", "201-500", "501-1000", "1001-2000", "2001-5000", "5001-10000"]
Q = {
 "co_pharma_industry_201plus": ("search-company", {"company_industry": {"include": PH_IND}, "company_headcount_range": SZ, "company_location_search": US}),
 "co_pharma_naics_201plus": ("search-company", {"company_naics": {"include": ["325412", "325414", "325411", "325413"]}, "company_headcount_range": SZ, "company_location_search": US}),
 "co_device_51_10000": ("search-company", {"company_industry": {"include": DEV_IND}, "company_headcount_range": DEV_SZ, "company_location_search": US}),
 "co_device_10000plus": ("search-company", {"company_industry": {"include": DEV_IND}, "company_headcount_range": ["10000+"], "company_location_search": US}),
}
PERS = {
 "c1_brand_marketing": ["Brand Director", "Brand Manager", "Brand Lead", "Head of Marketing", "VP Marketing", "Marketing Director", "Franchise Head", "Chief Marketing Officer"],
 "c2_media_omni": ["Omnichannel", "Customer Engagement", "HCP Marketing", "Digital Marketing", "Marketing Operations", "Multichannel"],
 "c3_commops_field": ["Commercial Operations", "Sales Operations", "Commercial Excellence", "CRM", "Sales Force Effectiveness", "National Sales Director", "VP Sales"],
 "c4_data_analytics": ["Commercial Analytics", "Insights", "Data Strategy", "Marketing Analytics", "Chief Data Officer", "Data Science"],
 "c5_market_access": ["Market Access", "Payer", "Managed Markets", "National Accounts", "Trade Relations", "Access Analytics"],
}
for k, t in PERS.items():
    Q[f"people_{k}"] = ("search-person", {"person_job_title": {"include": t}, "person_seniority": {"include": ["C-Suite", "Vice President", "Director", "Manager", "Head"]},
                        "person_location_search": US, "company_industry": {"include": PH_IND}, "company_headcount_range": SZ})
out = {}
for k, (path, f) in Q.items():
    r = post(path, {"page": 1, "filters": f})
    out[k] = {"path": path, "filters": f, "total_count": (r.get("pagination") or {}).get("total_count"), "error": r.get("error_code") or (r if r.get("error") else None),
              "sample": [((x.get("company") or {}).get("name"), (x.get("person") or {}).get("current_job_title")) for x in (r.get("results") or [])[:5]]}
    print(k, out[k]["total_count"], out[k]["error"] or "", out[k]["sample"][:3], flush=True)
json.dump(out, open("2026-11-18-doc-2-prospeo.json", "w"), indent=1)
