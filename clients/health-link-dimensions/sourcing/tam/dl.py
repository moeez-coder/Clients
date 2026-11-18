import json,os,urllib.request,urllib.parse,time
BASE="https://api.discolike.com/v1"
def get(path,params):
    q=urllib.parse.urlencode(params,doseq=False)
    r=urllib.request.Request(BASE+path+"?"+q,headers={"x-discolike-key":os.environ["DISCOLIKE_API_KEY"]})
    try: return json.load(urllib.request.urlopen(r,timeout=180))
    except urllib.error.HTTPError as e: return {"error":e.code,"body":e.read().decode()[:400]}
