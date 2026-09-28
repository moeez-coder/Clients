import json,os,time,urllib.request,concurrent.futures as cf
K=os.environ['BLITZ_API_KEY']
def b(path,body):
    for a in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':K,'Content-Type':'application/json'}),timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503): time.sleep(2**a); continue
            return {'found':False,'err':e.code}
        except Exception: time.sleep(2**a)
    return {'found':False}
N=json.load(open('exa_new_domains.json'))
def job(dm):
    r=b('/v2/enrichment/domain-to-linkedin',{'domain':dm})
    if not r.get('found'): return dm,None
    c=b('/v2/enrichment/company',{'company_linkedin_url':r['company_linkedin_url']})
    return dm,{'li':r['company_linkedin_url'],'name':r.get('company_name'),'company':c.get('company')}
with cf.ThreadPoolExecutor(10) as ex: out=dict(ex.map(job,N))
json.dump(out,open('exa_resolved.json','w'))
print('resolved',sum(1 for v in out.values() if v),'enriched',sum(1 for v in out.values() if v and v['company']))
