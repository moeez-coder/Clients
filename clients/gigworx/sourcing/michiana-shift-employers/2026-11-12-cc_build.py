"""Claude Code list build for GigWorx C1-C6 (2026-11-12).
Input: ccb/cands.json (Blitz company universe + hiring-signal companies) and ccb/out*.csv (subagent segment labels).
Steps: assign segment -> Blitz /v2/jobs/company signal -> Blitz waterfall people (Michiana cities) -> Blitz email -> copy.
Output: ccb/leads_all.json, ccb/companies_all.json, ccb/stats.json
"""
import json, os, csv, glob, re, subprocess, time, datetime, concurrent.futures as cf

D = os.path.dirname(os.path.abspath(__file__))
K = os.environ['BLITZ_API_KEY']
CITIES = ["South Bend", "Mishawaka", "Granger", "Elkhart", "Goshen", "Nappanee", "Middlebury", "Bristol", "Osceola", "Wakarusa"]
TODAY = datetime.date(2026, 11, 12)
calls = {'jobs': 0, 'waterfall': 0, 'email': 0}

_CACHE_F = os.path.join(D, 'api_cache.json')
_CACHE = json.load(open(_CACHE_F)) if os.path.exists(_CACHE_F) else {}
def post(path, body):
    key = path + json.dumps(body, sort_keys=True)
    if key in _CACHE: return _CACHE[key]
    r = _post(path, body)
    if r: _CACHE[key] = r
    return r
def _post(path, body):
    for _ in range(3):
        r = subprocess.run(['curl', '-sS', '--max-time', '60', 'https://api.blitz-api.ai' + path, '-H', 'x-api-key: ' + K,
                            '-H', 'Content-Type: application/json', '-d', json.dumps(body)], capture_output=True, text=True).stdout
        try:
            return json.loads(r)
        except Exception:
            time.sleep(2)
    return {}

# ---- 1. segment labels (validated by name against the input) ----
C = {c['_n']: c for c in json.load(open(f'{D}/cands.json'))}
label, reason, bad = {}, {}, 0
for f in sorted(glob.glob(f'{D}/out*.csv')):
    for row in csv.DictReader(open(f)):
        try:
            n = int(row['n'])
        except Exception:
            bad += 1; continue
        c = C.get(n)
        if not c or (row['name'] or '').strip().lower()[:12] != (c.get('name') or '').strip().lower()[:12]:
            bad += 1; continue
        label[n] = row['label'].strip().upper(); reason[n] = row.get('reason', '')
SMALL = {'1-10', '11-50'}
def size_small(c): return (c.get('size') or '') in SMALL

# ---- 2. assignment ----
need_jobs, plan = set(), {}
for n, lab in label.items():
    c = C[n]
    if lab == 'NO' or not c.get('linkedin_url'):
        continue
    small = size_small(c)
    p = []
    if lab == 'RV':
        p.append('C3')
    elif lab in ('MFG', 'WH', 'FB', 'RETAIL_BIG', 'RETAIL_SMALL') and small:
        p.append('C5')
    elif lab == 'MFG':
        p.append('C1')
    elif lab in ('WH', 'FB', 'RETAIL_BIG'):
        p.append('C2')
    elif lab == 'HOSP':
        p.append('C6')
    if not small and lab in ('RV', 'MFG', 'WH', 'FB', 'RETAIL_BIG', 'HOSP'):
        p.append('C4')
    if p:
        plan[n] = p
        if any(x in ('C1', 'C2', 'C3', 'C4', 'C6') for x in p):
            need_jobs.add(n)

# ---- 3. hiring signal (Blitz jobs at the company, last 60 days) ----
HOURLY = ["assembler", "assembly", "production", "laborer", "welder", "fabricator", "material handler", "forklift", "machine operator",
          "warehouse", "picker", "packer", "shipping", "loader", "order selector", "stocker", "painter", "cabinet", "upholstery", "sanitation",
          "housekeeping", "housekeeper", "banquet", "server", "dishwasher", "prep cook", "line cook", "cook", "event staff", "setup", "cashier",
          "seasonal", "temporary", "associate"]
EXCL = re.compile(r'manager|director|engineer|supervisor|analyst|sales|account|specialist|coordinator|nurse|driver cdl|cdl', re.I)
HOSP_RE = re.compile(r'housekeep|banquet|server|dishwash|prep cook|line cook|\bcook\b|event|setup|bartend|host', re.I)
SEAS_RE = re.compile(r'seasonal|temporary|\btemp\b|peak|holiday', re.I)

def jobs_for(n):
    c = C[n]
    d = post('/v2/jobs/company', {'company_linkedin_url': c['linkedin_url'],
                                  'job': {'title': {'include': HOURLY}, 'date_posted': {'last_days': 60},
                                          'location': {'city': {'include': CITIES + ['Bremen', 'Millersburg', 'Lakeville', 'New Carlisle', 'Walkerton', 'Edwardsburg']}, 'country_code': {'include': ['US']}}}, 'max_results': 25})
    out = []
    for j in d.get('results', []):
        t = j.get('title') or ''
        if EXCL.search(t):
            continue
        loc = json.dumps(j.get('location') or j.get('job_location') or '').lower()
        if not any(x.lower() in loc for x in CITIES + ['indiana', ', in']):
            continue
        dt = j.get('date_posted') or j.get('posted_at') or j.get('created_at') or ''
        city = None
        L = j.get('location') or {}
        if isinstance(L, dict):
            city = L.get('city')
        out.append({'title': t, 'date': str(dt)[:10], 'city': city, 'url': j.get('url') or j.get('job_url')})
    return n, out

JOBS = {}
with cf.ThreadPoolExecutor(5) as ex:
    for n, js in ex.map(jobs_for, sorted(need_jobs)):
        JOBS[n] = js
calls['jobs'] = len(need_jobs)

def sig(n):
    js = JOBS.get(n, [])
    s = {'open': len(js), 'aged30': 0, 'seasonal': [j for j in js if SEAS_RE.search(j['title'])], 'hosp': [j for j in js if HOSP_RE.search(j['title'])]}
    oldest = None
    for j in js:
        try:
            d = datetime.date.fromisoformat(j['date'])
            if (TODAY - d).days >= 30:
                s['aged30'] += 1
            if not oldest or d < datetime.date.fromisoformat(oldest['date']):
                oldest = j
        except Exception:
            pass
    s['oldest'] = oldest or (js[0] if js else None)
    return s

# ---- 4. which campaigns pass their signal gate ----
assign = {}
for n, p in plan.items():
    s = sig(n); keep = []
    for camp in p:
        if camp == 'C1' and s['open'] >= 3: keep.append(camp)      # doc: 3+ open, 1 aged/reposted (aged check recorded, see below)
        elif camp == 'C2' and (s['seasonal'] or s['open'] >= 5): keep.append(camp)
        elif camp == 'C4' and s['open'] >= 5: keep.append(camp)
        elif camp == 'C6' and s['hosp']: keep.append(camp)
        elif camp in ('C3', 'C5'): keep.append(camp)
    if keep:
        assign[n] = keep

# ---- 5. people (Waterfall, Michiana cities) ----
TIERS = {
    'C1': [['Plant Manager', 'Production Manager', 'Operations Manager'], ['Production Supervisor', 'General Manager', 'Director of Operations']],
    'C2': [['Warehouse Manager', 'Distribution Center Manager', 'Distribution Manager'], ['Operations Manager', 'General Manager', 'Store Manager', 'Logistics Manager']],
    'C3': [['Plant Manager', 'Production Manager', 'General Manager'], ['Production Supervisor', 'Operations Manager', 'Director of Operations', 'VP Operations'], ['[Owner]', '[President]', 'CEO']],
    'C4': [['HR Manager', 'Human Resources Manager', 'HR Business Partner', 'Human Resources Business Partner'], ['HR Director', 'Human Resources Director', 'HR Generalist']],
    'C5': [['[Owner]', '[President]', 'CEO', 'Founder'], ['General Manager']],
    'C6': [['General Manager', 'Housekeeping Manager', 'Executive Housekeeper', 'Food and Beverage', 'Kitchen Manager'], ['Banquet Manager', 'Event Manager', 'Catering Manager', 'Operations Manager', '[Owner]']],
}
EXT = ['assistant', 'intern', 'sales', 'account', 'marketing', 'recruiter', 'finance', 'it ']
def nppl(camp, c):
    if camp == 'C5': return 1
    if camp == 'C4': return 2
    return 1 if size_small(c) else 3

def ppl_for(job):
    n, camp = job; c = C[n]
    casc = [{'include_title': t, 'exclude_title': EXT if camp != 'C4' else ['assistant', 'intern', 'recruiter'],
             'location': {'city': {'include': CITIES}, 'country_code': ['US']}} for t in TIERS[camp]]
    if camp == 'C3' and not size_small(c) and (c.get('size') not in ('51-200',)):
        casc = casc[:2]  # owner/president only at suppliers under ~200
    d = post('/v2/search/waterfall-icp-keyword', {'company_linkedin_url': c['linkedin_url'], 'cascade': casc, 'max_results': nppl(camp, c)})
    return n, camp, d.get('results', [])

jobs_list = [(n, camp) for n, cs in assign.items() for camp in cs]
PEOPLE = []
with cf.ThreadPoolExecutor(5) as ex:
    for n, camp, rs in ex.map(ppl_for, jobs_list):
        for r in rs:
            p = r.get('person', r)
            exp = (p.get('experiences') or [{}])
            loc = p.get('location') if isinstance(p.get('location'), dict) else {}
            PEOPLE.append({'n': n, 'campaign': camp, 'linkedin_url': (p.get('linkedin_url') or '').rstrip('/'),
                           'first_name': p.get('first_name'), 'last_name': p.get('last_name'),
                           'job_title': exp[0].get('job_title') if exp and exp[0] else p.get('headline'),
                           'person_city': loc.get('city'), 'tier': r.get('icp')})
calls['waterfall'] = len(jobs_list)

# ---- 6. dedupe across campaigns (priority C4 > C3 > C6 > C1 > C2 > C5) ----
PRI = {'C4': 0, 'C3': 1, 'C6': 2, 'C1': 3, 'C2': 4, 'C5': 5}
PEOPLE.sort(key=lambda x: PRI[x['campaign']])
seen, uniq = set(), []
for p in PEOPLE:
    u = p['linkedin_url'].lower()
    if not u or u in seen: continue
    seen.add(u); uniq.append(p)

# ---- 7. email (Blitz), with company-domain match ----
def email_for(p):
    d = post('/v2/enrichment/email', {'person_linkedin_url': p['linkedin_url']})
    return p['linkedin_url'], d.get('email') if d.get('found', True) else None
EM = {}
with cf.ThreadPoolExecutor(5) as ex:
    for u, e in ex.map(email_for, uniq):
        EM[u] = e
calls['email'] = len(uniq)

# ---- 8. copy (approved doc, C1-C6) ----
def clean_co(s):
    return re.sub(r',?\s+(Inc\.?|LLC|L\.L\.C\.|Corp\.?|Corporation|Co\.?|Company|Incorporated|Ltd\.?)$', '', (s or '').strip(), flags=re.I).strip(' ,') or s
def fn(s):
    s = (s or '').strip()
    return s[:1].upper() + s[1:].lower() if (s.isupper() or s.islower()) else s
def clean_role(t):
    if not t: return t
    t = re.sub(r'^[^:]{0,40}:\s*', '', t)                      # 'Plant 163F (Elkhart, IN): '
    t = re.sub(r'\([^)]*\)', '', t)                            # parentheses
    t = re.split(r'\s+[-–|/]\s+|,', t)
    t = [x for x in t if not re.search(r'(?i)^(part[- ]time|full[- ]time|flexible|temporary|seasonal|\d+(st|nd|rd|th)\s*shift|.*shift$|\$|weekend|days|nights)', x.strip())] or t
    t = t[0]
    t = re.sub(r'(?i)\b(1st|2nd|3rd|first|second|third)\s+shift\b|\b\d+\b|\bI{1,3}\b', '', t)
    return re.sub(r'\s+', ' ', t).strip(' -–') or None
def month(d):
    try: return datetime.date.fromisoformat(d).strftime('%B')
    except Exception: return None

out = []
for p in uniq:
    c = C[p['n']]; s = sig(p['n']); camp = p['campaign']
    co = clean_co(c.get('name')); f = fn(p['first_name']); city = (s['oldest'] or {}).get('city') or (c.get('hq') or {}).get('city')
    role = clean_role((s['oldest'] or {}).get('title')); others = max(s['open'] - 1, 0)
    em = EM.get(p['linkedin_url']); dom = (c.get('domain') or '').lower().replace('www.', '')
    em_ok = bool(em and dom and dom.split('.')[0] in em.split('@')[-1].lower())
    if camp == 'C1':
        m1 = f"Hi {f}, saw {co} has had a {role} opening up since {month((s['oldest'] or {}).get('date')) or 'recently'}, with {others} other hourly roles open.\n\nWhile you hire, GigWorx can cover the shifts. You post a shift in our app, vetted local workers claim it, and you only pay for the hours worked.\n\nWant me to comp your first {role} shift so you can see the quality for yourself?"
    elif camp == 'C2':
        j = (s['seasonal'] or [s['oldest']])[0] or {}; seas = 'seasonal ' if s['seasonal'] else ''
        m1 = f"Hi {f}, noticed {co} is hiring {seas}{clean_role(j.get('title'))} help in {j.get('city') or city}.\n\nPeak is when call-offs hurt most. GigWorx fills short-notice shifts with vetted local workers, and you only pay for the hours worked. No contract to unwind in January.\n\nWant your first peak shift on us?"
    elif camp == 'C3':
        m1 = (f"Hi {f}, saw {co} is hiring {role} in {city}.\n\nRV builds swing with dealer orders, so a lot of plants around here run short on the line one month and overstaffed the next. GigWorx lets you add vetted workers by the shift and only pay for the hours worked.\n\nWant me to comp a shift on your next ramp?"
              if role else f"Hi {f}, RV builds swing with dealer orders, so a lot of plants around here run short on the line one month and overstaffed the next.\n\nHow are you covering ramps at {co} today: overtime, agency, or running short?")
    elif camp == 'C4':
        m1 = f"Hi {f}, saw {co} has {s['open']} hourly roles open, including {role}.\n\nGigWorx lets you see people work real shifts before you make an offer. Our workers are vetted W-2 employees on our payroll, and there are no minimum hours before you can hire one onto your team.\n\nWant your first shift on us to try it?"
    elif camp == 'C5':
        m1 = f"Hi {f}, quick question from one local business owner to another.\n\nWhen a couple of people call off at {co}, who ends up covering? You, overtime, or does the work just wait?"
    else:
        j = s['hosp'][0]
        r6 = (clean_role(j['title']) or 'shift').lower()
        m1 = f"Hi {f}, saw {co} is looking for {r6} help in {j.get('city') or city}.\n\nGigWorx fills short-notice shifts with vetted local W-2 workers, so you can add hands for a busy weekend or an event and only pay for the hours worked.\n\nWant me to comp a shift on your next one?"
    out.append({**p, 'first_name': f, 'company': co, 'company_linkedin_url': c['linkedin_url'], 'company_domain': dom or None,
                'company_size': c.get('size'), 'segment': label[p['n']], 'segment_reason': reason.get(p['n']),
                'hourly_jobs_60d': s['open'], 'aged_30d': s['aged30'], 'role_title': role, 'posted_month': month((s['oldest'] or {}).get('date')),
                'open_roles_count': others if camp == 'C1' else s['open'], 'city': city, 'job_url': (s['oldest'] or {}).get('url'),
                'email': em if em_ok else None, 'email_dropped_mismatch': bool(em and not em_ok), 'message_1': m1,
                'copy_variant': 'signal' if (camp != 'C5' and role) else ('question-only' if camp in ('C3', 'C5') else 'signal')})

json.dump(out, open(f'{D}/leads_all.json', 'w'))
json.dump(_CACHE, open(_CACHE_F, 'w'))
comp = [{'n': n, 'name': C[n].get('name'), 'linkedin_url': C[n].get('linkedin_url'), 'size': C[n].get('size'), 'label': label[n], 'reason': reason.get(n),
         'planned': plan.get(n, []), 'assigned': assign.get(n, []), 'hourly_jobs_60d': len(JOBS.get(n, []))} for n in label]
json.dump(comp, open(f'{D}/companies_all.json', 'w'))
from collections import Counter
st = {'labels': Counter(label.values()), 'label_rows_rejected': bad, 'planned': Counter(x for v in plan.values() for x in v),
      'assigned': Counter(x for v in assign.values() for x in v), 'people_raw': len(PEOPLE), 'people_unique': len(uniq),
      'by_campaign': Counter(p['campaign'] for p in out), 'emails': sum(1 for p in out if p['email']),
      'email_mismatch_dropped': sum(1 for p in out if p['email_dropped_mismatch']), 'calls': calls}
json.dump(st, open(f'{D}/stats.json', 'w'), default=dict, indent=1)
print(json.dumps(st, default=dict, indent=1))
