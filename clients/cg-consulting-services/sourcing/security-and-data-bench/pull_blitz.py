"""Blitz pull for Security and Data Bench (C&G). Raw API pages -> two JSONL files in the scratch dir.

Usage: python3 pull_blitz.py <out_dir>
  companies: POST /v2/search/companies  (firmographic filter only)
  people:    POST /v2/search/people     (same company filter + persona title keywords, person in US)
Cursor-paged at max_results=25 (Blitz cap). Both totals are under the 50k/query cap, so no sharding.
"""
import http.client, json, os, sys, time, urllib.request, urllib.error
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
        except (urllib.error.URLError, TimeoutError, http.client.IncompleteRead, ConnectionError, json.JSONDecodeError):
            time.sleep(2 ** attempt)
    raise RuntimeError("Blitz retries exhausted")


def sweep(path, body, out):
    """Resumable: the next-page cursor is saved to <out>.cursor after each page is written."""
    state = out + ".cursor"
    cursor, mode = None, "w"
    if os.path.exists(state):
        cursor, mode = open(state).read().strip() or None, "a"
        if cursor is None:
            print(f"{path}: already complete -> {out}", flush=True)
            return
    total = None
    with open(out, mode) as f:
        while True:
            b = dict(body, max_results=25, **({"cursor": cursor} if cursor else {}))
            d = post(path, b)
            total = d.get("total_results", total)
            for row in d.get("results", []):
                f.write(json.dumps(row) + "\n")
            f.flush()
            cursor = d.get("cursor") if d.get("results") else None
            open(state, "w").write(cursor or "")
            if not cursor:
                break
    n = sum(1 for _ in open(out))
    print(f"{path}: {n} rows written (total_results {total}) -> {out}", flush=True)


if __name__ == "__main__":
    out = sys.argv[1]
    sweep("/v2/search/companies", {"company": COMPANY}, os.path.join(out, "blitz_companies.jsonl"))
    sweep("/v2/search/people", {"company": COMPANY, "people": PEOPLE}, os.path.join(out, "blitz_people.jsonl"))
