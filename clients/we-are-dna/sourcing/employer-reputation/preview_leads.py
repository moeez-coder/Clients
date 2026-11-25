"""Doc 1 Campaigns 1-3 PREVIEW (2026-11-23), We Are DNA. 25 companies per campaign from <date>-companies.csv
(C1 and C2 share one 25-company sample across all sizes; C3 uses 25 from the 201+ rows), 5 per sector, seeded.
Blitz POST /v2/search/waterfall-icp-keyword per company per campaign, cascade from personas.py, max_results 3 (to measure
depth; only 1 per company is used). LinkedIn URLs only, no email. Usage: python3 preview_leads.py 2026-11-23
Writes <date>-preview-sample.csv, <date>-preview-blitz-raw.jsonl."""
import csv, json, os, random, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from personas import CASCADES
HERE = os.path.dirname(os.path.abspath(__file__)); D = sys.argv[1]
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
USED = [0]
def post(body):
    for a in range(6):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai/v2/search/waterfall-icp-keyword", json.dumps(body).encode(), H, method="POST")
            d = json.load(urllib.request.urlopen(r, timeout=90)); USED[0] += (d.get("fair_usage") or {}).get("records_used", 0); return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"results": [], "_error": e.code, "_body": e.read()[:300].decode(errors="replace")}
        except Exception as e:
            time.sleep(2 ** a)
    return {"results": [], "_error": "retries"}
cos = [r for r in csv.DictReader(open(os.path.join(HERE, f"{D}-companies.csv"))) if r["excluded"] == "-" and r["company_linkedin_url"] not in ("", "-")]
def sample(rows, seed):
    rnd = random.Random(seed); out = []
    for s in sorted({r["sector"] for r in rows}):
        pool = [r for r in rows if r["sector"] == s]; rnd.shuffle(pool); out += pool[:5]
    return out
s12 = sample(cos, 23); s3 = sample([r for r in cos if r["c3_eligible"] == "yes"], 1123)
jobs = [("c1", c) for c in s12] + [("c2", c) for c in s12] + [("c3", c) for c in s3]
with open(os.path.join(HERE, f"{D}-preview-sample.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["campaign"] + list(cos[0])); w.writeheader()
    for camp, c in jobs: w.writerow({"campaign": camp, **c})
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(lambda j: (j, post({"company_linkedin_url": j[1]["company_linkedin_url"], "cascade": CASCADES[j[0]], "max_results": 3})), jobs))
with open(os.path.join(HERE, f"{D}-preview-blitz-raw.jsonl"), "w") as f:
    for (camp, c), r in res: f.write(json.dumps({"campaign": camp, "company_linkedin_url": c["company_linkedin_url"], "response": r}) + "\n")
print("jobs", len(jobs), "with results", sum(1 for _, r in res if r.get("results")), "blitz records", USED[0],
      "errors", [r.get("_body") or r.get("_error") for _, r in res if r.get("_error")][:3])
