"""Step 5b: where a company's chosen posting is closed, try its other kept postings (newest first) for one still open.
Appends to raw/jd_rescue.jsonl; writes <date>-job-descriptions-2.csv = final posting per company (open one if any exists)."""
import csv, json, os, collections
from pull_job_descriptions import one, HERE, DATE
base = {json.loads(l)["company_linkedin_url"]: json.loads(l) for l in open(os.path.join(HERE, "raw", "jd.jsonl"))}
jobs = collections.defaultdict(list)
for j in csv.DictReader(open(os.path.join(HERE, f"{DATE}-jobs.csv"))):
    if j["status"] == "kept": jobs[j["company_linkedin_url"]].append(j)
out = os.path.join(HERE, "raw", "jd_rescue.jsonl")
res = {json.loads(l)["company_linkedin_url"]: json.loads(l) for l in open(out)} if os.path.exists(out) else {}
with open(out, "a") as f:
    for n, (u, b) in enumerate(base.items()):
        if not (b["closed"] or not b["description"]) or u in res: continue
        seen = {b["job_url"]}; got = None
        for j in sorted(jobs[u], key=lambda x: x["date_posted"], reverse=True)[:6]:
            if j["job_url"] in seen: continue
            seen.add(j["job_url"])
            r = one({"company_linkedin_url": u, "job_url": j["job_url"]})
            if r["description"] and not r["closed"]:
                got = {**r, "title": j["title"], "role_family": j["role_family"], "date_posted": j["date_posted"]}; break
        res[u] = got or {"company_linkedin_url": u, "none_open": True}
        f.write(json.dumps(res[u]) + "\n"); f.flush()
rows = []
for u, b in base.items():
    r = res.get(u)
    if r and not r.get("none_open"): rows.append({"company_linkedin_url": u, "job_url": r["job_url"], "posting_open": "yes", "switched_to_other_posting": "yes", "new_title": r["title"], "new_role_family": r["role_family"], "new_date_posted": r["date_posted"], "description": r["description"]})
    else: rows.append({"company_linkedin_url": u, "job_url": b["job_url"], "posting_open": "no" if (b["closed"] or not b["description"]) else "yes", "switched_to_other_posting": "no", "new_title": "-", "new_role_family": "-", "new_date_posted": "-", "description": b["description"] or "-"})
with open(os.path.join(HERE, f"{DATE}-job-descriptions-2.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), collections.Counter((r["posting_open"], r["switched_to_other_posting"]) for r in rows))
