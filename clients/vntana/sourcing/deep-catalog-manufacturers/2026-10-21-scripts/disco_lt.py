import json,os,concurrent.futures as cf
from dl_lib import q,NEG_SUB
IMG=["image coming soon","image not available","no image available","photo coming soon","picture coming soon","image unavailable","no photo available","image to come","coming soon image"]
CAT=["part number","catalog number","add to cart","request a quote","distributor portal","download cad","cad models","configure your","product configurator","view catalog","online catalog"]
GEO={"US":["US"],"CA":["CA"],"UKI_AUNZ":["GB","IE","AU","NZ"],"EU_W":["DE","FR","IT","ES","NL","BE","AT","CH"],"EU_N":["SE","DK","NO","FI","PL"]}
ALLCAT=["MANUFACTURING","ENERGY","AGRICULTURE_AND_NATURAL_RESOURCES","CONSTRUCTION","COMPUTER_HARDWARE_AND_SEMICONDUCTORS","BUSINESS_PRODUCTS_AND_SERVICES","AUTOMOTIVE","MINING_AND_METALS","RENEWABLE_ENERGY","ENGINEERING","DEFENSE_AND_AEROSPACE","CONSUMER_PRODUCTS"]
NEG={"MANUFACTURING":["MANUFACTURING/"+x for x in NEG_SUB],"AUTOMOTIVE":["AUTOMOTIVE/"+x for x in("CAR_DEALERSHIP","AUTO_REPAIR_SHOP","AUTO_BODY_SHOP","TIRE_SHOP","AUTO_DETAILING","TOWING")]}
KEEP=("domain","name","address","social_urls","description","keywords","industry_groups","sub_industry","employees","revenue_range","business_model","score")
def run(item):
    kind,cat,g,cs=item; fn=f"disco/{kind}__{cat}__{g}.jsonl"
    if os.path.exists(fn+".done"): return fn,-1
    ph=IMG if kind=="img" else CAT
    p={"phrase_match":ph,"category":[cat],"country":cs,"employee_range":"51,"}
    if NEG.get(cat): p["negate_sub_industry"]=NEG[cat]
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
    items=[("img",c,g,cs) for c in ALLCAT for g,cs in GEO.items()]+[("cat",c,g,cs) for c in ("MANUFACTURING","ENERGY","COMPUTER_HARDWARE_AND_SEMICONDUCTORS","ENGINEERING") for g,cs in GEO.items()]
    tot=0
    with cf.ThreadPoolExecutor(4) as ex:
        for fn,n in ex.map(run,items): tot+=max(n,0); print(fn,n,tot,flush=True)
    print("DONE",tot,flush=True)
