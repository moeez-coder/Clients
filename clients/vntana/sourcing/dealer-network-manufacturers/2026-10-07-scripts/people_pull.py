import json,os,csv,sys,time,urllib.request,concurrent.futures as cf
KEY=os.environ['BLITZ_API_KEY']
T=["Channel Marketing","Dealer Marketing","Dealer Development","Co-op Marketing","Coop Marketing","Cooperative Marketing","Marketing Communications","Marcom","Distributor Marketing","Dealer Programs","Dealer Network","Dealer Relations","Dealer Operations","Partner Marketing","Channel Manager","Channel Programs","Rep Program","Dealer Experience","Dealer Support"]
EXC=["Intern","Student","Assistant","Receptionist","Recruiter","Consultant","Freelance","Retired"]
LOC=["US","CA","GB","IE","AU","NZ"]
def call(body):
    for a in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai/v2/search/people',data=json.dumps(body).encode(),headers={'x-api-key':KEY,'Content-Type':'application/json'}),timeout=120))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504): time.sleep(2**a); continue
            return {'error':e.code,'msg':e.read()[:300].decode('utf8','ignore'),'results':[],'cursor':None}
        except Exception: time.sleep(2**a)
    return {'error':'retries','results':[],'cursor':None}
def run(item):
    n,urls=item; fn=f'people/p{n:04d}.jsonl'
    if os.path.exists(fn+'.done'): return n,-1
    cnt=0; cur=None
    with open(fn,'w') as f:
        for page in range(40):
            body={"company":{"linkedin_url":urls},"people":{"job_title":{"include":T,"exclude":EXC},"job_level":["C-Team","VP","Director","Manager"],"location":{"country_code":LOC}},"max_results":50}
            if cur: body['cursor']=cur
            d=call(body)
            if d.get('error'): f.write(json.dumps({'_error':d,'urls':urls})+'\n'); break
            for r in d['results']:
                f.write(json.dumps({'person':{k:r.get(k) for k in ('first_name','last_name','full_name','headline','linkedin_url','location','connections_count')},'jobs':[e for e in (r.get('experiences') or []) if e.get('job_is_current')][:4]})+'\n'); cnt+=1
            cur=d.get('cursor')
            if not cur: break
    open(fn+'.done','w').write(str(cnt)); return n,cnt
if __name__=="__main__":
    rows=list(csv.DictReader(open('/home/user/Clients/clients/vntana/sourcing/dealer-network-manufacturers/2026-10-07-companies-qualified.csv')))
    urls=[r['company_linkedin_url'] for r in rows if r['tier'][:2] in('Q1','Q2','Q3') and r['company_linkedin_url']!='-']
    urls=list(dict.fromkeys(urls)); print(len(urls),'companies',flush=True)
    items=[(i,urls[i*10:(i+1)*10]) for i in range((len(urls)+9)//10)]
    tot=0
    with cf.ThreadPoolExecutor(8) as ex:
        for n,c in ex.map(run,items):
            tot+=max(c,0)
            if n%20==0: print(n,len(items),tot,flush=True)
    print('DONE',tot,flush=True)
