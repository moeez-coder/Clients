"""Doc 2 sizing step 2: fit samples (Blitz). Mid-band company samples + people title samples per persona.
Writes 2026-11-18-doc-2-blitz-samples.json."""
import json
from doc2_common import *
out, used = {}, 0
def get(key, path, body):
    global used
    r = call(path, body); used += r.get("fair_usage", {}).get("records_used", 0)
    out[key] = {"body": body, "results": r.get("results", []), "error": r.get("_body")}
    print(key, len(r.get("results", [])), r.get("_body") or "")
get("pharma_201_500", "/v2/search/companies", {"company": pharma_co(True, True, ["201-500"]), "max_results": 20})
get("pharma_501_5000", "/v2/search/companies", {"company": pharma_co(True, True, ["501-1000", "1001-5000"]), "max_results": 10})
get("device_51_200", "/v2/search/companies", {"company": device_co(True, ["51-200"]), "max_results": 10})
get("device_201_1000", "/v2/search/companies", {"company": device_co(True, ["201-500", "501-1000"]), "max_results": 10})
for camp, cells in PHARMA_CELLS.items():
    inc, exc = cells["decision_makers"]; b = people_body(pharma_co(True, True), inc, exc, LV["decision_makers"]); b["max_results"] = 4
    get(f"people/{camp}/decision_makers", "/v2/search/people", b)
    inc, exc = cells["advocates"]; b = people_body(pharma_co(True, True), inc, exc, LV["advocates"]); b["max_results"] = 2
    get(f"people/{camp}/advocates", "/v2/search/people", b)
for lv, (inc, exc) in DEVICE_CELLS.items():
    b = people_body(device_co(True, ["51-200", "201-500", "501-1000"]), inc, exc, LV[lv]); b["max_results"] = 4
    get(f"people/c7_device/{lv}", "/v2/search/people", b)
out["records_used"] = used; print("used", used)
json.dump(out, open("2026-11-18-doc-2-blitz-samples.json", "w"), indent=1)
