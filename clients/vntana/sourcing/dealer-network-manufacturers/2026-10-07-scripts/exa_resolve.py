import json,re,glob,collections,concurrent.futures as cf,os,time,urllib.request
KEY=os.environ['BLITZ_API_KEY']
def dom(u):
    u=re.sub(r'^https?://','',(u or '').lower()).split('/')[0].split(':')[0]; return re.sub(r'^www\.','',u)
def root(d):
    p=d.split('.'); 
    if len(p)>=3 and p[-2] in ('co','com','org','net','gov','ac') and len(p[-1])==2: return '.'.join(p[-3:])
    return '.'.join(p[-2:]) if len(p)>=2 else d
NOISE=re.compile(r'(linkedin|youtube|facebook|instagram|twitter|x\.com|wikipedia|medium\.com|reddit|pinterest|tiktok|amazon|ebay|alibaba|aliexpress|indiamart|thomasnet|globalspec|manta|yellowpages|zoominfo|dnb\.com|crunchbase|bloomberg|glassdoor|indeed|clutch|g2\.com|capterra|made-in-china|tradekey|europages|kompass|machinerytrader|tractorhouse|truckpaper|equipmentwatch|equipmentfacts|ritchiebros|ironplanet|govdeals|rbauction|alibaba|walmart|homedepot|lowes|northerntool|grainger|zoro|mcmaster|fastenal|motion\.com|applied\.com|tractorsupply|cabelas|rurallifestyle|craigslist|facebook|nada|rvtrader|truckandtrailer|commercialtrucktrader|cars\.com|autotrader|cargurus|carfax|edmunds|kbb|yelp|bbb\.org|mapquest|google|bing|apple\.com|microsoft)')
D=json.load(open('exa_disc.json'))
c=collections.Counter(); first={}
for q in D:
    for r in q['results']:
        d=root(dom(r['url']))
        if not d or NOISE.search(d): continue
        c[d]+=1; first.setdefault(d,r['title'])
known=set()
for f in glob.glob('blitz/*.jsonl'):
    for l in open(f):
        x=json.loads(l)
        if 'domain' in x and x['domain']: known.add(root(dom(x['domain'])))
        if 'website' in x and x.get('website'): known.add(root(dom(x['website'])))
for f in glob.glob('disco/*.jsonl'):
    for l in open(f):
        x=json.loads(l)
        if x.get('domain'): known.add(root(dom(x['domain'])))
print('exa domains',len(c),'already in blitz/disco pools',sum(1 for d in c if d in known))
new=[d for d in c if d not in known]
print('new to resolve',len(new))
def b(path,body):
    for a in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':KEY,'Content-Type':'application/json'}),timeout=60))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503): time.sleep(2**a); continue
            return {'found':False}
        except Exception: time.sleep(2**a)
    return {'found':False}
def job(d):
    r=b('/v2/enrichment/domain-to-linkedin',{'domain':d})
    if not r.get('found'): return d,None
    e=b('/v2/enrichment/company',{'company_linkedin_url':r['company_linkedin_url']})
    return d,{'li':r['company_linkedin_url'],'company':e.get('company')}
with cf.ThreadPoolExecutor(12) as ex: res=dict(ex.map(job,new))
json.dump({'counts':c,'titles':first,'resolved':res,'known_hits':[d for d in c if d in known]},open('exa_resolved.json','w'))
print('resolved',sum(1 for v in res.values() if v),'enriched',sum(1 for v in res.values() if v and v['company']))
