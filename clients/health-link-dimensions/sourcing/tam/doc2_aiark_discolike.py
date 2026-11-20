"""Doc 2 cross-check: AI Ark POST /v1/companies (total only, size 1) and DiscoLike GET /count (free).
Writes 2026-11-18-doc-2-aiark-discolike.json."""
import json, os, urllib.request, urllib.error
from dl import get as dlget
def aiark(path, body, method="POST"):
    r = urllib.request.Request("https://api.ai-ark.com/api/developer-portal" + path, data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={"X-TOKEN": os.environ["AIARK_API_KEY"], "Content-Type": "application/json", "User-Agent": "curl/8.5.0"})
    try: return json.load(urllib.request.urlopen(r, timeout=90))
    except urllib.error.HTTPError as e: return {"error": e.code, "body": e.read()[:400].decode(errors="ignore")}
out = {"aiark": {}, "discolike": {}}
out["aiark"]["credits_before"] = aiark("/v1/payments/credits", None, "GET")
A = {
 "baseline_no_filter": {"page": 0, "size": 1},
 "pharma_us_201plus": {"page": 0, "size": 1, "account": {"location": {"any": {"include": ["United States"]}},
     "industries": {"any": {"include": ["pharmaceutical manufacturing", "biotechnology research"]}},
     "employeeSize": {"type": "RANGE", "range": [{"start": 201, "end": 1000000}]}}},
}
for k, b in A.items():
    r = aiark("/v1/companies", b)
    out["aiark"][k] = {"body": b, "totalElements": r.get("totalElements"), "error": r.get("error"), "errbody": r.get("body"),
                       "sample": [((x.get("summary") or {}).get("name")) for x in (r.get("content") or [])[:3]]}
    print("aiark", k, out["aiark"][k]["totalElements"], out["aiark"][k]["error"] or "", out["aiark"][k]["errbody"] or "", out["aiark"][k]["sample"])
out["aiark"]["credits_after"] = aiark("/v1/payments/credits", None, "GET")
P = lambda **kw: [(k, x) for k, v in kw.items() for x in (v if isinstance(v, list) else [v])]
D = {
 "pharma_us_201plus": P(category="PHARMACEUTICALS", country="US", employee_range="201,"),
 "pharma_us_201plus_commercial": P(category="PHARMACEUTICALS", country="US", employee_range="201,", phrase_match=["+commercial|commercialization|marketed|FDA-approved|launch"]),
 "biotech_us_201plus": P(category="BIOTECHNOLOGY", country="US", employee_range="201,"),
 "biotech_us_201plus_commercial": P(category="BIOTECHNOLOGY", country="US", employee_range="201,", phrase_match=["+commercial|commercialization|marketed|FDA-approved|launch"]),
 # DiscoLike has no medical-device category (valid health categories: HEALTHCARE, PHARMACEUTICALS, BIOTECHNOLOGY)
 "healthcare_device_phrases_us_51_10000": P(category="HEALTHCARE", country="US", employee_range="51,10000", phrase_match=["+medical device|medical devices|medtech|surgical device|implant"]),
 "healthcare_device_phrases_us_10001plus": P(category="HEALTHCARE", country="US", employee_range="10001,", phrase_match=["+medical device|medical devices|medtech|surgical device|implant"]),
}
for k, p in D.items():
    r = dlget("/count", p); out["discolike"][k] = {"params": p, "response": r}; print("discolike", k, json.dumps(r)[:200])
print("credits", out["aiark"]["credits_before"], out["aiark"]["credits_after"])
json.dump(out, open("2026-11-18-doc-2-aiark-discolike.json", "w"), indent=1)
