import json,os,sys,urllib.request
KEY=os.environ['BLITZ_API_KEY']
STATES=['[District of Columbia]','[Maryland]','[Virginia]','[New York]','[New Jersey]','[Pennsylvania]','[Massachusetts]','[Connecticut]','[Delaware]','[North Carolina]','[Georgia]','[Florida]','[Ohio]','[Michigan]','[Illinois]','[Indiana]','[Wisconsin]','[Minnesota]','[Missouri]','[South Carolina]','[Rhode Island]','[New Hampshire]','[Maine]','[Vermont]','[Iowa]','[Kansas]','[Nebraska]']
TECH=["Software Engineer","Software Developer","DevOps","Data Engineer","Cloud Engineer","Cybersecurity","Security Engineer","Systems Engineer","Network Engineer","Site Reliability","Full Stack","Java Developer",".NET Developer","Solutions Architect","Systems Administrator"]
def body(cursor=None,n=50):
  return {"job":{"title":{"include":TECH},"work_arrangement":{"include":["Hybrid","Remote OK","Remote Solely"]},"date_posted":{"last_days":30}},
 "company":{"is_agency":False,"employee_count":{"min":501,"max":10000},"hq":{"country_code":{"include":["US"]},"state":{"include":STATES}}},"max_results":n,"cursor":cursor}
def call(b):
  req=urllib.request.Request('https://api.blitz-api.ai/v2/company/tam-by-jobs',json.dumps(b).encode(),{'Content-Type':'application/json','x-api-key':KEY})
  try: return json.load(urllib.request.urlopen(req,timeout=120))
  except urllib.error.HTTPError as e: return {'error':e.code,'msg':e.read().decode()[:800]}
if __name__=='__main__':
  d=call(body(n=5))
  print({k:v for k,v in d.items() if k!='results'})
  for r in d.get('results',[]): c=r.get('company') or {}; print(r.get('matched_jobs'),c.get('name'),c.get('revenue_range'),(c.get('hq') or {}).get('state'),c.get('employees_on_linkedin') or c.get('employee_count'))
  if d.get('results'): print(list(d['results'][0].keys()), list((d['results'][0].get('company') or {}).keys()))
