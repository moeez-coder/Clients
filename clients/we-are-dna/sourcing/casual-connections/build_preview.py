"""Combine Blitz + Clay preview rows into the 2026-11-18 wave-1 preview (Casual Connections, We Are DNA).
Rules: UK-located people only; strict C-suite title regex (same as preview_leads.py); max 2 per company, tier 1
(CEO/MD/Managing or Senior Partner/Founder) before tier 2 (CPO/COO/CFO/CMO); DNC (context/dnc-list.csv) excluded.
Rows that fail a check stay in the file with status 'removed: <reason>' so removals are visible.
Usage: python3 build_preview.py  -> 2026-11-18-preview-combined-raw.csv (then tools/leads.py normalize)."""
import csv, json, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
CSUITE = re.compile(r"\b(ceo|chief [a-z &]*officer|c[foptm]o|managing director|managing partner|senior partner|founder|co-founder|owner|executive chair(man|woman)?)\b", re.I)
BAD = re.compile(r"\b(assistant|ea to|pa to|business partner|people partner|product owner|deputy|regional|non[- ]executive|recruit)", re.I)
TIER1 = re.compile(r"\b(ceo|chief executive|managing director|managing partner|senior partner|founder)\b", re.I)
CHARITY = {"hft.org.uk", "sirona-cic.org.uk", "brandontrust.org"}   # charities / CIC: flagged, Moe's scope is private sector
dnc = {r["company_domain"].lower() for r in csv.DictReader(open(os.path.join(HERE, "../../context/dnc-list.csv"))) if r.get("company_domain")}
rows = []
for r in csv.DictReader(open(os.path.join(HERE, "2026-11-18-preview-blitz-raw.csv"))):
    rows.append({**r, "source": "blitz"})
blitz_by_dom = {r["company_domain"]: r for r in rows}
d = json.load(open(os.path.join(HERE, "2026-11-18-preview-clay-raw.json")))
for c in d["contacts"]:
    li = "https://www.linkedin.com/in/" + c["url"].rstrip("/").split("/in/")[-1].lower()
    base = blitz_by_dom.get(c["domain"], {})
    fn, _, ln = re.sub(r"\(.*?\)", "", c["name"]).strip().partition(" ")
    rows.append({"linkedin_url": li, "first_name": fn or "-", "last_name": ln or "-", "job_title": c["latest_experience_title"],
        "company_name": base.get("company_name", c["latest_experience_company"]), "company_domain": c["domain"],
        "company_linkedin_url": base.get("company_linkedin_url", "-"), "industry": base.get("industry", "-"),
        "person_country": "GB" if "United Kingdom" in (c["location_name"] or "") else (c["location_name"] or "-"),
        "company_country": "GB", "sector": base.get("sector", "-"), "size_band": base.get("size_band", "-"),
        "hq_city": base.get("hq_city", "-"), "waterfall_tier": "-", "source": "clay"})
seen, out, per = {}, [], {}
for r in rows:
    if r["linkedin_url"] in seen: seen[r["linkedin_url"]]["source"] = "blitz+clay"; continue
    seen[r["linkedin_url"]] = r
    t = r["job_title"]
    if r["person_country"] != "GB": r["status"] = "removed: not UK-based"
    elif not CSUITE.search(t) or BAD.search(t): r["status"] = "removed: not C-suite"
    elif re.fullmatch(r"(director & )?owner|dental practice owner", t.strip(), re.I): r["status"] = "removed: 'Owner' self-label, not a company owner (check)"
    elif r["first_name"] in ("-", "") or r["last_name"] in ("-", ""): r["status"] = "removed: no name"
    elif r["company_domain"].lower() in dnc: r["status"] = "removed: DNC"
    elif r["company_domain"] in CHARITY: r["status"] = "removed: charity / CIC, not private sector (check with Moe)"
    else: r["status"] = "preview"
    r["tier"] = "1" if TIER1.search(t) else "2"
    out.append(r)
# cap 2 per company, tier 1 first
out.sort(key=lambda r: (r["company_domain"], r["status"] != "preview", r["tier"]))
for r in out:
    if r["status"] == "preview":
        per[r["company_domain"]] = per.get(r["company_domain"], 0) + 1
        if per[r["company_domain"]] > 2: r["status"] = "removed: over 2-per-company cap"
f = os.path.join(HERE, "2026-11-18-preview-combined-raw.csv")
with open(f, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
from collections import Counter
print(len(out), Counter(r["status"] for r in out), Counter(r["source"] for r in out if r["status"] == "preview"))
