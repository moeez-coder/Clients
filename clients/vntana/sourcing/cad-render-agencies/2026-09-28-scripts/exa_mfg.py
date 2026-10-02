import csv,json,concurrent.futures as cf
from exa_clients import exa
P='/home/user/Clients/clients/vntana/sourcing/cad-render-agencies/2026-09-28-agency-clients.csv'
rows=[r for r in csv.DictReader(open(P)) if r['physical_product_maker']!='no']
def job(r):
    name=r['likely_company'] if r['likely_company'] not in ('unknown','-') else r['client_name']
    res=exa({"query":f"{name} company — what it manufactures","category":"company","numResults":2,
             "contents":{"highlights":{"query":"what products does this company design and manufacture","numSentences":3,"highlightsPerUrl":2}}})
    ev=[{"url":x.get('url'),"title":x.get('title'),"hl":' '.join(x.get('highlights') or [])[:600]} for x in res.get('results',[])]
    return r['client_name'],{"query_name":name,"evidence":ev,"err":res.get('error'),"cost":(res.get('costDollars') or {}).get('total',0)}
out={}
with cf.ThreadPoolExecutor(8) as ex:
    for i,(k,v) in enumerate(ex.map(job,rows)):
        out[k]=v
        if i%500==0: print(i,flush=True)
json.dump(out,open('exa_mfg.json','w'))
print('done',len(out),'with evidence',sum(1 for v in out.values() if v['evidence']),'errors',sum(1 for v in out.values() if v['err']),'cost',round(sum(v['cost'] for v in out.values()),2))
