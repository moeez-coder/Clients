import json, collections
from concurrent.futures import ThreadPoolExecutor
exec(open('people_blitz.py').read().split("def run(r):")[0].split("R=json.load")[0])  # bpost, cache
src=open('people_blitz.py').read()
ns={}; exec(src[src.index("CITIES="):src.index("def run(r):")], ns)
TIERS, EXC_BASE = ns['TIERS'], ns['EXC_BASE']
R=json.load(open('c7_236.json')); P=json.load(open('people_blitz.json'))
n=collections.Counter(p['company_name'] for p in P)
BIG={'10,000+','5,001 to 10,000','1,001 to 5,000','10001+','5001-10000','1001-5000'}
todo=[r for r in R if n[r['company_name']]<3 and r['company_linkedin_url']!='-' and r['size'] not in BIG]
def run(r):
    casc=[{'include_title':t,'exclude_title':EXC_BASE+([] if 'Assistant Store Manager' in t else ['assistant']),'location':{'country_code':['US']}} for t in TIERS[r['icp_bucket']]]
    d=bpost('/v2/search/waterfall-icp-keyword',{'company_linkedin_url':r['company_linkedin_url'],'cascade':casc,'max_results':10})
    return r, d.get('results',[])
seen={p['linkedin_url'] for p in P}; add=[]
with ThreadPoolExecutor(6) as ex:
    for r,res in ex.map(run,todo):
        for x in res:
            p=x.get('person',x); exp=(p.get('experiences') or [{}]); loc=p.get('location') if isinstance(p.get('location'),dict) else {}
            st=(loc.get('state') or ''); u=(p.get('linkedin_url') or '').rstrip('/')
            if st not in ('Indiana','Michigan') or u in seen: continue
            seen.add(u)
            add.append({'company_name':r['company_name'],'company_linkedin_url':r['company_linkedin_url'],'icp_bucket':r['icp_bucket'],'linkedin_url':u,
                        'first_name':p.get('first_name'),'last_name':p.get('last_name'),'job_title':(exp[0] or {}).get('job_title') or p.get('headline'),
                        'person_city':loc.get('city'),'person_state':st,'waterfall_tier':x.get('icp'),'source':'blitz_wide'})
json.dump(cache,open(CF,'w')); json.dump(add,open('people_blitz2.json','w'))
print('pass2 companies',len(todo),'added people',len(add),'new companies covered',len({a['company_name'] for a in add}-set(n)))
print(collections.Counter(a['person_state'] for a in add), collections.Counter(a['person_city'] for a in add).most_common(12))
