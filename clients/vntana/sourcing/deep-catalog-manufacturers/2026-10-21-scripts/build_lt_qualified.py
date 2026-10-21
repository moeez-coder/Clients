import json,csv,re,glob,pickle,collections
S='/home/user/Clients/clients/vntana/sourcing/'
keep={x['i']:x for x in json.load(open('keep_lt.json'))}
ev=json.load(open('exa_catalog_out.json'))
cand=pickle.load(open('cand_lt_final.pkl','rb'))
def norm(s): return re.sub(r'\s+',' ',(s or '').replace(' ',' ')).strip().lower()
ext={}
for k in range(10):
    for r in csv.DictReader(open(f'ext/w{k}/out_e{k}.csv',encoding='utf-8')): ext[int(r['i'])]=r
print('ext rows',len(ext))
DNC_DOM={"jnj.com","ab-inbev.com","bobcat.com","fruit.com","astecindustries.com","cottoninc.com","kohler.com","michaelkors.com","patagonia.com","puma.com","nureg.de","quad.com","ykk.com","sony.com","accenture.com","michaels.com","costco.com","xsolla.com","millerknoll.com","doosan.com","tacocomfort.com"}
DNC_BRAND={'jnj','johnsonandjohnson','abinbev','bobcat','fruit','astec','astecindustries','cottoninc','kohler','michaelkors','patagonia','puma','nureg','quad','ykk','sony','accenture','michaels','costco','xsolla','millerknoll','hermanmiller','doosan','tacocomfort'}
DNC_NAME=re.compile(r'\b(bobcat|astec|doosan|kohler|patagonia|puma|ykk|sony|accenture|xsolla|costco|millerknoll|miller ?knoll|herman miller|knoll|michael kors|johnson & johnson|anheuser|taco comfort|cotton incorporated|fruit of the loom|nureg|quad/graphics|quad graphics)\b',re.I)
def dnc(x):
    d=(x['domain'] or '').lower().replace('www.','')
    if d in DNC_DOM: return True
    lab=d.split('.')[0]
    if lab in DNC_BRAND: return True
    return bool(DNC_NAME.search(x['name'] or ''))
# previously sourced domains
prev=set()
for f in glob.glob(S+'**/*companies*.csv',recursive=True)+glob.glob(S+'*.csv'):
    if 'deep-catalog' in f: continue
    try:
        for r in csv.DictReader(open(f,encoding='utf-8',errors='ignore')):
            for c in ('domain','company_domain','website','primary_domain'):
                v=(r.get(c) or '').lower().replace('https://','').replace('http://','').replace('www.','').split('/')[0]
                if v and v!='-': prev.add(v)
    except Exception as e: pass
def num(q):
    q=q.lower().replace(' ',' ')
    best=0
    for m in re.finditer(r'(\d[\d,\.]*)\s*(k\b|million|m\b|thousand)?\+?',q):
        t=m.group(1).replace(',','')
        try: v=float(t)
        except: continue
        u=m.group(2)
        if u in('million','m'): v*=1e6
        elif u in('k','thousand'): v*=1e3
        best=max(best,v)
    return int(best)
PROD=re.compile(r'(product|sku|part|item|model|variant|catalog|component|fastener|valve|pump|fitting|connector|cable|bearing|tool|type|size|configur)',re.I)
stats=collections.Counter();rows=[]
for i,x in keep.items():
    e=ext.get(i)
    if not e: stats['no_ext']+=1; continue
    if dnc(x): stats['dnc']+=1; continue
    if x['cls_type']=='distributor_reseller' or 'ibselectronics' in (x['name'] or '').lower() or 'ibselectronics' in (x['domain'] or ''): stats['distributor']+=1; continue
    key=str(i); pages=ev.get(key,{}).get('pages',[]) if key in ev else []
    evtext=norm(' '.join((p.get('title') or '')+' '+(p.get('hl') or '') for p in pages))
    q=e['count_quote']; verified='-'; cnt=0
    if q!='-':
        if norm(q) in evtext: verified='yes'; cnt=num(q)
        else: verified='no'
    depth=e['depth']; ct=e['catalog_type']; ph=e['placeholder']
    if verified=='yes' and cnt>=1000 and PROD.search(q): tier='L1_stated_1000plus'
    elif ph=='yes' and ct!='none_found': tier='L1_placeholder_images_seen'
    elif depth in('deep','likely') and ct!='none_found': tier='L2_deep_catalog_evidenced'
    elif depth in('deep','likely'): tier='L3_catalog_claimed_no_channel'
    elif x['cls_catalog_depth']=='deep' and depth=='unclear': tier='L3_classifier_deep_no_site_evidence'
    elif depth=='shallow': stats['shallow_drop']+=1; continue
    else: tier='L4_low_confidence'
    c=cand[i]
    rows.append({'company_linkedin_url':c['linkedin_url'],'name':x['name'],'domain':x['domain'],'country':x['country'],'employees':x['employees'],'industry':x['industry'],
      'product_family':x['cls_family'],'company_type':x['cls_type'],'classifier_keep':x['cls_keep'],'classifier_catalog_depth':x['cls_catalog_depth'],'classifier_channel':x['cls_channel'],
      'tier':tier,'sku_count_stated':e['sku_count'] if verified=='yes' else '-','sku_count_quote':q if verified=='yes' else '-','count_quote_verified':verified,'catalog_type':ct,'configurator':e['configurator'],'placeholder_image_text_seen':ph,'site_depth_read':depth,
      'evidence_url':e['evidence_url'],'catalog_signals':'; '.join(sorted(c['flags'])) or '-','candidate_group':c['grp'],'prev_sourced_in_repo':'yes' if (x['domain'] or '').lower() in prev else 'no','classifier_reason':x['cls_reason']})
    stats[tier]+=1
order=['L1_stated_1000plus','L1_placeholder_images_seen','L2_deep_catalog_evidenced','L3_catalog_claimed_no_channel','L3_classifier_deep_no_site_evidence','L4_low_confidence']
rows.sort(key=lambda r:(order.index(r['tier']),-(int(r['employees']) if str(r['employees']).isdigit() else 0)))
out='/home/user/Clients/clients/vntana/sourcing/deep-catalog-manufacturers/2026-10-21-companies-qualified.csv'
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader()
    for r in rows: w.writerow({k:(str(v).replace('\n',' ').strip() or '-') for k,v in r.items()})
print(len(rows),dict(stats))
print('quote unverified',sum(1 for r in rows if r['count_quote_verified']=='no'))
print('prev',sum(1 for r in rows if r['prev_sourced_in_repo']=='yes'),'US/CA/GB/IE/AU/NZ',sum(1 for r in rows if r['country'] in('US','CA','GB','IE','AU','NZ')))
print(collections.Counter(r['product_family'] for r in rows))
