import json,re,csv,sys,collections
S=sys.argv[1]; KEPT=sys.argv[2]; PPL=sys.argv[3]
comps=json.load(open(S+'/'+KEPT)); ppl=json.load(open(S+'/'+PPL))['results']
def nurl(u): u=(u or '').strip().split('?')[0].rstrip('/'); return re.sub(r'^https?://([a-z]+\.)?linkedin\.com','https://www.linkedin.com',u).lower()
def tclass(t):
  tl=(t or '').lower()
  if re.search(r'assistant|intern|coordinator|sourcer|former|retired|student|partner\b|consultant|specialist|contract|campus|university|early career|payroll|benefits|compensation|operations',tl): return None
  if not re.search(r'talent acquisition|recruit',tl): return None
  if re.search(r'\b(director|head|vp|vice president|svp|chief)\b',tl): return 1
  if re.search(r'\bmanager\b',tl): return 2
  return None
rows=[]
for u,x in comps.items():
  c=x['company']; seen=set(); names=set(); cand=[]
  for r in (ppl.get(u) or {}).get('results') or []:
    p=r['person']; e=(p.get('experiences') or [{}])[0]; k=nurl(p.get('linkedin_url'))
    if not k or '/in/' not in k or k in seen: continue
    cls=tclass(e.get('job_title'))
    if cls is None: continue
    fn=re.sub(r"[^A-Za-z'\-]",'',(p.get('first_name') or '').split()[0] if p.get('first_name') else '')
    ln=(p.get('last_name') or '').split(',')[0].strip()
    if len(fn)<2 or not ln: continue
    nk=(fn+' '+ln).lower()
    if nk in names: continue
    seen.add(k); names.add(nk); l=p.get('location') or {}
    cand.append(dict(linkedin_url=k,first_name=fn,last_name=ln,full_name=p.get('full_name'),job_title=re.sub(r'\s+',' ',e.get('job_title') or ''),title_priority=cls,person_location=', '.join(filter(None,[l.get('city'),l.get('state_code')])) or '-',company_name=c['name'],company_linkedin_url=u,company_domain=c.get('domain') or '-',hq_state=(c.get('hq') or {}).get('state') or '-',company_industry=c.get('industry') or '-',employees_on_linkedin=c.get('employees_on_linkedin') or '-',revenue_evidence='Blitz '+str(c.get('revenue_range')),trigger_matched_jobs=x.get('matched_jobs'),trigger='open remote/hybrid technical role(s) posted in window (Blitz /v2/company/tam-by-jobs)',source='blitz'))
  cand.sort(key=lambda r:r['title_priority'])
  for i,r in enumerate(cand): r['selected_for_launch']='yes' if i<3 else 'no'; rows.append(r)
print('people',len(rows),'selected',sum(r['selected_for_launch']=='yes' for r in rows),'companies',len({r['company_linkedin_url'] for r in rows}))
print(collections.Counter(len([r for r in rows if r['company_linkedin_url']==u and r['selected_for_launch']=='yes']) for u in {r['company_linkedin_url'] for r in rows}))
json.dump(rows,open(S+'/c9_rows.json','w'))
