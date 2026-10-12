import json,re,collections,sys
d=json.load(open('refined.json'))
BADJ=r"(intern\b|co-?op|sales|business development|relationship manager|loan officer|teller|branch|mortgage loan|underwriter|collector)"
WEAK_AI=r"(award|nominat|literacy|course|scam|deepfake|survey|webinar|panel|event)"
def root(dm): return re.sub(r'\.(com|org|net|bank|us|io|co)$','',dm.split('.')[0]) if dm and dm!='-' else ''
out=[]
for p,jobs,news in d:
    rt=root(p['company_domain']);n=p['company_name']
    nn={}
    for s,it in news.items():
        st,title,url,date,hl=it
        domok=rt and len(rt)>=4 and rt in re.sub(r'[^a-z0-9]','',url.lower())
        namefull=n!='-' and re.sub(r'[^a-z0-9 ]','',n.lower()) in re.sub(r'[^a-z0-9 ]','',title.lower())
        if not (domok or namefull): continue
        if s=='AI' and re.search(WEAK_AI,title,re.I): continue
        nn[s]=it
    jj=[(u,(t,dt)) for u,(t,dt) in jobs if not re.search(BADJ,t,re.I)]
    out.append((p,jj,nn))
print('with job',sum(1 for o in out if o[1]),'news',sum(1 for o in out if o[2]),'any',sum(1 for o in out if o[1] or o[2]),collections.Counter(s for o in out for s in o[2]))
for p,j,nw in out:
    if not(j or nw): continue
    print(f"{p['company_name'][:28]:28}|{p['persona_group'][:6]}|"+' ; '.join(f"{s} {it[3]} {it[1][:60]}" for s,it in nw.items())+(' || JOBS '+str(len(j))+': '+j[0][1][0][:50] if j else ''))
json.dump(out,open('refined2.json','w'))
