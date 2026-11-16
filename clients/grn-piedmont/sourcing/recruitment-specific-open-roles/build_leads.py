"""Step 4: flatten raw/people.jsonl into a raw leads CSV for tools/leads.py normalize, and write <date>-companies.csv.
Usage: python3 build_leads.py   (then normalize + overlap, see <date>-leads.query.md)"""
import csv, json, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); DATE = "2026-11-16"
comps = {c["company_linkedin_url"]: c for c in json.load(open(os.path.join(HERE, "raw", "companies.json")))}
PERSONA = re.compile(r"\b(chief|ceo|coo|cfo|cto|chro|cpo|president|owner|founder|vp|svp|evp|avp|vice[- ]president|v\.p\.|partner|principal|chairman)\b", re.I)
OFF = re.compile(r"\b(business development|marketing|product owner|account|franchise|commercial|customer|"
                 r"technology|information|digital|legal|counsel|communications|strategy|revenue|"
                 r"assistant|asst|associate|retired|former)\b", re.I)
SUFFIX = re.compile(r",.*$|\s+(MBA|PMP|CPA|PE|P\.E\.|PhD|Ph\.D\.|SHRM-\w+|SPHR|CSCP|Jr\.?|Sr\.?|II|III)$", re.I)

def first_clean(n):
    n = re.sub(r"\(.*?\)|\".*?\"", "", n or "").split(",")[0].strip()
    n = re.sub(r"\s+[A-Z]\.?$", "", n).strip()
    return n.split(" ")[0].title() if n.isupper() or n.islower() else n.split(" ")[0]

rows, per = [], collections.Counter()
for line in open(os.path.join(HERE, "raw", "people.jsonl")):
    r = json.loads(line); c = comps[r["company_linkedin_url"]]
    for p in r["results"]:
        q = p["person"]; exp = (q.get("experiences") or [{}])[0]
        title = exp.get("job_title") or (q.get("headline") or "").split(" | @")[0] or "-"
        loc = q.get("location") or {}
        status = "launch set"
        if not q.get("linkedin_url"): status = "removed: no LinkedIn URL"
        elif not PERSONA.search(title): status = "removed: title outside persona"
        elif OFF.search(title) and p.get("icp") != 1: status = "removed: title outside persona"
        last = SUFFIX.sub("", q.get("last_name") or "").strip()
        rows.append({"linkedin_url": q.get("linkedin_url") or "-", "first_name": q.get("first_name") or "-", "last_name": last or "-",
                     "full_name": q.get("full_name") or "-", "job_title": title, "company_name": c["company_name"],
                     "company_linkedin_url": c["company_linkedin_url"], "person_country": loc.get("country_code") or "-",
                     "company_country": "US", "first_name_clean": first_clean(q.get("first_name")) or "-",
                     "waterfall_tier": p.get("icp", "-"), "role_family": c["role_family"], "open_role": c["open_role"],
                     "job_url": c["job_url"], "job_posted": c["job_posted"], "jd_summary": c["jd_summary"],
                     "person_state": loc.get("state_code") or "-", "status": status})
        if status == "launch set": per[c["company_linkedin_url"]] += 1
with open(os.path.join(HERE, "raw", "leads-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(HERE, f"{DATE}-companies.csv"), "w", newline="") as f:
    cols = ["company_name", "company_linkedin_url", "role_family", "open_role", "job_posted", "job_url", "kept_postings", "role_families", "leads_launch_set"]
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for u, c in comps.items():
        w.writerow({**{k: c[k] for k in cols[:7]}, "role_families": "; ".join(c["role_families"]), "leads_launch_set": per.get(u, 0)})
st = collections.Counter(r["status"] for r in rows)
print(len(rows), st, "companies with >=1 launch lead:", len(per), "of", len(comps))
import random; random.seed(3); rem = [r for r in rows if r["status"] != "launch set"]
for r in random.sample([r for r in rows if r["status"] == "launch set"], 40): print(r["waterfall_tier"], "|", r["job_title"][:60], "|", r["company_name"][:30])
print("-- removed")
for r in rem[:25]: print(r["waterfall_tier"], "|", r["job_title"][:60])
