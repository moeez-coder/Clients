"""Campaign 6 leads: Blitz POST /v2/search/waterfall-icp-keyword per qualified company (2026-11-16).
Tier 1 CEO / MD / Managing or Senior Partner / Founder; tier 2 CPO / People Director / HR Director / COO. UK only,
max 3 per company (small trigger pool -> deeper per company, CLAUDE.md inverse rule). LinkedIn URLs only, no emails.
Writes 2026-11-16-waterfall-raw.jsonl and 2026-11-16-leads.csv (linkedin_url first). Usage: python3 pull_leads.py
"""
import csv, json, os, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__))
EXCL = ["Assistant", "Intern", "Executive Assistant", "PA to", "Recruiter", "Talent Acquisition", "Sales", "Non-Executive", "Non Executive", "Advisor", "Board Member"]
CASCADE = [
 {"include_title": ["CEO", "Chief Executive Officer", "Managing Director", "Managing Partner", "Senior Partner", "Founder", "Group Managing Director"], "exclude_title": EXCL, "location": {"country_code": ["GB"]}, "include_headline_search": False},
 {"include_title": ["Chief People Officer", "People Director", "HR Director", "Group HR Director", "Director of People", "Human Resources Director", "Chief Operating Officer", "Chief HR Officer"], "exclude_title": EXCL, "location": {"country_code": ["GB"]}, "include_headline_search": False}]
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
comps = [r for r in csv.DictReader(open(os.path.join(HERE, "2026-11-16-companies-qualified.csv"))) if r["qualified"] == "yes"]
with ThreadPoolExecutor(10) as ex:
    res = list(ex.map(lambda c: (c, post({"company_linkedin_url": c["company_linkedin_url"], "cascade": CASCADE, "max_results": 3})), comps))
with open(os.path.join(HERE, "2026-11-16-waterfall-raw.jsonl"), "w") as f:
    for c, r in res: f.write(json.dumps({"company_linkedin_url": c["company_linkedin_url"], "response": r}) + "\n")
leads, seen = [], set()
for c, r in res:
    for p in r.get("results", []):
        person = p.get("person") or p
        li = norm(person.get("linkedin_url") or p.get("linkedin_url"))
        if not li or li in seen: continue
        seen.add(li)
        last = (person.get("last_name") or "").split(",")[0].strip()
        leads.append({"linkedin_url": li, "first_name": person.get("first_name") or "-", "last_name": last or "-",
                      "title": person.get("job_title") or person.get("title") or (person.get("experiences") or [{}])[0].get("job_title") or "-",
                      "waterfall_tier": p.get("icp") or "-", "company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"],
                      "sector": c["sector"], "investor": c["investor"], "deal_date": c["deal_date"], "deal_line": c["deal_line"],
                      "source_url": c["source_url"], "status": "launch set"})
with open(os.path.join(HERE, "2026-11-16-leads.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(leads[0])); w.writeheader(); w.writerows(leads)
found = sum(1 for _, r in res if r.get("results"))
print("companies", len(comps), "with leads", found, "leads", len(leads), "blitz records", USED[0], "errors", [r.get("_body") for _, r in res if r.get("_error")][:3])
