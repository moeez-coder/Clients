import csv,json,os,re,random,time,datetime,urllib.request,urllib.parse,concurrent.futures as cf,collections
BK=os.environ['BLITZ_API_KEY'];EK=os.environ['EXA_API_KEY']
L='/home/user/Clients/clients/teleion/sourcing/icp-decision-makers-by-persona/2026-10-12-leads.csv'
r=list(csv.DictReader(open(L)))
random.seed(7)
S=[]
for g in ['Compliance, Risk & Fraud','AI & Data Governance','Payments & Finance','Executive Sponsor']:
    rows=[x for x in r if x['persona_group']==g];random.shuffle(rows);seen=set();n=0
    for x in rows:
        if x['company_domain'] in seen: continue
        seen.add(x['company_domain']);S.append(x);n+=1
        if n==50: break
def post(url,body,hdr):
    for i in range(4):
        try:
            rq=urllib.request.Request(url,json.dumps(body).encode(),{**hdr,'content-type':'application/json','User-Agent':'curl/8.5.0'})
            return json.load(urllib.request.urlopen(rq,timeout=60))
        except Exception as e: time.sleep(2+2*i)
    return None
def blitz(path,body): return post('https://api.blitz-api.ai/v2/'+path,body,{'x-api-key':BK})
JR={
 'Compliance, Risk & Fraud':r"\b(bsa|aml|kyc|ofac|sanctions|financial crimes?|compliance|fraud|risk)\b",
 'AI & Data Governance':r"(model risk|\bai\b|artificial intelligence|machine learning|data governance|cyber|information security|security (analyst|engineer|architect|officer)|technology risk|it risk)",
 'Payments & Finance':r"(treasury|payments?|accounting|controller|reconciliation|financial reporting|finance operations|accounts payable)",
}
JR['Executive Sponsor']='|'.join(JR[k] for k in list(JR))
def exa(q):
    d=(datetime.date(2026,10,12)-datetime.timedelta(days=120)).isoformat()
    j=post('https://api.exa.ai/search',{'query':q,'numResults':6,'startPublishedDate':d,'type':'auto','contents':{'highlights':{'numSentences':2,'highlightsPerUrl':1}}},{'x-api-key':EK})
    return (j or {}).get('results',[])
KW={'M&A':r"(acqui|merger|merge[sd]?\b|definitive agreement|business combination|to combine)",
    'Regulatory':r"(consent order|enforcement action|cease and desist|formal agreement|civil money penalt|written agreement|BSA/AML|bank secrecy)",
    'AI':r"(artificial intelligence|\bAI\b|generative|agentic|machine learning)"}
QT={'M&A':'{n} announces acquisition OR merger','Regulatory':'{n} consent order OR enforcement action OR regulatory agreement','AI':'{n} launches AI OR artificial intelligence'}
def tok(n): 
    t=re.sub(r'[^a-z0-9 ]','',n.lower()); t=re.sub(r'\b(inc|corp|corporation|llc|co|company|bank|financial|group|holdings|the)\b','',t).split()
    return ' '.join(t[:2]) if t else n.lower()
def work(x):
    n=x['company_name'];d=x['company_domain'];out={'jobs':[],'news':[]}
    li=blitz('enrichment/domain-to-linkedin',{'domain':d})
    u=(li or {}).get('company_linkedin_url')
    if u:
        jobs=[];cur=None
        for p in range(4):
            j=blitz('jobs/company',{'company_linkedin_url':u,'job':{'date_posted':{'last_days':90}},'max_results':50,'cursor':cur})
            if not j: break
            jobs+=j.get('results',[]);cur=j.get('cursor')
            if not cur: break
        rx=re.compile(JR[x['persona_group']],re.I)
        seen={}
        for j in jobs:
            if rx.search(j['title'] or ''): seen[j['url']]=(j['title'],j['date_posted'][:10])
        out['jobs']=sorted(seen.items(),key=lambda i:i[1][1],reverse=True)
    key=tok(n)
    for st,q in QT.items():
        for res in exa(q.format(n=n)):
            blob=(res['title'] or '')+' '+' '.join(res.get('highlights') or [])
            if key not in blob.lower() and key.replace(' ','') not in res['url'].lower().replace('-',''): continue
            if not re.search(KW[st],blob,re.I): continue
            out['news'].append((st,res['title'],res['url'],(res.get('publishedDate') or '')[:10],(res.get('highlights') or [''])[0].strip().replace('\n',' ')[:220]))
    return out
with cf.ThreadPoolExecutor(10) as ex: R=list(ex.map(work,S))
json.dump([{'person':x,'res':o} for x,o in zip(S,R)],open('personalize_raw.json','w'))
print(len(S),sum(1 for o in R if o['jobs']),sum(1 for o in R if o['news']))
