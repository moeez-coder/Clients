import pickle,re,csv,collections
R=pickle.load(open('ai2_comp.pkl','rb'))
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
base="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/7cb2e220-Teleion_target_accounts_with_signals-2-Default-view-export-1791818754556.csv"
B={nd(x['domain']):x for x in csv.DictReader(open(base))}
NOISE=re.compile(r"(interview|tracker|questions|guide|dataford|larridin|what is|how to|best |vs\.?|review|pricing|alternatives)",re.I)
DEPLOY=re.compile(r"(launch|deploy|adopt|partner|rolls? out|announc|select|uses|using|integrat|powered|driven|introduc|unveil|build|invest)",re.I)
NATIVE=re.compile(r"(ai[- ](powered|driven|native|first|based)|ai platform|ai agents?|agentic)",re.I)
TECH=re.compile(r"(software|information technology|it services|internet|computer|data infrastructure|information services)",re.I)
def revstat(d):
    b=B.get(d)
    if not b: return 'unknown (not in export)'
    r=b['revenue_range']
    if not r or r=='-': return 'unknown (no revenue in export)'
    lo=int(r.split('-')[0])
    return 'confirmed >= $20M ('+r+')' if lo>=20000000 else 'unverified: band '+r+' straddles $20M'
out={}
for d,v in R.items():
    news=[n for n in v['news'] if not NOISE.search(n[1])]
    txt=v['about_ai']+v['spec_ai'];share=(v['ai_jobs']/v['jobs']) if v['jobs'] else 0
    native_news=[n for n in news if NATIVE.search(n[1])]
    deploy_news=[n for n in news if DEPLOY.search(n[1])]
    why=[];tier=None
    if txt>=3 or (TECH.search(v['industry'] or '') and share>=0.15 and v['ai_jobs']>=5) or (native_news and TECH.search(v['industry'] or '')):
        tier='AI-first / AI-native'
    elif v['ai_jobs']>=5 or (v['ai_jobs']>=3 and share>=0.05) or (len(deploy_news)>=2 and v['ai_jobs']>=2) or (native_news and v['ai_jobs']>=2):
        tier='AI-enabled (heavy use)'
    if tier:
        if txt: why.append(f"company page mentions AI {txt}x")
        if v['ai_jobs']: why.append(f"{v['ai_jobs']} AI/ML roles of {v['jobs']} postings in 90 days")
        for n in (native_news or deploy_news)[:2]: why.append(f"{n[0]}: {n[1]} ({n[2]})")
    out[d]=dict(v,tier=tier,why=' | '.join(why),news_ok=news,revstat=revstat(d))
pickle.dump(out,open('ai2_class.pkl','wb'))
q={d:v for d,v in out.items() if v['tier']}
print(len(q),collections.Counter(v['tier'] for v in q.values()),collections.Counter(v['revstat'].split(' ')[0] for v in q.values()))
for d,v in sorted(q.items(),key=lambda kv:(kv[1]['tier'],-kv[1]['ai_jobs'])):
    print(f"{v['name'][:24]:24}|{v['tier'][:8]}|{(v['industry'] or '')[:14]:14}|e{v['employees']}|ai {v['ai_jobs']}/{v['jobs']}|txt {v['about_ai']+v['spec_ai']}|{v['revstat'][:22]}|"+(v['news_ok'][0][1][:55] if v['news_ok'] else ''))
