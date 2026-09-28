import json,re,csv
def norm_li(u):
    if not u: return ''
    u=u.strip().rstrip('/').replace('http://','https://').replace('://linkedin','://www.linkedin')
    u=re.sub(r'https://[a-z]{2}\.linkedin','https://www.linkedin',u)
    return u.lower()
def dom(u):
    if not u: return ''
    u=re.sub(r'^https?://','',u.lower()).split('/')[0]
    return re.sub(r'^www\.','',u)
recs={}
def add(key,row,src):
    if not key: return
    if key in recs:
        recs[key]['sources'].add(src)
        for k,v in row.items():
            if not recs[key].get(k) and v: recs[key][k]=v
    else:
        row['sources']={src}; recs[key]=row
for r in json.load(open('raw.json'))['results']:
    hq=r.get('hq') or {}
    add(norm_li(r['linkedin_url']),dict(name=r['name'],domain=dom(r.get('domain') or r.get('website')),company_linkedin_url=norm_li(r['linkedin_url']),industry=r.get('industry'),employees=r.get('employees_on_linkedin') or '',size_range=r.get('size') or '',hq_city=hq.get('city') or '',hq_country=hq.get('country_code') or '',text=(r.get('about') or '')+' | '+' '.join(r.get('specialties') or [])),'Blitz /v2/search/companies')
for f,src in [('aiark_q1.json','AI Ark keyword'),('aiark_q2_0.json','AI Ark lookalike A'),('aiark_q2_1.json','AI Ark lookalike B')]:
    for r in json.load(open(f))['results']:
        s=r['summary'];l=r.get('link') or {};hq=(r.get('location') or {}).get('headquarter') or {}
        st=s.get('staff') or {};rg=st.get('range') or {}
        add(norm_li(l.get('linkedin')),dict(name=s['name'],domain=dom(l.get('domain') or l.get('website')),company_linkedin_url=norm_li(l.get('linkedin')),industry=s.get('industry'),employees=st.get('total') or '',size_range=f"{rg.get('start','')}-{rg.get('end','')}" if rg else '',hq_city=hq.get('city') or '',hq_country=hq.get('country') or '',text=(s.get('description') or '')+' | '+(s.get('seo') or '')+' | '+' '.join(r.get('keywords') or [])),src)
print('merged unique',len(recs))
json.dump({k:{**v,'sources':sorted(v['sources'])} for k,v in recs.items()},open('merged.json','w'))
T=json.load(open('exa_new_domains.json'))
for dm,v in json.load(open('exa_resolved.json')).items():
    if not v: continue
    c=v['company'] or {}; hq=c.get('hq') or {}
    add(norm_li(v['li']),dict(name=c.get('name') or v['name'],domain=dm,company_linkedin_url=norm_li(v['li']),industry=c.get('industry'),employees=c.get('employees_on_linkedin') or '',size_range=c.get('size') or '',hq_city=hq.get('city') or '',hq_country=hq.get('country_code') or '',text=(T.get(dm) or '')+' | '+(c.get('about') or '')+' | '+' '.join(c.get('specialties') or [])),'EXA /search (+ Blitz enrichment)')
json.dump({k:{**v,'sources':sorted(v['sources'])} for k,v in recs.items()},open('merged.json','w'))
print('merged unique incl EXA',len(recs))
