import csv,re,collections,pickle,json
csv.field_size_limit(10**8)
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
FA="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/a502d029-12th-Oct-Default-view-export-1791823550720.csv"
FB="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/a87ac85c-List-1-Default-view-export-1791825335377.csv"
base="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/7cb2e220-Teleion_target_accounts_with_signals-2-Default-view-export-1791818754556.csv"
BASE={nd(x['domain']):x for x in csv.DictReader(open(base))}
contacted={d for d,x in BASE.items() if x['has_signal']=='yes'}
EXP={nd(x['domain']):x for x in csv.DictReader(open('/home/user/Clients/clients/teleion/sourcing/all-icps-job-signals-expansion/2026-10-12-companies.csv'))}
REC={nd(x['domain']):x for x in csv.DictReader(open('/home/user/Clients/clients/teleion/sourcing/fs-compliance-ops-signals-recheck/2026-10-12-companies.csv'))}
dnc=['amazon','starbucks','lyft','becu','gates foundation','gatesfoundation','microsoft','aws','twitch']
EXCL=re.compile(r"\b(retired|former|ex-|emeritus|advis(or|ory)|board member|interim|aspiring|incoming|intern|assistant|avp|associate director|ceo|chief executive|coo|chief operating|(?<!vice )(?<!vice-)president|founder|owner|recruit\w*|talent acquisition|account (executive|manager|director)|sales (manager|director|executive|representative|rep)|(vp|vice president|director|head)[^|]{0,20}\bsales\b(?! op)|business development|student|professor|consultant|contractor)\b",re.I)
SEN=re.compile(r"\b(chief|vp|vice president|svp|evp|director|head|controller|treasurer|officer|cio|ciso|cdo|cfo|cmo|chro)\b",re.I)
LEAD=r"(?:chief|vp|vice president|svp|evp|director|head|lead|leader|manager of|officer)"
BC=[
 ('Compliance, risk & fraud',re.compile(r"(chief compliance|chief risk|bsa|\baml\b|anti[- ]money|bank secrecy|financial crimes?|\bofac\b|sanctions|\bkyc\b|baas|banking as a service|\bfraud\b|compliance (director|officer)|director[^|]{0,25}compliance|(vp|vice president|head)[^|]{0,25}(compliance|risk management|enterprise risk))",re.I)),
 ('AI & data governance',re.compile(r"(chief (ai|artificial intelligence)\b|head of (ai|artificial intelligence|machine learning|data science)|\bciso\b|chief information security|chief information officer|\bcio\b|chief data|\bcdo\b|chief technology|\bcto\b|infrastructure|(vp|vice president|svp|evp|director|head)[^|]{0,30}\b(ai|artificial intelligence|machine learning|data|analytics|information security|cyber ?security|security|information technology|\bit\b|technology)\b)",re.I)),
 ('Marketing operations',re.compile(r"(chief marketing|\bcmo\b|marketing operations|sales operations|(vp|vice president|svp|evp|director|head)[^|]{0,25}marketing|marketing director)",re.I)),
 ('Payments & finance',re.compile(r"(head of payments|payments?\b[^|]{0,20}(director|head|vp|vice president)|(director|head|vp|vice president)[^|]{0,25}payments?|treasur|controller|chief financial|\bcfo\b|head of finance|(vp|vice president|svp|director)[^|]{0,20}finance|chief accounting|accounting (director|head)|director[^|]{0,20}accounting)",re.I)),
 ('Operations & procurement',re.compile(r"(head of (business |process )?operations|operations director|director[^|]{0,25}operations|(vp|vice president|svp|evp)[^|]{0,25}operations|procurement|sourcing (director|head)|chief procurement|supplier|vendor management)",re.I)),
 ('Executive sponsor (CHRO)',re.compile(r"(chief human resources|\bchro\b|chief people officer)",re.I)),
]
def bc(t):
    return [n for n,rx in BC if rx.search(t)]
def company(d,srcname,x):
    if d in BASE:
        b=BASE[d];emp=int(b['employees']);rv=b['revenue_range'] or ''
        seg=b['segment'];name=b['company_name'];li=b['linkedin_url']
    elif d in EXP:
        e=EXP[d];emp=int(e['employees']) if e['employees'].isdigit() else None;rv='';seg=e['segment'];name=e['company_name'];li=e['linkedin_url']
    else: return None
    return dict(emp=emp,rev=rv,seg=seg,name=name,li=li)
people=[];drop=collections.Counter()
def handle(x,t,d,src):
    c=company(d,src,x)
    if not c: drop['company not in any account file']+=1;return
    if not c['emp'] or c['emp']<201 or c['emp']>10000: drop['headcount outside 201-10,000']+=1;return
    if d in contacted: drop['contacted account']+=1;return
    if any(k in (c['name'] or '').lower() for k in dnc): drop['DNC']+=1;return
    if EXCL.search(t): drop['excluded title']+=1;return
    if not SEN.search(t): drop['below seniority']+=1;return
    g=bc(t)
    if not g: drop['no buying center']+=1;return
    people.append({'linkedin_url':(x['LinkedIn Profile'] or '').strip(),'first_name':x['First Name'],'last_name':x['Last Name'],'full_name':x['Full Name'],'job_title':t,'buying_center':g[0],'also':g[1:],'company_domain':d,'location':x['Location'],'source_list':src,**{'c_'+k:v for k,v in c.items()}})
for x in csv.DictReader(open(FA)): handle(x,x['Job Title'] or '',nd(x['Company Domain']),'12th-Oct people export')
for x in csv.DictReader(open(FB)): handle(x,x['Job Title'] or '',nd(x['Domain'] or x['Company Domain']),'List-1 people export')
seen=set();P=[]
for p in people:
    if not p['linkedin_url'] or p['linkedin_url'] in seen: continue
    seen.add(p['linkedin_url']);P.append(p)
print(len(P),dict(drop))
print(collections.Counter(p['buying_center'] for p in P),'companies',len({p['company_domain'] for p in P}))
print(collections.Counter(p['source_list'] for p in P))
pickle.dump(P,open('k_people.pkl','wb'))
