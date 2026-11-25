#!/usr/bin/env python3
"""Load one MPC segment workbook (2026-11-24) from the repo CSVs through each table's webhook.

Usage: load_mpc_segment.py <segment> <companies_webhook|-> <jobs_webhook|-> <leads_webhook|->
  segment = executive | operations-plant | engineering-quality | supply-chain-purchasing | ehs-maintenance
Webhook URLs can write to their tables: pass them as arguments, never commit them. A webhook load APPENDS, so a
re-run duplicates rows ("-" skips a table already loaded). Leads get company_name cleaned for the {Company_Name}
variable, as in load_tables.py; the CSV value is kept as company_name_raw.
"""
import csv, json, os, re, sys, time, urllib.request
SUF = re.compile(r"[,.]?\s+(inc|llc|l\.l\.c|l\.p|lp|ltd|corp|co|company|incorporated|corporation|llp|plc)\.?$", re.I)
def clean_company(n):
    n = re.sub(r"[®™©]|\(.*?\)", "", n).split(" - ")[0].split(" | ")[0].strip(" ,.")
    for _ in range(2): n = SUF.sub("", n).strip(" ,.")
    return n.title() if n.isupper() and len(n) > 5 else n
def send(url, rows):
    for i in range(0, len(rows), 500):
        req = urllib.request.Request(url, json.dumps(rows[i:i + 500]).encode(), {"Content-Type": "application/json", "User-Agent": "curl/8.5.0"}, method="POST")
        for a in range(4):
            try: body = urllib.request.urlopen(req, timeout=120).read().decode()[:120]; break
            except Exception as e:
                if a == 3: sys.exit(f"FAILED at {i}: {e}")
                time.sleep(2 ** (a + 1))
        print(i + len(rows[i:i + 500]), body, flush=True)
seg = sys.argv[1]; DATE = os.environ.get("DATE", "2026-11-24")  # DATE=2026-11-25 loads a later wave (pass "-" for tables not in it)
D = f"clients/grn-piedmont/sourcing/mpc-{seg}/{DATE}-"
leads = list(csv.DictReader(open(D + "leads.csv")))
assert len({r["linkedin_url"] for r in leads}) == len(leads)
for r in leads: r["company_name_raw"] = r["company_name"]; r["company_name"] = clean_company(r["company_name"])
tables = [("companies", list(csv.DictReader(open(D + "companies.csv"))) if sys.argv[2] != "-" else []),
          ("jobs", list(csv.DictReader(open(D + "jobs.csv"))) if sys.argv[3] != "-" else []), ("leads", leads)]
for (name, rows), url in zip(tables, sys.argv[2:5]):
    if url == "-": continue
    print(seg, name, len(rows), "launch set:", sum(1 for r in rows if r.get("status") == "launch set")); send(url, rows)
