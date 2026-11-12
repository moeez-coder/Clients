"""Sample read for We Are DNA doc 1 (2026-11-12): the 25 most recent UK hook-role postings per segment (last 30d).
Same request body as tam_counts.json `jobs_30d_body`, with max_results=25 (Blitz cap). Measures how concentrated
postings are per company and how much noise is in the pool. Output: tam_samples.json. Usage: python3 tam_samples.py"""
import json, os, urllib.request, urllib.error, time, collections
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
here = os.path.dirname(os.path.abspath(__file__))
counts = json.load(open(os.path.join(here, "tam_counts.json")))

def post(path, body):
    for a in range(6):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai" + path, json.dumps(body).encode(), H, method="POST")
            return json.load(urllib.request.urlopen(r, timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"_error": e.code, "_body": e.read()[:400].decode(errors="replace")}

out = {}
for slug, row in counts.items():
    body = dict(row["jobs_30d_body"]); body["max_results"] = 25
    r = post("/v2/jobs/search", body)
    res = r.get("results", [])
    jobs = [{k: x.get(k) for k in ("title", "company_name", "company_linkedin_url", "date_posted", "location")} for x in res]
    cc = collections.Counter(j["company_name"] for j in jobs)
    out[slug] = {"body": body, "records_used": (r.get("fair_usage") or {}).get("records_used"), "n": len(jobs),
                 "distinct_companies": len(cc), "company_counts": cc.most_common(), "jobs": jobs, "error": r.get("_body")}
    print(slug, len(jobs), "jobs,", len(cc), "companies:", cc.most_common(12), flush=True)
json.dump(out, open(os.path.join(here, "tam_samples.json"), "w"), indent=1)
