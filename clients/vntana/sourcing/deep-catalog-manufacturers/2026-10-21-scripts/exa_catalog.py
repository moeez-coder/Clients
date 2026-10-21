import json,sys,concurrent.futures as cf
from exa_clients import exa
# input: json list of {key,domain,name}; output: exa_dealers.json {key:{...}}
items=json.load(open(sys.argv[1])); out={}
Q="authorized dealers, dealer locator, find a dealer, distributor network, number of dealer locations"
def job(it):
    r=exa({"query":f"{it['name']} online product catalog number of products SKUs part numbers image coming soon distributor portal","includeDomains":[it['domain']],"numResults":5,
           "contents":{"highlights":{"query":"how many products, SKUs, part numbers or variants are in this manufacturer's catalog; online catalog, distributor or dealer portal, configurator; missing or coming-soon product images","numSentences":3,"highlightsPerUrl":2}}})
    return it['key'],{"domain":it['domain'],"err":r.get('error'),"cost":(r.get('costDollars') or {}).get('total',0),
        "pages":[{"url":x.get('url'),"title":(x.get('title') or '')[:100],"hl":' '.join(x.get('highlights') or [])[:700]} for x in r.get('results',[])]}
with cf.ThreadPoolExecutor(8) as ex:
    for i,(k,v) in enumerate(ex.map(job,items)):
        out[k]=v
        if i%250==0: print(i,flush=True)
json.dump(out,open(sys.argv[2],'w'))
print('done',len(out),'with pages',sum(1 for v in out.values() if v['pages']),'cost',round(sum(v['cost'] for v in out.values()),2))
