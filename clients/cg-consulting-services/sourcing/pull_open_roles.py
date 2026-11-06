"""Blitz pull for C&G's recruiter-specific open-role segments. Raw API pages -> JSONL in <raw_dir>/<slug>/.

Usage: python3 pull_open_roles.py <slug> <raw_dir>

Steps (filters in open_role_spec.py; exact bodies are logged to <raw_dir>/<slug>/requests.jsonl):
  1. jobs:      POST /v2/jobs/search          (cursor, 50/page, cap per segment job_cap; Tech: Northeast HQ first)
  2. companies: POST /v2/company/tam-by-jobs  (same filters -> distinct hiring companies with HQ state)
                Tech non-Northeast only: POST /v2/enrichment/company per company seen in the pulled jobs
                (cheaper than paging the full non-NE TAM, which is far larger than the 5,000-job cap needs)
  3. people:    POST /v2/search/waterfall-icp-keyword per company (tier 1 hiring manager, tier 2 talent fallback)
Every response's fair_usage.records_used is summed into <raw_dir>/<slug>/usage.json.
Resumable: each step skips if its output is already complete.
"""
import http.client, json, os, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor
from open_role_spec import (SEGMENTS, SIZES, JOB_TITLE_EXCLUDE, DATE_POSTED_DAYS, NORTHEAST_STATES,
                            FALLBACK_TITLES, PEOPLE_EXCLUDE)

H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
USAGE = {}


def post(path, body):
    for attempt in range(7):
        r = urllib.request.Request("https://api.blitz-api.ai" + path, data=json.dumps(body).encode(), headers=H,
                                   method="POST")
        try:
            d = json.load(urllib.request.urlopen(r, timeout=90))
            USAGE[path] = USAGE.get(path, 0) + (d.get("fair_usage") or {}).get("records_used", 0)
            return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt); continue
            if e.code == 404:
                return {"results": [], "_404": True}
            raise RuntimeError(f"{path} {e.code} {e.read()[:500]}")
        except (urllib.error.URLError, TimeoutError, http.client.IncompleteRead, ConnectionError,
                json.JSONDecodeError):
            time.sleep(2 ** attempt)
    raise RuntimeError("Blitz retries exhausted")


def filters(seg, northeast=None):
    company = {"is_agency": False, "industry": {"include": seg["industries"]}, "size": {"include": SIZES},
               "hq": {"country_code": {"include": ["US"]}}}
    if northeast is True:
        company["hq"]["state"] = {"include": NORTHEAST_STATES}
    elif northeast is False:
        company["hq"]["state"] = {"exclude": NORTHEAST_STATES}
    return {"job": {"title": {"include": seg["job_titles"], "exclude": JOB_TITLE_EXCLUDE},
                    "location": {"country_code": {"include": ["US"]}},
                    "date_posted": {"last_days": DATE_POSTED_DAYS}},
            "company": company}


def sweep(path, body, out, cap, log):
    done = out + ".done"
    if os.path.exists(done):
        return sum(1 for _ in open(out))
    log.write(json.dumps({"path": path, "body": body, "cap": cap}) + "\n"); log.flush()
    n, cursor = 0, None
    with open(out, "w") as f:
        while n < cap:
            d = post(path, dict(body, max_results=min(50, cap - n), **({"cursor": cursor} if cursor else {})))
            for row in d.get("results", []):
                f.write(json.dumps(row) + "\n"); n += 1
            cursor = d.get("cursor")
            if not cursor or not d.get("results"):
                break
    open(done, "w").write(str(n))
    print(f"{path}: {n} -> {out}", flush=True)
    return n


def main(slug, raw):
    seg = SEGMENTS[slug]
    d = os.path.join(raw, slug); os.makedirs(d, exist_ok=True)
    log = open(os.path.join(d, "requests.jsonl"), "a")
    tech = slug.endswith("tech-eng-security-data")

    # 1 + 2. jobs and companies
    if tech:
        n_ne = sweep("/v2/jobs/search", filters(seg, True), os.path.join(d, "jobs_ne.jsonl"), seg["job_cap"], log)
        sweep("/v2/jobs/search", filters(seg, False), os.path.join(d, "jobs_rest.jsonl"), seg["job_cap"] - n_ne, log)
        sweep("/v2/company/tam-by-jobs", filters(seg, True), os.path.join(d, "companies_ne.jsonl"), 50000, log)
        have = {json.loads(l)["company"]["linkedin_url"] for l in open(os.path.join(d, "companies_ne.jsonl"))}
        need = sorted({json.loads(l)["company_linkedin_url"] for l in open(os.path.join(d, "jobs_rest.jsonl"))
                       if json.loads(l).get("company_linkedin_url")} - have)
        out = os.path.join(d, "companies_rest_enriched.jsonl")
        if not os.path.exists(out + ".done"):
            log.write(json.dumps({"path": "/v2/enrichment/company", "count": len(need)}) + "\n")
            with ThreadPoolExecutor(20) as ex:
                res = list(ex.map(lambda u: (u, post("/v2/enrichment/company", {"company_linkedin_url": u})), need))
            with open(out, "w") as f:
                for u, r in res:
                    f.write(json.dumps({"company_linkedin_url": u, "response": r}) + "\n")
            open(out + ".done", "w").write(str(len(res)))
    else:
        sweep("/v2/jobs/search", filters(seg), os.path.join(d, "jobs.jsonl"), seg["job_cap"], log)
        sweep("/v2/company/tam-by-jobs", filters(seg), os.path.join(d, "companies.jsonl"), 50000, log)

    # 3. people: one waterfall per company that has a pulled job
    urls = set()
    for fn in os.listdir(d):
        if fn.startswith("jobs") and fn.endswith(".jsonl"):
            urls |= {json.loads(l).get("company_linkedin_url") for l in open(os.path.join(d, fn))}
    urls = sorted(u for u in urls if u)
    out = os.path.join(d, "people.jsonl")
    if not os.path.exists(out + ".done"):
        cascade = [
            {"include_title": seg["tier1"], "exclude_title": PEOPLE_EXCLUDE,
             "location": {"country_code": ["US"]}, "include_headline_search": False},
            {"include_title": FALLBACK_TITLES, "exclude_title": PEOPLE_EXCLUDE,
             "location": {"country_code": ["US"]}, "include_headline_search": False},
        ]
        log.write(json.dumps({"path": "/v2/search/waterfall-icp-keyword", "companies": len(urls),
                              "body_template": {"company_linkedin_url": "<url>", "cascade": cascade,
                                                "max_results": seg["per_company"]}}) + "\n"); log.flush()
        with ThreadPoolExecutor(20) as ex:
            res = list(ex.map(lambda u: (u, post("/v2/search/waterfall-icp-keyword",
                                                 {"company_linkedin_url": u, "cascade": cascade,
                                                  "max_results": seg["per_company"]})), urls))
        with open(out, "w") as f:
            for u, r in res:
                f.write(json.dumps({"company_linkedin_url": u, "results": r.get("results", [])}) + "\n")
        open(out + ".done", "w").write(str(len(res)))
        print(f"waterfall: {len(res)} companies -> {out}", flush=True)

    prev = json.load(open(os.path.join(d, "usage.json"))) if os.path.exists(os.path.join(d, "usage.json")) else {}
    for k, v in USAGE.items():
        prev[k] = prev.get(k, 0) + v
    json.dump(prev, open(os.path.join(d, "usage.json"), "w"), indent=1)
    print("records_used this run:", USAGE, "cumulative:", prev, flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
