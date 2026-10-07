import json,re,glob,csv,collections
def dom(u):
    u=re.sub(r'^https?://','',(u or '').lower()).split('/')[0].split(':')[0]; return re.sub(r'^www\.','',u)
def root(d):
    p=d.split('.')
    if len(p)>=3 and p[-2] in ('co','com','org','net','gov','ac') and len(p[-1])==2: return '.'.join(p[-3:])
    return '.'.join(p[-2:]) if len(p)>=2 else d
def li(u):
    if not u: return ''
    u=u.strip().lower().split('?')[0].rstrip('/').replace('http://','https://')
    u=re.sub(r'https://[a-z]{2,3}\.linkedin\.com','https://www.linkedin.com',u); u=u.replace('https://linkedin.com','https://www.linkedin.com')
    return u if '/company/' in u else ''
CC={'united states':'US','canada':'CA','united kingdom':'GB','ireland':'IE','australia':'AU','new zealand':'NZ','germany':'DE','france':'FR','italy':'IT','spain':'ES','netherlands':'NL','belgium':'BE','sweden':'SE','denmark':'DK','norway':'NO','finland':'FI','austria':'AT','switzerland':'CH','poland':'PL','mexico':'MX','brazil':'BR','south africa':'ZA','india':'IN','japan':'JP','china':'CN','turkey':'TR','korea':'KR'}
def cc(x):
    x=(x or '').strip()
    return x.upper() if len(x)==2 else CC.get(x.lower(),x)
def emp_band(n):
    try: n=int(n)
    except: return ''
    for lo,hi,b in [(1,10,'1-10'),(11,50,'11-50'),(51,200,'51-200'),(201,500,'201-500'),(501,1000,'501-1000'),(1001,5000,'1001-5000'),(5001,10000,'5001-10000')]:
        if lo<=n<=hi: return b
    return '10001+' if n>10000 else ''
R={}; BYDOM={}
def get(l,d):
    k=li(l); dr=root(dom(d)) if d else ''
    key=None
    if k and k in R: key=k
    elif dr and dr in BYDOM: key=BYDOM[dr]
    if key is None:
        key=k or ('dom:'+dr)
        if key=='dom:': return None
        R[key]={'linkedin_url':k,'domain':dr,'sources':set(),'flags':set(),'texts':[]}
    r=R[key]
    if k and not r['linkedin_url']: r['linkedin_url']=k
    if dr and not r['domain']: r['domain']=dr
    if dr: BYDOM.setdefault(dr,key)
    return r
def setf(r,**kw):
    for k,v in kw.items():
        if v not in (None,'',[],{}) and not r.get(k): r[k]=v
# Blitz
for f in sorted(glob.glob('blitz/*.jsonl')):
    slice_=f.split('/')[-1].split('__')[0]
    for l in open(f):
        x=json.loads(l)
        if '_meta' in x or '_error' in x: continue
        r=get(x['linkedin_url'],x.get('domain') or x.get('website'))
        if r is None: continue
        hq=x.get('hq') or {}
        setf(r,name=x['name'],industry=x['industry'],employees=x.get('employees_on_linkedin'),size_band=x.get('size'),country=cc(hq.get('country_code')),city=hq.get('city'),state=hq.get('state'),founded=x.get('founded_year'),ctype=x.get('type'))
        r['sources'].add('Blitz /v2/search/companies'); r['flags'].add('blitz:'+slice_)
        if slice_=='dealer_kw': r['flags'].add('dealer_text_blitz')
        r['texts'].append(((x.get('about') or '')+' | '+' '.join(x.get('specialties') or []))[:900])
# Prospeo
for f in sorted(glob.glob('prospeo/*.jsonl')):
    slice_=f.split('/')[-1].split('__')[0]
    for l in open(f):
        x=json.loads(l)
        if '_meta' in x or '_error' in x: continue
        r=get(x.get('linkedin_url'),x.get('domain') or x.get('website'))
        if r is None: continue
        loc=x.get('location') or {}
        setf(r,name=x['name'],industry=x['industry'],employees=x.get('employee_count'),size_band=x.get('employee_range'),country=cc(loc.get('country_code')),city=loc.get('city'),state=loc.get('state'),founded=x.get('founded'),ctype=x.get('type'))
        rv=x.get('revenue_range') or {}
        setf(r,revenue_range=x.get('revenue_range_printed'),revenue_min=rv.get('min'),revenue_max=rv.get('max'))
        setf(r,naics=','.join((x.get('naics_codes') or [])[:6]),keywords='; '.join((x.get('keywords') or [])[:15]))
        r['sources'].add('Prospeo /search-company'); r['flags'].add('prospeo:'+slice_)
        if slice_=='kwdealer': r['flags'].add('dealer_text_prospeo')
        r['texts'].append(((x.get('description_ai') or '')+' | '+(x.get('description') or ''))[:900])
# DiscoLike
for f in sorted(glob.glob('disco/*.jsonl')):
    cat=f.split('/')[-1].split('__')[0]
    for l in open(f):
        x=json.loads(l)
        if '_error' in x: continue
        lis=[u for u in (x.get('social_urls') or []) if 'linkedin.com/company' in u]
        r=get(lis[0] if lis else '',x.get('domain'))
        if r is None: continue
        a=x.get('address') or {}
        setf(r,name=x['name'],country=cc(a.get('country')),city=a.get('city'),state=a.get('state'),size_band=x.get('employees'),revenue_range=x.get('revenue_range'))
        r['sources'].add('DiscoLike /v1/discover'); r['flags'].add('site_dealer_phrase'); r['flags'].add('disco:'+cat)
        r['texts'].append(((x.get('description') or ''))[:700])
# EXA resolved
E=json.load(open('exa_resolved.json'))
for d,v in E['resolved'].items():
    if not v: continue
    c=v.get('company') or {}; hq=c.get('hq') or {}
    r=get(v['li'],d)
    if r is None: continue
    setf(r,name=c.get('name'),industry=c.get('industry'),employees=c.get('employees_on_linkedin'),size_band=c.get('size'),country=cc(hq.get('country_code')),city=hq.get('city'),state=hq.get('state'))
    r['sources'].add('EXA /search (+Blitz enrichment)'); r['flags'].add('exa_discovery'); r['flags'].add('exa_hits:%d'%E['counts'].get(d,1))
    r['texts'].append(((c.get('about') or '')+' | '+(E['titles'].get(d) or ''))[:900])
for d in E['known_hits']:
    k=BYDOM.get(d)
    if k: R[k]['flags'].add('exa_discovery'); R[k]['sources'].add('EXA /search (+Blitz enrichment)')
# previously sourced in repo
prev=set()
import os
for f in glob.glob('/home/user/Clients/clients/vntana/sourcing/*/20*-companies*.csv')+['/home/user/Clients/clients/vntana/sourcing/2026-09-16-us-icp-triage.csv']:
    if 'cad-render' in f: continue
    for x in csv.DictReader(open(f,encoding='utf8',errors='ignore')):
        u=li(x.get('linkedin_url') or x.get('company_linkedin_tag') and 'https://www.linkedin.com/company/'+x['company_linkedin_tag'])
        d=root(dom(x.get('domain') or x.get('standardised_domain') or x.get('website')))
        if u: prev.add(u)
        if d: prev.add('dom:'+d)
n_prev=0
for k,r in R.items():
    if (r['linkedin_url'] and r['linkedin_url'] in prev) or ('dom:'+r['domain'] in prev): r['flags'].add('prev_sourced_in_repo'); n_prev+=1
print('unique companies',len(R),'with linkedin',sum(1 for r in R.values() if r['linkedin_url']),'prev sourced',n_prev)
print(collections.Counter(len(r['sources']) for r in R.values()))
import pickle; pickle.dump(R,open('wide.pkl','wb'))
