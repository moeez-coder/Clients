import json,re,csv,sys,collections
S,D,COMPF,PEOPLEF,OUTNAME=sys.argv[1:6]
comps=json.load(open(S+'/'+COMPF)); ppl=json.load(open(S+'/'+PEOPLEF))['results']
AG={'Animal and Plant Health Inspection Service':'USDA APHIS','Department of State':'State Department','Department of Veterans Affairs':'VA','Environmental Protection Agency':'EPA','Federal Emergency Management Agency':'FEMA','Federal Railroad Administration':'FRA','Food and Drug Administration':'FDA','Health Resources and Services Administration':'HRSA','National Aeronautics and Space Administration':'NASA','National Institutes of Health':'NIH','National Oceanic and Atmospheric Administration':'NOAA','National Science Foundation':'NSF','Transportation Security Administration':'TSA','U.S. Customs and Border Protection':'CBP','U.S. Geological Survey':'USGS','Office of Procurement Operations':'DHS','Office of the Assistant Secretary for Administration and Management':'Department of Labor','Office of the Assistant Secretary for Financial Resources':'HHS','Public Buildings Service':'GSA','Federal Acquisition Service':'GSA','Federal Bureau of Investigation':'FBI','Centers for Medicare and Medicaid Services':'CMS','Federal Highway Administration':'FHWA','U.S. Immigration and Customs Enforcement':'ICE','National Institute of Standards and Technology':'NIST','Centers for Disease Control and Prevention':'CDC','Federal Aviation Administration':'FAA','U.S. Coast Guard':'Coast Guard','Internal Revenue Service':'IRS','Department of the Army':'Army','Department of the Navy':'Navy','Department of the Air Force':'Air Force','Defense Logistics Agency':'DLA','Defense Information Systems Agency':'DISA','Missile Defense Agency':'Missile Defense Agency','U.S. Special Operations Command':'SOCOM','Defense Health Agency':'Defense Health Agency','Defense Threat Reduction Agency':'DTRA','Washington Headquarters Services':'DoD','U.S. Army Corps of Engineers':'Army Corps of Engineers','Bureau of Prisons':'Bureau of Prisons','Federal Prison System / Bureau of Prisons':'Bureau of Prisons','U.S. Secret Service':'Secret Service','Cybersecurity and Infrastructure Security Agency':'CISA','U.S. Census Bureau':'Census Bureau','Social Security Administration':'SSA','Department of Energy':'Department of Energy','Department of Education':'Department of Education','Indian Health Service':'IHS','National Park Service':'National Park Service','Bureau of Reclamation':'Bureau of Reclamation','Forest Service':'Forest Service','ARMY':'Army','AIR FORCE':'Air Force','NAVY':'Navy','DEFENSE LOGISTICS AGENCY':'DLA','MISSILE DEFENSE AGENCY':'Missile Defense Agency','DEFENSE INFORMATION SYSTEMS AGENCY':'DISA','SPACE FORCE':'Space Force','U.S. SPECIAL OPERATIONS COMMAND':'SOCOM','DEFENSE HEALTH AGENCY':'Defense Health Agency'}
PARENT={'Department of the Interior':'Department of the Interior','Department of the Treasury':'Treasury','Department of Homeland Security':'DHS','Department of Health and Human Services':'HHS','Department of Defense':'DoD','Department of Commerce':'Department of Commerce','Department of Justice':'Department of Justice','Department of Transportation':'Department of Transportation','Department of Agriculture':'USDA','General Services Administration':'GSA','Department of Labor':'Department of Labor','Department of Veterans Affairs':'VA','Department of State':'State Department','National Aeronautics and Space Administration':'NASA','Environmental Protection Agency':'EPA','Department of Energy':'Department of Energy','Department of Education':'Department of Education','Small Business Administration':'SBA','Social Security Administration':'SSA','Agency for International Development':'USAID','Nuclear Regulatory Commission':'NRC','Department of Housing and Urban Development':'HUD'}
def agency(a):
  sub=a.get('Awarding Sub Agency'); par=a.get('Awarding Agency')
  if sub in AG: return AG[sub]
  return PARENT.get(par) or (par if par and len(par)<=35 else 'federal')
def nurl(u): u=(u or '').strip().split('?')[0].rstrip('/'); return re.sub(r'^https?://([a-z]+\.)?linkedin\.com','https://www.linkedin.com',u).lower()
def tclass(t):
  tl=(t or '').lower()
  if re.search(r'assistant|intern|coordinator|sourcer|recruiter\b|member|consultant|partnerships|human resources|sales|former|retired',tl): return None
  if re.search(r'talent acquisition|recruiting|contingent|workforce solutions',tl): return 2 if re.search(r'director|head|vp|vice president|manager|chief',tl) else None
  if re.search(r'\b(cio|cto|ciso|chief)\b',tl) and not re.search(r'\b(vp|vice president|director)\b',tl): return 3
  if re.search(r'director|\bvp\b|vice president|\bsvp\b|evp|head of',tl) and re.search(r'engineer|it\b|information|technolog|technical|software|infrastructure|operations|cyber|security|data|cio|cto|\bai\b',tl): return 1
  if re.search(r'\b(cio|cto)\b|chief (information|technology)',tl): return 3
  return None
rows=[]
for u,x in comps.items():
  c=x['company'];a=x['award']
  url=('https://www.usaspending.gov/award/'+a['generated_internal_id']) if a.get('generated_internal_id') else a.get('url','-')
  base=dict(company_name=c['name'],company_linkedin_url=u,company_domain=c.get('domain') or '-',hq_state=(c.get('hq') or {}).get('state') or '-',company_industry=c.get('industry') or '-',revenue_evidence='Blitz '+str(c.get('revenue_range')),award_recipient=a['Recipient Name'],award_source=a['_src'],award_id=a.get('Award ID') or '-',award_amount_usd=round(a.get('Award Amount') or 0),awarding_agency=a.get('Awarding Agency') or '-',awarding_sub_agency=a.get('Awarding Sub Agency') or '-',award_start=a.get('Start Date') or a.get('award_date') or '-',award_description=re.sub(r'\s+',' ',a.get('Description') or '')[:200],award_url=url,contract_or_agency=agency(a))
  seen=set(); cand=[]
  for r in (ppl.get(u) or {}).get('results') or []:
    p=r['person']; e=(p.get('experiences') or [{}])[0]; k=nurl(p.get('linkedin_url'))
    if not k or '/in/' not in k or k in seen: continue
    cls=tclass(e.get('job_title'))
    if cls is None: continue
    seen.add(k); l=p.get('location') or {}
    cand.append(dict(linkedin_url=k,first_name=re.sub(r"[^A-Za-z'\-]",'',(p.get('first_name') or '-').split()[0]) or '-',last_name=(p.get('last_name') or '-').split(',')[0],full_name=p.get('full_name'),job_title=re.sub(r'\s+',' ',e.get('job_title') or ''),title_priority=cls,person_location=', '.join(filter(None,[l.get('city'),l.get('state_code')])) or '-',source='blitz',**base))
  p1=[r for r in cand if r['title_priority']==1]; p2=[r for r in cand if r['title_priority']==2]
  pick=p1[:2]+p2[:1]; pick+=[r for r in p1[2:]+p2[1:] if r not in pick][:3-len(pick)]
  for r in cand: r['selected_for_launch']='yes' if r in pick else 'no'; rows.append(r)
cols=['linkedin_url','first_name','last_name','full_name','job_title','title_priority','selected_for_launch','person_location','company_name','company_linkedin_url','company_domain','hq_state','company_industry','revenue_evidence','contract_or_agency','award_recipient','award_source','award_id','award_amount_usd','awarding_agency','awarding_sub_agency','award_start','award_description','award_url','source']
rows.sort(key=lambda r:(r['selected_for_launch']!='yes',r['company_name'],r['title_priority']))
with open(D+'/'+OUTNAME,'w',newline='') as f: w=csv.DictWriter(f,cols); w.writeheader(); [w.writerow(r) for r in rows]
s=[r for r in rows if r['selected_for_launch']=='yes']
print('leads',len(rows),'selected',len(s),'companies',len({r['company_name'] for r in s}),collections.Counter(r['title_priority'] for r in s))
print(collections.Counter(r['contract_or_agency'] for r in s).most_common(25))
