import json,os,sys,urllib.request,datetime,time,re
S=sys.argv[1]; K=os.environ['EXA_API_KEY']
def exa(path,body):
  req=urllib.request.Request('https://api.exa.ai'+path,json.dumps(body).encode(),{'x-api-key':K,'Content-Type':'application/json'})
  for a in range(3):
    try: return json.load(urllib.request.urlopen(req,timeout=120))
    except Exception as e: err=e; time.sleep(3)
  return {'error':str(err)}
MON={9:'Sept.',10:'Oct.',8:'Aug.'}
urls={}; cost=0
d=datetime.date(2026,8,31)
while d<=datetime.date(2026,10,29):
  if d.weekday()<5:
    title=f"Contracts for {MON[d.month]} {d.day}, 2026"
    r=exa('/search',{"query":title,"includeDomains":["war.gov","defense.gov"],"numResults":5})
    cost+=r.get('costDollars',{}).get('total',0) if isinstance(r.get('costDollars'),dict) else 0
    for x in r.get('results',[]):
      if (x.get('title') or '').strip().lower()==title.lower(): urls[d.isoformat()]=x['url']; break
  d+=datetime.timedelta(days=1)
print('found',len(urls),'cost',round(cost,3),file=sys.stderr)
pages={}
L=list(urls.items())
for i in range(0,len(L),10):
  chunk=L[i:i+10]
  r=exa('/contents',{"urls":[u for _,u in chunk],"text":True})
  cost+=r.get('costDollars',{}).get('total',0) if isinstance(r.get('costDollars'),dict) else 0
  bu={x['url']:x.get('text','') for x in r.get('results',[])}
  for dte,u in chunk: pages[dte]={'url':u,'text':bu.get(u,'')}
json.dump(pages,open(S+'/dod_pages.json','w'))
print('pages',len(pages),'with text',sum(1 for p in pages.values() if len(p['text'])>500),'total cost',round(cost,3))
