"""DiscoLike GET /v1/discover (paid, approved by Moe 2026-11-24, cap $2). Free GET /v1/count first.
  mfg : country=US, state=NC,SC, employee_range=201,1000, category=MANUFACTURING  (count 204)
  fls : country=US, 38 ET/CT states, employee_range=201,1000, phrase_match fire sprinkler|fire alarm|fire suppression (count 268)
Output: raw/discolike.json (+ month_to_date_spend before/after from GET /v1/usage)."""
import json, os, urllib.parse as up
from common import *
K = {"x-discolike-key": os.environ["DISCOLIKE_API_KEY"]}
ABBR = "AL AR CT DE FL GA IL IN IA KS KY LA ME MD MA MI MN MS MO NE NH NJ NY NC ND OH OK PA RI SC SD TN TX VT VA WV WI DC".split()
spend = lambda: http("GET", "https://api.discolike.com/v1/usage", K)[1]["month_to_date_spend"]
Q = {"mfg": [("country", "US"), ("state", "NC"), ("state", "SC"), ("employee_range", "201,1000"), ("category", "MANUFACTURING")],
     "fls": [("country", "US"), ("employee_range", "201,1000")] + [("state", s) for s in ABBR]
            + [("phrase_match", p) for p in ["fire sprinkler", "fire alarm", "fire suppression"]]}
s0, out = spend(), {}
for k, q in Q.items():
    n = http("GET", "https://api.discolike.com/v1/count?" + up.urlencode(q), K)[1]["count"]
    st, r = http("GET", "https://api.discolike.com/v1/discover?" + up.urlencode(q + [("max_records", str(n))]), K, timeout=300)
    rows = r if isinstance(r, list) else (r.get("records") or r.get("results") or r.get("data") or r)
    print(k, "count", n, "status", st, "rows", len(rows) if isinstance(rows, list) else str(rows)[:300], flush=True)
    out[k] = {"params": q, "count": n, "results": rows}
out["spend_usd"] = round(spend() - s0, 4)
print("spend", out["spend_usd"])
json.dump(out, open(os.path.join(HERE, "raw", "discolike.json"), "w"))
