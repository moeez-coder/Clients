from exa_clients import exa
import json
Q=["3D product rendering agency that turns manufacturer CAD files into photorealistic marketing renders",
"CGI studio creating product visualization and animations from engineering CAD data for industrial equipment manufacturers",
"agency that converts SolidWorks and STEP files into photoreal product images for ecommerce and catalogs",
"technical animation studio for machinery and industrial products marketing",
"CGI replacing product photography for manufacturers, renders from CAD",
"3D configurator and product visualization agency for B2B manufacturers",
"automotive CGI production studio renders from CAD data",
"industrial product marketing agency 3D animation and rendering"]
out=[]
for q in Q:
    for cat in ("company",None):
        b={"query":q,"numResults":100,"type":"auto"}
        if cat: b["category"]=cat
        r=exa(b); out.append({"query":q,"category":cat,"results":[{k:x.get(k) for k in ('url','title')} for x in r.get('results',[])],"error":r.get('error'),"cost":(r.get('costDollars') or {}).get('total')})
        print(q[:50],cat,len(out[-1]['results']),r.get('error'),r.get('msg','')[:100])
json.dump(out,open('exa_discover.json','w'))
