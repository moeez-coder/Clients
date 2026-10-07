import json,os,concurrent.futures as cf
from people_pull import call,EXC
todo=json.load(open('nolead_companies.json'))
def run(item):
    n,urls=item; fn=f'people3/p{n:04d}.jsonl'
    if os.path.exists(fn+'.done'): return n,-1
    cnt=0; cur=None
    with open(fn,'w') as f:
        for page in range(6):
            body={"company":{"linkedin_url":urls},"people":{"job_function":["Advertising & Marketing"],"job_level":["C-Team","VP","Director","Manager"],"job_title":{"include":[],"exclude":EXC}},"max_results":50}
            if cur: body['cursor']=cur
            d=call(body)
            if d.get('error'): f.write(json.dumps({'_error':d,'urls':urls})+'\n'); break
            for r in d['results']:
                f.write(json.dumps({'person':{k:r.get(k) for k in ('first_name','last_name','full_name','headline','linkedin_url','location','connections_count')},'jobs':[e for e in (r.get('experiences') or []) if e.get('job_is_current')][:4]})+'\n'); cnt+=1
            cur=d.get('cursor')
            if not cur: break
    open(fn+'.done','w').write(str(cnt)); return n,cnt
items=[(i,todo[i*5:(i+1)*5]) for i in range((len(todo)+4)//5)]; tot=0
with cf.ThreadPoolExecutor(8) as ex:
    for n,c in ex.map(run,items): tot+=max(c,0)
print('DONE',tot,'rows from',len(todo),'companies')
