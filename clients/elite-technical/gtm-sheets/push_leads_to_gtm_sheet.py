#!/usr/bin/env python3
"""Push a recruiter segment's leads.csv into its GTM Sheets table via the table's inbound webhook.

Usage: push_leads_to_gtm_sheet.py <leads.csv> <webhook_url> [--start N] [--limit N]

- Sends only rows with selected_for_launch == "yes" (the launch set recorded in the README).
- Sends the CSV's columns unchanged as JSON keys; the table's field columns read them.
- Batches of 500 (the webhook takes up to 1,000 per request). The webhook APPENDS rows,
  so a re-run duplicates them. Use --start to resume after a partial run.
- The webhook URL can write to the table, so it is passed as an argument and never committed.
"""
import csv, json, sys, time, argparse, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("csv"); ap.add_argument("url")
ap.add_argument("--start", type=int, default=0); ap.add_argument("--limit", type=int, default=None)
ap.add_argument("--batch", type=int, default=500)
a = ap.parse_args()

rows = [r for r in csv.DictReader(open(a.csv, newline="")) if r.get("selected_for_launch") == "yes"]
assert len({r["linkedin_url"] for r in rows}) == len(rows), "duplicate linkedin_url in launch set"
end = len(rows) if a.limit is None else min(len(rows), a.start + a.limit)
print(f"launch rows {len(rows)}; sending [{a.start}, {end})", flush=True)
i = a.start
while i < end:
    chunk = rows[i:min(i + a.batch, end)]
    req = urllib.request.Request(a.url, data=json.dumps(chunk).encode(), headers={"Content-Type": "application/json"}, method="POST")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                body = resp.read().decode()[:200]
            break
        except Exception as e:
            if attempt == 3: print(f"FAILED at offset {i}: {e}"); sys.exit(1)
            time.sleep(2 ** (attempt + 1))
    i += len(chunk)
    print(f"sent through {i}: {body}", flush=True)
print("done")
