import json,os,sys,time,urllib.request,urllib.error
K=os.environ['BLITZ_API_KEY']
def call(body):
    rq=urllib.request.Request('https://api.blitz-api.ai/v2/company/tam-by-jobs',json.dumps(body).encode(),{'x-api-key':K,'content-type':'application/json','User-Agent':'curl/8.5.0'})
    for i in range(5):
        try: return json.load(urllib.request.urlopen(rq,timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503): time.sleep(2+i*3); continue
            return {'http':e.code,'body':e.read().decode()[:1500]}
        except Exception: time.sleep(2+i*3)
    return {'http':0,'body':'network failure after retries'}
if __name__=='__main__':
    for ind in (["Banking"],["Financial Services"],["Credit Intermediation"],["Insurance"]):
        r=call({"job":{"title":{"include":["BSA","AML","KYC","OFAC"]},"date_posted":{"last_days":90},"min_per_company":2},"company":{"industry":{"include":ind},"size":{"include":["201-500","501-1000","1001-5000"]}},"max_results":5})
        print(ind,json.dumps(r)[:900])
