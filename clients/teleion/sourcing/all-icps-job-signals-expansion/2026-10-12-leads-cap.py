import pickle,csv,collections,os,re,shutil
r=pickle.load(open('rows3.pkl','rb'))
def rank(x):
    t=x['job_title'].lower()
    s=0 if re.search(r"chief|ceo|chair|treasurer|\bcfo\b|\bciso\b|\bcio\b|chro",t) else 1
    return (s, 1 if 'group' in t else 0, len(t))
by=collections.defaultdict(list)
for x in r: by[(x['company_domain'],x['persona_group'])].append(x)
keep=[];cut=0
for k,v in by.items():
    v.sort(key=rank)
    keep+=v[:3];cut+=max(0,len(v)-3)
seen=set();fin=[]
for x in keep:
    if x['linkedin_url'] in seen: continue
    seen.add(x['linkedin_url']);fin.append(x)
o={'Compliance, Risk & Fraud':0,'AI & Data Governance':1,'Payments & Finance':2,'Executive Sponsor':3}
fin.sort(key=lambda x:(o[x['persona_group']],x['company_name']))
dd='/home/user/Clients/clients/teleion/sourcing/all-icps-job-signals-expansion'
f=dd+'/2026-10-12-leads.csv'
assert not os.path.exists(f)
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(fin[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(fin)
shutil.copy('people3.py',dd+'/2026-10-12-leads-filter.py');shutil.copy('final3.py',dd+'/2026-10-12-leads-cap.py')
print(len(r),'->',len(fin),'cut by cap',cut)
print(collections.Counter(x['persona_group'] for x in fin),len({x['company_domain'] for x in fin}))
print(collections.Counter(c for x in fin for c in x['signal_codes'].split(',')))
for x in fin[:5]+fin[-3:]: print(x['persona_group'][:6],x['full_name'],'|',x['job_title'],'|',x['company_name'],'|',x['signal_codes'])
