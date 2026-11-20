"""Campaign 6 signal source: Exa Websets API (direct, POST https://api.exa.ai/websets/v0/websets), 2026-11-16.
One webset per doc-1 sector: UK-headquartered companies in that sector that received private equity investment
(new PE owner, buyout, growth investment or secondary buyout) announced since 2026-08-18 (~90 days).
Each result is verified by Exa against the criteria below; an enrichment captures the deal (investor, date, source URL).
Usage: python3 exa_websets.py create   -> creates websets, saves ids to 2026-11-16-exa-websets.json
       python3 exa_websets.py fetch    -> polls until idle, writes 2026-11-16-exa-websets-raw.json
"""
import json, os, sys, time, urllib.request, urllib.error
BASE = "https://api.exa.ai/websets/v0"
H = {"x-api-key": os.environ["EXA_API_KEY"], "Content-Type": "application/json", "User-Agent": "curl/8.5.0"}
HERE = os.path.dirname(os.path.abspath(__file__))
IDS = os.path.join(HERE, "2026-11-16-exa-websets.json")
SECTORS = {
 "1-health-care-vet-dental": "healthcare, care homes, home care, veterinary, dental, clinical or medical services",
 "2-retail-hospitality": "retail, restaurants, pubs, hotels, leisure or hospitality",
 "3-manufacturing-engineering": "manufacturing, engineering, automotive, aerospace, defence or food manufacturing",
 "4-law-accounting": "law firms, legal services, accountancy or professional services firms",
 "5-financial-services": "financial services, insurance, insurance broking, wealth management or financial advice",
}
CRITERIA = [
 "The company is headquartered in the United Kingdom",
 "The company received private equity investment (a buyout, growth investment, majority or minority stake from a private equity firm) announced on or after 18 August 2026",
 "The company has more than 50 employees",
]
def call(method, path, body=None):
    for a in range(5):
        try:
            r = urllib.request.Request(BASE + path, json.dumps(body).encode() if body else None, H, method=method)
            return json.load(urllib.request.urlopen(r, timeout=120))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 ** a); continue
            raise SystemExit(f"{e.code} {e.read()[:500].decode(errors='replace')}")
if sys.argv[1] == "create":
    ids = {}
    for seg, desc in SECTORS.items():
        body = {"search": {"query": f"UK {desc} companies that received private equity investment or were bought by a private equity firm since August 2026",
                           "count": 50, "entity": {"type": "company"},
                           "criteria": [{"description": c} for c in CRITERIA[:1]] + [{"description": f"The company operates in {desc}"}] + [{"description": c} for c in CRITERIA[1:]]},
                "enrichments": [
                    {"description": "Name of the private equity firm that invested", "format": "text"},
                    {"description": "Date the private equity investment was announced (YYYY-MM-DD)", "format": "date"},
                    {"description": "URL of the news article or press release announcing the investment", "format": "url"},
                    {"description": "The company's LinkedIn company page URL", "format": "url"}],
                "externalId": f"we-are-dna-c6-{seg}"}
        r = call("POST", "/websets", body); ids[seg] = r["id"]; print(seg, r["id"], r.get("status"), flush=True)
    json.dump(ids, open(IDS, "w"), indent=1)
elif sys.argv[1] == "fetch":
    ids = json.load(open(IDS)); out = {}
    for seg, wid in ids.items():
        while True:
            w = call("GET", f"/websets/{wid}")
            if w.get("status") == "idle": break
            time.sleep(20)
        items, cur = [], None
        while True:
            r = call("GET", f"/websets/{wid}/items?limit=100" + (f"&cursor={cur}" if cur else ""))
            items += r.get("data", []); cur = r.get("nextCursor")
            if not r.get("hasMore"): break
        out[seg] = {"webset_id": wid, "items": items}; print(seg, wid, len(items), flush=True)
    json.dump(out, open(os.path.join(HERE, "2026-11-16-exa-websets-raw.json"), "w"), indent=1)
