import json,urllib.request,sys,time
OUT=sys.argv[1]
STATES={'DC':'DC Metro','MD':'DC Metro','VA':'DC Metro'}
for s in 'ME NH VT MA RI CT NY NJ PA DE NC SC GA FL'.split(): STATES[s]='East Coast'
for s in 'OH MI IN IL WI MN IA MO ND SD NE KS'.split(): STATES[s]='Midwest'
GROUPS={'contracts':["A","B","C","D"]}
rows=[]
for st,tier in STATES.items():
 for g,codes in GROUPS.items():
  page=1
  while True:
    body={"filters":{"award_type_codes":codes,
      "time_period":[{"start_date":"2025-10-30","end_date":"2026-10-29","date_type":"new_awards_only"}],
      "recipient_locations":[{"country":"USA","state":st}],
      "award_amounts":[{"lower_bound":500000}],"naics_codes":{"require":["5415","5413","5417","5416","5182","3364","3345","5419","5112","5132","3344","3342","3341","5174"]}},
      "fields":["Award ID","Recipient Name","Recipient UEI","Award Amount","Start Date","Awarding Agency","Awarding Sub Agency","Description","NAICS","recipient_id"],
      "limit":100,"page":page,"sort":"Award Amount","order":"desc"}
    req=urllib.request.Request("https://api.usaspending.gov/api/v2/search/spending_by_award/",json.dumps(body).encode(),{'Content-Type':'application/json'})
    r=None
    for a in range(4):
      try: r=json.load(urllib.request.urlopen(req,timeout=90)); break
      except Exception as e: print('retry',st,g,page,e,file=sys.stderr); time.sleep(4)
    if r is None: break
    for x in r.get('results',[]): x['_state']=st; x['_tier']=tier; x['_group']=g; rows.append(x)
    if not r.get('page_metadata',{}).get('hasNext') or page>=100: break
    page+=1
 print(st,len(rows),file=sys.stderr,flush=True)
json.dump(rows,open(OUT,'w'))
print(len(rows))
