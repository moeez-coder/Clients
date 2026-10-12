import csv,json,re,collections as C,sys
csv.field_size_limit(10**9)
SRC='/root/.claude/uploads/b2fdc545-1906-55b7-b792-11d7fb45cd44/82667d49-Companies-Default-view-export-1791802094134.csv'
r=list(csv.DictReader(open(SRC,encoding='utf-8-sig')))
n=lambda u:(u or '').lower().rstrip('/').split('?')[0].replace('http://','https://').replace('://www.','://')
h={n(x['linkedin_url']):x for x in json.load(open('ops_hiring.json')) if x['linkedin_url']}
VOL=re.compile(r"\b(support|ticket|service desk|help ?desk|customer service|customer experience|contact cent|call cent|claims?|case management|cases|incident|alerts?|managed services?|managed security|security operations|SOC|monitoring|payments?|lending|loans?|insurance|servicing|billing|patient access|revenue cycle|member services?|health plan|payer|pharmacy|SaaS|platform|subscribers?|customers)\b",re.I)
STRONG=re.compile(r"\b(support|ticket|service desk|help ?desk|customer service|contact cent|call cent|claims?|case management|incident|alerts?|managed services?|managed security|security operations|monitoring|servicing|billing|revenue cycle|member services?|health plan|payer)\b",re.I)
out=[];stat=C.Counter()
for x in r:
    t=x['Type'];u=n(x['LinkedIn URL']);hj=h.get(u);mj=hj['matched_jobs'] if hj else 0
    d=x['Description'] or ''
    if t in('Government Agency','Educational','Self Employed','Self Owned'):
        q,reason,tier='Disqualified',f'Out of scope entity type ({t})','-'
    elif mj>=5:
        q,reason,tier='Disqualified',f'Adding ops headcount: {mj} open support/ops/case roles in last 90d (US)','-'
    elif STRONG.search(d) or x['Primary Industry'] in('Computer and Network Security','IT Services and IT Consulting'):
        q,reason,tier='Qualified','Ticket/case/alert-heavy business model' + (f'; {mj} open ops role(s) only' if mj else '; no open ops roles in last 90d'),'A'
    elif VOL.search(d):
        q,reason,tier='Qualified','Customer/platform-volume model (weaker signal)'+ (f'; {mj} open ops role(s) only' if mj else '; no open ops roles in last 90d'),'B'
    else:
        q,reason,tier='Disqualified','No evidence of ticket/case/alert-driven operations in description/industry','-'
    stat[(q,tier)]+=1
    out.append({'linkedin_url':x['LinkedIn URL'] or '-','name':x['Name'] or '-','domain':x['Domain'] or '-','industry':x['Primary Industry'] or '-','size':x['Size'] or '-','type':t or '-','open_ops_roles_90d':mj,'qualification':q,'confidence_tier':tier,'reason':reason})
print(stat)
w=csv.DictWriter(open('qualified.csv','w',newline=''),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
