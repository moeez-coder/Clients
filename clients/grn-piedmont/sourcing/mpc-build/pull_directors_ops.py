"""Ops & Plant Director wave (2026-11-25). Moe chose Ops & Plant to go live with the expanded list (lever 1, Directors;
see ../tam/2026-11-25-levers-review.md). Expanding existing segment mpc-operations-plant.
Blitz API POST /v2/search/waterfall-icp-keyword on all 362 companies assigned to the segment (../mpc-operations-plant/2026-11-24-companies.csv):
  tier 1 = operations/plant Directors, tier 2 = HR Directors; Managers still excluded; US; max_results 5.
Anyone already in any GRN lead file (live 734516/756466 + the 5 MPC files, URL or name+company) is marked removed.
Output: $RAW/dir-people.jsonl (resumable) and $RAW/dir-leads-raw.csv.  Usage: RAW=/path [PASS=2] python3 pull_directors_ops.py  (pass 2 = all Director functions, max 10; output merges both passes)"""
import csv, json, os, re, sys, glob, collections
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, ".."); sys.path.insert(0, os.path.join(S, "tam")); sys.path.insert(0, os.path.join(S, "recruitment-specific-open-roles"))
from tam_counts import post
from build_leads import SUFFIX, first_clean
RAW = os.environ["RAW"]
T1 = ["Director Operations", "Director Manufacturing", "Plant Director", "Director Production", "Director Plant Operations",
      "Director Continuous Improvement", "Director Operational Excellence", "Head Operations", "Head Manufacturing", "Site Director"]
T2 = ["Director Human Resources", "HR Director", "Director People"]
# Pass 2 (same day): every manufacturing Director function, up to 10 per company, so the wave reaches the ~800 Moe asked for.
T3 = ["Director Engineering", "Director Manufacturing Engineering", "Director Quality", "Director Supply Chain", "Director Purchasing",
      "Director Procurement", "Director Materials", "Director Logistics", "Director Maintenance", "Director EHS", "Director Safety",
      "Director Finance", "Director Facilities", "Director Planning"]
PASS = int(os.environ.get("PASS", "1"))
EXC = ["Manager", "Assistant", "Associate", "Former", "Retired", "Sales", "Marketing", "Intern", "Recruiter", "IT", "Information Technology", "Finance"]
DIRT = re.compile(r"\b(director|head)\b", re.I)
comps = list(csv.DictReader(open(os.path.join(S, "mpc-operations-plant", "2026-11-24-companies.csv"))))
norm = lambda u: (u or "").lower().split("?")[0].rstrip("/").replace("http://", "https://").replace("://linkedin", "://www.linkedin")
held, names = set(), set()
for f in glob.glob(os.path.join(S, "*", "*-leads.csv")):
    for r in csv.DictReader(open(f)):
        held.add(norm(r["linkedin_url"])); names.add((r["first_name"].lower(), r["last_name"].lower(), r["company_linkedin_url"].lower()))
pp = os.path.join(RAW, "dir-people.jsonl" if PASS == 1 else "dir-people-2.jsonl"); done = {json.loads(l)["company_linkedin_url"] for l in open(pp)} if os.path.exists(pp) else set()
def one(c):
    casc = [{"include_title": t, "exclude_title": EXC, "location": {"country_code": ["US"]}, "include_headline_search": False} for t in ((T1, T2) if PASS == 1 else (T1, T3, T2))]
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc, "max_results": 5 if PASS == 1 else 10})
    return {"company_linkedin_url": c["company_linkedin_url"], "results": r.get("results") or [], "used": (r.get("fair_usage") or {}).get("records_used", 0)}
used = 0
with ThreadPoolExecutor(12) as ex, open(pp, "a") as f:
    for r in ex.map(one, [c for c in comps if c["company_linkedin_url"] not in done]): used += r["used"]; f.write(json.dumps(r) + "\n")
cm = {c["company_linkedin_url"]: c for c in comps}; out = []; seen = set()
for l in [x for f in ("dir-people.jsonl", "dir-people-2.jsonl") if os.path.exists(os.path.join(RAW, f)) for x in open(os.path.join(RAW, f))]:
    d = json.loads(l); c = cm[d["company_linkedin_url"]]
    for p in d["results"]:
        q = p["person"]; u = norm(q.get("linkedin_url"))
        if not u or u in seen: continue
        seen.add(u); t = (q.get("experiences") or [{}])[0].get("job_title") or (q.get("headline") or "").split(" | @")[0] or "-"
        st = "launch set"
        if u in held or ((q.get("first_name") or "").lower(), (q.get("last_name") or "").lower(), c["company_linkedin_url"]) in names: st = "removed: already in another GRN lead file"
        elif not DIRT.search(t): st = "removed: title not Director level"
        elif c["launch_note"] != "-": st = c["launch_note"]
        out.append({"linkedin_url": q["linkedin_url"], "first_name": q.get("first_name") or "-", "last_name": SUFFIX.sub("", q.get("last_name") or "").strip() or "-",
                    "full_name": q.get("full_name") or "-", "job_title": t, "company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"],
                    "person_country": (q.get("location") or {}).get("country_code") or "-", "company_country": "US", "first_name_clean": first_clean(q.get("first_name")) or "-",
                    "waterfall_tier": p.get("icp", "-"), "segment": "operations-plant", "wave": "2026-11-25 directors", "vertical": c["vertical"],
                    "company_in_live_campaign": c["in_live_campaign"], "person_state": (q.get("location") or {}).get("state_code") or "-", "status": st})
with open(os.path.join(RAW, "dir-leads-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("rows", len(out), collections.Counter(r["status"] for r in out), "companies w/ launch", len({r["company_linkedin_url"] for r in out if r["status"] == "launch set"}), "records", used)
