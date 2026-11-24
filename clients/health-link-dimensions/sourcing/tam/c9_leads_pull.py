"""Campaign 9 (Agency Leadership) launch lead pull, 2026-11-19.

Universe: the Doc 2 sizing's wide agency universe for the leadership persona (2026-11-18-doc-2-agency-companies.json,
key "leadership", from doc2_agency_companies.py), keeping health-focused agencies (health_text) and dropping DNC/client
matches with dnc.match() (the SOLVE(D)-fixed matcher). That is the "352 agencies" figure in sizing section 14.

Blitz API POST /v2/search/people, company.linkedin_url in batches of 50, titles = persona_counts.CELLS["leadership"]
influencer + decision-maker includes, influencer excludes (same as the sizing), levels C-Team/VP/Director/Manager, US people.
A person is kept when a CURRENT experience is at one of those agencies.

Cap (Moe, 2026-11-19): "10 if less number of people are found and 5 if more". The C9 pool is small (sizing: about 938
people at 352 agencies, under 3 per agency), so the cap is 10 per agency, influencers first.

Writes ../c9-agency-leadership/2026-11-19-leads.csv (linkedin_url first), -companies.csv and a raw people cache."""
import csv, json, os, sys
from collections import defaultdict
from doc2_common import call
from persona_counts import CELLS
from dnc import match as dnc_match

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "c9-agency-leadership")
CAP = int(sys.argv[1]) if len(sys.argv) > 1 else 10
def nurl(u): return (u or "").lower().rstrip("/").replace("http://", "https://").replace("://linkedin", "://www.linkedin")

rows = json.load(open(os.path.join(HERE, "2026-11-18-doc-2-agency-companies.json")))["leadership"]
agencies, dropped = {}, []
for r in rows:
    if not r.get("health_text") or not r.get("linkedin_url"): continue
    m = dnc_match(r["name"])
    if m and not m.get("review"): dropped.append((r["name"], m["dnc_source"])); continue
    agencies.setdefault(nurl(r["linkedin_url"]), r)
print("agencies", len(agencies), "dnc dropped", len(dropped), dropped[:10])

INF, EXC = CELLS["leadership"]["influencers"][0], CELLS["leadership"]["influencers"][1]
DM = CELLS["leadership"]["decision_makers"][0]
inc = INF + DM
inf_words = [t.lower().strip("[]") for t in INF]
os.makedirs(OUT_DIR, exist_ok=True)
CACHE = os.path.join(OUT_DIR, "2026-11-19-blitz-people-cache.json")
people, used = {}, 0
if os.path.exists(CACHE):
    people = {p["linkedin_url"]: p for p in json.load(open(CACHE))}; print("cache", len(people))
else:
    urls = [a["linkedin_url"] for a in agencies.values()]
    for i in range(0, len(urls), 50):
        cursor = None
        while True:
            b = {"company": {"linkedin_url": urls[i:i+50]},
                 "people": {"job_title": {"include": inc, "exclude": EXC}, "job_level": ["C-Team", "VP", "Director", "Manager"],
                            "location": {"country_code": ["US"]}}, "max_results": 50}
            if cursor: b["cursor"] = cursor
            r = call("/v2/search/people", b); used += r.get("fair_usage", {}).get("records_used", 0)
            if r.get("_body"): print("error", r["_body"]); break
            for p in r.get("results", []):
                exp = next((e for e in p.get("experiences", []) if e.get("job_is_current")
                            and nurl(e.get("company_linkedin_url")) in agencies), None)
                if not exp or not p.get("linkedin_url"): continue
                url = p["linkedin_url"].rstrip("/")
                t = (exp.get("job_title") or "").lower()
                lvl = "influencer" if any(w in t for w in inf_words) else "decision_maker"
                a = agencies[nurl(exp["company_linkedin_url"])]
                people.setdefault(url, {"linkedin_url": url, "first_name": p.get("first_name") or "-", "last_name": p.get("last_name") or "-",
                    "title": exp.get("job_title") or "-", "level": lvl, "company_name": exp.get("company_name") or a["name"],
                    "company_linkedin_url": a["linkedin_url"], "company_size": a.get("size") or "-",
                    "city": (p.get("location") or {}).get("city") or "-", "state": (p.get("location") or {}).get("state_code") or "-",
                    "job_start_date": exp.get("job_start_date") or "-"})
            cursor = r.get("cursor")
            if not cursor or not r.get("results"): break
        print("batch", i // 50 + 1, "people", len(people), "used", used, flush=True)
    json.dump(list(people.values()), open(CACHE, "w"))

by = defaultdict(list)
for p in people.values(): by[p["company_linkedin_url"]].append(p)
out = []
for co, ps in by.items():
    ps.sort(key=lambda p: (p["level"] != "influencer", p["job_start_date"]))
    out += ps[:CAP]
cols = ["linkedin_url", "first_name", "last_name", "title", "level", "company_name", "company_linkedin_url", "company_size", "city", "state", "job_start_date"]
with open(os.path.join(OUT_DIR, "2026-11-19-leads.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
with open(os.path.join(OUT_DIR, "2026-11-19-companies.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["company_linkedin_url", "company_name", "company_size", "universe_group", "people_found", "leads", "about"])
    w.writeheader()
    for u, a in sorted(agencies.items(), key=lambda kv: kv[1]["name"].lower()):
        n = len(by.get(a["linkedin_url"], []))
        w.writerow({"company_linkedin_url": a["linkedin_url"], "company_name": a["name"], "company_size": a.get("size") or "-",
                    "universe_group": a.get("group") or "-", "people_found": n, "leads": min(n, CAP), "about": a.get("about") or "-"})
print(json.dumps({"agencies": len(agencies), "agencies_with_people": len(by), "people": len(people), "leads": len(out), "cap": CAP, "blitz_records_used": used}))
