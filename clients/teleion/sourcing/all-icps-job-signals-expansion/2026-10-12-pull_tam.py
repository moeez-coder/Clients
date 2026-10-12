import json,csv,re,sys,time,concurrent.futures as cf
from tam import call
FS=["Banking","Financial Services"]
SZ_FS=["201-500","501-1000","1001-5000"]
SZ_ENT=["1001-5000","5001-10000","10001+"]
Q={
 'P3':dict(cfg='d17cad6a-b9ee-4b07-91d5-8273c0e3dc6a',titles=["BSA","AML","anti-money laundering","money laundering","KYC","know your customer","OFAC","sanctions","financial crimes","financial crime","bank secrecy"],ind=FS,size=SZ_FS,min=2),
 'P5':dict(cfg='b3dd9cc8-7eab-4774-96d0-f5e2dc03aed3',titles=["model risk","model validation","AI governance","responsible AI","AI risk","artificial intelligence risk","AI model risk"],ind=FS,size=SZ_FS,min=1),
 'P2':dict(cfg='41e54db9-f4f8-47b5-b976-72a2ac5ad09c',titles=["BaaS","banking as a service","embedded finance","embedded banking","fintech partnerships","fintech program","bank partnerships","fintech relationship"],ind=FS,size=SZ_FS,min=1),
 'M1':dict(cfg='f3e11468-68f8-4555-9c9f-5dd919d87d9e',titles=["payments operations","payment operations","treasury operations","treasury analyst","card operations","payments analyst","payment analyst","settlement analyst","reconciliation analyst"],ind=FS,size=SZ_FS,min=2),
 'M2':dict(cfg='1a436fdd-d5f2-426b-826f-781b2087e8ac',titles=["marketing compliance","content review","marketing legal","advertising compliance","marketing review","compliance review"],ind=FS,size=SZ_FS,min=1),
 'E1':dict(cfg='91734597-7a99-4eca-b725-68428e2bc9c1',titles=["AI governance","responsible AI","AI risk","AI compliance","AI policy","AI ethics","AI assurance"],ind=[],size=SZ_ENT,min=1),
 'E2':dict(cfg='fc9333cd-94d4-4296-b494-4c28df2573da',titles=["post-merger integration","merger integration","M&A integration","integration management office","M&A"],ind=[],size=SZ_ENT,min=1),
 'E3':dict(cfg='19d6f7c2-bfe4-406d-914c-f119ee83ef4b',titles=["vendor management","contingent workforce","vendor governance","supplier management","managed services program","contract labor"],ind=[],size=SZ_ENT,min=2),
}
def body(q,cursor=None):
    b={"job":{"title":{"include":q['titles']},"date_posted":{"last_days":90},"min_per_company":q['min']},"company":{"size":{"include":q['size']}},"max_results":50}
    if q['ind']: b["company"]["industry"]={"include":q['ind']}
    if cursor: b['cursor']=cursor
    return b
import os
out=json.load(open('tam_raw.json')) if os.path.exists('tam_raw.json') else {}
for code,q in Q.items():
    if code in out: continue
    cur=None;n=0;rows=[]
    for p in range(60):
        r=call(body(q,cur))
        if 'http' in r: print(code,'ERR',r); break
        rows+=r['results'];cur=r.get('cursor')
        if not cur: break
    out[code]=rows;print(code,len(rows),flush=True)
    json.dump(out,open('tam_raw.json','w'))
