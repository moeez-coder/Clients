"""Doc 1 C1-3 gap-fill with Prospeo POST /search-person (We Are DNA, 2026-11-23; Moe: "for finding more prospects use other
tools"). Companies with no launch-set lead in <date>-2-<camp>-leads.csv. Filters: company.websites.include = root domains
(<=500 per search), person_job_title include (CONTAINS) per campaign, person_location_search = United Kingdom. 25 results a
page, 1 credit per page with results. Results kept only when the result company's domain or LinkedIn URL matches a target.
Usage: python3 prospeo_gap.py <date> <camp> <n_companies|all> <max_pages> <tag>  -> <date>-prospeo-<tag>-<camp>-raw.jsonl"""
import csv, json, os, sys, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); D, CAMP, N, MAXP, TAG = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
NAMES = {"c1": "c1-ceo", "c2": "c2-people", "c3": "c3-ta"}
TITLES = {"c1": ["CEO", "Chief Executive", "Managing Director", "Managing Partner", "Senior Partner", "Chief Operating Officer", "COO",
                 "Chief Financial Officer", "CFO", "Founder", "Owner", "Chairman"],
          "c2": ["Chief People Officer", "People Director", "HR Director", "Human Resources Director", "Director of People", "Head of People",
                 "Head of HR", "Head of Human Resources", "HR Manager", "Human Resources Manager", "People Manager", "People and Culture"],
          "c3": ["Talent Acquisition", "Head of Resourcing", "Resourcing Manager", "Head of Recruitment", "Recruitment Manager",
                 "Head of Talent", "Recruitment Lead"]}
def root(d):
    d = (d or "").lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].strip()
    return "" if d in ("", "-", "linktr.ee", "bit.ly") else d
has = {r["company_linkedin_url"] for r in csv.DictReader(open(os.path.join(HERE, f"{D}-2-{NAMES[CAMP]}-leads.csv"))) if r["status"] == "launch set"}
gap = [c for c in csv.DictReader(open(os.path.join(HERE, f"{D}-2-{NAMES[CAMP]}-companies.csv"))) if c["company_linkedin_url"] not in has and root(c["company_domain"])]
gap = gap if N == "all" else gap[:int(N)]
doms = sorted({root(c["company_domain"]) for c in gap})
out = open(os.path.join(HERE, f"{D}-prospeo-{TAG}-{CAMP}-raw.jsonl"), "a"); credits = 0; total = None
for i in range(0, len(doms), 500):
    chunk = doms[i:i + 500]
    for page in range(1, MAXP + 1):
        body = {"page": page, "filters": {"company": {"websites": {"include": chunk}},
                "person_job_title": {"include": TITLES[CAMP], "match_mode": "CONTAINS"},
                "person_location_search": {"include": ["United Kingdom"]}}}
        for a in range(5):
            try:
                r = urllib.request.urlopen(urllib.request.Request("https://api.prospeo.io/search-person", json.dumps(body).encode(),
                    {"X-KEY": os.environ["PROSPEO_API_KEY"], "Content-Type": "application/json"}, method="POST"), timeout=90); d = json.load(r); break
            except urllib.error.HTTPError as e:
                d = json.loads(e.read() or b"{}")
                if e.code == 429: time.sleep(3 * (a + 1)); continue
                break
        out.write(json.dumps({"campaign": CAMP, "chunk": i // 500, "page": page, "domains": len(chunk), "response": d}) + "\n"); out.flush()
        if d.get("error") or not d.get("results"): print("stop", d.get("error_code")); break
        if not d.get("free"): credits += 1
        pg = d.get("pagination") or {}; total = pg.get("total_count")
        if page >= (pg.get("total_page") or 0): break
        time.sleep(0.25)
print(CAMP, "gap companies", len(gap), "domains", len(doms), "total_count", total, "credits", credits)
