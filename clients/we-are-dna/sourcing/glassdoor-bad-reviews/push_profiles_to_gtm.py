"""Load the scored Glassdoor profiles CSV into GTM Sheets table "2 Glassdoor company profiles"
(55c0230b-f042-47c2-927a-243594553677) through the table's inbound webhook. Stdlib only.

Usage: python -I push_profiles_to_gtm.py <profiles.csv> <webhook_url> [--start N]

- Row order: companies passing the profile bar first, then high > medium > low > none confidence,
  then most reviews, so the table opens on the usable list.
- 1,000 rows per POST (the webhook's maximum). The webhook APPENDS: a re-run duplicates rows, so
  resume a partial load with --start (the offset printed after the last good POST).
- The webhook URL can write to the table: pass it as an argument, never commit it.
"""
import argparse, csv, json, sys, time, urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("csv"); ap.add_argument("url")
ap.add_argument("--start", type=int, default=0)
ap.add_argument("--batch", type=int, default=1000)
a = ap.parse_args()

CONF = {"high": 0, "medium": 1, "low": 2, "none": 3}
rows = list(csv.DictReader(open(a.csv, newline="", encoding="utf-8")))
rows.sort(key=lambda r: (r["passes_profile_bar"] != "yes", CONF[r["match_confidence"]],
                         -int(r["review_count"]) if r["review_count"] != "-" else 1))
print(f"rows {len(rows)}; sending from {a.start}", flush=True)
i = a.start
while i < len(rows):
    chunk = rows[i:i + a.batch]
    req = urllib.request.Request(a.url, data=json.dumps(chunk).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                body = resp.read().decode()[:200]
            break
        except Exception as e:
            if attempt == 3:
                sys.exit(f"FAILED at offset {i}: {e}")
            time.sleep(2 ** (attempt + 2))
    i += len(chunk)
    print(f"sent through {i}: {body}", flush=True)
