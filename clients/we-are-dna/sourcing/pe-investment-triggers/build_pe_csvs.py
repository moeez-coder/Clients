"""Build campaign 6 funnel CSVs from the Exa news pull (2026-11-16-exa-news-raw.json).
1) 2026-11-16-pe-deal-news.csv : every article, one row, with status kept / dropped:<reason>
2) 2026-11-16-companies.csv     : one row per distinct candidate company from kept articles (first-pass, deterministic),
   which GTM Sheets then qualifies (AI column) before any leads are found.
Usage: python3 build_pe_csvs.py
"""
import csv, json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "2026-11-16-exa-news-raw.json")))["results"]
SEG = {"1-health-care-vet-dental": "Health, care, vet and dental", "2-retail-hospitality": "Retail and hospitality",
       "3-manufacturing-engineering": "Manufacturing and engineering", "4-law-accounting": "Law and accounting",
       "5-financial-services": "Financial services"}
INVESTORISH = re.compile(r"\b(reit|capital|partners|investors|equity|fund|holdings? inc|private equity|bank|blue owl|welltower|omega)\b", re.I)
def norm(n): return re.sub(r"\b(ltd|limited|plc|group|llp|holdings?|uk)\b", "", re.sub(r"[^a-z0-9 ]+", " ", n.lower())).split() and " ".join(re.sub(r"\b(ltd|limited|plc|group|llp|holdings?|uk)\b", "", re.sub(r"[^a-z0-9 ]+", " ", n.lower())).split())
deals = []
for seg, items in raw.items():
    for x in items:
        s = x["summary"]; s = json.loads(s) if isinstance(s, str) else (s or {})
        name, inv, dt = (s.get("company_name") or "").strip(), (s.get("investor") or "").strip(), (s.get("deal_type") or "").strip()
        uk = s.get("uk_headquartered")
        if not name or name.lower() in ("null", "none") or "not determinable" in name.lower() or len(name) > 80: st = "dropped: no single company named"
        elif "not a pe" in dt.lower() or dt.lower() in ("null", ""): st = "dropped: not a private equity deal"
        elif re.search(r"\b(loan|debt|facility|refinanc)", dt, re.I): st = "dropped: debt financing, not equity"
        elif uk is not True: st = "dropped: not UK headquartered"
        elif not inv or inv.lower() in ("null", "not disclosed", "none"): st = "dropped: investor not named"
        elif INVESTORISH.search(name): st = "dropped: company named is an investor or REIT"
        else: st = "kept"
        deals.append({"sector": SEG[seg], "company_name": name or "-", "investor": inv or "-", "deal_type": dt or "-",
                      "uk_headquartered": {True: "yes", False: "no"}.get(uk, "-"), "employees_mentioned": s.get("employees_mentioned") or "-",
                      "published": (x["published"] or "-")[:10], "article_title": x["title"] or "-", "source_url": x["url"],
                      "search_query": x["query"], "status": st, "company_key": norm(name) or "-"})
with open(os.path.join(HERE, "2026-11-16-pe-deal-news.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(deals[0])); w.writeheader(); w.writerows(deals)
comp = {}
for d in deals:
    if d["status"] != "kept": continue
    k = d["company_key"]
    if k not in comp:
        comp[k] = {"company_name": d["company_name"], "sector": d["sector"], "investor": d["investor"], "deal_type": d["deal_type"],
                   "latest_article_date": d["published"], "source_url": d["source_url"], "article_count": 0}
    c = comp[k]; c["article_count"] += 1
    if d["published"] > c["latest_article_date"]: c.update(latest_article_date=d["published"], source_url=d["source_url"], investor=d["investor"], deal_type=d["deal_type"])
rows = sorted(comp.values(), key=lambda r: (r["sector"], r["company_name"].lower()))
with open(os.path.join(HERE, "2026-11-16-companies.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter
print("articles", len(deals), Counter(d["status"] for d in deals).most_common())
print("companies", len(rows), Counter(r["sector"] for r in rows).most_common())
