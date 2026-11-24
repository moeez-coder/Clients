"""Resolve domain-only list sources to firmographics with Blitz (plan records), so their precision can be
scored on the same size / HQ rules as the API sources:
  POST /v2/enrichment/domain-to-linkedin  (domain -> company LinkedIn URL, 1 record on success)
  POST /v2/enrichment/company             (LinkedIn URL -> size, employees, HQ state, industry, type, 1 record)
Inputs: Exa (mfg + fls), Apify Google Maps (fls), NFSA directory (fls), FABTECH 2025 NC/SC (mfg) sample CSVs.
Output: 2026-11-24-domain-resolution.csv (one row per domain; `found=no` rows kept so misses are visible)."""
import csv, json, os
from concurrent.futures import ThreadPoolExecutor
from common import HERE, http, norm_domain, norm_li

K = {"x-api-key": os.environ["BLITZ_API_KEY"]}
D = "2026-11-24"
SRC = [("exa", "mfg", f"{D}-exa-mfg-sample.csv", "company_domain"), ("exa", "fls", f"{D}-exa-fls-sample.csv", "company_domain"),
       ("apify-googlemaps", "fls", f"{D}-apify-googlemaps-fls-sample.csv", "company_domain"),
       ("nfsa", "fls", f"{D}-nonapi-nfsa-contractors-sample.csv", "domain"),
       ("fabtech", "mfg", f"{D}-nonapi-fabtech2025-ncsc-sample.csv", "domain")]
todo = {}
for src, sl, f, col in SRC:
    for r in csv.DictReader(open(os.path.join(HERE, f))):
        d = norm_domain(r.get(col, ""))
        if d: todo.setdefault(d, set()).add(f"{src}:{sl}")
# Exa rows that are LinkedIn company pages already carry the URL
li_rows = {}
for sl in ("mfg", "fls"):
    for r in csv.DictReader(open(os.path.join(HERE, f"{D}-exa-{sl}-sample.csv"))):
        if norm_li(r["company_linkedin_url"]): li_rows[norm_li(r["company_linkedin_url"])] = {f"exa:{sl}"}


def one(item):
    d, li = item
    if not li:
        st, r = http("POST", "https://api.blitz-api.ai/v2/enrichment/domain-to-linkedin", K, {"domain": d})
        li = r.get("company_linkedin_url") if r.get("found") else None
    if not li: return d, None, None
    st, c = http("POST", "https://api.blitz-api.ai/v2/enrichment/company", K, {"company_linkedin_url": li})
    return d, li, (c.get("company") if c.get("found") else None)


items = [(d, None) for d in todo] + [("", "https://www." + l) for l in li_rows]
rows = []
with ThreadPoolExecutor(8) as ex:
    for d, li, c in ex.map(one, items):
        c = c or {}; hq = c.get("hq") or {}
        rows.append({"company_domain": d or norm_domain(c.get("domain")) or "-", "company_linkedin_url": li or "-",
                     "found": "yes" if c else "no", "company_name": c.get("name") or "-", "size": c.get("size") or "-",
                     "employees": c.get("employees_on_linkedin") if c.get("employees_on_linkedin") is not None else "-",
                     "revenue": c.get("revenue_range") or "-", "hq_city": hq.get("city") or "-", "hq_state": hq.get("state") or "-",
                     "industry": c.get("industry") or "-", "ownership_type": c.get("type") or "-",
                     "listed_by": "|".join(sorted(todo.get(d) or li_rows.get(norm_li(li or ""), set())))})
with open(os.path.join(HERE, f"{D}-domain-resolution.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
print("domains", len(items), "resolved", sum(1 for r in rows if r["found"] == "yes"),
      "201-1000:", sum(1 for r in rows if r["size"] in ("201-500", "501-1000")))
