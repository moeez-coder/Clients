"""Doc 1 C2 HR Business Partner lever (We Are DNA, 2026-11-25; Moe: "Add HR Business Partners" to close C2's gap to +800).
Stage 1 (pull): Blitz POST /v2/search/waterfall-icp-keyword, UK, max_results 5, on every C2 company with no launch-set lead
in 2026-11-25-c2-people-leads.csv; titles HR / People Business Partner (senior/lead too). Resumable; appends to
2026-11-25-hrbp-blitz-raw.jsonl.  Stage 2 (build): adds the matches to the 2026-11-25 C2 rows as tier 'BP' -> writes
2026-11-25-2-c2-people-leads-raw.csv (append-only). Then tools/leads.py normalize.
Usage: python3 c2_hrbp.py pull | build"""
import csv, json, os, re, sys, time, threading, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
from variables import first_name, company
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "2026-11-25-hrbp-blitz-raw.jsonl")
GB = {"country_code": ["GB"]}
CASCADE = [{"include_title": ["HR Business Partner", "Senior HR Business Partner", "People Business Partner", "People Partner",
                              "Senior People Partner", "Lead HR Business Partner", "HRBP", "Human Resources Business Partner"],
            "exclude_title": ["Assistant", "Intern", "Graduate", "Apprentice", "Trainee", "Advisor", "Adviser", "Coordinator",
                              "Administrator", "Talent", "Recruitment", "Payroll", "Learning", "Reward", "Consultant"],
            "location": GB, "include_headline_search": False}]
OK = re.compile(r"\b(senior |lead |principal |group |head )?(hr|human resources|people)( and culture)? business partner\b|\bhrbp\b|\b(senior )?people partner\b", re.I)
BAD = re.compile(r"\b(assistant|intern|graduate|apprentice|trainee|advis[eo]r|coordinator|administrator|talent|recruit|payroll|learning|reward|consultant|junior)\b", re.I)
def norm(u):
    u = unquote(u or "").split("?")[0].rstrip("/").lower()
    return re.sub(r"https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", u)
rows = list(csv.DictReader(open(os.path.join(HERE, "2026-11-25-c2-people-leads-raw.csv"))))
cos = list(csv.DictReader(open(os.path.join(HERE, "2026-11-25-c2-people-companies.csv"))))
has = {r["company_linkedin_url"] for r in rows if r["status"] == "launch set"}
gap = [c for c in cos if c["company_linkedin_url"] not in has and c["company_linkedin_url"] not in ("", "-")]
if sys.argv[1] == "pull":
    H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}; LOCK = threading.Lock(); USED = [0]
    done = {json.loads(l)["company_linkedin_url"] for l in open(OUT) if not json.loads(l)["response"].get("_error")} if os.path.exists(OUT) else set()
    jobs = [c["company_linkedin_url"] for c in gap if c["company_linkedin_url"] not in done]; print("todo", len(jobs), flush=True)
    def post(body):
        for a in range(7):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request("https://api.blitz-api.ai/v2/search/waterfall-icp-keyword",
                    json.dumps(body).encode(), H, method="POST"), timeout=90))
                USED[0] += (d.get("fair_usage") or {}).get("records_used", 0); return d
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
                return {"results": [], "_error": e.code}
            except Exception: time.sleep(2 ** a)
        return {"results": [], "_error": "retries"}
    def run(li):
        r = post({"company_linkedin_url": li, "cascade": CASCADE, "max_results": 5})
        with LOCK:
            with open(OUT, "a") as f: f.write(json.dumps({"campaign": "c2", "company_linkedin_url": li, "response": r}) + "\n")
    with ThreadPoolExecutor(8) as ex: list(ex.map(run, jobs))
    print("done, blitz records", USED[0])
else:
    P = os.path.join(HERE, "2026-11-25-2-c2-people-leads-raw.csv"); assert not os.path.exists(P), "append-only"
    info = {c["company_linkedin_url"]: c for f in ("2026-11-23-companies.csv", "2026-11-25-companies.csv") for c in csv.DictReader(open(os.path.join(HERE, f)))}
    seen = {}
    for r in rows: seen.setdefault(r["company_linkedin_url"], set()).update({r["linkedin_url"], (r["first_name"].lower(), (r["last_name"].split() or ["-"])[0].lower())})
    C6 = {norm(r["linkedin_url"]) for r in csv.DictReader(open(os.path.join(HERE, "../pe-investment-triggers/2026-11-16-3-leads.csv")))}
    ACC = re.compile(r"\b(recruit\w*|talent|careers?|hiring|jobs|hr|people|team|internal|ltd|limited)\b", re.I)
    add = 0
    for l in open(OUT):
        d = json.loads(l); c = info[d["company_linkedin_url"]]
        for p in d["response"].get("results", []):
            per = p.get("person") or p; exp = (per.get("experiences") or [{}])[0]
            fn, ln, t = per.get("first_name") or "-", per.get("last_name") or "-", exp.get("job_title") or "-"
            u, cc = norm(per.get("linkedin_url")), ((per.get("location") or {}).get("country_code")) or "-"
            k2 = (fn.lower(), (ln.split() or ["-"])[0].lower())
            if u in seen.setdefault(c["company_linkedin_url"], set()) or k2 in seen[c["company_linkedin_url"]]: continue
            seen[c["company_linkedin_url"]] |= {u, k2}
            cf = first_name(fn, f"{fn} {ln}")
            st = ("removed: not UK-based" if cc != "GB" else "removed: title not the persona" if (BAD.search(t) or not OK.search(t))
                  else "removed: no name" if "-" in (fn, ln) else "removed: company account, not a person" if ACC.search(fn)
                  else "removed: first name is an initial" if len(re.sub(r"[^A-Za-z]", "", cf)) < 2
                  else "hold: also in Campaign 6 (PE investment) lead list" if u in C6 else "launch set")
            rows.append({"linkedin_url": u, "first_name": fn, "last_name": ln, "full_name": f"{fn} {ln}", "job_title": t,
                "company_name": c["company_name"], "company_domain": c["company_domain"], "company_linkedin_url": c["company_linkedin_url"],
                "person_country": cc, "company_country": "GB", "status": st, "tier": "BP" if st == "launch set" else "-", "source": "blitz-hrbp",
                "sector": c["sector"], "size_band": c["size_band"], "clean_first_name": cf, "clean_company": company(c["company_name"]),
                "sector_peers": c["sector_peers"], "theme": c["theme"], "theme_source": c["theme_source"], "campaign": "c2"})
            add += st == "launch set"
    with open(P, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    print("gap companies", len(gap), "HRBP launch set added", add, "at", len({r["company_linkedin_url"] for r in rows if r["tier"] == "BP"}), "companies")
