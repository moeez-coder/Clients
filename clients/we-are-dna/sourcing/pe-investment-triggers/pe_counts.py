"""Campaign 6 (Fresh Investment, PE-backed growth) count read, 2026-11-16.
Blitz POST /v2/search/companies, max_results=1, reading total_results. UK HQ, 51+ employees,
last_funding_type = Private equity, last_funding_year >= YEAR, industries = the five doc-1 sectors
(exact Blitz enum labels, same lists as ../tam/tam_counts.py). Usage: python3 pe_counts.py
"""
import json, os, sys, urllib.request, urllib.error, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tam"))
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
IND = {
 "1-health-care-vet-dental": ["Hospitals and Health Care","Hospital and Health Care","Hospitals","Home Health Care Services","Nursing Homes and Residential Care Facilities","Mental Health Care","Medical Practices","Medical Practice","Outpatient Care Centers","Veterinary","Veterinary Services","Ambulance Services","Individual and Family Services"],
 "2-retail-hospitality": ["Retail","Retail Apparel and Fashion","Retail Groceries","Retail Health and Personal Care Products","Retail Luxury Goods and Jewelry","Retail Furniture and Home Furnishings","Online and Mail Order Retail","Apparel and Fashion","Hospitality","Restaurants","Hotels and Motels","Food and Beverage Services","Leisure; Travel and Tourism"],
 "3-manufacturing-engineering": ["Manufacturing","Industrial Machinery Manufacturing","Machinery Manufacturing","Automotive","Motor Vehicle Manufacturing","Motor Vehicle Parts Manufacturing","Defense and Space Manufacturing","Defense and Space","Aviation and Aerospace Component Manufacturing","Engineering Services","Mechanical Or Industrial Engineering","Food and Beverage Manufacturing","Food Production","Meat Products Manufacturing","Electrical Equipment Manufacturing","Chemical Manufacturing"],
 "4-law-accounting": ["Law Practice","Legal Services","Accounting"],
 "5-financial-services": ["Financial Services","Banking","Insurance","Insurance Carriers","Investment Management","Credit Intermediation","Capital Markets"],
}
SIZES = ["51-200","201-500","501-1000","1001-5000","5001-10000","10001+"]
def post(path, body):
    for a in range(6):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai"+path, json.dumps(body).encode(), H, method="POST")
            return json.load(urllib.request.urlopen(r, timeout=90))
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503,504): time.sleep(2**a); continue
            return {"_error": e.code, "_body": e.read()[:400].decode(errors="replace")}
out = {}
for seg, ind in IND.items():
    for yr in (2026, 2025):
        body = {"company": {"industry": {"include": ind}, "employee_range": SIZES, "hq": {"country_code": ["GB"]},
                            "last_funding_type": {"include": ["Private equity"]}, "last_funding_year": {"min": yr}}, "max_results": 1}
        r = post("/v2/search/companies", body)
        out[f"{seg}|{yr}+"] = {"total": r.get("total_results", r.get("_error")), "body": body,
                               "sample": [{k: x.get(k) for k in ("name","linkedin_url","last_funding_date","last_funding_type","employee_count")} for x in r.get("results", [])],
                               "records_used": (r.get("fair_usage") or {}).get("records_used"), "err": r.get("_body")}
        print(seg, yr, out[f"{seg}|{yr}+"]["total"], out[f"{seg}|{yr}+"]["sample"], out[f"{seg}|{yr}+"]["err"], flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "2026-11-16-pe-counts.json"), "w"), indent=1)
