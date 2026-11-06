import json,re,sys
S=sys.argv[1]
pages=json.load(open(S+'/dod_pages.json'))
ST={'District of Columbia':'DC','Maryland':'MD','Virginia':'VA'}
for s in 'Maine NewHampshire Vermont Massachusetts RhodeIsland Connecticut NewYork NewJersey Pennsylvania Delaware NorthCarolina SouthCarolina Georgia Florida'.split(): ST[re.sub(r'(?<!^)([A-Z])',r' \1',s)]='East Coast'
for s in 'Ohio Michigan Indiana Illinois Wisconsin Minnesota Iowa Missouri NorthDakota SouthDakota Nebraska Kansas'.split(): ST[re.sub(r'(?<!^)([A-Z])',r' \1',s)]='Midwest'
TIER=lambda st: 'DC Metro' if st in ('District of Columbia','Maryland','Virginia') else ST.get(st)
STATES='|'.join(sorted(map(re.escape,list(ST)+['Texas','California','Washington','Oregon','Colorado','Alabama','Arizona','Utah','Tennessee','Kentucky','Louisiana','Mississippi','Oklahoma','New Mexico','Nevada','Hawaii','Alaska','Arkansas','West Virginia','Idaho','Montana','Wyoming']),key=len,reverse=True))
ONE=re.compile(r'^(?P<co>[^\n]+?), (?P<city>[A-Z][A-Za-z .\'-]+?), (?P<st>'+STATES+r'),? (?:\(\w+\),? )?(?:was|has been|is being|is|were|have been|have each been|has each been) awarded (?P<rest>.*)$')
BAD=re.compile(r'\b(modification|option|exercis|extend|extension|bridge|undefinitized|definitiz)',re.I)
out=[]
for dte,p in sorted(pages.items()):
  branch=None
  for para in p['text'].split('\n'):
    para=para.strip()
    if re.fullmatch(r'[A-Z][A-Z ,&\-]+',para): branch=para; continue
    m=ONE.match(para)
    if not m: continue
    first=m.group('rest').split('. ')[0]
    if BAD.search(first): continue
    amt=re.search(r'\$([\d,]+)',m.group('rest'))
    out.append(dict(announce_date=dte,award_date=(re.search(r'\(Awarded ([A-Z][a-z]+\.? \d+, 2026)\)',para) or [None,None])[1] or dte,company=m.group('co').strip(),city=m.group('city'),state=m.group('st'),tier=TIER(m.group('st')),branch=branch,amount=int(amt.group(1).replace(',','')) if amt else None,summary=first[:300],url=p['url']))
json.dump(out,open(S+'/dod_awards.json','w'))
import collections
print(len(out),'new awards parsed');print(collections.Counter(o['tier'] for o in out))
print(len({o['company'] for o in out if o['tier']}),'distinct companies in target geos')
