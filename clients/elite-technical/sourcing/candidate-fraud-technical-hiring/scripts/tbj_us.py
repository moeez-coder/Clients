import json,sys,collections
import tbj
TECH=tbj.TECH+["Engineer","Developer","Data Scientist","Architect","Machine Learning","Programmer","QA Automation","IT Manager","Infrastructure","Database Administrator","Platform Engineer","Embedded"]
def body(cur):
  b=tbj.body(cur,50); b['job']['title']['include']=TECH; b['job']['date_posted']={'last_days':90}
  b['company']['hq']={"country_code":{"include":["US"]}}; return b
out={};cur=None;pages=0
while True:
  d=tbj.call(body(cur)); pages+=1
  if 'error' in d: print('ERR',d,file=sys.stderr); break
  for r in d.get('results',[]): out[r['company']['linkedin_url']]=r
  cur=d.get('cursor')
  if not cur or pages>1200: break
json.dump(out,open('c9_tam_jobs_us.json','w'))
print('companies',len(out),'pages',pages,collections.Counter(r['company'].get('revenue_range') for r in out.values()))
