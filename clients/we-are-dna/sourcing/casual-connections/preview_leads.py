"""Casual Connections wave-1 PREVIEW (2026-11-18): Blitz POST /v2/search/waterfall-icp-keyword on Bristol-HQ
TAM companies (glassdoor lookup-input list: private sector ICP, 51-5,000 staff, DNC + Campaign 6 already excluded).
C-suite only, UK only, max 2 per company. LinkedIn URLs only, no emails. Usage: python3 preview_leads.py
Writes 2026-11-18-preview-waterfall-raw.jsonl and 2026-11-18-preview-blitz-raw.csv (normalised after via tools/leads.py)."""
import csv, json, os, re, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
HERE = os.path.dirname(os.path.abspath(__file__)); GD = os.path.join(HERE, "..", "glassdoor-bad-reviews")
EXCL = ["Assistant", "Intern", "PA to", "Recruiter", "Talent Acquisition", "Sales", "Non-Executive", "Non Executive", "Advisor",
        "Board Member", "Deputy", "Regional", "Area", "Store", "Branch", "Site", "Practice Manager", "Account", "Business Partner", "People Partner", "Product Owner", "EA to", "Recruitment", "Finance Partner", "HR Partner"]
CASCADE = [
 {"include_title": ["CEO", "Chief Executive Officer", "Managing Director", "Group Managing Director", "Managing Partner", "Senior Partner", "Founder", "Owner"],
  "exclude_title": EXCL, "location": {"country_code": ["GB"]}, "include_headline_search": False},
 {"include_title": ["Chief People Officer", "Chief Operating Officer", "COO", "Chief Financial Officer", "CFO", "Chief Marketing Officer", "CMO", "Chief HR Officer"],
  "exclude_title": EXCL, "location": {"country_code": ["GB"]}, "include_headline_search": False}]
USED = [0]; DROPPED = []
def post(body):
    for a in range(6):
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
inp = {r["company_linkedin_url"]: r for r in csv.DictReader(open(os.path.join(GD, "2026-11-17-glassdoor-lookup-input.csv")))}
bristol = []
for f in ["2026-11-17-companies.csv", "2026-11-17-2-companies.csv"]:
    for r in csv.DictReader(open(os.path.join(GD, f))):
        if r["company_linkedin_url"] in inp and "bristol" in r["hq_city"].lower():
            bristol.append(r)
bristol.sort(key=lambda r: -int(r["employees_on_linkedin"]) if r["employees_on_linkedin"].isdigit() else 0)
# spread: take up to 4 per sector, largest first, 20 companies
pick, per = [], {}
for r in bristol:
    if per.get(r["sector"], 0) < 4: pick.append(r); per[r["sector"]] = per.get(r["sector"], 0) + 1
    if len(pick) == 20: break
with ThreadPoolExecutor(8) as ex:
    res = list(ex.map(lambda c: (c, post({"company_linkedin_url": c["company_linkedin_url"], "cascade": CASCADE, "max_results": 2})), pick))
with open(os.path.join(HERE, "2026-11-18-preview-waterfall-raw.jsonl"), "w") as f:
    for c, r in res: f.write(json.dumps({"company_linkedin_url": c["company_linkedin_url"], "response": r}) + "\n")
CSUITE = re.compile(r"\b(ceo|chief [a-z &]*officer|c[foptm]o|managing director|group managing director|managing partner|senior partner|founder|co-founder|owner|executive chair(man|woman)?)\b", re.I)
BAD = re.compile(r"\b(assistant|ea to|pa to|business partner|people partner|product owner|deputy|regional|non[- ]executive|recruit)", re.I)
leads, seen = [], set()
for c, r in res:
    for p in r.get("results", []):
        person = p.get("person") or p
        li = norm(person.get("linkedin_url") or p.get("linkedin_url"))
        if not li or li in seen: continue
        title = person.get("job_title") or (person.get("experiences") or [{}])[0].get("job_title") or "-"
        if not CSUITE.search(title) or BAD.search(title): DROPPED.append((c["company_name"], title)); continue
        seen.add(li)
        loc = person.get("location") or {}
        leads.append({"linkedin_url": li, "first_name": person.get("first_name") or "-", "last_name": (person.get("last_name") or "-").split(",")[0].strip(),
            "job_title": person.get("job_title") or (person.get("experiences") or [{}])[0].get("job_title") or "-",
            "company_name": c["company_name"], "company_domain": c["company_domain"], "company_linkedin_url": c["company_linkedin_url"],
            "industry": c["industry"], "person_country": (loc.get("country_code") if isinstance(loc, dict) else "-") or "GB",
            "company_country": "GB", "sector": c["sector"], "size_band": c["size_band"], "hq_city": c["hq_city"], "waterfall_tier": p.get("icp") or "-"})
with open(os.path.join(HERE, "2026-11-18-preview-blitz-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(leads[0])); w.writeheader(); w.writerows(leads)
print("bristol companies", len(bristol), "picked", len(pick), "with leads", sum(1 for _, r in res if r.get("results")), "leads", len(leads), "blitz records", USED[0],
      "dropped (not C-suite)", DROPPED, "errors", [r.get("_body") for _, r in res if r.get("_error")][:3])
