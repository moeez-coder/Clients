"""Step 2: filter the raw postings and pick one open role per company.  Usage: python3 build_companies.py
Writes <date>-jobs.csv (every posting, with keep/removed reason) and raw/companies.json (one row per kept company)."""
import csv, json, os, re, glob
from spec import TITLE_NOISE, COMPANY_NOISE, FLS_GATE, DNC
HERE = os.path.dirname(os.path.abspath(__file__)); DATE = "2026-11-16"

def norm(u): return re.sub(r"/+$", "", (u or "").split("?")[0]).lower().replace("http://", "https://")

rows = []
for p in sorted(glob.glob(os.path.join(HERE, "raw", "jobs-*.jsonl"))):
    fam = os.path.basename(p)[5:-6]
    for line in open(p):
        x = json.loads(line); t = x.get("title") or ""; c = x.get("company_name") or ""; u = norm(x.get("company_linkedin_url"))
        why = "-"
        if not u or "/company/" not in u: why = "removed: no company LinkedIn page"
        elif DNC.search(c): why = "removed: client DNC list"
        elif COMPANY_NOISE.search(c): why = "removed: company outside ICP (name)"
        elif TITLE_NOISE.search(t): why = "removed: title not a placed role"
        elif fam == "fire-life-safety" and not (FLS_GATE.search(c) or FLS_GATE.search(t)): why = "removed: not fire & life safety"
        loc = x.get("location"); loc = loc if isinstance(loc, str) else json.dumps(loc) if loc else "-"
        rows.append({"role_family": fam, "title": t or "-", "company_name": c or "-", "company_linkedin_url": u or "-",
                     "location": loc, "date_posted": (x.get("date_posted") or "-")[:10], "job_url": x.get("url") or "-",
                     "jd_summary": re.sub(r"\s+", " ", x.get("ai_summary") or "-"), "status": "kept" if why == "-" else why})
seen = set(); out = []
for r in rows:  # same posting can sit in two families or be reposted daily
    k = (r["company_linkedin_url"], r["title"].lower(), r["date_posted"])
    if k in seen and r["status"] == "kept": r["status"] = "removed: duplicate posting"
    seen.add(k); out.append(r)
with open(os.path.join(HERE, f"{DATE}-jobs.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
comp = {}
for r in sorted((r for r in out if r["status"] == "kept"), key=lambda r: r["date_posted"], reverse=True):
    c = comp.setdefault(r["company_linkedin_url"], {"company_name": r["company_name"], "company_linkedin_url": r["company_linkedin_url"],
        "role_family": r["role_family"], "open_role": r["title"], "job_url": r["job_url"], "job_posted": r["date_posted"],
        "jd_summary": r["jd_summary"], "kept_postings": 0, "role_families": set()})
    c["kept_postings"] += 1; c["role_families"].add(r["role_family"])
for c in comp.values(): c["role_families"] = sorted(c["role_families"])
json.dump(list(comp.values()), open(os.path.join(HERE, "raw", "companies.json"), "w"))
import collections
print(len(out), "postings;", collections.Counter(r["status"] for r in out).most_common())
print(len(comp), "companies;", collections.Counter(c["role_family"] for c in comp.values()).most_common())
