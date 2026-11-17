import json, os, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
KEY=os.environ['BLITZ_API_KEY']; CF='blitz_cache.json'; cache=json.load(open(CF)) if os.path.exists(CF) else {}
def bpost(path, body):
    k=path+json.dumps(body,sort_keys=True)
    if k in cache: return cache[k]
    try:
        r=urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':KEY,'content-type':'application/json'})
        d=json.load(urllib.request.urlopen(r,timeout=60))
    except urllib.error.HTTPError as e: d={'_error':e.code,'_body':e.read().decode()[:200]}
    except Exception as e: d={'_error':str(e)[:80]}
    cache[k]=d; return d
R=[r for r in json.load(open('indeed_companies_180d_final.json')) if r['icp_fit']=='yes' and r['distinct_roles']>=2]
def clean(n):
    n=re.sub(r'\s+-\s+.*$','',n); n=re.sub(r'(?i)\b(inc|llc|l\.l\.c|corp|corporation|co|company|ltd|incorporated)\b\.?|[,®™]','',n)
    return re.sub(r'\s+',' ',n).strip()
def resolve(r):
    if r['company_linkedin_url']!='-': return r['company_linkedin_url'],'existing'
    if r['website']!='-':
        x=bpost('/v2/enrichment/domain-to-linkedin',{'domain':r['website']})
        if x.get('found') and x.get('company_linkedin_url'): return x['company_linkedin_url'],'domain'
    nm=clean(r['company_name'])
    for body in ({"company":{"name":{"include":[nm]},"hq":{"state":{"include":["Indiana"]}}},"max_results":3},
                 {"company":{"name":{"include":[nm]}},"max_results":3}):
        x=bpost('/v2/search/companies',body)
        res=x.get('results') or []
        if res:
            c=res[0].get('company',res[0])
            if c.get('linkedin_url'): return c['linkedin_url'],'name:'+c.get('name','')
    return '-','unresolved'
with ThreadPoolExecutor(8) as ex: out=list(ex.map(resolve,R))
for r,(u,how) in zip(R,out): r['company_linkedin_url']=u; r['li_resolved_by']=how
json.dump(R,open('c7_236.json','w')); json.dump(cache,open(CF,'w'))
import collections; print(collections.Counter(h.split(':')[0] for _,h in out))
for r in R:
    if r['li_resolved_by'].startswith('name:'): print('NAME |',r['company_name'],'=>',r['li_resolved_by'][5:],r['company_linkedin_url'])
print('unresolved:',[r['company_name'] for r in R if r['company_linkedin_url']=='-'])
