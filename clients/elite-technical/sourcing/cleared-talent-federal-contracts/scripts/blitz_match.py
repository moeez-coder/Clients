import json,re,os,sys,urllib.request,time,concurrent.futures as cf
S=sys.argv[1]
recs=json.load(open(S+'/usas_recipients.json'))
KEY=os.environ['BLITZ_API_KEY']
STOP=r'\b(INC|INCORPORATED|LLC|L\.L\.C|CORP|CORPORATION|CO|COMPANY|LTD|LP|LLP|PLLC|PC|THE|JV|JOINT VENTURE|GROUP|HOLDINGS)\b'
def norm(s): s=re.sub(r'[^A-Z0-9 ]',' ',(s or '').upper()); s=re.sub(STOP,' ',s); return re.sub(r'\s+',' ',s).strip()
def call(body):
  req=urllib.request.Request('https://api.blitz-api.ai/v2/search/companies',json.dumps(body).encode(),{'Content-Type':'application/json','x-api-key':KEY})
  for a in range(4):
    try: return json.load(urllib.request.urlopen(req,timeout=60))
    except Exception as e: err=e; time.sleep(2*(a+1))
  return {'error':str(err)}
def one(x):
  n=norm(x['Recipient Name'])
  if not n: return x,None,[]
  d=call({'company':{'name':{'include':[n]},'hq':{'country_code':['US']}},'max_results':5})
  res=d.get('results') or []
  best=None
  for c in res:
    if norm(c.get('name'))==n: best=c; break
  return x,best,res
out=[]
with cf.ThreadPoolExecutor(8) as ex:
  for x,best,res in ex.map(one,recs):
    out.append({'award':x,'match':best,'candidates':res})
json.dump(out,open(S+'/blitz_matches.json','w'))
m=[o for o in out if o['match']]
print('matched',len(m),'of',len(out),'records returned',sum(len(o['candidates']) for o in out))
if m: print(json.dumps(m[0]['match'],indent=0)[:1500])
