"""Exa POST /search (approved by Moe 2026-11-24, cap $1). Two uses:
  company discovery : category "company", F&LS queries per region + NC/SC manufacturer queries
  signal            : category "news", NC/SC new-plant / expansion announcements, last 90 days
Output: raw/exa.json with each response's costDollars."""
import json, os
from common import *
K = {"x-api-key": os.environ["EXA_API_KEY"]}
Q = [("fls", "company", q) for q in [
        "fire sprinkler contractor company headquartered in North Carolina",
        "fire protection and life safety contractor headquartered in Texas with several hundred employees",
        "fire alarm and sprinkler inspection testing maintenance company headquartered in Ohio",
        "fire protection contractor headquartered in Georgia or Florida",
        "fire sprinkler and fire alarm contractor headquartered in Illinois or Missouri"]] + \
    [("mfg", "company", q) for q in [
        "mid-sized manufacturer headquartered in South Carolina with 200 to 1000 employees",
        "family-owned manufacturing company headquartered in North Carolina with 300 employees",
        "industrial equipment manufacturer headquartered in Greenville South Carolina",
        "plastics or metal fabrication manufacturer headquartered in North Carolina"]] + \
    [("signal", "news", q) for q in [
        "manufacturer announces new plant in North Carolina creating jobs",
        "manufacturer announces expansion in South Carolina new jobs investment",
        "fire protection company acquisition announced"]]
out, cost = [], 0.0
for seg, cat, q in Q:
    body = {"query": q, "category": cat, "numResults": 25, "type": "auto"}
    if cat == "news": body["startPublishedDate"] = "2026-08-26T00:00:00.000Z"
    st, r = http("POST", "https://api.exa.ai/search", K, body)
    c = ((r.get("costDollars") or {}).get("total")) or 0
    cost += c
    out.append({"segment": seg, "category": cat, "query": q, "status": st, "cost": c,
                "results": [{k: x.get(k) for k in ("title", "url", "publishedDate", "author")} for x in (r.get("results") or [])]})
    print(seg, st, len(out[-1]["results"]), c, flush=True)
    if cost > 0.9: break
print("total cost", cost)
json.dump({"queries": out, "cost_usd": cost}, open(os.path.join(HERE, "raw", "exa.json"), "w"), indent=1)
