"""Blitz pull + CSV build for C&G's MQC campaign (talent leaders at fresh Northeast hiring companies).

Usage:
  python3 pull_mqc.py pull  <raw_dir> ne|rest [max_new]   # Blitz calls, resumable, raw JSONL in <raw_dir>/mqc/
  python3 pull_mqc.py build <raw_dir> <date>     # writes mqc-talent-leaders/<date>-{companies,jobs,leads}.csv

Steps (filters in mqc_spec.py; every request body is logged to <raw_dir>/mqc/requests.jsonl):
  1. POST /v2/company/tam-by-jobs (1 record/company): Northeast HQ, LS + tech industries, 51-1,000 staff,
     is_agency false, a C&G role-family posting in the last 30 days. Skips every company already touched by a
     CG campaign (see excluded_companies) and stops at MAX_NEW_COMPANIES new ones.
  2. POST /v2/jobs/company (max_results 1) per new company -> its {Open_Role}.
  3. POST /v2/search/waterfall-icp-keyword per company with a job: tier 1 TA leaders, tier 2 HR leaders, 1 person.
Dedupe is mandatory (Moe's brief): a lead is live only if its LinkedIn URL is in no CG campaign list
(1056840 = wave1 + wave2 rows 1-2100; 1141179-1141182 = live_eligible rows of the open-role leads files)
and in no other CG *-leads.csv at all.
"""
import csv, glob, html, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
import pull_open_roles as P
from build_open_roles import norm, v, clean_last
from mqc_spec import (INDUSTRIES, SIZES, DATE_POSTED_DAYS, JOB_TITLES, JOB_TITLE_EXCLUDE, NORTHEAST_STATES,
                      TA_TITLES, HR_TITLES, PEOPLE_EXCLUDE, PER_COMPANY, MAX_NEW_COMPANIES)

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "mqc-talent-leaders"
BENCH = os.path.join(HERE, "security-and-data-bench")


def heyreach_bench_rows():
    rows = list(csv.DictReader(open(os.path.join(BENCH, "2026-10-23-2-heyreach-wave1.csv"))))
    rows += list(csv.DictReader(open(os.path.join(BENCH, "2026-10-27-heyreach-wave2.csv"))))[:2100]
    return rows


def excluded_companies():
    """Every company a CG campaign has touched or may touch: Bench waves, all open-role companies files."""
    s = {norm(r["company_linkedin_url"]) for r in heyreach_bench_rows()}
    for p in glob.glob(os.path.join(HERE, "recruiter-open-role-*", "*-companies.csv")):
        s |= {norm(r["company_linkedin_url"]) for r in csv.DictReader(open(p))}
    for p in glob.glob(os.path.join(HERE, "recruiter-open-role-*", "*-leads.csv")):
        s |= {norm(r["company_linkedin_url"]) for r in csv.DictReader(open(p))}
    s.discard("")
    return s


def prior_people():
    """url -> where it already is. Any appearance in any other CG leads file blocks the lead."""
    m = {}
    for r in heyreach_bench_rows():
        m.setdefault(norm(r["linkedin_url"]), set()).add("heyreach list 1056840")
    for p in sorted(glob.glob(os.path.join(HERE, "*", "*-leads.csv"))):
        if os.path.basename(os.path.dirname(p)) == SLUG:
            continue
        tag = os.path.relpath(p, HERE)
        for r in csv.DictReader(open(p)):
            m.setdefault(norm(r["linkedin_url"]), set()).add(tag)
    return m


def tam_body(ne=True):
    return {"job": {"title": {"include": JOB_TITLES, "exclude": JOB_TITLE_EXCLUDE},
                    "location": {"country_code": {"include": ["US"]}},
                    "date_posted": {"last_days": DATE_POSTED_DAYS}},
            "company": {"is_agency": False, "industry": {"include": INDUSTRIES}, "size": {"include": SIZES},
                        "hq": {"country_code": {"include": ["US"]},
                               "state": {("include" if ne else "exclude"): NORTHEAST_STATES}}}}


def pull(raw, part="ne", max_new=MAX_NEW_COMPANIES):
    """part 'ne' = Northeast-HQ companies (run first); 'rest' = the rest of the US (added 2026-11-12 after the
    Northeast pass returned only 91 untouched companies: earlier CG campaigns already cover most of it)."""
    max_new = int(max_new)
    sfx = "" if part == "ne" else "_rest"
    d = os.path.join(raw, "mqc"); os.makedirs(d, exist_ok=True)
    log = open(os.path.join(d, "requests.jsonl"), "a")
    excl = excluded_companies()
    print(f"excluded companies (already in CG campaigns/snapshots): {len(excl)}", flush=True)

    if part == "rest":  # never re-pick a company the Northeast pass already took
        excl |= {norm(json.loads(l)["company"]["linkedin_url"]) for l in open(os.path.join(d, "companies.jsonl"))}
    out = os.path.join(d, f"companies{sfx}.jsonl")
    if not os.path.exists(out + ".done"):
        body = tam_body(part == "ne")
        log.write(json.dumps({"path": "/v2/company/tam-by-jobs", "part": part, "body": body,
                              "stop_at_new_companies": max_new}) + "\n"); log.flush()
        new, paged, cursor = {}, 0, None
        while True:
            r = P.post("/v2/company/tam-by-jobs", dict(body, max_results=50, **({"cursor": cursor} if cursor else {})))
            if paged == 0:
                print("total_results (indicative):", r.get("total_results"), flush=True)
            for row in r.get("results", []):
                paged += 1
                k = norm(row["company"]["linkedin_url"])
                if k and k not in excl and k not in new:
                    new[k] = row
            cursor = r.get("cursor")
            if not cursor or not r.get("results") or len(new) >= max_new:
                break
        with open(out, "w") as f:
            for row in list(new.values())[:max_new]:
                f.write(json.dumps(row) + "\n")
        open(out + ".done", "w").write(json.dumps({"paged": paged, "new": len(new)}))
        print(f"tam-by-jobs: paged {paged}, new companies {len(new)}", flush=True)
    rows = [json.loads(l) for l in open(out)]
    urls = [r["company"]["linkedin_url"] for r in rows]
    names = {r["company"]["linkedin_url"]: r["company"].get("name") for r in rows}

    out = os.path.join(d, f"jobs{sfx}.jsonl")
    if not os.path.exists(out + ".done"):
        jbody = {"title": {"include": JOB_TITLES, "exclude": JOB_TITLE_EXCLUDE},
                 "location": {"country_code": {"include": ["US"]}}, "date_posted": {"last_days": DATE_POSTED_DAYS}}
        log.write(json.dumps({"path": "/v2/jobs/company", "count": len(urls),
                              "body_template": {"company_linkedin_url": "<url>", "job": jbody, "max_results": 1}}) + "\n"); log.flush()
        with ThreadPoolExecutor(20) as ex:
            res = list(ex.map(lambda u: (u, P.post("/v2/jobs/company",
                                                   {"company_linkedin_url": u, "job": jbody, "max_results": 1})), urls))
        with open(out, "w") as f:
            for u, r in res:
                for j in r.get("results", [])[:1]:
                    j.setdefault("company_linkedin_url", u); j.setdefault("company_name", names.get(u))
                    f.write(json.dumps(j) + "\n")
        open(out + ".done", "w").write(str(len(res)))
        print(f"jobs/company: {sum(1 for _ in open(out))} jobs for {len(urls)} companies", flush=True)

    have_job = sorted({json.loads(l)["company_linkedin_url"] for l in open(out)})
    out = os.path.join(d, f"people{sfx}.jsonl")
    if not os.path.exists(out + ".done"):
        cascade = [{"include_title": t, "exclude_title": PEOPLE_EXCLUDE, "location": {"country_code": ["US"]},
                    "include_headline_search": False} for t in (TA_TITLES, HR_TITLES)]
        log.write(json.dumps({"path": "/v2/search/waterfall-icp-keyword", "companies": len(have_job),
                              "body_template": {"company_linkedin_url": "<url>", "cascade": cascade,
                                                "max_results": PER_COMPANY}}) + "\n"); log.flush()
        with ThreadPoolExecutor(20) as ex:
            res = list(ex.map(lambda u: (u, P.post("/v2/search/waterfall-icp-keyword",
                                                   {"company_linkedin_url": u, "cascade": cascade,
                                                    "max_results": PER_COMPANY})), have_job))
        with open(out, "w") as f:
            for u, r in res:
                f.write(json.dumps({"company_linkedin_url": u, "results": r.get("results", [])}) + "\n")
        open(out + ".done", "w").write(str(len(res)))
        print(f"waterfall: {len(res)} companies", flush=True)

    prev = json.load(open(os.path.join(d, "usage.json"))) if os.path.exists(os.path.join(d, "usage.json")) else {}
    for k, val in P.USAGE.items():
        prev[k] = prev.get(k, 0) + val
    json.dump(prev, open(os.path.join(d, "usage.json"), "w"), indent=1)
    print("records_used this run:", P.USAGE, "cumulative:", prev, flush=True)


SUFFIX = re.compile(r"[,]?\s+(inc\.?|llc|l\.l\.c\.|corp\.?|corporation|co\.|ltd\.?|plc|lp|l\.p\.|pbc|holdings)$", re.I)


def clean_company(name):
    """{Company_Name} for copy: drop legal suffixes and trailing punctuation, keep the brand."""
    n = html.unescape(name or "").strip()
    for _ in range(2):
        n = SUFFIX.sub("", n).strip().rstrip(",").strip()
    return n


def first_clean(fn):
    """Same rule as the GTM Sheets First Name Clean formula: strip a bracketed nickname, keep the first token."""
    f = re.sub(r"\(.*?\)|\".*?\"", "", fn or "").strip()
    return f.split(" ")[0] if f else ""


def clean_role(t):
    """{Open_Role} for copy: drop location/remote/req-id tails and brackets so it reads as a role name."""
    t = re.sub(r"\s*[\(\[].*?[\)\]]", "", html.unescape(t or ""))
    parts = re.split(r"\s+[-\u2013\u2014|/]\s+|\s*\|\s*", t)
    # "Director - Regulatory Compliance": a one-word head is not a role name, keep the next part with it
    t = parts[0].strip() if len(parts[0].split()) > 1 or len(parts) == 1 else f"{parts[0].strip()}, {parts[1].strip()}"
    if len(t) > 55:
        t = t.split(",")[0].strip()
    if len(t.split()) == 1 and t.lower() in {"manager", "director", "faculty", "lab", "analyst", "lead", "staff"}:
        return ""  # a bare generic word would read badly in the copy
    return t if 3 <= len(t) <= 55 else ""


def build(raw, date):
    d = os.path.join(raw, "mqc")
    out = os.path.join(HERE, SLUG); os.makedirs(out, exist_ok=True)
    for kind in ("jobs", "companies", "leads"):
        if os.path.exists(os.path.join(out, f"{date}-{kind}.csv")):
            sys.exit(f"{date}-{kind}.csv exists; snapshots are append-only")
    def rd(stem):
        return [json.loads(l) for sfx in ("", "_rest") if os.path.exists(os.path.join(d, f"{stem}{sfx}.jsonl"))
                for l in open(os.path.join(d, f"{stem}{sfx}.jsonl"))]
    comps = {norm(c["company"]["linkedin_url"]): c["company"] for c in rd("companies")}
    jobs = {norm(j["company_linkedin_url"]): j for j in rd("jobs")}
    prior = prior_people()

    with open(os.path.join(out, f"{date}-jobs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["job_url", "title", "date_posted", "company_name", "company_linkedin_url", "job_city", "ai_summary"])
        for j in sorted(jobs.values(), key=lambda j: j.get("date_posted") or "", reverse=True):
            w.writerow([v(j.get("url")), v(j.get("title")), v((j.get("date_posted") or "")[:10]), v(j.get("company_name")),
                        v(j.get("company_linkedin_url")), v((j.get("location") or {}).get("city")), v(j.get("ai_summary"))])

    leads, seen, co_leads = [], set(), {}
    for rec in rd("people"):
        k = norm(rec["company_linkedin_url"])
        for res in rec["results"]:
            p = res.get("person") or {}
            u = norm(p.get("linkedin_url"))
            if not u or u in seen:
                continue
            seen.add(u)
            exp = next((e for e in p.get("experiences") or [] if norm(e.get("company_linkedin_url")) == k),
                       (p.get("experiences") or [{}])[0])
            c, j = comps.get(k, {}), jobs.get(k, {})
            dup = "; ".join(sorted(prior.get(u, set())))
            fc = first_clean(p.get("first_name"))
            cn = clean_company(c.get("name") or j.get("company_name"))
            title = exp.get("job_title") or p.get("headline") or ""
            bad_title = any(re.search(r"\b" + re.escape(x) + r"\b", title, re.I) for x in PEOPLE_EXCLUDE)
            ok = not dup and not bad_title and fc and len(fc) > 1 and not fc.endswith(".") and cn
            leads.append({
                "linkedin_url": p.get("linkedin_url"), "first_name": v(p.get("first_name")), "first_name_clean": v(fc),
                "last_name": v(clean_last(p.get("last_name"))),
                "title": v(exp.get("job_title") or p.get("headline")),
                "persona_tier": "1 talent acquisition" if res.get("icp") == 1 else "2 hr leader",
                "company_name": v(c.get("name") or j.get("company_name")), "company_name_clean": v(cn),
                "company_linkedin_url": v(rec["company_linkedin_url"]), "industry": v(c.get("industry")),
                "size": v(c.get("size")), "hq_state": v((c.get("hq") or {}).get("state")),
                "open_role": v(j.get("title")), "open_role_clean": v(clean_role(j.get("title"))), "job_url": v(j.get("url")), "job_posted": v((j.get("date_posted") or "")[:10]),
                "dupe_of": v(dup), "live_eligible": "yes" if ok else "no",
                "excluded_reason": "-" if ok else ("dupe" if dup else "title excluded (mqc_spec.PEOPLE_EXCLUDE)" if bad_title
                                                   else "name not usable in {Fname}/{Company}"),
            })
            co_leads[k] = co_leads.get(k, 0) + 1
    leads.sort(key=lambda r: (r["persona_tier"], r["job_posted"]), reverse=False)
    cols = list(leads[0].keys())
    with open(os.path.join(out, f"{date}-leads.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(leads)

    with open(os.path.join(out, f"{date}-companies.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company_linkedin_url", "company_name", "domain", "industry", "size", "hq_city", "hq_state",
                    "open_role", "job_url", "job_posted", "leads_in_snapshot"])
        for k, c in sorted(comps.items(), key=lambda kv: kv[1].get("name") or ""):
            j = jobs.get(k, {})
            w.writerow([v(c.get("linkedin_url")), v(c.get("name")), v(c.get("domain")), v(c.get("industry")),
                        v(c.get("size")), v((c.get("hq") or {}).get("city")), v((c.get("hq") or {}).get("state")),
                        v(j.get("title")), v(j.get("url")), v((j.get("date_posted") or "")[:10]), co_leads.get(k, 0)])
    s = {"companies": len(comps), "companies_with_job": len(jobs), "companies_with_lead": len(co_leads),
         "leads": len(leads), "tier1_ta": sum(r["persona_tier"].startswith("1") for r in leads),
         "dupes": sum(r["dupe_of"] != "-" for r in leads),
         "live_eligible": sum(r["live_eligible"] == "yes" for r in leads),
         "usage": json.load(open(os.path.join(d, "usage.json")))}
    s["records_total"] = sum(s["usage"].values())
    print(json.dumps(s, indent=1))
    json.dump(s, open(os.path.join(d, "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    {"pull": lambda a: pull(*a), "build": lambda a: build(a[0], a[1])}[sys.argv[1]](sys.argv[2:])
