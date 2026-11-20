"""TAM/SAM count read for We Are DNA campaign doc 1 (2026-11-12).

Counts only: every call uses max_results=1 and reads total_results. No full pull (doc not yet approved).
  - companies: POST /v2/search/companies  (segment firmographics, UK HQ, two size bands)
  - open jobs: POST /v2/jobs/search       (hook roles posted in the UK, last 30 and 90 days, same firmographics)
Method copied from clients/health-link-dimensions/sourcing/tam/tam_counts.py (branch
claude/health-link-dimensions-doc-1-clean). Industry labels are exact Blitz enum values from
docs/blitz-api/company-search-industries.txt on origin/claude/stoic-hypatia-yxvmmu.
The open role is a SIGNAL of talent-attraction pressure (We Are DNA is an employer-brand agency, not a recruiter),
so hook roles are the volume / hard-to-fill roles each sector struggles to fill.
Output: tam_counts.json next to this script.  Usage: python3 tam_counts.py
"""
import json, os, urllib.request, urllib.error, time

H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
SIZE_51 = ["51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"]
SIZE_201 = SIZE_51[1:]
EXCL = ["Intern", "Internship", "Work Experience", "Volunteer", "Recruitment Consultant", "Recruiter"]

SEGMENTS = {
    "1-health-care-medical": dict(
        industries=["Hospitals and Health Care", "Hospital and Health Care", "Hospitals", "Home Health Care Services",
                    "Nursing Homes and Residential Care Facilities", "Mental Health Care", "Medical Practices",
                    "Medical Practice", "Outpatient Care Centers", "Veterinary", "Veterinary Services",
                    "Ambulance Services", "Individual and Family Services"],
        roles=["Care Assistant", "Support Worker", "Healthcare Assistant", "Care Worker", "Nurse", "Registered Nurse",
               "Veterinary Surgeon", "Veterinary Nurse", "Vet", "Dental Nurse", "Dentist", "Paramedic", "Call Handler",
               "Clinician", "Pharmacist", "Care Home Manager", "Deputy Manager"]),
    "2-retail-hospitality": dict(
        industries=["Retail", "Retail Apparel and Fashion", "Retail Groceries", "Retail Health and Personal Care Products",
                    "Retail Luxury Goods and Jewelry", "Retail Furniture and Home Furnishings", "Online and Mail Order Retail",
                    "Apparel and Fashion", "Hospitality", "Restaurants", "Hotels and Motels", "Food and Beverage Services",
                    "Leisure; Travel and Tourism"],
        roles=["Store Manager", "Assistant Store Manager", "Assistant Manager", "Sales Assistant", "Retail Assistant",
               "Customer Assistant", "Sales Advisor", "Chef", "Sous Chef", "Head Chef", "Restaurant Manager",
               "General Manager", "Team Leader", "Supervisor", "Kitchen Porter", "Bartender", "Front of House"]),
    "3-manufacturing-engineering-automotive-defence": dict(
        industries=["Manufacturing", "Industrial Machinery Manufacturing", "Machinery Manufacturing", "Automotive",
                    "Motor Vehicle Manufacturing", "Motor Vehicle Parts Manufacturing", "Defense and Space Manufacturing",
                    "Defense and Space", "Aviation and Aerospace Component Manufacturing", "Engineering Services",
                    "Mechanical Or Industrial Engineering", "Food and Beverage Manufacturing", "Food Production",
                    "Meat Products Manufacturing", "Electrical Equipment Manufacturing", "Chemical Manufacturing"],
        roles=["Maintenance Engineer", "Engineer", "Technician", "Service Technician", "Mechanic", "HGV Technician",
               "Electrician", "Fitter", "Welder", "Machinist", "CNC", "Production Operative", "Operative",
               "Production Manager", "Shift Manager", "Quality Engineer", "Design Engineer"]),
    "4-law-accounting-top100": dict(
        industries=["Law Practice", "Legal Services", "Accounting"],
        roles=["Solicitor", "Associate Solicitor", "Trainee Solicitor", "Paralegal", "Legal Secretary", "Lawyer",
               "Accountant", "Audit", "Auditor", "Tax", "Trainee Accountant", "Chartered Accountant", "ACA", "ACCA",
               "Audit Manager", "Tax Manager", "Payroll"]),
    "5-financial-services": dict(
        industries=["Financial Services", "Banking", "Insurance", "Insurance Carriers", "Investment Management",
                    "Credit Intermediation", "Capital Markets"],
        roles=["Financial Adviser", "Financial Advisor", "Mortgage Adviser", "Mortgage Advisor", "Paraplanner",
               "Underwriter", "Claims Handler", "Customer Service Advisor", "Relationship Manager", "Compliance",
               "Risk Analyst", "Analyst", "Collections", "Software Engineer", "Data Analyst", "Actuarial"]),
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


def ru(*rs): return sum((r.get("fair_usage") or {}).get("records_used", 0) for r in rs)


out = {}
for slug, s in SEGMENTS.items():
    row = {"errors": []}
    resps = []
    for band, sizes in (("51plus", SIZE_51), ("201plus", SIZE_201)):
        cbody = {"company": {"industry": {"include": s["industries"]}, "employee_range": sizes, "hq": {"country_code": ["GB"]}}, "max_results": 1}
        c = post("/v2/search/companies", cbody); resps.append(c)
        row[f"companies_{band}"] = c.get("total_results", c.get("_error"))
        row[f"companies_{band}_body"] = cbody
        row[f"companies_{band}_sample"] = [x.get("name") for x in c.get("results", [])]
        if c.get("_body"): row["errors"].append(c["_body"])
    for days in (30, 90):
        jbody = {"job": {"title": {"include": s["roles"], "exclude": EXCL}, "location": {"country_code": {"include": ["GB"]}},
                         "date_posted": {"last_days": days}},
                 "company": {"is_agency": False, "industry": {"include": s["industries"]}, "size": {"include": SIZE_51},
                             "hq": {"country_code": {"include": ["GB"]}}}, "max_results": 1}
        j = post("/v2/jobs/search", jbody); resps.append(j)
        row[f"jobs_{days}d"] = j.get("total_results", j.get("_error"))
        row[f"jobs_{days}d_body"] = jbody
        row[f"jobs_{days}d_sample"] = [(x.get("title"), x.get("company_name")) for x in j.get("results", [])]
        if j.get("_body"): row["errors"].append(j["_body"])
    row["records_used"] = ru(*resps)
    out[slug] = row
    print(slug, row["companies_51plus"], row["companies_201plus"], row["jobs_30d"], row["jobs_90d"], row["errors"], row["jobs_30d_sample"], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tam_counts.json"), "w"), indent=1)
