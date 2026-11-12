"""Regenerate catalog.md / catalog.json from openapi.json in this folder (offline; no API calls).
Refresh the spec first: curl -sS https://api.coldiq.com/openapi.json -H "User-Agent: algo-clients" -o openapi.json
"""
import json, re, collections


def fmt(c):
    if not c: return None
    if 'amount' in c: s=f"{c['amount']} cr/{c['unit']} ({c['billing_shape']})"
    else: s=f"{', '.join(f'{k}={v}' for k,v in c.get('rates',{}).items())} cr/{c['unit']} ({c['billing_shape']})"
    if c.get('rows_per_call'): s+=f", {c['rows_per_call']} rows/call"
    return s
d = json.load(open('openapi.json'))
S = d['components']['schemas']
TAGS = {t['name']: t for t in d['tags']}
USD = 0.014285714285714287  # from GET /v1/me/credits usd_per_credit (1/70)

SLUG = {'LinkUp API':'linkup-api','Lima Data':'lima-data','Meta Ads Library':'meta-ads-library','LinkedIn Ad Library':'linkedin-ad-library',
        'Twitter Ads Scraper':'twitter-ads-scraper','Google Ads':'google-ads','Google Maps':'google-maps','LinkedIn Jobs API':'linkedin-jobs-api',
        'Career Site Jobs':'career-site-jobs','Influencers Club':'influencers-club','ColdIQ Mailbox':'coldiq-mailbox','Visitor ID':'visitor-id',
        'GTM Verbs':'gtm-verbs','AI Ark':'ai-ark'}
def mp_url(t): return f"https://coldiq.com/marketplace/apis/{SLUG.get(t, t.lower().replace(' ','-'))}"

CATS = [
 ('Managed GTM verbs (ColdIQ waterfall over many providers)', ['GTM Verbs']),
 ('People & company search / B2B databases', ['AI Ark','Prospeo','Apollo','Lima Data','DiscoLike','LinkUp API','Sumble','Wiza','Openmart']),
 ('LinkedIn scraping & engagement extraction', ['HarvestAPI','LeadsFactory','Jungler']),
 ('Email / phone finding & verification', ['FullEnrich','Findymail','Icypeas','LeadMagic','BounceBan']),
 ('Signals, intent, technographics & job postings', ['PredictLeads','Signalbase','TheirStack','BuiltWith','LinkedIn Jobs API','Career Site Jobs']),
 ('Ad intelligence', ['Adyntel','LinkedIn Ad Library','Meta Ads Library','Google Ads','Twitter Ads Scraper']),
 ('Web search, crawling & SEO', ['Exa','Jina','Serper','DataForSEO']),
 ('Social / web / local scraping', ['Twitter','Reddit','Google Maps','Influencers Club']),
 ('Outreach, sequencing & messaging (BYOK)', ['Instantly','Lemlist','Unipile']),
 ('CRM (BYOK)', ['Attio']),
 ('ColdIQ-native products', ['Visitor ID','ColdIQ Mailbox','Mailboxes']),
 ('Account, billing & workspace admin', ['Account','Public','Dashboard','Team','Slack','Connections','Chats']),
]

REL = {
 'GTM Verbs': 'HIGH. /v1/people/search and /v1/companies/search are provider-agnostic waterfalls (AI Ark, Prospeo, Apollo, LinkUp, Lima Data, DiscoLike, etc.) with charge-on-success billing, max_credits caps and 50-row batching; /v1/person/enrich resolves a person to a LinkedIn profile. Best default entry point.',
 'AI Ark': 'HIGH. Cheapest large people/company DB here (people 1.03 cr/returned person, companies 0.21 cr/returned company); returns LinkedIn URLs. Same vendor the repo already calls directly.',
 'Prospeo': 'HIGH. Person/company search with 30+ filters at 3.5 cr/call; enrich by LinkedIn URL. Same vendor already used directly by the repo.',
 'Apollo': 'MEDIUM. People/org search at 9.91 cr per CALL (flat, not per row) - results are obfuscated (last names hidden) unless revealed; LinkedIn URLs available on match/enrich. Pricier per useful row than AI Ark/Prospeo.',
 'Lima Data': 'MEDIUM-HIGH. Database search-people/search-companies/search-employees at 0.35 cr/result is very cheap; the "prospect" (LinkedIn/Sales-Nav-style) endpoints are expensive (87.5 cr/call). Has company-linkedin finder (3.5 cr).',
 'DiscoLike': 'MEDIUM. Lookalike-domain company discovery (TAM from seed domains) - company-level; 37.8 cr/query + 0.74 cr/record. Same vendor used by listbuild directly (currently overdrawn there - via ColdIQ it bills ColdIQ credits instead).',
 'LinkUp API': 'MEDIUM. LinkedIn-profile/company search at 6.3 cr per 10 results, plus funded/hiring-company lists.',
 'Sumble': 'MEDIUM. Find people by role at orgs (2.1 cr/result), org find/match by technology; good for tech-stack-defined segments.',
 'Wiza': 'LOW-MEDIUM. LinkedIn prospect search at 17.5 cr/profile - expensive for LinkedIn-URL-only needs; value is in email/phone reveals.',
 'Openmart': 'LOW. Local/retail/SMB business search - only for local-business ICPs.',
 'HarvestAPI': 'HIGH. Real-time LinkedIn without a LinkedIn account: profile search (0.67 cr/10 results), Sales Navigator lead search and account search (16.8 cr/25 results), company search (0.67 cr/50), post engagers. Directly yields LinkedIn URLs; fills the "Sales Nav not wired in" gap.',
 'LeadsFactory': 'HIGH. Contact Finder (titles across a company list, 0.35 cr/contact) and Sales Navigator search scraper (0.35 cr/profile) on ColdIQ\'s shared SN account - cheapest LinkedIn-URL-per-row option in the catalog.',
 'Jungler': 'MEDIUM. Pull commenters/reactors from a LinkedIn post (35 cr/task, results free) - intent-based LinkedIn lists.',
 'FullEnrich': 'LOW. Email/phone waterfall from LinkedIn URL; people/company search at 11.63 cr/result (pricey).',
 'Findymail': 'LOW. Email finder/verifier; employee search (3.57 cr/result) and cheap lookalike companies (0.36 cr/result) are the sourcing-relevant parts. Note even list/admin calls cost 3.57 cr.',
 'Icypeas': 'MEDIUM. Beyond email: find-people / find-companies (1.05 cr/result) and URL-search (find a LinkedIn profile/company page from name+company, 1.05 cr) - cheap LinkedIn URL resolution.',
 'LeadMagic': 'LOW-MEDIUM. Mostly email/mobile; employee-finder (0.21 cr/employee) and role-finder are sourcing-relevant.',
 'BounceBan': 'LOW. Email verification (catch-all) only.',
 'PredictLeads': 'MEDIUM (signals). Job openings, financing, news, tech detections, similar companies - "why now" triggers and lookalikes; 2.51 cr per call/result.',
 'Signalbase': 'MEDIUM (signals). Funding, acquisition, job-change, hiring signals at 3.5 cr/call.',
 'TheirStack': 'MEDIUM (signals). Jobs by tech stack, companies by technology usage, buying intents (12.6 cr/company).',
 'BuiltWith': 'LOW-MEDIUM. Tech-stack profiling of a domain / list of sites using a tech (3.13 cr/call).',
 'LinkedIn Jobs API': 'MEDIUM (signals). LinkedIn job search (0.74 cr/job) - hiring-intent company lists.',
 'Career Site Jobs': 'MEDIUM (signals). ATS/career-site job postings (1.26 cr/job) with LinkedIn company data.',
 'Adyntel': 'LOW. Ad intelligence by domain/keyword (1.85 cr/call).',
 'LinkedIn Ad Library': 'LOW. Who advertises on LinkedIn (0.21 cr/ad) - possible intent signal.',
 'Meta Ads Library': 'LOW. Facebook/Instagram ads scraping.',
 'Google Ads': 'LOW. Google Ads Transparency scraping.',
 'Twitter Ads Scraper': 'LOW. X ad transparency scraping.',
 'Exa': 'LOW-MEDIUM. Semantic web search/crawl for research and signals (repo already has a direct Exa key).',
 'Jina': 'LOW. Web reader/search/rerank/classify, token-billed - research utility.',
 'Serper': 'LOW-MEDIUM. Very cheap Google SERP (0.063 cr/call) - useful for "site:linkedin.com/in" style URL resolution and research.',
 'DataForSEO': 'LOW. SEO/SERP/backlink data.',
 'Twitter': 'LOW. Tweet scraping.',
 'Reddit': 'LOW. Reddit scraping.',
 'Google Maps': 'LOW. Places/reviews scraping - local-business ICPs only.',
 'Influencers Club': 'NONE. Creator/influencer data (125.58 cr/call) - not B2B.',
 'Instantly': 'NONE for sourcing. Cold-email platform control (BYOK, free in credits).',
 'Lemlist': 'NONE for sourcing. Outreach platform control (BYOK, free).',
 'Unipile': 'LOW. LinkedIn/WhatsApp/email messaging API (BYOK, free in credits) - outreach side, not sourcing.',
 'Attio': 'NONE for sourcing. CRM (BYOK, free).',
 'Visitor ID': 'LOW-MEDIUM. Website visitor de-anonymization incl. LinkedIn profiles; needs a pixel on a client site.',
 'ColdIQ Mailbox': 'NONE for sourcing. Buy domains/inboxes (subscription-billed, 0 credits).',
 'Mailboxes': 'NONE. Dashboard-session versions of the mailbox routes (not usable with the API key).',
 'Account': 'USEFUL. GET /v1/me/credits is the free balance + usd_per_credit check.',
 'Public': 'Info only. Public price lists (no auth).',
 'Dashboard': 'Admin. Requires a dashboard session JWT - API key returns 401 "Malformed session token".',
 'Team': 'Admin (dashboard session).', 'Slack': 'Admin (dashboard session).', 'Connections': 'Admin: where BYOK provider keys are stored (dashboard session).', 'Chats': 'Admin (dashboard session).',
}
WHAT = {'Mailboxes':'Dashboard (session-auth) mailbox purchase/management routes mirroring ColdIQ Mailbox.',
        'Account':'API-key account endpoints: credit balance and feedback.','Public':'Unauthenticated public billing/product listings.',
        'Dashboard':'Web dashboard routes: billing, API keys, usage, credits, quota, Visitor ID websites.','Connections':'Store/validate your own (BYOK) provider API keys.',
        'Chats':'Saved ColdIQ agent chats.'}

def resolve(s, depth=0):
    if not isinstance(s, dict) or depth > 4: return s or {}
    if '$ref' in s: return resolve(S.get(s['$ref'].split('/')[-1], {}), depth+1)
    if 'allOf' in s:
        out = {'properties': {}}
        for x in s['allOf']: out['properties'].update(resolve(x, depth+1).get('properties', {}))
        return out
    return s

def params_of(o):
    ps = []
    for p in o.get('parameters', []):
        if '$ref' in p: p = d['components']['parameters'].get(p['$ref'].split('/')[-1], {})
        desc = p.get('description') or p.get('schema', {}).get('description') or ''
        if re.search(r'Your .* (API key|access token|DSN)', desc): continue
        ps.append({'name': p.get('name'), 'in': p.get('in'), 'required': p.get('required', False), 'description': desc[:200]})
    rb = o.get('requestBody', {}).get('content', {})
    sch = resolve(next(iter(rb.values()), {}).get('schema', {})) if rb else {}
    props = sch.get('properties', {})
    req = set(sch.get('required', []))
    wrapped = 'input' in props
    if wrapped:
        inner = resolve(props['input'])
        for k, v in inner.get('properties', {}).items():
            v = resolve(v); ps.append({'name': f'input.{k}', 'in': 'body', 'required': k in set(inner.get('required', [])), 'description': (v.get('description') or '')[:200]})
    for k, v in props.items():
        if wrapped and k == 'input': continue
        v = resolve(v)
        if k in ('api_key','access_token','dsn') : continue
        ps.append({'name': k, 'in': 'body', 'required': k in req, 'description': (v.get('description') or '')[:200]})
    return ps

by = collections.defaultdict(list)
for path, ops in d['paths'].items():
    for m, o in ops.items():
        if m == 'parameters': continue
        t = o['tags'][0]
        desc = re.sub(r'\s*Call get_endpoint_details for the live rate\.?', '', o.get('description', '')).strip()
        by[t].append({'method': m.upper(), 'path': path, 'summary': o.get('summary'), 'description': desc[:600],
                      'params': params_of(o), 'cost_raw': o.get('x-credits-cost'), 'cost': fmt(o.get('x-credits-cost')),
                      'auth': 'bearer (API key)' if o.get('security') else ('none (public)' if o.get('security') == [] else 'dashboard session JWT (not API key)' if path.startswith('/dashboard') else 'none declared'),
                      })

covered = [t for _, ts in CATS for t in ts]
missing = [t for t in by if t not in covered]
assert not missing, missing

def cost_summary(eps):
    c = collections.Counter(e['cost'] for e in eps if e['cost'])
    return '; '.join(f'{k} x{v}' for k, v in c.most_common(4)) + (' ...' if len(c) > 4 else '') if c else 'not stated (no x-credits-cost)'

catalog = []
for cat, ts in CATS:
    for t in ts:
        eps = by[t]; tag = TAGS.get(t, {})
        ext = (tag.get('externalDocs') or {}).get('url')
        byok = any(re.search(r'Optional if you have connected', json.dumps(e)) for e in eps) or t in ('Instantly','Lemlist','Attio','Unipile')
        catalog.append({'provider': t, 'category': cat, 'what_it_does': tag.get('description') or WHAT.get(t, ''),
            'endpoint_count': len(eps), 'endpoints': [{k: e[k] for k in ('method','path','summary','description','params','cost','auth')} | {'cost_raw': e['cost_raw']} for e in eps],
            'cost': cost_summary(eps), 'byok': byok,
            'doc_url': {'coldiq_api_reference': 'https://api.coldiq.com/docs', 'coldiq_marketplace_page': mp_url(t) if t in TAGS and t not in ('Mailboxes',) else None, 'vendor_docs': ext},
            'relevance_linkedin_first': REL.get(t, ''),
            'source_of_info': 'OpenAPI spec GET https://api.coldiq.com/openapi.json (fetched 2026-09-30): tags, paths, x-credits-cost, request schemas. Category + relevance note are my classification (inferred). Provider list cross-checked against https://coldiq.com/marketplace/apis (45 entries = 45 declared spec tags; 51 tags in use incl. 6 undeclared admin tags).'})

meta = {'generated': '2026-09-30', 'spec': {'url': 'https://api.coldiq.com/openapi.json', 'openapi': d['openapi'], 'title': d['info']['title'], 'version': d['info']['version'],
        'paths': len(d['paths']), 'operations': sum(len(v) for v in by.values()), 'tags': len(d['tags'])},
        'interactive_docs': 'https://api.coldiq.com/docs (Scalar UI over the same spec)',
        'base_url': 'https://api.coldiq.com', 'auth': 'Authorization: Bearer $COLDIQ_API_KEY; send a User-Agent (Python-urllib UA gets a bare 403 at Cloudflare)',
        'rate_limit': d['x-rate-limit'], 'credit_usd': {'usd_per_credit': USD, 'note': '1 credit = $0.0142857 (1/70), from GET /v1/me/credits; spec warns not to assume a round number'},
        'free_account_endpoint': 'GET /v1/me/credits -> {balance, usedThisMonth, usd_per_credit, credit_rate_plan, billing_scope}',
        'balance_at_research_time': {'balance': 1.7246, 'usedThisMonth': 23703.2754, 'checked': '2026-09-30'},
        'billing_notes': ['x-credits-cost billing_shape: per_call (flat per request even if 0 rows), per_result, per_page (N rows per charge), per_call_variable (rate depends on options), query_plus_record.',
                          'Charges are reported in the X-ColdIQ-Credits-Charged response header (per spec).',
                          'GTM verbs are charge-on-success with a per-record max_credits cap; up to 50 inputs per request count as 1 request for rate limiting.',
                          'Instantly/Lemlist/Attio/Unipile routes cost 0 credits but need your own account key (param or dashboard connection).',
                          'Operations without x-credits-cost: GTM verbs (priced by the routed provider), account/dashboard/public/admin routes.']}
json.dump({'meta': meta, 'providers': catalog}, open('catalog.json', 'w'), indent=1)

# ---------- markdown ----------
L = []
A = L.append
A('# ColdIQ API gateway - full catalog\n')
A(f"Generated 2026-09-30 from the live OpenAPI spec `GET https://api.coldiq.com/openapi.json` ({d['info']['title']} v{d['info']['version']}, OpenAPI {d['openapi']}): "
  f"**{len(d['paths'])} paths / {meta['spec']['operations']} operations / {len(d['tags'])} declared tags**. Interactive docs: https://api.coldiq.com/docs. "
  "Provider list cross-checked against https://coldiq.com/marketplace/apis (45 entries, identical to the 45 tags the spec declares; operations also use 6 undeclared admin tags - Account, Public, Dashboard, Chats, Connections, Mailboxes - for 51 in use).\n")
A('**Source key:** everything below (endpoints, params, costs, vendor doc URLs) is read from the spec unless marked *(inferred)*. Categories and the relevance notes are my own classification.\n')
A('## Essentials\n')
A('- Base URL `https://api.coldiq.com`, header `Authorization: Bearer $COLDIQ_API_KEY`. **Send a User-Agent**: default `Python-urllib` is blocked at Cloudflare with a bare 403 (spec note).')
A(f"- Rate limit (per billing account, shared by all keys): 120 req/min, 3000 req/h; a batched verb call (`inputs[]`, <=50 rows) counts as 1. 429 carries `Retry-After`.")
A('- **Free balance check:** `GET /v1/me/credits` -> `balance`, `usedThisMonth`, `usd_per_credit`, `credit_rate_plan`, `billing_scope`. Checked 2026-09-30: **balance 1.72 credits, 23,703 used this month**, usd_per_credit = **0.0142857 ($1 = 70 credits)**. Balance is effectively empty; any paid call will 402.')
A('- `/dashboard/*` routes (credits, quota, usage, API keys, team, connections) need a dashboard session JWT - the API key gets `401 Malformed session token`. `/public/billing/*` needs no auth (price lists).')
A('- Credit packs (from `GET /public/billing/products`): PAYG $100 = 6,000 cr ... $2,000 = 135,000 cr; subscriptions Starter $99/mo = 7,000 cr, Pro $199/mo = 15,000, Scale $499/mo = 40,000.')
A('- Cost shapes (`x-credits-cost`): `per_call` = flat per request even if nothing returns; `per_result`; `per_page` (N rows per charge); `per_call_variable`; `query_plus_record`. Actual charge returned in `X-ColdIQ-Credits-Charged` header.')
A('- **Correction to prior assumption:** `POST /v1/apollo/people/search` is **not free** - spec prices it at **9.91 credits per call** (flat, ~$0.14), results obfuscated. Earlier "free preview" test calls were most likely billed.')
A('- Many per-provider endpoints say "Managed alternative: POST /v1/<verb>" - the GTM verb runs that provider in a waterfall with charge-on-success billing.\n')
A('## Summary by category\n')
A('| Category | Providers | Operations |'); A('|---|---|---|')
for cat, ts in CATS:
    A(f"| {cat} | {', '.join(ts)} | {sum(len(by[t]) for t in ts)} |")
A('')
A('## Top picks for LinkedIn-first sourcing\n')
A('| Rank | Tool | Endpoint(s) | Cost (credits; x $0.0143) | Why |'); A('|---|---|---|---|---|')
tops = [
 ('GTM verb Find People', '`POST /v1/people/search`', 'charge-on-success; routed provider rate; `max_credits` cap', 'One normalized schema (100+ filters incl. company_linkedin_urls, titles, seniorities, headcount, industries, max_per_company); routable providers: AI Ark, LeadMagic, Findymail, Prospeo, LinkUp, Apollo, FullEnrich, Lima Data (the default auto waterfall order is not stated in the spec); 50 rows/request'),
 ('GTM verb Search Companies', '`POST /v1/companies/search`', 'charge-on-success', 'Firmographic / tech / funding / hiring / lookalike (`similar_to_domains` -> DiscoLike) account lists; `linkedin_search_url` input'),
 ('LeadsFactory', '`POST /v1/leadsfactory/contact-finder/searches`, `POST /v1/leadsfactory/sn-scraper/jobs` (+ GET status, free)', '0.35/contact, 0.35/profile', 'Titles across a company list, and Sales Navigator search-URL scraping on ColdIQ\'s shared SN seat - cheapest LinkedIn URL per row'),
 ('HarvestAPI', '`GET /v1/harvestapi/linkedin/lead-search`, `/account-search`, `/profile-search`, `/company-search`, `/profile`, `/company`', '16.8/25 SN leads; 0.67/10 profiles; 0.67/50 companies; 0.67-1.07/profile', 'Live LinkedIn + Sales Navigator search without an account'),
 ('AI Ark', '`POST /v1/ai-ark/people`, `POST /v1/ai-ark/companies`', '1.03/returned person; 0.21/returned company', 'Large DB, LinkedIn URLs, cheap per row'),
 ('Lima Data (database)', '`POST /v1/limadata/database/search-people`, `/search-employees`, `/search-companies`; `POST /v1/limadata/find/company-linkedin`', '0.35/result; 3.5/call', 'Very cheap per row; company LinkedIn finder'),
 ('Prospeo', '`POST /v1/prospeo/search-person`, `/search-company`, `/enrich-person`', '3.5/call', '30+ filters, enrich by LinkedIn URL'),
 ('Icypeas', '`POST /v1/icypeas/find-people`, `/find-companies`, `/url-search/profile(s)`, `/url-search/company(ies)`', '1.05/result or call', 'Cheap people/company search and name->LinkedIn URL resolution'),
 ('Jungler / Lima Data posts', '`POST /v1/jungler/workbooks`; `POST /v1/limadata/posts/reactions`', '35/task; 7/reaction', 'LinkedIn post engagers as intent lists'),
 ('Sumble / LinkUp', '`POST /v1/sumble/people/find`; `POST /v1/linkupapi/data/search/profiles`', '2.1/result; 6.3/10 results', 'Role-at-org and LinkedIn profile search alternatives'),
]
for i, (a, b, c, e) in enumerate(tops, 1): A(f'| {i} | {a} | {b} | {c} | {e} |')
A('\nSignals worth pairing (why-now): PredictLeads (`/v1/predictleads/discover/job_openings`, `/discover/financing_events`), Signalbase (`/v1/signalbase/*-signals`), TheirStack, LinkedIn Jobs API, Career Site Jobs, or the verb `POST /v1/signals/find`.\n')

A('## GTM verbs - routing slugs *(read from each verb\'s `provider` field description)*\n')
for e in by['GTM Verbs']:
    o = d['paths'][e['path']][e['method'].lower()]
    rb = o.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {}).get('properties', {})
    m = re.search(r'Valid slugs for this verb: (.*?)\. These', rb.get('provider', {}).get('description', ''))
    A(f"- `{e['method']} {e['path']}` - {e['summary']}" + (f" - providers: {m.group(1)}" if m else ''))
A('')

for cat, ts in CATS:
    A(f'## {cat}\n')
    for t in ts:
        p = next(x for x in catalog if x['provider'] == t)
        A(f"### {t}\n")
        A(f"- **What:** {p['what_it_does']}")
        A(f"- **Docs:** vendor {p['doc_url']['vendor_docs'] or '-'} | ColdIQ {p['doc_url']['coldiq_marketplace_page'] or '-'} | reference https://api.coldiq.com/docs")
        A(f"- **Cost (spec x-credits-cost):** {p['cost']}")
        if p['byok']: A('- **BYOK:** needs your own account key (per-request key param or a dashboard connection); routes cost 0 ColdIQ credits.')
        A(f"- **Relevance (LinkedIn-first sourcing):** {p['relevance_linkedin_first']}")
        A(f"- **Endpoints ({p['endpoint_count']}):**\n")
        big = len(p['endpoints']) > 40
        for e in p['endpoints']:
            keyp = [x['name'] for x in e['params']][:10]
            more = len(e['params']) - len(keyp)
            ptxt = '' if big or not keyp else ' - params: `' + '`, `'.join(keyp) + '`' + (f' (+{more})' if more > 0 else '')
            A(f"  - `{e['method']} {e['path']}` - {e['summary']}" + (f" - **{e['cost']}**" if e['cost'] and not big else '') + ptxt)
        if big: A('  - *(parameters omitted here for this large provider; see catalog.json)*')
        A('')
A('## Not in the gateway\n')
A('coldiq.com/apis/<name>-api pages (e.g. hunter-api, rocketreach-api, saleshandy-api, valid8-api, servicenow-api, apify-api) are a generic **API directory** on ColdIQ\'s marketing site linking to each vendor\'s own docs - they are *not* routed through api.coldiq.com (verified on hunter/rocketreach/saleshandy pages; none has a `/v1/<vendor>` path in the spec). Hunter, RocketReach, Saleshandy, Smartlead, Clay, Blitz are not gateway providers (Smartlead appears only as a mailbox-export target).\n')
A('## Caveats\n')
A('- Costs are the spec\'s published `x-credits-cost`; descriptions say "call get_endpoint_details for the live rate" (an agent/MCP tool, not an HTTP route in the spec), so live rates may differ.')
A('- No provider data endpoint was called during this research. Only free calls made: `/openapi.json`, `/docs`, `/health`, `GET /v1/me/credits`, `GET /public/billing/products`, `GET /public/billing/lite-products`, and three `/dashboard/*` reads (401).')
A('- Async providers (Twitter, Reddit, Google Maps, ad libraries, job APIs) submit a job then poll a free `GET .../{jobId}`; that they are Apify actors underneath is *(inferred)* from the pattern only.')
open('catalog.md', 'w').write('\n'.join(L))
print('ok', len(catalog), meta['spec'])
for cat, ts in CATS: print(cat, len(ts), sum(len(by[t]) for t in ts))
