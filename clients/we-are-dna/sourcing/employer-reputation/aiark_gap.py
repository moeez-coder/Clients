"""Doc 1 C3 gap-fill with AI Ark POST /api/developer-portal/v1/people (We Are DNA, 2026-11-23; Moe: Prospeo then AI Ark up
to 90 credits). C3 companies with no launch-set lead in <date>-3-c3-ta-leads-raw.csv, 25 company LinkedIn URLs per search
(the plan returns at most 25 results a search), current title SMART match on TA/resourcing/recruitment leader titles,
person location United Kingdom. 0.5 credit per returned person; stops when the balance would fall below 100 - CAP.
Usage: python3 aiark_gap.py <date> <cap_credits>  -> <date>-aiark-full-c3-raw.jsonl"""
import csv, json, os, sys, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); D, CAP = sys.argv[1], float(sys.argv[2])
H = {"X-TOKEN": os.environ["AIARK_API_KEY"], "Content-Type": "application/json", "User-Agent": "curl/8.5.0"}
def call(url, body=None):
    for a in range(8):   # 429 = rate limit: back off and retry (a rejected request costs nothing)
        r = urllib.request.Request(url, json.dumps(body).encode() if body else None, H, method="POST" if body else "GET")
        try: return json.load(urllib.request.urlopen(r, timeout=90))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(min(60, 5 * 2 ** a)); continue
            return {"_error": e.code, "body": e.read()[:300].decode()}
    return {"_error": 429, "body": "retries exhausted"}
start = call("https://api.ai-ark.com/api/developer-portal/v1/payments/credits")["total"]
has = {r["company_linkedin_url"] for r in csv.DictReader(open(os.path.join(HERE, f"{D}-3-c3-ta-leads-raw.csv"))) if r["status"] == "launch set"}
gap = [c["company_linkedin_url"] for c in csv.DictReader(open(os.path.join(HERE, f"{D}-3-c3-ta-companies.csv"))) if c["company_linkedin_url"] not in has]
OUT = os.path.join(HERE, f"{D}-aiark-full-c3-raw.jsonl"); done = set()
if os.path.exists(OUT):   # keep only successful batches, redo the rest
    keep = [l for l in open(OUT) if not json.loads(l)["response"].get("_error")]
    open(OUT, "w").writelines(keep); done = {json.loads(l)["batch"] for l in keep}
out = open(OUT, "a"); spent = 0
for i in range(0, len(gap), 25):
    if i // 25 in done: continue
    if spent + 12.5 > CAP: print("cap reached"); break
    body = {"page": 0, "size": 25, "account": {"linkedin": {"any": {"include": gap[i:i + 25]}}},
            "contact": {"experience": {"current": {"title": {"any": {"include": {"mode": "SMART", "content": ["Head of Talent Acquisition", "Talent Acquisition Manager",
                "Head of Resourcing", "Head of Recruitment", "Recruitment Manager", "Talent Acquisition Lead", "Resourcing Manager"]}}}}},
                        "location": {"any": {"include": ["United Kingdom"]}}}}
    d = call("https://api.ai-ark.com/api/developer-portal/v1/people", body)
    out.write(json.dumps({"campaign": "c3", "batch": i // 25, "companies": gap[i:i + 25], "response": d}) + "\n"); out.flush()
    spent += 0.5 * len(d.get("content") or []); time.sleep(2)
end = call("https://api.ai-ark.com/api/developer-portal/v1/payments/credits")["total"]
print("gap companies", len(gap), "credits before", start, "after", end, "spent", start - end)
