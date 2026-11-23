"""Doc 1 C1-3 widening pass, Blitz stage (We Are DNA, 2026-11-23, Moe: "run them" / "proceed"). Only companies with no
launch-set lead in <date>-<camp>-leads.csv. Blitz POST /v2/search/waterfall-icp-keyword with personas.WIDEN_CASCADES
(C1: Founder/Owner/Chair/Partner/Director; C2: HR/People Manager), UK only, max_results 5. Resumable; appends to
<date>-widen-blitz-raw.jsonl. Usage: python3 widen_blitz.py 2026-11-23"""
import csv, json, os, sys, time, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from personas import WIDEN_CASCADES
HERE = os.path.dirname(os.path.abspath(__file__)); D = sys.argv[1]
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
OUT = os.path.join(HERE, f"{D}-widen-blitz-raw.jsonl"); LOCK = threading.Lock(); USED = [0]
def post(body):
    for a in range(7):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai/v2/search/waterfall-icp-keyword", json.dumps(body).encode(), H, method="POST")
            d = json.load(urllib.request.urlopen(r, timeout=90)); USED[0] += (d.get("fair_usage") or {}).get("records_used", 0); return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"results": [], "_error": e.code}
        except Exception: time.sleep(2 ** a)
    return {"results": [], "_error": "retries"}
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        d = json.loads(l)
        if not d["response"].get("_error"): done.add((d["campaign"], d["company_linkedin_url"]))
jobs = []
for camp, n in (("c1", "c1-ceo"), ("c2", "c2-people")):
    has = {r["company_linkedin_url"] for r in csv.DictReader(open(os.path.join(HERE, f"{D}-{n}-leads.csv"))) if r["status"] == "launch set"}
    for c in csv.DictReader(open(os.path.join(HERE, f"{D}-{n}-companies.csv"))):
        li = c["company_linkedin_url"]
        if li not in has and li not in ("", "-") and (camp, li) not in done: jobs.append((camp, li))
print("todo", len(jobs), flush=True)
def run(j):
    r = post({"company_linkedin_url": j[1], "cascade": WIDEN_CASCADES[j[0]], "max_results": 5})
    with LOCK:
        with open(OUT, "a") as f: f.write(json.dumps({"campaign": j[0], "company_linkedin_url": j[1], "response": r}) + "\n")
with ThreadPoolExecutor(8) as ex: list(ex.map(run, jobs))
print("done, blitz records", USED[0], flush=True)
