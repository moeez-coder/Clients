"""Campaign 6 qualification via Exa (the GTM Sheets AI column's web tools were out of credits on 2026-11-16).
For each candidate in 2026-11-16-companies.csv:
  1) Exa POST /contents on the source article with a structured summary that applies the qualification rules.
  2) Exa POST /search (includeDomains linkedin.com, category company) to find the company's LinkedIn page.
Writes 2026-11-16-companies-qualified.csv (all candidates, with qualified yes/no and reason) and prints cost.
Usage: python3 qualify_exa.py
"""
import csv, json, os, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
H = {"x-api-key": os.environ["EXA_API_KEY"], "Content-Type": "application/json", "User-Agent": "curl/8.5.0"}
HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = {"type": "object", "properties": {
 "target_company": {"type": "string", "description": "the company that RECEIVED the investment or was bought"},
 "is_target_named_company": {"type": "boolean", "description": "true if the target is the named company (not the investor, fund, REIT or the acquiring platform)"},
 "private_equity_equity_deal": {"type": "boolean", "description": "true if a private equity firm (or a PE-backed platform) took an equity stake or bought it; false for debt, trade sale to a non-PE corporate, administration, listing"},
 "uk_headquartered": {"type": "boolean"},
 "employees": {"type": "number", "description": "employee count if stated, else 0"},
 "deal_date": {"type": "string", "description": "YYYY-MM-DD the deal was announced, or empty"},
 "investor": {"type": "string"},
 "deal_line": {"type": "string", "description": "6 to 12 words for a message, e.g. 'the investment from Bridgepoint'"}},
 "required": ["target_company", "is_target_named_company", "private_equity_equity_deal", "uk_headquartered", "employees", "deal_date", "investor", "deal_line"]}
def post(path, body):
    for a in range(5):
        try:
            r = urllib.request.Request("https://api.exa.ai" + path, json.dumps(body).encode(), H, method="POST")
            return json.load(urllib.request.urlopen(r, timeout=120))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 ** a + 1); continue
            return {"_error": e.code}
        except Exception:
            time.sleep(2 ** a)
    return {"_error": "retries"}
def one(c):
    cost = 0.0
    r = post("/contents", {"urls": [c["source_url"]], "summary": {"query": f"About {c['company_name']}: extract the private equity deal and check each field.", "schema": SCHEMA}})
    cost += (r.get("costDollars") or {}).get("total", 0) or 0
    s = {}
    try: s = json.loads(r["results"][0]["summary"])
    except Exception: pass
    q = post("/search", {"query": f"{c['company_name']} UK company LinkedIn page", "numResults": 3, "includeDomains": ["linkedin.com"], "category": "company"})
    cost += (q.get("costDollars") or {}).get("total", 0) or 0
    li = "-"
    for x in q.get("results", []):
        u = (x.get("url") or "").split("?")[0].rstrip("/")
        if re.match(r"https?://([a-z]{2,3}\.)?linkedin\.com/company/[^/]+$", u): li = re.sub(r"https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", u); break
    reasons = []
    if not s: reasons.append("article could not be read")
    else:
        if not s.get("is_target_named_company"): reasons.append("named company is not the deal target")
        if not s.get("private_equity_equity_deal"): reasons.append("not a private equity equity deal")
        if s.get("uk_headquartered") is False: reasons.append("not UK headquartered")
        emp = s.get("employees") or 0
        if emp and emp <= 50: reasons.append(f"only {int(emp)} employees")
        dd = s.get("deal_date") or ""
        if dd and dd < "2026-05-18": reasons.append(f"deal announced {dd}, before the window")
    if li == "-": reasons.append("no LinkedIn company page found")
    out = dict(c)
    out.update(qualified="yes" if not reasons else "no", reason="; ".join(reasons) or "meets all rules",
               company_linkedin_url=li, employees_stated=int(s.get("employees") or 0) if s else "-",
               deal_date=s.get("deal_date") or "-", deal_line=s.get("deal_line") or "-", exa_cost_usd=round(cost, 4))
    return out
rows = list(csv.DictReader(open(os.path.join(HERE, "2026-11-16-companies.csv"))))
with ThreadPoolExecutor(4) as ex: res = list(ex.map(one, rows))
with open(os.path.join(HERE, "2026-11-16-companies-qualified.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(res[0])); w.writeheader(); w.writerows(res)
from collections import Counter
print("candidates", len(res), "qualified", sum(r["qualified"] == "yes" for r in res), "cost_usd", round(sum(r["exa_cost_usd"] for r in res), 2))
print(Counter(r["sector"] for r in res if r["qualified"] == "yes"))
print(Counter(x.strip() for r in res for x in r["reason"].split(";")).most_common(10))
