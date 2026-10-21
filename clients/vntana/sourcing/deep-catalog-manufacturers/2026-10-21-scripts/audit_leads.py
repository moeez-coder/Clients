import csv,re,glob,collections,json
A='audit2/'
def load(ds):
    r=[]
    for d in ds: r+=list(csv.DictReader(open(A+d+'/out.csv',encoding='utf-8')))
    return r
L1=load(['b1','b2','b3']);L2=load(['b4','b5','b6'])
D='/home/user/Clients/clients/vntana/sourcing/deep-catalog-manufacturers/'
sku=list(csv.DictReader(open(D+'2026-10-21-sku-counts.csv',encoding='utf-8')))
def nu(u): return re.sub(r'/+$','',(u or '').lower().replace('http://','https://').replace('://www.','://').split('?')[0])
def nn(s):
    s=(s or '').lower();s=re.sub(r'\b(inc|llc|ltd|co|corp|corporation|company|gmbh|limited|group|usa|us|international|the)\b','',s);return re.sub(r'[^a-z0-9]','',s)
byurl={nu(x['company_linkedin_url']):x for x in sku}
byname=collections.defaultdict(list)
for x in sku: byname[nn(x['name'])].append(x)
bydom={x['domain'].lower().replace('www.',''):x for x in sku}
print('lists',len(L1),len(L2))
for nm,L in (('L1',L1),('L2',L2)):
    urls=[nu(x['profileUrl']) for x in L]
    c=collections.Counter(urls);print(nm,'unique',len(c),'dups within',sum(1 for v in c.values() if v>1))
u1={nu(x['profileUrl']) for x in L1};u2={nu(x['profileUrl']) for x in L2}
both=u1&u2;print('in BOTH lists',len(both),'| only L1',len(u1-u2),'| only L2',len(u2-u1))
def blank(v): return v in('','null','NONE',None)
for nm,L in (('L1',L1),('L2',L2)):
    print(nm,'blank first',sum(blank(x['firstName']) for x in L),'blank company',sum(blank(x['companyName']) for x in L),'blank/NONE sku',sum(blank(x['sku']) for x in L),'non-numeric sku',sum(1 for x in L if not blank(x['sku']) and not re.fullmatch(r'\d+',x['sku'].replace(',',''))),'null companyUrl',sum(blank(x['companyUrl']) for x in L),'null position',sum(blank(x['position']) for x in L))
    print(nm,'sku with comma/rounded?',sum(1 for x in L if ',' in x['sku']),'ends 00',sum(1 for x in L if re.fullmatch(r'\d*00',x['sku'])))
# sku parity
res=collections.Counter();bad=[]
def lookup(x):
    u=nu(x['companyUrl']) if not blank(x['companyUrl']) else None
    if u and u in byurl: return byurl[u],'url'
    m=byname.get(nn(x['companyName']))
    if m and len(m)==1: return m[0],'name'
    return None,'none'
for nm,L in (('L1',L1),('L2',L2)):
    for x in L:
        s,how=lookup(x)
        if not s: res[(nm,'unmatched')]+=1;bad.append((nm,'UNMATCHED',x['companyName'],x['sku']));continue
        try: v=int(x['sku'].replace(',',''))
        except: res[(nm,'nonnumeric')]+=1;bad.append((nm,'NONNUM',x['companyName'],x['sku']));continue
        if v==int(s['sku_count_used']): res[(nm,'match_'+how)]+=1
        else: res[(nm,'MISMATCH')]+=1;bad.append((nm,'MISMATCH',x['companyName'],x['sku'],s['sku_count_used']))
print(dict(res))
for b in bad[:25]:print(b)
# companies
cs=collections.defaultdict(set)
for L in (L1,L2):
    for x in L: cs[nn(x['companyName'])].add(x['companyName'])
print('distinct companies',len(cs))
# inconsistent sku within company
inc=collections.defaultdict(set)
for x in L1+L2: inc[nn(x['companyName'])].add(x['sku'])
print('companies with >1 distinct sku value',sum(1 for v in inc.values() if len(v)>1))
# titles
EXC=re.compile(r'\b(security|cyber|cfo|chief financial|finance|financial|accounting|controller|procurement|purchasing|human resources|hr\b|recruit|legal|counsel|compliance|analytics|intern|assistant|sales representative|account executive|account manager|sales manager|director of sales|vp sales|vice president.{0,12}sales|inside sales|sales development|business development representative|sdr|bdr)\b',re.I)
INC=re.compile(r'(digital|aftermarket|service|marketing|ecommerce|e-commerce|communications|creative|information officer|cio|cto|technolog|technical|it\b|business development|operations|business operations|product|3d|visualization|architecture|growth)',re.I)
AD=re.compile(r'(aerospace|defen[cs]e|space|military|aviation|aircraft)',re.I)
DNC=re.compile(r'\b(bobcat|astec|doosan|kohler|patagonia|puma|ykk|sony|accenture|xsolla|costco|millerknoll|miller knoll|herman miller|knoll|michael kors|johnson & johnson|anheuser|taco comfort|cotton incorporated|fruit of the loom|nureg|quad)\b',re.I)
for nm,L in (('L1',L1),('L2',L2)):
    e=[x for x in L if EXC.search(x['position'])];a=[x for x in L if AD.search(x['position'])];d=[x for x in L if DNC.search(x['companyName'])]
    ni=[x for x in L if not INC.search(x['position'] or '') ]
    print(nm,'EXCLUDE-title hits',len(e),'A&D in title',len(a),'DNC company hits',len(d),'title matches no include keyword',len(ni))
    if nm=='L1':
        for x in e[:12]:print('  EXC',x['position'][:60],'|',x['companyName'])
        for x in a[:8]:print('  A&D',x['position'][:60],'|',x['companyName'])
        for x in d[:8]:print('  DNC',x['position'][:50],'|',x['companyName'])
        for x in ni[:15]:print('  NOINC',x['position'][:60],'|',x['companyName'])
# prior repo overlap
prior=set()
for f in glob.glob('/home/user/Clients/clients/vntana/sourcing/**/*leads*.csv',recursive=True):
    try:
        for r in csv.DictReader(open(f,encoding='utf-8',errors='ignore')):
            u=r.get('linkedin_url') or r.get('profileUrl') or ''
            if '/in/' in u: prior.add(nu(u))
    except: pass
print('prior repo leads',len(prior),'L1 overlap',len(u1&prior),'L2 overlap',len(u2&prior))

print('\n=== PASS 2 ===')
vals={x['sku_count_used'] for x in sku}
def toks(s): return set(re.findall(r'[a-z0-9]{3,}',(s or '').lower()))-{'inc','llc','ltd','corp','corporation','company','the','group','usa','international','industries','now','and'}
um=collections.Counter();detail=[]
for nm,L in (('L1',L1),('L2',L2)):
    for x in L:
        s,how=lookup(x)
        if s: continue
        if blank(x['companyName']): um[(nm,'null_company')]+=1;continue
        t=toks(x['companyName']);cand=[y for y in sku if t and (toks(y['name'])&t) and y['sku_count_used']==x['sku'].replace(',','')]
        if cand: um[(nm,'fuzzy_name_and_value_match')]+=1
        elif x['sku'] in vals: um[(nm,'value_exists_for_other_company')]+=1;detail.append((nm,x['companyName'],x['sku']))
        else: um[(nm,'NO_MATCH_value_not_in_file')]+=1;detail.append((nm,x['companyName'],x['sku']))
print(dict(um))
for d in detail[:20]:print(d)
# mismatches
for nm,L in (('L1',L1),('L2',L2)):
    for x in L:
        s,how=lookup(x)
        if s and not blank(x['sku']) and int(x['sku'])!=int(s['sku_count_used']): print('MISMATCH',nm,x['companyName'],'sent',x['sku'],'file',s['sku_count_used'],s['name'])
# null company with sku: which share of leads
print('null-company leads L1/L2',sum(blank(x['companyName']) for x in L1),sum(blank(x['companyName']) for x in L2))
# strict violations
STRICT=re.compile(r'(security|cyber|\bcfo\b|chief financial|\bfinance\b|financial officer|\bhr\b|human resources|recruit|legal|counsel|procurement|purchasing)',re.I)
AD2=re.compile(r'(aerospace|defen[cs]e|military|\bspace programs?\b|aviation|aircraft)',re.I)
for nm,L in (('L1',L1),('L2',L2)):
    s=[(x['position'][:55],x['companyName']) for x in L if STRICT.search(x['position'] or '')]
    a=[(x['position'][:55],x['companyName']) for x in L if AD2.search(x['position'] or '')]
    print(nm,'strict exclude',len(s),s[:8]);print(nm,'A&D',len(a),a)
# who is in both lists, sample + whether same company
both_rows=[x for x in L1 if nu(x['profileUrl']) in both]
print('both sample',[(x['firstName'],x['companyName']) for x in both_rows[:10]])
# leads per company
cnt=collections.Counter(nn(x['companyName']) for x in L1+L2 if not blank(x['companyName']))
print('max leads/company',cnt.most_common(5))
dist=collections.Counter(cnt.values());print('leads per company dist',sorted(dist.items())[:10])
# unique persons overall, companies covered vs 1000
pc=len({nn(x['companyName']) for x in L1+L2 if not blank(x['companyName'])});print('distinct non-null companies',pc)

# ---- flags file ----
import os
rows=[]
STRICT2=re.compile(r'(security|cyber|\bcfo\b|chief financial|\bfinance\b|\bhr\b|human resources|recruit|legal|counsel|procurement|purchasing)',re.I)
for nm,L in (('Offer1_1049528',L1),('Offer2_1049529',L2)):
    for x in L:
        f=[]
        if nu(x['profileUrl']) in both: f.append('in_both_lists')
        if blank(x['companyName']): f.append('null_company_name(fallback message would send)')
        if blank(x['position']): f.append('null_position')
        if STRICT2.search(x['position'] or ''): f.append('excluded_title(security/cyber/HR/finance/legal/procurement)')
        if AD2.search(x['position'] or ''): f.append('aerospace_defense_title')
        s,how=lookup(x)
        if s and not blank(x['sku']) and int(x['sku'])!=int(s['sku_count_used']): f.append(f"sku_mismatch(file={s['sku_count_used']})")
        if not s and not blank(x['companyName']):
            t=toks(x['companyName']);cand=[y for y in sku if t and (toks(y['name'])&t) and y['sku_count_used']==x['sku'].replace(',','')]
            if not cand: f.append('company_name_not_matching_sku_source(person may have moved)')
        if nu(x['profileUrl']) in prior: f.append('already_in_earlier_repo_leads_file')
        if f: rows.append([nm,x['profileUrl'],x['firstName'],x['lastName'],x['companyName'],x['position'],x['sku'],'; '.join(f)])
out='/home/user/Clients/clients/vntana/sourcing/deep-catalog-manufacturers/2026-10-21-heyreach-lead-audit.csv'
with open(out,'w',newline='',encoding='utf-8') as fo:
    w=csv.writer(fo);w.writerow(['heyreach_list','linkedin_url','first_name','last_name','company_name','position','sku','flags']);w.writerows([[('-' if (c in('null','') ) else c) for c in r] for r in rows])
print('flag rows',len(rows),collections.Counter(fl.split('(')[0] for r in rows for fl in r[-1].split('; ')))
