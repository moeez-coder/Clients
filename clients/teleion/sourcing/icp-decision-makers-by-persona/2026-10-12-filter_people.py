import csv,re,collections,os,glob
F="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/a502d029-12th-Oct-Default-view-export-1791823550720.csv"
r=list(csv.DictReader(open(F)))
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
BAD=re.compile(r"\b(retired|former|ex-|emeritus|advis(or|ory)|deputy|interim|aspiring|incoming)\b|^\s*assistant\b|\bassistant (treasurer|cfo|chief)|\bboard (member|treasurer|director)\b|\bpast\b|vice[ -]chair",re.I)
VP=re.compile(r"(?<!vice )(?<!vp )\bpresident\b",re.I)
CAT=[
 (1,'Compliance, Risk & Fraud',re.compile(r"chief compliance officer|chief risk officer|chief risk (&|and) compliance|chief compliance (&|and) risk|\bbsa\b.*officer|bank secrecy.*officer|\baml\b.*officer|bsa/aml officer|\bbsa officer",re.I),'More push back, but higher conversion rate on 30-60 day posts'),
 (2,'AI & Data Governance',re.compile(r"chief information security officer|\bciso\b|chief information officer|\bcio\b|chief model risk officer|chief security (&|and) information officer|\bcsio\b",re.I),'Easy to talk with (CISO/CIO)'),
 (3,'Payments & Finance',re.compile(r"\btreasurer\b|chief financial officer|\bcfo\b|chief accounting officer",re.I),'CFO and Treasurer easiest and most flexible to talk to; Treasurer especially'),
 (4,'Executive Sponsor',None,'Fewer pickups'),
]
def cats(t):
    if BAD.search(t): return []
    out=[]
    for n,name,rx,note in CAT:
        if n==4:
            if re.search(r"\b(ceo|chief executive officer|chief human resources officer|chro|chief people officer)\b|(chair(man|woman|person)?)\b.*(board|directors)|board.*chair|chair of the board|^chair$|\bchairman\b",t,re.I) or (VP.search(t) and not re.search(r"vice|vp\b",t,re.I)): out.append(n)
        elif rx.search(t): out.append(n)
    return out
# signal lookup from my two new files
sig={}
for f in glob.glob('/home/user/Clients/clients/teleion/sourcing/*/2026-10-12-companies.csv'):
    for x in csv.DictReader(open(f)): sig[nd(x['domain'])]=(x['signal_codes'],x['tier'])
base="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/7cb2e220-Teleion_target_accounts_with_signals-2-Default-view-export-1791818754556.csv"
contacted={nd(x['domain']) for x in csv.DictReader(open(base)) if x['has_signal']=='yes'}
dnc=['amazon','starbucks','lyft','becu','gates foundation','gatesfoundation','microsoft','aws']
out=[];drop=collections.Counter()
for x in r:
    t=x['Job Title'] or ''
    c=cats(t)
    if not c: drop['no title match']+=1; continue
    d=nd(x['Company Domain'])
    if d in contacted: drop['contacted signalled account']+=1; continue
    if any(k in x['Company Name'].lower() for k in dnc): drop['DNC']+=1; continue
    n,name,_,note=CAT[c[0]-1]
    s=sig.get(d)
    out.append({'linkedin_url':x['LinkedIn Profile'] or '-','first_name':x['First Name'] or '-','last_name':x['Last Name'] or '-','full_name':x['Full Name'] or '-','job_title':t,'persona_group':name,'also_matches':'; '.join(CAT[i-1][1] for i in c[1:]) or '-','caller_note':note,'company_name':x['Company Name'] or '-','company_domain':d or '-','location':x['Location'] or '-','company_signal_codes':s[0] if s else '-','company_signal_tier':s[1] if s else '-'})
order={'Compliance, Risk & Fraud':1,'AI & Data Governance':2,'Payments & Finance':3,'Executive Sponsor':4}
seen=set();fin=[]
for o in sorted(out,key=lambda o:(o['company_signal_codes']=='-',order[o['persona_group']],o['company_name'])):
    if o['linkedin_url'] in seen: continue
    seen.add(o['linkedin_url']);fin.append(o)
dd='/home/user/Clients/clients/teleion/sourcing/icp-decision-makers-by-persona'
os.makedirs(dd,exist_ok=True)
f=dd+'/2026-10-12-leads.csv'
assert not os.path.exists(f)
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(fin[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(fin)
print(len(r),'->',len(fin),dict(drop))
print(collections.Counter(o['persona_group'] for o in fin))
print('companies',len({o['company_domain'] for o in fin}),'with signal',len({o['company_domain'] for o in fin if o['company_signal_codes']!='-'}))
for g in order:
    print(g,collections.Counter(o['job_title'] for o in fin if o['persona_group']==g).most_common(8))
print('also',collections.Counter(o['also_matches'] for o in fin).most_common(5))
