"""Step 3: find the executives above each open role.  Usage: python3 pull_people.py
Blitz API POST /v2/search/waterfall-icp-keyword, one call per kept company (raw/companies.json):
tier 1 = executive over the role family, tier 2 = CEO/President/Owner, tier 3 = CHRO/VP HR. US only.
Manager and Director titles excluded (client instruction). LinkedIn URLs only, no email enrichment.
Output raw/people.jsonl (resumable by company url) + raw/usage.json."""
import json, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tam"))
from tam_counts import post
from spec import TIER1, TIER2, TIER3, PEOPLE_EXCLUDE, PER_COMPANY
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw"); out = os.path.join(RAW, "people.jsonl")
comps = json.load(open(os.path.join(RAW, "companies.json")))
done = {json.loads(l)["company_linkedin_url"] for l in open(out)} if os.path.exists(out) else set()
todo = [c for c in comps if c["company_linkedin_url"] not in done]

def one(c):
    fam = c["role_family"]
    casc = [{"include_title": t, "exclude_title": PEOPLE_EXCLUDE, "location": {"country_code": ["US"]},
             "include_headline_search": False} for t in (TIER1[fam], TIER2, TIER3)]
    r = post("/v2/search/waterfall-icp-keyword", {"company_linkedin_url": c["company_linkedin_url"], "cascade": casc,
                                                  "max_results": PER_COMPANY.get(fam, PER_COMPANY["mfg"])})
    return {"company_linkedin_url": c["company_linkedin_url"], "results": r.get("results") or [], "error": r.get("_error"),
            "used": (r.get("fair_usage") or {}).get("records_used", 0)}

used = 0
with ThreadPoolExecutor(12) as ex, open(out, "a") as f:
    for i, r in enumerate(ex.map(one, todo)):
        used += r.pop("used"); f.write(json.dumps(r) + "\n")
        if i % 200 == 0: f.flush(); print(i, flush=True)
u = json.load(open(os.path.join(RAW, "usage.json"))); u["/v2/search/waterfall-icp-keyword"] = u.get("/v2/search/waterfall-icp-keyword", 0) + used
json.dump(u, open(os.path.join(RAW, "usage.json"), "w")); print("done", len(todo), u)
