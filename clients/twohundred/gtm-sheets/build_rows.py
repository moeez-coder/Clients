#!/usr/bin/env python3
"""Turn a segment's repo CSVs into the JSON row sets loaded into its GTM Sheets tables.
Usage: build_rows.py <segment-folder> <date> <out-dir>
Leads get status = "launch set" (no freshness removals yet). Rows are the CSVs unchanged otherwise."""
import csv, json, sys, os
seg, date, out = sys.argv[1].rstrip('/'), sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True); base = os.path.basename(seg)
cos = list(csv.DictReader(open(f'{seg}/{date}-companies.csv')))
leads = list(csv.DictReader(open(f'{seg}/{date}-leads.csv')))
assert len({r['linkedin_url'] for r in leads}) == len(leads)
for r in leads: r['status'] = 'launch set'
json.dump(cos, open(f'{out}/{base}.companies.json', 'w')); json.dump(leads, open(f'{out}/{base}.leads.json', 'w'))
print(base, 'companies', len(cos), 'leads', len(leads))
