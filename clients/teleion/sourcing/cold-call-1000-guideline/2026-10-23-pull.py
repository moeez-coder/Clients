import os,json,pickle,time,urllib.request,urllib.error,concurrent.futures as cf
K=os.environ['BLITZ_API_KEY']
U=pickle.load(open('m_univ.pkl','rb'))
KW=["compliance","risk","BSA","AML","fraud","financial crimes","sanctions","BaaS","security","CISO","CIO","information officer","data","AI","artificial intelligence","machine learning","infrastructure","technology","marketing","sales operations","payments","treasury","treasurer","controller","CFO","financial officer","finance","accounting","operations","procurement","vendor","supplier","human resources","CHRO","people officer"]
def call(b):
    for i in range(5):
        try:
            rq=urllib.request.Request('https://api.blitz-api.ai/v2/search/people',json.dumps(b).encode(),{'x-api-key':K,'content-type':'application/json','User-Agent':'curl/8.5.0'})
            return json.load(urllib.request.urlopen(rq,timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503): time.sleep(2+3*i);continue
            return {'error':e.code,'body':e.read().decode()[:300]}
        except Exception: time.sleep(2+3*i)
    return {'error':'net'}
urls=[v['li'] for v in U.values() if v['li']]
batches=[urls[i:i+5] for i in range(0,len(urls),5)]
def run(bt):
    out=[];cur=None
    for p in range(12):
        b={"company":{"linkedin_url":bt},"people":{"job_level":["C-Team","VP","Director"],"job_title":{"include":KW},"location":{"country_code":["US"]}},"max_results":50}
        if cur: b['cursor']=cur
        r=call(b)
        if 'error' in r: return out,r
        out+=r.get('results',[]);cur=r.get('cursor')
        if not cur: break
    return out,None
res=[];errs=[]
with cf.ThreadPoolExecutor(12) as ex:
    for o,e in ex.map(run,batches):
        res+=o
        if e: errs.append(e)
json.dump(res,open('m_people_raw.json','w'))
print('batches',len(batches),'people',len(res),'errors',len(errs),errs[:2])
