import csv,json,glob,collections,re,unicodedata
def key(n):
    n=unicodedata.normalize('NFKD',n or '').encode('ascii','ignore').decode().lower()
    n=re.sub(r'\b(inc|llc|ltd|limited|gmbh|ag|sa|plc|corp|corporation|co|company|group|s\.?p\.?a|b\.?v)\b\.?','',n)
    return re.sub(r'[^a-z0-9]','',n)
CL={}
for f in sorted(glob.glob('batches/cls_[0-9].csv')):
    for r in csv.DictReader(open(f,encoding='utf8',errors='ignore')): CL[r['key'].strip()]=r
B=json.load(open('brands.json')); R=json.load(open('client_rows.json'))
G=collections.defaultdict(list)
for r in R: G[key(r['client_name'])].append(r)
DNC={'johnsonjohnson','jnj','janssen','abinbev','anheuserbusch','anheuserbuschinbev','bobcat','doosanbobcat','fruitoftheloom','astec','astecindustries','cottoninc','kohler','michaelkors','patagonia','puma','nureg','quad','quadgraphics','ykk','sony','accenture','accenturesong','michaels','costco','costcowholesale','kirklandsignature','xsolla','millerknoll','hermanmiller','knoll','knollstudio','doosan','tacocomfort','tacocomfortsolutions'}
CUST={'drilquip','adidas','vf','vfcorp','vfcorporation','pvh','pvhcorp','aldo','aldo','hanesbrands','giorgioarmani','armani','meta','metaplatforms','ptc','timberland','hugoboss','boss','deckers','deckersbrands','dickies','diesel','pepkor','arcteryx','wolverine','wolverineworldwide','decorgrates','idealfastener','idealfastenercorporation','roeslien','roeslienassociates','calvinklein','tommyhilfiger','thenorthface','northface','vans','michaels'}
def flag(b,c):
    ks={key(b['client_name']),key(c.get('likely_company'))}
    ks|={k.replace('the','',1) for k in ks}
    if ks&DNC or any(k.startswith(('sony','johnsonjohnson','doosan','kohler','costco','puma')) for k in ks): return 'DNC (tracking_clients dncList)'
    if ks&CUST: return 'existing VNTANA customer (per client brief/site)'
    return '-'
CORE={'industrial_equipment_machinery','automotive_mobility','building_products_home','medical_devices','other_manufacturer'}
MAKER={'furniture','consumer_durables_electronics','fashion_footwear_apparel','consumer_goods_cpg'}
out=[]
for b in B:
    c=CL.get(b['key'],{}); seg=c.get('vntana_segment') or 'unknown'; size=c.get('company_size_guess') or 'unknown'
    fl=flag(b,c)
    if fl!='-': pr='EXCLUDE'
    elif seg in CORE and size in('enterprise','mid'): pr='P1'
    elif seg in MAKER and size in('enterprise','mid'): pr='P2'
    elif seg in CORE|MAKER: pr='P3'
    else: pr='SKIP'
    AD=re.compile(r'(airbus|boeing|general dynamics|lockheed|raytheon|rtx|northrop|bae systems|curtiss|avionics|aerospace|defen[cs]e|thales|leonardo|saab|rafael|elbit|embraer|dassault aviation|safran|rolls-royce|gmf aero|helicopter)',re.I)
    if pr=='P1' and AD.search((b['client_name'] or '')+' '+(c.get('likely_company') or '')+' '+(c.get('note') or '')): pr='P3'; c=dict(c,note='aerospace/defense primary = VNTANA ICP disqualifier; '+(c.get('note') or ''))
    rs=G[b['key']]; ags=sorted({r['agency_name'] for r in rs})
    urls=[]
    for r in rs:
        if r['evidence_url'] not in urls: urls.append(r['evidence_url'])
    out.append({'client_name':b['client_name'],'likely_company':c.get('likely_company') or 'unknown','pitch_priority':pr,'vntana_segment':seg,'physical_product_maker':c.get('is_physical_product_maker') or 'unknown','size_guess':size,'classification_confidence':c.get('confidence') or 'low','flag':fl,'n_agencies':len(ags),'agencies':'; '.join(ags),'agency_linkedin_urls':'; '.join(sorted({r['agency_linkedin_url'] for r in rs})),'evidence_urls':' ; '.join(urls[:3]),'evidence_quote':(rs[0]['evidence_quote'] or '-').replace('\n',' ')[:200],'evidence_type':'; '.join(sorted({r['evidence_type'] for r in rs})),'company_linkedin_url':'-','note':c.get('note') or '-'})
order={'P1':0,'P2':1,'P3':2,'SKIP':3,'EXCLUDE':4}
out.sort(key=lambda r:(order[r['pitch_priority']],-r['n_agencies'],r['client_name'].lower()))
for r in out:
    for k,v in r.items():
        if v in ('',None): r[k]='-'
D='/home/user/Clients/clients/vntana/sourcing/cad-render-agencies/'
w=csv.DictWriter(open(D+'2026-09-28-agency-clients.csv','w',newline=''),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
L=[{'agency_linkedin_url':r['agency_linkedin_url'],'agency_name':r['agency_name'],'agency_domain':r['agency_domain'] or '-','client_name':r['client_name'],'evidence_type':r['evidence_type'] or '-','evidence_url':r['evidence_url'] or '-','evidence_quote':(r['evidence_quote'] or '-').replace('\n',' ')} for r in R]
w=csv.DictWriter(open(D+'2026-09-28-agency-client-links.csv','w',newline=''),fieldnames=list(L[0])); w.writeheader(); w.writerows(L)
print('classified',sum(1 for b in B if b['key'] in CL),'/',len(B))
print(collections.Counter(r['pitch_priority'] for r in out)); print(len(L),'links; agencies with clients',len({r['agency_linkedin_url'] for r in R}))
print('P1',collections.Counter(r['vntana_segment'] for r in out if r['pitch_priority']=='P1'))
print('P2',collections.Counter(r['vntana_segment'] for r in out if r['pitch_priority']=='P2'))
print([(r['client_name'],r['flag'][:8]) for r in out if r['pitch_priority']=='EXCLUDE'])
print([r['client_name'] for r in out if r['pitch_priority']=='P1' and r['vntana_segment']=='industrial_equipment_machinery'][:60])
