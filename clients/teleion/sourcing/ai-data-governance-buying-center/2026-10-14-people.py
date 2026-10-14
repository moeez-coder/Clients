import csv,re,collections,pickle
csv.field_size_limit(10**8)
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
FA="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/a502d029-12th-Oct-Default-view-export-1791823550720.csv"
FB="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/a87ac85c-List-1-Default-view-export-1791825335377.csv"
base="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/7cb2e220-Teleion_target_accounts_with_signals-2-Default-view-export-1791818754556.csv"
BASE={nd(x['domain']):x for x in csv.DictReader(open(base))}
contacted={d for d,x in BASE.items() if x['has_signal']=='yes'}
EXP={nd(x['domain']):x for x in csv.DictReader(open('/home/user/Clients/clients/teleion/sourcing/all-icps-job-signals-expansion/2026-10-12-companies.csv'))}
dnc=['amazon','starbucks','lyft','becu','gates foundation','gatesfoundation','microsoft','aws']
BAD=re.compile(r"\b(retired|former|ex-|emeritus|advis(or|ory)|interim|aspiring|incoming|intern|associate director|assistant|avp|ceo|chief executive|coo|chief operating|sales|marketing|recruit\w*|talent|account (executive|manager|director)|customer success|business development|partner(s|ship)|alliances|legal|counsel|human resources|finance|financial|procurement|real estate|facilities|credit|lending|loan|mortgage|audit|compliance|risk)\b",re.I)
SEN=re.compile(r"(\bvice president\b|\bvp\b|\bdirector\b|\bhead of\b|\bchief\b|\bcio\b|\bciso\b|\bcdo\b|\bcaio\b|\bsvp\b|\bevp\b)",re.I)
FUN=[
 ('Chief AI / Head of AI',re.compile(r"(chief (ai|artificial intelligence|a\.i\.)( |,|&|$)|\bcaio\b|head of (ai|a\.i\.|artificial intelligence|generative ai|machine learning|ml|data science)|(vice president|vp|svp|evp|director|head)\b[^|]{0,40}\b(ai|artificial intelligence|generative ai|machine learning|ml|data science|applied science)\b)",re.I)),
 ('CISO / Security',re.compile(r"(chief information security officer|\bciso\b|chief security officer|(vice president|vp|svp|evp|director|head)\b[^|]{0,40}\b(information security|cyber ?security|security|infosec)\b)",re.I)),
 ('Chief Data Officer / Data',re.compile(r"(chief data officer|\bcdo\b|chief data (and|&) analytics|(vice president|vp|svp|evp|director|head)\b[^|]{0,40}\b(data|analytics|data governance)\b)",re.I)),
 ('CIO / IT',re.compile(r"(chief information officer|\bcio\b|(vice president|vp|svp|evp|director|head)\b[^|]{0,40}\b(information technology|\bit\b|technology)\b)",re.I)),
 ('Infrastructure',re.compile(r"(director|vice president|vp|svp|head)\b[^|]{0,40}\binfrastructure\b|infrastructure[^|]{0,30}\b(director|vice president|vp|head)\b",re.I)),
]
people=[];drop=collections.Counter()
def handle(x,t,d,name,srcname,emp):
    if not emp or emp>1000: drop['company >1000 or unknown headcount']+=1;return
    if BAD.search(t): drop['excluded title']+=1;return
    if not SEN.search(t): drop['not VP/Director+']+=1;return
    g=[n for n,rx in FUN if rx.search(t)]
    if not g: drop['not buying-center']+=1;return
    if d in contacted: drop['contacted']+=1;return
    if any(k in (name or '').lower() for k in dnc): drop['DNC']+=1;return
    people.append({'linkedin_url':x['LinkedIn Profile'] or '-','first_name':x['First Name'] or '-','last_name':x['Last Name'] or '-','full_name':x['Full Name'] or '-','job_title':t,'function':g[0],'also_matches':'; '.join(g[1:]) or '-','company_name':name or '-','company_domain':d,'location':x['Location'] or '-','source_list':srcname,'employees':emp})
for x in csv.DictReader(open(FA)):
    d=nd(x['Company Domain']);b=BASE.get(d)
    handle(x,x['Job Title'] or '',d,x['Company Name'],'Persona people list (12th-Oct export)',int(b['employees']) if b else None)
for x in csv.DictReader(open(FB)):
    d=nd(x['Domain'] or x['Company Domain']);e=EXP.get(d)
    handle(x,x['Job Title'] or '',d,x['Company Name'] or (e['company_name'] if e else ''),'Signal-account people list (List-1 export)',int(e['employees']) if e and e['employees'].isdigit() else None)
seen=set();P=[]
for p in people:
    if p['linkedin_url'] in seen: continue
    seen.add(p['linkedin_url']);P.append(p)
print(len(P),dict(drop))
print(collections.Counter(p['function'] for p in P),len({p['company_domain'] for p in P}))
print(collections.Counter(p['job_title'] for p in P).most_common(12))
pickle.dump(P,open('ai2_people.pkl','wb'))
