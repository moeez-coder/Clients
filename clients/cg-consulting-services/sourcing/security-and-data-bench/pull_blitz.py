"""Blitz pull for Security and Data Bench (C&G). Raw API pages -> two JSONL files in the scratch dir.

Usage: python3 pull_blitz.py <out_dir>
  companies: POST /v2/search/companies  (firmographic filter only)
  people:    POST /v2/search/people     (same company filter + persona title keywords, person in US)
Cursor-paged at max_results=25 (Blitz cap). Both totals are under the 50k/query cap, so no sharding.
"""
import json, os, sys, time, urllib.request, urllib.error
from spec import (BLITZ_INDUSTRIES, EMPLOYEE_RANGES_BLITZ, REVENUE_MIN_USD, TITLE_KEYWORDS, TITLE_EXCLUDE)

H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
COMPANY = {"industry": {"include": BLITZ_INDUSTRIES}, "hq": {"country_code": ["US"]},
           "employee_range": EMPLOYEE_RANGES_BLITZ, "revenue": {"min": REVENUE_MIN_USD}}
PEOPLE = {"job_title": {"include": TITLE_KEYWORDS, "exclude": TITLE_EXCLUDE}, "location": {"country_code": ["US"]}}


def post(path, body):
    for attempt in range(6):
        r = urllib.request.Request("https://api.blitz-api.ai" + path, data=json.dumps(body).encode(), headers=H, method="POST")
        try:
            return json.load(urllib.request.urlopen(r, timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt); continue
            raise RuntimeError(f"{e.code} {e.read()[:500]}")
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 ** attempt)
    raise RuntimeError("Blitz retries exhausted")


def sweep(path, body, out):
    cursor, n, total = None, 0, None
    with open(out, "w") as f:
        while True:
            b = dict(body, max_results=25, **({"cursor": cursor} if cursor else {}))
            d = post(path, b)
            total = d.get("total_results", total)
            for row in d.get("results", []):
                f.write(json.dumps(row) + "\n"); n += 1
            cursor = d.get("cursor")
            if not cursor or not d.get("results"):
                break
    print(f"{path}: {n} rows written (total_results {total}) -> {out}", flush=True)
    return n, total


if __name__ == "__main__":
    out = sys.argv[1]
    sweep("/v2/search/companies", {"company": COMPANY}, os.path.join(out, "blitz_companies.jsonl"))
    sweep("/v2/search/people", {"company": COMPANY, "people": PEOPLE}, os.path.join(out, "blitz_people.jsonl"))
