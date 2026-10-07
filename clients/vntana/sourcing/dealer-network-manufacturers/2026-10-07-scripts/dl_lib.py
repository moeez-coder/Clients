import json,os,time,urllib.request,urllib.parse
KEY=os.environ['DISCOLIKE_API_KEY']
PH=["find a dealer","dealer locator","become a dealer","authorized dealers","authorised dealers","dealer network","dealer portal","dealer login","find a distributor","distributor locator","where to buy","find a rep","become a distributor","become an authorized dealer"]
NEG_SUB=["MACHINE_SHOP","METAL_FABRICATION","INJECTION_MOLDING","CONTRACT_MANUFACTURER","PACKAGING_MANUFACTURER"]
def q(path,params):
    qs=urllib.parse.urlencode(params,doseq=True)
    for a in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.discolike.com/v1/{path}?{qs}",headers={"x-discolike-key":KEY}),timeout=180))
        except urllib.error.HTTPError as e:
            b=e.read()[:300].decode('utf8','ignore')
            if e.code in (429,500,502,503,504): time.sleep(2**a); continue
            return {"error":e.code,"msg":b}
        except Exception: time.sleep(2**a)
    return {"error":"retries"}
def params(cat,country,emp="51,",ph=PH,neg_sub=NEG_SUB):
    p={"phrase_match":ph,"category":cat,"country":country,"employee_range":emp}
    if neg_sub and "MANUFACTURING" in cat: p["negate_sub_industry"]=["MANUFACTURING/"+x for x in neg_sub]
    return p
