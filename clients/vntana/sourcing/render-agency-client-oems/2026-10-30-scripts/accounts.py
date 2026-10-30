import csv,re,json
S='/tmp/claude-0/-home-user-Clients/d9029565-3ba2-56c8-9df7-0a4f13af66b9/scratchpad/wt/clients/vntana/sourcing/cad-render-agencies/2026-10-07-agency-clients-discrete-2.csv'
d=list(csv.DictReader(open(S,encoding='utf-8')))
SEG={'industrial_equipment_machinery','building_products_home','other_manufacturer'}
DNC=re.compile(r'\b(bobcat|astec|doosan|kohler|patagonia|puma|ykk|sony|accenture|xsolla|costco|millerknoll|miller knoll|herman miller|knoll|michael kors|johnson & johnson|j&j|anheuser|taco|cotton incorporated|fruit of the loom|nureg|quad)\b',re.I)
AERO=re.compile(r'(aerospace|defen[cs]e|military|aircraft|aviation|missile|space)',re.I)
out=[];drop={'dnc':0,'aero':0}
for x in d:
    if x['is_discrete_manufacturer'] not in('yes','partly') or x['pitch_priority'] not in('P1','P2') or x['vntana_segment'] not in SEG: continue
    nm=x['client_name']+' '+x['likely_company']
    if DNC.search(nm): drop['dnc']+=1;continue
    if AERO.search(x['what_they_make']): drop['aero']+=1;continue
    out.append({k:x[k] for k in('client_name','likely_company','what_they_make','vntana_segment','size_guess','company_linkedin_url','agencies','evidence_urls','evidence_quote','pitch_priority')})
print(len(out),drop)
json.dump(out,open('rs/accounts.json','w'))
