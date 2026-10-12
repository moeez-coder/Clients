import json,re,collections,csv,sys
sys.path.insert(0,'.')
d=json.load(open('personalize_raw.json'))
TITLE={'M&A':r"(acquir|acquisition|acquires|merger|merges|to combine|definitive agreement|business combination|completes (the )?purchase)",
 'Regulatory':r"(consent order|enforcement action|cease and desist|formal agreement|civil money penalt|written agreement|regulatory agreement)",
 'AI':r"(\bai\b|artificial intelligence|generative|agentic)"}
BAD=r"(job description|careers?\b|/jobs?/|naming rights|rebrand|quarter|earnings|financial results|dividend|reposted|linkedin\.com|facebook\.com|instagram\.com|ayondo|sponsorship|scholarship|training|webinar|podcast)"
def tok(n):
    t=re.sub(r'[^a-z0-9 ]','',n.lower()); t=re.sub(r'\b(inc|corp|corporation|llc|co|company|bank|financial|group|holdings|the|national|savings|federal|credit|union)\b','',t).split()
    return ' '.join(t[:2]) if t else ''
out=[]
for x in d:
    p=x['person'];n=p['company_name'];k=tok(n)
    keep=[]
    if n.strip() not in('-','') and k:
        for st,title,url,date,hl in x['res']['news']:
            if re.search(BAD,title+' '+url,re.I): continue
            if k not in title.lower() and k.replace(' ','') not in url.lower().replace('-',''): continue
            if not re.search(TITLE[st],title,re.I): continue
            keep.append((st,title,url,date,hl))
    # dedupe by type: newest
    best={}
    for it in sorted(keep,key=lambda i:i[3],reverse=True):
        best.setdefault(it[0],it)
    out.append((p,x['res']['jobs'],best))
print('companies',len(out),'with job',sum(1 for o in out if o[1]),'with news',sum(1 for o in out if o[2]),'any',sum(1 for o in out if o[1] or o[2]))
print(collections.Counter(s for o in out for s in o[2]))
for o in out[:200:9]:
    p,j,b=o;print('\n##',p['company_name'],'|',p['persona_group'],'|',p['job_title'][:35])
    for s,it in b.items(): print('  NEWS',s,it[3],it[1][:80])
    for u,(t,dt) in j[:2]: print('  JOB',dt,t)
json.dump([(o[0],o[1],o[2]) for o in out],open('refined.json','w'))
