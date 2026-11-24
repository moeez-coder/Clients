import json,os,sys,re,csv,time,urllib.request,concurrent.futures as cf,collections
from segs8 import SEGS,FALLBACK
KEY=os.environ['BLITZ_API_KEY']; seg=sys.argv[1]; s=SEGS[seg]
def call(path,b):
  req=urllib.request.Request('https://api.blitz-api.ai'+path,json.dumps(b).encode(),{'Content-Type':'application/json','x-api-key':KEY})
  for a in range(5):
    try: return json.load(urllib.request.urlopen(req,timeout=120))
    except urllib.error.HTTPError as e: err=e.read().decode()[:300]
    except Exception as e: err=str(e)
    time.sleep(2*(a+1))
  return {'error':err}
JOB={"title":{"include":s['titles'],"exclude":s['exclude']},"date_posted":{"last_days":30},"location":{"country_code":{"include":["US"]}}}
tam={};cur=None;pages=0
while True:
  d=call('/v2/company/tam-by-jobs',{"job":JOB,"company":{"is_agency":False,"employee_count":{"min":501,"max":10000},"hq":{"country_code":{"include":["US"]}}},"max_results":50,"cursor":cur}); pages+=1
  if 'error' in d: print('TAM ERR',d,file=sys.stderr); break
  for r in d.get('results',[]): tam[r['company']['linkedin_url']]=r
  cur=d.get('cursor')
  if not cur or pages>1000: break
def nm(x): x=re.sub(r'[^a-z0-9 ]',' ',(x or '').lower()); x=re.sub(r'\b(inc|llc|corp|corporation|co|company|the|group|holdings|ltd)\b',' ',x); return re.sub(r'\s+',' ',x).strip()
dnc=[nm(r['Company Name']) for r in csv.DictReader(open('/home/user/Clients/clients/elite-technical/context/dnc-list.csv'))]
def isdnc(n):
  n=nm(n); return any(x and (x==n or (len(x)>=6 and re.search(r'\b'+re.escape(x)+r'\b',n)) or (len(n)>=6 and re.search(r'\b'+re.escape(n)+r'\b',x))) for x in dnc)
BAD={'Higher Education','Primary and Secondary Education','Education Administration Programs','Government Administration','Non-profit Organizations','Individual and Family Services','Staffing and Recruiting','Armed Forces','Public Safety','Civic and Social Organizations','Religious Institutions','Political Organizations','Legislative Offices','Public Policy Offices','International Affairs','Executive Offices','Administration of Justice'}
funnel=collections.Counter({'hiring companies':len(tam)}); keep={}
for u,r in tam.items():
  c=r['company']
  if c.get('revenue_range')!='$100M-$1B': funnel['revenue']+=1; continue
  if c.get('industry') in BAD: funnel['industry']+=1; continue
  if re.search(r'staffing|recruit',(c.get('name') or '')+' '+(c.get('industry') or ''),re.I): funnel['staffing']+=1; continue
  if isdnc(c['name']): funnel['dnc']+=1; continue
  keep[u]=r
funnel['passed']=len(keep)
EXC=["Assistant","Intern","Coordinator","Sourcer","Former","Retired","Student","Recruiter","Specialist","Partner","Consultant","Sales"]
def one(u):
  j=call('/v2/jobs/company',{"company_linkedin_url":u,"job":JOB,"max_results":5})
  h=call('/v2/search/waterfall-icp-keyword',{"company_linkedin_url":u,"cascade":[{"include_title":s['hm'],"exclude_title":EXC,"location":["US"],"include_headline_search":False}],"max_results":10})
  f=None
  if not h.get('results'): f=call('/v2/search/waterfall-icp-keyword',{"company_linkedin_url":u,"cascade":[{"include_title":FALLBACK,"exclude_title":EXC,"location":["US"],"include_headline_search":False}],"max_results":3})
  return u,j,h,f
out={}
with cf.ThreadPoolExecutor(20) as ex:
  for u,j,h,f in ex.map(one,list(keep)): out[u]={'company':keep[u]['company'],'matched_jobs':keep[u].get('matched_jobs'),'jobs':j,'hm':h,'fb':f}
json.dump({'funnel':funnel,'data':out},open(f'pull8_{seg}.json','w'))
print(seg,dict(funnel),'errors',sum(sum('error' in (v[k] or {}) for k in ('jobs','hm','fb')) for v in out.values()),flush=True)
