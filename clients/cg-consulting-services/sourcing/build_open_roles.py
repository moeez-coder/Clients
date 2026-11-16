"""Build the committed CSVs for one open-role segment from the raw Blitz JSONL (pull_open_roles.py).

Usage: python3 build_open_roles.py <slug> <raw_dir> <date>
Writes into sourcing/<slug>/:  <date>-jobs.csv, <date>-companies.csv, <date>-leads.csv
Dedupe (flagged, never dropped), by normalised LinkedIn URL:
  - in_heyreach_list_1056840: wave1 file + wave2 rows 1-2100 (the exact content of list 1056840 used by
    HeyReach 677893/686451, verified at 2,593 on 2026-11-05)
  - dupe_of: every other CG *-leads.csv in this repo (incl. the open-role segments built earlier in the
    order clinical-data -> regulatory-quality -> medical-affairs -> tech), so a person is kept live in the
    first segment only.
"""
import csv, json, os, re, sys, urllib.parse
from glob import glob
from open_role_spec import SEGMENTS, NORTHEAST_STATES

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = list(SEGMENTS)
LEAD_COLS = ["linkedin_url", "first_name", "last_name", "title", "waterfall_tier", "company_name",
             "company_linkedin_url", "open_role", "job_url", "job_posted", "jd_summary", "hq_state", "northeast",
             "in_heyreach_list_1056840", "dupe_of", "live_eligible"]


def norm(u):
    if not u:
        return ""
    u = urllib.parse.unquote(u.strip()).lower().split("?")[0].rstrip("/")
    u = re.sub(r"^https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", u)
    return u


def v(x):
    x = "" if x is None else str(x).strip()
    return x if x else "-"


def clean_last(s):
    return (s or "").split(",")[0].strip()


def load_jsonl(p):
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


def main(slug, raw, date):
    d = os.path.join(raw, slug)
    out = os.path.join(HERE, slug); os.makedirs(out, exist_ok=True)
    for kind in ("jobs", "companies", "leads"):
        if os.path.exists(os.path.join(out, f"{date}-{kind}.csv")):
            sys.exit(f"{date}-{kind}.csv exists; snapshots are append-only, pass a new date suffix")

    jobs = []
    for fn in sorted(os.listdir(d)):
        if fn.startswith("jobs") and fn.endswith(".jsonl"):
            for j in load_jsonl(os.path.join(d, fn)):
                j["_pass"] = "northeast" if fn == "jobs_ne.jsonl" else ("rest" if fn == "jobs_rest.jsonl" else "all")
                jobs.append(j)

    comp = {}
    for fn in ("companies.jsonl", "companies_ne.jsonl"):
        for c in load_jsonl(os.path.join(d, fn)):
            comp[norm(c["company"]["linkedin_url"])] = dict(c["company"], matched_jobs=c.get("matched_jobs"))
    for r in load_jsonl(os.path.join(d, "companies_rest_enriched.jsonl")):
        body = r["response"]
        c = body.get("company") or body
        if c and c.get("name"):
            comp.setdefault(norm(r["company_linkedin_url"]), dict(c, matched_jobs=None))

    # most recent posting per company = that company's {Open_Role}/{JD}
    by_co = {}
    for j in jobs:
        k = norm(j.get("company_linkedin_url"))
        if k and (k not in by_co or (j.get("date_posted") or "") > (by_co[k].get("date_posted") or "")):
            by_co[k] = j
    njobs = {}
    for j in jobs:
        njobs[norm(j.get("company_linkedin_url"))] = njobs.get(norm(j.get("company_linkedin_url")), 0) + 1

    def hq_state(k):
        c = comp.get(k) or {}
        return ((c.get("hq") or {}).get("state")) or ""

    def is_ne(k):
        s = hq_state(k)
        if s:
            return "yes" if any(n.lower() == s.lower() for n in NORTHEAST_STATES) else "no"
        return "-"

    # jobs csv
    with open(os.path.join(out, f"{date}-jobs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["job_url", "title", "date_posted", "company_name", "company_linkedin_url", "job_city",
                    "job_country", "ai_summary", "pull_pass"])
        for j in sorted(jobs, key=lambda j: j.get("date_posted") or "", reverse=True):
            loc = j.get("location") or {}
            w.writerow([v(j.get("url")), v(j.get("title")), v(j.get("date_posted")), v(j.get("company_name")),
                        v(j.get("company_linkedin_url")), v(loc.get("city")), v(loc.get("country_code")),
                        v(j.get("ai_summary")), j["_pass"]])

    # dedupe sources
    heyreach = set()
    hr_dir = os.path.join(HERE, "security-and-data-bench")
    for fn, limit in (("2026-10-23-2-heyreach-wave1.csv", None), ("2026-10-27-heyreach-wave2.csv", 2100)):
        for i, r in enumerate(csv.DictReader(open(os.path.join(hr_dir, fn)))):
            if limit is None or i < limit:
                heyreach.add(norm(r["linkedin_url"]))
    prior = {}
    earlier = ORDER[:ORDER.index(slug)]
    for p in sorted(glob(os.path.join(HERE, "*", "*-leads.csv"))):
        seg_dir = os.path.basename(os.path.dirname(p))
        older = os.path.basename(p)[:10] < date[:10]  # an earlier snapshot: its live rows are in campaigns now
        if seg_dir in SEGMENTS and not older and (seg_dir == slug or seg_dir not in earlier):
            continue
        tag = f"{seg_dir}/{os.path.basename(p)}"
        for r in csv.DictReader(open(p)):
            if seg_dir in SEGMENTS and r.get("live_eligible") != "yes":
                continue  # only the copy that stays live elsewhere blocks this one
            prior.setdefault(norm(r["linkedin_url"]), set()).add(tag)

    # leads
    leads, seen = [], set()
    co_leads = {}
    for rec in load_jsonl(os.path.join(d, "people.jsonl")):
        k = norm(rec["company_linkedin_url"])
        for res in rec["results"]:
            p = res.get("person") or {}
            u = norm(p.get("linkedin_url"))
            if not u or u in seen:
                continue
            seen.add(u)
            exp = next((e for e in p.get("experiences") or [] if norm(e.get("company_linkedin_url")) == k),
                       (p.get("experiences") or [{}])[0])
            j = by_co.get(k, {})
            c = comp.get(k, {})
            in_hr = "yes" if u in heyreach else "no"
            dup = "; ".join(sorted(prior.get(u, set())))
            leads.append({
                "linkedin_url": p.get("linkedin_url"), "first_name": v(p.get("first_name")),
                "last_name": v(clean_last(p.get("last_name"))), "title": v(exp.get("job_title") or p.get("headline")),
                "waterfall_tier": "1 hiring manager" if res.get("icp") == 1 else "2 talent fallback",
                "company_name": v(c.get("name") or j.get("company_name")),
                "company_linkedin_url": v(rec["company_linkedin_url"]), "open_role": v(j.get("title")),
                "job_url": v(j.get("url")), "job_posted": v((j.get("date_posted") or "")[:10]),
                "jd_summary": v(j.get("ai_summary")), "hq_state": v(hq_state(k)), "northeast": is_ne(k),
                "in_heyreach_list_1056840": in_hr, "dupe_of": v(dup),
                "live_eligible": "yes" if in_hr == "no" and not dup else "no",
            })
            co_leads[k] = co_leads.get(k, 0) + 1
    # Northeast first, then most recent posting
    leads.sort(key=lambda r: r["job_posted"], reverse=True)
    leads.sort(key=lambda r: r["northeast"] != "yes")
    with open(os.path.join(out, f"{date}-leads.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, LEAD_COLS); w.writeheader(); w.writerows(leads)

    # companies csv
    with open(os.path.join(out, f"{date}-companies.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company_linkedin_url", "company_name", "domain", "industry", "size", "revenue_range",
                    "hq_city", "hq_state", "northeast", "jobs_in_snapshot", "open_role", "job_url", "job_posted",
                    "leads_in_snapshot"])
        for k, j in sorted(by_co.items(), key=lambda kv: (is_ne(kv[0]) != "yes", kv[1].get("company_name") or "")):
            c = comp.get(k, {})
            w.writerow([v(j.get("company_linkedin_url")), v(c.get("name") or j.get("company_name")), v(c.get("domain")),
                        v(c.get("industry")), v(c.get("size")), v(c.get("revenue_range")),
                        v((c.get("hq") or {}).get("city")), v(hq_state(k)), is_ne(k), njobs.get(k, 0),
                        v(j.get("title")), v(j.get("url")), v((j.get("date_posted") or "")[:10]), co_leads.get(k, 0)])

    s = {"jobs": len(jobs), "companies": len(by_co), "companies_with_leads": len(co_leads), "leads": len(leads),
         "tier1": sum(r["waterfall_tier"].startswith("1") for r in leads),
         "in_heyreach": sum(r["in_heyreach_list_1056840"] == "yes" for r in leads),
         "dupe_prior": sum(r["dupe_of"] != "-" for r in leads),
         "live_eligible": sum(r["live_eligible"] == "yes" for r in leads),
         "northeast_leads": sum(r["northeast"] == "yes" for r in leads),
         "northeast_companies": sum(is_ne(k) == "yes" for k in by_co),
         "usage": json.load(open(os.path.join(d, "usage.json")))}
    s["records_total"] = sum(s["usage"].values())
    print(json.dumps(s, indent=1))
    json.dump(s, open(os.path.join(d, "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
