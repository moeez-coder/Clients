import csv,json,pickle,re,os,collections
cand=pickle.load(open('cand.pkl','rb'))
cls={}
for k in range(14):
    for r in csv.DictReader(open(f'cls/out_c{k}.csv',encoding='utf8',errors='ignore')): cls[int(r['i'])]=r
EV={}
for k in range(10):
    inp=json.load(open(f'ext/e{k}.json')); rows=list(csv.DictReader(open(f'ext/out_e{k}.csv',encoding='utf8',errors='ignore')))
    assert len(rows)==len(inp),(k,len(rows),len(inp))
    for r,x in zip(rows,inp):
        assert str(x['k'])==r['k'].strip() and x['name'][:12].strip().lower()==r['name_prefix'].strip().lower(),(k,x['k'])
        norm=lambda s:re.sub(r'\s+',' ',(s or '').lower())
        blob=norm(' '.join(p['text']+' '+p['title'] for p in x['pages']))
        r['_blob']=blob; r['_urls']={p['url'] for p in x['pages']}
        EV[int(r['k'])]=r
print('evidence rows',len(EV))
# verbatim verification of stated counts
n_stated=n_ok=0; 
for k,r in EV.items():
    if r['scale']=='50plus_stated':
        n_stated+=1
        ct=re.sub(r'\s+',' ',(r['count_text'] or '').lower()).strip(' .')
        nums=re.findall(r'\d[\d,]*',ct)
        ok=bool(ct and ct!='-' and (ct in r['_blob'] or (nums and all(n in r['_blob'] for n in nums[:2]) and len(ct)<=40)))
        r['verified']='yes' if ok else 'no'
        n_ok+=ok
    else: r['verified']='-'
print('50plus_stated',n_stated,'quote found in evidence',n_ok)
DNC={"jnj.com","ab-inbev.com","bobcat.com","fruit.com","astecindustries.com","cottoninc.com","kohler.com","michaelkors.com","patagonia.com","puma.com","nureg.de","quad.com","ykk.com","sony.com","accenture.com","michaels.com","costco.com","xsolla.com","millerknoll.com","doosan.com","tacocomfort.com"}
CUST_DOM={"drilquip.com","adidas.com","vfc.com","pvh.com","aldo.com","hanes.com","armani.com","meta.com","ptc.com","timberland.com","hugoboss.com","deckers.com","dickies.com","diesel.com","pepkor.co.za","arcteryx.com","wolverineworldwide.com","ideal-fastener.com"}
AD=re.compile(r'\b(aerospace|aircraft|avionics|defen[cs]e|missiles?|military|helicopters?)\b',re.I)
NA=('US','CA','GB','IE','AU','NZ')
out=[];stats=collections.Counter()
for i,c in cand.items() if isinstance(cand,dict) else enumerate(cand):
    d=cls[i]
    if d['keep'] not in ('Y','M'): continue
    ev=EV.get(i)
    dom=c['domain']
    tier=None; why=''
    if dom in DNC: stats['dnc']+=1; continue
    if dom in CUST_DOM: stats['customer']+=1; continue
    if d['type'] not in ('oem','component_oem'): stats['not_oem']+=1; continue
    if AD.search((d['reason'] or '')+' '+(c.get('name') or '')) and d['vertical']=='not_target': stats['aero']+=1; continue
    if d['vertical']=='not_target': stats['not_target']+=1; continue
    if ev is None:
        tier='Q4_no_site_evidence' if d['network'] in('yes','likely') else None
    else:
        loc=ev['locator']; nt=ev['network_type']; sc=ev['scale']
        if sc=='under50_stated': stats['under50']+=1; continue
        if sc=='50plus_stated' and ev['verified']=='yes': tier='Q1_verified_50plus'
        elif loc=='yes' and nt in('dealers','distributors','reps','mixed'): tier='Q2_network_evidenced_count_unstated' if sc!='50plus_stated' else 'Q2_network_evidenced_count_unverified'
        elif d['network']=='yes' and loc!='no': tier='Q3_network_claimed'
        elif d['network']=='likely' and d['keep']=='Y' and loc!='no': tier='Q4_likely_unverified'
        elif loc=='no' and nt=='none': stats['direct_only']+=1; continue
    if tier is None: stats['no_tier']+=1; continue
    out.append((i,c,d,ev,tier))
print(stats); print(collections.Counter(t for *_,t in out))
pickle.dump(out,open('qualified.pkl','wb'))
