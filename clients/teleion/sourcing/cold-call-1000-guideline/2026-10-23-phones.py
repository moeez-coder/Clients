import os,json,urllib.request,urllib.error,csv,time,concurrent.futures as cf
K=os.environ['PROSPEO_API_KEY']
def post(path,b):
    for i in range(4):
        rq=urllib.request.Request('https://api.prospeo.io/'+path,json.dumps(b).encode(),{'X-KEY':K,'Content-Type':'application/json','User-Agent':'curl/8.5.0'})
        try: return json.load(urllib.request.urlopen(rq,timeout=90))
        except urllib.error.HTTPError as e:
            body=e.read().decode()[:300]
            if e.code==429: time.sleep(3+3*i);continue
            return {'http':e.code,'body':body}
        except Exception as e: time.sleep(3+3*i)
    return {'http':0,'body':'network'}
def credits(): return post('account-information',{})['response']['remaining_credits']
F='/home/user/Clients/clients/teleion/sourcing/cold-call-1000-guideline/2026-10-23-leads.csv'
rows=list(csv.DictReader(open(F)))
done={}
if os.path.exists('m_phone.json'): done=json.load(open('m_phone.json'))
FLOOR=1500
def one(x):
    j=post('enrich-person',{'only_verified_mobile':True,'enrich_mobile':True,'data':{'linkedin_url':x['linkedin_url']}})
    m=((j.get('person') or {}).get('mobile') or {}) if 'http' not in j else {}
    return x['linkedin_url'],{'mobile':m.get('mobile_international') or m.get('mobile'),'country':m.get('mobile_country'),'status':m.get('status'),'err':j.get('body') if 'http' in j else None}
todo=[x for x in rows if x['linkedin_url'] not in done]
i=0
while i<len(todo):
    c=credits()
    if c-10*25<FLOOR: print('stopping at credits',c);break
    batch=todo[i:i+25];i+=25
    with cf.ThreadPoolExecutor(5) as ex:
        for u,v in ex.map(one,batch): done[u]=v
    json.dump(done,open('m_phone.json','w'))
print('processed',len(done),'found',sum(1 for v in done.values() if v['mobile']),'credits left',credits())
