import csv,re,json,os,time,collections,urllib.request,concurrent.futures as cf
S='/home/user/Clients/clients/vntana/sourcing/'
KEY=os.environ['BLITZ_API_KEY']
def rd(f): return list(csv.DictReader(open(S+f,encoding='utf8',errors='ignore')))
def dom(u):
    u=re.sub(r'^https?://','',(u or '').lower()).split('/')[0].split(':')[0]; return re.sub(r'^www\.','',u)
def root(d):
    p=d.split('.')
    if len(p)>=3 and p[-2] in('co','com','org','net','gov','ac') and len(p[-1])==2: return '.'.join(p[-3:])
    return '.'.join(p[-2:]) if len(p)>=2 else d
def li(u):
    u=(u or '').strip().lower().split('?')[0].rstrip('/').replace('http://','https://')
    u=re.sub(r'https://[a-z]{2,3}\.linkedin\.com','https://www.linkedin.com',u); u=u.replace('https://linkedin.com','https://www.linkedin.com')
    return u if '/company/' in u else ''
# DNC (client list, identical to tracking_clients) + existing customers named in the client brief; match on name tokens and domain brand
DNCDOM={'jnj.com','ab-inbev.com','bobcat.com','fruit.com','astecindustries.com','cottoninc.com','kohler.com','michaelkors.com','patagonia.com','puma.com','nureg.de','quad.com','ykk.com','sony.com','accenture.com','michaels.com','costco.com','xsolla.com','millerknoll.com','doosan.com','tacocomfort.com'}
DNCTOK=['johnson & johnson','j&j','janssen','depuy','ethicon','ab inbev','anheuser','inbev','bobcat','fruit of the loom','astec','cotton incorporated','cotton, inc','kohler','michael kors','patagonia','puma','nureg','quad graphics','quad/graphics','ykk','sony','accenture','michaels stores','costco','xsolla','millerknoll','miller knoll','herman miller','knoll','doosan','taco comfort']
CUSTTOK=['dril-quip','drilquip','adidas','vf corp','pvh','aldo group','hanesbrands','armani','meta platforms','ptc inc','timberland','hugo boss','deckers','dickies','diesel s.p.a','pepkor','arc\'teryx','wolverine world','decor grates','ideal fastener','roeslien','calvin klein','tommy hilfiger','the north face','vans']
BRAND={d.split('.')[0].replace('-','') for d in DNCDOM if d not in('quad.com','michaels.com','fruit.com')}|{'bobcat','doosan','astec','kohler'}
def blocked(name,domain):
    n=(name or '').lower(); d=root(dom(domain)); lab=d.split('.')[0].replace('-','')
    if d in DNCDOM: return 'DNC domain'
    for t in DNCTOK:
        if re.search(r'(?<![a-z0-9])'+re.escape(t)+r'(?![a-z0-9])',n): return 'DNC name: '+t
    for b in BRAND:
        if len(b)>=5 and b in lab: return 'DNC domain-brand: '+b
    for t in CUSTTOK:
        if re.search(r'(?<![a-z0-9])'+re.escape(t)+r'(?![a-z0-9])',n): return 'existing customer: '+t
    return None
A={}  # key -> account
def add(key,**kw):
    a=A.setdefault(key,{'linkedin_url':'','name':'','domain':'','employees':0,'country':'','industry':'','vertical':'','src':[],'pts':0,'note':[]})
    for k in ('linkedin_url','name','domain','country','industry','vertical'):
        if kw.get(k) and not a[k]: a[k]=kw[k]
    try:
        e=int(float(kw.get('employees') or 0)); a['employees']=max(a['employees'],e)
    except: pass
    a['src'].append(kw['src']); a['pts']+=kw['pts']; 
    if kw.get('note'): a['note'].append(kw['note'])
# 1. triage FIT >=500
for x in rd('2026-09-16-us-icp-triage.csv'):
    if x['agent_verdict']!='FIT': continue
    try: e=int(float(x['employees']))
    except: e=0
    if e<500: continue
    k=li(x['linkedin_url']) or 'dom:'+root(dom(x['domain']))
    add(k,linkedin_url=li(x['linkedin_url']),name=x['company_name'],domain=root(dom(x['domain'])),employees=e,country='US',industry=x['industry'],src='us-icp-triage FIT (2026-09-16)',pts=2)
# 2. dealer-network qualified-2 >=500
for x in rd('dealer-network-manufacturers/2026-10-07-companies-qualified-2.csv'):
    e=int(x['employees']) if x['employees'].isdigit() else 0
    if e<500 or x['tier'].startswith('Q4'): continue
    pts={'Q1':3,'Q2':2,'Q3':1}[x['tier'][:2]]
    k=li(x['company_linkedin_url']) or 'dom:'+root(dom(x['domain']))
    add(k,linkedin_url=li(x['company_linkedin_url']),name=x['name'],domain=root(dom(x['domain'])),employees=e,country=x['country'],industry=x['industry'],vertical=x['vertical'],src='dealer-network '+x['tier'][:2]+' (2026-10-07)',pts=pts)
# 3. client's own IMTS "Yes" verdicts (need LinkedIn resolution)
imts=[x for x in rd('2026-09-15-imts-client-icp-verdicts.csv') if x['ICP']=='Yes']
def b(path,body):
    for a in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':KEY,'Content-Type':'application/json'}),timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in(429,500,502,503): time.sleep(2**a); continue
            return {'found':False}
        except Exception: time.sleep(2**a)
    return {'found':False}
def res(x):
    d=root(dom(x['Website']))
    if not d: return x,None,None
    r=b('/v2/enrichment/domain-to-linkedin',{'domain':d})
    if not r.get('found'): return x,d,None
    c=b('/v2/enrichment/company',{'company_linkedin_url':r['company_linkedin_url']}).get('company') or {}
    return x,d,(r['company_linkedin_url'],c)
with cf.ThreadPoolExecutor(10) as ex: R=list(ex.map(res,imts))
nolink=0
for x,d,r in R:
    if r is None: nolink+=1; 
    lu=li(r[0]) if r else ''; c=r[1] if r else {}
    hq=(c.get('hq') or {})
    add(lu or 'dom:'+(d or x['Exhibitor Name'].lower()),linkedin_url=lu,name=c.get('name') or x['Exhibitor Name'],domain=d or '',employees=c.get('employees_on_linkedin') or 0,country=hq.get('country_code') or '',industry=c.get('industry') or x['Industry'],src="client's own ICP 'Yes' verdict (IMTS 2026)",pts=3,note='Revenue(client file): '+(x['Total Revenue'] or '-'))
print('IMTS yes',len(imts),'without linkedin',nolink)
# DNC / customer filter
out={};drop=collections.Counter();dropped=[]
for k,a in A.items():
    why=blocked(a['name'],a['domain'])
    if why: drop[why.split(':')[0]]+=1; dropped.append((a['name'],a['domain'],why)); continue
    out[k]=a
print('accounts',len(A),'after DNC/customer filter',len(out),dict(drop))
print([d for d in dropped][:25])
print('with linkedin',sum(1 for a in out.values() if a['linkedin_url']),'| multi-source',sum(1 for a in out.values() if len(set(a['src']))>1))
print(collections.Counter(len(set(a['src'])) for a in out.values()))
json.dump({'accounts':out,'dropped':dropped},open('accounts.json','w'))
