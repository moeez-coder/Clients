"""HLD agency persona sizing, 2026-11-18. Blitz API, counts only (max_results: 1, 1 record per call).
Reproduces the final numbers in 2026-11-18-agency-persona-sizing.query.md. Writes persona_counts.json."""
import json, os, urllib.request
def call(path, body):
    r = urllib.request.Request("https://api.blitz-api.ai" + path, data=json.dumps(body).encode(),
        headers={"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=120))

# ---- company universe (core): US health/pharma agencies, 51 to 5,000 employees ----
IND = ["Advertising Services", "Marketing and Advertising", "Marketing Services"]  # exact Blitz enum labels
KW_PHARMA = ["pharmaceutical marketing", "pharma marketing", "pharmaceutical advertising", "pharma advertising",
             "medical communications", "life sciences marketing", "life sciences communications", "HCP marketing",
             "HCP", "biopharma", "healthcare communications", "health and wellness communications", "pharmaceutical", "pharma"]
KW_EXCL = ["staffing", "SEO", "hospital marketing", "dental marketing", "senior living"]
# existing HLD clients + HLD itself + identity/adtech vendors (competitors or partners, not buyers)
NAME_EXCL = ["Publicis Health Media", "EVERSANA", "Relevate Health", "HealthLink Dimensions", "Health Link Dimensions",
             "Throtle", "DeepIntent", "PulsePoint", "OptimizeRx", "IQVIA", "Komodo"]
SIZES = ["51-200", "201-500", "501-1000", "1001-5000"]
def company(): return {"industry": {"include": IND}, "employee_range": SIZES, "hq": {"country_code": ["US"]},
                       "keywords": {"include": KW_PHARMA, "exclude": KW_EXCL}, "name": {"exclude": NAME_EXCL}}

# ---- persona title map (Blitz job_title keyword match; priority D&A > Investment > Planning > Leadership) ----
NOISE = ["Intern", "Assistant", "Coordinator", "Recruiter", "Talent", "Human Resources", "Finance", "Accounting", "Legal",
         "Facilities", "Media Relations", "Public Relations", "Social Media", "Sales Activation"]
DA   = ["Analytics", "Measurement", "Data Science", "Data Scientist", "Data Strategy", "Data Analyst", "Attribution",
        "Insights", "Marketing Science", "Decision Science"]
INV  = ["Media Investment", "Investment", "Programmatic", "Media Buying", "Media Buyer", "Biddable", "Trading",
        "Activation Economics", "Supply Partnerships", "Media Partnerships"]
PLAN = ["Media Planning", "Media Planner", "Activation", "Omnichannel", "Omni-channel", "HCP Media", "Media Strategy",
        "Media Director", "Media Supervisor", "Channel Planning", "Connections Planning", "Paid Media", "Engagement Planning"]
LEAD_FUNC_EXCL = ["Analytics", "Measurement", "Insights", "Programmatic", "Activation", "Omnichannel", "Planning", "Account",
                  "Creative", "Client", "Business Development", "Sales", "Copy", "Art Director", "Editorial",
                  "Medical Director", "Scientific", "Production", "Technology", "Engineering"]
LEAD_C  = ["CEO", "Chief Executive", "[President]", "President and CEO", "President & CEO", "Chief Strategy Officer",
           "Chief Media Officer", "Chief Operating Officer", "Chief Growth Officer", "Chief Innovation Officer",
           "Chief Commercial Officer", "Founder", "Co-Founder"]
LEAD_DM = ["Managing Director", "General Manager", "Executive Vice President", "EVP", "Head of Strategy",
           "SVP, Strategy", "SVP Strategy", "Group President", "Office Lead"]
CELLS = {  # persona -> level -> (title include, title exclude, job_level)
 "data_analytics": {
   "influencers": (DA, NOISE, ["C-Team", "VP"]), "decision_makers": (DA, NOISE, ["Director"]), "advocates": (DA, NOISE, ["Manager"])},
 "investment": {
   "influencers": (INV, NOISE + DA, ["C-Team", "VP"]), "decision_makers": (INV, NOISE + DA, ["Director"]),
   "advocates": (INV, NOISE + DA, ["Manager"])},
 "planning_activation": {
   "influencers": (PLAN, NOISE + DA + INV, ["C-Team", "VP"]), "decision_makers": (PLAN, NOISE + DA + INV, ["Director"]),
   "advocates": (PLAN, NOISE + DA + INV, ["Manager"])},
 "leadership": {
   "influencers": (LEAD_C, NOISE + LEAD_FUNC_EXCL + ["Vice President"], ["C-Team", "VP"]),
   "decision_makers": (LEAD_DM, NOISE + LEAD_FUNC_EXCL + ["Media", "Data", "Investment", "Assistant Vice President", "CEO", "Chief", "Founder"], ["C-Team", "VP", "Director"])},
}
def people(inc, exc, lv, comp=None, desc=None):
    p = {"job_title": {"include": inc, "exclude": exc}, "job_level": lv, "location": {"country_code": ["US"]}}
    if desc: p["job_description"] = {"include": desc}
    return {"company": comp or company(), "people": p, "max_results": 1}

if __name__ == "__main__":
    out, used = {"companies": {}, "cells": {}, "extension_general_agencies": {}}, 0
    b = {"company": company(), "max_results": 1}; r = call("/v2/search/companies", b); used += r["fair_usage"]["records_used"]
    out["companies"] = {"body": b, "total_results": r["total_results"]}; print("companies", r["total_results"])
    for pn, levels in CELLS.items():
        for ln, (inc, exc, lv) in levels.items():
            assert len(exc) <= 50 and len(inc) <= 50
            b = people(inc, exc, lv); r = call("/v2/search/people", b); used += r["fair_usage"]["records_used"]
            out["cells"][f"{pn}/{ln}"] = {"body": b, "total_results": r["total_results"]}
            print(pn, ln, r["total_results"])
    # extension: health-practice people inside general ad/media agencies (any size, no company keyword filter),
    # caught by "pharma/HCP/healthcare" in their job description. Not additive to core (overlap), sensitivity only.
    gen = {"industry": {"include": IND}, "hq": {"country_code": ["US"]}, "name": {"exclude": NAME_EXCL}}
    desc = ["pharma", "pharmaceutical", "HCP", "healthcare clients", "health clients", "life sciences"]
    for pn in ["data_analytics", "investment", "planning_activation"]:
        inc, exc, _ = CELLS[pn]["influencers"]
        b = people(inc, exc, ["C-Team", "VP", "Director", "Manager"], comp=gen, desc=desc)
        r = call("/v2/search/people", b); used += r["fair_usage"]["records_used"]
        out["extension_general_agencies"][pn] = {"body": b, "total_results": r["total_results"]}
        print("ext", pn, r["total_results"])
    out["records_used"] = used; print("records_used", used)
    json.dump(out, open("2026-11-18-persona_counts.json", "w"), indent=1)
