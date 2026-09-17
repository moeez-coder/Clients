#!/usr/bin/env python3
"""
Push the qualified-company set and the decision-maker set to their Clay webhooks.

Clay's "pull in data from a webhook" source takes ONE JSON object per request and
creates one row from it, so this posts records individually with a small worker pool
and a global rate limit. It is deliberately not fire-and-forget: every response code
is counted, failures are written to a file for retry, and --dry-run prints what would
be sent without sending anything.

Sending twice creates DUPLICATE rows in Clay — there is no upsert on this source — so
--state records what has already been sent and is skipped on a re-run.

Usage:
  python3 push_to_clay.py companies --dry-run
  python3 push_to_clay.py companies
  python3 push_to_clay.py prospects --limit 1     # verify the shape on one real row first
"""
import os,sys,json,csv,time,argparse,threading,urllib.request
import concurrent.futures as cf

HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'..','sourcing')
COMPANIES=os.path.join(SRC,'2026-09-17-combined-universe-companies.csv')
VERDICTS=os.path.join(SRC,'2026-09-17-combined-universe-verdicts.csv')
PROSPECTS=os.path.join(SRC,'2026-09-17-combined-universe-leads.csv')

HOOKS={
 'companies':'https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-393d7c98-2437-478b-91bc-72d7449997cc',
 'prospects':'https://api.clay.com/v3/sources/webhook/pull-in-data-from-a-webhook-7e211b54-bf7e-4405-970f-d0e23c0ce76f',
}

_lk=threading.Lock(); _next=[0.0]
def throttle(rps):
    with _lk:
        now=time.time(); wait=_next[0]-now
        if wait>0: time.sleep(wait)
        _next[0]=max(now,_next[0])+1.0/rps

def post(url,rec,rps,tries=4):
    body=json.dumps(rec).encode()
    for a in range(tries):
        throttle(rps)
        r=urllib.request.Request(url,data=body,
          headers={'Content-Type':'application/json','User-Agent':'algo-acquisition-sourcing/1.0'})
        try:
            with urllib.request.urlopen(r,timeout=60) as resp:
                return resp.status,resp.read()[:200].decode('utf8','replace')
        except urllib.error.HTTPError as e:
            b=e.read()[:200].decode('utf8','replace')
            if e.code in (429,500,502,503,504): time.sleep(2**a); continue
            return e.code,b
        except Exception as ex:
            if a==tries-1: return 'ERR',str(ex)[:150]
            time.sleep(2**a)
    return 'ERR','retries exhausted'

def build_companies(verdicts=('QUALIFIED',)):
    """The verdict file is the source of truth for who is in, joined back to the universe
    row for the firmographics Clay will want. `verdicts` selects which verdicts to send —
    the verdict travels with every record so LIKELY rows stay distinguishable in Clay
    rather than being silently mixed in with confirmed ones."""
    uni={r['company_linkedin_tag']:r for r in csv.DictReader(open(COMPANIES))}
    out=[]
    for v in csv.DictReader(open(VERDICTS)):
        if v['verdict'] not in verdicts: continue
        u=uni.get(v['company_linkedin_tag'],{})
        out.append({
          'company_linkedin_url':u.get('linkedin_url') or v.get('domain') or '',
          'company_name':v['name'],'domain':v['domain'],
          'website':u.get('website',''),'description':u.get('description',''),
          'segment':v['segment'],'size_band':v['size_band'],
          'employees':u.get('employees_on_linkedin',''),'industry':u.get('industry',''),
          'hq_city':u.get('hq_city',''),'hq_country':v['hq_country'],
          'verdict':v['verdict'],'payroll_service_confirmed':v['payroll_service_confirmed'],
          'evidence_url':v['evidence_url'],'evidence_quote':v['evidence_quote'],
          'evidence_quality':v['evidence_quality'],'buying_signals':v['signals'],
          'notes':v['notes'],'tier':u.get('tier',''),
          'client':'Brain Payroll','sourced_date':'2026-09-17'})
    return out

def build_prospects():
    """Never send a prospect whose company the qualifier agent disqualified. 237 went out
    before qualification finished — including the co-founder of ANNA Money, which sells
    payroll software. Those are listed in 2026-09-17-clay-suppression-list.csv for
    removal on the Clay side; this filter stops it recurring."""
    out=[]
    for r in csv.DictReader(open(PROSPECTS)):
        if r.get('company_verdict')=='DISQUALIFIED': continue
        out.append(dict(r))
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('what',choices=['companies','prospects'])
    ap.add_argument('--dry-run',action='store_true')
    ap.add_argument('--limit',type=int)
    ap.add_argument('--rps',type=float,default=8)
    ap.add_argument('--workers',type=int,default=8)
    ap.add_argument('--state',default=None,help='file of already-sent keys (skip these)')
    ap.add_argument('--verdict',default='QUALIFIED',
                    help='comma-separated verdicts to send, e.g. LIKELY or QUALIFIED,LIKELY')
    a=ap.parse_args()

    recs=build_companies(tuple(a.verdict.split(','))) if a.what=='companies' else build_prospects()
    keyf=(lambda r:r.get('company_linkedin_url') or r.get('domain')) if a.what=='companies' \
         else (lambda r:r.get('linkedin_url'))
    state=a.state or os.path.join(HERE,'work',f'clay-sent-{a.what}.txt')
    sent=set()
    if os.path.exists(state): sent={l.strip() for l in open(state) if l.strip()}
    recs=[r for r in recs if keyf(r) not in sent]
    if a.limit: recs=recs[:a.limit]
    print(f'{a.what}: {len(recs)} to send ({len(sent)} already sent, skipped)')
    if a.dry_run:
        print(json.dumps(recs[0],indent=1)[:1200] if recs else 'nothing to send'); return

    url=HOOKS[a.what]; codes={}; fails=[]; lock=threading.Lock(); n=[0]
    sf=open(state,'a')
    def go(rec):
        code,body=post(url,rec,a.rps)
        with lock:
            codes[code]=codes.get(code,0)+1; n[0]+=1
            if code in (200,201,202):
                sf.write(str(keyf(rec))+'\n')
                if n[0]%100==0: sf.flush(); print(f'  {n[0]}/{len(recs)}',flush=True)
            else:
                fails.append({'key':keyf(rec),'code':code,'body':body})
    with cf.ThreadPoolExecutor(a.workers) as ex: list(ex.map(go,recs))
    sf.close()
    print('response codes:',codes)
    if fails:
        fp=os.path.join(HERE,'work',f'clay-failed-{a.what}.json')
        json.dump(fails,open(fp,'w'),indent=1)
        print(f'{len(fails)} failed -> {fp}')
        print('sample:',json.dumps(fails[0])[:250])

if __name__=='__main__': main()
