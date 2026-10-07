import json,glob,csv,re,collections
from cc_rank import score
S='/home/user/Clients/clients/vntana/sourcing/'
OUT=S+'founders-ceos-industrial-manufacturers/'
import os; os.makedirs(OUT,exist_ok=True)
A=json.load(open('accounts.json'))['accounts']; norm=lambda u:(u or '').lower().strip().rstrip('/')
byurl={norm(a['linkedin_url']):k for k,a in A.items() if a['linkedin_url']}
INC={'US','CA','GB','IE','AU','NZ','DE'}
cand=collections.defaultdict(dict)
for folder in ('pA','pB'):
    for f in glob.glob(folder+'/*.jsonl'):
        for l in open(f):
            x=json.loads(l)
            if '_error' in x: continue
            p=x['person']
            for j in x['jobs']:
                cu=norm(j.get('company_linkedin_url'))
                if cu not in byurl: continue
                s,tier=score(j.get('job_title'))
                if not s: continue
                fn_=(p.get('first_name') or '').strip(); ln_=(p.get('last_name') or '').strip()
                if not fn_ or not ln_ or re.search(r'[&0-9@]',fn_+ln_): continue
                loc=(p.get('location') or {}).get('country_code') or ''
                eff=s+(10 if loc in INC else 0)
                key=p['linkedin_url']
                if key not in cand[cu] or eff>cand[cu][key]['eff']:
                    cand[cu][key]={'p':p,'title':j.get('job_title'),'s':s,'tier':tier,'eff':eff,'loc':loc,'src':'Blitz /v2/search/people ('+('in-country pass: US/CA/GB/IE/AU/NZ/DE' if folder=='pA' else 'worldwide pass')+')'}
# overlaps
def people(f,col): 
    try: return {norm(r[col]) for r in csv.DictReader(open(S+f,encoding='utf8',errors='ignore')) if r.get(col)}
    except Exception: return set()
dn=people('dealer-network-manufacturers/2026-10-07-leads.csv','linkedin_url')
earlier=set()
for f in glob.glob(S+'open-check-combined-personas/*leads*.csv'):
    for r in csv.DictReader(open(f,encoding='utf8',errors='ignore')): earlier.add(norm(r.get('linkedin_url')))
NAMED=['caterpillar','john deere','deere &','komatsu','volvo construction','terex','cnh','hitachi construction','liebherr','jcb','kubota','agco','sandvik','epiroc','oshkosh','paccar','parker hannifin','parker-hannifin','eaton','emerson','flowserve','atlas copco','ingersoll rand','danfoss','bosch rexroth']
def named(n): 
    n=(n or '').lower(); return next((t for t in NAMED if t in n),'')
sel=[]
for cu,d in cand.items():
    a=A[byurl[cu]]
    vs=sorted(d.values(),key=lambda v:(-v['eff'],v['p']['full_name'] or ''))
    take=vs[:1]
    if a['employees']>=5000:
        for v in vs[1:]:
            if v['s']>=70 and v['tier'] not in ('1_founder_ceo_owner','5_chair') and v['p']['linkedin_url']!=take[0]['p']['linkedin_url']: take.append(v); break
    for r,v in enumerate(take,1): sel.append((cu,a,v,r))
print('accounts with a lead',len({cu for cu,*_ in sel}),'of',len(byurl),'| leads',len(sel))
print(collections.Counter(v['tier'] for *_,v,_ in sel)); print('in-country',sum(1 for *_,v,_ in sel if v['loc'] in INC),'outside',sum(1 for *_,v,_ in sel if v['loc'] not in INC))
# hand-pick score
def hp(a,v): return a['pts']*20+min(a['employees'],10000)/1000+v['s']/10
rows=[]
for cu,a,v,r in sel:
    p=v['p']; rows.append((hp(a,v),cu,a,v,r))
rows.sort(key=lambda x:-x[0])
top=set(); n=0
for sc,cu,a,v,r in rows:
    if r==1:
        n+=1; 
        if n<=500: top.add(cu)
cols=['linkedin_url','first_name','last_name','title','headline','person_country','company_name','company_linkedin_url','company_domain','company_employees','company_country','company_industry','account_sources','account_points','title_tier','title_score','geo_scope','rank_in_company','shortlist_500','verify_flag','also_in_dealer_network_leads','also_in_earlier_repo_leads','named_accounts_overlap','source']
def v_(x): return x if x not in (None,'',[]) else '-'
seen=set(); wrote=0
with open(OUT+'2026-10-07-leads.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(cols)
    for sc,cu,a,v,r in rows:
        p=v['p']; u=norm(p['linkedin_url'])
        if u in seen: continue
        seen.add(u); wrote+=1
        w.writerow([p['linkedin_url'],v_(p['first_name']),v_(p['last_name']),v_(v['title']),v_(p.get('headline')),v_(v['loc']),a['name'],a['linkedin_url'],v_(a['domain']),a['employees'] or '-',v_(a['country']),v_(a['industry']),'; '.join(sorted(set(a['src']))),a['pts'],v['tier'],v['s'],'target_country' if v['loc'] in INC else 'outside_target_countries',r,'yes' if (cu in top and r==1) else '-',('owner title at 1,000+ employee company: check not a dealer/reseller owner' if (re.search(r'\b(owner|proprietor)\b',(v['title'] or '').lower()) and not re.search(r'(ceo|chief executive|founder|president)',(v['title'] or '').lower()) and (a['employees'] or 0)>=1000) else '-'),'yes' if u in dn else '-','yes' if u in earlier else '-',v_(named(a['name'])),v['src']])
print('leads written',wrote)
with open(OUT+'2026-10-07-companies.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['company_linkedin_url','name','domain','employees','country','industry','vertical','account_sources','account_points','has_lead','named_accounts_overlap'])
    for k,a in sorted(A.items(),key=lambda kv:(-kv[1]['pts'],-kv[1]['employees'])):
        has='yes' if (a['linkedin_url'] and norm(a['linkedin_url']) in cand) else '-'
        w.writerow([v_(a['linkedin_url']),a['name'],v_(a['domain']),a['employees'] or '-',v_(a['country']),v_(a['industry']),v_(a['vertical']),'; '.join(sorted(set(a['src']))),a['pts'],has,v_(named(a['name']))])
L=list(csv.DictReader(open(OUT+'2026-10-07-leads.csv')))
print('shortlist',sum(1 for l in L if l['shortlist_500']=='yes'),'| dealer-network overlap',sum(1 for l in L if l['also_in_dealer_network_leads']=='yes'),'| earlier-repo overlap',sum(1 for l in L if l['also_in_earlier_repo_leads']=='yes'),'| named-accounts',sum(1 for l in L if l['named_accounts_overlap']!='-'))
print(collections.Counter(l['title_tier'] for l in L if l['shortlist_500']=='yes')); print(collections.Counter(l['geo_scope'] for l in L))
for l in L[:10]: print(l['first_name'],l['last_name'],'|',l['title'],'|',l['company_name'],'|',l['account_points'])
