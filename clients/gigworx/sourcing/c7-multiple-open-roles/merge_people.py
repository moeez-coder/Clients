import json, glob, re, csv, collections
R=json.load(open('c7_236.json')); B=json.load(open('clay_batches.json'))
byname={r['company_name']:r for r in R}
def nd(u):
    u=re.sub(r'^https?://','',(u or '').lower()); u=re.sub(r'^www\.','',u); return u.split('/')[0]
def nli(u): return re.sub(r'^https?://(www\.)?','https://www.',(u or '').lower().split('?')[0].rstrip('/'))
def nname(s): return re.sub(r'[^a-z0-9]','',re.sub(r'\b(inc|llc|corp|company|co|the)\b','',(s or '').lower()))
INC=re.compile(r"plant manager|production (team )?(manager|supervisor|lead|superintendent|director)|operations? (team )?(manager|director|supervisor|lead|leader)|(vp|vice president|director)\b.*\boperations\b|director of (operations|manufacturing|food|housekeeping)|general manager|\bgm\b|warehouse (manager|supervisor|lead)|distribution (center )?(manager|director)|site (manager|leader|director|lead)|store (manager|director|leader|team leader)|restaurant (general )?manager|kitchen manager|executive chef|chef manager|food (and|&) beverage|f&b|housekeeping|executive housekeeper|banquet|catering (manager|director)|event(s)? manager|human resources|\bhr\b|people (manager|partner|lead|operations)|talent acquisition (manager|lead|director)|\bowner\b|\bpresident\b|\bceo\b|\bcoo\b|founder|(vp|vice president)[ ,\-of]*(operations|manufacturing)|manufacturing (manager|director|supervisor)|shift (manager|supervisor|lead)|terminal manager|logistics manager|district manager|area manager|department manager|plant superintendent|dining (services )?(manager|director)",re.I)
EXC=re.compile(r"\bsales\b|marketing|finance|financial|account(ing|ant)?\b|engineer|software|\bit\b|technology|quality|safety|controller|intern\b|legal|procurement|purchasing|\bvp (?!.*operations)|senior vp|technical",re.I)
def rank(t):
    t=t or ''
    if re.search(r"human resources|\bhr\b|people (manager|partner|lead|operations)|talent acquisition",t,re.I): return 2
    if re.search(r"\bowner\b|\bpresident\b|\bceo\b|\bcoo\b|founder|vice president|\bvp\b",t,re.I): return 3
    if re.search(r"supervisor|\blead\b|assistant|shift",t,re.I): return 4
    return 1
P=[]
for p in json.load(open('people_blitz_all.json')):
    P.append(dict(p, person_state={'IN':'Indiana','MI':'Michigan'}.get(p['person_state'],p['person_state'])))
for f in sorted(glob.glob('clay_people_*.json')):
    for c in json.load(open(f)):
        batch=B[c['batch']]; cand=None
        d=nd(c.get('company_domain')); li=nli(c.get('company_linkedin_url'))
        for b in batch:
            ident=b['identifier']
            if (d and nd(ident)==d) or (li and nli(ident)==li) or nname(c.get('company_name'))==nname(b['company_name']) or (c.get('company_identifier') and c['company_identifier']==ident):
                cand=b['company_name']; break
        if not cand: continue
        r=byname[cand]
        P.append({'company_name':cand,'company_linkedin_url':r['company_linkedin_url'],'icp_bucket':r['icp_bucket'],'linkedin_url':(c.get('linkedin_url') or '').rstrip('/'),
                  'first_name':c.get('first_name'),'last_name':c.get('last_name'),'job_title':c.get('job_title'),'person_city':c.get('location_city'),
                  'person_state':c.get('location_state'),'waterfall_tier':None,'source':'clay'})
# dedupe on linkedin url, collect sources
by={}
for p in P:
    u=nli(p['linkedin_url'])
    if not u or '/in/' not in u: continue
    if u in by: by[u]['sources'].add(p['source']); continue
    p['sources']={p['source']}; by[u]=p
kept=[]; dropped=collections.Counter()
for p in by.values():
    t=p['job_title'] or ''
    if not INC.search(t) or EXC.search(t): dropped[t]+=1; continue
    p['persona_rank']=rank(t); kept.append(p)
per=collections.defaultdict(list)
for p in kept: per[p['company_name']].append(p)
final=[]
for cn,ps in per.items():
    ps.sort(key=lambda p:(p['persona_rank'], 0 if len(p['sources'])>1 else 1))
    final+=ps[:10]
json.dump([dict(p,sources=';'.join(sorted(p['sources']))) for p in final],open('people_final.json','w'))
cov=collections.Counter(p['company_name'] for p in final)
print('raw',len(P),'unique',len(by),'title-fit',len(kept),'final (cap 10)',len(final))
print('companies covered',len(cov),'of',len(R),' dist',sorted(collections.Counter(cov.values()).items()))
print('by source',collections.Counter(';'.join(sorted(p['sources'])) for p in final))
print('persona',collections.Counter(p['persona_rank'] for p in final))
print('dropped titles sample',dropped.most_common(25))
