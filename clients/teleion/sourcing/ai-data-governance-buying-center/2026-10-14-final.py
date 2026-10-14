import pickle,re,csv,collections,os,shutil,json,gzip
exec(open('ai2_class.py').read().split("out={}")[0])
P=pickle.load(open('ai2_people.pkl','rb'))
NATIVE_TEXT=re.compile(r"(ai[- ](native|first|forward)|ai[- ]powered platform)",re.I)
out={}
for d,v in R.items():
    name=v['name'] if v['name'] not in('-','') else d
    news=[n for n in v['news'] if not NOISE.search(n[1])]
    if name=='Stash': news=[n for n in news if 'stashfin' not in n[1].lower()]
    txt=v['about_ai']+v['spec_ai'];share=(v['ai_jobs']/v['jobs']) if v['jobs'] else 0
    nat=[n for n in news if NATIVE.search(n[1])];dep=[n for n in news if DEPLOY.search(n[1])]
    tier=None
    if txt>=3 or (TECH.search(v['industry'] or '') and share>=0.15 and v['ai_jobs']>=5) or [n for n in news if NATIVE_TEXT.search(n[1])]:
        tier='AI-first / AI-native'
    elif v['ai_jobs']>=5 or (v['ai_jobs']>=3 and share>=0.05) or (len(dep)>=2 and v['ai_jobs']>=2) or (nat and v['ai_jobs']>=2) or (nat and TECH.search(v['industry'] or '')):
        tier='AI-enabled (heavy use)'
    why=[]
    if tier:
        if txt: why.append(f"company page mentions AI {txt}x")
        if v['ai_jobs']: why.append(f"{v['ai_jobs']} AI/ML roles of {v['jobs']} postings in 90 days")
        for n in (nat or dep)[:2]: why.append(f"{n[0]}: {n[1]} ({n[2]})")
    out[d]=dict(v,name=name,tier=tier,why=' | '.join(why),revstat=revstat(d))
# Manual overrides after reading the evidence (documented in the query record):
for d,v in list(out.items()):
    if v['name'] in('altruist.com',) or d=='altruist.com':
        v['why']='; '.join(w for w in v['why'].split(' | ') if 'BPCE' not in w)   # BPCE news is about another company
    if v['name']=='WorkWave': v['tier']='AI-enabled (heavy use)'                  # AI product launch, but not an AI-first company
    if v['name']=='Forge': v['tier']=None                                         # evidence concerns Atlassian Forge, a different company
Q={d:v for d,v in out.items() if v['tier']}
print('qualified',len(Q),collections.Counter(v['tier'] for v in Q.values()))
conf={d:v for d,v in Q.items() if v['revstat'].startswith('confirmed')}
oth={d:v for d,v in Q.items() if not v['revstat'].startswith('confirmed')}
print('confirmed',len(conf),'other',len(oth))
FO={'Chief AI / Head of AI':0,'CISO / Security':1,'Chief Data Officer / Data':2,'CIO / IT':3,'Infrastructure':4}
def sen(t):
    t=t.lower()
    return 0 if re.search(r"chief|\bc[a-z]o\b",t) else 1 if re.search(r"head of|svp|evp|senior vice|vice president|\bvp\b",t) else 2
def build(cs):
    rows=[];by=collections.defaultdict(list)
    for p in P:
        if p['company_domain'] in cs: by[p['company_domain']].append(p)
    for d,ps in by.items():
        ps.sort(key=lambda p:(FO[p['function']],sen(p['job_title']),len(p['job_title'])))
        for p in ps[:10]:
            v=cs[d]
            rows.append({'linkedin_url':p['linkedin_url'],'first_name':p['first_name'],'last_name':p['last_name'],'full_name':p['full_name'],'job_title':p['job_title'],'buying_center_function':p['function'],'company_name':v['name'],'company_domain':d,'company_employees':v['employees'],'revenue_status':v['revstat'],'ai_classification':v['tier'],'ai_evidence':v['why'] or '-','location':p['location'],'source_list':p['source_list']})
    rows.sort(key=lambda r:(r['ai_classification'],r['company_name'],FO[r['buying_center_function']]))
    return rows
A=build(conf);Bk=build(oth)
dd='/home/user/Clients/clients/teleion/sourcing/ai-data-governance-buying-center'
os.makedirs(dd,exist_ok=True)
def wr(f,rows):
    assert not os.path.exists(f)
    w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(rows[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(rows)
wr(dd+'/2026-10-14-leads.csv',A);wr(dd+'/2026-10-14-leads-revenue-unconfirmed.csv',Bk)
crow=[{'company_name':v['name'],'company_domain':d,'linkedin_url':v['li'] or '-','industry':v['industry'] or '-','employees':v['employees'],'revenue_status':v['revstat'],'ai_classification':v['tier'],'ai_roles_90d':v['ai_jobs'],'postings_90d':v['jobs'] if v['jobs'] is not None else '-','ai_evidence':v['why'] or '-','prospects_in_leads_file':sum(1 for r in A if r['company_domain']==d)} for d,v in sorted(Q.items(),key=lambda kv:(kv[1]['tier'],kv[1]['name']))]
wr(dd+'/2026-10-14-companies.csv',crow)
json.dump({d:{k:(v[k] if k!='news' else v[k]) for k in v} for d,v in out.items()},gzip.open(dd+'/2026-10-14-company-evidence-raw.json.gz','wt'),default=str)
for f,s in [('ai2_people.py','people'),('ai2_comp.py','pull'),('ai2_class.py','class0'),('ai2_final.py','final')]: shutil.copy(f,dd+f'/2026-10-14-{s}.py')
print('leads confirmed',len(A),len({r['company_domain'] for r in A}),collections.Counter(r['ai_classification'] for r in A),collections.Counter(r['buying_center_function'] for r in A))
print('leads unconfirmed',len(Bk),len({r['company_domain'] for r in Bk}))
for d,v in conf.items(): print(' ',v['name'],'|',v['tier'],'|',v['revstat'][:30],'|',sum(1 for r in A if r['company_domain']==d))
