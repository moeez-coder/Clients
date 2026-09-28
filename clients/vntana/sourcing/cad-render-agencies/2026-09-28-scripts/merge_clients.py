import csv,glob,json,re,collections
S={r['company_linkedin_url']:r for r in json.load(open('scored.json'))}
def dom(u): return re.sub(r'^www\.','',re.sub(r'^https?://','',(u or '').lower()).split('/')[0])
SOC=re.compile(r'(facebook|instagram|linktr\.ee|behance|linkedin|youtube|vimeo|twitter|x\.com|dribbble|pinterest|tiktok|artstation|medium\.com)')
rows=[];bad=0;badfile=collections.Counter()
for f in sorted(glob.glob('batches/out_b*.csv')):
    for r in csv.DictReader(open(f,newline='',encoding='utf8',errors='ignore')):
        a=S.get((r.get('agency_linkedin_url') or '').strip())
        if not a or not (r.get('client_name') or '').strip(): bad+=1; continue
        ad=a['domain']; ed=dom(r.get('evidence_url'))
        own = r.get('evidence_type')=='description' or (ed and ad and (ed==ad or ed.endswith('.'+ad) or ad.endswith('.'+ed)))
        if SOC.search(ad or ''): own = r.get('evidence_type')=='description'
        if not own: badfile[f]+=1; continue
        rows.append({**r,'agency_domain':ad,'agency_tier':a['tier'],'agency_country':a['hq_country']})
print('kept',len(rows),'dropped malformed',bad,'dropped off-domain',sum(badfile.values()))
json.dump(rows,open('client_rows.json','w'))
c=collections.Counter(r['client_name'].strip() for r in rows)
print(len(c),'distinct client names'); print(c.most_common(40))
