import json,glob,csv,re,collections
Q=list(csv.DictReader(open('/home/user/Clients/clients/vntana/sourcing/dealer-network-manufacturers/2026-10-07-companies-qualified.csv')))
norm=lambda u:(u or '').lower().strip().rstrip('/')
comp={norm(r['company_linkedin_url']):r for r in Q if r['tier'][:2] in('Q1','Q2','Q3') and r['company_linkedin_url']!='-'}
WRONG=re.compile(r'\b(analytics?|analyst|compliance|procurement|purchasing|vmo|finance|financial|human resources|\bhr\b|recruit\w*|legal|counsel|\bit\b|information technology|engineer\w*|supply chain|logistics|quality|safety|accounting|payroll|facilit\w+|photograph\w*|videograph\w*|graphic designer|designer)\b',re.I)
PERSONA=re.compile(r'(channel marketing|dealer marketing|dealer development|co-?op(erative)? marketing|distributor marketing|dealer programs?|dealer network|dealer relations|partner marketing|rep program|channel programs?|dealer experience|dealer support)',re.I)
MARCOM=re.compile(r'(marketing communications?|marcom|brand (manager|director|marketing|lead|head)|head of brand|director of brand|corporate communications|marketing (and|&) communications)',re.I)
LEAD=re.compile(r'(chief marketing|\bcmo\b|vp,? (of )?marketing|vice president,? (of )?marketing|(director|head|manager|lead)(,| of| -)? (global |regional |north america(n)? |national |senior )?marketing|marketing (director|manager|lead|head)|digital marketing|content marketing|product marketing|\bmarketing\b)',re.I)
def score(t):
    t=t or ''; s=0; fit=None
    if WRONG.search(t) and not PERSONA.search(t): return 0,None
    if PERSONA.search(t):
        s=100; fit='A_persona_title'
        if re.search(r'\bsales\b',t,re.I) and not re.search(r'marketing|development|programs?|relations|experience|support',t,re.I): s=45
    elif MARCOM.search(t): s=80; fit='B_marcom_brand'
    elif LEAD.search(t): s=60; fit='C_marketing_lead'
    else: return 0,None
    if re.search(r'(director|head of|vice president|\bvp\b|chief|cmo)',t,re.I): s+=10
    elif re.search(r'senior manager|sr\.? manager|\bmanager\b|\blead\b',t,re.I): s+=5
    if re.search(r'(product marketing|field marketing)',t,re.I): s-=10
    if re.search(r'(demand gen|performance|seo|social media|lifecycle|crm|email marketing|events?\b|trade ?show)',t,re.I): s-=15
    return s,fit
people={}
for src,pat in (('Blitz /v2/search/people (persona-title pass, US/CA/GB/IE/AU/NZ)','people/*.jsonl'),('Blitz /v2/search/people (marketing-function pass, US/CA/GB/IE/AU/NZ)','people2/*.jsonl'),('Blitz /v2/search/people (marketing-function pass, worldwide; only companies with no in-country lead)','people3/*.jsonl')):
    for f in glob.glob(pat):
        for l in open(f):
            x=json.loads(l)
            if '_error' in x: continue
            p=x['person']
            for j in x['jobs']:
                cu=norm(j.get('company_linkedin_url'))
                if cu not in comp: continue
                s,fit=score(j.get('job_title'))
                if s<60: continue
                key=(p['linkedin_url'],cu)
                if key not in people or s>people[key]['score']:
                    people[key]={'p':p,'job':j,'score':s,'fit':fit,'src':src}
by=collections.defaultdict(list)
for (pu,cu),v in people.items(): by[cu].append(v)
leads=[]
for cu,vs in by.items():
    vs.sort(key=lambda v:(-v['score'],v['p']['full_name'] or ''))
    for rank,v in enumerate(vs[:2],1): leads.append((cu,rank,v))
print('companies with >=1 lead',len(by),'of',len(comp),'| leads',len(leads),'unique people',len({v['p']['linkedin_url'] for _,_,v in leads}))
print(collections.Counter(v['fit'] for _,_,v in leads)); print(collections.Counter(comp[cu]['tier'][:2] for cu,_,_ in leads))
D='/home/user/Clients/clients/vntana/sourcing/dealer-network-manufacturers/'
def v_(x): return x if x not in (None,'',[]) else '-'
cols=['linkedin_url','first_name','last_name','title','headline','person_country','person_city','company_name','company_linkedin_url','company_domain','company_tier','company_vertical','company_country','company_employees','dealer_count_stated','company_evidence_url','geo_scope','persona_fit','title_score','rank_in_company','source']
with open(D+'2026-10-07-leads.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(cols); seen=set()
    for cu,rank,v in sorted(leads,key=lambda t:(comp[t[0]]['tier'],-t[2]['score'])):
        p=v['p']; c=comp[cu]; loc=p.get('location') or {}
        if p['linkedin_url'] in seen: continue
        seen.add(p['linkedin_url'])
        w.writerow([p['linkedin_url'],v_(p['first_name']),v_(p['last_name']),v_(v['job'].get('job_title')),v_(p.get('headline')),v_(loc.get('country_code')),v_(loc.get('city')),c['name'],c['company_linkedin_url'],c['domain'],c['tier'],c['vertical'],c['country'],c['employees'],c['dealer_count_stated'],c['evidence_url'],('target_country' if (loc.get('country_code') or '') in ('US','CA','GB','IE','AU','NZ') else 'outside_target_countries'),v['fit'],v['score'],rank,v['src']])
    print('rows written',len(seen))
import random; random.seed(4)
for cu,rank,v in random.sample(leads,14): print(comp[cu]['name'],'|',v['job'].get('job_title'),'|',v['fit'],v['score'])
