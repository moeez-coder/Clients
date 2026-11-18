import json
from dl import get
ICP=("US healthcare and pharmaceutical marketing agencies: advertising, media, omnichannel and medical communications "
     "agencies whose clients are pharma, biotech and medical device brands, that plan and buy media, run programmatic or "
     "HCP-targeted campaigns, or provide healthcare marketing data and analytics for those brands.")
NEG=("hospitals, clinics, medical practices, dental or medspa marketing, staffing and recruiting, CROs and clinical trial "
     "services, drug manufacturers, healthcare software vendors, SEO and web design shops")
p=[("icp_text",ICP),("negate_icp_text",NEG),("country","US"),("employee_range","11,"),("relevance","BALANCED"),("max_records","600")]
for d in ["cmimediagroup.com","realchemistry.com","klick.com","digitashealth.com","fingerpaint.com"]: p.append(("domain",d))
for d in ["publicishealthmedia.com","eversana.com","relevatehealth.com","healthlinkdimensions.com","throtle.io","deepintent.com","pulsepoint.com"]: p.append(("exclude_domain",d))
r=get("/discover",p)
json.dump({"params":p,"response":r},open("dl_discover.json","w"),indent=1)
recs=r if isinstance(r,list) else (r.get("records") or r.get("results") or r.get("data") or [])
print(type(r), (list(r.keys()) if isinstance(r,dict) else ""), len(recs))
if recs: print(list(recs[0].keys()))
for x in recs[:40]: print(" |",x.get("domain"),"|",x.get("name"),"|",x.get("similarity") or x.get("score"),"|",x.get("employees"),"|",str(x.get("description") or "")[:90])
