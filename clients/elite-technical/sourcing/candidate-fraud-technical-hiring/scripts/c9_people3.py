import json,os,sys,urllib.request,time,concurrent.futures as cf
S=sys.argv[1]; KEY=os.environ['BLITZ_API_KEY']
kept=json.load(open(S+'/c9_kept3.json'))
EXC=["Assistant","Intern","Coordinator","Sourcer","Former","Retired","Student","Specialist","Partner","Consultant","Recruiter II","Contract"]
CASCADE=[
 {"include_title":["Director of Talent Acquisition","Talent Acquisition Director","Head of Talent Acquisition","VP Talent Acquisition","Vice President Talent Acquisition","Vice President of Talent Acquisition","Director of Recruiting","Director of Recruitment","Head of Recruiting","VP Recruiting","Senior Director Talent Acquisition"],"exclude_title":EXC,"location":["US"],"include_headline_search":False},
 {"include_title":["Talent Acquisition Manager","Manager Talent Acquisition","Manager of Talent Acquisition","Recruiting Manager","Manager Recruiting","Recruitment Manager","Technical Recruiting Manager","Senior Manager Talent Acquisition"],"exclude_title":EXC,"location":["US"],"include_headline_search":False},
]
def call(path,body):
  req=urllib.request.Request('https://api.blitz-api.ai'+path,json.dumps(body).encode(),{'Content-Type':'application/json','x-api-key':KEY})
  for a in range(4):
    try: return json.load(urllib.request.urlopen(req,timeout=90))
    except urllib.error.HTTPError as e: err=e.read().decode()[:400]
    except Exception as e: err=str(e)
    time.sleep(2*(a+1))
  return {'error':err}
def one(u): return u, call('/v2/search/waterfall-icp-keyword',{"company_linkedin_url":u,"cascade":CASCADE,"max_results":5})
out={}
with cf.ThreadPoolExecutor(12) as ex:
  for k,v in ex.map(one,list(kept)): out[k]=v
json.dump({'cascade':CASCADE,'results':out},open(S+'/c9_people3.json','w'))
errs=sum('error' in v for v in out.values())
print('companies',len(out),'errors',errs,'people',sum(len(v.get('results') or []) for v in out.values()),'with>=1',sum(bool(v.get('results')) for v in out.values()))
