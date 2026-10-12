import csv,json,re,collections
pool={x['linkedin_url']:x for x in csv.DictReader(open('pool.csv'))}
P3=re.compile(r"\b(bsa|aml|bank secrecy|anti[- ]money|money laundering|kyc|know your customer|ofac|sanctions|financial crimes?|cdd|edd|transaction monitoring)\b|\bcft\b",re.I)
P5=re.compile(r"(model (risk|validation|governance)|ai governance|responsible ai|ai[ /-]*(innovation )?risk|(artificial intelligence|\bai\b|machine learning).*(risk|governance|compliance|control)|(risk|governance|compliance|control).*(artificial intelligence|\bai\b))",re.I)
P2=re.compile(r"(baas|banking[- ]as[- ]a[- ]service|embedded (finance|banking|payments|lending)|fintech (program|partner|relationship|onboarding|oversight)|(sponsor )?bank partner(s|ship|ships)?|bank[- ]fintech|program (manager|analyst|lead).*(fintech|baas|sponsor bank)|(fintech|baas|sponsor bank).*program (manager|analyst|lead))",re.I)
res=[]
for l in open('jobs_raw.jsonl'):
    r=json.loads(l);x=pool[r['linkedin_url']]
    if x['company_name'].startswith('Federal Reserve Bank'): continue
    h={'P2':{},'P3':{},'P5':{}}
    for j in r['jobs'] or []:
        t=j['title'] or ''
        for c,rx in (('P2',P2),('P3',P3),('P5',P5)):
            if rx.search(t) and not (c=='P2' and re.search(r'engineer|developer',t,re.I)): h[c][j['url']]=(t,j['date_posted'][:10])
    # P3 needs 2+ roles
    if len(h['P3'])<2: h['P3']={}
    codes=[c for c in ('P2','P3','P5') if h[c]]
    pts={'P2':30,'P3':20,'P5':10}
    score=sum(pts[c] for c in codes)
    names={'P2':'Bank-fintech partnership hiring (proxy)','P3':'Hiring BSA/AML/KYC analysts','P5':'AI / model-risk role posted'}
    notes=[]
    for c in codes:
        items=sorted(h[c].items(),key=lambda i:-int(i[1][1].replace('-','')))
        lst='; '.join(f"{t} ({d})" for u,(t,d) in items[:3])
        if c=='P3': notes.append(f"[P3] {len(items)} open BSA/AML/KYC roles in last 90 days, latest {items[0][1][1]}: {lst}. Example: {items[0][0]}")
        elif c=='P5': notes.append(f"[P5] {len(items)} AI/model-risk role(s): {lst}. {items[0][0]}")
        else: notes.append(f"[P2] Partnership-type role open (hiring proxy only, not an announced partnership): {lst}. {items[0][0]}")
    tier='A' if score>=35 else 'B' if score>=20 else 'C'
    row=dict(x)
    row.update(tier=tier if codes else 'C',score=score,has_signal='yes' if codes else 'no',
      signals_triggers=' + '.join(names[c] for c in codes) or '-',signal_codes=','.join(codes) or '-',
      pilot_tag='-',notes=' || '.join(notes) or 'No signal found')
    for k,v in row.items():
        if v=='' : row[k]='-'
    res.append(row)
res.sort(key=lambda r:(-int(r['score']),-int(r['employees'])))
import os
d='/home/user/Clients/clients/teleion/sourcing/fs-compliance-ops-signals-recheck'
os.makedirs(d,exist_ok=True)
f=d+'/2026-10-12-companies.csv'
assert not os.path.exists(f)
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(res[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(res)
s=[r for r in res if r['has_signal']=='yes']
print(len(res),len(s),collections.Counter(r['signal_codes'] for r in s),collections.Counter(r['tier'] for r in s))
for r in s[:12]: print(r['company_name'],r['employees'],r['score'],r['signal_codes'])
