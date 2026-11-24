"""Merge Indeed (Apify valig) jobs with the Blitz/LinkedIn 60-day pull and size C7.

Inputs (scratchpad gw/):
  rows.json         Blitz companies (tam-by-jobs) with job counts, from classify.py
  jobs_60d.jsonl    Blitz LinkedIn jobs, last 60 days
  indeed/bucket_*.csv  Indeed jobs exported from GTM table 1c (IN only)
Outputs:
  indeed_jobs_clean.csv, companies_merged.json, summary printed
"""
import csv, glob, json, os, re, sys, time, datetime, collections, urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location('cl', os.path.join(os.path.dirname(__file__), 'classify.py'))
src = open(spec.origin).read().split('jobs=collections.defaultdict')[0]  # only defs (bucket, HOURLY, hourly)
ns = {}; exec(src, ns)
bucket, hourly = ns['bucket'], ns['hourly']

TODAY = datetime.date(2026, 11, 17)
WINDOW = 60
TOWNS = {'south bend','mishawaka','elkhart','goshen','nappanee','middlebury','bristol','wakarusa','millersburg',
         'dunlap','granger','osceola','new carlisle','north liberty','walkerton','lakeville','notre dame'}
KEY = os.environ['BLITZ_API_KEY']
CACHE = 'blitz_cache.json'
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def post(path, body):
    k = path + json.dumps(body, sort_keys=True)
    if k in cache: return cache[k]
    for i in range(4):
        try:
            r = urllib.request.Request('https://api.blitz-api.ai' + path, data=json.dumps(body).encode(),
                                       headers={'x-api-key': KEY, 'content-type': 'application/json'})
            d = json.load(urllib.request.urlopen(r, timeout=60)); break
        except urllib.error.HTTPError as e:
            d = {'_error': e.code}
            if e.code in (400, 404, 422): break
            time.sleep(2 * (i + 1))
        except Exception:
            d = {'_error': 'net'}; time.sleep(2 * (i + 1))
    cache[k] = d; return d

def norm_name(s):
    s = (s or '').lower()
    s = re.sub(r'&', ' and ', s)
    s = re.sub(r'\b(inc|llc|l\.l\.c|corp|corporation|co|company|ltd|the|group|holdings|usa|us|of america)\b\.?', ' ', s)
    return re.sub(r'[^a-z0-9]+', '', s)

def norm_dom(u):
    u = (u or '').lower().strip()
    u = re.sub(r'^https?://', '', u); u = re.sub(r'^www\.', '', u)
    return u.split('/')[0].split('?')[0]

def li(u):
    u = (u or '').lower().split('?')[0].rstrip('/')
    return re.sub(r'^https?://(www\.)?', 'https://www.', u)

# ---- Indeed jobs ----
ind = {}
for f in sorted(glob.glob('indeed/2026-*.csv')):
    for r in csv.DictReader(open(f, newline='')):
        k = r.get('Job key')
        if not k or k in ind: continue
        town = (r.get('City') or '').strip().lower()
        if (r.get('State') or '') != 'IN' or town not in TOWNS: continue
        r['Posted'] = (r.get('Published') or '')[:10]; r['Town'] = (r.get('City') or '') + ', IN'
        ind[k] = r
print('indeed unique IN-town jobs:', len(ind))
def age(r):
    try: return (TODAY - datetime.date.fromisoformat(r['Posted'][:10])).days
    except Exception: return 9999
ind60 = {k: r for k, r in ind.items() if age(r) <= WINDOW}
print('indeed jobs posted in last %d days:' % WINDOW, len(ind60))

# ---- Blitz companies ----
B = json.load(open('rows.json'))
by_li = {li(r['company_linkedin_url']): r for r in B}
by_dom = {norm_dom(r['domain']): r for r in B if r['domain'] not in ('-', '')}
by_name = {norm_name(r['company_name']): r for r in B}

# ---- group Indeed jobs by employer ----
emp = collections.defaultdict(list)
for k, r in ind60.items():
    emp[(r.get('Employer') or '').strip()].append(r)
emp.pop('', None)
print('indeed employers (60d):', len(emp))

def resolve(name, jobs):
    site = next((j.get('Employer website') for j in jobs if j.get('Employer website')), '')
    d = norm_dom(site)
    if d and d in by_dom: return by_dom[d]['company_linkedin_url'], 'domain'
    n = norm_name(name)
    if n and n in by_name: return by_name[n]['company_linkedin_url'], 'name'
    if d:
        x = post('/v2/enrichment/domain-to-linkedin', {'domain': d})
        if x.get('found') and x.get('company_linkedin_url'): return x['company_linkedin_url'], 'blitz_domain'
    return None, 'unresolved'

names = list(emp)
with ThreadPoolExecutor(10) as ex:
    res = dict(zip(names, ex.map(lambda n: resolve(n, emp[n]), names)))

# enrich resolved LinkedIn URLs not already in Blitz rows
need = sorted({li(u) for u, how in res.values() if u and li(u) not in by_li})
def enrich(u):
    x = post('/v2/enrichment/company', {'company_linkedin_url': u})
    return u, (x.get('company') or {})
with ThreadPoolExecutor(10) as ex:
    extra = dict(ex.map(enrich, need))
json.dump(cache, open(CACHE, 'w'))
print('blitz enrich calls for new companies:', len(need))

# ---- merged company table ----
blitz_jobs = collections.defaultdict(list)
for l in open('jobs_60d.jsonl'):
    j = json.loads(l)
    if j.get('company_linkedin_url'): blitz_jobs[li(j['company_linkedin_url'])].append(j)

C = {}
def get(u, name):
    key = li(u) if u else 'name:' + norm_name(name)
    if key not in C:
        base = by_li.get(key) if u else None
        co = extra.get(key, {}) if u else {}
        C[key] = dict(company_linkedin_url=u or '-', company_name=(base or {}).get('company_name') or co.get('name') or name,
                      domain=(base or {}).get('domain') or co.get('domain') or '-',
                      industry=(base or {}).get('industry') or co.get('industry') or '-',
                      size=(base or {}).get('size') or co.get('size') or '-',
                      hq_state=(base or {}).get('hq_state') or ((co.get('hq') or {}).get('state')) or '-',
                      li_jobs=set(), indeed_jobs=set(), titles=collections.Counter(), hourly_keys=set(), towns=set(),
                      indeed_size='-', resolved_by='-')
    return C[key]
for u, js in blitz_jobs.items():
    c = get(u, js[0]['company_name'])
    for j in js:
        c['li_jobs'].add(j['url']); c['titles'][j['title']] += 1; c['towns'].add(j['_query_city'])
        if hourly(j['title']): c['hourly_keys'].add('li:' + j['url'])
    c['resolved_by'] = 'blitz'
for name, js in emp.items():
    u, how = res[name]
    c = get(u, name)
    if c['resolved_by'] == '-': c['resolved_by'] = how
    for j in js:
        c['indeed_jobs'].add(j['Job key']); c['titles'][j['Job title']] += 1
        c['towns'].add(j['Town'].rsplit(',', 1)[0].strip())
        if hourly(j['Job title']): c['hourly_keys'].add('in:' + j['Job key'])
        if j.get('Employer size'): c['indeed_size'] = j['Employer size']

ICP = {'manufacturing', 'warehousing_logistics', 'retail', 'hospitality_fb_events'}
SMALL_INDEED = {'1 to 10', 'Less than 10', ''}
out = []
for k, c in C.items():
    b = bucket(c['industry'] if c['industry'] != '-' else '', c['company_name'] or '')
    if c['industry'] == '-' : b = 'unknown_industry'
    n_jobs = len(c['li_jobs']) + len(c['indeed_jobs'])   # may double count a role posted on both boards
    titles_distinct = len(c['titles'])
    small = c['size'] in ('1-10',) or (c['size'] == '-' and c['indeed_size'] in ('1 to 10',))
    out.append(dict(company_name=c['company_name'], company_linkedin_url=c['company_linkedin_url'], domain=c['domain'],
                    industry=c['industry'], icp_bucket=b, size=c['size'], indeed_size=c['indeed_size'], hq_state=c['hq_state'],
                    linkedin_jobs_60d=len(c['li_jobs']), indeed_jobs_60d=len(c['indeed_jobs']),
                    distinct_titles_60d=titles_distinct, hourly_postings_60d=len(c['hourly_keys']),
                    hourly_distinct_titles=len({t for t in c['titles'] if hourly(t)}),
                    towns=';'.join(sorted(c['towns'])), source=('both' if c['li_jobs'] and c['indeed_jobs'] else 'linkedin' if c['li_jobs'] else 'indeed'),
                    resolved_by=c['resolved_by'], small=small,
                    sample_titles=' | '.join(t for t, _ in c['titles'].most_common(5))))
json.dump(out, open('companies_merged.json', 'w'))

def fit(r): return r['icp_bucket'] in ICP and not r['small'] and (r['size'] != '-' or r['indeed_size'] not in ('-', ''))
f = [r for r in out if fit(r)]
print('\nall hiring companies (merged):', len(out), dict(collections.Counter(r['source'] for r in out)))
print('ICP-fit:', len(f))
for lab, key, k in [('2+ distinct titles (any)', 'distinct_titles_60d', 2), ('2+ distinct hourly titles', 'hourly_distinct_titles', 2),
                    ('3+ distinct hourly titles', 'hourly_distinct_titles', 3), ('5+ distinct hourly titles', 'hourly_distinct_titles', 5)]:
    s = [r for r in f if r[key] >= k]
    print(f'{lab:28s}', len(s), dict(collections.Counter(r['icp_bucket'] for r in s)), dict(collections.Counter(r['source'] for r in s)))
u = [r for r in out if r['icp_bucket'] == 'unknown_industry' and r['hourly_distinct_titles'] >= 2]
print('unknown industry with 2+ hourly titles (needs review):', len(u))
