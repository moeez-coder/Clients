import json,os,sys,time,urllib.request,concurrent.futures as cf
KEY=os.environ['BLITZ_API_KEY']
EMP=["51-200","201-500","501-1000","1001-5000","5001-10000","10001+"]
CG={"US":["US"],"CA":["CA"],"UKI_AUNZ":["GB","IE","AU","NZ"],"EU_W":["DE","FR","IT","ES","NL","BE","AT","CH"],"EU_N":["SE","DK","NO","FI","PL","CZ"],"ROW":["MX","BR","ZA","IN","JP","KR","CN","TR","TW"]}
I_MFG=["Industrial Machinery Manufacturing","Machinery Manufacturing","Machinery","Fabricated Metal Products","Electrical Equipment Manufacturing","Electrical and Electronic Manufacturing","Appliances; Electrical; and Electronics Manufacturing","Metal Valve; Ball; and Roller Manufacturing","Engines and Power Transmission Equipment Manufacturing","Turned Products and Fastener Manufacturing","Spring and Wire Product Manufacturing","Automation Machinery Manufacturing","Metalworking Machinery Manufacturing","Construction Hardware Manufacturing","Commercial and Service Industry Machinery Manufacturing","Abrasives and Nonmetallic Minerals Manufacturing","Renewable Energy Equipment Manufacturing","Electric Lighting Equipment Manufacturing","Building Materials","Plastics Manufacturing","Rubber Products Manufacturing","Motor Vehicle Parts Manufacturing","Primary Metal Manufacturing"]
K={"flow":["pump","pumps","valve","valves","hydraulic","hydraulics","pneumatic","fluid power","flow control","actuator","actuators","filtration","hose","hoses","fittings","couplings","manifold","regulators","seals"],
"fasteners":["fastener","fasteners","bolts","screws","nuts","washers","rivets","anchors","springs","clamps","pins","standoffs","inserts","o-rings","gaskets","hardware"],
"electrical":["connector","connectors","relay","relays","sensors","switches","enclosures","terminal blocks","contactors","circuit breakers","fuses","cable assemblies","wire and cable","motors","drives","automation components","controls"],
"tools":["hand tools","power tools","cutting tools","drill bits","saw blades","abrasives","tooling","workholding","measuring tools","industrial tools","wrenches","pliers"],
"power_transmission":["bearings","gears","gearboxes","chains","sprockets","belts","clutches","brakes","shafts","power transmission","motion control","linear motion","couplings"],
"catalog":["online catalog","product catalog","catalogue","part numbers","part number","catalog number","SKU","SKUs","stock items","standard parts","catalog items","thousands of products","tens of thousands","10,000 products","configurator"]}
def slices():
    for v,kw in K.items():
        for e in EMP:
            for cg,cs in CG.items():
                yield f"{v}__{e}__{cg}",{"company":{"industry":{"include":I_MFG},"employee_range":[e],"hq":{"country_code":cs},"keywords":{"include":kw}},"max_results":25}
def call(body):
    for a in range(6):
        try: return json.load(urllib.request.urlopen(urllib.request.Request("https://api.blitz-api.ai/v2/search/companies",data=json.dumps(body).encode(),headers={"x-api-key":KEY,"Content-Type":"application/json"}),timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in(429,500,502,503,504): time.sleep(2**a); continue
            return {"error":e.code,"msg":e.read()[:200].decode('utf8','ignore'),"results":[],"cursor":None}
        except Exception: time.sleep(2**a)
    return {"error":"retries","results":[],"cursor":None}
def run(item):
    sid,body=item; fn=f"blitz/{sid}.jsonl"
    if os.path.exists(fn+".done"): return sid,-1
    n=0;cur=None
    with open(fn,"w") as f:
        for p in range(400):
            b=dict(body)
            if cur: b["cursor"]=cur
            d=call(b)
            if d.get("error"): f.write(json.dumps({"_error":d})+"\n"); break
            if p==0: f.write(json.dumps({"_meta":{"total_results":d.get("total_results"),"body":body}})+"\n")
            for r in d["results"]: f.write(json.dumps({k:r.get(k) for k in("linkedin_url","name","domain","website","industry","type","size","employees_on_linkedin","followers","founded_year","hq","about","specialties")})+"\n"); n+=1
            cur=d.get("cursor")
            if not cur: break
    open(fn+".done","w").write(str(n)); return sid,n
if __name__=="__main__":
    items=list(slices()); print(len(items),"slices",flush=True); tot=0
    with cf.ThreadPoolExecutor(10) as ex:
        for i,(sid,n) in enumerate(ex.map(run,items)):
            tot+=max(n,0)
            if i%20==0: print(i,sid,n,tot,flush=True)
    print("DONE rows",tot,flush=True)
