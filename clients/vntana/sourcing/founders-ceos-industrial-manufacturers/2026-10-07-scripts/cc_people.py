import json,os,sys,time,urllib.request,concurrent.futures as cf
KEY=os.environ['BLITZ_API_KEY']
T=["Founder","Co-Founder","CEO","Chief Executive Officer","President","Owner","Chairman","Managing Director","General Manager","Division President","Group President","Business Unit President","Division Head","Head of Division","Executive Director"]
EXC=["Assistant","Intern","Student","Associate","Retired","Advisor","Board Member","Non-Executive"]
LOC=["US","CA","GB","IE","AU","NZ","DE"]
def call(body):
    for a in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai/v2/search/people',data=json.dumps(body).encode(),headers={'x-api-key':KEY,'Content-Type':'application/json'}),timeout=120))
        except urllib.error.HTTPError as e:
            if e.code in(429,500,502,503,504): time.sleep(2**a); continue
            return {'error':e.code,'msg':e.read()[:300].decode('utf8','ignore'),'results':[],'cursor':None}
        except Exception: time.sleep(2**a)
    return {'error':'retries','results':[],'cursor':None}
def run(item):
    folder,n,urls,loc=item; fn=f'{folder}/p{n:04d}.jsonl'
    if os.path.exists(fn+'.done'): return n,-1
    cnt=0;cur=None
    with open(fn,'w') as f:
        for page in range(8):
            body={"company":{"linkedin_url":urls},"people":{"job_title":{"include":T,"exclude":EXC}},"max_results":50}
            if loc: body["people"]["location"]={"country_code":loc}
            if cur: body['cursor']=cur
            d=call(body)
            if d.get('error'): f.write(json.dumps({'_error':d,'urls':urls})+'\n'); break
            for r in d['results']:
                f.write(json.dumps({'person':{k:r.get(k) for k in('first_name','last_name','full_name','headline','linkedin_url','location','connections_count')},'jobs':[e for e in (r.get('experiences') or []) if e.get('job_is_current')][:4]})+'\n'); cnt+=1
            cur=d.get('cursor')
            if not cur: break
    open(fn+'.done','w').write(str(cnt)); return n,cnt
def go(urls,folder,loc):
    items=[(folder,i,urls[i*5:(i+1)*5],loc) for i in range((len(urls)+4)//5)]; tot=0
    with cf.ThreadPoolExecutor(8) as ex:
        for n,c in ex.map(run,items): tot+=max(c,0)
    return tot
if __name__=='__main__':
    A=json.load(open('accounts.json'))['accounts']
    urls=[a['linkedin_url'] for a in A.values() if a['linkedin_url']]
    print(len(urls),'companies',flush=True)
    print('passA rows',go(urls,'pA',LOC),flush=True)
