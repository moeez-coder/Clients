import json, os, urllib.request, collections
from concurrent.futures import ThreadPoolExecutor
KEY=os.environ['BLITZ_API_KEY']; CF='blitz_cache.json'; cache=json.load(open(CF))
def bpost(path, body):
    k=path+json.dumps(body,sort_keys=True)
    if k in cache: return cache[k]
    try:
        r=urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':KEY,'content-type':'application/json'})
        d=json.load(urllib.request.urlopen(r,timeout=90))
    except urllib.error.HTTPError as e: d={'_error':e.code,'_body':e.read().decode()[:300]}
    except Exception as e: d={'_error':str(e)[:80]}
    cache[k]=d; return d
R=json.load(open('c7_236.json'))
WRONG={'FS Transportation, LLC','Tramec LLC','Exit 76 Corporation','Villa International','Metro Services, LLC'}
for r in R:
    if r['company_name'] in WRONG: r['company_linkedin_url']='-'; r['li_resolved_by']='wrong_name_match_cleared'
json.dump(R,open('c7_236.json','w'))
CITIES=["South Bend","Mishawaka","Granger","Elkhart","Goshen","Nappanee","Middlebury","Bristol","Osceola","Wakarusa"]
HR=['HR Manager','Human Resources Manager','HR Business Partner','Human Resources Business Partner','HR Director','Human Resources Director','HR Generalist','Human Resources Generalist','Talent Acquisition Manager','People Manager']
OWN=['[Owner]','[President]','CEO','COO','Founder','VP Operations','Vice President of Operations','Director of Operations']
TIERS={
 'manufacturing':[['Plant Manager','Production Manager','Operations Manager','General Manager','Manufacturing Manager','Plant Superintendent'],
                  ['Production Supervisor','Manufacturing Supervisor','Shift Supervisor','Director of Manufacturing','Production Lead'],HR,OWN],
 'warehousing_logistics':[['Warehouse Manager','Distribution Center Manager','Operations Manager','Site Manager','General Manager','Terminal Manager'],
                  ['Warehouse Supervisor','Operations Supervisor','Logistics Manager','Distribution Manager','Shipping Manager'],HR,OWN],
 'retail':[['Store Manager','General Manager','Store Director','Store Leader','District Manager'],
                  ['Assistant Store Manager','Operations Manager','Department Manager','Area Manager'],HR,OWN],
 'hospitality_fb_events':[['General Manager','Restaurant General Manager','Food and Beverage Director','Food and Beverage Manager','Director of Food and Beverage','Kitchen Manager','Executive Chef'],
                  ['Housekeeping Manager','Executive Housekeeper','Director of Housekeeping','Banquet Manager','Catering Manager','Event Manager','Operations Manager','Restaurant Manager'],HR,OWN],
}
EXC_BASE=['intern','sales','account','marketing','recruiter','finance','software','engineer','it ','quality','safety','regional sales']
def run(r):
    if r['company_linkedin_url']=='-': return r['company_name'],[]
    casc=[]
    for t in TIERS[r['icp_bucket']]:
        exc=EXC_BASE+([] if 'Assistant Store Manager' in t else ['assistant'])
        casc.append({'include_title':t,'exclude_title':exc,'location':{'city':{'include':CITIES},'country_code':['US']}})
    d=bpost('/v2/search/waterfall-icp-keyword',{'company_linkedin_url':r['company_linkedin_url'],'cascade':casc,'max_results':10})
    if d.get('_error'): print('ERR',r['company_name'],d.get('_error'),d.get('_body','')[:150])
    return r['company_name'],d.get('results',[])
with ThreadPoolExecutor(6) as ex: res=dict(ex.map(run,R))
json.dump(cache,open(CF,'w'))
P=[]
for r in R:
    for x in res.get(r['company_name'],[]):
        p=x.get('person',x); exp=(p.get('experiences') or [{}]); loc=p.get('location') if isinstance(p.get('location'),dict) else {}
        P.append({'company_name':r['company_name'],'company_linkedin_url':r['company_linkedin_url'],'icp_bucket':r['icp_bucket'],
                  'linkedin_url':(p.get('linkedin_url') or '').rstrip('/'),'first_name':p.get('first_name'),'last_name':p.get('last_name'),
                  'job_title':(exp[0] or {}).get('job_title') or p.get('headline'),'person_city':loc.get('city'),'person_state':loc.get('state'),
                  'waterfall_tier':x.get('icp'),'source':'blitz'})
json.dump(P,open('people_blitz.json','w'))
per=collections.Counter(p['company_name'] for p in P)
print('people',len(P),'companies with >=1',len(per),'of',sum(r['company_linkedin_url']!='-' for r in R))
print('per-company dist',sorted(collections.Counter(per.values()).items()))
print('tier mix',collections.Counter(p['waterfall_tier'] for p in P))
