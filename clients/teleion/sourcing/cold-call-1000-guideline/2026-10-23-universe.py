import csv,re,collections,pickle
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
base="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/7cb2e220-Teleion_target_accounts_with_signals-2-Default-view-export-1791818754556.csv"
REG=re.compile(r'(federal reserve|finra|securities and exchange|consumer financial protection|\bfdic\b|comptroller of the currency|ncua)',re.I)
dnc=['amazon','starbucks','lyft','becu','gates foundation','gatesfoundation','microsoft','aws','twitch']
U={}
for x in csv.DictReader(open(base)):
    if x['has_signal']=='yes': continue
    e=int(x['employees']);r=x['revenue_range']
    if e<201 or e>10000: continue
    if r: 
        if int(r.split('-')[0])<20000000: continue
        rs,rn='confirmed','revenue range '+r+' (account export)'
    elif e>=1000: rs,rn='inferred','no revenue figure; inferred over $20M from %d employees'%e
    else: continue
    if REG.search(x['company_name']) or any(k in x['company_name'].lower() for k in dnc): continue
    U[nd(x['domain'])]=dict(name=x['company_name'],li=x['linkedin_url'],emp=e,rs=rs,rn=rn,seg=x['segment'])
for x in csv.DictReader(open('/home/user/Clients/clients/teleion/sourcing/all-icps-job-signals-expansion/2026-10-12-companies.csv')):
    d=nd(x['domain'])
    if d in U or not x['employees'].isdigit(): continue
    e=int(x['employees'])
    if e<1000 or e>10000: continue
    if REG.search(x['company_name']) or any(k in x['company_name'].lower() for k in dnc): continue
    U[d]=dict(name=x['company_name'],li=x['linkedin_url'],emp=e,rs='inferred',rn='no revenue figure; inferred over $20M from %d employees'%e,seg=x['segment'])
print(len(U),collections.Counter(v['rs'] for v in U.values()))
pickle.dump(U,open('m_univ.pkl','wb'))
