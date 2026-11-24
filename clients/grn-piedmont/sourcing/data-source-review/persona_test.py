"""Persona reach: for the same 15 companies (raw/persona-sample-companies.csv: 10 NC/SC manufacturers found by
both Blitz and Prospeo, 5 fire & life safety companies from Blitz), how many C-level / VP / Owner contacts with a
LinkedIn URL does each people source return?
  Blitz    POST /v2/search/waterfall-icp-keyword (persona titles, Manager/Director excluded, max 10). Plan records.
  Prospeo / ColdIQ people searches are NOT run here: they spend credits outside what Moe approved on 2026-11-24
  and were left for his go-ahead (see the review doc).
Output: 2026-11-24-persona-reach.csv (one row per company)."""
import csv, json, os, re
from common import *
from concurrent.futures import ThreadPoolExecutor

EXEC = ["Chief Executive Officer", "CEO", "[President]", "[Owner]", "[Founder]", "Chief Operating Officer", "COO",
        "Chief Financial Officer", "CFO", "Chief Human Resources Officer", "CHRO", "Vice President", "VP"]
EXCL = ["Manager", "Director", "Assistant", "Coordinator", "Recruiter", "Former", "Sales", "Retired", "Intern"]
EXEC_RE = re.compile(r"\b(chief|ceo|coo|cfo|chro|cto|president|owner|founder|vp|vice president|svp|evp|partner|principal)\b", re.I)
JUNIOR_RE = re.compile(r"\b(manager|director|assistant|coordinator|intern|specialist)\b", re.I)
BK = {"x-api-key": os.environ["BLITZ_API_KEY"]}
comps = list(csv.DictReader(open(os.path.join(HERE, "raw", "persona-sample-companies.csv"))))


def title_of(p):
    p = p.get("person") or p
    return p.get("job_title") or ((p.get("experiences") or [{}])[0].get("job_title")) or ""


def blitz(c):
    st, r = http("POST", "https://api.blitz-api.ai/v2/search/waterfall-icp-keyword", BK,
                 {"company_linkedin_url": c["company_linkedin_url"], "max_results": 10,
                  "cascade": [{"include_title": EXEC, "exclude_title": EXCL, "location": {"country_code": ["US"]},
                               "include_headline_search": False}]})
    return [title_of(p) for p in (r.get("results") or []) if (p.get("person") or p).get("linkedin_url")], st


rows = []
with ThreadPoolExecutor(5) as ex:
    for c, (titles, st) in zip(comps, ex.map(blitz, comps)):
        ex_ = [t for t in titles if t and EXEC_RE.search(t) and not JUNIOR_RE.search(t)]
        rows.append({"company_linkedin_url": c["company_linkedin_url"], "company_domain": c["company_domain"],
                     "company_name": c["company_name"], "slice": c["slice"], "source": "blitz",
                     "contacts_returned": len(titles), "exec_persona_contacts": len(ex_),
                     "titles": " | ".join(t for t in titles if t) or "-", "http_status": st})
with open(os.path.join(HERE, "2026-11-24-persona-reach.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(rows[0])); w.writeheader(); w.writerows(rows)
print("companies with >=1 exec:", sum(1 for r in rows if r["exec_persona_contacts"]), "/", len(rows),
      "exec contacts:", sum(r["exec_persona_contacts"] for r in rows), "returned:", sum(r["contacts_returned"] for r in rows))
for r in rows: print(r["company_name"], r["exec_persona_contacts"], r["titles"][:120])
