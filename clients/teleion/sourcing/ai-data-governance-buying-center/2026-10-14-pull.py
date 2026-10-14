import os,json,pickle,re,time,csv,datetime,urllib.request,concurrent.futures as cf
BK=os.environ['BLITZ_API_KEY'];EK=os.environ['EXA_API_KEY']
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
P=pickle.load(open('ai2_people.pkl','rb'))
base="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/7cb2e220-Teleion_target_accounts_with_signals-2-Default-view-export-1791818754556.csv"
LI={nd(x['domain']):x['linkedin_url'] for x in csv.DictReader(open(base))}
for x in csv.DictReader(open('/home/user/Clients/clients/teleion/sourcing/all-icps-job-signals-expansion/2026-10-12-companies.csv')): LI.setdefault(nd(x['domain']),x['linkedin_url'])
comps={}
for p in P: comps.setdefault(p['company_domain'],{'name':p['company_name'],'employees':p['employees'],'li':LI.get(p['company_domain'])})
def post(url,body,h):
    for i in range(4):
        try:
            rq=urllib.request.Request(url,json.dumps(body).encode(),{**h,'content-type':'application/json','User-Agent':'curl/8.5.0'})
            return json.load(urllib.request.urlopen(rq,timeout=60))
        except Exception: time.sleep(2+2*i)
    return None
AI=re.compile(r"\b(ai|a\.i\.|artificial intelligence|machine learning|ml|deep learning|llm|generative|genai|nlp|computer vision|data scien\w+|applied scien\w+|research scien\w+|mlops)\b",re.I)
AITXT=re.compile(r"(artificial intelligence|\bai\b|machine learning|generative|\bllm\b|deep learning|agentic|computer vision|neural)",re.I)
def tok(n):
    t=re.sub(r'[^a-z0-9 ]','',(n or '').lower());t=re.sub(r'\b(inc|corp|corporation|llc|co|company|group|holdings|the|financial|bank|credit|union|federal)\b','',t).split()
    return ' '.join(t[:2]) if t else (n or '').lower()
def exa(q):
    d=(datetime.date(2026,10,14)-datetime.timedelta(days=365)).isoformat()
    j=post('https://api.exa.ai/search',{'query':q,'numResults':6,'startPublishedDate':d,'type':'auto','contents':{'highlights':{'numSentences':2,'highlightsPerUrl':1}}},{'x-api-key':EK})
    return (j or {}).get('results',[])
def work(item):
    d,c=item;out={'name':c['name'],'employees':c['employees'],'li':c['li'],'about':'','spec':'','industry':'','jobs':None,'ai_jobs':0,'ai_titles':[],'news':[]}
    if not c['li']:
        j=post('https://api.blitz-api.ai/v2/enrichment/domain-to-linkedin',{'domain':d},{'x-api-key':BK});c['li']=(j or {}).get('company_linkedin_url');out['li']=c['li']
    if c['li']:
        e=post('https://api.blitz-api.ai/v2/enrichment/company',{'company_linkedin_url':c['li']},{'x-api-key':BK}) or {}
        co=e.get('company') or e
        out['about']=(co.get('about') or '')[:600];sp=co.get('specialties');out['spec']=' '.join(sp) if isinstance(sp,list) else str(sp or '');out['industry']=co.get('industry') or ''
        js=[];cur=None
        for _ in range(4):
            j=post('https://api.blitz-api.ai/v2/jobs/company',{'company_linkedin_url':c['li'],'job':{'date_posted':{'last_days':90}},'max_results':50,'cursor':cur},{'x-api-key':BK})
            if not j: break
            js+=j.get('results',[]);cur=j.get('cursor')
            if not cur: break
        out['jobs']=len(js);t=[(j['title'],j['date_posted'][:10]) for j in js if AI.search(j['title'] or '')]
        out['ai_jobs']=len(t);out['ai_titles']=t[:4]
    k=tok(c['name'])
    if k:
        ev=[]
        for q in (f"{c['name']} AI-first company artificial intelligence",f"{c['name']} uses generative AI across the business"):
            for r in exa(q):
                if k not in (r['title'] or '').lower() and k.replace(' ','') not in r['url'].lower(): continue
                if not AI.search(r['title'] or '') or re.search(r"(job|career|award|webinar)",(r['title'] or '')+r['url'],re.I): continue
                if r.get('publishedDate'): ev.append(((r.get('publishedDate') or '')[:10],r['title'][:110],r['url']))
        seen=set()
        for e in sorted(ev,reverse=True):
            if e[2] not in seen: seen.add(e[2]);out['news'].append(e)
        out['news']=out['news'][:3]
    out['about_ai']=len(AITXT.findall(out['about']));out['spec_ai']=len(AITXT.findall(out['spec']))
    return d,out
with cf.ThreadPoolExecutor(12) as ex: R=dict(ex.map(work,comps.items()))
pickle.dump(R,open('ai2_comp.pkl','wb'))
print(len(R),'with jobs',sum(1 for v in R.values() if v['jobs'] is not None),'ai>=1',sum(1 for v in R.values() if v['ai_jobs']>=1),'ai>=3',sum(1 for v in R.values() if v['ai_jobs']>=3),'news',sum(1 for v in R.values() if v['news']),'about_ai>=1',sum(1 for v in R.values() if v['about_ai']>=1))
