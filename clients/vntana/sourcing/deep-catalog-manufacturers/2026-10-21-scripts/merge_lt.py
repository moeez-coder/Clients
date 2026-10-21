import json,re,glob,csv,collections,pickle
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
CC={'united states':'US','canada':'CA','united kingdom':'GB','ireland':'IE','australia':'AU','new zealand':'NZ','germany':'DE','france':'FR','italy':'IT','spain':'ES','netherlands':'NL','belgium':'BE','sweden':'SE','denmark':'DK','norway':'NO','finland':'FI','austria':'AT','switzerland':'CH','poland':'PL','mexico':'MX','brazil':'BR','south africa':'ZA','india':'IN','japan':'JP','china':'CN','turkey':'TR','korea':'KR','taiwan':'TW','czech republic':'CZ','czechia':'CZ'}
def cc(x):
    x=(x or '').strip(); return x.upper() if len(x)==2 else CC.get(x.lower(),x)
R={};BYDOM={}
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
for f in sorted(glob.glob('blitz/*.jsonl')):
    sl=f.split('/')[-1].split('__')[0]
    for l in open(f):
        x=json.loads(l)
        if '_meta' in x or '_error' in x: continue
        r=get(x['linkedin_url'],x.get('domain') or x.get('website'))
        if r is None: continue
        hq=x.get('hq') or {}
        setf(r,name=x['name'],industry=x['industry'],employees=x.get('employees_on_linkedin'),size_band=x.get('size'),country=cc(hq.get('country_code')),city=hq.get('city'),state=hq.get('state'))
        r['sources'].add('Blitz /v2/search/companies'); r['flags'].add('blitz:'+sl)
        if sl=='catalog': r['flags'].add('catalog_text_blitz')
        r['texts'].append(((x.get('about') or '')+' | '+' '.join(x.get('specialties') or []))[:900])
for f in sorted(glob.glob('prospeo/*.jsonl')):
    sl=f.split('/')[-1].split('__')[0]
    for l in open(f):
        x=json.loads(l)
        if '_meta' in x or '_error' in x: continue
        r=get(x.get('linkedin_url'),x.get('domain') or x.get('website'))
        if r is None: continue
        loc=x.get('location') or {}
        setf(r,name=x['name'],industry=x['industry'],employees=x.get('employee_count'),size_band=x.get('employee_range'),country=cc(loc.get('country_code')),city=loc.get('city'),state=loc.get('state'))
        rv=x.get('revenue_range') or {}
        setf(r,revenue_range=x.get('revenue_range_printed'),revenue_min=rv.get('min'),naics=','.join((x.get('naics_codes') or [])[:6]),keywords='; '.join((x.get('keywords') or [])[:15]))
        r['sources'].add('Prospeo /search-company'); r['flags'].add('prospeo:'+sl)
        if sl=='kwcatalog': r['flags'].add('catalog_text_prospeo')
        r['texts'].append(((x.get('description_ai') or '')+' | '+(x.get('description') or ''))[:900])
for f in sorted(glob.glob('disco/*.jsonl')):
    kind=f.split('/')[-1].split('__')[0]
    for l in open(f):
        x=json.loads(l)
        if '_error' in x: continue
        lis=[u for u in (x.get('social_urls') or []) if 'linkedin.com/company' in u]
        r=get(lis[0] if lis else '',x.get('domain'))
        if r is None: continue
        a=x.get('address') or {}
        setf(r,name=x['name'],country=cc(a.get('country')),city=a.get('city'),state=a.get('state'),size_band=x.get('employees'),revenue_range=x.get('revenue_range'))
        r['sources'].add('DiscoLike /v1/discover'); r['flags'].add('site_image_placeholder_phrase' if kind=='img' else 'site_catalog_phrase')
        r['texts'].append((x.get('description') or '')[:700])
for f in sorted(glob.glob('ai2/*.jsonl')):
    v=f.split('/')[-1].split('.')[0]
    for l in open(f):
        x=json.loads(l)
        if '_meta' in x or '_error' in x: continue
        r=get(x.get('linkedin'),x.get('domain') or x.get('website'))
        if r is None: continue
        setf(r,name=x['name'],industry=x['industry'],employees=x.get('staff'),country=cc(x.get('country')))
        r['sources'].add('AI Ark POST /v1/companies'); r['flags'].add('aiark:'+v)
        if v=='catalog': r['flags'].add('catalog_text_aiark')
        r['texts'].append(((x.get('description') or '')+' | '+(x.get('seo') or '')+' | '+' '.join(x.get('keywords') or []))[:900])
E=json.load(open('exa_resolved_lt.json'))
for d,v in E['resolved'].items():
    if not v: continue
    c=v.get('company') or {}; hq=c.get('hq') or {}
    r=get(v['li'],d)
    if r is None: continue
    setf(r,name=c.get('name') or E['titles'].get(d),industry=c.get('industry'),employees=c.get('employees_on_linkedin'),size_band=c.get('size'),country=cc(hq.get('country_code')),city=hq.get('city'),state=hq.get('state'))
    r['sources'].add('EXA /search (+Blitz enrichment)'); r['flags'].add('exa_discovery')
    r['texts'].append(((c.get('about') or '')+' | '+(E['titles'].get(d) or ''))[:900])
for d in E['known_hits']:
    k=BYDOM.get(d)
    if k: R[k]['flags'].add('exa_discovery'); R[k]['sources'].add('EXA /search (+Blitz enrichment)')
# earlier dealer-network wide pool: bring in flow/hydraulics + power-equipment rule matches
W=pickle.load(open('../dn/wide2.pkl','rb')); nw=0
for k,w in W.items():
    if not (set(w.get('verts') or [])&{'flow_hydraulics','power_equipment'}): continue
    r=get(w['linkedin_url'],w['domain'])
    if r is None: continue
    setf(r,name=w.get('name'),industry=w.get('industry'),employees=w.get('employees'),size_band=w.get('size_band'),country=w.get('country'),city=w.get('city'),state=w.get('state'),revenue_range=w.get('revenue_range'),naics=w.get('naics'),keywords=w.get('keywords'))
    r['sources'].add('2026-10-07 dealer-network wide pool (flow/power rule match)'); r['flags'].add('from_dealer_network_wide'); r['texts'].append(' '.join(w['texts'])[:900]); nw+=1
print('from earlier wide pool',nw)
print('unique companies',len(R),'with linkedin',sum(1 for r in R.values() if r['linkedin_url']))
print(collections.Counter(len(r['sources']) for r in R.values()))
print('img placeholder',sum(1 for r in R.values() if 'site_image_placeholder_phrase' in r['flags']),'| site catalog phrase',sum(1 for r in R.values() if 'site_catalog_phrase' in r['flags']),'| catalog text any',sum(1 for r in R.values() if r['flags']&{'catalog_text_blitz','catalog_text_prospeo','catalog_text_aiark'}))
pickle.dump(R,open('wide_lt.pkl','wb'))
