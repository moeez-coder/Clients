"""Doc 2 step 4b (leadership = influencer + decision-maker titles, influencer exclusions): distinct agencies per functional persona in the wider universe (Blitz POST /v2/company/tam-by-people,
company filter = the linkedin_url groups from doc2_agency.py, 50 urls per call, all levels). 1 record per company returned.
Writes 2026-11-18-doc-2-agency-companies.json."""
import json, csv, re
from persona_counts import CELLS
from doc2_common import call
import doc2_agency_groups as G
out, used = {}, 0
HEALTH = ["pharma", "health", "life science", "hcp", "biotech", "medical", "patient", "clinician", "physician"]
for pn in ["investment", "planning_activation", "data_analytics", "leadership"]:
    inc, exc, _ = CELLS[pn]["influencers"] if pn != "leadership" else (CELLS[pn]["influencers"][0] + CELLS[pn]["decision_makers"][0], CELLS[pn]["influencers"][1], None)
    rows = []
    for g, urls in G.groups.items():
        for i in range(0, len(urls), 50):
            cursor = None
            while True:
                b = {"company": {"linkedin_url": urls[i:i+50]}, "people": {"job_title": {"include": inc, "exclude": exc},
                     "job_level": ["C-Team", "VP", "Director", "Manager"], "location": {"country_code": ["US"]}}, "max_results": 50}
                if cursor: b["cursor"] = cursor
                r = call("/v2/company/tam-by-people", b); used += r.get("fair_usage", {}).get("records_used", 0)
                for x in r.get("results", []):
                    c = x.get("company") or {}
                    rows.append({"group": g, "name": c.get("name"), "linkedin_url": c.get("linkedin_url"), "size": c.get("size"),
                                 "people": x.get("matched_people"), "industry": c.get("industry"),
                                 "health_text": any(h in ((c.get("about") or "") + " " + " ".join(c.get("specialties") or [])).lower() for h in HEALTH),
                                 "about": (c.get("about") or "")[:160].replace("\n", " ")})
                cursor = r.get("cursor")
                if not cursor: break
    out[pn] = rows; print(pn, len(rows), "used", used, flush=True)
out["records_used"] = used
json.dump(out, open("2026-11-18-doc-2-agency-companies.json", "w"), indent=1)
