"""Persona reachability sample for the GRN general TAM (2026-11-24).
Blitz POST /v2/search/waterfall-icp-keyword on 40 random qc_tier=core manufacturing companies + all 36
F&LS specialists in core (seed 24). Persona = client ICP form: CEO, COO, CFO, CHRO, President, Owner, VP;
Manager and Director excluded. US people only, LinkedIn URL only (no email). max_results 10 per company,
so the per-company count is capped at 10.
Output: raw prospect rows, landed via tools/leads.py normalize as 2026-11-24-leads.csv + persona_reach_sample.json
"""
import csv, json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tam"))
from tam_counts import post
T1 = ["Chief Executive Officer", "CEO", "[President]", "[Owner]", "[Founder]", "Owner President", "President CEO"]
T2 = ["Chief Operating Officer", "COO", "Chief Financial Officer", "CFO", "Chief Human Resources Officer", "CHRO",
      "Chief People Officer"]
T3 = ["Vice President", "VP"]
EXCL = ["Manager", "Director", "Assistant", "Coordinator", "Recruiter", "Former", "Retired", "Intern", "Sales Representative"]
rows = list(csv.DictReader(open(os.path.join(HERE, "2026-11-24-companies-qc.csv"))))
random.seed(24)
mfg = random.sample([r for r in rows if r["qc_tier"] == "core" and r["segment"] == "manufacturing"], 40)
fls = [r for r in rows if r["qc_tier"] == "core" and r["qc_fls"] == "fls_specialist"]
comps = [("manufacturing", r) for r in mfg] + [("fls_specialist", r) for r in fls]


def one(item):
    seg, c = item
    casc = [{"include_title": t, "exclude_title": EXCL, "location": {"country_code": ["US"]}, "include_headline_search": False}
            for t in (T1, T2, T3)]
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc, "max_results": 10})
    return seg, c, r


out, summ, used = [], [], 0
with ThreadPoolExecutor(8) as ex:
    for seg, c, r in ex.map(one, comps):
        used += (r.get("fair_usage") or {}).get("records_used", 0)
        res = r.get("results") or []
        tiers = {}
        for x in res:
            p = x.get("person") or x
            tier = x.get("icp") or x.get("tier") or x.get("cascade_index") or "-"
            url = p.get("linkedin_url") or "-"
            exp = (p.get("experiences") or [{}])[0] if p.get("experiences") else {}
            out.append({"linkedin_url": url, "full_name": p.get("full_name") or "-", "job_title": exp.get("job_title") or p.get("headline") or "-",
                        "cascade_tier": tier, "company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"],
                        "segment": seg, "source_tool": "Blitz POST /v2/search/waterfall-icp-keyword", "pulled_on": "2026-11-24"})
            tiers[str(tier)] = tiers.get(str(tier), 0) + 1
        summ.append({"company": c["company_name"], "segment": seg, "n": len(res), "tiers": tiers, "error": r.get("_error")})
w = csv.DictWriter(open(os.environ.get("RAW_OUT", "persona-raw.csv"), "w", newline=""), fieldnames=list(out[0]))
w.writeheader(); w.writerows(out)
json.dump({"records_used": used, "companies": summ}, open(os.path.join(HERE, "persona_reach_sample.json"), "w"), indent=1)
for seg in ("manufacturing", "fls_specialist"):
    s = [x for x in summ if x["segment"] == seg]; n = [x["n"] for x in s]
    print(seg, len(s), "companies; with >=1:", sum(v > 0 for v in n), "mean", round(sum(n) / len(n), 2), "dist", sorted(n))
print("records used", used, "errors", [x for x in summ if x["error"]][:3])
