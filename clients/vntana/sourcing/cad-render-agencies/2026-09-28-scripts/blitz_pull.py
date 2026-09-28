import json,os,sys,time,urllib.request
KEY=os.environ['BLITZ_API_KEY']
INDUSTRIES=["Advertising Services","Marketing Services","Design Services","Graphic Design","Animation and Post-production","Media Production","Photography","Architecture and Planning"]
KW=["CGI","3D rendering","3D render","renders","product rendering","product visualization","3D visualization","3D animation","CAD","photorealistic","3D product"]
body={"company":{"industry":{"include":INDUSTRIES},"keywords":{"include":KW},"employee_range":["1-10","11-50","51-200","201-500","501-1000","1001-5000"]},"max_results":25}
out=[];cursor=None;pages=0
while True:
    if cursor: body["cursor"]=cursor
    req=urllib.request.Request("https://api.blitz-api.ai/v2/search/companies",data=json.dumps(body).encode(),headers={"x-api-key":KEY,"Content-Type":"application/json"})
    for a in range(4):
        try: d=json.load(urllib.request.urlopen(req,timeout=60));break
        except Exception as e: print('retry',e,file=sys.stderr);time.sleep(2**a)
    if pages==0: print('total_results',d['total_results'],file=sys.stderr)
    out+=d['results'];pages+=1;cursor=d.get('cursor')
    if not cursor or pages>=int(sys.argv[1]): break
json.dump({"body":{k:v for k,v in body.items() if k!='cursor'},"pages":pages,"final_cursor":cursor,"results":out},open('raw.json','w'))
print('pulled',len(out),'pages',pages,'cursor_null',cursor is None,file=sys.stderr)
