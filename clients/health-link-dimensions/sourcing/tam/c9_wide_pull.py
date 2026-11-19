"""Campaign 9 expansion, 2026-11-19 (Moe approved widening C9 past leadership titles to reach 1,000+ leads).
Same agencies as c9_leads_pull.py, limited to the 269 that passed the GTM Agency Fit check (fit slugs file).
Blitz POST /v2/search/people, company.linkedin_url batches of 50, wider agency titles (WIDE below), leadership excludes,
levels C-Team/VP/Director/Manager, US. People already in the leadership cache are skipped.
Cap: 10 per agency INCLUDING the leads already loaded (Moe's small-pool rule).
Writes ../c9-agency-leadership/2026-11-19-wide-blitz-people-cache.json and 2026-11-19-leads-2.csv (new leads only)."""
import csv, json, os, re
from collections import Counter, defaultdict
from doc2_common import call
from persona_counts import CELLS
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "c9-agency-leadership")
def nurl(u): return (u or "").lower().rstrip("/")
fit = set(open(os.path.join(OUT, "2026-11-19-fit-agency-slugs.txt")).read().split())
cos = {nurl(r["company_linkedin_url"]): r for r in csv.DictReader(open(os.path.join(OUT, "2026-11-19-companies.csv")))
       if nurl(r["company_linkedin_url"]).split("/company/")[-1] in fit}
live = list(csv.DictReader(open(os.path.join(OUT, "2026-11-19-launch-leads.csv"))))
known = {x["linkedin_url"] for x in json.load(open(os.path.join(OUT, "2026-11-19-blitz-people-cache.json")))}
WIDE = ["Vice President", "VP", "SVP", "Senior Vice President", "Group Account Director", "Account Director", "Account Lead",
        "Client Services", "Client Partner", "Head of", "Director, Strategy", "Strategy Director", "Media Director", "Director of Media",
        "Data", "Analytics", "Engagement Director", "Executive Director", "Business Development", "Growth"]
EXC = [e for e in CELLS["leadership"]["influencers"][1] if e != "Analytics"] + ["Engineer", "Developer", "Designer", "Copywriter"]
NOISE = r"\berg\b|employee resource|business resource|chapter|board member|advisory board|recruit|talent|human resources|finance|accounting|legal|it support"
def level(t):
    t = t.lower()
    if re.search(r"\b(svp|evp|senior vice president|executive vice president|head of|executive director|group account director|vice president|vp)\b", t): return "decision_maker"
    return "advocate"
people, used = {}, 0
urls = [r["company_linkedin_url"] for r in cos.values()]
for i in range(0, len(urls), 50):
    cursor = None
    while True:
        b = {"company": {"linkedin_url": urls[i:i+50]}, "people": {"job_title": {"include": WIDE, "exclude": EXC[:50]},
             "job_level": ["C-Team", "VP", "Director", "Manager"], "location": {"country_code": ["US"]}}, "max_results": 50}
        if cursor: b["cursor"] = cursor
        r = call("/v2/search/people", b); used += r.get("fair_usage", {}).get("records_used", 0)
        if r.get("_body"): print("error", r["_body"]); break
        for p in r.get("results", []):
            u = (p.get("linkedin_url") or "").rstrip("/")
            if not u or u in known or u in people: continue
            e = next((e for e in p.get("experiences", []) if e.get("job_is_current") and nurl(e.get("company_linkedin_url")) in cos), None)
            if not e or re.search(NOISE, (e.get("job_title") or "").lower()) or not p.get("first_name"): continue
            a = cos[nurl(e["company_linkedin_url"])]
            people[u] = {"linkedin_url": u, "first_name": p["first_name"], "last_name": p.get("last_name") or "-", "title": e.get("job_title") or "-",
                "level": level(e.get("job_title") or ""), "company_name": e.get("company_name") or a["company_name"],
                "company_linkedin_url": a["company_linkedin_url"], "company_size": a["company_size"],
                "city": (p.get("location") or {}).get("city") or "-", "state": (p.get("location") or {}).get("state_code") or "-",
                "job_start_date": e.get("job_start_date") or "-"}
        cursor = r.get("cursor")
        if not cursor or not r.get("results"): break
    print("batch", i // 50 + 1, len(people), "used", used, flush=True)
json.dump(list(people.values()), open(os.path.join(OUT, "2026-11-19-wide-blitz-people-cache.json"), "w"))
have = Counter(x["company_linkedin_url"] for x in live)
by = defaultdict(list)
for p in people.values(): by[p["company_linkedin_url"]].append(p)
add = []
for co, ps in by.items():
    ps.sort(key=lambda p: (p["level"] != "decision_maker", p["job_start_date"]))
    add += ps[:max(0, 10 - have.get(co, 0))]
cols = list(live[0].keys())
with open(os.path.join(OUT, "2026-11-19-leads-2.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(add)
print(json.dumps({"fit_agencies": len(cos), "new_people": len(people), "new_leads": len(add), "levels": Counter(a["level"] for a in add), "blitz_records_used": used}))
