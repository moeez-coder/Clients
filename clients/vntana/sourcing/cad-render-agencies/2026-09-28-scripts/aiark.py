import json,os,sys,time,urllib.request
H={"X-TOKEN":os.environ['AIARK_API_KEY'],"Content-Type":"application/json","User-Agent":"curl/8.5.0"}
URL="https://api.ai-ark.com/api/developer-portal/v1/companies"
def call(body):
    for a in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(URL,data=json.dumps(body).encode(),headers=H),timeout=90))
        except urllib.error.HTTPError as e:
            msg=e.read()[:300]; print('HTTP',e.code,msg,file=sys.stderr)
            if e.code in (400,422): raise
            time.sleep(2**a)
        except Exception as e: print('err',e,file=sys.stderr); time.sleep(2**a)
def pull(body,maxpages,out):
    res=[]
    for p in range(maxpages):
        body['page']=p; d=call(body)
        if p==0: print(out,'totalElements',d['totalElements'],file=sys.stderr)
        res+=d['content']; time.sleep(0.25)
        if d['last']: break
    json.dump({"body":{k:v for k,v in body.items() if k!='page'},"pages":p+1,"results":res},open(out,'w'))
    print(out,'pulled',len(res),'pages',p+1,'last',d['last'],file=sys.stderr)
