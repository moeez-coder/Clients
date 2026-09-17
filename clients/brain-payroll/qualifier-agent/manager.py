#!/usr/bin/env python3
"""
Brain Payroll qualifier agent manager.

Turns the combined company universe into per-company QUALIFIED / LIKELY / DISQUALIFIED
verdicts. Two tiers, because spinning one LLM sub-agent per company for 2,492 companies
is neither affordable nor necessary:

  Tier 1  evidence   deterministic, every company, ~1.5 ColdIQ credits each.
                     Site-scoped search of the company's OWN domain for a payroll
                     service page. Cheap, parallel, and it answers the question
                     outright for most rows.
  Tier 2  adjudicate LLM sub-agents, one per shard of companies, reading the Tier-1
                     evidence pack and applying rubric.md. This is where judgment
                     calls live: is this a bureau or an end employer, is this firm a
                     competitor, was it acquired.

Subcommands
-----------
  evidence    Tier 1. Collect website evidence for every company in the universe CSV.
  shard       Split the evidence into JSON shards for sub-agents, + a brief per shard.
  merge       Fold sub-agent verdict JSON back into a verdicts CSV joined to the universe.
  status      Show how far through the pipeline we are.

Usage
-----
  python3 manager.py evidence --limit 250        # omit --limit for the whole universe
  python3 manager.py shard --size 60
  python3 manager.py merge

Requires COLDIQ_API_KEY in the environment. See README.md in this directory.
"""
import os,json,csv,sys,argparse,threading,time,urllib.request
import concurrent.futures as cf

HERE=os.path.dirname(os.path.abspath(__file__))
UNIVERSE=os.path.join(HERE,'..','sourcing','2026-09-17-combined-universe-companies.csv')
WORK=os.path.join(HERE,'work')
EVIDENCE=os.path.join(WORK,'evidence.jsonl')
SHARDS=os.path.join(WORK,'shards')
VERDICTS=os.path.join(WORK,'verdicts')
OUT=os.path.join(HERE,'..','sourcing','2026-09-17-combined-universe-verdicts.csv')

CIQ='https://api.coldiq.com'
def ciq(path,body,tries=3):
    """ColdIQ needs a non-default User-Agent: Python-urllib is blocked at the Cloudflare
    edge and returns a bare 403 that looks exactly like an auth failure."""
    K=os.environ['COLDIQ_API_KEY']
    for a in range(tries):
        r=urllib.request.Request(CIQ+path,data=json.dumps(body).encode(),
            headers={'Content-Type':'application/json','Authorization':'Bearer '+K,
                     'User-Agent':'algo-acquisition-qualifier/1.0'})
        try:
            with urllib.request.urlopen(r,timeout=120) as resp: return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            b=e.read()[:200].decode('utf8','replace')
            if e.code in (429,503): time.sleep(2+3*a); continue
            return {'_err':f'{e.code} {b}'}
        except Exception: time.sleep(1+a)
    return {'_err':'retries exhausted'}

def load_universe():
    with open(UNIVERSE) as f: return list(csv.DictReader(f))

# ---------------------------------------------------------------- Tier 1: evidence
PAYROLL_PAGE_HINTS=('payroll','bureau','umbrella','cis','paye','auto enrolment','auto-enrolment')
_STOP={'limited','ltd','llp','group','the','and','accountants','accountancy','chartered',
       'services','service','company','partners','associates','consulting','consultants',
       'solutions','payroll','advisory','advisers','advisors','financial','business','tax',
       'uk','ireland','plc','co','part','of'}

def name_tokens(name):
    import re as _r
    return {t for t in _r.findall(r'[a-z0-9]{3,}',(name or '').lower()) if t not in _STOP}

def pages_mention_company(name,pages):
    """Does the fetched content actually belong to THIS company?

    Source APIs sometimes attach a domain belonging to an entirely different entity —
    observed live: an accountancy practice carrying mail.co.uk (a German email provider),
    another carrying bms.com, a third carrying a borough council's site. Because Tier-1
    evidence is domain-scoped, a wrong domain silently returns a *different company's*
    payroll page and would manufacture a confident false QUALIFIED. Cheap guard: at least
    one distinctive token of the company name should appear in the fetched title/text.
    Abbreviated domains are fine (hwca.com for Haines Watts) — this checks the CONTENT,
    not the domain string."""
    toks=name_tokens(name)
    if not toks or not pages: return None          # unknown, not a failure
    blob=' '.join(((p.get('title') or '')+' '+(p.get('text') or '')) for p in pages).lower()
    return any(t in blob for t in toks)

def collect_one(row):
    dom=row.get('domain','-')
    if dom in ('','-'):
        return {'company_linkedin_tag':row['company_linkedin_tag'],'name':row['name'],
                'pages':[],'error':'no-domain'}
    d=ciq('/v1/exa/search',{'query':f'payroll services for clients site:{dom}',
                            'numResults':4,
                            'contents':{'text':{'maxCharacters':900}}})
    if '_err' in d:
        return {'company_linkedin_tag':row['company_linkedin_tag'],'name':row['name'],
                'pages':[],'error':d['_err'][:120]}
    pages=[]
    for res in (d.get('results') or []):
        url=res.get('url') or ''; txt=(res.get('text') or '').strip()
        # keep only pages that are actually on this company's own domain — a site:
        # query can still return aggregators, and an off-domain page is not evidence
        # that THIS firm offers payroll.
        if dom.lower() not in url.lower(): continue
        low=(url+' '+txt).lower()
        pages.append({'url':url,'title':res.get('title'),
                      'text':' '.join(txt.split())[:900],
                      'payroll_mentioned':any(h in low for h in PAYROLL_PAGE_HINTS)})
    return {'company_linkedin_tag':row['company_linkedin_tag'],'name':row['name'],
            'domain':dom,'pages':pages,'error':'',
            'domain_matches_company':pages_mention_company(row['name'],pages)}

def cmd_evidence(args):
    os.makedirs(WORK,exist_ok=True)
    rows=load_universe()
    done=set(); failed=set()
    if os.path.exists(EVIDENCE) and not args.restart:
        keep=[]
        with open(EVIDENCE) as f:
            for l in f:
                try: e=json.loads(l)
                except Exception: continue
                # A transient API failure is not a result. With --retry-failed we drop
                # those rows so the resume logic picks them up again; 'no-domain' is a
                # permanent property of the row, so it stays done.
                if args.retry_failed and e.get('error') and e['error']!='no-domain':
                    failed.add(e['company_linkedin_tag']); continue
                keep.append(e); done.add(e['company_linkedin_tag'])
        if args.retry_failed and failed:
            with open(EVIDENCE,'w') as f:
                for e in keep: f.write(json.dumps(e)+'\n')
            print(f're-queued {len(failed)} previously-failed rows')
    todo=[r for r in rows if r['company_linkedin_tag'] not in done]
    if args.only_medium: todo=[r for r in todo if r['icp_confidence']=='medium']
    if args.limit: todo=todo[:args.limit]
    print(f'universe {len(rows)} | already done {len(done)} | collecting {len(todo)}')
    lock=threading.Lock(); n=[0]
    mode='w' if args.restart else 'a'
    with open(EVIDENCE,mode) as out, cf.ThreadPoolExecutor(args.workers) as ex:
        for res in ex.map(collect_one,todo):
            with lock:
                out.write(json.dumps(res)+'\n'); n[0]+=1
                if n[0]%100==0: out.flush(); print(f'  {n[0]}/{len(todo)}',flush=True)
    print('evidence rows written:',n[0])

# ---------------------------------------------------------------- Tier 2: shards
BRIEF="""You are a qualification sub-agent for Brain Payroll UK Limited.

Read the rubric at {rubric} and apply it to EVERY company in {shard}.

Each company comes with an evidence pack: pages found on its own website by a
site-scoped search for payroll services. Use that first. Where the pack is empty,
inconclusive, or contradicts the firmographics, research the company yourself
(its website, LinkedIn, recent news) before deciding.

The decisive question for every company is the one in the rubric: does this company
process payroll for clients other than itself?

Write your answer as a JSON array of verdict objects, in the rubric's exact schema,
to {outfile}. One object per input company, {n} in total. No prose, no markdown fence.
Do not guess to fill the shard: LIKELY with evidence_quality "none" is the correct
answer for a practice whose website you could not reach.
"""

def cmd_shard(args):
    os.makedirs(SHARDS,exist_ok=True); os.makedirs(VERDICTS,exist_ok=True)
    uni={r['company_linkedin_tag']:r for r in load_universe()}
    ev=[]
    with open(EVIDENCE) as f:
        for l in f:
            try: ev.append(json.loads(l))
            except Exception: pass
    if args.only_unresolved:
        ev=[e for e in ev if not any(p.get('payroll_mentioned') for p in e.get('pages',[]))]
    packs=[]
    for e in ev:
        u=uni.get(e['company_linkedin_tag'])
        if not u: continue
        packs.append({'company_linkedin_tag':u['company_linkedin_tag'],'name':u['name'],
            'domain':u['domain'],'website':u['website'],'linkedin_url':u['linkedin_url'],
            'size_band':u['size_band'],'industry':u['industry'],'hq_country':u['hq_country'],
            'current_segment':u['segment'],'current_confidence':u['icp_confidence'],
            'description':u['description'][:700],
            'evidence_pages':e.get('pages',[])[:4],
            'evidence_domain_matches_company':e.get('domain_matches_company'),
            'evidence_warning':('' if e.get('domain_matches_company') is not False else
                'The fetched pages do not mention this company by name — the domain on this '
                'record may belong to a different entity. Verify the real website before '
                'trusting this pack, and do NOT qualify on it alone.')})
    n=args.size; made=[]
    for i in range(0,len(packs),n):
        idx=i//n
        sp=os.path.join(SHARDS,f'shard-{idx:03d}.json')
        json.dump(packs[i:i+n],open(sp,'w'),indent=1)
        bp=os.path.join(SHARDS,f'shard-{idx:03d}.brief.txt')
        open(bp,'w').write(BRIEF.format(rubric=os.path.join(HERE,'rubric.md'),shard=sp,
            outfile=os.path.join(VERDICTS,f'shard-{idx:03d}.verdicts.json'),n=len(packs[i:i+n])))
        made.append(sp)
    print(f'{len(packs)} companies -> {len(made)} shards of <= {n} in {SHARDS}')

# ---------------------------------------------------------------- merge
def cmd_merge(args):
    uni={r['company_linkedin_tag']:r for r in load_universe()}
    verds={}
    if os.path.isdir(VERDICTS):
        for fn in sorted(os.listdir(VERDICTS)):
            if not fn.endswith('.json'): continue
            try: data=json.load(open(os.path.join(VERDICTS,fn)))
            except Exception as e: print('  skip',fn,e); continue
            for v in (data if isinstance(data,list) else [data]):
                t=v.get('company_linkedin_tag')
                if t: verds[t]=v
    print('verdicts loaded:',len(verds))
    COLS=['company_linkedin_tag','name','domain','hq_country','size_band',
          'verdict','payroll_service_confirmed','segment','evidence_url','evidence_quote',
          'evidence_quality','reason','signals','notes',
          'prior_segment','prior_confidence']
    n=0
    with open(OUT,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=COLS); w.writeheader()
        for t,u in uni.items():
            v=verds.get(t)
            if not v and args.only_verdicts: continue
            v=v or {}
            w.writerow({'company_linkedin_tag':t,'name':u['name'],'domain':u['domain'],
              'hq_country':u['hq_country'],'size_band':u['size_band'],
              'verdict':v.get('verdict','NOT_YET_REVIEWED'),
              'payroll_service_confirmed':v.get('payroll_service_confirmed',''),
              'segment':v.get('segment',u['segment']),
              'evidence_url':v.get('evidence_url','') or '-',
              'evidence_quote':' '.join(str(v.get('evidence_quote','')).split())[:200] or '-',
              'evidence_quality':v.get('evidence_quality','') or '-',
              'reason':v.get('reason','') or '-',
              'signals':'; '.join(v.get('signals') or []) or '-',
              'notes':' '.join(str(v.get('notes','')).split())[:200] or '-',
              'prior_segment':u['segment'],'prior_confidence':u['icp_confidence']}); n+=1
    print(f'wrote {OUT} ({n} rows)')

def cmd_status(args):
    rows=load_universe(); print('universe:',len(rows))
    if os.path.exists(EVIDENCE):
        ev=[json.loads(l) for l in open(EVIDENCE) if l.strip()]
        withp=sum(1 for e in ev if any(p.get('payroll_mentioned') for p in e.get('pages',[])))
        print(f'evidence: {len(ev)} collected | {withp} have a payroll page on their own domain')
    else: print('evidence: none yet')
    for d,lab in ((SHARDS,'shards'),(VERDICTS,'verdict files')):
        print(f'{lab}:',len(os.listdir(d)) if os.path.isdir(d) else 0)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    sub=ap.add_subparsers(dest='cmd',required=True)
    e=sub.add_parser('evidence'); e.add_argument('--limit',type=int); e.add_argument('--workers',type=int,default=12)
    e.add_argument('--restart',action='store_true'); e.add_argument('--only-medium',action='store_true')
    e.add_argument('--retry-failed',action='store_true',
                   help='re-queue rows whose previous attempt errored (not no-domain)')
    e.set_defaults(fn=cmd_evidence)
    s=sub.add_parser('shard'); s.add_argument('--size',type=int,default=60)
    s.add_argument('--only-unresolved',action='store_true'); s.set_defaults(fn=cmd_shard)
    m=sub.add_parser('merge'); m.add_argument('--only-verdicts',action='store_true'); m.set_defaults(fn=cmd_merge)
    st=sub.add_parser('status'); st.set_defaults(fn=cmd_status)
    a=ap.parse_args(); a.fn(a)
