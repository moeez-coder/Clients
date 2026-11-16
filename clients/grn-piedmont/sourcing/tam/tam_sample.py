"""Eyeball sample for the GRN Piedmont open-role TAM read (2026-11-16). NOT a full pull.

1. One page (50 newest postings) per role family from POST /v2/jobs/search, same bodies as tam_counts.py
   with max_results 50 -> 2026-11-16-jobs-sample.csv. Gives the postings-per-company ratio and lets a
   person read the titles/companies for noise.
2. POST /v2/search/waterfall-icp-keyword on the first 3 distinct companies of each family (15 companies),
   max_results 3 -> 2026-11-16-sample-leads.csv. Checks that the persona (C-level / VP / Owner only, no
   Manager or Director) is reachable. LinkedIn URLs only, no email enrichment.
Usage: python3 tam_sample.py
"""
import csv, json, os, re
from tam_counts import ROLES, FLS_ROLES, MFG, FLS_IND, FLS_KW, jobs_body, post

HERE = os.path.dirname(os.path.abspath(__file__))
TIER1 = {
    "operations-plant-leadership": ["Chief Operating Officer", "COO", "VP Operations", "Vice President Operations",
                                    "VP Manufacturing", "Vice President Manufacturing", "SVP Operations", "EVP Operations"],
    "engineering-quality": ["VP Engineering", "Vice President Engineering", "Chief Technology Officer", "CTO",
                            "VP Quality", "Vice President Quality", "Chief Operating Officer", "COO", "VP Operations",
                            "Vice President Operations"],
    "supply-chain-purchasing": ["VP Supply Chain", "Vice President Supply Chain", "Chief Supply Chain Officer",
                                "Chief Procurement Officer", "VP Procurement", "VP Purchasing", "Chief Operating Officer",
                                "COO", "VP Operations", "Vice President Operations"],
    "executive-finance-hr": ["Chief Executive Officer", "CEO", "President", "Owner", "Chief Financial Officer", "CFO",
                             "Chief Human Resources Officer", "CHRO"],
    "fire-life-safety": ["Chief Operating Officer", "COO", "VP Operations", "Vice President Operations", "President",
                         "Chief Executive Officer", "CEO", "Owner"],
}
TIER2 = ["Chief Executive Officer", "CEO", "President", "Owner", "Founder"]
TIER3 = ["Chief Human Resources Officer", "CHRO", "Chief People Officer", "VP Human Resources",
         "Vice President Human Resources", "VP People"]
P_EXCL = ["Manager", "Director", "Assistant", "Coordinator", "Recruiter", "Former", "Sales", "Vice President Sales"]

used, jobs, leads = 0, [], []
fams = {k: (v, MFG, None) for k, v in ROLES.items()}
fams["fire-life-safety"] = (FLS_ROLES, FLS_IND, FLS_KW)
for fam, (titles, inds, kw) in fams.items():
    b = jobs_body(titles, 30, inds, kw); b["max_results"] = 50
    halves = [inds] if len(inds) <= 50 else [inds[:35], inds[35:]]
    rows = []
    for h in halves:
        bb = json.loads(json.dumps(b)); bb["company"]["industry"]["include"] = h; bb["max_results"] = 50 // len(halves)
        r = post("/v2/jobs/search", bb); used += (r.get("fair_usage") or {}).get("records_used", 0)
        rows += r.get("results") or []
    for x in rows:
        jobs.append({"role_family": fam, "title": x.get("title") or "-", "company_name": x.get("company_name") or "-",
                     "company_linkedin_url": x.get("company_linkedin_url") or "-", "location": json.dumps(x.get("location")) if isinstance(x.get("location"), (dict, list)) else (x.get("location") or "-"),
                     "date_posted": (x.get("date_posted") or "-")[:10], "job_url": x.get("url") or "-",
                     "ai_summary": re.sub(r"\s+", " ", x.get("ai_summary") or "-")})
    seen = []
    for x in rows:
        u = x.get("company_linkedin_url")
        if u and u not in seen: seen.append(u)
    for u in seen[:3]:
        casc = [{"include_title": t, "exclude_title": P_EXCL, "location": {"country_code": ["US"]},
                 "include_headline_search": False} for t in (TIER1[fam], TIER2, TIER3)]
        r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": u, "cascade": casc, "max_results": 3})
        used += (r.get("fair_usage") or {}).get("records_used", 0)
        res = r.get("results") or []
        if not res:
            leads.append({"linkedin_url": "-", "first_name": "-", "last_name": "-", "job_title": "-", "waterfall_tier": "-",
                          "company_linkedin_url": u, "role_family": fam, "note": "no persona match " + str(r.get("_error", ""))})
        for p in res:
            q = p.get("person") or p
            leads.append({"linkedin_url": q.get("linkedin_url") or "-", "first_name": q.get("first_name") or "-",
                          "last_name": q.get("last_name") or "-", "job_title": q.get("job_title") or q.get("title") or q.get("headline") or "-",
                          "waterfall_tier": p.get("icp", "-"), "company_linkedin_url": u, "role_family": fam, "note": "-"})
    print(fam, len(rows), "jobs,", len({x.get('company_linkedin_url') for x in rows}), "companies", flush=True)

for name, rows in (("2026-11-16-jobs-sample.csv", jobs), ("2026-11-16-sample-leads.csv", leads)):
    with open(os.path.join(HERE, name), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump({"records_used": used, "jobs_rows": len(jobs), "lead_rows": len(leads)}, open(os.path.join(HERE, "tam_sample_usage.json"), "w"))
print("records used:", used)
