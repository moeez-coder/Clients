import json,re
A=json.load(open('accounts.json'));R1={o['i']:o for o in json.load(open('resolved.json'))};R2={o['i']:o['pages'] for o in json.load(open('resolved2.json'))}
EXTRA={'kg','ab','as','oy','bv','nv','ag','sa','spa','llc','inc','ltd','gmbh','co','corp','corporation','group','global','usa','us','uk','america','north','international','europe','holding','holdings','the','plc','sas','srl','industries','company'}
def toks(s): return set(re.findall(r'[a-z0-9]{2,}',(s or '').lower()))
def root(d):
    d=(d or '').lower().replace('www.','');p=d.split('.');return '.'.join(p[-2:]) if len(p)>1 else d
out={};
for i,a in enumerate(A):
    allowed=toks(a['client_name'])|toks(a['likely_company'])|EXTRA
    pages=[];seen=set()
    o=R1[i];r1root=root(o['domain']) if o['domain'] else None
    if o['li'] and 'company/1337' not in o['li'] and toks(o['li_name'])<=allowed:
        pages.append({'li':o['li'],'name':o['li_name'],'emp':10**6,'domain':o['domain']});seen.add(o['li'].lower())
    roots={r1root} if r1root and pages else set()
    for p in R2[i]:
        if p['li'].lower() in seen: continue
        if toks(p['name'])<=allowed or (root(p.get('domain')) in roots and root(p.get('domain'))):
            pages.append(p);seen.add(p['li'].lower())
    pages=sorted(pages,key=lambda p:-p['emp'])[:3]
    out[i]=pages
json.dump(out,open('pages.json','w'))
print('accounts with pages',sum(1 for v in out.values() if v),'total pages',sum(len(v) for v in out.values()))
for i in (0,5,9,12,40):
    if i in out:print(A[i]['client_name'],[(p['name'],p['emp'] if p['emp']<10**6 else 'r1') for p in out[i]])
print('none:',[A[i]['client_name'] for i,v in out.items() if not v])
