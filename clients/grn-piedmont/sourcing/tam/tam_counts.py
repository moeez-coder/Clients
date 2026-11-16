"""TAM/SAM count read for the GRN Piedmont open-role (MPC) campaign doc (2026-11-16).

Counts only: every call uses max_results=1 and reads total_results (1 Blitz record per call).
  - companies: POST /v2/search/companies  (firmographics, US HQ, Eastern/Central states)
  - open jobs: POST /v2/jobs/search       (role-family titles, US job location, posted last 30 / 90 / 120 days (120 = the campaign window, set by Moe 2026-11-16))
Industry labels are exact values from the Blitz /v2/jobs/search OpenAPI enum (read 2026-11-16 via the
Blitz-API docs MCP). Title matching is keyword-based (all words of a phrase, whole words, any order).
Output: tam_counts.json next to this script.  Usage: python3 tam_counts.py
"""
import json, os, time, urllib.request, urllib.error

H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json", "User-Agent": "curl/8.5.0"}

# Mountain + Pacific + AK/HI HQ states are excluded (client: Eastern and Central time zones only).
NON_ET_CT = ["Montana", "Idaho", "Wyoming", "Utah", "Colorado", "Arizona", "New Mexico", "Nevada",
             "Washington", "Oregon", "California", "Alaska", "Hawaii"]
SIZES = ["201-500", "501-1000"]

MFG = """Abrasives and Nonmetallic Minerals Manufacturing|Agricultural Chemical Manufacturing|Agriculture; Construction; Mining Machinery Manufacturing|Animal Feed Manufacturing|Appliances; Electrical; and Electronics Manufacturing|Architectural and Structural Metal Manufacturing|Artificial Rubber and Synthetic Fiber Manufacturing|Automation Machinery Manufacturing|Aviation and Aerospace Component Manufacturing|Baked Goods Manufacturing|Beverage Manufacturing|Boilers; Tanks; and Shipping Container Manufacturing|Building Materials|Chemical Manufacturing|Chemical Raw Materials Manufacturing|Chemicals|Clay and Refractory Products Manufacturing|Commercial and Service Industry Machinery Manufacturing|Construction Hardware Manufacturing|Cutlery and Handtool Manufacturing|Dairy Product Manufacturing|Defense and Space Manufacturing|Electrical and Electronic Manufacturing|Electrical Equipment Manufacturing|Electric Lighting Equipment Manufacturing|Engines and Power Transmission Equipment Manufacturing|Fabricated Metal Products|Food and Beverage Manufacturing|Food Production|Fruit and Vegetable Preserves Manufacturing|Furniture and Home Furnishings Manufacturing|Glass; Ceramics and Concrete Manufacturing|Glass Product Manufacturing|Household and Institutional Furniture Manufacturing|Household Appliance Manufacturing|HVAC and Refrigeration Equipment Manufacturing|Industrial Automation|Industrial Machinery Manufacturing|Lime and Gypsum Products Manufacturing|Machinery|Machinery Manufacturing|Manufacturing|Measuring and Control Instrument Manufacturing|Meat Products Manufacturing|Mechanical Or Industrial Engineering|Metal Valve; Ball; and Roller Manufacturing|Metalworking Machinery Manufacturing|Motor Vehicle Manufacturing|Motor Vehicle Parts Manufacturing|Office Furniture and Fixtures Manufacturing|Packaging and Containers|Packaging and Containers Manufacturing|Paint; Coating; and Adhesive Manufacturing|Paper and Forest Product Manufacturing|Paper and Forest Products|Plastics|Plastics and Rubber Product Manufacturing|Plastics Manufacturing|Primary Metal Manufacturing|Railroad Equipment Manufacturing|Railroad Manufacture|Rubber Products Manufacturing|Soap and Cleaning Product Manufacturing|Spring and Wire Product Manufacturing|Textile Manufacturing|Transportation Equipment Manufacturing|Turned Products and Fastener Manufacturing|Wood Product Manufacturing""".split("|")

# Fire & life safety companies sit under contractor / security labels, so the label list is wide and
# a company keyword gate does the real work.
FLS_IND = ["Fire Protection", "Construction", "Building Equipment Contractors", "Specialty Trade Contractors",
           "Security Systems Services", "Facilities Services", "Building Construction",
           "Nonresidential Building Construction"]
FLS_KW = ["fire protection", "fire sprinkler", "fire alarm", "fire suppression", "life safety"]

# "Automotive" (legacy label) is left out of MFG: it is mostly car dealerships. Motor Vehicle (Parts) Manufacturing stay in.
EXCL = ["Intern", "Internship", "Assistant", "Sales", "Store", "Restaurant", "Account", "Trainee", "Shift",
        "Software", "Analyst", "Technician", "Clearance", "Dealership"]


def heads(fams, hs=("Director", "VP", "Vice President", "Head")):
    return [f"{h} {f}" for f in fams for h in hs]


ROLES = {
    "operations-plant-leadership": ["Plant Manager", "General Manager", "Operations Manager", "Production Manager",
                                    "Manufacturing Manager", "Maintenance Manager",
                                    "Continuous Improvement Manager", "Chief Operating Officer", "COO"]
                                   + heads(["Operations", "Manufacturing", "Production"]),
    "engineering-quality": ["Engineering Manager", "Quality Manager", "Chief Engineer", "Manufacturing Engineering Manager",
                            "Process Engineering Manager", "Quality Assurance Manager"]
                           + heads(["Engineering", "Quality"]),
    "supply-chain-purchasing": ["Supply Chain Manager", "Purchasing Manager", "Procurement Manager", "Materials Manager",
                                "Sourcing Manager"]
                               + heads(["Supply Chain", "Purchasing", "Procurement", "Materials"]),
    "executive-finance-hr": ["Chief Executive Officer", "CEO", "Chief Financial Officer", "CFO", "Corporate Controller", "Plant Controller", "[Controller]",
                             "Human Resources Director", "HR Director", "Chief Human Resources Officer", "CHRO",
                             "VP Finance", "Vice President Finance", "VP Human Resources",
                             "Vice President Human Resources", "Director Finance"],
}
ALL_MFG_ROLES = sorted({r for v in ROLES.values() for r in v})  # 50 max per include list -> split below
FLS_ROLES = ["Branch Manager", "General Manager", "Operations Manager", "Service Manager", "Project Manager",
             "Design Manager", "Engineering Manager", "Inspection Manager", "Construction Manager",
             "Regional Manager", "District Manager", "Chief Operating Officer", "Chief Financial Officer",
             "Area Manager"] + heads(["Operations", "Engineering", "Service", "Construction"])


def post(path, body):
    for a in range(6):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai" + path, json.dumps(body).encode(), H, method="POST")
            return json.load(urllib.request.urlopen(r, timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"_error": e.code, "_body": e.read()[:400].decode(errors="replace")}
    return {"_error": "retries"}


def jobs_body(titles, days, industries, keywords=None, et_ct=True, sizes=SIZES):
    comp = {"is_agency": False, "industry": {"include": industries}, "size": {"include": sizes},
            "hq": {"country_code": {"include": ["US"]}}}
    if et_ct: comp["hq"]["state"] = {"exclude": NON_ET_CT}
    if keywords: comp["keywords"] = {"include": keywords}
    return {"job": {"title": {"include": titles, "exclude": EXCL}, "location": {"country_code": {"include": ["US"]}},
                    "date_posted": {"last_days": days}, "employment_type": {"include": ["FULL_TIME"]}},
            "company": comp, "max_results": 1}


def comp_body(industries, keywords=None, et_ct=True, sizes=SIZES):
    c = {"industry": {"include": industries}, "employee_range": sizes, "hq": {"country_code": ["US"]}}
    if et_ct: c["hq"]["state"] = {"exclude": NON_ET_CT}
    if keywords: c["keywords"] = {"include": keywords}
    return {"company": c, "max_results": 1}


out, used = {}, 0


def run(key, path, body):
    """Blitz caps industry.include at 50 labels. MFG has 69, so a body carrying MFG is sent as two
    disjoint halves and the totals are summed (a company has one industry label, so no double count)."""
    global used
    ind = body["company"]["industry"]["include"]
    if len(ind) > 50:
        parts = []
        for half in (ind[:35], ind[35:]):
            b = json.loads(json.dumps(body)); b["company"]["industry"]["include"] = half
            r = post(path, b); used += (r.get("fair_usage") or {}).get("records_used", 0); parts.append(r)
        tot = [p.get("total_results", p.get("_error")) for p in parts]
        res = [x for p in parts for x in (p.get("results") or [])]
        out[key] = {"path": path, "total_results": sum(tot) if all(isinstance(t, int) for t in tot) else tot,
                    "split_totals": tot, "body": body,
                    "sample": [{k: x.get(k) for k in ("name", "title", "company_name", "date_posted", "url") if x.get(k)} for x in res],
                    "error": [p.get("_body") for p in parts if p.get("_body")] or None}
        print(key, out[key]["total_results"], tot, out[key]["error"] or "", flush=True)
        return
    r = post(path, body)
    used += (r.get("fair_usage") or {}).get("records_used", 0)
    res = r.get("results") or []
    out[key] = {"path": path, "total_results": r.get("total_results", r.get("_error")), "body": body,
                "sample": [{k: x.get(k) for k in ("name", "title", "company_name", "date_posted", "url") if x.get(k)} for x in res],
                "error": r.get("_body")}
    print(key, out[key]["total_results"], out[key]["error"] or "", flush=True)


if __name__ == "__main__":
    run("mfg/companies/et-ct", "/v2/search/companies", comp_body(MFG))
    run("mfg/companies/all-us", "/v2/search/companies", comp_body(MFG, et_ct=False))
    run("fls/companies/et-ct", "/v2/search/companies", comp_body(FLS_IND, FLS_KW))
    run("fls/companies/et-ct/51-5000", "/v2/search/companies", comp_body(FLS_IND, FLS_KW, sizes=["51-200", "201-500", "501-1000", "1001-5000"]))
    for fam, titles in ROLES.items():
        for d in (30, 90, 120):
            run(f"mfg/jobs/{fam}/{d}d/et-ct", "/v2/jobs/search", jobs_body(titles, d, MFG))
        run(f"mfg/jobs/{fam}/30d/all-us", "/v2/jobs/search", jobs_body(titles, 30, MFG, et_ct=False))
    for d in (30, 90, 120):
        run(f"fls/jobs/{d}d/et-ct", "/v2/jobs/search", jobs_body(FLS_ROLES, d, FLS_IND, FLS_KW))
        run(f"fls/jobs/{d}d/et-ct/51-5000", "/v2/jobs/search",
            jobs_body(FLS_ROLES, d, FLS_IND, FLS_KW, sizes=["51-200", "201-500", "501-1000", "1001-5000"]))
    out["_records_used"] = used
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tam_counts.json"), "w"), indent=1)
    print("records used:", used)
