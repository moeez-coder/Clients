import json,sys,collections
from tbj import body,call
out={};cur=None;pages=0
while True:
  d=call(body(cur,50)); pages+=1
  if 'error' in d: print('ERR',d,file=sys.stderr); break
  for r in d.get('results',[]): out[r['company']['linkedin_url']]=r
  cur=d.get('cursor')
  if not cur or pages>400: break
json.dump(out,open('c9_tam_jobs.json','w'))
c=collections.Counter(r['company'].get('revenue_range') for r in out.values())
print('companies',len(out),'pages',pages,c)
