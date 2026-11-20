"""Distinct companies per persona (all levels) via Blitz POST /v2/company/tam-by-people. 1 record per company returned.
Hard cap 450 records across all personas. Writes persona_companies.json (company name, linkedin_url, matched-people count)."""
import json
from persona_counts import call, company, CELLS
CAP, used, out = 450, 0, {}
order = ["investment", "data_analytics", "planning_activation", "leadership"]
for pn in order:
    rows, cursor, bodies = [], None, []
    for ln, (inc, exc, lv) in CELLS[pn].items():
        cursor = None
        while True:
            if used + 50 > CAP: break
            b = {"company": company(), "people": {"job_title": {"include": inc, "exclude": exc}, "job_level": lv,
                 "location": {"country_code": ["US"]}}, "max_results": 50, "cursor": cursor}
            r = call("/v2/company/tam-by-people", b); used += r["fair_usage"]["records_used"]
            for x in r.get("results", []):
                c = x.get("company", {})
                rows.append({"level": ln, "name": c.get("name"), "linkedin_url": c.get("linkedin_url"),
                             "matched": x.get("people_count") or x.get("count") or x.get("matched_people_count")})
            cursor = r.get("cursor")
            if not cursor: break
        bodies.append({k: v for k, v in b.items() if k != "cursor"})
    uniq = sorted({r["linkedin_url"] for r in rows})
    out[pn] = {"distinct_companies": len(uniq), "capped": used + 50 > CAP, "rows": rows, "bodies": bodies}
    print(pn, "distinct companies", len(uniq), "records so far", used)
out["records_used"] = used
json.dump(out, open("2026-11-18-persona_companies.json", "w"), indent=1)
