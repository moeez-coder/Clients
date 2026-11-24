"""Seed leads for the 5 GRN MPC role-family campaigns (2026-11-24, Moe approved the segment build: "Yes to all 3").

Input: ../tam/2026-11-24-mpc-segments-jobs.csv (kept postings, 120 days) + -companies.csv. F&LS companies are left out
(folded into the existing F&LS campaign, not built here).
Each company goes to ONE segment: its role family with the most kept postings (tie -> the family of its newest posting).
Its open role = the newest kept posting in that family (open-posting check and swap happen in fetch_jds.py).
Blitz API POST /v2/search/waterfall-icp-keyword per company, same tiers/excludes as the live campaign (spec.py):
  net-new companies max_results 5; companies already in the live campaign max_results 10 (to reach past the people
  already contacted). Anyone already in 2026-11-16/-23 leads (734516 / 756466) is excluded afterwards (URL or name+company).
Output: raw in $RAW/people.jsonl (resumable), then raw leads CSV $RAW/leads-raw.csv for tools/leads.py normalize.
Usage: RAW=/path python3 pull_segment_leads.py"""
import csv, json, os, re, sys, collections
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, ".."); LIVE = os.path.join(S, "recruitment-specific-open-roles")
sys.path.insert(0, os.path.join(S, "tam")); sys.path.insert(0, LIVE)
from tam_counts import post
from spec import TIER1, TIER2, TIER3, PEOPLE_EXCLUDE
from build_leads import PERSONA, OFF, SUFFIX, first_clean
RAW = os.environ["RAW"]; os.makedirs(RAW, exist_ok=True)
FAMS = ["executive", "operations-plant", "engineering-quality", "supply-chain-purchasing", "ehs-maintenance"]
T1 = {"executive": TIER1["executive-finance-hr"], "operations-plant": TIER1["operations-plant-leadership"],
      "engineering-quality": TIER1["engineering-quality"], "supply-chain-purchasing": TIER1["supply-chain-purchasing"],
      "ehs-maintenance": TIER1["operations-plant-leadership"]}
jobs = [r for r in csv.DictReader(open(os.path.join(S, "tam", "2026-11-24-mpc-segments-jobs.csv"))) if r["status"] == "kept" and r["segment_vertical"] != "fire-life-safety"]
by = collections.defaultdict(list)
for r in jobs: by[r["company_linkedin_url"]].append(r)
norm = lambda u: (u or "").lower().split("?")[0].rstrip("/").replace("http://", "https://").replace("://linkedin", "://www.linkedin")
held, held_names = set(), set()
live_cos = set()
for f in ("2026-11-16-leads.csv", "2026-11-23-leads.csv"):
    for r in csv.DictReader(open(os.path.join(LIVE, f))):
        held.add(norm(r["linkedin_url"])); held_names.add((r["first_name"].lower(), r["last_name"].lower(), r["company_linkedin_url"].lower()))
        if r.get("status", "launch set") == "launch set": live_cos.add(r["company_linkedin_url"].lower().rstrip("/"))
comps = []
for u, rs in by.items():
    cnt = collections.Counter(r["role_family"] for r in rs); newest = max(rs, key=lambda r: r["date_posted"])
    fam = max(cnt, key=lambda f: (cnt[f], f == newest["role_family"]))
    pick = max((r for r in rs if r["role_family"] == fam), key=lambda r: r["date_posted"])
    comps.append({"company_linkedin_url": u, "company_name": pick["company_name"], "segment": fam, "vertical": pick["segment_vertical"],
                  "open_role": pick["title"], "job_url": pick["job_url"], "job_posted": pick["date_posted"], "jd_summary": pick["jd_summary"],
                  "kept_postings": len(rs), "in_live_campaign": "yes" if u in live_cos else "no"})
json.dump(comps, open(os.path.join(RAW, "companies.json"), "w"))
pp = os.path.join(RAW, "people.jsonl")
done = {json.loads(l)["company_linkedin_url"] for l in open(pp)} if os.path.exists(pp) else set()
def one(c):
    casc = [{"include_title": t, "exclude_title": PEOPLE_EXCLUDE, "location": {"country_code": ["US"]}, "include_headline_search": False}
            for t in (T1[c["segment"]], TIER2, TIER3)]
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc,
                                                  "max_results": 10 if c["in_live_campaign"] == "yes" else 5})
    return {"company_linkedin_url": c["company_linkedin_url"], "results": r.get("results") or [], "error": r.get("_error"),
            "used": (r.get("fair_usage") or {}).get("records_used", 0)}
used = 0
with ThreadPoolExecutor(12) as ex, open(pp, "a") as f:
    for i, r in enumerate(ex.map(one, [c for c in comps if c["company_linkedin_url"] not in done])):
        used += r["used"]; f.write(json.dumps(r) + "\n")
        if i % 200 == 0: f.flush(); print(i, flush=True)
u = json.load(open(os.path.join(RAW, "usage.json"))) if os.path.exists(os.path.join(RAW, "usage.json")) else {}
u["waterfall"] = u.get("waterfall", 0) + used; json.dump(u, open(os.path.join(RAW, "usage.json"), "w"))
cm = {c["company_linkedin_url"]: c for c in comps}; out = []; seen = set()
for l in open(pp):
    d = json.loads(l); c = cm[d["company_linkedin_url"]]
    for p in d["results"]:
        q = p["person"]; url = norm(q.get("linkedin_url")); exp = (q.get("experiences") or [{}])[0]
        title = exp.get("job_title") or (q.get("headline") or "").split(" | @")[0] or "-"; loc = q.get("location") or {}
        last = SUFFIX.sub("", q.get("last_name") or "").strip()
        if not url or url in seen: continue
        seen.add(url)
        st = "launch set"
        if url in held or ((q.get("first_name") or "").lower(), (q.get("last_name") or "").lower(), c["company_linkedin_url"]) in held_names:
            st = "removed: already in 734516/756466"
        elif not PERSONA.search(title) or (OFF.search(title) and p.get("icp") != 1): st = "removed: title outside persona"
        out.append({"linkedin_url": q["linkedin_url"], "first_name": q.get("first_name") or "-", "last_name": last or "-",
                    "full_name": q.get("full_name") or "-", "job_title": title, "company_name": c["company_name"],
                    "company_linkedin_url": c["company_linkedin_url"], "person_country": loc.get("country_code") or "-", "company_country": "US",
                    "first_name_clean": first_clean(q.get("first_name")) or "-", "waterfall_tier": p.get("icp", "-"), "segment": c["segment"],
                    "vertical": c["vertical"], "company_in_live_campaign": c["in_live_campaign"], "person_state": loc.get("state_code") or "-", "status": st})
with open(os.path.join(RAW, "leads-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
st = collections.Counter((r["segment"], r["status"]) for r in out)
for k in sorted(st): print(k, st[k])
print("companies", len(comps), collections.Counter(c["segment"] for c in comps), "records", u)
