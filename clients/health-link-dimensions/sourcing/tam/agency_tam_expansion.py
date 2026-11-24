import json
from persona_counts import call, KW_PHARMA, KW_EXCL, NAME_EXCL
AD=["Advertising Services","Marketing and Advertising","Marketing Services"]
PR=["Public Relations and Communications Services","Public Relations and Communications"]
MR=["Market Research"]
HEALTH_IND=["Hospitals and Health Care","Hospital and Health Care","Pharmaceutical Manufacturing","Pharmaceuticals","Biotechnology Research","Health and Human Services","Medical Equipment Manufacturing"]
DATA_IND=["Data Infrastructure and Analytics","Business Consulting and Services","IT Services and IT Consulting","Information Services","Online Audio and Video Media","Online Media","Media Production"]
KW_BROAD=KW_PHARMA+["healthcare marketing","healthcare advertising","health communications","healthcare media","life sciences","medical marketing","HCP engagement","omnichannel healthcare","healthcare agency"]
KW_AGENCY=["healthcare marketing agency","healthcare advertising agency","pharmaceutical marketing agency","pharma agency","health agency","HCP marketing","healthcare media agency","healthcare communications agency","medical communications agency","life sciences agency","omnichannel agency","media agency"]
S51=["51-200","201-500","501-1000","1001-5000"]; S11=["11-50"]+S51; S_ALL=S11+["5001-10000","10001+"]
def c(ind,kw,sizes,kwex=KW_EXCL): return {"company":{"industry":{"include":ind},"employee_range":sizes,"hq":{"country_code":["US"]},"keywords":{"include":kw,"exclude":kwex},"name":{"exclude":NAME_EXCL}},"max_results":1}
V={
 "0_current_core":c(AD,KW_PHARMA,S51),
 "1_add_11_50":c(AD,KW_PHARMA,["11-50"]),
 "2_add_5001plus":c(AD,KW_PHARMA,["5001-10000","10001+"]),
 "3_broad_kw_51plus_ad":c(AD,KW_BROAD,S51),
 "4_PR_industry_pharma_kw_51plus":c(PR,KW_PHARMA,S51),
 "5_market_research_pharma_kw_51plus":c(MR,KW_PHARMA,S51),
 "6_health_industries_agency_kw_11plus":c(HEALTH_IND,KW_AGENCY,S11),
 "7_data_media_industries_agency_kw_11plus":c(DATA_IND,KW_AGENCY+["HCP","pharma marketing","pharmaceutical marketing"],S11),
}
def main():
  out={};used=0
  for k,b in V.items():
    r=call("/v2/search/companies",b); used+=r["fair_usage"]["records_used"]; out[k]={"body":b,"total_results":r["total_results"]}; print(k,r["total_results"])
  out["records_used"]=used; json.dump(out,open("expand.json","w"),indent=1); print("used",used)
if __name__=="__main__": main()
