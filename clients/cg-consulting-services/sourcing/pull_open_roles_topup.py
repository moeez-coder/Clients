"""Top-up pull for C&G's open-role segments: NEW hiring companies only, so nothing is paid for twice.

Usage: python3 pull_open_roles_topup.py <slug> <raw_dir> <days> [max_new_companies]

Why a separate script: the first pull (pull_open_roles.py, 2026-11-05) paged /v2/jobs/search, which costs
1 record per job, including jobs at companies we have already sourced. For a top-up, that would re-buy
the 5,000 jobs already pulled. Instead this script:
  1. pages POST /v2/company/tam-by-jobs (1 record per company) with the segment filters and a <days>
     posting window, skipping every company already in an earlier <date>-companies.csv of this segment;
     Tech pages the Northeast-HQ TAM first, then the rest, and stops at max_new_companies;
  2. POST /v2/jobs/company (max_results 1, same title filters and window) per NEW company, which gives
     that company's {Open_Role}/{JD};
  3. POST /v2/search/waterfall-icp-keyword per NEW company (same cascade and per-company count as the
     first pull).
Writes jobs.jsonl / companies.jsonl / people.jsonl / usage.json / requests.jsonl in <raw_dir>/<slug>/
in the same shape pull_open_roles.py does, so build_open_roles.py builds the CSVs unchanged.
"""
import csv, glob, json, os, sys
from concurrent.futures import ThreadPoolExecutor
import pull_open_roles as P
from build_open_roles import norm
from open_role_spec import SEGMENTS, JOB_TITLE_EXCLUDE, FALLBACK_TITLES, PEOPLE_EXCLUDE

HERE = os.path.dirname(os.path.abspath(__file__))


def known_companies(slug):
    seen = set()
    for p in glob.glob(os.path.join(HERE, slug, "*-companies.csv")):
        for r in csv.DictReader(open(p)):
            seen.add(norm(r["company_linkedin_url"]))
    return seen


def main(slug, raw, days, max_new=None):
    seg = SEGMENTS[slug]
    days = int(days)
    max_new = int(max_new) if max_new else None
    d = os.path.join(raw, slug); os.makedirs(d, exist_ok=True)
    log = open(os.path.join(d, "requests.jsonl"), "a")
    tech = slug.endswith("tech-eng-security-data")
    known = known_companies(slug)
    print(f"{slug}: {len(known)} companies already sourced", flush=True)

    # 1. new hiring companies from tam-by-jobs
    out = os.path.join(d, "companies.jsonl")
    new = {}
    if not os.path.exists(out + ".done"):
        passes = [True, False] if tech else [None]
        paged = 0
        for ne in passes:
            body = P.filters(seg, ne)
            body["job"]["date_posted"] = {"last_days": days}
            log.write(json.dumps({"path": "/v2/company/tam-by-jobs", "body": body,
                                  "stop_at_new_companies": max_new}) + "\n"); log.flush()
            cursor = None
            while True:
                r = P.post("/v2/company/tam-by-jobs", dict(body, max_results=50, **({"cursor": cursor} if cursor else {})))
                for row in r.get("results", []):
                    paged += 1
                    k = norm(row["company"]["linkedin_url"])
                    if k not in known and k not in new:
                        new[k] = row
                cursor = r.get("cursor")
                if not cursor or not r.get("results") or (max_new and len(new) >= max_new):
                    break
            if max_new and len(new) >= max_new:
                break
        with open(out, "w") as f:
            for row in list(new.values())[: max_new or None]:
                f.write(json.dumps(row) + "\n")
        open(out + ".done", "w").write(str(len(new)))
        print(f"tam-by-jobs: paged {paged}, new companies {len(new)}", flush=True)
    rows = [json.loads(l) for l in open(out)]
    urls = [r["company"]["linkedin_url"] for r in rows]
    names = {r["company"]["linkedin_url"]: r["company"].get("name") for r in rows}

    # 2. one current open job per new company
    out = os.path.join(d, "jobs.jsonl")
    if not os.path.exists(out + ".done"):
        jbody = {"title": {"include": seg["job_titles"], "exclude": JOB_TITLE_EXCLUDE},
                 "location": {"country_code": {"include": ["US"]}}, "date_posted": {"last_days": days}}
        log.write(json.dumps({"path": "/v2/jobs/company", "count": len(urls),
                              "body_template": {"company_linkedin_url": "<url>", "job": jbody, "max_results": 1}}) + "\n"); log.flush()
        with ThreadPoolExecutor(20) as ex:
            res = list(ex.map(lambda u: (u, P.post("/v2/jobs/company", {"company_linkedin_url": u, "job": jbody, "max_results": 1})), urls))
        with open(out, "w") as f:
            for u, r in res:
                for j in r.get("results", [])[:1]:
                    j.setdefault("company_linkedin_url", u)
                    j.setdefault("company_name", names.get(u))
                    f.write(json.dumps(j) + "\n")
        open(out + ".done", "w").write(str(len(res)))
        print(f"jobs/company: {sum(1 for _ in open(out))} jobs for {len(urls)} companies", flush=True)

    # 3. waterfall on the new companies that returned a job
    have_job = {json.loads(l)["company_linkedin_url"] for l in open(out)}
    out = os.path.join(d, "people.jsonl")
    if not os.path.exists(out + ".done"):
        cascade = [
            {"include_title": seg["tier1"], "exclude_title": PEOPLE_EXCLUDE,
             "location": {"country_code": ["US"]}, "include_headline_search": False},
            {"include_title": FALLBACK_TITLES, "exclude_title": PEOPLE_EXCLUDE,
             "location": {"country_code": ["US"]}, "include_headline_search": False},
        ]
        targets = sorted(have_job)
        log.write(json.dumps({"path": "/v2/search/waterfall-icp-keyword", "companies": len(targets),
                              "body_template": {"company_linkedin_url": "<url>", "cascade": cascade,
                                                "max_results": seg["per_company"]}}) + "\n"); log.flush()
        with ThreadPoolExecutor(20) as ex:
            res = list(ex.map(lambda u: (u, P.post("/v2/search/waterfall-icp-keyword",
                                                   {"company_linkedin_url": u, "cascade": cascade,
                                                    "max_results": seg["per_company"]})), targets))
        with open(out, "w") as f:
            for u, r in res:
                f.write(json.dumps({"company_linkedin_url": u, "results": r.get("results", [])}) + "\n")
        open(out + ".done", "w").write(str(len(res)))
        print(f"waterfall: {len(res)} companies", flush=True)

    prev = json.load(open(os.path.join(d, "usage.json"))) if os.path.exists(os.path.join(d, "usage.json")) else {}
    for k, v in P.USAGE.items():
        prev[k] = prev.get(k, 0) + v
    json.dump(prev, open(os.path.join(d, "usage.json"), "w"), indent=1)
    print("records_used this run:", P.USAGE, "cumulative:", prev, flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:5])
