#!/usr/bin/env python3
"""Build the three GTM Sheets row sets (Companies, Jobs, Leads) for one recruiter segment.

Usage: build_gtm_payloads.py <segment-folder> <out-dir>

- Companies: every row of <date>-companies.csv (all hiring companies that passed the revenue/
  industry/DNC filters), with leads_selected showing which ones produced leads.
- Jobs: one row per job_url behind the launch set, derived from <date>-leads.csv. Also written to
  the repo as <date>-jobs.csv, a derived file and not a new API pull. The raw Blitz /v2/jobs/company pulls
  (pull8_<seg>.json) were never committed, so only the postings that drove a lead are reproducible.
- Leads: rows with selected_for_launch == "yes", plus a `status` key: "launch set", or
  "removed: <reason>" when the folder has a <date>-heyreach-removed.csv.
"""
import csv, json, sys, os, glob, urllib.parse
seg, out = sys.argv[1].rstrip('/'), sys.argv[2]
date = '2026-11-05'
leads = [r for r in csv.DictReader(open(f'{seg}/{date}-leads.csv')) if r['selected_for_launch'] == 'yes']
companies = list(csv.DictReader(open(f'{seg}/{date}-companies.csv')))
def n(u): return urllib.parse.unquote(u).strip().lower().rstrip('/')
removed = {}
rf = f'{seg}/{date}-heyreach-removed.csv'
if os.path.exists(rf):
    for r in csv.DictReader(open(rf)): removed[n(r['linkedin_url'])] = r['reason']
for r in leads:
    r['status'] = f"removed: {removed[n(r['linkedin_url'])]}" if n(r['linkedin_url']) in removed else 'launch set'
jobs, cnt = {}, {}
for r in leads:
    k = r['job_url']; cnt[k] = cnt.get(k, 0) + 1
    jobs.setdefault(k, dict(job_url=k, job_title=r['open_role_raw'], open_role=r['open_role'],
        open_role_with_article=r['open_role_with_article'], job_posted=r['job_posted'],
        job_ai_summary=r['job_ai_summary'], jd=r['jd'], company_name=r['company_name_clean'],
        company_linkedin_url=r['company_linkedin_url'], company_domain=r['company_domain'], segment=r['segment']))
for k, j in jobs.items(): j['leads_on_job'] = cnt[k]
jl = list(jobs.values())
with open(f'{seg}/{date}-jobs.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(jl[0].keys())); w.writeheader(); w.writerows(jl)
os.makedirs(out, exist_ok=True); base = os.path.basename(seg)
for name, rows in (('companies', companies), ('jobs', jl), ('leads', leads)):
    json.dump(rows, open(f'{out}/{base}.{name}.json', 'w'))
print(base, 'companies', len(companies), 'jobs', len(jl), 'leads', len(leads), 'removed', sum(1 for r in leads if r['status'] != 'launch set'))
