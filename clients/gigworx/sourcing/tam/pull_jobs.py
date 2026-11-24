import json, os, sys, time, urllib.request
KEY=os.environ['BLITZ_API_KEY']
def post(path, body):
    for i in range(5):
        try:
            r=urllib.request.Request('https://api.blitz-api.ai'+path, data=json.dumps(body).encode(),
              headers={'x-api-key':KEY,'content-type':'application/json'})
            return json.load(urllib.request.urlopen(r, timeout=60))
        except Exception as e:
            print('retry', e, file=sys.stderr); time.sleep(2*(i+1))
    raise SystemExit('failed')
CITIES=["South Bend","Mishawaka","Elkhart","Goshen","Nappanee","Wakarusa","Notre Dame"]
DAYS=int(sys.argv[1]) if len(sys.argv)>1 else 60
out=open(f'jobs_{DAYS}d.jsonl','w')
for c in CITIES:
    body={"job":{"location":{"city":{"include":[c]},"country_code":{"include":["US"]}},"date_posted":{"last_days":DAYS}},"max_results":50}
    n=0; total=None
    while True:
        d=post('/v2/jobs/search', body)
        total=d.get('total_results')
        for j in d.get('results',[]):
            j['_query_city']=c; out.write(json.dumps(j)+'\n'); n+=1
        cur=d.get('cursor')
        if not cur or not d.get('results'): break
        body['cursor']=cur
    print(c, 'pulled', n, 'total_results', total, flush=True)
