import json,concurrent.futures as cf
from exa_clients import exa
Q={
"const":["compact construction equipment manufacturer sold through an independent dealer network","skid steer and compact track loader attachments manufacturer authorized dealers","agricultural equipment manufacturer with authorized dealers across North America","tractor and implement manufacturer find a dealer","mining and quarry equipment manufacturer distributors and dealers","forestry and timber equipment manufacturer dealer network","paving and compaction equipment manufacturer dealers","concrete equipment manufacturer authorized distributors","lawn and turf equipment manufacturer dealer locator"],
"trailer":["trailer manufacturer with an authorized dealer network find a dealer","dump trailer and flatbed trailer manufacturer dealers","cargo and enclosed trailer manufacturer dealer locator","horse and livestock trailer manufacturer dealers","truck body and upfit manufacturer through truck equipment distributors","dump body hoist and snow plow manufacturer distributors","utility body and service body manufacturer dealer network","tow truck and wrecker manufacturer distributors","refuse truck body manufacturer dealers"],
"matl":["forklift and lift truck manufacturer authorized dealers","pallet jack and material handling equipment manufacturer dealer network","conveyor and warehouse equipment manufacturer through distributors","hoist crane and rigging equipment manufacturer distributors","aerial work platform and scissor lift manufacturer dealers","telehandler manufacturer dealer network","dock and loading equipment manufacturer distributors"],
"power":["generator manufacturer authorized dealers and distributors","outdoor power equipment manufacturer dealer locator","pressure washer and air compressor manufacturer authorized dealers","welding equipment manufacturer distributors","light tower and portable power manufacturer dealers","engine manufacturer distributor network","electric motors and drives manufacturer authorized distributors","battery and charger manufacturer for industrial equipment dealers"],
"hvac":["HVAC equipment manufacturer sold through independent distributors and contractors","furnace and air conditioner manufacturer dealer locator","boiler and hydronic heating manufacturer dealer network","commercial refrigeration equipment manufacturer authorized dealers","water heater manufacturer distributors and dealers","ventilation and air handling manufacturer representatives network"],
"flow":["hydraulic components manufacturer through distributors network","pump manufacturer independent distributors and manufacturers representatives","valve manufacturer authorized distributors rep network","pneumatic and fluid power manufacturer distributor locator","hose fittings and couplings manufacturer authorized distributors","filtration equipment manufacturer distributor network"],
"specialty":["fire apparatus manufacturer dealers","ambulance and specialty vehicle manufacturer dealer network","school bus and commercial bus manufacturer dealers","electric utility vehicle and golf cart manufacturer dealers","RV and towable manufacturer dealer network","street sweeper and vacuum truck manufacturer dealers","cranes and truck-mounted equipment manufacturer dealer network"],
}
def job(a):
    v,q,cat=a
    b={"query":q,"numResults":100,"type":"auto"}
    if cat: b["category"]="company"
    r=exa(b)
    return {"vert":v,"query":q,"cat":cat,"err":r.get("error"),"cost":(r.get("costDollars") or {}).get("total",0),"results":[{"url":x.get("url"),"title":x.get("title")} for x in r.get("results",[])]}
args=[(v,q,c) for v,qs in Q.items() for q in qs for c in (True,False)]
with cf.ThreadPoolExecutor(6) as ex: out=list(ex.map(job,args))
json.dump(out,open("exa_disc.json","w"))
print(len(out),"queries; results",sum(len(o["results"]) for o in out),"cost",round(sum(o["cost"] for o in out),2),"errors",sum(1 for o in out if o["err"]))
