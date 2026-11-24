import json,re,csv,sys,collections
S=sys.argv[1]; OUT=sys.argv[2]
P='/root/.claude/projects/-home-user-Clients/50c281f3-20cb-5a4f-886e-65be03c1e1fc/tool-results/'
sel=json.load(open(S+'/wide_sel.json'))
blitz={}; [blitz.update(json.load(open(S+f))['results']) for f in ['/blitz_people_raw.json','/blitz_people_raw2.json']]
clay_rev={}; clay_contacts=[]
for f in ['/clay_batch1_4.json','/clay_batch6.json']:
  d=json.load(open(S+f)); clay_rev.update(d['company_revenue']); clay_contacts+=d['contacts']
for f in ['toolu_01TrPBCN5E3A3DrpPxwwaLqS.txt','mcp-Clay-search-contacts-1793298372205.txt','mcp-Clay-search-contacts-1793353502290.txt']:
  d=json.loads(open(P+f).read())
  clay_rev.update({k:v.get('annual_revenue') for k,v in d['companies'].items()})
  clay_contacts+=[[c['name'],c['url'],c['latest_experience_company'],c['latest_experience_title'],c['location_name'],c['companyIdentifier']] for c in d['contacts']]
AG={'Animal and Plant Health Inspection Service':'USDA APHIS','Department of State':'State Department','Department of Veterans Affairs':'VA','Environmental Protection Agency':'EPA','Federal Emergency Management Agency':'FEMA','Federal Railroad Administration':'FRA','Food and Drug Administration':'FDA','Health Resources and Services Administration':'HRSA','National Aeronautics and Space Administration':'NASA','National Institutes of Health':'NIH','National Oceanic and Atmospheric Administration':'NOAA','National Science Foundation':'NSF','Transportation Security Administration':'TSA','U.S. Customs and Border Protection':'CBP','U.S. Geological Survey':'USGS','Office of Procurement Operations':'DHS','Office of the Assistant Secretary for Administration and Management':'Department of Labor','Office of the Assistant Secretary for Financial Resources':'HHS','Public Buildings Service':'GSA','Federal Bureau of Investigation':'FBI','Centers for Medicare and Medicaid Services':'CMS','Federal Highway Administration':'FHWA','U.S. Immigration and Customs Enforcement':'ICE','National Institute of Standards and Technology':'NIST','Centers for Disease Control and Prevention':'CDC',
 'ARMY':'Army','AIR FORCE':'Air Force','NAVY':'Navy','DEFENSE LOGISTICS AGENCY':'DLA','MISSILE DEFENSE AGENCY':'Missile Defense Agency','DEFENSE INFORMATION SYSTEMS AGENCY':'DISA','SPACE FORCE':'Space Force'}
PARENT={'Department of the Interior':'Department of the Interior','Department of the Treasury':'Treasury','Department of Homeland Security':'DHS','Department of Health and Human Services':'HHS','Department of Defense':'DoD'}
EXCLUDE={'https://www.linkedin.com/company/institute-for-defense-analyses':'Clay revenue 1B-10B','https://www.linkedin.com/company/ilc-dover':'Clay 1B-10B; Ingersoll Rand (DNC) subsidiary','https://www.linkedin.com/company/goldbelt-c6-llc':'Clay 25M-75M','https://www.linkedin.com/company/systems-plus-solutions':'entity mismatch','https://www.linkedin.com/company/wsp-usa-solutions-inc':'subsidiary of WSP Global (>$1B)','https://www.linkedin.com/company/wsp-usa-corp':'subsidiary of WSP Global (>$1B)','https://www.linkedin.com/company/leidos-biomedical-research-inc.':'subsidiary of Leidos (>$1B)','https://www.linkedin.com/company/manhattan-associates':'revenue >$1B','https://www.linkedin.com/company/srcdefense':'Clay revenue 1B-10B','https://www.linkedin.com/company/cdm-federal-programs-corporation':'subsidiary of CDM Smith (>$1B); Clay 500K-1M for this entity','https://www.linkedin.com/company/mag-ds-corp.':'Clay revenue 10M-25M'}
def rev(u):
  c=clay_rev.get(u)
  if c in ('200M-500M','500M-1B'): return 'confirmed','Blitz $100M-$1B; Clay '+c
  if c=='75M-200M': return 'overlap','Blitz $100M-$1B; Clay 75M-200M (straddles $100M floor)'
  return 'blitz-only','Blitz $100M-$1B; Clay '+str(c or 'no value')
STALE={'https://www.linkedin.com/in/nathan-mcfarland-40141964','https://www.linkedin.com/in/devinbrownmba','https://www.linkedin.com/in/kameron-turner-71420'}
def nurl(u): u=(u or '').strip().split('?')[0].rstrip('/'); return re.sub(r'^https?://([a-z]+\.)?linkedin\.com','https://www.linkedin.com',u).lower()
def tclass(t):
  tl=(t or '').lower()
  if re.search(r'assistant|intern|coordinator|sourcer|recruiter\b|member|consultant|partnerships|human resources|sales',tl): return None
  if re.search(r'talent acquisition|recruiting|contingent|workforce solutions',tl): return 2 if re.search(r'director|head|vp|vice president|manager|chief',tl) else None
  if re.search(r'\b(cio|cto|ciso|chief)\b',tl) and not re.search(r'\b(vp|vice president|director)\b',tl): return 3
  if re.search(r'director|\bvp\b|vice president|\bsvp\b|evp|head of',tl) and re.search(r'engineer|it\b|information|technolog|technical|software|infrastructure|operations|cyber|security|data|cio|cto|\bai\b',tl): return 1
  if re.search(r'\b(cio|cto)\b|chief (information|technology)',tl): return 3
  return None
rows={}; comps=[]
for x in sel:
  u=x['match']['linkedin_url']; a=x['award']; m=x['match']
  rs,rn=rev(u)
  ag=AG.get(a.get('Awarding Sub Agency')) or PARENT.get(a.get('Awarding Agency'),a.get('Awarding Agency'))
  if a.get('Awarding Sub Agency')=='Departmental Offices': ag=PARENT.get(a['Awarding Agency'],a['Awarding Agency'])
  url=('https://www.usaspending.gov/award/'+a['generated_internal_id']) if a.get('generated_internal_id') else a.get('url')
  comp=dict(company_name=m['name'],company_linkedin_url=u,company_domain=m.get('domain') or '-',hq_state=(m.get('hq') or {}).get('state') or '-',geo_tier=x['geo_tier'],revenue_status=rs,revenue_evidence=rn,
    award_source=a['_src'],award_id=a.get('Award ID') or '-',award_date_signed=x['date_signed'],award_type=x.get('award_type') or '-',award_amount_usd=round(a.get('Award Amount') or 0),awarding_agency=a.get('Awarding Agency') or '-',awarding_sub_agency=a.get('Awarding Sub Agency') or '-',award_description=re.sub(r'\s+',' ',(a.get('Description') or '')).strip()[:200],award_url=url or '-',contract_or_agency=ag)
  comps.append(dict(comp,decision=('EXCLUDED: '+EXCLUDE[u]) if u in EXCLUDE else 'included ('+rs+')'))
  if u in EXCLUDE: continue
  def add(url,first,last,full,title,loc,src):
    k=nurl(url)
    if not k or '/in/' not in k or k in STALE: return
    c=tclass(title)
    if c is None: return
    if k in rows:
      if src not in rows[k]['source']: rows[k]['source']+='+'+src
      return
    rows[k]=dict(linkedin_url=k,first_name=re.sub(r"[^A-Za-z'\-]",'',(first or '-').split()[0]) or '-',last_name=last or '-',full_name=full,job_title=re.sub(r'\s+',' ',title),title_priority=c,person_location=loc or '-',source=src,**comp)
  for r in (blitz.get(u) or {}).get('results') or []:
    p=r['person']; e=(p.get('experiences') or [{}])[0]; l=p.get('location') or {}
    add(p.get('linkedin_url'),p.get('first_name'),p.get('last_name'),p.get('full_name'),e.get('job_title'),', '.join(filter(None,[l.get('city'),l.get('state_code')])),'blitz')
  for name,curl,company,title,loc,ci in clay_contacts:
    cu=ci if ci.startswith('http') else None
    if cu!=u and not (cu is None and (m.get('domain') or '#')==ci): continue
    if company.split()[0].lower() not in m['name'].lower() and company.lower() not in m['name'].lower(): continue
    parts=name.split(); add(curl,parts[0],' '.join(parts[1:]),name,title,loc,'clay')
L=list(rows.values())
by=collections.defaultdict(list)
for r in L: by[r['company_linkedin_url']].append(r)
for u,rs in by.items():
  rs.sort(key=lambda r:(r['title_priority'],0 if '+' in r['source'] else 1,r['full_name']))
  p1=[r for r in rs if r['title_priority']==1]; p2=[r for r in rs if r['title_priority']==2]
  pick=p1[:2]+p2[:1]; pick+= [r for r in p1[2:]+p2[1:] if r not in pick][:3-len(pick)]
  for r in rs: r['selected_for_launch']='yes' if r in pick else 'no'
cols=['linkedin_url','first_name','last_name','full_name','job_title','title_priority','selected_for_launch','person_location','company_name','company_linkedin_url','company_domain','hq_state','geo_tier','revenue_status','revenue_evidence','contract_or_agency','award_source','award_id','award_date_signed','award_type','award_amount_usd','awarding_agency','awarding_sub_agency','award_description','award_url','source']
L.sort(key=lambda r:(r['selected_for_launch']!='yes',r['geo_tier']!='DC Metro',r['company_name'],r['title_priority']))
with open(OUT+'/2026-10-30-leads.csv','w',newline='') as f: w=csv.DictWriter(f,cols); w.writeheader(); [w.writerow(r) for r in L]
cc=list(comps[0].keys())
with open(OUT+'/2026-10-30-companies.csv','w',newline='') as f: w=csv.DictWriter(f,cc); w.writeheader(); [w.writerow(dict(c,contacts_found=0) if False else c) for c in sorted(comps,key=lambda c:(c['decision'],c['company_name']))]
sel_rows=[r for r in L if r['selected_for_launch']=='yes']
print('leads',len(L),'companies w/ contacts',len(by),'selected',len(sel_rows),'from',len({r['company_name'] for r in sel_rows}),'companies')
print(collections.Counter(r['revenue_status'] for r in sel_rows), collections.Counter(r['title_priority'] for r in sel_rows), collections.Counter(len([r for r in rs if r['selected_for_launch']=='yes']) for rs in by.values()))
print('no contacts:',[c['company_name'] for c in comps if c['decision'].startswith('included') and c['company_linkedin_url'] not in by])
