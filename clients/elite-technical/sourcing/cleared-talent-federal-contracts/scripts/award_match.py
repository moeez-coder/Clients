import json,re,sys,collections
S=sys.argv[1]
comp={u:c for u,c in json.load(open(S+'/blitz_company_sweep.json')).items() if c.get('revenue_range')=='$100M-$1B'}
AB={'District of Columbia':'DC','Maryland':'MD','Virginia':'VA','Maine':'ME','New Hampshire':'NH','Vermont':'VT','Massachusetts':'MA','Rhode Island':'RI','Connecticut':'CT','New York':'NY','New Jersey':'NJ','Pennsylvania':'PA','Delaware':'DE','North Carolina':'NC','South Carolina':'SC','Georgia':'GA','Florida':'FL','Ohio':'OH','Michigan':'MI','Indiana':'IN','Illinois':'IL','Wisconsin':'WI','Minnesota':'MN','Iowa':'IA','Missouri':'MO','North Dakota':'ND','South Dakota':'SD','Nebraska':'NE','Kansas':'KS'}
STOP=set('INC INCORPORATED LLC L C CORP CORPORATION CO COMPANY LTD LP LLP PLLC PC THE JV JOINT VENTURE GROUP HOLDINGS SERVICES SERVICE SOLUTIONS TECHNOLOGIES TECHNOLOGY INTERNATIONAL FEDERAL US USA AND OF DBA DOING BUSINESS AS AMERICA AMERICAN NORTH SYSTEMS'.split())
def toks(s): return [w for w in re.sub(r'[^A-Z0-9 ]',' ',(s or '').upper()).split() if w not in STOP]
BAD=re.compile(r'\b(OPTION|EXTENSION|EXTEND|BRIDGE|RENEW|RENEWAL|CONTINUATION|EXERCISE)\b',re.I)
aw=[]
for f in ['/usas_12mo_raw.json','/usas_wide_raw.json']:
  for x in json.load(open(S+f)):
    if BAD.search(x.get('Description') or ''): continue
    x['_src']='usaspending'; aw.append(x)
for o in json.load(open(S+'/dod_awards.json')):
  if o['tier']: aw.append({'Recipient Name':o['company'],'_state':{v:k for k,v in AB.items()}.get(o['state'],o['state']) if len(o['state'])>2 else o['state'],'_st_full':o['state'],'Award Amount':o['amount'] or 0,'_src':'war.gov','Description':o['summary'],'Awarding Agency':'Department of Defense','Awarding Sub Agency':o['branch'],'award_date':o['award_date'],'url':o['url'],'Award ID':None,'generated_internal_id':None})
# DoD state stored as full name; normalise to abbrev
for a in aw:
  if a['_src']=='war.gov': a['_state']=AB.get(a.get('_st_full'),a['_state'])
idx=collections.defaultdict(list)
for a in aw:
  t=toks(a['Recipient Name'])
  for w in set(t): idx[(a['_state'],w)].append(a)
matches={}
for u,c in comp.items():
  st=AB.get((c.get('hq') or {}).get('state'))
  bt=toks(c.get('name'))
  if not bt or not st: continue
  if len(bt)==1 and len(bt[0])<5: continue
  cands=idx.get((st,bt[0]),[])
  hits=[]
  for a in cands:
    rt=toks(a['Recipient Name'])
    if set(bt)<=set(rt) and (len(rt)-len(bt))<=2 and rt[:len(bt)]==bt: hits.append(a)
  if hits:
    best=max(hits,key=lambda a:a.get('Award Amount') or 0)
    matches[u]={'company':c,'award':best,'n_awards':len(hits)}
json.dump(matches,open(S+'/award_matches.json','w'))
print('companies in band',len(comp),'with award match',len(matches))
print(collections.Counter(AB.get(m['company']['hq']['state']) for m in matches.values()).most_common(10))
print(collections.Counter(m['company'].get('industry') for m in matches.values()).most_common(12))
import random; random.seed(1)
for m in random.sample(list(matches.values()),15): print(' ',m['company']['name'],'<=',m['award']['Recipient Name'],'|',(m['award'].get('Description') or '')[:60])
