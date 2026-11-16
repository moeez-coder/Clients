"""Step 5: full job description for each company's chosen posting (needed by Moe's JD-phrase prompt, 2026-11-16).

Blitz returns only a two-sentence ai_summary, so the description is read from the public posting page:
GET https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/<job id>  (no login; the id is the number in job_url).
Only companies with a launch lead are fetched. A 404/410 means the posting is closed. Output:
<date>-job-descriptions.csv (company_linkedin_url, job_url, http_status, closed, description). Resumable via raw/jd.jsonl.
Usage: python3 pull_job_descriptions.py
"""
import csv, html, json, os, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); DATE = "2026-11-16"; out = os.path.join(HERE, "raw", "jd.jsonl")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36", "Accept-Language": "en-US"}
want = {r["company_linkedin_url"] for r in csv.DictReader(open(os.path.join(HERE, f"{DATE}-role-phrases-2.csv")))}
comps = [c for c in csv.DictReader(open(os.path.join(HERE, f"{DATE}-companies.csv"))) if c["company_linkedin_url"] in want]
done = {json.loads(l)["company_linkedin_url"] for l in open(out)} if os.path.exists(out) else set()

def one(c):
    jid = re.search(r"(\d{8,})", c["job_url"]).group(1); st, d, closed = 0, "", False
    for a in range(5):
        try:
            t = urllib.request.urlopen(urllib.request.Request(f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{jid}", headers=UA), timeout=40).read().decode("utf8", "replace")
            st = 200
            m = re.search(r'show-more-less-html__markup[^>]*>(.*?)</div>', t, re.S)
            d = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", m.group(1)))).strip() if m else ""
            closed = "No longer accepting applications" in t
            break
        except urllib.error.HTTPError as e:
            st = e.code
            if e.code in (404, 410): closed = True; break
            time.sleep(3 * (a + 1))
        except Exception:
            st = -1; time.sleep(3 * (a + 1))
    time.sleep(0.4)
    return {"company_linkedin_url": c["company_linkedin_url"], "job_url": c["job_url"], "http_status": st, "closed": closed, "description": d}

with ThreadPoolExecutor(4) as ex, open(out, "a") as f:
    for i, r in enumerate(ex.map(one, [c for c in comps if c["company_linkedin_url"] not in done])):
        f.write(json.dumps(r) + "\n")
        if i % 100 == 0: f.flush(); print(i, r["http_status"], flush=True)
rows = [json.loads(l) for l in open(out)]
with open(os.path.join(HERE, f"{DATE}-job-descriptions.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader()
    for r in rows: w.writerow({**r, "description": r["description"] or "-"})
import collections
print(len(rows), collections.Counter(r["http_status"] for r in rows), "closed:", sum(r["closed"] for r in rows), "with desc:", sum(bool(r["description"]) for r in rows))
