import json,re,csv,datetime,collections,os,gzip,shutil
d=json.load(open('refined2.json'))
TODAY=datetime.date(2026,10,12)
FIN=r"(bank|credit union|bancorp|bancshares|\bcu\b|fcu|financial|savings)"
SPAC=r"(acquisition corp|spac|pricing of|machine|audio|plant and)"
PAIN={'Compliance, Risk & Fraud':'BSA/AML and compliance load tends to spike through an integration',
 'AI & Data Governance':'keeping systems, data and model governance consistent through a combination is usually the hard part',
 'Payments & Finance':'reconciliation, treasury and payment-rail changes tend to pile up after a deal',
 'Executive Sponsor':'integration usually strains operations and compliance capacity at the same time'}
JPAIN={'Compliance, Risk & Fraud':'Teleion helped a BaaS sponsor bank reach examiner agreement to close 64% of its outstanding regulatory findings within 12 months',
 'AI & Data Governance':'Teleion got a software company\'s Outreach to ISO/IEC 42001 in 4 months with zero findings',
 'Payments & Finance':'Teleion cleared a 3,663-ticket operations backlog for a global tech client and cut resolution time 92%',
 'Executive Sponsor':'Teleion has run enterprise operations for clients from Fortune 10 to nonprofits for 18+ years'}
def art(w): return 'an' if w[:1].lower() in 'aeiou' else 'a'
rows=[]
for p,jobs,news in d:
    g=p['persona_group'];n=p['company_name']
    cands=[]
    if 'M&A' in news:
        s,title,url,dt,hl=news['M&A']
        ok=re.search(FIN,title+' '+n,re.I) and not re.search(SPAC,title,re.I)
        cands.append(('M&A deal','high' if ok else 'low',title,dt,url,
          f"Saw the news: \"{title[:110]}\" ({dt}). {PAIN[g][0].upper()+PAIN[g][1:]} — is that on your radar?"))
    if 'Regulatory' in news:
        s,title,url,dt,hl=news['Regulatory']
        cands.append(('Regulatory action','medium',title,dt,url,f"I saw the regulatory item: \"{title[:110]}\" ({dt}). We help banks close findings with examiners — how is remediation going?"))
    if jobs:
        u,(t,dt)=jobs[0];days=(TODAY-datetime.date.fromisoformat(dt)).days
        conf='high' if days<=60 else 'medium'
        cands.append(('Open role in your area',conf,t,dt,u,f"I noticed {n} is hiring {art(t)} {t} (posted {dt}, {days} days ago). {JPAIN[g]}. Is that role under you?"))
    if 'AI' in news:
        s,title,url,dt,hl=news['AI']
        cands.append(('AI announcement','medium' if g=='AI & Data Governance' else 'low',title,dt,url,f"Saw \"{title[:110]}\" ({dt}) — who's owning governance and risk review on that?"))
    rank={'high':0,'medium':1,'low':2}
    cands=[c for c in cands if re.match(r'\d{4}-\d\d-\d\d',c[3] or '')]
    if n.strip()=='-': cands=[]
    cands.sort(key=lambda c:(rank[c[1]],-int(c[3].replace('-',''))))
    b=cands[0] if cands else None
    rows.append({'linkedin_url':p['linkedin_url'],'full_name':p['full_name'],'job_title':p['job_title'],'persona_group':g,'company_name':n,'company_domain':p['company_domain'],
      'best_signal_type':b[0] if b else '-','confidence':b[1] if b else 'none','signal_detail':b[2] if b else '-','signal_date':b[3] if b else '-','signal_url':b[4] if b else '-','call_opener':b[5] if b else '-',
      'other_signals':'; '.join(f"{c[0]}: {c[2][:60]} ({c[3]})" for c in cands[1:]) or '-'})
o={'high':0,'medium':1,'low':2,'none':3}
rows.sort(key=lambda r:(o[r['confidence']],r['persona_group'],r['company_name']))
dd='/home/user/Clients/clients/teleion/sourcing/icp-decision-makers-by-persona'
f=dd+'/2026-10-12-leads-2.csv'
assert not os.path.exists(f)
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(rows[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(rows)
print(len(rows),collections.Counter(r['confidence'] for r in rows))
print(collections.Counter((r['persona_group'][:8],r['confidence']) for r in rows))
print(collections.Counter(r['best_signal_type'] for r in rows))
for r in [x for x in rows if x['confidence']=='high'][:8]: print('-',r['company_name'],'|',r['call_opener'][:230])
