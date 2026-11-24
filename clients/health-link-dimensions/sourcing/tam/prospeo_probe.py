import json,os,urllib.request,urllib.error,sys
def post(path,body):
    try: return json.load(urllib.request.urlopen(urllib.request.Request("https://api.prospeo.io/"+path,data=json.dumps(body).encode(),headers={"X-KEY":os.environ["PROSPEO_API_KEY"],"Content-Type":"application/json"}),timeout=90))
    except urllib.error.HTTPError as e:
        b=e.read()[:600].decode(errors="ignore")
        try: return json.loads(b)
        except: return {"error":True,"code":e.code,"raw":b}
if __name__=="__main__":
    body=json.loads(sys.argv[2]); r=post(sys.argv[1],body)
    print(json.dumps({k:v for k,v in r.items() if k not in("results",)})[:800]); 
    for x in (r.get("results") or [])[:3]: print(json.dumps(x)[:300])
