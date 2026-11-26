"""Leads for the 2026-11-26 MPC company expansion (Moe: "add 51 - 5000"). Companies: kept postings in
../tam/2026-11-26-mpc-wide-jobs.csv (size bands 51-200 and 1001-5000; disjoint from the 201-1000 companies built 11-24/25).
Each company goes to ONE segment, same rule as pull_segment_leads.py (family with most kept postings, tie -> newest posting's).
Two Blitz API POST /v2/search/waterfall-icp-keyword calls per company, the same two passes the 201-1000 companies got:
  pass "cvp": tiers = segment TIER1, TIER2, TIER3 from spec.py, PEOPLE_EXCLUDE (Managers + Directors out), max_results 5
  pass "dir": tiers = segment Director titles, other manufacturing Director functions, HR Directors (pull_directors.py), max_results 10
Anyone already in any GRN lead file (URL or first+last+company) is marked removed. Persona/title gates as before.
Output: $RAW/wide-people.jsonl (resumable), $RAW/wide-companies.json, $RAW/wide-leads-raw.csv.
Usage: RAW=/path python3 pull_wide_leads.py"""
import csv, json, os, re, sys, glob, collections
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, ".."); LIVE = os.path.join(S, "recruitment-specific-open-roles")
sys.path.insert(0, os.path.join(S, "tam")); sys.path.insert(0, LIVE)
from tam_counts import post
from spec import TIER1, TIER2, TIER3, PEOPLE_EXCLUDE
from build_leads import PERSONA, OFF, SUFFIX, first_clean
RAW = os.environ["RAW"]; os.makedirs(RAW, exist_ok=True)
T1 = {"executive": TIER1["executive-finance-hr"], "operations-plant": TIER1["operations-plant-leadership"],
      "engineering-quality": TIER1["engineering-quality"], "supply-chain-purchasing": TIER1["supply-chain-purchasing"],
      "ehs-maintenance": TIER1["operations-plant-leadership"]}
OPS_DIR = ["Director Operations", "Director Manufacturing", "Plant Director", "Director Production", "Director Plant Operations",
           "Director Continuous Improvement", "Director Operational Excellence", "Head Operations", "Head Manufacturing", "Site Director"]
FAM = {"operations-plant": OPS_DIR,
       "executive": ["Director Operations", "Director Manufacturing", "Plant Director", "Director Finance", "Finance Director",
                     "Director Human Resources", "HR Director", "Director Business Operations", "Head Operations", "Site Director"],
       "engineering-quality": ["Director Engineering", "Director Manufacturing Engineering", "Director Process Engineering", "Director Quality",
                               "Director Quality Assurance", "Head Engineering", "Head Quality", "Director Product Engineering", "Director Engineering Quality"],
       "supply-chain-purchasing": ["Director Supply Chain", "Director Purchasing", "Director Procurement", "Director Materials", "Director Logistics",
                                   "Director Planning", "Director Sourcing", "Head Supply Chain", "Head Procurement"],
       "ehs-maintenance": ["Director EHS", "Director Safety", "Director Environmental Health Safety", "Director Maintenance", "Director Facilities",
                           "Director Reliability", "Head EHS", "Head Maintenance"]}
ALL_DIR = sorted(set(OPS_DIR + ["Director Engineering", "Director Manufacturing Engineering", "Director Quality", "Director Supply Chain",
      "Director Purchasing", "Director Procurement", "Director Materials", "Director Logistics", "Director Maintenance", "Director EHS",
      "Director Safety", "Director Finance", "Director Facilities", "Director Planning"]))
HR_DIR = ["Director Human Resources", "HR Director", "Director People"]
DIR_EXC = ["Manager", "Assistant", "Associate", "Former", "Retired", "Sales", "Marketing", "Intern", "Recruiter", "IT", "Information Technology", "Finance"]
DIRT = re.compile(r"\b(director|head)\b", re.I)
norm = lambda u: (u or "").lower().split("?")[0].rstrip("/").replace("http://", "https://").replace("://linkedin", "://www.linkedin")

jobs = [r for r in csv.DictReader(open(os.path.join(S, "tam", "2026-11-26-mpc-wide-jobs.csv"))) if r["status"] == "kept"]
by = collections.defaultdict(list)
for r in jobs: by[r["company_linkedin_url"]].append(r)
comps = []
for u, rs in by.items():
    cnt = collections.Counter(r["role_family"] for r in rs); newest = max(rs, key=lambda r: r["date_posted"])
    fam = max(cnt, key=lambda f: (cnt[f], f == newest["role_family"]))
    pick = max((r for r in rs if r["role_family"] == fam), key=lambda r: r["date_posted"])
    comps.append({"company_linkedin_url": u, "company_name": pick["company_name"], "segment": fam, "vertical": pick["segment_vertical"],
                  "size_band": pick["size_band"], "open_role": pick["title"], "job_url": pick["job_url"], "job_posted": pick["date_posted"],
                  "jd_summary": pick["jd_summary"], "kept_postings": len(rs), "in_live_campaign": "no"})
json.dump(comps, open(os.path.join(RAW, "wide-companies.json"), "w"))

held, names = set(), set()
for f in glob.glob(os.path.join(S, "*", "*-leads.csv")):
    for r in csv.DictReader(open(f)):
        held.add(norm(r["linkedin_url"])); names.add((r["first_name"].lower(), r["last_name"].lower(), r["company_linkedin_url"].lower()))

pp = os.path.join(RAW, "wide-people.jsonl")
done = {(d["company_linkedin_url"], d["pass"]) for d in map(json.loads, open(pp))} if os.path.exists(pp) else set()
def one(job):
    c, ps = job
    if ps == "cvp":
        casc = [{"include_title": t, "exclude_title": PEOPLE_EXCLUDE, "location": {"country_code": ["US"]}, "include_headline_search": False}
                for t in (T1[c["segment"]], TIER2, TIER3)]; mx = 5
    else:
        casc = [{"include_title": t, "exclude_title": DIR_EXC, "location": {"country_code": ["US"]}, "include_headline_search": False}
                for t in (FAM[c["segment"]], sorted(set(ALL_DIR) - set(FAM[c["segment"]])), HR_DIR)]; mx = 10
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc, "max_results": mx})
    return {"company_linkedin_url": c["company_linkedin_url"], "pass": ps, "results": r.get("results") or [], "error": r.get("_error"),
            "used": (r.get("fair_usage") or {}).get("records_used", 0)}
todo = [(c, ps) for c in comps for ps in ("cvp", "dir") if (c["company_linkedin_url"], ps) not in done]
used = 0
with ThreadPoolExecutor(12) as ex, open(pp, "a") as f:
    for i, r in enumerate(ex.map(one, todo)):
        used += r["used"]; f.write(json.dumps(r) + "\n")
        if i % 300 == 0: f.flush(); print(i, "/", len(todo), flush=True)
u = json.load(open(os.path.join(RAW, "wide-usage.json"))) if os.path.exists(os.path.join(RAW, "wide-usage.json")) else {}
u["waterfall"] = u.get("waterfall", 0) + used; json.dump(u, open(os.path.join(RAW, "wide-usage.json"), "w"))

cm = {c["company_linkedin_url"]: c for c in comps}; out = []; seen = set()
for d in map(json.loads, open(pp)):
    c = cm[d["company_linkedin_url"]]
    for p in d["results"]:
        q = p["person"]; url = norm(q.get("linkedin_url"))
        if not url or url in seen: continue
        seen.add(url)
        title = (q.get("experiences") or [{}])[0].get("job_title") or (q.get("headline") or "").split(" | @")[0] or "-"
        loc = q.get("location") or {}; st = "launch set"
        if url in held or ((q.get("first_name") or "").lower(), (q.get("last_name") or "").lower(), c["company_linkedin_url"]) in names:
            st = "removed: already in another GRN lead file"
        elif d["pass"] == "cvp" and (not PERSONA.search(title) or (OFF.search(title) and p.get("icp") != 1)): st = "removed: title outside persona"
        elif d["pass"] == "dir" and not DIRT.search(title): st = "removed: title not Director level"
        out.append({"linkedin_url": q["linkedin_url"], "first_name": q.get("first_name") or "-", "last_name": SUFFIX.sub("", q.get("last_name") or "").strip() or "-",
                    "full_name": q.get("full_name") or "-", "job_title": title, "company_name": c["company_name"],
                    "company_linkedin_url": c["company_linkedin_url"], "person_country": loc.get("country_code") or "-", "company_country": "US",
                    "first_name_clean": first_clean(q.get("first_name")) or "-", "waterfall_tier": p.get("icp", "-"), "segment": c["segment"],
                    "wave": "2026-11-26 size expansion " + ("C-level/VP" if d["pass"] == "cvp" else "Directors"), "size_band": c["size_band"],
                    "vertical": c["vertical"], "company_in_live_campaign": "no", "person_state": loc.get("state_code") or "-", "status": st})
with open(os.path.join(RAW, "wide-leads-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
st = collections.Counter((r["segment"], r["status"]) for r in out)
for k in sorted(st): print(k, st[k])
print("companies", len(comps), "records", u, "errors", sum(1 for d in map(json.loads, open(pp)) if d["error"]))
