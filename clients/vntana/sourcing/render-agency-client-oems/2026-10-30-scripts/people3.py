import json,os,time,urllib.request,concurrent.futures as cf
K=os.environ['BLITZ_API_KEY']
EXC=["Security","Cyber","CFO","Chief Financial","Finance","Financial","Human Resources","HR","Recruiter","Legal","Counsel","Compliance","Procurement","Purchasing","Sales Representative","Account Executive","Account Manager","Intern","Student","Assistant","Retired","Advisor","Board Member"]
LOC=["US","CA","GB","IE","DE","FR","NL","SE","IT","ES","CH","DK","NO","FI","BE","AT"]
G={'A':["Director Product Marketing","VP Product Marketing","Product Marketing","Marketing Communications Manager","Marketing and Communications Director","Director eCommerce","VP eCommerce","Global Ecommerce Manager","E-Commerce Channel Manager","Head of E-Commerce","Director Digital Experience","Head of Digital Transformation","Chief Digital Officer","Head of Digital","VP of Digital","3D Visualization","Senior Digital Product Manager"],
 'B':["Director Aftermarket","VP Aftermarket","Head of Aftermarket","VP Service","Aftermarket Program Manager"],
 'C':["Director of Marketing","Head of Marketing","Marketing Director","Global Growth Marketing Leader","Senior Manager Creative","Chief Information Officer","CTO","Vice President of Technology","Director of IT Program Management","Vice President of Business Architecture","Global Technical Director","Director of Business Development","Chief Business Operations Officer"]}
def call(body):
    for a in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai/v2/search/people',data=json.dumps(body).encode(),headers={'x-api-key':K,'Content-Type':'application/json'}),timeout=120))
        except urllib.error.HTTPError as e:
            if e.code in(429,500,502,503,504): time.sleep(2**a);continue
            return {'error':e.code,'results':[],'cursor':None}
        except Exception: time.sleep(2**a)
    return {'error':'retries','results':[],'cursor':None}
P=json.load(open('pages.json'))
lis=sorted({p['li'] for v in P.values() for p in v})
def run(u):
    out=[]
    for g,titles in G.items():
        cur=None
        for page in range(8):
            body={"company":{"linkedin_url":[u]},"people":{"job_title":{"include":titles,"exclude":EXC},"location":{"country_code":LOC}},"max_results":50}
            if cur: body['cursor']=cur
            d=call(body)
            if d.get('error'):break
            for r in d['results']:
                out.append({'person':{k:r.get(k) for k in('first_name','last_name','full_name','headline','linkedin_url','location')},'jobs':[e for e in (r.get('experiences') or []) if e.get('job_is_current')][:3]})
            cur=d.get('cursor')
            if not cur:break
    open('pp3/'+u.rstrip('/').split('/')[-1][:80]+'.jsonl','w').write('\n'.join(json.dumps(x) for x in out));return len(out)
if __name__=='__main__':
    print(len(lis),'pages',flush=True)
    with cf.ThreadPoolExecutor(8) as ex: n=list(ex.map(run,lis))
    print('rows',sum(n),'max',max(n))
