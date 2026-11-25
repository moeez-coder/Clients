"""Doc 1 Campaigns 1-3 FULL pull, Blitz stage (We Are DNA, 2026-11-23). Moe's go after the preview: every contact
matching the accepted persona per company (no 1-per-company cap); a person may appear in more than one campaign.
Blitz POST /v2/search/waterfall-icp-keyword, one call per company per campaign, cascade from personas.py, UK only,
max_results 10. C1 and C2 run on all 1,384 companies, C3 on the 995 at 201+. Resumable: appends to
<date>-blitz-raw.jsonl and skips (campaign, company) pairs already there. Usage: python3 full_pull_blitz.py 2026-11-23"""
import csv, json, os, sys, time, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from personas import CASCADES
HERE = os.path.dirname(os.path.abspath(__file__)); D = sys.argv[1]
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
OUT = os.path.join(HERE, f"{D}-blitz-raw.jsonl"); LOCK = threading.Lock(); USED = [0]
def post(body):
    for a in range(7):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai/v2/search/waterfall-icp-keyword", json.dumps(body).encode(), H, method="POST")
            d = json.load(urllib.request.urlopen(r, timeout=90)); USED[0] += (d.get("fair_usage") or {}).get("records_used", 0); return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"results": [], "_error": e.code, "_body": e.read()[:300].decode(errors="replace")}
        except Exception: time.sleep(2 ** a)
    return {"results": [], "_error": "retries"}
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        d = json.loads(l)
        if not d["response"].get("_error"): done.add((d["campaign"], d["company_linkedin_url"]))
cos = [r for r in csv.DictReader(open(os.path.join(HERE, f"{D}-companies.csv"))) if r["excluded"] == "-" and r["company_linkedin_url"] not in ("", "-")]
jobs = [(c, r) for c in ("c1", "c2", "c3") for r in cos if (c != "c3" or r["c3_eligible"] == "yes") and (c, r["company_linkedin_url"]) not in done]
print("todo", len(jobs), "already", len(done), flush=True)
n = [0]
def run(j):
    camp, c = j
    r = post({"company_linkedin_url": c["company_linkedin_url"], "cascade": CASCADES[camp], "max_results": 10})
    with LOCK:
        with open(OUT, "a") as f: f.write(json.dumps({"campaign": camp, "company_linkedin_url": c["company_linkedin_url"], "response": r}) + "\n")
        n[0] += 1
        if n[0] % 250 == 0: print(n[0], "records", USED[0], flush=True)
with ThreadPoolExecutor(8) as ex: list(ex.map(run, jobs))
print("done", n[0], "blitz records this run", USED[0], flush=True)
