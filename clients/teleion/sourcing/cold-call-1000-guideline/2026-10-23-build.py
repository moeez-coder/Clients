import json,pickle,csv,re,collections,os
kp=open('k_people.py').read()
exec(kp[kp.find('EXCL='):kp.find('def company')])  # EXCL, SEN, BC, bc
ks=open('k_select.py').read()
exec(ks[ks.find('US=re.compile'):ks.find('def rev(')])
exec(ks[ks.find('def sen('):ks.find('rows=[]')])  # sen, service, PROOF, QUEST, OPEN, kind
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
nl=lambda u:re.sub(r'^https?://([a-z]{2,3}\.)?(www\.)?','',(u or '').strip().lower().split('?')[0].rstrip('/'))
U=pickle.load(open('m_univ.pkl','rb'))
LI2D={nl(v['li']):d for d,v in U.items() if v['li']}
X=set(open('k_exclusion_urls.txt').read().split('\n'))
used={nl(x['linkedin_url']) for x in csv.DictReader(open('/home/user/Clients/clients/teleion/sourcing/cold-call-1000-guideline/2026-10-14-leads-2.csv'))}
used|={nl(x['linkedin_url']) for x in csv.DictReader(open('/home/user/Clients/clients/teleion/sourcing/cold-call-1000-guideline/2026-10-14-leads.csv'))}
cand={};drop=collections.Counter()
def add(url,first,last,full,title,loc,d,src):
    k=nl(url)
    if not k: drop['no url']+=1;return
    if k in X: drop['in already-worked lists']+=1;return
    if k in used: drop['already in the 1,000 list']+=1;return
    if d not in U: drop['company not qualified']+=1;return
    if re.search(r'\bassociation\b',U[d]['name'] or '',re.I): drop['trade association']+=1;return
    if re.search(r'\brevenue\b(?! operations)',title,re.I): drop['revenue (sales) title']+=1;return
    if EXCL.search(title) or re.search(r'associate vice president|\bavp\b',title,re.I): drop['excluded title']+=1;return
    if not SEN.search(title): drop['below seniority']+=1;return
    g=bc(title)
    if not g: drop['no buying center']+=1;return
    if not US.search(loc or ''): drop['not US']+=1;return
    if k in cand: return
    cand[k]=dict(linkedin_url=url,first_name=first,last_name=last,full_name=full,job_title=title,buying_center=g[0],location=loc,company_domain=d,source=src)
# 1) Blitz
for p in json.load(open('m_people_raw.json')):
    ex=[e for e in p.get('experiences') or [] if e.get('job_is_current') and nl(e.get('company_linkedin_url') or '') in LI2D]
    if not ex: drop['current job not at a qualified company']+=1;continue
    e=ex[0];loc=p.get('location') or {}
    locs=', '.join(x for x in [loc.get('city'),loc.get('state_code'),'United States' if loc.get('country_code')=='US' else loc.get('country_code')] if x)
    add(p['linkedin_url'],p.get('first_name'),p.get('last_name'),p.get('full_name'),e.get('job_title') or '',locs,LI2D[nl(e['company_linkedin_url'])],'Blitz API /v2/search/people (2026-10-23)')
nb=len(cand)
# 2) leftover export pool
for r in pickle.load(open('k_people.pkl','rb')):
    add(r['linkedin_url'],r['first_name'],r['last_name'],r['full_name'],r['job_title'],r['location'],r['company_domain'],r['source_list'])
print('candidates',len(cand),'from Blitz',nb,'from exports',len(cand)-nb,dict(drop))
GEN={'AI':'getting AI from pilot into production with evidence it is controlled','Data':'data governance and reporting','Payments':'cost per transaction by channel','Ops':'backlogs and manual queues as volume grows','Vendor':'governing your vendor and contractor network','Compliance, risk & fraud':'alert volume and screening as the business grows','Marketing operations':'review of AI-generated content'}
rows=[]
for k,c in cand.items():
    u=U[c['company_domain']]
    fs=bool(FS.search(u['seg'] or ''))
    score=(15 if u['rs']=='confirmed' else 10)+(10 if fs else 0)+(3 if WEST.search(c['location'] or '') else 0)+sen(c['job_title'])*3
    kk=kind(c)
    rows.append(dict(c,score=score,u=u,svc=service(c),k=kk))
rows.sort(key=lambda r:-r['score'])
by=collections.Counter();bybc=collections.Counter();out=[]
for CAP,BCC in [(4,2),(7,3),(10,4)]:
    for r in rows:
        if len(out)>=2000: break
        d=r['company_domain'];k=nl(r['linkedin_url'])
        if r.get('_in') or by[d]>=CAP or bybc[(d,r['buying_center'])]>=BCC: continue
        by[d]+=1;bybc[(d,r['buying_center'])]+=1;r['_in']=1;out.append(r)
print('selected',len(out),'companies',len(by),'max/co',max(by.values()))
print(collections.Counter(r['buying_center'] for r in out),collections.Counter(r['u']['rs'] for r in out),collections.Counter(r['source'][:5] for r in out))
dd='/home/user/Clients/clients/teleion/sourcing/cold-call-1000-guideline'
f=dd+'/2026-10-23-leads.csv'
assert not os.path.exists(f)
res=[]
for i,r in enumerate(out,1):
    u=r['u']
    res.append({'linkedin_url':r['linkedin_url'],'first_name':r['first_name'] or '-','last_name':r['last_name'] or '-','full_name':r['full_name'] or '-','job_title':r['job_title'],'buying_center':r['buying_center'],'teleion_service_to_sell':r['svc'],
      'company_name':u['name'],'company_domain':r['company_domain'],'company_linkedin_url':u['li'] or '-','segment':u['seg'] or '-','employees':u['emp'],'revenue_status':u['rs'],'revenue_note':u['rn'],'location':r['location'] or '-',
      'call_opener':'General opener: "Hi {first_name}, {caller_name} here, calling on behalf of Teleion. We are a Seattle based firm that has spent 18 years embedded in enterprise operations, building, running and improving them. I am reaching out to people in '+r['buying_center'].split(' (')[0].lower()+' to see how you are handling '+GEN[r['k']]+'. Worth a quick chat, or is now a bad time?"',
      'proof_point':PROOF[r['k']],'discovery_question':QUEST[r['k']],'priority_rank':i,'source':r['source']})
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(res[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(res)
chk=sum(nl(x['linkedin_url']) in X|used for x in res);print('wrote',len(res),'overlap with exclusions/previous',chk,'dup urls',len(res)-len({nl(x['linkedin_url']) for x in res}))
