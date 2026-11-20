"""Campaign 1 expansion, 2026-11-19: brand-marketing people at 51-200 employee pharma/biotech companies.
Blitz POST /v2/search/people, same C1 persona filters as c1_leads_pull.py (BRAND / BRAND_EXCL, C-Team/VP/Director/Manager,
US people) with company filter pharma_co(excl_names=True, kw_excl=True, sizes=["51-200"]). People are kept with their
current matching role; their companies go to the GTM "Rx Brand Fit" check before any lead is loaded.
Writes ../c1-brand-marketing/2026-11-19-small-blitz-people-cache.json and 2026-11-19-small-companies.csv."""
import csv, json, os, re
from collections import Counter
from doc2_common import *
from dnc import match as dnc_match
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "c1-brand-marketing")
def title_ok(t):
    t = (t or "").lower(); return any(k.lower() in t for k in BRAND) and not any(x.lower() in t for x in BRAND_EXCL)
lvl = {"C-Team": "influencer", "VP": "influencer", "Director": "decision_maker", "Manager": "advocate"}
people, cos, used = {}, {}, 0
for L, name in lvl.items():
    body = people_body(pharma_co(True, True, ["51-200"]), BRAND, BRAND_EXCL, [L]); body["max_results"] = 50
    cursor = None
    while True:
        r = call("/v2/search/people", dict(body, cursor=cursor) if cursor else body); used += r.get("fair_usage", {}).get("records_used", 0)
        for p in r.get("results", []):
            e = next((e for e in p.get("experiences", []) if e.get("job_is_current") and title_ok(e.get("job_title")) and e.get("company_linkedin_url")), None)
            if not e or not p.get("linkedin_url"): continue
            m = dnc_match(e.get("company_name"))
            if m and not m.get("review"): continue
            u = p["linkedin_url"].rstrip("/")
            people.setdefault(u, {"linkedin_url": u, "first_name": p.get("first_name") or "-", "last_name": p.get("last_name") or "-",
                "title": e["job_title"], "level": name, "company_name": e["company_name"], "company_linkedin_url": e["company_linkedin_url"].rstrip("/"),
                "company_size": "51-200", "city": (p.get("location") or {}).get("city") or "-", "state": (p.get("location") or {}).get("state_code") or "-",
                "job_start_date": e.get("job_start_date") or "-"})
            cos.setdefault(e["company_linkedin_url"].rstrip("/"), e["company_name"])
        cursor = r.get("cursor")
        if not cursor or not r.get("results"): break
    print(L, len(people), "used", used, flush=True)
json.dump(list(people.values()), open(os.path.join(OUT, "2026-11-19-small-blitz-people-cache.json"), "w"))
n = Counter(p["company_linkedin_url"] for p in people.values())
with open(os.path.join(OUT, "2026-11-19-small-companies.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["company_linkedin_url", "company_name", "company_size", "persona_people_us"])
    for u, nm in sorted(cos.items(), key=lambda kv: kv[1].lower()): w.writerow([u, nm, "51-200", n[u]])
print(json.dumps({"people": len(people), "companies": len(cos), "blitz_records_used": used}))
