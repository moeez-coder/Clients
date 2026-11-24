import json,random,re
from persona_counts import call, company
from expand import c, AD, KW_BROAD, S51
dl=json.load(open("dl_discover.json"))["response"]
cand=[x for x in dl[:300] if x.get("employees") in ("51-200","201-500","501-1000","1001-5000") and "eversana" not in x["domain"]]
random.seed(11); smp=random.sample(cand,30)
def nm(x): return re.sub(r",? (LLC|Inc\.?|Limited|Ltd\.?|Corp\.?)$","",x["name"]).strip()
rows=[];used=0
for x in smp:
    n=nm(x)
    b={"company":dict(company(),name={"include":[n],"exclude":company()["name"]["exclude"]}),"max_results":1}
    r=call("/v2/search/companies",b); used+=r["fair_usage"]["records_used"]
    core=r.get("total_results",0)>0
    exp=None; anyb=None; ind=None
    if not core:
        b2=c(AD,KW_BROAD,S51+["11-50"]); b2["company"]["name"]={"include":[n]}
        r2=call("/v2/search/companies",b2); used+=r2["fair_usage"]["records_used"]; exp=r2.get("total_results",0)>0
        if not exp:
            b3={"company":{"name":{"include":[n]},"hq":{"country_code":["US"]}},"max_results":1}
            r3=call("/v2/search/companies",b3); used+=r3["fair_usage"]["records_used"]; anyb=r3.get("total_results",0)>0
            if anyb: ind=(r3["results"][0].get("industry"),r3["results"][0].get("employees_on_linkedin"),r3["results"][0].get("name"))
    rows.append({"domain":x["domain"],"name":n,"dl_similarity":x["similarity"],"dl_employees":x["employees"],"in_blitz_core":core,"in_blitz_expanded_ad":exp,"in_blitz_any_us":anyb,"blitz_industry_if_outside":ind})
    print(x["domain"],n,"| core",core,"| exp",exp,"| any",anyb,ind)
print("used",used)
json.dump({"rows":rows,"records_used":used},open("capture.json","w"),indent=1)
