"""GRN Piedmont general TAM, independent sizing with AI Ark (2026-11-24). Count probes only.

AI Ark POST /v1/companies costs 0.1 credit per RETURNED result, so every probe uses size=1 and
reads totalElements (0.1 credit each). The account had 64 credits; this script makes 6 probes (0.6 credits). A first run hit the rate limit (429) after 3 probes, so it was re-run with a 6 s gap; the first 3 probes were paid twice (0.3 credits).
Header X-TOKEN, User-Agent curl/8.5.0 (AI Ark 403s Python's UA).
Caveats: AI Ark `account.location` matches ANY office, not HQ, so it cannot apply the ET/CT HQ rule
exactly; the ET/CT probe includes the 37 ET/CT states + DC by name (a company with any office there matches).
Industries are AI Ark's own 919-value enum (not LinkedIn labels): the manufacturing values that map to
the Blitz TAM's 69 labels, match mode STRICT. Output: aiark_counts.json
"""
import json, os, time, urllib.request, urllib.error

URL = "https://api.ai-ark.com/api/developer-portal/v1/companies"
H = {"X-TOKEN": os.environ["AIARK_API_KEY"], "User-Agent": "curl/8.5.0", "Content-Type": "application/json"}
MFG = ['manufacturing', 'appliances, electrical, and electronics manufacturing', 'machinery manufacturing',
       'motor vehicle manufacturing', 'food and beverage manufacturing', 'industrial machinery manufacturing',
       'furniture and home furnishings manufacturing', 'textile manufacturing', 'chemical manufacturing',
       'paper and forest product manufacturing', 'plastics manufacturing', 'automation machinery manufacturing',
       'beverage manufacturing', 'glass, ceramics and concrete manufacturing', 'defense and space manufacturing',
       'packaging and containers manufacturing', 'dairy product manufacturing',
       'aviation and aerospace component manufacturing', 'railroad equipment manufacturing',
       'industrial manufacturing', 'plastics and rubber manufacturing', 'paper manufacturing', 'industrial automation']
ET_CT = ["Alabama", "Arkansas", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Illinois",
         "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
         "Minnesota", "Mississippi", "Missouri", "Nebraska", "New Hampshire", "New Jersey", "New York",
         "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Pennsylvania", "Rhode Island", "South Carolina",
         "South Dakota", "Tennessee", "Texas", "Vermont", "Virginia", "West Virginia", "Wisconsin"]
SIZE = {"type": "RANGE", "range": [{"start": 201, "end": 500}, {"start": 501, "end": 1000}]}
FLS_KW = ["fire protection", "fire sprinkler", "fire alarm", "fire suppression", "life safety"]


def body(industries=None, loc=("United States",), keywords=None):
    a = {"employeeSize": SIZE, "location": {"any": {"include": list(loc)}}}
    if industries: a["industries"] = {"any": {"include": {"mode": "STRICT", "content": industries}}}
    if keywords:
        a["keyword"] = {"any": {"include": {"sources": [{"mode": "SMART", "source": s} for s in ("NAME", "DESCRIPTION", "KEYWORD")],
                                           "content": keywords}}}
    return {"account": a, "page": 0, "size": 1}


def post(b):
  for a in range(6):
    time.sleep(6)  # plan rate limit is tight: the first run hit 429 after 3 calls
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(URL, json.dumps(b).encode(), H, method="POST"), timeout=90))
        c = (r.get("content") or [{}])[0]
        return {"totalElements": r.get("totalElements"), "sample": (c.get("summary") or {}).get("name")}
    except urllib.error.HTTPError as e:
        if e.code == 429: time.sleep(int(e.headers.get("Retry-After") or 20)); continue
        return {"_error": e.code, "_body": e.read()[:300].decode(errors="replace")}


def credits():
    time.sleep(6)
    r = urllib.request.Request("https://api.ai-ark.com/api/developer-portal/v1/payments/credits", headers=H)
    return json.load(urllib.request.urlopen(r, timeout=60)).get("total")


if __name__ == "__main__":
    out = {"_credits_before": credits()}
    probes = {
        "mfg/us-any-office": body(MFG),
        "mfg/et-ct-any-office": body(MFG, loc=ET_CT),
        "fls-keyword/us/any-industry": body(None, keywords=FLS_KW),
        "fls-keyword/et-ct/any-industry": body(None, loc=ET_CT, keywords=FLS_KW),
        "fls-keyword/et-ct/construction+facilities+security": body(["construction", "facilities services", "security and investigations"], loc=ET_CT, keywords=FLS_KW),
        "mfg/et-ct/name-or-desc 'manufactur' any industry": body(None, loc=ET_CT, keywords=["manufacturer", "manufacturing"]),
    }
    for k, b in probes.items():
        out[k] = {"body": b, **post(b)}; print(k, out[k].get("totalElements", out[k]))
    out["_credits_after"] = credits(); print(out["_credits_before"], "->", out["_credits_after"])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "aiark_counts.json"), "w"), indent=1)
