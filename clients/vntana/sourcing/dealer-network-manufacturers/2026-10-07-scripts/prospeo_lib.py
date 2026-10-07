import json,os,time,urllib.request
KEY=os.environ['PROSPEO_API_KEY']
BANDS=["51-100","101-200","201-500","501-1000","1001-2000","2001-5000","5001-10000","10000+"]
LOC=["United States #US","Canada #CA","United Kingdom #GB","Ireland #IE","Australia #AU","New Zealand #NZ","Germany #DE","France #FR","Italy #IT","Spain #ES","Netherlands #NL","Belgium #BE","Sweden #SE","Denmark #DK","Norway #NO","Finland #FI","Austria #AT","Switzerland #CH","Poland #PL","Mexico #MX","Brazil #BR","South Africa #ZA","India #IN","Japan #JP"]
VERT={
 "const":["333120","333131","333111","333112"],
 "matl":["333924","333923","333922"],
 "veh":["336212","336211","336120","336213","336214"],
 "power":["335312","333618","333611","333992","333912","335311","335313"],
 "hvac":["333415","333414","333413"],
 "flow":["333911","333914","333995","333996","332911","332912"],
}
def post(path,body):
    for a in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request("https://api.prospeo.io/"+path,data=json.dumps(body).encode(),headers={"X-KEY":KEY,"Content-Type":"application/json"}),timeout=90))
        except urllib.error.HTTPError as e:
            b=e.read()[:300].decode('utf8','ignore')
            if e.code in (429,500,502,503,504): time.sleep(2**a); continue
            try: return json.loads(b)
            except: return {"error":True,"error_code":e.code,"raw":b}
        except Exception: time.sleep(2**a)
    return {"error":True,"error_code":"retries"}
def filt(vert,band,loc=LOC): return {"company_naics":{"include":VERT[vert]},"company_headcount_range":[band],"company_location_search":{"include":loc}}
