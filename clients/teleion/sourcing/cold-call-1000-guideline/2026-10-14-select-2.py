import pickle,csv,re,collections,os
P=pickle.load(open('k_people.pkl','rb'))
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
SIG={}
for f in ['/home/user/Clients/clients/teleion/sourcing/fs-compliance-ops-signals-recheck/2026-10-12-companies.csv','/home/user/Clients/clients/teleion/sourcing/all-icps-job-signals-expansion/2026-10-12-companies.csv']:
    for x in csv.DictReader(open(f)):
        if x['has_signal']=='yes': SIG[nd(x['domain'])]=x
US=re.compile(r"(united states|, (al|ak|az|ar|ca|co|ct|de|fl|ga|hi|id|il|in|ia|ks|ky|la|me|md|ma|mi|mn|ms|mo|mt|ne|nv|nh|nj|nm|ny|nc|nd|oh|ok|or|pa|ri|sc|sd|tn|tx|ut|vt|va|wa|wv|wi|wy)\b|metropolitan area|greater .* area|bay area)",re.I)
WEST=re.compile(r"(washington|oregon|california|seattle|portland|san francisco|los angeles|san diego|bay area|san jose)",re.I)
FS=re.compile(r"(bank|credit union|fintech|payments|financial services|insurance)",re.I)
def rev(p):
    r=p['c_rev']
    if r and r!='-':
        lo=int(r.split('-')[0])
        return ('confirmed','revenue range '+r+' (account export)') if lo>=20000000 else ('unverified','revenue range '+r+' straddles $20M')
    if p['c_emp'] and p['c_emp']>=1000: return ('inferred','no revenue figure; inferred over $20M from %d employees'%p['c_emp'])
    return ('unknown','no revenue figure in account export')
SIGBC={'P3':'Compliance, risk & fraud','P2':'Compliance, risk & fraud','P5':'AI & data governance','E1':'AI & data governance','M1':'Payments & finance','M2':'Marketing operations','E2':'Operations & procurement','E3':'Operations & procurement'}
def sen(t):
    t=t.lower()
    if re.search(r"\bchief\b|\bc[a-z]o\b|\bciso\b|treasurer",t): return 3
    if re.search(r"\b(evp|svp|executive vice president|senior vice president)\b",t): return 2.5
    if re.search(r"\b(vp|vice president|head)\b",t): return 2
    return 1
def service(p):
    b=p['buying_center'];t=p['job_title'].lower()
    if b=='AI & data governance':
        if re.search(r"\b(data|analytics)\b",t) and not re.search(r"\b(ai|artificial|machine)\b",t): return 'Data and business intelligence (data strategy, pipelines, dashboards, governance)'
        return 'AI governance and AI in production (get AI out of pilot, with evidence it is controlled)'
    if b=='Compliance, risk & fraud': return 'Compliance and financial services operations (AML, sanctions screening, fraud, BaaS, regulator-flagged fixes)'
    if b=='Marketing operations': return 'Marketing operations (campaign operations end to end, AI-generated content review)'
    if b=='Payments & finance':
        if re.search(r"payment|treasur",t): return 'Payments and merchant cost (true cost per transaction by channel)'
        return 'Payments and merchant cost, plus finance operations that cannot scale without hiring'
    if b=='Operations & procurement':
        if re.search(r"procure|sourcing|supplier|vendor",t): return 'Vendor and supplier management (governing large vendor and contractor networks)'
        return 'Operations that cannot scale without hiring (clear backlogs and manual queues by redesigning the process)'
    return 'Executive sponsor for any Teleion program; lead with operations that cannot scale without hiring'
PROOF={'Compliance, risk & fraud':'"For a BaaS sponsor bank we reached examiner agreement to close 64% of outstanding findings within 12 months."',
 'AI':'"We governed 800+ AI assets at a Fortune 10 technology company, and took an enterprise SaaS platform to ISO 42001 in 4 months with zero findings."',
 'Data':'"We got AI tools to production in days instead of months at a Fortune 10 technology company."',
 'Marketing operations':'"For a global retail brand we cut campaign defect rate from 23% to 3% and rework from 47% to 6%."',
 'Payments':'No quantified payments result supplied yet; do not quote a number. Teleion\'s Payments Strategy Sprint measures cost economics, settlement timing and reconciliation for one channel or contract.',
 'Ops':'"For a global technology company we cleared a 3,663 ticket backlog and cut average resolution time 92%, from about 30 days to about 2."',
 'Vendor':'"For a global technology company with 650+ vendors and 18,000+ contract resources, we cut operational cost and rework 26% in year one."'}
QUEST={'Compliance, risk & fraud':'"What happens to your backlog or alert queue when volume grows 20%?"','AI':'"Where is your AI work today: pilot, partial production, or live?"','Data':'"If an examiner or auditor asked which data trained a model and who approved it, how long would the answer take?"','Marketing operations':'"How is compliance reviewing content that AI helped produce?"','Payments':'"Can your team say what a channel costs per transaction today?"','Ops':'"How much of that work is still manual today?"','Vendor':'"Do you use outside contractors or vendors for this work today?"'}
OPEN={'P3':'"I noticed {company} is hiring several BSA and AML roles. That usually means alert volume and OFAC screening are outrunning the team." Ask: "Is the hiring to catch up on backlog, or to support new growth?"',
 'M2':'"I saw you are hiring for marketing compliance review. That role often appears when AI generated content starts outpacing manual review." Ask: "Is the new hire meant to clear a backlog or keep up with ongoing volume?"',
 'M1':'"I noticed {company} is hiring a payments analyst. Often that is because nobody has one view of true cost per transaction." Ask: "Is the new analyst meant to build that cost visibility from scratch?"',
 'P5':'"I saw {company} is hiring for AI governance. That usually means the program is being built while AI is already in production." Ask: "Is the mandate to build from the ground up, or formalize something that partly exists?"',
 'E1':'"I saw {company} is hiring for AI governance. That usually means the program is being built while AI is already in production." Ask: "Is the mandate to build from the ground up, or formalize something that partly exists?"',
 'P2':'"I saw {company} is expanding its fintech partner program. Every new partner adds monitoring and KYC load faster than most compliance teams can absorb." Ask: "Is compliance scaling at the same pace as partner onboarding?" (Signal is a job-posting proxy, not an announced partnership; phrase as hiring.)',
 'E2':'Structural-event pattern (no scripted opener): name the M&A-integration hiring in one sentence, one proof point, one question. Signal is a job-posting proxy, not an announced deal.',
 'E3':'Vendor/contractor pattern: name the vendor-management or contingent-workforce hiring, use the vendor proof point, ask whether outside contractors do this work today. Signal is a proxy.'}
def kind(p):
    s=service(p)
    if s.startswith('AI'): return 'AI'
    if s.startswith('Data'): return 'Data'
    if s.startswith('Vendor'): return 'Vendor'
    if s.startswith('Operations') or s.startswith('Executive'): return 'Ops'
    if s.startswith('Payments'): return 'Payments'
    return p['buying_center']
rows=[]
for p in P:
    d=p['company_domain'];s=SIG.get(d);codes=s['signal_codes'].split(',') if s else []
    match=[c for c in codes if SIGBC.get(c)==p['buying_center']]
    rs,rnote=rev(p)
    us=bool(US.search(p['location'] or ''))
    fs=bool(FS.search(p['c_seg'] or ''))
    score=(40 if match else 0)+(10 if codes else 0)+{'confirmed':15,'inferred':10,'unverified':3,'unknown':0}[rs]+(10 if fs else 0)+(8 if us else -30)+(3 if WEST.search(p['location'] or '') else 0)+sen(p['job_title'])*3
    k=kind(p)
    if match:
        c=match[0];note=[n for n in s['notes'].split(' || ') if n.startswith('['+c+']')]
        trig=s['signals_triggers'].split(' + ')[codes.index(c)] if ' + ' in s['signals_triggers'] or len(codes)==1 else s['signals_triggers']
        trigger=f"{c}: {trig} — {note[0][:300] if note else ''}"
        opener=OPEN[c].replace('{company}',p['c_name'])
    elif codes:
        trigger='Company signal not in this person\'s area ('+s['signals_triggers']+'); '+s['notes'][:200]
        opener='General opener (signal belongs to another buying center): "...I am reaching out to people in '+p['buying_center'].split(' (')[0].lower()+' to see how you are handling '+{'AI':'getting AI from pilot into production with evidence it is controlled','Data':'data governance and reporting','Payments':'cost per transaction by channel','Ops':'backlogs and manual queues as volume grows','Vendor':'governing your vendor and contractor network','Compliance, risk & fraud':'alert volume and screening as the business grows','Marketing operations':'review of AI-generated content'}[k]+'."'
    else:
        trigger='none found — use the general opener'
        opener='General opener: "...I am reaching out to people in '+p['buying_center'].split(' (')[0].lower()+' to see how you are handling '+{'AI':'getting AI from pilot into production with evidence it is controlled','Data':'data governance and reporting','Payments':'cost per transaction by channel','Ops':'backlogs and manual queues as volume grows','Vendor':'governing your vendor and contractor network','Compliance, risk & fraud':'alert volume and screening as the business grows','Marketing operations':'review of AI-generated content'}[k]+'."'
    rows.append(dict(p,score=score,rs=rs,rnote=rnote,us=us,fs=fs,match=bool(match),codes=','.join(codes) or '-',trigger=trigger,opener=opener,proof=PROOF[k],question=QUEST[k],service=service(p)))
# require revenue not 'unknown' unless needed
REG=re.compile(r'(federal reserve|finra|securities and exchange|consumer financial protection|\bfdic\b|comptroller of the currency|ncua)',re.I)
rows.sort(key=lambda r:-r['score'])
def nl(u):
    u=(u or '').strip().lower().split('?')[0].rstrip('/')
    return re.sub(r'^https?://([a-z]{2,3}\.)?(www\.)?','',u)
X1='/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/01d219d5-2026-10-12-leads-Default-view-export-1792005282379.csv'
X2='/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/2c42096b-qualified_leads-Default-view-export-1792005263164.csv'
XL=set();XN=set();xc=collections.Counter()
for f,lc,nc,dc in [(X1,'linkedin_url','full_name','company_domain'),(X2,'LinkedIn Profile','Full Name','Company Domain')]:
    for x in csv.DictReader(open(f)):
        xc[f]+=1
        if x.get(lc): XL.add(nl(x[lc]))
        XN.add(((x.get(nc) or '').strip().lower(),nd(x.get(dc) or '')))
print('exclusion rows',dict((k[-40:],v) for k,v in xc.items()),'urls',len(XL))
open('k_exclusion_urls.txt','w').write('\n'.join(sorted(XL)))
excluded=collections.Counter()
by=collections.Counter();bybc=collections.Counter();out=[]
CAP=4;BCCAP=2
for r in rows:
    if r['rs']=='unknown' or not r['us']: continue
    if nl(r['linkedin_url']) in XL: excluded['url']+=1; continue
    if ((r['full_name'] or '').strip().lower(),r['company_domain']) in XN: excluded['name+domain']+=1; continue
    if REG.search(r['c_name'] or '') or re.search(r'associate vice president|\bavp\b',r['job_title'],re.I): continue
    d=r['company_domain']
    if by[d]>=CAP or bybc[(d,r['buying_center'])]>=BCCAP: continue
    by[d]+=1;bybc[(d,r['buying_center'])]+=1;out.append(r)
    if len(out)==1000: break
print('excluded from selection',dict(excluded));print('selected',len(out),'companies',len(by))
print(collections.Counter(r['buying_center'] for r in out))
print(collections.Counter(r['rs'] for r in out),'signal match',sum(r['match'] for r in out),'any signal',sum(r['codes']!='-' for r in out),'FS',sum(r['fs'] for r in out))
print('pool sizes: unknown-rev',sum(1 for r in rows if r['rs']=='unknown'),'non-US',sum(1 for r in rows if not r['us']))
pickle.dump((rows,out),open('k_sel.pkl','wb'))

dd='/home/user/Clients/clients/teleion/sourcing/cold-call-1000-guideline'
os.makedirs(dd,exist_ok=True)
f=dd+'/2026-10-14-leads-2.csv'
assert not os.path.exists(f)
res=[]
for i,r in enumerate(out,1):
    res.append({'linkedin_url':r['linkedin_url'],'first_name':r['first_name'] or '-','last_name':r['last_name'] or '-','full_name':r['full_name'] or '-','job_title':r['job_title'],'buying_center':r['buying_center'],'teleion_service_to_sell':r['service'],
     'company_name':r['c_name'] or '-','company_domain':r['company_domain'],'company_linkedin_url':r['c_li'] or '-','segment':r['c_seg'] or '-','employees':r['c_emp'],'revenue_status':r['rs'],'revenue_note':r['rnote'],'location':r['location'] or '-',
     'company_signal_codes':r['codes'],'trigger':r['trigger'],'call_opener':r['opener'],'proof_point':r['proof'],'discovery_question':r['question'],'priority_rank':i,'source_list':r['source_list']})
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(res[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(res)
print('wrote',len(res))
