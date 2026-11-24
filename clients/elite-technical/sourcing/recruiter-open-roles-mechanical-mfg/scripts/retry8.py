import json,sys,time
import importlib; sys.argv=[sys.argv[0],sys.argv[1]]
seg=sys.argv[1]
src=open('pull8.py').read().split("tam={};cur=None")[0]   # reuse call/JOB/defs
exec(src)
from segs8 import FALLBACK
EXC=["Assistant","Intern","Coordinator","Sourcer","Former","Retired","Student","Recruiter","Specialist","Partner","Consultant","Sales"]
D=json.load(open(f'pull8_{seg}.json')); fixed=0
for u,v in D['data'].items():
  if 'error' in (v['jobs'] or {}): v['jobs']=call('/v2/jobs/company',{"company_linkedin_url":u,"job":JOB,"max_results":5}); fixed+=1
  if 'error' in (v['hm'] or {}): v['hm']=call('/v2/search/waterfall-icp-keyword',{"company_linkedin_url":u,"cascade":[{"include_title":s['hm'],"exclude_title":EXC,"location":["US"],"include_headline_search":False}],"max_results":10}); fixed+=1
  if (v['hm'] or {}).get('results') is not None and not v['hm'].get('results') and (v['fb'] is None or 'error' in v['fb']):
    v['fb']=call('/v2/search/waterfall-icp-keyword',{"company_linkedin_url":u,"cascade":[{"include_title":FALLBACK,"exclude_title":EXC,"location":["US"],"include_headline_search":False}],"max_results":3}); fixed+=1
json.dump(D,open(f'pull8_{seg}.json','w'))
print(seg,'retried',fixed,'remaining errors',sum(sum('error' in (v[k] or {}) for k in ('jobs','hm','fb')) for v in D['data'].values()))
