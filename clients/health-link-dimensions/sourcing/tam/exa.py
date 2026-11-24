import json,os,urllib.request,re
def search(q,n=100):
    body={"query":q,"category":"company","numResults":n,"type":"auto"}
    r=urllib.request.Request("https://api.exa.ai/search",data=json.dumps(body).encode(),headers={"x-api-key":os.environ["EXA_API_KEY"],"Content-Type":"application/json"})
    try: return body,json.load(urllib.request.urlopen(r,timeout=120))
    except urllib.error.HTTPError as e: return body,{"error":e.code,"body":e.read().decode()[:400]}
Q=["US healthcare advertising agency for pharmaceutical brands",
   "pharma media agency programmatic HCP targeting United States",
   "independent health and wellness communications agency serving biotech and pharma clients",
   "medical communications agency United States pharmaceutical marketing",
   "healthcare marketing data and analytics agency for life sciences brands",
   "omnichannel HCP engagement agency for medical device and pharma companies"]
def dom(u):
    m=re.match(r"https?://(?:www\.)?([^/]+)",u or ""); return m.group(1).lower() if m else None
out={"queries":[],"cost":0}
for q in Q:
    b,r=search(q)
    res=r.get("results",[])
    out["queries"].append({"body":b,"n":len(res),"cost":r.get("costDollars"),"results":[{"domain":dom(x.get("url")),"title":x.get("title"),"url":x.get("url")} for x in res],"err":r.get("body")})
    c=(r.get("costDollars") or {}).get("total",0); out["cost"]+=c
    print(len(res),c,q, r.get("body",""))
json.dump(out,open("exa.json","w"),indent=1)
doms={x["domain"] for q in out["queries"] for x in q["results"] if x["domain"]}
dl={x["domain"] for x in json.load(open("dl_discover.json"))["response"]}
print("exa unique domains",len(doms),"in DiscoLike 600:",len(doms&dl),"total cost",out["cost"])
