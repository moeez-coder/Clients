import json,os,sys,time,urllib.request
KEY=os.environ['BLITZ_API_KEY']
def call(body):
    for a in range(5):
        try:
            req=urllib.request.Request('https://api.blitz-api.ai/v2/company/tam-by-jobs',json.dumps(body).encode(),{'x-api-key':KEY,'Content-Type':'application/json'})
            return json.load(urllib.request.urlopen(req,timeout=90))
        except Exception as e:
            print('retry',a,e,file=sys.stderr); time.sleep(2*(a+1))
    raise SystemExit('fail')
name,titles,days,minpc=sys.argv[1],json.loads(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
body={"job":{"title":{"include":titles},"location":{"country_code":{"include":["US"]}},"date_posted":{"last_days":days},"min_per_company":minpc},"company":{"employee_count":{"min":1000}},"max_results":50,"cursor":None}
out=[];pages=0
while True:
    r=call(body);pages+=1
    for x in r['results']:
        c=x['company'];out.append({'linkedin_url':c['linkedin_url'],'name':c['name'],'matched_jobs':x['matched_jobs'],'employee_growth':c.get('employee_growth'),'employees_on_linkedin':c.get('employees_on_linkedin')})
    body['cursor']=r.get('cursor')
    if not body['cursor'] or pages>=300: break
json.dump(out,open(name+'.json','w'))
print(name,len(out),'pages',pages)
