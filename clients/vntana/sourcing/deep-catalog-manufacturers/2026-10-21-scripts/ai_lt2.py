import json,os,time
import urllib.request,urllib.error
H={'X-TOKEN':os.environ['AIARK_API_KEY'],'Content-Type':'application/json','User-Agent':'curl/8.5.0'}
def call(body):
    for a in range(40):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.ai-ark.com/api/developer-portal/v1/companies',data=json.dumps(body).encode(),headers=H),timeout=120))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504): time.sleep(min(30,5+a*5)); continue
            return {'_err':e.code,'msg':e.read()[:200].decode('utf8','ignore')}
        except Exception: time.sleep(10)
    return None
src=[{"mode":"WORD","source":s} for s in ("DESCRIPTION","SEO","KEYWORD")]
IND=["machinery manufacturing","industrial machinery manufacturing","fabricated metal products","electrical equipment manufacturing","appliances, electrical, and electronics manufacturing","metal valve, ball, and roller manufacturing","engines and power transmission equipment manufacturing","turned products and fastener manufacturing","spring and wire product manufacturing","automation machinery manufacturing","metalworking machinery manufacturing","construction hardware manufacturing","hvac and refrigeration equipment manufacturing","motor vehicle parts manufacturing","computers and electronics manufacturing"]
V={"catalog":["online catalog","product catalog","online catalogue","part numbers","catalog number","catalogue","SKUs","stock items","thousands of products","standard parts"],
"flow":["pumps","valves","fittings","hose","hydraulic","pneumatic","fluid power","flow control","couplings","actuators","filtration"],
"fasteners":["fasteners","bolts","screws","nuts","washers","rivets","anchors","springs","clamps","o-rings","gaskets","standoffs"],
"electrical":["connectors","relays","sensors","switches","enclosures","terminal blocks","contactors","circuit breakers","fuses","cable assemblies","wire and cable","motors","drives"],
"tools":["hand tools","power tools","cutting tools","drill bits","saw blades","abrasives","tooling","workholding","measuring tools"],
"power_transmission":["bearings","gears","gearboxes","chains","sprockets","belts","clutches","brakes","shafts","power transmission","motion control"]}
os.makedirs("ai2",exist_ok=True)
for v,kw in V.items():
    fn=f"ai2/{v}.jsonl"
    if os.path.exists(fn+".done"): continue
    body={"size":100,"account":{"keyword":{"any":{"include":{"sources":src,"content":kw}}},"industries":{"any":{"include":{"mode":"WORD","content":IND}}},"employeeSize":{"type":"RANGE","range":[{"start":51,"end":1000000}]}}}
    n=0
    with open(fn,"w") as f:
        p=0
        while True:
            body["page"]=p; d=call(body)
            if not isinstance(d,dict) or "content" not in d: f.write(json.dumps({"_error":str(d)[:200]})+"\n"); break
            if p==0: f.write(json.dumps({"_meta":{"total":d["totalElements"],"vertical":v}})+"\n"); print(v,"total",d["totalElements"],flush=True)
            for r in d["content"]:
                s=r.get("summary") or {}; l=r.get("link") or {}; loc=((r.get("location") or {}).get("headquarter") or {})
                f.write(json.dumps({"name":s.get("name"),"description":(s.get("description") or "")[:900],"seo":(s.get("seo") or "")[:300],"industry":s.get("industry"),"staff":(s.get("staff") or {}).get("total"),"staff_range":(s.get("staff") or {}).get("range"),"website":l.get("website"),"domain":l.get("domain"),"linkedin":l.get("linkedin"),"country":loc.get("country") or loc.get("raw_address"),"keywords":(r.get("keywords") or [])[:15],"naics":(r.get("naics") or [])[:6],"revenue":(r.get("financial") or {}).get("revenue")})+"\n"); n+=1
            if d.get("last") or p>=99: break
            p+=1; time.sleep(0.5)
    open(fn+".done","w").write(str(n)); print(v,"rows",n,flush=True)
print("DONE",flush=True)
