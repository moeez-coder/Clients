#!/usr/bin/env python3
"""POST a JSON array of rows to a GTM Sheets table webhook in batches of 500.
Usage: push_rows.py <rows.json> <webhook_url> [--start N]
The webhook APPENDS, so a re-run duplicates rows (use --start to resume). The URL can write to the table, so it is never committed."""
import json, sys, time, urllib.request
rows = json.load(open(sys.argv[1])); url = sys.argv[2]
i = int(sys.argv[sys.argv.index('--start') + 1]) if '--start' in sys.argv else 0
while i < len(rows):
    chunk = rows[i:i + 500]
    req = urllib.request.Request(url, data=json.dumps(chunk).encode(), headers={'Content-Type': 'application/json'}, method='POST')
    for a in range(4):
        try:
            body = urllib.request.urlopen(req, timeout=120).read().decode()[:80]; break
        except Exception as e:
            if a == 3: sys.exit(f'FAILED at offset {i}: {e}')
            time.sleep(2 ** (a + 1))
    i += len(chunk)
print(f'{sys.argv[1].split("/")[-1]}: sent {i} ({body})')
