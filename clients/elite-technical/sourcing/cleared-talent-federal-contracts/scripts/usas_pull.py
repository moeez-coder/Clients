import json,urllib.request,sys,time
OUT=sys.argv[1]
STATES={'DC':'DC Metro','MD':'DC Metro','VA':'DC Metro'}
for s in 'ME NH VT MA RI CT NY NJ PA DE NC SC GA FL'.split(): STATES[s]='East Coast'
for s in 'OH MI IN IL WI MN IA MO ND SD NE KS'.split(): STATES[s]='Midwest'
NAICS=['5415','5413','5417','5416','5182','3364','3345','5419']
rows=[]
for st,tier in STATES.items():
  page=1
  while True:
    body={"filters":{"award_type_codes":["A","B","C","D"],
      "time_period":[{"start_date":"2026-08-30","end_date":"2026-10-29","date_type":"new_awards_only"}],
      "recipient_locations":[{"country":"USA","state":st}],
      "naics_codes":{"require":NAICS},
      "award_amounts":[{"lower_bound":1000000}]},
      "fields":["Award ID","Recipient Name","Recipient UEI","Award Amount","Start Date","Awarding Agency","Awarding Sub Agency","Description","NAICS","recipient_id"],
      "limit":100,"page":page,"sort":"Award Amount","order":"desc"}
    req=urllib.request.Request("https://api.usaspending.gov/api/v2/search/spending_by_award/",json.dumps(body).encode(),{'Content-Type':'application/json'})
    for a in range(3):
      try: r=json.load(urllib.request.urlopen(req,timeout=60)); break
      except Exception as e: print('retry',st,e,file=sys.stderr); time.sleep(3)
    else: break
    for x in r.get('results',[]): x['_state']=st; x['_tier']=tier; rows.append(x)
    if not r.get('page_metadata',{}).get('hasNext'): break
    page+=1
  print(st,len(rows),file=sys.stderr)
json.dump(rows,open(OUT,'w'),indent=0)
print(len(rows))
