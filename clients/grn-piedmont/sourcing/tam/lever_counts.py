"""Levers to reach ~800 leads per MPC campaign (2026-11-25, Moe: "do 1-3 and 5 and give me a review").
A. Posting counts (levers 2 size, 3 geography, 5 window): Blitz POST /v2/jobs/search, max_results 1, total_results, same
   71-title list and gates as mpc_segments_pull.py (titles in 2 chunks x MFG labels in 2 halves = 4 calls per variant, summed).
   total_results is indicative (CLAUDE.md); the base variant is compared with the real 11-24 pull to calibrate.
B. Lever 1 (Director contacts): Blitz POST /v2/search/waterfall-icp-keyword on 80 seeded-random hiring companies from the
   11-24 pull, Director-level titles only (Managers still excluded), max_results 10. Counts Directors reachable per company.
Writes 2026-11-25-levers.json + 2026-11-25-levers-director-sample.csv.  Usage: python3 lever_counts.py"""
import csv, json, os, random, sys, collections
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from tam_counts import MFG, NON_ET_CT, EXCL, post
from mpc_segments_pull import CHUNKS
OUT = {"variants": {}, "records_used": 0}
def body(titles, inds, days, sizes, et_ct):
    comp = {"is_agency": False, "industry": {"include": inds}, "size": {"include": sizes}, "hq": {"country_code": {"include": ["US"]}}}
    if et_ct: comp["hq"]["state"] = {"exclude": NON_ET_CT}
    return {"job": {"title": {"include": titles, "exclude": EXCL}, "location": {"country_code": {"include": ["US"]}},
                    "date_posted": {"last_days": days}, "employment_type": {"include": ["FULL_TIME"]}}, "company": comp, "max_results": 1}
VARIANTS = {
    "base 201-1000 ET/CT 120d": (["201-500", "501-1000"], True, 120),
    "lever2 +1001-5000": (["1001-5000"], True, 120),
    "lever2 +51-200": (["51-200"], True, 120),
    "lever3 Mountain/Pacific/AK/HI only (201-1000)": (None, "west", 120),
    "lever5 window 180d (201-1000 ET/CT)": (["201-500", "501-1000"], True, 180),
    "lever5 window 365d (201-1000 ET/CT)": (["201-500", "501-1000"], True, 365),
}
def run(name, sizes, geo, days):
    tot = 0
    for t in CHUNKS:
        for half in (MFG[:35], MFG[35:]):
            if geo == "west":
                b = body(t, half, days, ["201-500", "501-1000"], False); b["company"]["hq"]["state"] = {"include": NON_ET_CT}
            else: b = body(t, half, days, sizes, geo)
            r = post("/v2/jobs/search", b); OUT["records_used"] += (r.get("fair_usage") or {}).get("records_used", 0)
            tot += r.get("total_results") or 0
    OUT["variants"][name] = {"postings_total_results": tot, "sizes": sizes, "geo": geo, "days": days}
    print(name, tot, flush=True)
for k, v in VARIANTS.items(): run(k, *v)
# ---- B. Director sample
DIR = ["Director Operations", "Director Manufacturing", "Plant Director", "Director Engineering", "Director Quality",
       "Director Supply Chain", "Director Purchasing", "Director Procurement", "Director Materials", "Director Human Resources",
       "HR Director", "Director Finance", "Director EHS", "Director Maintenance", "Director Production", "Director Continuous Improvement"]
comps = [c for c in csv.DictReader(open(os.path.join(HERE, "2026-11-24-mpc-segments-companies.csv"))) if c["vertical"] != "fire-life-safety"]
random.seed(20261125); samp = random.sample(comps, 80)
def one(c):
    casc = [{"include_title": DIR, "exclude_title": ["Assistant", "Associate", "Former", "Retired", "Sales", "Marketing", "Intern", "Recruiter", "Manager"],
             "location": {"country_code": ["US"]}, "include_headline_search": False}]
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc, "max_results": 10})
    return c, r.get("results") or [], (r.get("fair_usage") or {}).get("records_used", 0)
rows = []
with ThreadPoolExecutor(8) as ex:
    for c, res, u in ex.map(one, samp):
        OUT["records_used"] += u
        if not res: rows.append({"company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"], "in_live_campaign": c["in_live_campaign"], "linkedin_url": "-", "job_title": "-"})
        for p in res:
            q = p["person"]; t = (q.get("experiences") or [{}])[0].get("job_title") or "-"
            rows.append({"company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"], "in_live_campaign": c["in_live_campaign"],
                         "linkedin_url": q.get("linkedin_url") or "-", "job_title": t})
with open(os.path.join(HERE, "2026-11-25-levers-director-sample.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
people = [r for r in rows if r["linkedin_url"] != "-"]
per = collections.Counter(r["company_linkedin_url"] for r in people)
OUT["director_sample"] = {"companies": len(samp), "companies_with_director": len(per), "directors": len(people),
                          "directors_per_company_all": round(len(people) / len(samp), 2), "at_cap_10": sum(1 for v in per.values() if v >= 10)}
print(OUT["director_sample"], "records", OUT["records_used"])
json.dump(OUT, open(os.path.join(HERE, "2026-11-25-levers.json"), "w"), indent=1)
