"""TAM/SAM count read for Health Link Dimensions campaign doc 1 (2026-11-09).

Counts only: every call uses max_results=1 and reads total_results. No full pull.
  - companies: POST /v2/search/companies   (segment firmographics, US HQ)
  - open jobs: POST /v2/jobs/search        (MPC hook roles, US, posted last 30 days, same firmographics)
Industry labels are exact Blitz enum values (docs/blitz-api/company-search-industries.txt on
origin/claude/stoic-hypatia-yxvmmu). Output: tam_counts.json next to this script.
Usage: python3 tam_counts.py
"""
import json, os, urllib.request, urllib.error, time

H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
PHARMA = ["Pharmaceutical Manufacturing", "Pharmaceuticals", "Biotechnology Research", "Biotechnology"]
DEVICE = ["Medical Equipment Manufacturing", "Medical Device"]
AGENCY = ["Advertising Services", "Marketing and Advertising", "Marketing Services"]
HEALTH_KW = ["healthcare", "pharma", "pharmaceutical", "life sciences", "HCP", "medical"]

COMMERCIAL_ROLES = ["Commercial Operations", "Omnichannel", "Marketing Analytics", "Commercial Analytics",
                    "Marketing Operations", "CRM", "Customer Engagement", "Brand Manager", "Brand Director",
                    "Multichannel", "HCP Marketing", "Digital Marketing"]
LAUNCH_ROLES = COMMERCIAL_ROLES + ["Commercial Lead", "Head of Commercial", "Launch", "Market Access",
                                   "Sales Operations", "Sales Force Effectiveness", "Key Account Manager"]
DEVICE_ROLES = ["Marketing Operations", "CRM", "Product Marketing", "Marketing Analytics", "Commercial Operations",
                "Sales Operations", "Digital Marketing", "Professional Education", "Marketing Manager"]
AGENCY_ROLES = ["Programmatic", "Media Planner", "Media Director", "Media Supervisor", "Media Strategy",
                "Data Strategy", "HCP", "Audience", "Media Buyer", "Activation"]
EXCL = ["Intern", "Internship", "Warehouse"]

SEGMENTS = {
    "1-specialty-pharma-commercial-biotech": dict(industries=PHARMA, sizes=["201-500", "501-1000", "1001-5000"], roles=COMMERCIAL_ROLES),
    "2-prelaunch-newly-launched-biotech": dict(industries=PHARMA, sizes=["11-50", "51-200"], roles=LAUNCH_ROLES),
    "3-specialist-med-device": dict(industries=DEVICE, sizes=["51-200", "201-500", "501-1000", "1001-5000", "5001-10000"], roles=DEVICE_ROLES),
    "4-large-pharma": dict(industries=PHARMA, sizes=["5001-10000", "10001+"], roles=COMMERCIAL_ROLES),
    "5-hcp-agencies": dict(industries=AGENCY, sizes=["11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"], roles=AGENCY_ROLES, keywords=HEALTH_KW),
}


def post(path, body):
    for a in range(6):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai" + path, json.dumps(body).encode(), H, method="POST")
            return json.load(urllib.request.urlopen(r, timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"_error": e.code, "_body": e.read()[:400].decode(errors="replace")}
    return {"_error": "retries"}


out = {}
for slug, s in SEGMENTS.items():
    comp = {"industry": {"include": s["industries"]}, "employee_range": s["sizes"], "hq": {"country_code": ["US"]}}
    if s.get("keywords"): comp["keywords"] = {"include": s["keywords"]}
    cbody = {"company": comp, "max_results": 1}
    c = post("/v2/search/companies", cbody)
    jcomp = {"is_agency": False, "industry": {"include": s["industries"]}, "size": {"include": s["sizes"]},
             "hq": {"country_code": {"include": ["US"]}}}
    if slug.startswith("5-"): jcomp.pop("is_agency")  # agencies ARE the target here
    jbody = {"job": {"title": {"include": s["roles"], "exclude": EXCL}, "location": {"country_code": {"include": ["US"]}},
                     "date_posted": {"last_days": 30}}, "company": jcomp, "max_results": 1}
    j = post("/v2/jobs/search", jbody)
    out[slug] = {"companies_total": c.get("total_results", c.get("_error")), "companies_body": cbody,
                 "companies_sample": [x.get("name") for x in c.get("results", [])],
                 "jobs_total_30d": j.get("total_results", j.get("_error")), "jobs_body": jbody,
                 "jobs_sample": [(x.get("title"), x.get("company_name")) for x in j.get("results", [])],
                 "records_used": (c.get("fair_usage") or {}).get("records_used", 0) + (j.get("fair_usage") or {}).get("records_used", 0),
                 "errors": [x for x in (c.get("_body"), j.get("_body")) if x]}
    print(slug, out[slug]["companies_total"], out[slug]["jobs_total_30d"], out[slug]["errors"], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tam_counts.json"), "w"), indent=1)
