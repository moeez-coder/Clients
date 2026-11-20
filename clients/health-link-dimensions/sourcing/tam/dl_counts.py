import json,time
from dl import get
HEALTH_PH=["pharmaceutical marketing","pharma marketing","healthcare marketing","healthcare communications","health communications","medical communications","life sciences marketing","HCP marketing","healthcare professionals","pharmaceutical brands","biopharma","healthcare advertising","pharma brands","life sciences"]
MEDIA_PH=["programmatic","media planning","media buying","omnichannel","audience targeting","data and analytics"]
def P(**kw):
    out=[]
    for k,v in kw.items():
        for x in (v if isinstance(v,list) else [v]): out.append((k,x))
    return out
V={
 "a_adv_US":P(category="ADVERTISING_AND_MARKETING",country="US"),
 "b_adv_US_health_phrases":P(category="ADVERTISING_AND_MARKETING",country="US",phrase_match=HEALTH_PH),
 "c_adv_US_health_phrases_11plus":P(category="ADVERTISING_AND_MARKETING",country="US",phrase_match=HEALTH_PH,employee_range="11,"),
 "d_adv_US_health_phrases_51plus":P(category="ADVERTISING_AND_MARKETING",country="US",phrase_match=HEALTH_PH,employee_range="51,"),
 "e_adv_US_health_AND_media_11plus":P(category="ADVERTISING_AND_MARKETING",country="US",phrase_match=HEALTH_PH+["+"+"|".join(MEDIA_PH)],employee_range="11,"),
 "f_adv_US_pharma_strict_11plus":P(category="ADVERTISING_AND_MARKETING",country="US",phrase_match=["+pharmaceutical|pharma|biopharma|life sciences|HCP|healthcare professionals"],employee_range="11,"),
 "g_adv_or_pharma_US_strict_agency_11plus":P(category=["ADVERTISING_AND_MARKETING","PHARMACEUTICALS","HEALTHCARE","MEDIA"],country="US",phrase_match=["+pharmaceutical marketing|pharma marketing|healthcare marketing agency|medical communications|HCP marketing|healthcare communications agency|health communications agency|life sciences marketing"],employee_range="11,"),
}
out={}
for k,p in V.items():
    r=get("/count",p); time.sleep(2.5)
    out[k]={"params":p,"response":r}; print(k,json.dumps(r)[:200])
json.dump(out,open("dl_counts.json","w"),indent=1)
