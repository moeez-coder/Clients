"""Doc 2 Campaign 6 cross-check: Exa POST /search (category news), FDA new-indication approvals published in October 2026.
Compared with openFDA efficacy supplements dated 2026-10 (25). Writes 2026-11-18-doc-2-exa.json."""
import json, os, urllib.request
body = {"query": "FDA approves drug for new indication label expansion", "category": "news", "numResults": 50, "type": "auto",
        "startPublishedDate": "2026-10-01T00:00:00Z", "endPublishedDate": "2026-10-31T23:59:59Z"}
r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.exa.ai/search", data=json.dumps(body).encode(),
        headers={"x-api-key": os.environ["EXA_API_KEY"], "Content-Type": "application/json"}), timeout=120))
rows = [{"title": x.get("title"), "url": x.get("url"), "published": x.get("publishedDate")} for x in r.get("results", [])]
json.dump({"body": body, "cost": r.get("costDollars"), "rows": rows}, open("2026-11-18-doc-2-exa.json", "w"), indent=1)
print(r.get("costDollars")); [print(x["published"][:10] if x["published"] else "", x["title"]) for x in rows]
