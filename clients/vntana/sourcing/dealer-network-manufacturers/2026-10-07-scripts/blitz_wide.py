import json,os,sys,time,urllib.request,concurrent.futures as cf,itertools
KEY=os.environ['BLITZ_API_KEY']
EMP=["51-200","201-500","501-1000","1001-5000","5001-10000","10001+"]
CG={"US":["US"],"CA":["CA"],"UKI_AUNZ":["GB","IE","AU","NZ"],"EU_W":["DE","FR","IT","ES","NL","BE","AT","CH"],"EU_N":["SE","DK","NO","FI","PL"],"ROW":["MX","BR","ZA","IN","JP","KR","CN","TR"]}
I_CONST=["Agriculture; Construction; Mining Machinery Manufacturing"]
I_MACH=["Industrial Machinery Manufacturing","Machinery Manufacturing","Machinery","Commercial and Service Industry Machinery Manufacturing","Automation Machinery Manufacturing","Metalworking Machinery Manufacturing"]
I_POWER=["Electrical Equipment Manufacturing","Engines and Power Transmission Equipment Manufacturing","Electric Power Transmission; Control; and Distribution","Renewable Energy Equipment Manufacturing","Household Appliance Manufacturing"]
I_HVAC=["HVAC and Refrigeration Equipment Manufacturing"]
I_FLOW=["Metal Valve; Ball; and Roller Manufacturing"]
I_VEH=["Motor Vehicle Manufacturing","Motor Vehicle Parts Manufacturing","Transportation Equipment Manufacturing","Railroad Equipment Manufacturing","Alternative Fuel Vehicle Manufacturing"]
I_FAB=["Fabricated Metal Products","Appliances; Electrical; and Electronics Manufacturing","Building Materials","Construction Hardware Manufacturing"]
K_VEH=["trailer","trailers","truck body","truck bodies","dump body","upfit","service body","flatbed","hitch","towing","refuse truck","vacuum truck","fire apparatus","chassis","snowplow","truck equipment","hoist","liftgate","lift gate","tank truck","horse trailer","cargo trailer","utility trailer","lowboy","bus"]
K_POWER=["generator","generators","power equipment","outdoor power","mower","pressure washer","portable power","standby power","engine","engines","compressor","welder","light tower","pump"]
K_HVAC=["HVAC","furnace","boiler","air conditioning","heat pump","water heater","refrigeration","hydronic","heating"]
K_FLOW=["pump","pumps","valve","valves","hydraulic","hydraulics","pneumatic","fluid power","flow control","actuator","cylinder","filtration","hose","fittings"]
K_DEALER=["dealer network","authorized dealers","authorised dealers","dealer locator","find a dealer","independent dealers","network of dealers","dealers and distributors","distributor network","authorized distributors","manufacturers representatives","sales reps","dealer"]
G1=[("const",I_CONST,None),("mach",I_MACH,None),("power",I_POWER,None),("hvac",I_HVAC,None),("flow",I_FLOW,None)]
G2=[("veh_kw",I_VEH+I_MACH+I_CONST+["Fabricated Metal Products"],K_VEH),("power_kw",I_MACH+I_FAB+["Motor Vehicle Parts Manufacturing"],K_POWER),("hvac_kw",I_MACH+I_FAB+I_POWER,K_HVAC),("flow_kw",I_MACH+I_FAB+I_POWER+I_VEH,K_FLOW)]
G3=[("dealer_kw",I_CONST+I_MACH+I_POWER+I_HVAC+I_FLOW+I_VEH+I_FAB,K_DEALER)]
def slices():
    for vert,inds,kws in G1+G2+G3:
        for e in EMP:
            for cg,cs in CG.items():
                yield f"{vert}__{e}__{cg}",{"company":{"industry":{"include":inds},"employee_range":[e],"hq":{"country_code":cs},**({"keywords":{"include":kws}} if kws else {})},"max_results":25}
def call(body):
    for a in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request("https://api.blitz-api.ai/v2/search/companies",data=json.dumps(body).encode(),headers={"x-api-key":KEY,"Content-Type":"application/json"}),timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504): time.sleep(2**a); continue
            return {"error":e.code,"msg":e.read()[:200].decode('utf8','ignore'),"results":[],"cursor":None}
        except Exception: time.sleep(2**a)
    return {"error":"retries","results":[],"cursor":None}
def run(item):
    sid,body=item; fn=f"blitz/{sid}.jsonl"
    if os.path.exists(fn+".done"): return sid,-1
    n=0; cur=None
    with open(fn,"w") as f:
        for p in range(400):
            b=dict(body); 
            if cur: b["cursor"]=cur
            d=call(b)
            if d.get("error"): f.write(json.dumps({"_error":d})+"\n"); break
            if p==0: f.write(json.dumps({"_meta":{"total_results":d.get("total_results"),"body":body}})+"\n")
            for r in d["results"]: f.write(json.dumps({k:r.get(k) for k in ("linkedin_url","name","domain","website","industry","type","size","employees_on_linkedin","followers","founded_year","hq","about","specialties")})+"\n"); n+=1
            cur=d.get("cursor")
            if not cur: break
    open(fn+".done","w").write(str(n))
    return sid,n
if __name__=="__main__":
    items=list(slices()); print(len(items),"slices",flush=True)
    tot=0
    with cf.ThreadPoolExecutor(10) as ex:
        for i,(sid,n) in enumerate(ex.map(run,items)):
            tot+=max(n,0)
            if i%20==0: print(i,sid,n,tot,flush=True)
    print("DONE rows",tot,flush=True)
