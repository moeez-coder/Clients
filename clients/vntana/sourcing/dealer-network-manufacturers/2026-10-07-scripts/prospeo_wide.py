import json,os,sys,concurrent.futures as cf
from prospeo_lib import *
IND=["Machinery Manufacturing","Industrial Machinery Manufacturing","Motor Vehicle Manufacturing","Motor Vehicle Parts Manufacturing","Transportation Equipment Manufacturing","HVAC and Refrigeration Equipment Manufacturing","Electrical Equipment Manufacturing","Engines and Power Transmission Equipment Manufacturing","Agriculture, Construction, Mining Machinery Manufacturing","Commercial and Service Industry Machinery Manufacturing","Metal Valve, Ball, and Roller Manufacturing","Fabricated Metal Products","Appliances, Electrical, and Electronics Manufacturing","Automation Machinery Manufacturing","Railroad Equipment Manufacturing","Renewable Energy Equipment Manufacturing","Household Appliance Manufacturing"]
KW=["dealer network","authorized dealers","authorised dealers","dealer locator","find a dealer","independent dealers","network of dealers","dealers and distributors","distributor network","authorized distributors","manufacturers representatives","rep network"]
def slices():
    for v in VERT:
        for b in BANDS: yield f"naics_{v}__{b}",filt(v,b)
    for b in BANDS:
        yield f"kwdealer__{b}",{"company_keywords":{"include":KW},"company_industry":{"include":IND},"company_headcount_range":[b],"company_location_search":{"include":LOC}}
def run(item):
    sid,f=item; fn=f"prospeo/{sid}.jsonl"
    if os.path.exists(fn+".done"): return sid,-1
    n=0
    with open(fn,"w") as out:
        p=1;tp=1
        while p<=tp and p<=1000:
            d=post("search-company",{"page":p,"filters":f})
            if d.get("error"):
                if d.get("error_code")!="NO_RESULTS": out.write(json.dumps({"_error":d})+"\n")
                break
            tp=d["pagination"]["total_page"]
            if p==1: out.write(json.dumps({"_meta":{"total_count":d["pagination"]["total_count"],"filters":f}})+"\n")
            for r in d["results"]:
                c=r["company"]; 
                out.write(json.dumps({k:c.get(k) for k in ("company_id","name","domain","website","description","description_ai","type","industry","employee_count","employee_range","location","sic_codes","naics_codes","keywords","revenue_range","revenue_range_printed","linkedin_url","founded","technology","job_postings")})+"\n"); n+=1
            p+=1
    open(fn+".done","w").write(str(n)); return sid,n
if __name__=="__main__":
    items=list(slices()); print(len(items),"slices",flush=True); tot=0
    with cf.ThreadPoolExecutor(6) as ex:
        for i,(sid,n) in enumerate(ex.map(run,items)):
            tot+=max(n,0); print(i,sid,n,tot,flush=True)
    print("DONE",tot,flush=True)
