import json,os,sys,urllib.request,time
S=sys.argv[1]; KEY=os.environ['BLITZ_API_KEY']
STATES=['District of Columbia','Maryland','Virginia','Maine','New Hampshire','Vermont','Massachusetts','Rhode Island','Connecticut','New York','New Jersey','Pennsylvania','Delaware','North Carolina','South Carolina','Georgia','Florida','Ohio','Michigan','Indiana','Illinois','Wisconsin','Minnesota','Iowa','Missouri','North Dakota','South Dakota','Nebraska','Kansas']
IND=["Defense and Space","Defense and Space Manufacturing","IT Services and IT Consulting","Information Technology and Services","Engineering Services","Civil Engineering","Software Development","Computer and Network Security","Research Services","Aviation and Aerospace Component Manufacturing","Business Consulting and Services","Environmental Services","Professional Services","Telecommunications","Data Infrastructure and Analytics","Space Research and Technology","Architecture and Planning","Technology; Information and Internet","Information Services"]
def call(body):
  req=urllib.request.Request('https://api.blitz-api.ai/v2/search/companies',json.dumps(body).encode(),{'Content-Type':'application/json','x-api-key':KEY})
  for a in range(4):
    try: return json.load(urllib.request.urlopen(req,timeout=90))
    except urllib.error.HTTPError as e: err=e.read().decode()[:300]
    except Exception as e: err=str(e)
    time.sleep(2*(a+1))
  return {'error':err}
out={}; calls=0
for st in STATES:
  cur=None; n=0
  while True:
    body={'company':{'industry':{'include':IND},'revenue':{'min':100000000,'max':1000000000},'hq':{'country_code':['US'],'state':{'include':[st]}}},'max_results':50,'cursor':cur}
    d=call(body); calls+=1
    if 'error' in d: print('ERR',st,d['error'],file=sys.stderr); break
    for c in d.get('results') or []:
      if (c.get('hq') or {}).get('state')!=st: continue
      out[c['linkedin_url']]=c; n+=1
    cur=d.get('cursor')
    if not cur or n>3000: break
  print(st,n,len(out),file=sys.stderr,flush=True)
json.dump(out,open(S+'/blitz_company_sweep.json','w'))
print('companies',len(out),'calls',calls)
import collections; print(collections.Counter(c.get('revenue_range') for c in out.values()))
