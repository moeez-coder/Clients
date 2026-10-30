import json,csv,re,glob,collections,urllib.parse
A=json.load(open('accounts.json'));E=json.load(open('exa_products.json'));R={o['i']:o for o in json.load(open('resolved.json'))};PG={int(k):v for k,v in json.load(open('pages.json')).items()}
def norm(s): return re.sub(r'\s+',' ',(s or '').replace(' ',' ')).strip().lower()
B='https://vntana-store-production.up.railway.app/custom/'
DEMO={'skid_steer':B+'skid-steer-explorer','crane':B+'tadano-crane-explorer.html','sunsource':B+'sunsource','hvac_pump':B+'taco-007e.html','machine_tools':B+'imts','components':B+'imts-consumables','parts_catalog':B+'parts','process':B+'roeslein-adb.html','viewer':B+'product?uuid=ca4aebfc-ebc6-4e79-b4e7-8ce4bca4d58d&org=DCicero&workspace=example-files'}
P={}
for k in range(4):
    for r in csv.DictReader(open(f'w{k}/out_p{k}.csv',encoding='utf-8')): P[int(r['i'])]=r
print('research rows',len(P))
acc=[];qfail=0
for i,a in enumerate(A):
    r=P.get(i);o=R[i]
    if not r: continue
    ev=norm(' '.join((p['title'] or '')+' '+(p['hl'] or '') for p in E[str(i)]['pages']))
    q=r['product_quote'];ok='-'
    if q!='-':
        ok='yes' if norm(q) in ev else 'no'
        if ok=='no': qfail+=1
    prod=r['product'] if ok!='no' else '-'
    pg=PG.get(i) or [];li=pg[0]['li'] if pg else None;dom=(pg[0].get('domain') or o['domain']) if pg else None
    ready='yes' if (prod!='-' and r['confidence'] in('high','medium') and r['product_recent']=='yes' and li) else 'review'
    acc.append({'idx':i,'account':o['name'],'client_name':a['client_name'],'company_linkedin_url':li or '-','all_company_pages':' | '.join(p['li'] for p in pg) or '-','domain':dom or '-','what_they_make':a['what_they_make'],'segment':a['vntana_segment'],'product':prod,'product_quote':q if ok=='yes' else '-','product_url':r['product_url'] if ok=='yes' else '-','product_recent':r['product_recent'] if prod!='-' else '-','category':r['category'],'demo_key':r['demo'],'demo_link':DEMO.get(r['demo'],DEMO['viewer']),'research_confidence':r['confidence'],'render_copy_ready':ready,'quote_verified':ok})
print('quote failures',qfail,'ready',sum(1 for x in acc if x['render_copy_ready']=='yes'),collections.Counter(x['research_confidence'] for x in acc),collections.Counter(x['demo_key'] for x in acc))
json.dump(acc,open('accounts_final.json','w'))
# people
def nu(u): return re.sub(r'/+$','',(u or '').lower().replace('http://','').replace('https://','').replace('www.','').split('?')[0])
byli=collections.defaultdict(list)
for x in acc:
    for pu in PG.get(x['idx'],[]): byli[nu(pu['li'])].append(x)
def root(d): 
    d=(d or '').lower().replace('www.','');p=d.split('.');return '.'.join(p[-2:]) if len(p)>1 else d
bydom=collections.defaultdict(list)
for x in acc:
    for pu in PG.get(x['idx'],[]):
        if pu.get('domain'): bydom[root(pu['domain'])].append(x)
SC=[(100,r'product marketing|marketing communications|marcom|director of marketing|head of marketing|marketing director|vp.{0,12}marketing|vice president.{0,15}marketing|chief marketing|e-?commerce|digital experience|digital transformation|chief digital|head of digital|vp of digital|vice president.{0,10}digital|3d visual'),
    (80,r'aftermarket|digital product|chief information|\bcio\b|\bcto\b|technology|business architecture|global technical'),
    (65,r'creative|growth marketing|business development|product manager|operations manager|business operations')]
EXC=re.compile(r'(security|cyber|\bcfo\b|chief financial|finance|financial|accounting|controller|human resources|\bhr\b|recruit|legal|counsel|compliance|procurement|purchasing|sales representative|account executive|account manager|sales manager|director of sales|\bvp\b.{0,4}sales|inside sales|sdr\b|bdr\b|intern\b|student|assistant|retired|advisor|board member|people |talent|analyst|engineer|developer|consultant)',re.I)
AERO=re.compile(r'(aerospace|defen[cs]e|military|space programs?|aviation|aircraft)',re.I)
SEN=re.compile(r'(vice president|\bvp\b|head of|director|chief|global|senior director|svp|evp)',re.I)
rows=[];seen=set();stats=collections.Counter()
for f in sorted(glob.glob('pp3/*.jsonl')+glob.glob('pp/p*.jsonl')+glob.glob('pp2/*.jsonl')):
    for l in open(f):
        if not l.strip(): continue
        d=json.loads(l)
        if '_error' in d: continue
        p=d['person']
        p['first_name']=re.sub(r'^[^A-Za-z\u00C0-\u024F]+','',p.get('first_name') or '').strip()
        if not p.get('linkedin_url') or not p.get('first_name'): stats['noname']+=1;continue
        job=None;acct=None
        for j in d['jobs']:
            u=j.get('company_linkedin_url')
            cand=byli.get(nu(u)) or bydom.get(root(j.get('company_domain')))
            if cand: job=j;acct=cand[0];break
        if not job: stats['not_at_target']+=1;continue
        t=job.get('job_title') or ''
        if EXC.search(t) or AERO.search(t): stats['excluded_title']+=1;continue
        sc=0;tier=''
        for s,rx in SC:
            if re.search(rx,t,re.I): sc=s;break
        if not sc: stats['no_title_match']+=1;continue
        if SEN.search(t): sc+=10
        elif re.search(r'manager',t,re.I): sc+=5
        u=p['linkedin_url']
        if u in seen: continue
        seen.add(u)
        rows.append((acct['idx'],sc,t,p,job))
print(stats,len(rows))
byacct=collections.defaultdict(list)
for r in rows: byacct[r[0]].append(r)
leads=[]
for idx,L in byacct.items():
    L.sort(key=lambda r:-r[1])
    for r in L[:4]:
        if r[1]<75: continue
        a=acc[[x['idx'] for x in acc].index(idx)]
        p=r[3];loc=(p.get('location') or {})
        leads.append({'linkedin_url':p['linkedin_url'],'first_name':p['first_name'],'last_name':p.get('last_name') or '-','position':r[2],'title_score':r[1],'country':loc.get('country_code') or '-','company_name':a['account'],'company_linkedin_url':a['company_linkedin_url'],'domain':a['domain'],'product':a['product'],'category':a['category'],'demo_link':a['demo_link'],'render_copy_ready':a['render_copy_ready'],'research_confidence':a['research_confidence']})
leads.sort(key=lambda x:(x['company_name'],-x['title_score']))
print('leads',len(leads),'companies',len({l['company_name'] for l in leads}),'ready leads',sum(1 for l in leads if l['render_copy_ready']=='yes'))
json.dump(leads,open('leads_final.json','w'))
