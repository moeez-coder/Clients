#!/usr/bin/env python3
"""Load the Recruitment Specific workbook's three tables from the repo CSVs through each table's webhook.

Usage: load_tables.py <companies_webhook_url> <jobs_webhook_url> <leads_webhook_url>
Webhook URLs can write to their tables: pass them as arguments, never commit them. A webhook load APPENDS,
so a re-run duplicates rows. Leads get company_name cleaned for the {COMPANY} message variable (legal suffixes,
trademarks and brackets removed); the CSV value is kept as company_name_raw.
"""
import csv, json, re, sys, time, urllib.request
D = "clients/grn-piedmont/sourcing/recruitment-specific-open-roles/2026-11-16-"
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

leads = list(csv.DictReader(open(D + "leads.csv")))
assert len({r["linkedin_url"] for r in leads}) == len(leads)
for r in leads: r["company_name_raw"] = r["company_name"]; r["company_name"] = clean_company(r["company_name"])
for name, url, rows in (("companies", sys.argv[1], list(csv.DictReader(open(D + "companies.csv")))),
                        ("jobs", sys.argv[2], list(csv.DictReader(open(D + "jobs.csv")))), ("leads", sys.argv[3], leads)):
    print(name, len(rows)); send(url, rows)
