"""Campaign 1 (Pharma Brand Marketing) launch lead pull, 2026-11-19.

Blitz API POST /v2/search/people, paged with cursor, for the C1 persona cells used in the Doc 2 sizing
(doc2_common.PHARMA_CELLS["c1_brand_marketing"]: BRAND titles minus BRAND_EXCL, levels influencers / decision_makers /
advocates, US people, company filter pharma_co(excl_names=True, kw_excl=True) = post-DNC).

A person is kept only when a CURRENT experience is at one of the 441 C1 companies in
2026-11-18-doc-2-persona-companies.csv (campaign == c1_brand_marketing) and that role's title still passes the persona
filter. DNC re-checked with dnc.match() on the company name.

Per-company cap (Doc 2, Campaign 1 volume rule): 2 per company = 1 influencer-or-decision-maker + 1 advocate;
companies sized 10001+ get up to 5 (2 influencer/decision-maker + 3 advocates), distinct titles preferred.

Writes ../c1-brand-marketing/2026-11-19-leads.csv (linkedin_url first) and prints counts + Blitz records used."""
import csv, json, os, re, sys
from collections import defaultdict
from doc2_common import *
from dnc import match as dnc_match

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "c1-brand-marketing")
OUT = os.path.join(OUT_DIR, sys.argv[1] if len(sys.argv) > 1 else "2026-11-19-leads.csv")
# optional: argv[2] = file of fit company slugs (GTM "Rx Brand Fit" = yes); argv[3], argv[4] = cap for most / 10001+ companies
FIT = set(open(sys.argv[2]).read().split()) if len(sys.argv) > 2 else None
CAP_SMALL, CAP_BIG = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (2, 5)
WEAK = r"communicat|event|call center|content and partnerships|field strategy and operations|process and data|demand generation"
def weak(t): t = t.lower(); return bool(re.search(WEAK, t)) and not re.search(r"\b(vice president|vp|svp|evp|chief|head of|global head)\b", t)

def nurl(u): return (u or "").lower().rstrip("/").replace("http://", "https://").replace("://linkedin", "://www.linkedin")

companies = {nurl(r["company_linkedin_url"]): r for r in csv.DictReader(open(os.path.join(HERE, "2026-11-18-doc-2-persona-companies.csv")))
             if r["campaign"] == "c1_brand_marketing"
             and (FIT is None or r["company_linkedin_url"].rstrip("/").split("/company/")[-1].lower() in FIT)}
print("c1 companies", len(companies))

def title_ok(t):
    t = (t or "").lower()
    return any(k.lower() in t for k in BRAND) and not any(x.lower() in t for x in BRAND_EXCL)

level_of = {"influencers": "influencer", "decision_makers": "decision_maker", "advocates": "advocate"}
people, used = {}, 0
CACHE = os.path.join(OUT_DIR, "2026-11-19-blitz-people-cache.json")  # raw matched people, so a cap change needs no new Blitz pull
if os.path.exists(CACHE):
    people = {p["linkedin_url"]: p for p in json.load(open(CACHE)) if nurl(p["company_linkedin_url"]) in companies}
    print("loaded", len(people), "people from cache")
for lv, levels in ([] if people else LV.items()):
    body = people_body(pharma_co(True, True), BRAND, BRAND_EXCL, levels); body["max_results"] = 50
    cursor, n = None, 0
    while True:
        b = dict(body, cursor=cursor) if cursor else body
        r = call("/v2/search/people", b); used += r.get("fair_usage", {}).get("records_used", 0)
        for p in r.get("results", []):
            n += 1
            exp = next((e for e in p.get("experiences", []) if e.get("job_is_current")
                        and nurl(e.get("company_linkedin_url")) in companies and title_ok(e.get("job_title"))), None)
            if not exp or not p.get("linkedin_url"): continue
            url = p["linkedin_url"].rstrip("/")
            if url in people: continue
            people[url] = {"linkedin_url": url, "first_name": p.get("first_name") or "-", "last_name": p.get("last_name") or "-",
                           "title": exp["job_title"], "level": level_of[lv], "company_name": exp["company_name"],
                           "company_linkedin_url": companies[nurl(exp["company_linkedin_url"])]["company_linkedin_url"],
                           "company_size": companies[nurl(exp["company_linkedin_url"])]["size"],
                           "city": (p.get("location") or {}).get("city") or "-", "state": (p.get("location") or {}).get("state_code") or "-",
                           "job_start_date": exp.get("job_start_date") or "-"}
        cursor = r.get("cursor")
        print(lv, "page", n, "of", r.get("total_results"), "kept", len(people), "used", used, flush=True)
        if not cursor or not r.get("results"): break

if not os.path.exists(CACHE):
    os.makedirs(OUT_DIR, exist_ok=True); json.dump(list(people.values()), open(CACHE, "w"))
by_co = defaultdict(list)
for p in people.values():
    m = dnc_match(p["company_name"])
    if m and not m.get("review"): p["dnc"] = m["dnc_source"]; continue
    if FIT is not None and weak(p["title"]): continue
    by_co[p["company_linkedin_url"]].append(p)

rank = {"decision_maker": 0, "influencer": 1}
def pick(ps, n_top, n_adv):
    top = sorted([p for p in ps if p["level"] != "advocate"], key=lambda p: (rank[p["level"]], p["job_start_date"]), reverse=False)
    adv = sorted([p for p in ps if p["level"] == "advocate"], key=lambda p: p["job_start_date"], reverse=True)
    out, seen = [], set()
    for pool, n in ((top, n_top), (adv, n_adv)):
        k = 0
        for p in pool:  # distinct normalised titles first, then fill
            t = re.sub(r"[^a-z]", "", p["title"].lower())
            if t in seen: continue
            out.append(p); seen.add(t); k += 1
            if k == n: break
        for p in pool:
            if k == n: break
            if p not in out: out.append(p); k += 1
    return out

rows = []
for co, ps in by_co.items():
    big = ps[0]["company_size"] == "10001+"
    cap = CAP_BIG if big else CAP_SMALL
    n_top = max(1, round(cap * 0.4))
    chosen = pick(ps, n_top, cap - n_top)
    if not chosen: continue
    # a company with no advocate (or no top) still gets up to its cap from the other pool
    for p in sorted(ps, key=lambda p: p["job_start_date"], reverse=True):
        if len(chosen) >= cap: break
        if p not in chosen: chosen.append(p)
    rows += chosen

os.makedirs(OUT_DIR, exist_ok=True)
cols = ["linkedin_url", "first_name", "last_name", "title", "level", "company_name", "company_linkedin_url", "company_size",
        "city", "state", "job_start_date"]
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
print(json.dumps({"people_matched": len(people), "dnc_dropped": sum(1 for p in people.values() if p.get("dnc")),
                  "companies_with_people": len(by_co), "leads_written": len(rows), "blitz_records_used": used, "out": OUT}))
