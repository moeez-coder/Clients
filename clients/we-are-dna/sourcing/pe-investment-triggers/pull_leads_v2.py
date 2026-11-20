"""Campaign 6 leads, expansion pass (2026-11-16, Moe: "expand the leads have at least 5 per company").
Blitz POST /v2/search/waterfall-icp-keyword per qualified company, UK only, max_results 6, four priority tiers:
  1 CEO / MD / Managing or Senior Partner / Founder   2 CPO / People or HR Director / COO
  3 CFO, Finance, Commercial, Operations, Marketing, Brand Directors; Head of People / HR (just below C-suite)
  4 other Director / Head of titles (fills the count where the top tiers are thin)
Excludes the 'Business Partner' style titles that slipped through the first pass.
Writes 2026-11-16-2-waterfall-raw.jsonl and 2026-11-16-2-leads.csv (new snapshot; the first pull is kept as is).
Usage: python3 pull_leads_v2.py
"""
import csv, json, os, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
EXCL = ["Assistant", "Intern", "Executive Assistant", "Recruiter", "Talent Acquisition", "Non-Executive", "Non Executive",
        "NED", "Advisor", "Adviser", "Business Partner", "Talent Partner", "People Partner", "Resourcing Partner",
        "Finance Partner", "Analyst", "Coordinator", "Administrator", "Associate Director", "Student", "Trainee"]
T = [["CEO", "Chief Executive Officer", "Managing Director", "Group Managing Director", "Managing Partner", "Senior Partner", "Founder", "Co-Founder"],
     ["Chief People Officer", "People Director", "HR Director", "Group HR Director", "Director of People", "Human Resources Director", "Chief HR Officer", "Chief Operating Officer"],
     ["Chief Financial Officer", "Finance Director", "Chief Commercial Officer", "Commercial Director", "Operations Director", "Marketing Director", "Chief Marketing Officer", "Brand Director", "Head of People", "Head of HR", "Head of Human Resources"],
     ["Director", "Head of"]]
CASCADE = [{"include_title": t, "exclude_title": EXCL, "location": {"country_code": ["GB"]}, "include_headline_search": False} for t in T]
USED = [0]
def post(body):
    for a in range(7):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai/v2/search/waterfall-icp-keyword", json.dumps(body).encode(), H, method="POST")
            d = json.load(urllib.request.urlopen(r, timeout=90)); USED[0] += (d.get("fair_usage") or {}).get("records_used", 0); return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"results": [], "_error": e.code, "_body": e.read()[:300].decode(errors="replace")}
    return {"results": [], "_error": "retries"}
def norm(u):
    u = unquote(u or "").split("?")[0].rstrip("/").lower()
    return re.sub(r"https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", u)
def status(title):
    tl = title.lower()
    if re.search(r"business partner|talent partner|people partner|resourcing partner|private client partner|finance analyst", tl): return "removed: below C-suite (matched on the word Partner)"
    if re.search(r"\bned\b|non-exec", tl): return "removed: non-executive"
    if re.search(r"head of ceo office|chief sustainability officer", tl): return "removed: not a people or business leader for this campaign"
    return "launch set"
comps = [r for r in csv.DictReader(open(os.path.join(HERE, "2026-11-16-companies-qualified.csv"))) if r["qualified"] == "yes"]
with ThreadPoolExecutor(10) as ex:
    res = list(ex.map(lambda c: (c, post({"company_linkedin_url": c["company_linkedin_url"], "cascade": CASCADE, "max_results": 6})), comps))
with open(os.path.join(HERE, "2026-11-16-2-waterfall-raw.jsonl"), "w") as f:
    for c, r in res: f.write(json.dumps({"company_linkedin_url": c["company_linkedin_url"], "response": r}) + "\n")
first = {r["linkedin_url"]: r for r in csv.DictReader(open(os.path.join(HERE, "2026-11-16-leads.csv")))}
leads, seen = [], set()
for c, r in res:
    for p in r.get("results", []):
        per = p.get("person") or {}
        li = norm(per.get("linkedin_url"))
        if not li or li in seen: continue
        seen.add(li)
        title = (per.get("experiences") or [{}])[0].get("job_title") or per.get("headline") or "-"
        prev = first.get(li)
        st = prev["status"] if prev and prev["status"].startswith("removed") else status(title)
        leads.append({"linkedin_url": li, "first_name": per.get("first_name") or "-", "last_name": (per.get("last_name") or "-").split(",")[0].strip(),
                      "title": title, "waterfall_tier": p.get("icp") or "-", "location_country": (per.get("location") or {}).get("country_code") or "-",
                      "company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"], "sector": c["sector"],
                      "investor": c["investor"], "deal_date": c["deal_date"], "deal_line": c["deal_line"], "source_url": c["source_url"],
                      "in_first_pull": "yes" if prev else "no", "status": st})
# keep first-pull leads the new pass did not return (same company), so nothing found earlier is lost
for li, r in first.items():
    if li not in seen:
        leads.append({"linkedin_url": li, "first_name": r["first_name"], "last_name": r["last_name"], "title": r["title"], "waterfall_tier": r["waterfall_tier"],
                      "location_country": "-", "company_name": r["company_name"], "company_linkedin_url": r["company_linkedin_url"], "sector": r["sector"],
                      "investor": r["investor"], "deal_date": r["deal_date"], "deal_line": r["deal_line"], "source_url": r["source_url"],
                      "in_first_pull": "yes", "status": r["status"]})
with open(os.path.join(HERE, "2026-11-16-2-leads.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(leads[0])); w.writeheader(); w.writerows(leads)
from collections import Counter
ok = Counter(l["company_linkedin_url"] for l in leads if l["status"] == "launch set")
dist = Counter(min(ok.get(c["company_linkedin_url"], 0), 5) for c in comps)
print("blitz records", USED[0], "leads", len(leads), "launch set", sum(ok.values()), "new vs first pull", sum(l["in_first_pull"] == "no" for l in leads))
print("companies by launch-set count (5 = 5+):", sorted(dist.items()))
print("errors", [r.get("_body") for _, r in res if r.get("_error")][:3])
