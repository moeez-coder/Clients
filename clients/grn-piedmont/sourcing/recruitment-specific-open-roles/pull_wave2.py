"""Wave 2 for the Recruitment Specific Campaign (2026-11-23, Moe: "Source and Push more leads into the campaign").

Two sources, both Blitz API, same ICP and filters as wave 1 (spec.py, ../tam/tam_counts.py):
  A. New postings: POST /v2/jobs/search, last 8 days (since the 2026-11-16 pull) -> companies not in wave 1
     -> POST /v2/search/waterfall-icp-keyword (2 per company manufacturing, 4 fire & life safety).
  B. Deeper at wave-1 companies: the 2026-11-16 waterfall was capped at 2 per manufacturing company and 628 companies
     hit that cap. Same waterfall, max_results 5, people already held are dropped.
Output raw2/*.jsonl (git-ignored) + 2026-11-23-jobs.csv, -companies.csv and raw2/leads-raw.csv. Resumable.
Usage: python3 pull_wave2.py
"""
import csv, json, os, re, sys, collections
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "tam"))
from tam_counts import ROLES, FLS_ROLES, MFG, FLS_IND, FLS_KW, jobs_body, post
from spec import TITLE_NOISE, COMPANY_NOISE, FLS_GATE, DNC, TIER1, TIER2, TIER3, PEOPLE_EXCLUDE, PER_COMPANY
from build_leads import PERSONA, OFF, SUFFIX, first_clean
RAW = os.path.join(HERE, "raw2"); DATE = "2026-11-23"; DAYS = 8; usage = collections.Counter()
norm = lambda u: re.sub(r"/+$", "", (u or "").split("?")[0]).lower().replace("http://", "https://")

# ---- A1. new postings
jp = os.path.join(RAW, "jobs.jsonl")
if not os.path.exists(jp + ".done"):
    fams = {k: (v, MFG, None) for k, v in ROLES.items()}; fams["fire-life-safety"] = (FLS_ROLES, FLS_IND, FLS_KW)
    with open(jp, "w") as f:
        for fam, (titles, inds, kw) in fams.items():
            b = jobs_body(titles, DAYS, inds, kw); b["max_results"] = 50
            for half in ([inds] if len(inds) <= 50 else [inds[:35], inds[35:]]):
                bb = json.loads(json.dumps(b)); bb["company"]["industry"]["include"] = half; cur = None
                while True:
                    bb["cursor"] = cur; r = post("/v2/jobs/search", bb)
                    if r.get("_error"): raise SystemExit(f"{fam}: {r}")
                    usage["/v2/jobs/search"] += (r.get("fair_usage") or {}).get("records_used", 0)
                    for x in r.get("results") or []: f.write(json.dumps({**x, "role_family": fam}) + "\n")
                    cur = r.get("cursor")
                    if not cur or not r.get("results"): break
    open(jp + ".done", "w").write("ok")
old_comp = {c["company_linkedin_url"]: c for c in csv.DictReader(open(os.path.join(HERE, "2026-11-16-companies.csv")))}
rows, seen = [], set()
for line in open(jp):
    x = json.loads(line); fam = x["role_family"]; t = x.get("title") or ""; c = x.get("company_name") or ""; u = norm(x.get("company_linkedin_url"))
    why = "kept"
    if not u or "/company/" not in u: why = "removed: no company LinkedIn page"
    elif u in old_comp: why = "removed: company already in the 2026-11-16 pull"
    elif DNC.search(c): why = "removed: client DNC list"
    elif COMPANY_NOISE.search(c): why = "removed: company outside ICP (name)"
    elif TITLE_NOISE.search(t): why = "removed: title not a placed role"
    elif fam == "fire-life-safety" and not (FLS_GATE.search(c) or FLS_GATE.search(t)): why = "removed: not fire & life safety"
    k = (u, t.lower(), (x.get("date_posted") or "")[:10])
    if why == "kept" and k in seen: why = "removed: duplicate posting"
    seen.add(k)
    rows.append({"role_family": fam, "title": t or "-", "company_name": c or "-", "company_linkedin_url": u or "-", "date_posted": (x.get("date_posted") or "-")[:10],
                 "job_url": x.get("url") or "-", "jd_summary": re.sub(r"\s+", " ", x.get("ai_summary") or "-"), "status": why})
with open(os.path.join(HERE, f"{DATE}-jobs.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
new = {}
for r in sorted((r for r in rows if r["status"] == "kept"), key=lambda r: r["date_posted"], reverse=True):
    c = new.setdefault(r["company_linkedin_url"], {"company_name": r["company_name"], "company_linkedin_url": r["company_linkedin_url"], "role_family": r["role_family"],
        "open_role": r["title"], "job_url": r["job_url"], "job_posted": r["date_posted"], "jd_summary": r["jd_summary"], "kept_postings": 0, "source": "A new posting"})
    c["kept_postings"] += 1
print("postings", len(rows), collections.Counter(r["status"] for r in rows).most_common(), "new companies", len(new), flush=True)

# ---- B. wave-1 companies that hit the cap of 2
old_people = collections.defaultdict(set); held = set()
for l in open(os.path.join(HERE, "raw", "people.jsonl")):
    d = json.loads(l)
    for p in d["results"]:
        u = (p["person"].get("linkedin_url") or "").lower().rstrip("/"); old_people[d["company_linkedin_url"]].add(u); held.add(u)
oldc = {c["company_linkedin_url"]: c for c in json.load(open(os.path.join(HERE, "raw", "companies.json")))}
deeper = [dict(oldc[u], source="B deeper at wave-1 company") for u, s in old_people.items() if len(s) >= 2 and oldc[u]["role_family"] != "fire-life-safety"]
todo = [dict(c, max=PER_COMPANY.get(c["role_family"], 2)) for c in new.values()] + [dict(c, max=5) for c in deeper]
print("waterfall calls:", len(todo), "(new", len(new), "+ deeper", len(deeper), ")", flush=True)

pp = os.path.join(RAW, "people.jsonl")
done = {json.loads(l)["company_linkedin_url"] for l in open(pp)} if os.path.exists(pp) else set()
def one(c):
    casc = [{"include_title": t, "exclude_title": PEOPLE_EXCLUDE, "location": {"country_code": ["US"]}, "include_headline_search": False} for t in (TIER1[c["role_family"]], TIER2, TIER3)]
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc, "max_results": c["max"]})
    return {"company_linkedin_url": c["company_linkedin_url"], "results": r.get("results") or [], "used": (r.get("fair_usage") or {}).get("records_used", 0)}
with ThreadPoolExecutor(12) as ex, open(pp, "a") as f:
    for r in ex.map(one, [c for c in todo if c["company_linkedin_url"] not in done]):
        usage["/v2/search/waterfall-icp-keyword"] += r.pop("used"); f.write(json.dumps(r) + "\n")
allc = {c["company_linkedin_url"]: c for c in todo}; out = []; per = collections.Counter()
for l in open(pp):
    d = json.loads(l); c = allc.get(d["company_linkedin_url"])
    if not c: continue
    for p in d["results"]:
        q = p["person"]; u = (q.get("linkedin_url") or "").lower().rstrip("/")
        if not u or u in held: continue
        held.add(u); exp = (q.get("experiences") or [{}])[0]
        title = exp.get("job_title") or (q.get("headline") or "").split(" | @")[0] or "-"; loc = q.get("location") or {}
        st = "launch set"
        if not PERSONA.search(title) or (OFF.search(title) and p.get("icp") != 1): st = "removed: title outside persona"
        out.append({"linkedin_url": q["linkedin_url"], "first_name": q.get("first_name") or "-", "last_name": SUFFIX.sub("", q.get("last_name") or "").strip() or "-",
                    "full_name": q.get("full_name") or "-", "job_title": title, "company_name": c["company_name"], "company_linkedin_url": c["company_linkedin_url"],
                    "person_country": loc.get("country_code") or "-", "company_country": "US", "first_name_clean": first_clean(q.get("first_name")) or "-",
                    "waterfall_tier": p.get("icp", "-"), "role_family": c["role_family"], "open_role": c["open_role"], "job_url": c["job_url"], "job_posted": c["job_posted"],
                    "jd_summary": c["jd_summary"], "person_state": loc.get("state_code") or "-", "wave2_source": c["source"], "status": st})
        if st == "launch set": per[c["company_linkedin_url"]] += 1
with open(os.path.join(RAW, "leads-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
with open(os.path.join(HERE, f"{DATE}-companies.csv"), "w", newline="") as f:
    cols = ["company_name", "company_linkedin_url", "role_family", "open_role", "job_posted", "job_url", "source", "leads_launch_set"]
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for u, c in allc.items(): w.writerow({**{k: c[k] for k in cols[:7]}, "leads_launch_set": per.get(u, 0)})
prev = json.load(open(os.path.join(RAW, "usage.json"))) if os.path.exists(os.path.join(RAW, "usage.json")) else {}
for k, v in usage.items(): prev[k] = prev.get(k, 0) + v
json.dump(prev, open(os.path.join(RAW, "usage.json"), "w"))
print("new leads", len(out), collections.Counter(r["status"] for r in out), collections.Counter(r["wave2_source"] for r in out), "usage", prev)
