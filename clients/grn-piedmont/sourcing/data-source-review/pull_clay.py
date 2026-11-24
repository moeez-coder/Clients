"""Clay public REST API (api.clay.com/public/v0, query-mode search) full pull of both review slices.
Same DSL the Clay MCP `search-companies` tool takes. Industry labels = the 68 Blitz MFG labels mapped to
Clay's taxonomy (docs/clay/industry-taxonomy.txt; ';' -> ','; labels Clay lacks are listed in raw/clay.json).
Output: raw/clay.json. Clay quota: 1 result = 1 unit of the shared 1M/period quota."""
import json, os
from common import *
K = {"clay-api-key": os.environ["CLAY_API_KEY"]}
B = "https://api.clay.com/public/v0"
tax = set(open(os.path.join(HERE, "..", "..", "..", "..", "docs", "clay", "industry-taxonomy.txt")).read().splitlines())
mapped = [m.replace(";", ",") for m in MFG]
clay_mfg = [m for m in mapped if m in tax]; missing = [m for m in mapped if m not in tax]
lit = lambda v: ", ".join('"' + x + '"' for x in v)
Q = {
 "mfg": f'select from companies where industry in ({lit(clay_mfg)}) and company_size in ("201-500", "501-1,000") '
        f'and locations.any(is_headquarters = true and country_name = "United States" and state_or_province in ({lit(MFG_STATES)}))',
 "fls-kw": f'select from companies where company_size in ("201-500", "501-1,000") and '
           f'(industry = "Fire Protection" or description contains ({lit(FLS_KW)})) and '
           f'locations.any(is_headquarters = true and country_name = "United States" and state_or_province in ({lit(ET_CT_STATES)}))',
}
out = {"missing_labels": missing, "queries": Q}
for k, q in Q.items():
    st, s = http("POST", B + "/search/query-mode", K, {"query": q})
    if st != 200: print(k, st, s); out[k] = {"error": s}; continue
    sid, rows = s["search_id"], []
    for _ in range(40):
        st, r = http("POST", f"{B}/search/query-mode/{sid}/run", K, {"limit": 50})
        if st != 200: print(k, "run", st, str(r)[:300]); break
        got = r.get("results") or r.get("rows") or r.get("data") or []
        rows += got
        pass
        if len(got) < 50: break
    out[k] = {"search_id": sid, "results": rows}
    print(k, "total", len(rows))
json.dump(out, open(os.path.join(HERE, "raw", "clay.json"), "w"))
print("missing labels:", missing)
