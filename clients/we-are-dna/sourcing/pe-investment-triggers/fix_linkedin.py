"""Re-find LinkedIn company pages for qualified companies whose waterfall returned nobody (2026-11-16).
Exa POST /search on linkedin.com/company (5 results, category company) with the company name, sector and investor;
picks the first /company/ page whose slug or title shares a distinctive word with the name and is not a recruitment page.
Writes 2026-11-16-linkedin-fixes.csv (old url, candidates, chosen url). Usage: python3 fix_linkedin.py
"""
import csv, json, os, re, time, urllib.request
H = {"x-api-key": os.environ["EXA_API_KEY"], "Content-Type": "application/json", "User-Agent": "curl/8.5.0"}
HERE = os.path.dirname(os.path.abspath(__file__))
STOP = {"group","limited","ltd","plc","uk","the","and","of","holdings","company","brand","owned","by","services","care","dental","international","foods","food","engineering","travel","accountants","tyres","baking"}
leads = list(csv.DictReader(open(os.path.join(HERE, "2026-11-16-2-leads.csv"))))
have = {l["company_linkedin_url"] for l in leads}
comps = [r for r in csv.DictReader(open(os.path.join(HERE, "2026-11-16-companies-qualified.csv"))) if r["qualified"] == "yes" and r["company_linkedin_url"] not in have]
out = []
for c in comps:
    name = re.sub(r"\(.*?\)", "", c["company_name"]).strip()
    words = [w for w in re.findall(r"[a-z]+", name.lower()) if w not in STOP and len(w) > 2]
    body = {"query": f"{name} {c['sector']} UK LinkedIn company page", "numResults": 5, "includeDomains": ["linkedin.com"], "category": "company"}
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.exa.ai/search", json.dumps(body).encode(), H, method="POST"), timeout=60))
    cands = []
    for x in r.get("results", []):
        u = re.sub(r"https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", (x.get("url") or "").split("?")[0].rstrip("/"))
        if re.match(r"https://www\.linkedin\.com/company/[^/]+$", u): cands.append((u, x.get("title") or ""))
    pick = "-"
    for u, t in cands:
        hay = (u.rsplit("/", 1)[-1] + " " + t).lower()
        if u == c["company_linkedin_url"] or "recruit" in hay or "careers" in hay: continue
        if words and any(w in hay for w in words): pick = u; break
    out.append({"company_name": c["company_name"], "old_linkedin_url": c["company_linkedin_url"], "candidates": " | ".join(u for u, _ in cands) or "-", "new_linkedin_url": pick})
    print(c["company_name"][:35], "->", pick)
    time.sleep(0.3)
with open(os.path.join(HERE, "2026-11-16-linkedin-fixes.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
