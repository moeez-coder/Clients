"""Builds the wider agency universe groups used by doc2_agency.py (no API calls)."""
import csv, re
from dnc import match
def li(u):
    m = re.search(r"linkedin\.com/company/([^/?#]+)", u or ""); return f"https://www.linkedin.com/company/{m.group(1).lower()}" if m else None
dl = list(csv.DictReader(open("2026-11-18-discolike-agency-lookalike-companies.csv")))
core = list(csv.DictReader(open("2026-11-18-agency-persona-companies.csv")))
seen, groups, removed = set(), {"dl_rank_1_300": [], "dl_rank_301_600": [], "blitz_core_not_in_dl": []}, []
for r in dl:
    u = li(r["company_linkedin_url"]); m = match(r["company_name"])
    if m and not m["review"]: removed.append((r["company_name"], m["dnc_source"])); continue
    if u and u not in seen:
        seen.add(u); groups["dl_rank_1_300" if int(r["rank"]) <= 300 else "dl_rank_301_600"].append(u)
for r in core:
    u = li(r["company_linkedin_url"]); m = match(r["company_name"])
    if m and not m["review"]: removed.append((r["company_name"], m["dnc_source"])); continue
    if u and u not in seen: seen.add(u); groups["blitz_core_not_in_dl"].append(u)
