"""Glassdoor bad-review campaign: the stage-2 lookup list (Moe, 2026-11-17: ICP-form floor of 51 staff, ceiling 5,000, spend cap $10).
Reads 2026-11-17-companies.csv (201+) and 2026-11-17-2-companies.csv (51-200); keeps status=icp, public_sector=no,
size 51-5,000; drops LinkedIn showcase/school pages; dedupes by real domain and by company LinkedIn URL, keeping the
larger company. Sorted largest first and split into batches of BATCH so the best-fit firms are looked up first.
search_query = company name with bracketed text and "now ..."/" - ..." tails removed (Glassdoor search is by name).
Writes 2026-11-17-glassdoor-lookup-input.csv. Usage: python3 -I build_lookup_input.py"""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
CEIL = {"51-200", "201-500", "501-1000", "1001-5000"}
BAD_DOMAINS = {"bit.ly", "linktr.ee", "-", "facebook.com", "linkedin.com", "instagram.com"}
BATCH = 5000

def emp(x):
    return int(x["employees_on_linkedin"]) if x["employees_on_linkedin"].isdigit() else 0

def clean(name):
    n = re.sub(r"\(.*?\)|\[.*?\]", " ", name)
    n = re.split(r"\s+(?:now|formerly|part of)\s+|\s+[-–|]\s+", n, maxsplit=1, flags=re.I)[0]
    return " ".join(n.split()) or name

rows = []
for f in ("2026-11-17-companies.csv", "2026-11-17-2-companies.csv"):
    rows += [x for x in csv.DictReader(open(os.path.join(HERE, f))) if x["status"] == "icp" and x["public_sector"] == "no" and x["size_band"] in CEIL]
seen_dom, seen_li, keep = set(), set(), []
for x in sorted(rows, key=lambda x: (-emp(x), x["company_name"])):
    if "/showcase/" in x["company_linkedin_url"] or "/school/" in x["company_linkedin_url"]:
        continue
    d, l = x["company_domain"], x["company_linkedin_url"]
    if (d not in BAD_DOMAINS and d in seen_dom) or (l != "-" and l in seen_li):
        continue
    seen_dom.add(d); seen_li.add(l); keep.append(x)
out = os.path.join(HERE, "2026-11-17-glassdoor-lookup-input.csv")
assert not os.path.exists(out), "append-only"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["batch", "search_query", "company_name", "company_domain", "company_linkedin_url", "size_band", "employees_on_linkedin", "sector"])
    for i, x in enumerate(keep):
        w.writerow([i // BATCH + 1, clean(x["company_name"]), x["company_name"], x["company_domain"], x["company_linkedin_url"], x["size_band"], x["employees_on_linkedin"], x["sector"]])
print(len(keep), "companies,", (len(keep) - 1) // BATCH + 1, "batches")
