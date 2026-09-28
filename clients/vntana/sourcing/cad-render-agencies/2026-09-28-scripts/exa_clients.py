import json,os,time,urllib.request,concurrent.futures as cf
K=os.environ['EXA_API_KEY']
def exa(body,path='search'):
    for a in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request('https://api.exa.ai/'+path,data=json.dumps(body).encode(),headers={'x-api-key':K,'Content-Type':'application/json'}),timeout=90))
        except urllib.error.HTTPError as e:
            if e.code==429 or e.code>=500: time.sleep(2**a); continue
            return {'error':e.code,'msg':e.read()[:200].decode('utf8','ignore')}
        except Exception as e: time.sleep(2**a)
    return {'error':'retries'}
if __name__=='__main__':
    d=json.load(open('scored.json'))
    def emp(r):
        try: return int(r['employees'])
        except:
            try: return int((r.get('size_range') or '0').split('-')[0].replace('+',''))
            except: return 0
    big=[r for r in d if emp(r)>=11 and r['tier'] in 'AB' and r['domain']]
    def job(r):
        res=exa({"query":"our clients, brands we work with, case studies and portfolio projects","includeDomains":[r['domain']],"numResults":6,"contents":{"highlights":{"query":"names of client companies and brands this studio has worked for","numSentences":3,"highlightsPerUrl":2}}})
        return r['company_linkedin_url'],res
    out={}
    with cf.ThreadPoolExecutor(8) as ex:
        for i,(k,res) in enumerate(ex.map(job,big)):
            out[k]=res
            if i%100==0: print(i,flush=True)
    json.dump(out,open('exa_clients.json','w'))
    print('done',len(out),sum(1 for v in out.values() if v.get('results')),'cost',round(sum((v.get('costDollars') or {}).get('total',0) for v in out.values()),2))
