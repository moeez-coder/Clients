"""How much does loosening the F&LS size band add? (Moe 2026-11-24: "We can always loosen the icp filter if we
find close enough companies.") Counts only: Blitz POST /v2/search/companies max_results=1 (1 plan record each),
DiscoLike GET /v1/count (free). Plus the size spread of F&LS-type companies already resolved from the
list sources (2026-11-24-domain-resolution.csv). Output: 2026-11-24-loosen-counts.json"""
import csv, json, os, urllib.parse as up, collections as C
from common import *
BK = {"x-api-key": os.environ["BLITZ_API_KEY"]}; DK = {"x-discolike-key": os.environ["DISCOLIKE_API_KEY"]}
ABBR = "AL AR CT DE FL GA IL IN IA KS KY LA ME MD MA MI MN MS MO NE NH NJ NY NC ND OH OK PA RI SC SD TN TX VT VA WV WI DC".split()
out = {}
for label, sizes in (("201-1000", ["201-500", "501-1000"]), ("51-200", ["51-200"]), ("11-50", ["11-50"]), ("1001-5000", ["1001-5000"])):
    st, r = http("POST", "https://api.blitz-api.ai/v2/search/companies", BK, {"company": {"industry": {"include": FLS_IND},
        "keywords": {"include": FLS_KW}, "employee_range": sizes, "hq": {"country_code": ["US"], "state": {"exclude": NON_ET_CT}}}, "max_results": 1})
    out[f"blitz fls-kw {label}"] = r.get("total_results")
    st, r = http("POST", "https://api.blitz-api.ai/v2/search/companies", BK, {"company": {"industry": {"include": ["Fire Protection"]},
        "employee_range": sizes, "hq": {"country_code": ["US"], "state": {"exclude": NON_ET_CT}}}, "max_results": 1})
    out[f"blitz fire-protection-label {label}"] = r.get("total_results")
for label, rng in (("201-1000", "201,1000"), ("51-200", "51,200"), ("11-50", "11,50"), ("1001-5000", "1001,5000")):
    q = [("country", "US"), ("employee_range", rng)] + [("state", s) for s in ABBR] + [("phrase_match", p) for p in ["fire sprinkler", "fire alarm", "fire suppression"]]
    out[f"discolike fls-phrases {label}"] = http("GET", "https://api.discolike.com/v1/count?" + up.urlencode(q), DK)[1].get("count")
# size spread of resolved F&LS list companies (Exa / NFSA / Google Maps), any size, ET/CT HQ
spread = C.Counter()
for r in csv.DictReader(open(os.path.join(HERE, "2026-11-24-domain-resolution.csv"))):
    if r["found"] == "yes" and ":fls" in r["listed_by"] and r["hq_state"] in ET_CT_STATES:
        spread[r["size"]] += 1
out["resolved F&LS list companies in ET/CT by size"] = dict(spread)
json.dump(out, open(os.path.join(HERE, "2026-11-24-loosen-counts.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
