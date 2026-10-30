import json,os,re,time,urllib.request,concurrent.futures as cf
K=os.environ['BLITZ_API_KEY']
A=json.load(open('accounts.json'))
def c(path,body):
    for a in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':K,'Content-Type':'application/json'}),timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in(429,500,502,503): time.sleep(2**a);continue
            return {'results':[],'err':e.code}
        except Exception: time.sleep(2**a)
    return {'results':[]}
STOP={'the','group','corporation','company','inc','ltd','gmbh','holding','holdings','international','industries','north','america','llc','corp','plc','spa','ag','sa','co'}
def toks(s): return [t for t in re.findall(r'[a-z0-9]{2,}',(s or '').lower()) if t not in STOP]
def job(i):
    a=A[i];names=[a['client_name']]
    if a['likely_company'] not in('','-') and a['likely_company']!=a['client_name']: names.append(a['likely_company'])
    best={}
    for nm in names:
        t0=toks(nm)
        if not t0: continue
        r=c('/v2/search/companies',{"company":{"name":{"include":[nm]}},"max_results":25})
        for x in r.get('results',[]):
            xn=toks(x.get('name'));emp=x.get('employees_on_linkedin') or 0
            if not xn or xn[0]!=t0[0]: continue        # brand token must lead the page name
            if x.get('linkedin_url'): best[x['linkedin_url']]={'li':x['linkedin_url'],'name':x.get('name'),'emp':emp,'domain':x.get('domain') or x.get('website')}
    pages=sorted(best.values(),key=lambda p:-p['emp'])
    if pages:
        top=pages[0]['emp'];pages=[p for p in pages if p['emp']>=max(100,top*0.15)][:3]
    return {'i':i,'pages':pages}
with cf.ThreadPoolExecutor(8) as ex: out=list(ex.map(job,range(len(A))))
json.dump(out,open('resolved2.json','w'))
print('with pages',sum(1 for o in out if o['pages']),'of',len(out),'| total pages',sum(len(o['pages']) for o in out))
for o in out[:10]:print(A[o['i']]['client_name'],[(p['name'],p['emp']) for p in o['pages']])
print('none:',[A[o['i']]['client_name'] for o in out if not o['pages']])
