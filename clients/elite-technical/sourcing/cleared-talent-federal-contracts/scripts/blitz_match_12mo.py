import json,re,os,sys,urllib.request,time,concurrent.futures as cf
S=sys.argv[1]; KEY=os.environ['BLITZ_API_KEY']
raw=json.load(open(S+'/usas_12mo_raw.json'))
BAD=re.compile(r'\b(OPTION|EXTENSION|EXTEND|BRIDGE|RENEW|RENEWAL|CONTINUATION|EXERCISE)\b',re.I)
rec={}
for x in raw:
  if BAD.search(x['Description'] or ''): continue
  x['_src']='usaspending'
  k=x['Recipient UEI'] or x['Recipient Name']
  if k not in rec or x['Award Amount']>rec[k]['Award Amount']: rec[k]=x
for o in json.load(open(S+'/dod_awards.json')):
  if not o['tier']: continue
  k='DOD:'+o['company']
  if k not in rec or (o['amount'] or 0)>(rec[k]['Award Amount'] or 0):
    rec[k]={'Recipient Name':o['company'],'Recipient UEI':None,'Award Amount':o['amount'] or 0,'_state':o['state'],'_tier':o['tier'],'_src':'war.gov','Description':o['summary'],'Awarding Agency':'Department of Defense','Awarding Sub Agency':o['branch'],'award_date':o['award_date'],'url':o['url'],'Award ID':None,'generated_internal_id':None}
recs=list(rec.values())
cache={}
for f in ['/blitz_matches_wide2.json','/blitz_matches2.json']:
  for o in json.load(open(S+f)): cache[o['award']['Recipient Name']]=(o['match'],o['candidates'])
STOP=r'\b(INC|INCORPORATED|LLC|L\.L\.C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PLLC|PC|THE|JV|JOINT VENTURE|GROUP|HOLDINGS)\b'
STOP2=r'\b(INC|INCORPORATED|LLC|L L C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PLLC|PC|THE|JV|JOINT VENTURE|GROUP|HOLDINGS|SERVICES|SOLUTIONS|TECHNOLOGIES|TECHNOLOGY|INTERNATIONAL|FEDERAL|US|USA|AND|DOING BUSINESS AS|DBA)\b'
def norm(s): s=re.sub(r'[^A-Z0-9 ]',' ',(s or '').upper()); s=re.sub(STOP,' ',s); return re.sub(r'\s+',' ',s).strip()
def toks(s): s=re.sub(r'[^A-Z0-9 ]',' ',(s or '').upper()); s=re.sub(STOP2,' ',s); return set(s.split())
def call(body):
  req=urllib.request.Request('https://api.blitz-api.ai/v2/search/companies',json.dumps(body).encode(),{'Content-Type':'application/json','x-api-key':KEY})
  for a in range(4):
    try: return json.load(urllib.request.urlopen(req,timeout=60))
    except Exception as e: err=e; time.sleep(2*(a+1))
  return {'error':str(err)}
calls=0
def one(x):
  global calls
  nm=x['Recipient Name']
  if nm in cache: m,res=cache[nm]; return x,m,res
  n=norm(nm)
  if not n: return x,None,[]
  d=call({'company':{'name':{'include':[n]},'hq':{'country_code':['US']}},'max_results':5}); calls+=1
  res=d.get('results') or []
  best=next((c for c in res if norm(c.get('name'))==n),None) or next((c for c in res if toks(nm) and toks(c.get('name'))==toks(nm)),None)
  return x,best,res
out=[]
with cf.ThreadPoolExecutor(16) as ex:
  for x,m,res in ex.map(one,recs): out.append({'award':x,'match':m,'candidates':res})
json.dump(out,open(S+'/blitz_matches_12mo.json','w'))
import collections
m=[o for o in out if o['match']]
print('recipients',len(out),'matched',len(m),'new blitz calls',calls,'records',sum(len(o['candidates']) for o in out))
print(collections.Counter(o['match'].get('revenue_range') for o in m))
