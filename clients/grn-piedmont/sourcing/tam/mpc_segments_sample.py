"""Reachability + posting-open sample for the GRN MPC segment proposal (2026-11-24). Seeded, so it reproduces.

A. Net-new companies (not in the live campaign): up to 12 per role family (all 3 for F&LS) -> Blitz API
   POST /v2/search/waterfall-icp-keyword, same tiers/excludes as the live campaign (../recruitment-specific-open-roles/spec.py),
   max_results 5 (F&LS 4). Measures reachable persona contacts per new company.
B. 30 companies already in the live campaign -> same waterfall, max_results 10. People already in 734516/756466 are flagged
   afterwards by tools/leads.py overlap; measures how many *uncontacted* persona contacts are left there.
C. Posting still open? 40 postings aged 60-120 days vs 40 aged under 30 days, read from the public posting page
   (GET linkedin.com/jobs-guest/jobs/api/jobPosting/<id>, as pull_job_descriptions.py). Closed = 404/410 or
   "No longer accepting applications".
Outputs (raw in $RAW): 2026-11-24-mpc-segments-sample-leads-raw.csv (normalised next by tools/leads.py), -posting-check.csv, usage json.
Usage: RAW=/path python3 mpc_segments_sample.py"""
import csv, json, os, re, sys, random, time, collections, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); LIVE = os.path.join(HERE, "..", "recruitment-specific-open-roles")
sys.path.insert(0, HERE); sys.path.insert(0, LIVE)
from tam_counts import post
from spec import TIER1, TIER2, TIER3, PEOPLE_EXCLUDE
from build_leads import PERSONA, OFF, SUFFIX, first_clean
RAW = os.environ.get("RAW") or os.path.join(HERE, "raw-mpc"); DATE = "2026-11-24"; random.seed(20261124)
T1 = {"executive": TIER1["executive-finance-hr"], "operations-plant": TIER1["operations-plant-leadership"],
      "engineering-quality": TIER1["engineering-quality"], "supply-chain-purchasing": TIER1["supply-chain-purchasing"],
      "ehs-maintenance": TIER1["operations-plant-leadership"], "fire-life-safety": TIER1["fire-life-safety"]}
comps = list(csv.DictReader(open(os.path.join(HERE, f"{DATE}-mpc-segments-companies.csv"))))
jobs = [r for r in csv.DictReader(open(os.path.join(HERE, f"{DATE}-mpc-segments-jobs.csv"))) if r["status"] == "kept"]
def main_family(c): return "fire-life-safety" if c["vertical"] == "fire-life-safety" else c["role_families"].split(":")[0]
sample = []
for fam in T1:
    pool = [c for c in comps if c["in_live_campaign"] == "no" and main_family(c) == fam]
    for c in random.sample(pool, min(12, len(pool))): sample.append({**c, "family": fam, "set": "A net-new", "max": 4 if fam == "fire-life-safety" else 5})
for c in random.sample([c for c in comps if c["in_live_campaign"] == "yes" and c["vertical"] != "fire-life-safety"], 30):
    sample.append({**c, "family": main_family(c), "set": "B live company", "max": 10})

def one(c):
    casc = [{"include_title": t, "exclude_title": PEOPLE_EXCLUDE, "location": {"country_code": ["US"]}, "include_headline_search": False}
            for t in (T1[c["family"]], TIER2, TIER3)]
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc, "max_results": c["max"]})
    return c, r.get("results") or [], (r.get("fair_usage") or {}).get("records_used", 0), r.get("_error")
rows, used = [], 0
with ThreadPoolExecutor(8) as ex:
    for c, res, u, err in ex.map(one, sample):
        used += u
        if err: print("ERR", c["company_name"], err)
        if not res:
            rows.append({"linkedin_url": "-", "first_name": "-", "last_name": "-", "full_name": "-", "job_title": "-", "company_name": c["company_name"],
                         "company_linkedin_url": c["company_linkedin_url"], "waterfall_tier": "-", "sample_set": c["set"], "segment_family": c["family"],
                         "vertical": c["vertical"], "status": "no persona match"})
        for p in res:
            q = p["person"]; exp = (q.get("experiences") or [{}])[0]
            title = exp.get("job_title") or (q.get("headline") or "").split(" | @")[0] or "-"
            st = "persona" if q.get("linkedin_url") and PERSONA.search(title) and not (OFF.search(title) and p.get("icp") != 1) else "removed: title outside persona"
            rows.append({"linkedin_url": q.get("linkedin_url") or "-", "first_name": q.get("first_name") or "-",
                         "last_name": SUFFIX.sub("", q.get("last_name") or "").strip() or "-", "full_name": q.get("full_name") or "-",
                         "job_title": title, "company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"],
                         "waterfall_tier": p.get("icp", "-"), "sample_set": c["set"], "segment_family": c["family"], "vertical": c["vertical"], "status": st})
with open(os.path.join(RAW, f"{DATE}-mpc-segments-sample-leads-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("sample companies", collections.Counter(c["set"] for c in sample), "rows", len(rows), "records", used)

# ---- C. posting open check
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36", "Accept-Language": "en-US"}
import datetime; T = datetime.date(2026, 11, 24)
age = lambda r: (T - datetime.date.fromisoformat(r["date_posted"])).days
mfg = [r for r in jobs if r["segment_vertical"] != "fire-life-safety"]
chk = [dict(r, bucket="60-120d") for r in random.sample([r for r in mfg if age(r) >= 60], 40)] + \
      [dict(r, bucket="0-29d") for r in random.sample([r for r in mfg if age(r) < 30], 40)]
def openchk(r):
    m = re.search(r"(\d{8,})", r["job_url"]); st, closed = 0, None
    if not m: return {**r, "http_status": "-", "closed": "-"}
    for a in range(4):
        try:
            t = urllib.request.urlopen(urllib.request.Request(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{m.group(1)}", headers=UA), timeout=40).read().decode("utf8", "replace")
            st, closed = 200, "No longer accepting applications" in t; break
        except urllib.error.HTTPError as e:
            st = e.code
            if e.code in (404, 410): closed = True; break
            time.sleep(3 * (a + 1))
        except Exception: st = -1; time.sleep(3)
    time.sleep(0.4)
    return {"bucket": r["bucket"], "age_days": age(r), "role_family": r["role_family"], "title": r["title"], "company_name": r["company_name"],
            "date_posted": r["date_posted"], "job_url": r["job_url"], "http_status": st, "closed": "-" if closed is None else ("yes" if closed else "no")}
with ThreadPoolExecutor(4) as ex: res = list(ex.map(openchk, chk))
with open(os.path.join(HERE, f"{DATE}-mpc-segments-posting-check.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(res[0].keys())); w.writeheader(); w.writerows(res)
for b in ("60-120d", "0-29d"):
    x = [r for r in res if r["bucket"] == b]; print(b, collections.Counter(r["closed"] for r in x), collections.Counter(r["http_status"] for r in x))
json.dump({"waterfall_records_used": used}, open(os.path.join(HERE, f"{DATE}-mpc-segments-sample-usage.json"), "w"))
