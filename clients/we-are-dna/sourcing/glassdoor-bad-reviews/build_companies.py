"""Glassdoor bad-review campaign (We Are DNA): raw Blitz pull -> <date>-companies.csv.
- dedupe on company LinkedIn URL (a company can match several sectors' industry lists)
- exclude DNC (../../context/dnc-list.csv, 143 companies) on domain OR normalised name
- exclude Campaign 6 companies: every company in ../pe-investment-triggers/2026-11-16-companies-qualified.csv
  (all 280 candidates, qualified or not, by LinkedIn URL or name) and every company in its 491-lead snapshot
- flag public sector (NHS, councils, police, universities...) as `public_sector=yes`; kept, not dropped
Every excluded row stays in the file with `status` = "excluded: <reason>", so the drop-off is visible.
Usage: python3 build_companies.py 2026-11-17"""
import csv, json, os, re, sys
from urllib.parse import urlparse
HERE = os.path.dirname(os.path.abspath(__file__))
date = sys.argv[1]
SECT = {"1-health-care-medical": "Health, care, vet", "2-retail-hospitality": "Retail, hospitality",
        "3-manufacturing-engineering-automotive-defence": "Manufacturing, engineering",
        "4-law-accounting-top100": "Law, accounting", "5-financial-services": "Financial services"}

def host(u):
    u = (u or "").strip().lower()
    if not u or u == "-": return ""
    h = urlparse(u if "://" in u else "https://" + u).netloc
    return h[4:] if h.startswith("www.") else h

SUFFIX = r"\b(ltd|limited|plc|llp|group|uk|holdings|the|inc|co|company|& co|services)\b"
def nname(s):
    s = re.sub(r"\(.*?\)", " ", (s or "").lower()).replace("&", " and ")
    s = re.sub(SUFFIX, " ", s); s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())

def li(u):
    u = (u or "").strip().lower().rstrip("/")
    m = re.search(r"linkedin\.com/company/([^/?#]+)", u)
    return m.group(1) if m else ""

dnc = list(csv.DictReader(open(os.path.join(HERE, "..", "..", "context", "dnc-list.csv"))))
dnc_dom = {host(r["company_domain"]): r["company_name"] for r in dnc if host(r["company_domain"])}
dnc_nm = {nname(r["company_name"]): r["company_name"] for r in dnc}
pe = os.path.join(HERE, "..", "pe-investment-triggers")
c6_li, c6_nm = set(), set()
for r in csv.DictReader(open(os.path.join(pe, "2026-11-16-companies-qualified.csv"))):
    c6_li.add(li(r["company_linkedin_url"])); c6_nm.add(nname(r["company_name"]))
for r in csv.DictReader(open(os.path.join(pe, "2026-11-16-3-leads.csv"))):
    c6_li.add(li(r["company_linkedin_url"])); c6_nm.add(nname(r["company_name"]))
c6_li.discard(""); c6_nm.discard("")
PUBLIC = re.compile(r"\b(nhs|council|police|constabulary|university|college|hm |ministry|government|"
                    r"department for|borough|county|fire and rescue|ambulance service|health board|"
                    r"integrated care|foundation trust|nhs trust|clinical commissioning)\b", re.I)

rows, seen = {}, {}
import gzip
RAW = os.path.join(HERE, f"{date}-companies-blitz-raw.jsonl.gz")  # pull_companies.py writes .jsonl; gzip -9 it after
for line in gzip.open(RAW, "rt"):
    j = json.loads(line); r = j["record"]; key = li(r.get("linkedin_url")) or r.get("name")
    if key in rows:
        if SECT[j["segment"]] not in rows[key]["sectors"]: rows[key]["sectors"].append(SECT[j["segment"]])
        continue
    rows[key] = dict(r=r, sectors=[SECT[j["segment"]]], band=j["band"])

out = []
for key, x in rows.items():
    r = x["r"]; dom = host(r.get("domain") or r.get("website")); nm = nname(r.get("name"))
    if dom and dom in dnc_dom: status = f"excluded: DNC (domain match, {dnc_dom[dom]})"
    elif nm and nm in dnc_nm: status = f"excluded: DNC (name match, {dnc_nm[nm]})"
    elif li(r.get("linkedin_url")) in c6_li: status = "excluded: in Campaign 6 (LinkedIn match)"
    elif nm in c6_nm: status = "excluded: in Campaign 6 (name match)"
    else: status = "icp"
    hq = r.get("hq") or {}
    out.append({
        "company_name": r.get("name") or "-", "company_domain": dom or "-",
        "company_linkedin_url": (r.get("linkedin_url") or "-"), "sector": "; ".join(x["sectors"]),
        "industry": r.get("industry") or "-", "size_band": r.get("size") or "-",
        "employees_on_linkedin": r.get("employees_on_linkedin") if r.get("employees_on_linkedin") is not None else "-",
        "revenue_range": r.get("revenue_range") or "-", "company_type": r.get("type") or "-",
        "hq_city": hq.get("city") or "-", "public_sector": "yes" if PUBLIC.search(r.get("name") or "") or
            (r.get("type") or "").lower().startswith("government") else "no",
        "status": status, "source_tool": "Blitz API POST /v2/search/companies",
    })
out.sort(key=lambda d: (d["status"] != "icp", -(d["employees_on_linkedin"] if isinstance(d["employees_on_linkedin"], int) else 0)))
p = os.path.join(HERE, f"{date}-companies.csv")
assert not os.path.exists(p), f"{p} exists; snapshots are append-only"
with open(p, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
from collections import Counter
print("raw lines", sum(1 for _ in gzip.open(RAW, "rt")), "unique", len(out))
print(Counter(d["status"].split(" (")[0] for d in out))
icp = [d for d in out if d["status"] == "icp"]
print("icp public_sector", Counter(d["public_sector"] for d in icp))
print("icp by band", Counter(d["size_band"] for d in icp if d["public_sector"] == "no"))
print("icp by sector (first)", Counter(d["sector"].split(';')[0] for d in icp if d["public_sector"] == "no"))
