#!/usr/bin/env python3
"""Load the general TAM (2026-11-24-companies-qc.csv, all 22,631 rows, every QC tier) into GTM Sheets workbook
"GRN Piedmont | General TAM | 2026-11-24", table "1 Companies (TAM, all tiers)", through its webhook.
Usage: python3 load_general_tam.py <webhook_url>
The webhook URL can write to the table: pass it as an argument, never commit it. A webhook load APPENDS (re-run = duplicates).
"""
import csv, json, sys, time, urllib.request
SRC = "clients/grn-piedmont/sourcing/general-tam/2026-11-24-companies-qc.csv"
rows = list(csv.DictReader(open(SRC)))
url = sys.argv[1]
for i in range(0, len(rows), 1000):
    req = urllib.request.Request(url, json.dumps(rows[i:i + 1000]).encode(), {"Content-Type": "application/json", "User-Agent": "curl/8.5.0"}, method="POST")
    for a in range(4):
        try: body = urllib.request.urlopen(req, timeout=180).read().decode()[:100]; break
        except Exception as e:
            if a == 3: sys.exit(f"FAILED at {i}: {e}")
            time.sleep(2 ** (a + 1))
    print(i + len(rows[i:i + 1000]), body, flush=True)
