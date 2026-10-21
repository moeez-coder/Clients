import json,csv,re,statistics as st,collections,math
D='/home/user/Clients/clients/vntana/sourcing/deep-catalog-manufacturers/'
a={x['company_linkedin_url']:x for x in json.load(open('crawl/audit_out.json'))}
q=list(csv.DictReader(open(D+'2026-10-21-companies-qualified-2.csv',encoding='utf-8')))
RATES={'low':0.027,'mid':0.05,'high':0.10}  # low = pooled placeholder rate observed in 6-page sample (floor); mid/high are ASSUMPTIONS pending VNTANA scorecard benchmark
def num(t):
    t=t.lower().replace('\u00a0',' ');b=0
    for m in re.finditer(r'(\d+(?:\.\d+)?)\s*(k\b|million\b|thousand\b|mil\b|m\b)?',t.replace(',','')):
        v=float(m.group(1));u=m.group(2)
        if u in('million','m'):v*=1e6
        elif u in('k','thousand','mil'):v*=1e3
        b=max(b,v)
    return int(min(b,1000000))  # cap: "N million configurations" claims are variants, not imaged SKUs
def band(e):
    e=int(e) if str(e).isdigit() else 0
    return '51-200' if e<201 else '201-500' if e<501 else '501-1000' if e<1001 else '1001+'
rows=[]
for x in q:
    s=a[x['company_linkedin_url']]
    smv=s['sitemap_product_like'] if isinstance(s['sitemap_product_like'],int) else 0
    stv=num(x['sku_count_quote']) if x['sku_count_stated']!='-' else 0
    rows.append((x,smv if smv>=50 else 0,stv if stv>=50 else 0,band(x['employees'])))
# model fallback: median measured count by (family, size band), else by size band
meas=collections.defaultdict(list);bandm=collections.defaultdict(list)
for x,sm,stv,b in rows:
    v=sm or stv
    if v: meas[(x['product_family'],b)].append(v);bandm[b].append(v)
def r2(n): 
    if n<=0:return 0
    d=int(math.floor(math.log10(n)))-1; return int(round(n,-d)) if d>0 else int(round(n))
out=[]
for x,sm,stv,b in rows:
    if sm and stv:
        ratio=max(sm,stv)/min(sm,stv); used=min(sm,stv) if ratio>3 else int((sm+stv)/2); basis='sitemap+stated'; conf='high' if ratio<=3 else 'medium'
    elif sm: used,basis,conf=sm,'sitemap_product_urls','medium'
    elif stv: used,basis,conf=stv,'stated_on_site','medium'
    else:
        k=(x['product_family'],b)
        pool=meas[k] if len(meas[k])>=5 else bandm[b]
        used=int(st.median(pool)) if pool else 0; basis='modeled_median_family_size' if len(meas[k])>=5 else 'modeled_median_size_band'; conf='low'
    o={'company_linkedin_url':x['company_linkedin_url'],'name':x['name'],'domain':x['domain'],'tier':x['tier'],'product_family':x['product_family'],'employees':x['employees'],
       'sku_count_basis':basis,'sku_count_used':used,'confidence':conf,'audit_status':a[x['company_linkedin_url']]['status'],
       'observed_placeholder_in_sample':'yes' if a[x['company_linkedin_url']]['placeholder_pages'] and not re.search(r'(lazy|loading|animated|spinner|captcha|pageplaceholder|blank|spacer|1x1|via\.placeholder|data:image|instagram|youtube)',a[x['company_linkedin_url']]['placeholder_examples'],re.I) else 'no'}
    for k,r in RATES.items(): o[f'est_missing_{k}']=r2(used*r)
    o['copy_phrase']=f"roughly {r2(used*RATES['mid']):,}" if used else '-'
    out.append(o)
with open(D+'2026-10-21-missing-image-estimates.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0].keys()));w.writeheader();[w.writerow({k:(str(v) if str(v)!='' else '-') for k,v in o.items()}) for o in out]
print(collections.Counter((o['confidence'],o['sku_count_basis']) for o in out))
vals=sorted(o['est_missing_mid'] for o in out);print('mid est: min',vals[0],'median',vals[len(vals)//2],'p90',vals[int(len(vals)*.9)],'max',vals[-1],'sum',sum(vals))
print(collections.Counter(b for _,_,_,b in rows))
