import json,os,re,time,urllib.request,urllib.parse,concurrent.futures as cf
from exa_clients import exa
KEY=os.environ['BLITZ_API_KEY']
A=json.load(open('accounts.json'))
def b(path,body):
    for a in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':KEY,'Content-Type':'application/json'}),timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in(429,500,502,503): time.sleep(2**a);continue
            return {'found':False,'err':e.code}
        except Exception: time.sleep(2**a)
    return {'found':False}
def toks(s): return set(re.findall(r'[a-z0-9]{3,}',s.lower()))-{'the','group','corporation','company','inc','ltd','gmbh','holding','holdings','international','industries','north','america'}
def host(u):
    h=urllib.parse.urlparse(u).netloc.lower();return h[4:] if h.startswith('www.') else h
def job(i):
    a=A[i];nm=a['likely_company'] if a['likely_company'] not in('','-') else a['client_name']
    r=exa({"query":f"{a['client_name']} official website","numResults":4,"category":"company"})
    cands=[]
    for x in r.get('results',[]):
        h=host(x['url']);cands.append(h)
    res={'i':i,'name':nm,'cands':cands,'domain':None,'li':None,'li_name':None}
    t=toks(a['client_name'])|toks(nm)
    for h in cands:
        lab=h.split('.')[0]
        if not any(tok in lab or lab in tok for tok in t if len(tok)>=3) and not any(tok in h for tok in t): continue
        r1=b('/v2/enrichment/domain-to-linkedin',{'domain':h})
        if not r1.get('found'): continue
        e=b('/v2/enrichment/company',{'company_linkedin_url':r1['company_linkedin_url']}).get('company') or {}
        res.update(domain=h,li=r1['company_linkedin_url'],li_name=e.get('name'),emp=e.get('employees_on_linkedin') or e.get('employees_count'),country=(e.get('hq') or {}).get('country_code') if isinstance(e.get('hq'),dict) else None)
        break
    return res
with cf.ThreadPoolExecutor(8) as ex: out=list(ex.map(job,range(len(A))))
json.dump(out,open('resolved.json','w'))
print('resolved',sum(1 for o in out if o['li']),'of',len(out))
for o in out[:12]:print(o['name'],'|',o['domain'],'|',o['li'],'|',o['li_name'])
print('unresolved',[o['name'] for o in out if not o['li']][:40])
