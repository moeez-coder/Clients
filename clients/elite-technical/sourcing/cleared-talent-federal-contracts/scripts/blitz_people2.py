import json,os,sys,urllib.request,time,concurrent.futures as cf
S=sys.argv[1]; KEY=os.environ['BLITZ_API_KEY']
kept=json.load(open(S+'/kept.json.new'))
EXC=["Assistant","Intern","Recruiter","Coordinator","Sourcer","Specialist","Sales","Marketing","Business Development","Capture","Proposal","Contracts","Finance","Legal","Former","Retired","Student"]
CASCADE=[
 {"include_title":["VP Engineering","Vice President Engineering","Director of Engineering","Engineering Director","VP Information Technology","Vice President Information Technology","Director of Information Technology","IT Director","Director IT","Director of Technical Operations","Director Technical Operations","Director of Software Engineering","Director of Infrastructure","Chief Technology Officer","Chief Information Officer"],"exclude_title":EXC,"location":["US"],"include_headline_search":False},
 {"include_title":["Director of Talent Acquisition","Head of Talent Acquisition","VP Talent Acquisition","Vice President Talent Acquisition","Talent Acquisition Director","Director of Recruiting","VP Recruiting","Contingent Workforce","Contingent Labor","Workforce Solutions"],"exclude_title":["Assistant","Intern","Coordinator","Sourcer","Former"],"location":["US"],"include_headline_search":False},
]
def call(path,body):
  req=urllib.request.Request('https://api.blitz-api.ai'+path,json.dumps(body).encode(),{'Content-Type':'application/json','x-api-key':KEY})
  for a in range(4):
    try: return json.load(urllib.request.urlopen(req,timeout=90))
    except urllib.error.HTTPError as e: err=e.read().decode()[:400]; 
    except Exception as e: err=str(e)
    time.sleep(2*(a+1))
  return {'error':err}
def one(x):
  return x['match']['linkedin_url'], call('/v2/search/waterfall-icp-keyword',{"company_linkedin_url":x['match']['linkedin_url'],"cascade":CASCADE,"max_results":8})
out={}
with cf.ThreadPoolExecutor(6) as ex:
  for k,v in ex.map(one,kept): out[k]=v
json.dump({'cascade':CASCADE,'results':out},open(S+'/blitz_people_raw2.json','w'))
tot=0
for k,v in out.items():
  n=len(v.get('results') or []); tot+=n
  if 'error' in v: print('ERR',k,v['error'][:200])
print('people',tot)
first=next((v for v in out.values() if v.get('results')),None)
print(json.dumps(first['results'][0],indent=0)[:1500] if first else 'none')
