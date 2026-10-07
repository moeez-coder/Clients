import json,os,concurrent.futures as cf
from dl_lib import *
GEO={"US":["US"],"CA":["CA"],"UKI_AUNZ":["GB","IE","AU","NZ"],"EU_W":["DE","FR","IT","ES","NL","BE","AT","CH"],"EU_N":["SE","DK","NO","FI","PL"]}
CATS={"MANUFACTURING":["MANUFACTURING/"+x for x in NEG_SUB],
      "AUTOMOTIVE":["AUTOMOTIVE/"+x for x in ("CAR_DEALERSHIP","AUTO_REPAIR_SHOP","AUTO_BODY_SHOP","TIRE_SHOP","AUTO_DETAILING","TOWING")],
      "ENERGY":None,"AGRICULTURE_AND_NATURAL_RESOURCES":None,"MINING_AND_METALS":None,"CONSTRUCTION":None}
KEEP=("domain","name","address","social_urls","description","keywords","industry_groups","sub_industry","employees","revenue_range","business_model","score")
def run(item):
    cat,neg,g,cs=item; fn=f"disco/{cat}__{g}.jsonl"
    if os.path.exists(fn+".done"): return fn,-1
    p={"phrase_match":PH,"category":[cat],"country":cs,"employee_range":"51,"}
    if neg: p["negate_sub_industry"]=neg
    n=0
    with open(fn,"w") as f:
        off=0
        while True:
            d=q("discover",{**p,"max_records":1000,"offset":off})
            if isinstance(d,dict): f.write(json.dumps({"_error":d})+"\n"); break
            for r in d: f.write(json.dumps({k:r.get(k) for k in KEEP})+"\n"); n+=1
            if len(d)<1000 or off>=9000: break
            off+=1000
    open(fn+".done","w").write(str(n)); return fn,n
if __name__=="__main__":
    items=[(c,n,g,cs) for c,n in CATS.items() for g,cs in GEO.items()]
    tot=0
    with cf.ThreadPoolExecutor(4) as ex:
        for fn,n in ex.map(run,items): tot+=max(n,0); print(fn,n,tot,flush=True)
    print("DONE",tot,flush=True)
