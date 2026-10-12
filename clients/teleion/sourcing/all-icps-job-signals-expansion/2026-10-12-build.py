import json,csv,re,collections,os,sys,time,urllib.request,concurrent.futures as cf
sys.path.insert(0,'.')
from qdefs import Q
K=os.environ['BLITZ_API_KEY']
d=json.load(open('tam_raw.json'))
F="/root/.claude/uploads/394e1409-d675-5971-9524-30d3808207f0/7cb2e220-Teleion_target_accounts_with_signals-2-Default-view-export-1791818754556.csv"
base=list(csv.DictReader(open(F)))
nd=lambda x:re.sub(r'^https?://(www\.)?','',(x or '').lower()).strip('/').split('/')[0]
ex_li={x['linkedin_url'].lower().rstrip('/') for x in base};ex_d={nd(x['domain']) for x in base}
dnc=['amazon','starbucks','lyft','becu','gates foundation','gatesfoundation','microsoft','aws']
OK_IND=re.compile(r"^(Financial Services|Banking|Insurance|Hospitals and Health Care|Health.*|Medical.*|Pharmaceutical.*|Biotechnology.*|Software Development|Technology.*|Computer.*|Semiconductor.*|Telecommunications|Retail.*|Consumer.*|Food and Beverage.*|Apparel.*|.*Manufacturing|Online.*|E-Learning.*)$|^Information Services$|^Internet.*$|^Payments$",re.I)
RX={
 'P3':r"\b(bsa|aml|bank secrecy|anti[- ]money|money laundering|kyc|know your customer|ofac|sanctions|financial crimes?|transaction monitoring)\b",
 'P5':r"(model (risk|validation|governance)|ai governance|responsible ai|ai[ /-]*risk|artificial intelligence risk)",
 'P2':r"(\bbaas\b|banking[- ]as[- ]a[- ]service|embedded (finance|banking)|fintech (program|partner|relationship)|bank partner)",
 'M1':r"(payments? operations|treasury (operations|analyst)|card operations|payments? analyst|settlement analyst|reconciliation analyst)",
 'M2':r"(marketing compliance|content review|marketing legal|advertising compliance|marketing review|compliance review)",
 'E1':r"(ai governance|responsible ai|ai[ /-]*risk|ai compliance|ai policy|ai ethics|ai assurance)",
 'E2':r"(post[- ]merger|merger integration|m&a integration|integration management office|\bm&a\b)",
 'E3':r"(vendor management|contingent workforce|vendor governance|supplier management|managed services program|contract labor)",
}
MINJ={'P3':2,'M1':2,'E3':2}
PTS={'P3':20,'P2':30,'P5':10,'M1':15,'M2':20,'E1':20,'E2':10,'E3':10}
NAME={'P3':'Hiring BSA/AML/KYC analysts','P5':'AI / model-risk role posted','P2':'Bank-fintech partnership hiring (proxy)','M1':'Payments/Treasury/Card Ops analyst roles','M2':'Marketing compliance / content review roles','E1':'AI governance / responsible-AI roles','E2':'M&A integration roles (proxy)','E3':'Vendor / contingent-workforce mgmt roles (proxy)'}
cand={}
for c,rows in d.items():
    for r in rows:
        co=r['company']
        if (co['hq'] or {}).get('country_code')!='US': continue
        if co['linkedin_url'].lower().rstrip('/') in ex_li or nd(co['domain']) in ex_d: continue
        if any(k in co['name'].lower() for k in dnc): continue
        if c.startswith('E') and not OK_IND.match(co['industry'] or ''): continue
        cand.setdefault(co['linkedin_url'].lower().rstrip('/'),{'co':co,'codes':set()})['codes'].add(c)
print('candidates',len(cand),collections.Counter(c for v in cand.values() for c in v['codes']))
def call(body):
    for i in range(5):
        try:
            rq=urllib.request.Request('https://api.blitz-api.ai/v2/jobs/company',json.dumps(body).encode(),{'x-api-key':K,'content-type':'application/json','User-Agent':'curl/8.5.0'})
            return json.load(urllib.request.urlopen(rq,timeout=60))
        except Exception as e: time.sleep(2+i*2)
    return {'error':1}
def jobs(u):
    out=[];cur=None
    for p in range(6):
        r=call({'company_linkedin_url':u,'job':{'date_posted':{'last_days':90}},'max_results':50,'cursor':cur})
        if 'error' in r: return None
        out+=r.get('results',[]);cur=r.get('cursor')
        if not cur: break
    return out
items=list(cand.items())
with cf.ThreadPoolExecutor(14) as ex: res=list(ex.map(lambda kv:jobs(kv[1]['co']['linkedin_url']),items))
raw=open('expand_jobs_raw.jsonl','w')
rows=[]
for (k,v),js in zip(items,res):
    raw.write(json.dumps({'linkedin_url':v['co']['linkedin_url'],'jobs':js})+'\n')
    if js is None: continue
    co=v['co'];h={}
    for c in v['codes']:
        m={j['url']:(j['title'],j['date_posted'][:10]) for j in js if re.search(RX[c],j['title'] or '',re.I)}
        if len(m)>=MINJ.get(c,1): h[c]=m
    if not h: continue
    codes=[c for c in PTS if c in h];score=sum(PTS[c] for c in codes)
    notes=[]
    for c in codes:
        it=sorted(h[c].items(),key=lambda i:i[1][1],reverse=True)
        notes.append(f"[{c}] {len(it)} role(s) in last 90 days, latest {it[0][1][1]}: "+'; '.join(f"{t} ({dt})" for u,(t,dt) in it[:3])+f". Example: {it[0][0]}")
    hq=co['hq'] or {}
    ind=co['industry'] or '-'
    seg='bank' if ind=='Banking' else 'fintech/payments' if ind in('Financial Services','Payments') else ind
    rows.append({'company_name':co['name'],'domain':nd(co['domain']) or '-','website':co['website'] or '-','linkedin_url':co['linkedin_url'],'segment':seg,'employees':co['employees_on_linkedin'] or '-','revenue_range':'-','state':hq.get('state') or '-','city':hq.get('city') or '-','tier':'A' if score>=35 else 'B' if score>=20 else 'C','score':score,'has_signal':'yes','signals_triggers':' + '.join(NAME[c] for c in codes),'signal_codes':','.join(codes),'pilot_tag':'-','notes':' || '.join(notes)})
rows.sort(key=lambda r:(-r['score'],-(r['employees'] if isinstance(r['employees'],int) else 0)))
dd='/home/user/Clients/clients/teleion/sourcing/all-icps-job-signals-expansion'
os.makedirs(dd,exist_ok=True)
f=dd+'/2026-10-12-companies.csv'
assert not os.path.exists(f)
w=csv.DictWriter(open(f,'w',newline=''),fieldnames=list(rows[0].keys()),quoting=csv.QUOTE_ALL);w.writeheader();w.writerows(rows)
print(len(rows),collections.Counter(r['tier'] for r in rows),collections.Counter(r['signal_codes'] for r in rows).most_common(12))
print(collections.Counter(c for r in rows for c in r['signal_codes'].split(',')))
print(collections.Counter(r['segment'] for r in rows).most_common(12))
