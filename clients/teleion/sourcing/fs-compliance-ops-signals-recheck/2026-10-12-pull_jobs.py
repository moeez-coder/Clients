import csv,json,os,time,urllib.request,concurrent.futures as cf
K=os.environ['BLITZ_API_KEY']
pool=list(csv.DictReader(open('pool.csv')))
def call(body):
    for i in range(4):
        try:
            rq=urllib.request.Request('https://api.blitz-api.ai/v2/jobs/company',json.dumps(body).encode(),{'x-api-key':K,'content-type':'application/json','User-Agent':'curl/8.5.0'})
            return json.load(urllib.request.urlopen(rq,timeout=60))
        except Exception as e:
            err=str(e); time.sleep(1+i*2)
    return {'error':err}
def one(x):
    jobs=[];cur=None
    for p in range(6):
        b={'company_linkedin_url':x['linkedin_url'],'job':{'date_posted':{'last_days':90}},'max_results':50,'cursor':cur}
        r=call(b)
        if 'error' in r: return x['linkedin_url'],None,r['error']
        jobs+=r.get('results',[]);cur=r.get('cursor')
        if not cur: break
    return x['linkedin_url'],jobs,None
out=open('jobs_raw.jsonl','w')
with cf.ThreadPoolExecutor(16) as ex:
    for u,j,e in ex.map(one,pool):
        out.write(json.dumps({'linkedin_url':u,'jobs':j,'error':e})+'\n')
