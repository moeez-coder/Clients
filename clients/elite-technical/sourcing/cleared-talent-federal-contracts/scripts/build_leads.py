import json,re,csv,sys
S=sys.argv[1]; OUTDIR=sys.argv[2]
P='/root/.claude/projects/-home-user-Clients/50c281f3-20cb-5a4f-886e-65be03c1e1fc/tool-results/'
kept=json.load(open(S+'/kept.json'))
blitz=json.load(open(S+'/blitz_people_raw.json'))['results']
clay1=json.load(open(S+'/clay_batch1_4.json'))
clayf=[json.loads(open(P+f).read()) for f in ['toolu_01TrPBCN5E3A3DrpPxwwaLqS.txt','mcp-Clay-search-contacts-1793298372205.txt']]
clay_rev=dict(clay1['company_revenue'])
for d in clayf: clay_rev.update({k:v.get('annual_revenue') for k,v in d['companies'].items()})
AGENCY={'Animal and Plant Health Inspection Service':'USDA APHIS','Department of State':'State Department','Department of Veterans Affairs':'VA','Environmental Protection Agency':'EPA','Federal Emergency Management Agency':'FEMA','Federal Railroad Administration':'FRA','Food and Drug Administration':'FDA','Health Resources and Services Administration':'HRSA','National Aeronautics and Space Administration':'NASA','National Institutes of Health':'NIH','National Oceanic and Atmospheric Administration':'NOAA','National Science Foundation':'NSF','Transportation Security Administration':'TSA','U.S. Customs and Border Protection':'CBP','U.S. Geological Survey':'USGS','Office of Procurement Operations':'DHS','Office of the Assistant Secretary for Administration and Management':'Department of Labor','Office of the Assistant Secretary for Financial Resources':'HHS'}
PARENT_SHORT={'Department of the Interior':'Department of the Interior','Department of the Treasury':'Treasury'}
# company-level decisions (revenue cross-check Blitz vs Clay + entity checks), see query.md
EXCLUDE={'https://www.linkedin.com/company/institute-for-defense-analyses':'Clay revenue 1B-10B (outside $100M-$1B)',
 'https://www.linkedin.com/company/ilc-dover':'Clay revenue 1B-10B; subsidiary of Ingersoll Rand',
 'https://www.linkedin.com/company/goldbelt-c6-llc':'Clay revenue 25M-75M (outside range)',
 'https://www.linkedin.com/company/systems-plus-solutions':'entity mismatch: LinkedIn page is Systems Plus (Dallas/Pune), award recipient is Systems Plus, Inc. (Rockville MD)',
 'https://www.linkedin.com/company/wsp-usa-solutions-inc':'subsidiary of WSP Global (revenue well above $1B)',
 'https://www.linkedin.com/company/leidos-biomedical-research-inc.':'subsidiary of Leidos (revenue well above $1B)',
 'https://www.linkedin.com/company/manhattan-associates':'public company with revenue above $1B (FY2024 ~ $1.04B)'}
def rev_status(u):
  c=clay_rev.get(u)
  if c in ('200M-500M','500M-1B'): return 'confirmed','Blitz $100M-$1B; Clay '+c
  if c=='75M-200M': return 'overlap-verify','Blitz $100M-$1B; Clay 75M-200M (straddles $100M floor)'
  return 'blitz-only','Blitz $100M-$1B; Clay '+str(c)
def nurl(u): 
  u=(u or '').strip().split('?')[0].rstrip('/'); u=re.sub(r'^https?://([a-z]+\.)?linkedin\.com','https://www.linkedin.com',u); return u.lower()
def tclass(t):
  tl=(t or '').lower()
  if re.search(r'assistant|intern|coordinator|sourcer|recruiter\b|member|consultant|partnerships|human resources',tl): return None
  if re.search(r'talent acquisition|recruiting|contingent|workforce solutions',tl):
    return 2 if re.search(r'director|head|vp|vice president|manager|chief',tl) else None
  if re.search(r'\b(cio|cto|ciso|chief)\b',tl) and not re.search(r'\b(vp|vice president|director)\b',tl): return 3
  if re.search(r'director|\bvp\b|vice president|\bsvp\b|evp|head of',tl) and re.search(r'engineer|it\b|information|technolog|technical|software|infrastructure|operations|cyber|security|data|cio|cto',tl): return 1
  if re.search(r'\b(cio|cto)\b|chief (information|technology)',tl): return 3
  return None
rows={}
for x in kept:
  u=x['match']['linkedin_url']
  if u in EXCLUDE: continue
  a=x['award']
  ag=AGENCY.get(a['Awarding Sub Agency']) or PARENT_SHORT.get(a['Awarding Agency'],a['Awarding Agency'])
  if a['Awarding Sub Agency']=='Departmental Offices': ag=PARENT_SHORT.get(a['Awarding Agency'],a['Awarding Agency'])
  rs,rnote=rev_status(u)
  comp=dict(company_name=x['match']['name'],company_linkedin_url=u,company_domain=x['match'].get('domain') or '-',hq_state=x['match']['hq'].get('state') or '-',geo_tier=a['_tier'],revenue_status=rs,revenue_evidence=rnote,
    award_id=a['Award ID'],award_date_signed=x.get('date_signed') or '-',award_type=x.get('award_type') or '-',award_amount_usd=round(a['Award Amount']),awarding_agency=a['Awarding Agency'],awarding_sub_agency=a['Awarding Sub Agency'],award_description=(a['Description'] or '').strip()[:200],
    award_url='https://www.usaspending.gov/award/'+a['generated_internal_id'],contract_or_agency=ag)
  def add(url,first,last,full,title,loc,src):
    k=nurl(url)
    if not k or '/in/' not in k: return
    c=tclass(title)
    if c is None: return
    r=rows.get(k)
    if r: r['source']= r['source'] if src in r['source'] else r['source']+'+'+src; return
    rows[k]=dict(linkedin_url=k,first_name=first or '-',last_name=last or '-',full_name=full,job_title=re.sub(r'\s+',' ',title),title_priority=c,person_location=loc or '-',source=src,**comp)
  for r in (blitz.get(u) or {}).get('results') or []:
    p=r['person']; e=(p.get('experiences') or [{}])[0]; l=p.get('location') or {}
    add(p.get('linkedin_url'),p.get('first_name'),p.get('last_name'),p.get('full_name'),e.get('job_title'),', '.join(filter(None,[l.get('city'),l.get('state_code')])),'blitz')
  cl=[c for c in clay1['contacts'] if c[5]==u]
  for d in clayf: cl+= [[c['name'],c['url'],c['latest_experience_company'],c['latest_experience_title'],c['location_name'],c['companyIdentifier']] for c in d['contacts'] if c['companyIdentifier']==u]
  for name,url,company,title,loc,ci in cl:
    if company.split()[0].lower() not in x['match']['name'].lower() and company.lower() not in x['match']['name'].lower(): continue
    parts=name.split(); add(url,parts[0],' '.join(parts[1:]),name,title,loc,'clay')
L=list(rows.values())
# clean first names (strip credentials) for {first_name}
for r in L:
  r['first_name']=re.sub(r'[^A-Za-z\'\-]','',r['first_name'].split()[0]) if r['first_name']!='-' else '-'
# wave assignment: one contact per company per wave (client rule: no identical sequences to multiple contacts at one company at once)
from collections import defaultdict
by=defaultdict(list)
for r in L: by[r['company_linkedin_url']].append(r)
for u,rs in by.items():
  rs.sort(key=lambda r:(r['title_priority'],0 if '+' in r['source'] else 1,r['full_name']))
  for i,r in enumerate(rs): r['company_wave_rank']=i+1
cols=['linkedin_url','first_name','last_name','full_name','job_title','title_priority','person_location','company_name','company_linkedin_url','company_domain','hq_state','geo_tier','revenue_status','revenue_evidence','contract_or_agency','award_id','award_date_signed','award_type','award_amount_usd','awarding_agency','awarding_sub_agency','award_description','award_url','company_wave_rank','source']
L.sort(key=lambda r:(r['company_wave_rank'],r['geo_tier']!='DC Metro',r['company_name']))
with open(OUTDIR+'/2026-10-29-leads.csv','w',newline='') as f:
  w=csv.DictWriter(f,cols); w.writeheader(); [w.writerow(r) for r in L]
# companies file
C={}
for x in kept:
  u=x['match']['linkedin_url']; a=x['award']
  C[u]=dict(company_linkedin_url=u,company_name=x['match']['name'],usaspending_recipient=a['Recipient Name'],recipient_uei=a['Recipient UEI'] or '-',company_domain=x['match'].get('domain') or '-',hq_state=x['match']['hq'].get('state') or '-',recipient_state=a['_state'],geo_tier=a['_tier'],blitz_revenue=x['match'].get('revenue_range'),clay_revenue=clay_rev.get(u) or '-',decision='EXCLUDED: '+EXCLUDE[u] if u in EXCLUDE else 'included ('+rev_status(u)[0]+')',award_id=a['Award ID'],award_date_signed=x.get('date_signed') or '-',award_amount_usd=round(a['Award Amount']),awarding_sub_agency=a['Awarding Sub Agency'],award_url='https://www.usaspending.gov/award/'+a['generated_internal_id'],contacts_found=len(by.get(u,[])))
with open(OUTDIR+'/2026-10-29-companies.csv','w',newline='') as f:
  w=csv.DictWriter(f,list(next(iter(C.values())).keys())); w.writeheader(); [w.writerow(r) for r in sorted(C.values(),key=lambda r:(r['decision'],r['company_name']))]
import collections
print('leads',len(L),'companies w/ leads',len(by)); print(collections.Counter(r['title_priority'] for r in L)); print(collections.Counter((r['revenue_status']) for r in L))
for u,rs in sorted(by.items(),key=lambda kv:kv[1][0]['company_name']): print(f"{rs[0]['company_name'][:28]:28} {rs[0]['revenue_status']:15} {len(rs)} | "+' ; '.join(f"P{r['title_priority']} {r['job_title'][:35]}" for r in rs[:4]))
