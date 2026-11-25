"""Doc 1 C1-3 expansion, snapshot 2026-11-25 (We Are DNA). Moe's choices 2026-11-25:
  1. Companies: bar widened to overall < 3.8 OR culture/leadership < 3.6 on 15+ reviews (2026-11-25-companies.csv, built by
     build_companies_x.py; leads for them built by full_build.py 2026-11-25 --widen --out new).
  2. C3 "Add TA Partner/Specialist titles": tier 3 (personas.classify_widen c3) applied to (a) snapshot 3's C3 rows removed only
     for their title and (b) the C3 widen Blitz pull on snapshot-3 C3 companies with no TA lead (2026-11-25-widen-blitz-raw.jsonl).
  3. C3 "People-leader fallback": at every C3 company (201+) still without a launch-set TA lead after 2, the company's C2
     launch-set people leaders go into C3 too (status 'launch set', tier 'F', source 'c2-fallback'). They also stay in C2.
Writes 2026-11-25-<camp>-leads-raw.csv and -companies.csv = snapshot 3 + the new companies (+ C3 extras). Then run
tools/leads.py normalize per campaign. Usage: python3 expand_build.py"""
import csv, json, os, re, collections
from urllib.parse import unquote
from personas import classify_widen
from variables import first_name, company
HERE = os.path.dirname(os.path.abspath(__file__)); OLD, NEW, OUT = "2026-11-23-3", "2026-11-25-new", "2026-11-25"
N = {"c1": "c1-ceo", "c2": "c2-people", "c3": "c3-ta"}
def rd(p): return list(csv.DictReader(open(os.path.join(HERE, p))))
def norm(u):
    u = unquote(u or "").split("?")[0].rstrip("/").lower()
    return re.sub(r"https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", u)
raw = {c: rd(f"{OLD}-{n}-leads-raw.csv") + rd(f"{NEW}-{n}-leads-raw.csv") for c, n in N.items()}
cos = {c: rd(f"{OLD}-{n}-companies.csv") + rd(f"{NEW}-{n}-companies.csv") for c, n in N.items()}
info = {r["company_linkedin_url"]: r for r in rd("2026-11-23-companies.csv") + rd("2026-11-25-companies.csv")}
# 2a: snapshot-3 C3 rows removed for title only -> tier 3 if TA partner/specialist/adviser
re_tagged = 0
for r in raw["c3"]:
    if r["status"].startswith("removed: title not the persona") and r["person_country"] == "GB" and r["first_name"] not in ("-", "") \
            and classify_widen("c3", r["job_title"], r["sector"], r["size_band"]) == "3":
        r["status"], r["tier"] = "launch set", "3"; re_tagged += 1
# 2b: C3 widen pull on snapshot-3 C3 companies
old_c3 = {c["company_linkedin_url"] for c in rd(f"{OLD}-c3-ta-companies.csv")}
seen = collections.defaultdict(set)
for r in raw["c3"]:
    seen[r["company_linkedin_url"]] |= {r["linkedin_url"], (r["first_name"].lower(), (r["last_name"].split() or ["-"])[0].lower())}
C6 = {norm(r["linkedin_url"]) for r in csv.DictReader(open(os.path.join(HERE, "../pe-investment-triggers/2026-11-16-3-leads.csv")))}
def mk(camp, c, p, status, tier, source):
    return {"linkedin_url": p["linkedin_url"], "first_name": p["first_name"], "last_name": p["last_name"],
        "full_name": f'{p["first_name"]} {p["last_name"]}'.strip(), "job_title": p["job_title"], "company_name": c["company_name"],
        "company_domain": c["company_domain"], "company_linkedin_url": c["company_linkedin_url"], "person_country": p["person_country"],
        "company_country": "GB", "status": status, "tier": tier, "source": source, "sector": c["sector"], "size_band": c["size_band"],
        "clean_first_name": first_name(p["first_name"], f'{p["first_name"]} {p["last_name"]}'), "clean_company": company(c["company_name"]),
        "sector_peers": c["sector_peers"], "theme": c["theme"], "theme_source": c["theme_source"], "campaign": camp}
widen_added = 0
for l in open(os.path.join(HERE, "2026-11-25-widen-blitz-raw.jsonl")):
    d = json.loads(l)
    if d["campaign"] != "c3" or d["company_linkedin_url"] not in old_c3: continue
    c = info[d["company_linkedin_url"]]
    for p in d["response"].get("results", []):
        per = p.get("person") or p; exp = (per.get("experiences") or [{}])[0]
        q = {"linkedin_url": norm(per.get("linkedin_url")), "first_name": per.get("first_name") or "-", "last_name": per.get("last_name") or "-",
             "job_title": exp.get("job_title") or "-", "person_country": ((per.get("location") or {}).get("country_code")) or "-"}
        k2 = (q["first_name"].lower(), (q["last_name"].split() or ["-"])[0].lower())
        if q["linkedin_url"] in seen[c["company_linkedin_url"]] or k2 in seen[c["company_linkedin_url"]]: continue
        seen[c["company_linkedin_url"]] |= {q["linkedin_url"], k2}
        t = classify_widen("c3", q["job_title"], c["sector"], c["size_band"])
        st = ("removed: not UK-based" if q["person_country"] != "GB" else "removed: title not the persona" if t != "3"
              else "removed: no name" if "-" in (q["first_name"], q["last_name"]) else "hold: also in Campaign 6 (PE investment) lead list"
              if q["linkedin_url"] in C6 else "launch set")
        raw["c3"].append(mk("c3", c, q, st, t or "-", "blitz-widen")); widen_added += st == "launch set"
# 3: people-leader fallback at C3 companies with no launch-set TA lead
has_ta = {r["company_linkedin_url"] for r in raw["c3"] if r["status"] == "launch set"}
c3_cos = {c["company_linkedin_url"] for c in cos["c3"]}
fb = 0
for r in raw["c2"]:
    if r["status"] == "launch set" and r["company_linkedin_url"] in c3_cos and r["company_linkedin_url"] not in has_ta:
        raw["c3"].append({**r, "tier": "F", "source": "c2-fallback", "campaign": "c3"}); fb += 1
# name check (2026-11-25, after 'Recruitment Twentythreepointfivedegrees' and 'Internal Recruiter' reached HeyReach): a company
# account, a one-letter first name or a non-Latin name can't take "Hi {first name}", so the row is removed, not launched
ACCOUNT = re.compile(r"\b(recruit\w*|talent|careers?|hiring|jobs|hr|people|team|internal|human resources|ltd|limited|hotels?)\b", re.I)
ACCOUNT_LN = re.compile(r"\b(recruit\w*|talent|careers?|hiring|ltd|limited|hotels?)\b", re.I)   # not hr/people: "Bernie Warren, HR Ninja"
bad_name = collections.Counter()
for c in N:
    for r in raw[c]:
        if r["status"] != "launch set": continue
        fn, ln = r["first_name"].strip(), r["last_name"].strip()
        why = ("company account, not a person" if ACCOUNT.search(fn) or ACCOUNT_LN.search(ln) or fn.lower() in ("the", "internal") else
               "first name is an initial" if len(re.sub(r"[^A-Za-z]", "", r["clean_first_name"])) < 2 else
               "name not in Latin script" if not re.search(r"[A-Za-z]", fn) else None)
        if why: r["status"] = f"removed: {why}"; bad_name[(c, why)] += 1
print("name check", dict(bad_name))
for c, n in N.items():
    cnt = collections.Counter(r["company_linkedin_url"] for r in raw[c] if r["status"] == "launch set")
    for r in cos[c]: r["leads_launch_set"] = cnt[r["company_linkedin_url"]]
    for kind, rows in (("leads-raw", raw[c]), ("companies", cos[c])):
        p = os.path.join(HERE, f"{OUT}-{n}-{kind}.csv"); assert not os.path.exists(p), f"append-only: {p} exists"
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    print(c, "companies", len(cos[c]), "with lead", sum(1 for r in cos[c] if cnt[r["company_linkedin_url"]]), "launch set", sum(cnt.values()))
print("c3 extras: re-tagged", re_tagged, "widen", widen_added, "fallback", fb)
