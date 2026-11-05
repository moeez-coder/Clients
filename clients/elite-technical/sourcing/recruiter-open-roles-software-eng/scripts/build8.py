import json,re,csv,glob,collections
from segs8 import SEGS,ORDER
prev=set()
for f in glob.glob('/home/user/Clients/clients/elite-technical/sourcing/*/*leads.csv'):
  if '/recruiter-open-roles-' in f: continue   # superseded 3-segment draft, being rebuilt
  for r in csv.DictReader(open(f)): prev.add(r['linkedin_url'].rstrip('/').lower())
def nurl(u): u=(u or '').strip().split('?')[0].rstrip('/'); return re.sub(r'^https?://([a-z]+\.)?linkedin\.com','https://www.linkedin.com',u).lower()
def clean_co(n):
  n=re.sub(r'\s*\(.*?\)','',n or '').strip()
  n=re.sub(r',?\s+(Inc\.?|LLC|L\.L\.C\.|Corp\.?|Corporation|Co\.|Ltd\.?|LLP|PLLC|P\.C\.|Incorporated)$','',n,flags=re.I)
  return re.sub(r'[®™]','',n).strip()
KEY=r'engineer|developer|programmer|architect|analyst|administrator|admin|specialist|technician|scientist|support|desk|designer|consultant|sre|devops|qa|tester|sdet|lead'
def clean_role(t):
  raw=t or ''
  t=re.sub(r'\s*[\(\[].*?[\)\]]','',raw)
  t=re.sub(r'^\s*(\d+|[A-Z]{2,5}\d*)\s*[-–:]\s*','',t)
  parts=[p.strip() for p in re.split(r'\s+[-–|]\s+|\s*,\s*',t) if p.strip()]
  best=next((p for p in parts if re.search(KEY,p.lower()) and len(p.split())>=2),None) or (parts[0] if parts else '')
  best=re.sub(r'\b(remote|hybrid|on-?site)\b','',best,flags=re.I)
  best=re.sub(r'\s*-?\s*\d{4,}$','',best)
  return re.sub(r'\s+',' ',best).strip(' -,|/:')[:70]
def article(role):
  w=role.split()[0] if role else ''; base=re.sub(r'[^A-Za-z]','',w)
  if base.isupper() and 1<len(base)<=5: return 'an' if base[0] in 'AEFHILMNORSX' else 'a'
  l=base.lower()
  if re.match(r'(uni|use|usa|euro|one|ux)',l): return 'a'
  return 'an' if l[:1] in 'aeiou' else 'a'
BADPOST=r'\bintern(ship)?\b|co-?op\b|student|apprentice|^(vice president|vp\b|svp|evp|chief|cio\b|ciso\b|cto\b|director|head of|manager)'
def personok(seg,title,fallback):
  title=re.split(r'\s+(?:at|@)\s+|\s*[|•]\s*',title or '')[0]; tl=title.lower()
  if re.search(r'assistant|intern|coordinator|sourcer|recruiter\b|former|retired|student|sales|marketing|partner\b|specialist|consultant|training|finance|legal|program manager|project manager|business development|\bgtm\b|revenue|provider network|projects\b|customer|account|pricing|talent management',tl): return False
  if fallback: return bool(re.search(r'talent|people',tl) and re.search(r'\b(head|director|vp|vice president|svp|chief)\b',tl))
  if re.search(HMX.get(seg,r'$^'),tl): return False
  return bool(re.search(r'\b(manager|director|vp|vice president|head|svp|chief|ciso|cdo)\b',tl) and re.search(SEGS[seg]['hmrx'],tl))
HMX={'software':r'hardware|electrical|mechanical|manufactur|quality|controls|civil|\bdata\b|security|cyber|network|firmware|embedded|test engineering|systems engineering|process|plant',
 'electrical':r'software|\bdata\b|cloud|devops|security|cyber|\bit\b|information|network|application|web|mechanical|manufactur|civil|process|plant|quality',
 'mechanical':r'quality assurance|\bqa\b|software|\bdata\b|cloud|devops|security|cyber|\bit\b|information|network|application|web|electrical|controls|firmware|embedded|hardware|civil',
 'cloud':r'hardware|electrical|mechanical|manufactur|quality|security|cyber|\bdata\b',
 'itinfra':r'software engineering|hardware|electrical|mechanical|manufactur|quality|data science|analytics',
 'entapps':r'hardware|electrical|mechanical|manufactur|security|cyber|network|infrastructure',
 'data':r'hardware|electrical|mechanical|manufactur|security|cyber|network|people|culture|\bhr\b',
 'security':r'hardware|electrical|mechanical|manufactur|physical|loss prevention|life safety|safety compliance|environmental'}
GLOBALX=r'account executive|sales|business development|customer success|marketing|recruit|account manager|\bintern'
ROLE_INC={'security':r'secur|cyber|soc\b|incident|penetration|\biam\b|identity|grc|threat|vulnerab|forensic',
 'data':r'data|machine learning|\bml\b|\bai\b|analytics|business intelligence|\bbi\b|scientist|mlops|tableau|power bi',
 'cloud':r'devops|reliability|\bsre\b|cloud|platform|kubernetes|\baws\b|azure|gcp|release|build|infrastructure',
 'entapps':r'sap\b|oracle|workday|salesforce|servicenow|dynamics|netsuite|erp|business systems|crm|epic|peoplesoft|integration|hris|business analyst',
 'itinfra':r'system|network|help ?desk|service desk|desktop|support|administrator|database|\bdba\b|infrastructure|endpoint|intune|microsoft|windows|linux|voip|\bit\b|technician|telecom',
 'electrical':r'electrical|controls?\b|automation|plc|\brf\b|embedded|firmware|fpga|hardware|electronic|power|avionics|systems engineer|test engineer|instrumentation|asic|pcb',
 'mechanical':r'mechanical|manufactur|process|quality|reliability|design engineer|aerospace|industrial|product engineer|packaging|materials|npd|tooling|welding|stress',
 'software':r'software|developer|full ?stack|back ?end|front ?end|\bjava\b|\.net|python|mobile|ios|android|sdet|qa automation|web|application'}
jdold={}
for k,v in json.load(open('jd_by_company.json')).items(): jdold[v['job_url']]=v['jd']
used=set(); out={}; stats={}
for seg in ORDER:
  D=json.load(open(f'pull8_{seg}.json')); st=collections.Counter(D['funnel']); s=SEGS[seg]; rows=[]
  for u,v in D['data'].items():
    jobs=sorted((v['jobs'] or {}).get('results') or [],key=lambda j:j.get('date_posted') or '',reverse=True)
    def ok(j):
      t=(j.get('title') or '').lower(); cr=clean_role(j.get('title')).lower()
      if re.search(GLOBALX,t) or re.search(s['post_exc'],t) or re.search(BADPOST,cr) or len(cr)<4: return False
      return bool(re.search(ROLE_INC[seg],cr))
    jobs=[j for j in jobs if ok(j)]
    if not jobs: st['no qualifying posting']+=1; continue
    j=jobs[0]; c=v['company']
    def cands(res,fb):
      L=[]
      for r in (res or {}).get('results') or []:
        p=r['person']; e=(p.get('experiences') or [{}])[0]; k=nurl(p.get('linkedin_url'))
        if '/in/' not in k or not personok(seg,e.get('job_title'),fb): continue
        fn=re.sub(r"[^A-Za-z'\-]",'',(p.get('first_name') or '').split()[0]) if p.get('first_name') else ''
        ln=(p.get('last_name') or '').split(',')[0].strip()
        if len(fn)<2 or not ln: continue
        L.append((k,fn,ln,p,e))
      return L
    hm=cands(v['hm'],False); persona='hiring manager'
    if not hm:
      hm=cands(v['fb'],True)[:1]; persona='talent fallback'
    hm=[x for x in hm if x[0] not in used and x[0] not in prev]
    if not hm: st['no usable person']+=1; continue
    role=clean_role(j.get('title')); seen_names=set()
    for k,fn,ln,p,e in hm:
      if (fn+ln).lower() in seen_names: continue
      seen_names.add((fn+ln).lower()); used.add(k); l=p.get('location') or {}
      rows.append(dict(linkedin_url=k,first_name=fn,last_name=ln,full_name=p.get('full_name'),job_title=re.sub(r'\s+',' ',e.get('job_title') or ''),persona=persona,
        person_location=', '.join(filter(None,[l.get('city'),l.get('state_code')])) or '-',company_name=c['name'],company_name_clean=clean_co(c['name']),company_linkedin_url=u,
        company_domain=c.get('domain') or '-',hq_state=(c.get('hq') or {}).get('state') or '-',company_industry=c.get('industry') or '-',employees_on_linkedin=c.get('employees_on_linkedin') or '-',
        revenue_evidence='Blitz '+str(c.get('revenue_range')),open_role=role,open_role_with_article=article(role)+' '+role,open_role_raw=j.get('title'),job_url=j.get('url') or '-',
        job_posted=(j.get('date_posted') or '-')[:10],job_ai_summary=re.sub(r'\s+',' ',j.get('ai_summary') or '-'),jd=jdold.get(j.get('url'),''),segment=s['name'],selected_for_launch='yes',note='-',source='blitz'))
  st['companies with leads']=len({r['company_linkedin_url'] for r in rows}); st['leads']=len(rows); st['hiring manager leads']=sum(r['persona']=='hiring manager' for r in rows)
  st['jd reused']=sum(bool(r['jd']) for r in rows)
  out[seg]=rows; stats[seg]=dict(st); print(seg,stats[seg])
json.dump({'rows':out,'stats':stats},open('rows8.json','w'))
print('TOTAL leads',sum(len(v) for v in out.values()))
