"""Campaign 6 signal source 2: Exa search API (POST https://api.exa.ai/search, category news), 2026-11-16.
Deal-announcement articles published since 2026-08-18 about UK private equity investments in the five doc-1 sectors.
Each article gets an Exa structured summary (company, investor, sector, UK HQ, deal type) so no article is read by hand.
Usage: python3 exa_news.py  -> writes 2026-11-16-exa-news-raw.json
"""
import json, os, time, urllib.request, urllib.error
H = {"x-api-key": os.environ["EXA_API_KEY"], "Content-Type": "application/json", "User-Agent": "curl/8.5.0"}
HERE = os.path.dirname(os.path.abspath(__file__))
Q = {
 "1-health-care-vet-dental": ["private equity investment UK care home group", "private equity backs UK veterinary group", "private equity investment UK dental group", "private equity acquires UK healthcare services provider", "private equity investment UK home care provider"],
 "2-retail-hospitality": ["private equity acquires UK retailer", "private equity investment UK restaurant group", "private equity backs UK pub group", "private equity investment UK hotel group", "private equity investment UK leisure operator"],
 "3-manufacturing-engineering": ["private equity investment UK manufacturer", "private equity backs UK engineering firm", "private equity acquires UK food manufacturer", "private equity investment UK aerospace defence supplier", "management buyout private equity UK manufacturing"],
 "4-law-accounting": ["private equity investment UK accountancy firm", "private equity backs UK law firm", "private equity investment UK professional services firm", "private equity acquires UK accounting practice"],
 "5-financial-services": ["private equity investment UK insurance broker", "private equity backs UK wealth management firm", "private equity investment UK financial advice firm", "private equity acquires UK financial services company"],
}
SCHEMA = {"type": "object", "properties": {
  "company_name": {"type": "string", "description": "the company that received the private equity investment or was bought"},
  "investor": {"type": "string", "description": "the private equity firm(s)"},
  "deal_type": {"type": "string", "description": "buyout, growth investment, minority stake, secondary buyout, acquisition by PE-backed platform, or not a PE deal"},
  "uk_headquartered": {"type": "boolean"},
  "sector": {"type": "string"},
  "employees_mentioned": {"type": "string"}},
  "required": ["company_name", "investor", "deal_type", "uk_headquartered", "sector"]}
def search(q):
    body = {"query": q, "category": "news", "numResults": 50, "startPublishedDate": "2026-08-18T00:00:00.000Z",
            "contents": {"summary": {"query": "Extract the private equity deal described.", "schema": SCHEMA}}}
    for a in range(5):
        try:
            r = urllib.request.Request("https://api.exa.ai/search", json.dumps(body).encode(), H, method="POST")
            return json.load(urllib.request.urlopen(r, timeout=180))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 ** a); continue
            return {"_error": e.code, "_body": e.read()[:300].decode(errors="replace")}
out = {}; cost = 0.0
for seg, qs in Q.items():
    out[seg] = []
    for q in qs:
        r = search(q); cost += (r.get("costDollars") or {}).get("total", 0) or 0
        for x in r.get("results", []):
            out[seg].append({"query": q, "url": x.get("url"), "title": x.get("title"), "published": x.get("publishedDate"), "summary": x.get("summary")})
        print(seg, q, len(r.get("results", [])), r.get("_body", ""), flush=True)
        time.sleep(0.3)
json.dump({"cost_usd": cost, "results": out}, open(os.path.join(HERE, "2026-11-16-exa-news-raw.json"), "w"), indent=1)
print("cost_usd", round(cost, 3))
