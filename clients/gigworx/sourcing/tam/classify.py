import json, re, collections, csv, datetime
T=json.load(open('tam_60d.json'))
J=[json.loads(l) for l in open('jobs_60d.jsonl')]
TODAY=datetime.date(2026,11,17)
def bucket(ind, name):
    i=(ind or '')
    n=name.lower()
    if re.search(r'staffing|recruit|executive search|human resources services', i, re.I): return 'excl_staffing'
    if re.search(r'gurley|dealership|chevrolet|chevy|toyota|honda|hyundai|nissan|subaru|kia\b|buick|gmc|chrysler|jeep|dodge|ford\b|motors\b|auto mall|autoplex', n) and not re.search(r'forest river|thor|jayco|keystone|grand design', n): return 'excl_dealer'
    if i=='Retail Motor Vehicles' or i=='Wholesale Motor Vehicles and Parts': return 'excl_dealer'
    if 'Manufacturing' in i or i in ('Automotive','Food Production','Food and Beverages','Printing Services','Packaging and Containers','Building Materials','Shipbuilding','Plastics Manufacturing'): return 'manufacturing'
    if i.startswith('Wholesale') or i in ('Truck Transportation','Transportation; Logistics; Supply Chain and Storage','Freight and Package Transportation','Transportation/Trucking/Railroad','Rail Transportation','Warehousing and Storage'): return 'warehousing_logistics'
    if i.startswith('Retail') or i=='Food and Beverage Retail': return 'retail'
    if i in ('Hospitality','Restaurants','Food and Beverage Services','Events Services','Entertainment Providers','Facilities Services','Hotels and Motels','Spectator Sports','Recreational Facilities','Caterers'): return 'hospitality_fb_events'
    if i in ('Construction','Specialty Trade Contractors','Civil Engineering','Building Construction','Residential Building Construction','Nonresidential Building Construction'): return 'construction_held'
    return 'out_of_icp'
HOURLY=re.compile(r'\b(production|assembl\w*|warehouse|labor\w*|labour\w*|material handler|forklift|machine operator|operator|picker|packer|packag\w*|fabricat\w*|welder|welding|line worker|manufacturing (associate|technician|worker)|shipping|receiving|loader|unloader|sanitation|stocker|order selector|team member|associate|crew|cashier|cook|dishwasher|prep|server|bartender|host(ess)?|housekeep\w*|room attendant|janitor\w*|custodian|cleaner|cleaning|banquet|barista|busser|food service|merchandis\w*|sales associate|store associate|stock|freight|dock|inventory|sorter|handler|helper|trainee|general labor|painter|sander|upholster\w*|carpenter|installer|driver helper|delivery|porter|attendant|dietary|line lead|lead hand|valet|event staff|setup|caregiver|guest service\w*|froster|shift lead\w*|parts puller|mold shop|final finish|(1st|2nd|3rd|first|second|third|night) shift|key holder|sales help|seamstress|shipper|kitchen team|team|part[- ]time|pt\b|dishroom|line cook|baker|bakery|deli|meat cutter|clerk|parts pro|salesperson|machinist|cnc|set-?up|press|router|laminat\w*|finisher|trim|wire harness|maintenance (tech\w*|mechanic)|mechanic|technician)\b', re.I)
NOT_HOURLY=re.compile(r'\b(manager|director|supervisor|engineer|nurse|rn\b|lpn|physician|pharmacist|therapist|analyst|accountant|account executive|sales representative|recruiter|vp|vice president|president|controller|cdl|truck driver|class a|attorney|teacher|professor|specialist|coordinator|engineer\w*|sales manager|store manager|restaurant manager|general manager|assistant manager|scientist|developer|architect|consultant|planner|buyer|estimator|technologist|clinician|counselor|officer|executive)\b', re.I)
def hourly(t): return bool(HOURLY.search(t)) and not NOT_HOURLY.search(t)
jobs=collections.defaultdict(list)
for j in J:
    k=j.get('company_linkedin_url')
    if k: jobs[k].append(j)
rows=[]
for k,e in T.items():
    co=e['company']; js={j['url']:j for j in jobs.get(k,[])}.values()
    js=list(js)
    hr=[j for j in js if hourly(j['title'])]
    d30=[j for j in js if (TODAY-datetime.date.fromisoformat(j['date_posted'][:10])).days<=30]
    hq=co.get('hq') or {}
    b=bucket(co.get('industry'), co.get('name',''))
    size=co.get('size') or '-'
    titles=collections.Counter(j['title'] for j in js)
    rows.append(dict(company_linkedin_url=k, company_name=co.get('name'), domain=co.get('domain') or '-', industry=co.get('industry') or '-',
        icp_bucket=b, size=size, hq_city=hq.get('city') or '-', hq_state=hq.get('state') or '-',
        jobs_60d=len(js), distinct_titles_60d=len(titles), jobs_30d=len(d30), hourly_jobs_60d=len(hr),
        hourly_distinct_titles_60d=len(set(j['title'] for j in hr)),
        cities=';'.join(sorted(set(j['_query_city'] for j in js))),
        sample_titles=' | '.join(t for t,_ in titles.most_common(5)),
        latest_job_url=max(js,key=lambda j:j['date_posted'])['url'] if js else '-'))
json.dump(rows,open('rows.json','w'))
ICP={'manufacturing','warehousing_logistics','retail','hospitality_fb_events'}
SMALL={'1-10','-',None,''}
def fit(r): return r['icp_bucket'] in ICP and r['size'] not in SMALL
print('all companies',len(rows))
print('by bucket', collections.Counter(r['icp_bucket'] for r in rows))
f=[r for r in rows if fit(r)]
print('ICP fit (4 verticals, 11+ emp):',len(f))
for lab,key,k in [('2+ any jobs','jobs_60d',2),('3+ any','jobs_60d',3),('2+ hourly','hourly_jobs_60d',2),('3+ hourly','hourly_jobs_60d',3),('5+ hourly','hourly_jobs_60d',5),('2+ distinct hourly titles','hourly_distinct_titles_60d',2),('2+ any in 30d','jobs_30d',2)]:
    sub=[r for r in f if r[key]>=k]
    print(f'{lab:28s}', len(sub), dict(collections.Counter(r['icp_bucket'] for r in sub)))
print('construction held, 2+ hourly:', sum(1 for r in rows if r['icp_bucket']=='construction_held' and r['size'] not in SMALL and r['hourly_jobs_60d']>=2))
print('1-10/unknown size in ICP verticals w/ 2+ jobs:', sum(1 for r in rows if r['icp_bucket'] in ICP and r['size'] in SMALL and r['jobs_60d']>=2))
