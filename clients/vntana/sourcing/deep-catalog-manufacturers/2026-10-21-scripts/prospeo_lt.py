import json,os,concurrent.futures as cf
from prospeo_lib import post,BANDS,LOC
NAICS={"pumps_valves_fluid":["333911","333914","332911","332912","332919","333995","333996","333912"],
"fasteners_hardware":["332722","332721","332510","332613","332618","332439"],
"tools":["333991","332216","333515","333517"],
"power_transmission":["333612","333613","332991","333999"],
"electrical_automation":["335931","335313","335314","335311","335312","334513","335999","335991"]}
IND=["Machinery Manufacturing","Industrial Machinery Manufacturing","Fabricated Metal Products","Electrical Equipment Manufacturing","Appliances, Electrical, and Electronics Manufacturing","Metal Valve, Ball, and Roller Manufacturing","Engines and Power Transmission Equipment Manufacturing","Turned Products and Fastener Manufacturing","Spring and Wire Product Manufacturing","Automation Machinery Manufacturing","Metalworking Machinery Manufacturing","Construction Hardware Manufacturing","HVAC and Refrigeration Equipment Manufacturing","Motor Vehicle Parts Manufacturing","Plastics Manufacturing","Rubber Products Manufacturing"]
KW=["online catalog","product catalog","catalogue","part numbers","catalog number","SKU","SKUs","stock items","standard parts","configurator","thousands of products"]
def slices():
    for v,codes in NAICS.items():
        for b in BANDS: yield f"naics_{v}__{b}",{"company_naics":{"include":codes},"company_headcount_range":[b],"company_location_search":{"include":LOC}}
    for b in BANDS: yield f"kwcatalog__{b}",{"company_keywords":{"include":KW},"company_industry":{"include":IND},"company_headcount_range":[b],"company_location_search":{"include":LOC}}
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
                c=r["company"]
                out.write(json.dumps({k:c.get(k) for k in("company_id","name","domain","website","description","description_ai","type","industry","employee_count","employee_range","location","sic_codes","naics_codes","keywords","revenue_range","revenue_range_printed","linkedin_url","founded","technology")})+"\n"); n+=1
            p+=1
    open(fn+".done","w").write(str(n)); return sid,n
if __name__=="__main__":
    items=list(slices()); print(len(items),"slices",flush=True); tot=0
    with cf.ThreadPoolExecutor(6) as ex:
        for i,(sid,n) in enumerate(ex.map(run,items)):
            tot+=max(n,0); print(i,sid,n,tot,flush=True)
    print("DONE",tot,flush=True)
