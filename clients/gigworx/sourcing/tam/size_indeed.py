"""C7 sizing from Indeed only (live postings), last N days. Blitz is NOT used for jobs.

Inputs:  indeed_deep/*.csv  (GTM table b38a1682..., memo23 deep search, employer posts only, has Indeed industry)
         indeed/*.csv       (GTM table 70ebdabf..., valig split runs, no industry)
         tam_60d.json / tam_180d.json  (Blitz firmographics only: industry label fallback by company name)
Output:  indeed_jobs_<N>d.csv, indeed_companies_<N>d.json, printed summary
"""
import csv, glob, json, re, sys, datetime, collections, os
DAYS = int(sys.argv[1]) if len(sys.argv) > 1 else 180
TODAY = datetime.date(2026, 11, 17)
TOWNS = {'south bend','mishawaka','elkhart','goshen','nappanee','middlebury','bristol','wakarusa','millersburg','dunlap',
         'granger','osceola','new carlisle','north liberty','walkerton','lakeville','notre dame'}
ns = {}; exec(open('classify.py').read().split('jobs=collections.defaultdict')[0], ns)
hourly, blitz_bucket = ns['hourly'], ns['bucket']

def norm_name(s):
    s = (s or '').lower().replace('&', ' and ')
    s = re.sub(r'\b(inc|llc|corp|corporation|co|company|ltd|the|group|holdings|usa|us|of america|incorporated)\b\.?', ' ', s)
    s = re.sub(r'\s+-\s+.*$', '', s)          # "Pet Supplies Plus - Goshen, IN" -> brand
    return re.sub(r'[^a-z0-9]+', '', s)
def norm_dom(u):
    u = re.sub(r'^https?://', '', (u or '').lower().strip()); u = re.sub(r'^www\.', '', u)
    return u.split('/')[0].split('?')[0]

jobs = {}
for f in sorted(glob.glob('indeed_deep/*.csv')) + sorted(glob.glob('indeed/2026-*.csv')):
    src = 'deep' if 'indeed_deep' in f else 'fast'
    for r in csv.DictReader(open(f, newline='')):
        k = r.get('Job key')
        if not k: continue
        if (r.get('State') or '') != 'IN' or (r.get('City') or '').strip().lower() not in TOWNS: continue
        try: d = datetime.date.fromisoformat((r.get('Published') or '')[:10])
        except ValueError: continue
        if (TODAY - d).days > DAYS: continue
        prev = jobs.get(k)
        if prev and prev['_src'] == 'deep': continue      # deep rows carry industry; keep them
        r['_src'] = src; r['_date'] = d; jobs[k] = r
print(f'Indeed jobs: IN, 17 towns, last {DAYS} days, unique job keys: {len(jobs)}  by source:',
      dict(collections.Counter(r['_src'] for r in jobs.values())))

# group into employers: by website domain when present, else by normalised name
groups = {}; alias = {}
for r in jobs.values():
    name = (r.get('Employer') or '').strip()
    if not name: continue
    d = norm_dom(r.get('Employer website')); n = norm_name(name)
    key = alias.get(('d', d)) if d else None
    key = key or alias.get(('n', n)) or (('d', d) if d else ('n', n))
    alias[('n', n)] = key
    if d: alias[('d', d)] = key
    g = groups.setdefault(key, dict(names=collections.Counter(), industry=collections.Counter(), size=collections.Counter(),
                                     site='', titles=collections.Counter(), hourly=set(), towns=set(), keys=set(), latest=None))
    g['names'][name] += 1
    if r.get('Industry'): g['industry'][r['Industry']] += 1
    if r.get('Employer size'): g['size'][r['Employer size']] += 1
    if d: g['site'] = d
    t = (r.get('Job title') or '').strip()
    g['titles'][t] += 1; g['keys'].add(r['Job key']); g['towns'].add(r['City'])
    if hourly(t): g['hourly'].add(t.lower())
    g['latest'] = max(g['latest'] or r['_date'], r['_date'])

# Indeed industry -> ICP bucket
def indeed_bucket(ind, name):
    i = (ind or '').lower(); n = (name or '').lower()
    if re.search(r'staffing|recruit|hr consulting|employment', i + ' ' + n): return 'excl_staffing'
    if re.search(r'vehicle dealer|car dealer|automotive dealer', i): return 'excl_dealer'
    if not i: return None
    if 'construction' in i: return 'construction_held'
    if 'manufactur' in i or re.search(r'food production|printing', i): return 'manufacturing'
    if re.search(r'retail|stores|grocery|convenience|gas station|department|merchandise', i): return 'retail'
    if re.search(r'wholesale|logistic|shipping|trucking|freight|warehous|distribution|transportation', i): return 'warehousing_logistics'
    if re.search(r'restaurant|food service|hotel|hospitality|catering|event|casino|gambling|recreation|amusement|entertainment|cleaning|janitorial|facilities|lodging|travel', i): return 'hospitality_fb_events'
    return 'out_of_icp'

# Blitz firmographics: industry label fallback by company name only (no job data)
bl = {}
for fn in ('tam_180d.json', 'tam_60d.json'):
    if os.path.exists(fn):
        for v in json.load(open(fn)).values():
            co = v['company']; bl.setdefault(norm_name(co.get('name')), co)

import urllib.request, time
KEY=os.environ['BLITZ_API_KEY']; CF='blitz_cache.json'; cache=json.load(open(CF)) if os.path.exists(CF) else {}
def bpost(path, body):
    k=path+json.dumps(body,sort_keys=True)
    if k in cache: return cache[k]
    try:
        r=urllib.request.Request('https://api.blitz-api.ai'+path,data=json.dumps(body).encode(),headers={'x-api-key':KEY,'content-type':'application/json'})
        d=json.load(urllib.request.urlopen(r,timeout=60))
    except Exception as e: d={'_error':str(e)[:80]}
    cache[k]=d; return d
def dom2li(d):
    x=bpost('/v2/enrichment/domain-to-linkedin',{'domain':d}); return x.get('company_linkedin_url') if x.get('found') else None
def enrich(u): return bpost('/v2/enrichment/company',{'company_linkedin_url':u}).get('company') or {}
SMALL_IND = {'1 to 10', 'Less than 10'}
SMALL_BL = {'1-10'}
ICP = {'manufacturing', 'warehousing_logistics', 'retail', 'hospitality_fb_events'}
out = []
for key, g in groups.items():
    name = g['names'].most_common(1)[0][0]
    ind = g['industry'].most_common(1)[0][0] if g['industry'] else ''
    b = indeed_bucket(ind, name); ind_src = 'indeed' if ind else '-'
    co = bl.get(norm_name(name))
    if b is None and co:
        b = blitz_bucket(co.get('industry') or '', name); ind = co.get('industry') or ''; ind_src = 'blitz_firmographic'
    if b is None and g['site'] and len(g['titles']) >= 2:
        li_ = dom2li(g['site'])
        if li_:
            c2 = enrich(li_)
            if c2.get('industry'):
                co = c2; b = blitz_bucket(c2['industry'], name); ind = c2['industry']; ind_src = 'blitz_firmographic'
    if b is None: b = 'unknown_industry'
    size = g['size'].most_common(1)[0][0] if g['size'] else ((co or {}).get('size') or '-')
    small = size in SMALL_IND or size in SMALL_BL
    h = len(g['hourly']); a = len(g['titles'])
    out.append(dict(company_name=name, website=g['site'] or '-', industry=ind or '-', industry_source=ind_src, icp_bucket=b,
                    size=size, small=small, indeed_postings=len(g['keys']), distinct_roles=a, hourly_distinct_roles=h,
                    towns=';'.join(sorted(g['towns'])), latest_posted=str(g['latest']),
                    signal_tier=('A: 5+ hourly roles' if h >= 5 else 'B: 3-4 hourly roles' if h >= 3 else 'C: 2 hourly roles' if h == 2
                                 else 'D: 2+ roles, <2 hourly' if a >= 2 else 'E: 1 role'),
                    company_linkedin_url=(co or {}).get('linkedin_url') or '-',
                    sample_titles=' | '.join(t for t, _ in g['titles'].most_common(6))))
for r in out:
    r['icp_fit'] = 'yes' if (r['icp_bucket'] in ICP and not r['small']) else ('review' if r['icp_bucket'] == 'unknown_industry' and not r['small'] else 'no')
json.dump(out, open(f'indeed_companies_{DAYS}d.json', 'w')); json.dump(cache, open(CF,'w'))
with open(f'indeed_jobs_{DAYS}d.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['indeed_job_key', 'indeed_url', 'date_posted', 'title', 'employer', 'city', 'state', 'job_type', 'employer_size', 'industry', 'employer_website', 'scrape'])
    for r in sorted(jobs.values(), key=lambda r: r['_date'], reverse=True):
        w.writerow([r['Job key'], 'https://www.indeed.com/viewjob?jk=' + r['Job key'], r['_date'], r.get('Job title') or '-', r.get('Employer') or '-',
                    r['City'], 'IN', r.get('Job type') or '-', r.get('Employer size') or '-', r.get('Industry') or '-', r.get('Employer website') or '-', r['_src']])

print('employers:', len(out), ' buckets:', dict(collections.Counter(r['icp_bucket'] for r in out)))
for lab, key, k in [('2+ roles (any)', 'distinct_roles', 2), ('2+ hourly roles', 'hourly_distinct_roles', 2),
                    ('3+ hourly roles', 'hourly_distinct_roles', 3), ('5+ hourly roles', 'hourly_distinct_roles', 5)]:
    y = [r for r in out if r['icp_fit'] == 'yes' and r[key] >= k]; rv = [r for r in out if r['icp_fit'] == 'review' and r[key] >= k]
    print(f'{lab:18s} fit {len(y):4d}  review {len(rv):3d}  ', dict(collections.Counter(r['icp_bucket'] for r in y)))
