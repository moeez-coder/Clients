"""Open-posting check + full job description for each company with a launch-set lead (2026-11-24).
Public posting page GET linkedin.com/jobs-guest/jobs/api/jobPosting/<id> (as ../recruitment-specific-open-roles/pull_job_descriptions.py).
Order per company: its chosen posting first, then its other kept postings in the same family, newest first; the first OPEN one
wins (closed = 404/410 or "No longer accepting applications"). If none is open, the chosen posting is kept and marked closed.
Also flags reposted_since: the first-seen date when the same title was first posted 60+ days ago and reposted in the last 30.
Output $RAW/jd.jsonl (resumable) -> written to the segment CSVs by build_segments.py.  Usage: RAW=/path python3 fetch_jds.py"""
import csv, html, json, os, re, time, datetime, urllib.request, urllib.error, collections
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, ".."); RAW = os.environ["RAW"]
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36", "Accept-Language": "en-US"}
T = datetime.date(2026, 11, 24)
allj = list(csv.DictReader(open(os.path.join(S, "tam", "2026-11-24-mpc-segments-jobs.csv"))))
kept = [r for r in allj if r["status"] == "kept"]
latest = {}
for r in allj:
    if r["status"].startswith("removed: repost"):
        k = (r["company_linkedin_url"], r["title"].lower()); latest[k] = max(latest.get(k, ""), r["date_posted"])
comps = {c["company_linkedin_url"]: c for c in json.load(open(os.path.join(RAW, "companies.json")))}
want = {r["company_linkedin_url"] for r in csv.DictReader(open(os.path.join(RAW, "leads-raw.csv"))) if r["status"] == "launch set"}
out = os.path.join(RAW, "jd.jsonl"); done = {json.loads(l)["company_linkedin_url"] for l in open(out)} if os.path.exists(out) else set()

def page(url):
    m = re.search(r"(\d{8,})", url)
    if not m: return None, False, ""
    for a in range(5):
        try:
            t = urllib.request.urlopen(urllib.request.Request(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{m.group(1)}", headers=UA), timeout=40).read().decode("utf8", "replace")
            d = re.search(r'show-more-less-html__markup[^>]*>(.*?)</div>', t, re.S)
            time.sleep(0.4)
            return 200, "No longer accepting applications" in t, re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", d.group(1)))).strip() if d else ""
        except urllib.error.HTTPError as e:
            if e.code in (404, 410): return e.code, True, ""
            time.sleep(3 * (a + 1))
        except Exception: time.sleep(3 * (a + 1))
    return -1, None, ""

def one(u):
    c = comps[u]
    cands = [r for r in kept if r["company_linkedin_url"] == u and r["role_family"] == c["segment"]]
    cands.sort(key=lambda r: (r["job_url"] != c["job_url"], r["date_posted"]), reverse=False)
    cands = [cands[0]] + sorted(cands[1:], key=lambda r: r["date_posted"], reverse=True)
    first = None
    for r in cands[:4]:
        st, closed, d = page(r["job_url"])
        res = {"company_linkedin_url": u, "open_role": r["title"], "job_url": r["job_url"], "job_posted": r["date_posted"],
               "jd_summary": r["jd_summary"], "http_status": st, "posting_open": "no" if closed else ("yes" if closed is False else "-"),
               "switched_to_other_posting": "no" if r["job_url"] == c["job_url"] else "yes", "description": d}
        l = latest.get((u, r["title"].lower()))
        res["reposted_since"] = r["date_posted"] if ((T - datetime.date.fromisoformat(r["date_posted"])).days >= 60 and l and (T - datetime.date.fromisoformat(l)).days < 30) else "-"
        if first is None: first = res
        if res["posting_open"] == "yes": return res
    first["switched_to_other_posting"] = "no"
    return first

with ThreadPoolExecutor(4) as ex, open(out, "a") as f:
    for i, r in enumerate(ex.map(one, [u for u in want if u not in done])):
        f.write(json.dumps(r) + "\n")
        if i % 50 == 0: f.flush(); print(i, flush=True)
rows = [json.loads(l) for l in open(out)]
print(len(rows), collections.Counter(r["posting_open"] for r in rows), "switched", sum(r["switched_to_other_posting"] == "yes" for r in rows),
      "reposted", sum(r["reposted_since"] != "-" for r in rows), "with desc", sum(bool(r["description"]) for r in rows))
