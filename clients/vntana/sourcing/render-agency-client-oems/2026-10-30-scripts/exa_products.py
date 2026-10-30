import json,concurrent.futures as cf
from exa_clients import exa
A=json.load(open('accounts.json'))
HL={"highlights":{"query":"the name of a new product, model or product line this company launched or announced, and what type of product it is","numSentences":3,"highlightsPerUrl":2}}
def job(i):
    a=A[i];nm=a['likely_company'] if a['likely_company'] not in('','-') else a['client_name']
    r=exa({"query":f"{nm} launches new product {a['what_they_make'][:60]}","numResults":6,"startPublishedDate":"2025-10-01T00:00:00.000Z","contents":HL})
    res=r.get('results',[]);cost=(r.get('costDollars') or {}).get('total',0);dated=True
    if len(res)<2:
        r2=exa({"query":f"{nm} flagship product range {a['what_they_make'][:60]}","numResults":5,"contents":HL});res=res+r2.get('results',[]);cost+=(r2.get('costDollars') or {}).get('total',0);dated=False
    return i,{"company":nm,"dated":dated,"cost":cost,"pages":[{"url":x.get('url'),"title":(x.get('title') or '')[:120],"date":x.get('publishedDate'),"hl":' '.join(x.get('highlights') or [])[:600]} for x in res]}
out={}
with cf.ThreadPoolExecutor(8) as ex:
    for i,v in ex.map(job,range(len(A))): out[i]=v
json.dump(out,open('exa_products.json','w'))
print('done',len(out),'with pages',sum(1 for v in out.values() if v['pages']),'cost',round(sum(v['cost'] for v in out.values()),2))
