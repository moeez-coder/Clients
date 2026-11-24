"""Write the 5 MPC segment folders (2026-11-24) from the raw pull ($RAW: companies.json, leads-raw.csv, jd.jsonl, phr/).
Per segment folder ../mpc-<segment>/:
  2026-11-24-jobs.csv          kept postings at the segment's companies (from ../tam/2026-11-24-mpc-segments-jobs.csv)
  2026-11-24-companies.csv     every company assigned to the segment, with leads_launch_set (0 stays in, drop-off visible)
  2026-11-24-role-phrases.csv  per company with a launch lead: final posting, posting_open, role, JD phrase, open line
  2026-11-24-leads-raw.csv     raw leads + role/phrase columns -> tools/leads.py normalize writes 2026-11-24-leads.csv
Phrases: Moe's prompt (../recruitment-specific-open-roles/jd_phrase_prompt.md), 4 Claude sub-agents, from the full job description.
Usage: RAW=/path python3 build_segments.py"""
import csv, json, os, glob, datetime, collections
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, ".."); RAW = os.environ["RAW"]; D = "2026-11-24"
from sequence import OPEN_FRESH, OPEN_REPOST
# Companies outside the ICP seen while reviewing phrases (launch_note overrides lead status)
OUT = {"big dan": "removed: car wash, not a manufacturer",
       "arnold oil": "removed: fuel distributor, not a manufacturer",
       "dobbs equipment": "removed: equipment dealer, not a manufacturer",
       "continental battery": "removed: role is sales/account management, not a placed role"}
def out_note(c):
    for k, v in OUT.items():
        if k in c["company_linkedin_url"].lower() or k in c["company_name"].lower(): return v
    return "-"
comps = {c["company_linkedin_url"]: c for c in json.load(open(os.path.join(RAW, "companies.json")))}
jd = [json.loads(l) for l in open(os.path.join(RAW, "jd.jsonl"))]; ids = json.load(open(os.path.join(RAW, "phr", "ids.json")))
ph = {}
for f in glob.glob(os.path.join(RAW, "phr", "out_*.json")):
    for o in json.load(open(f)): ph[ids[o["id"]]] = o
J = {r["company_linkedin_url"]: r for r in jd}
leads = list(csv.DictReader(open(os.path.join(RAW, "leads-raw.csv"))))
jobs = [r for r in csv.DictReader(open(os.path.join(S, "tam", f"{D}-mpc-segments-jobs.csv"))) if r["status"] == "kept"]
for seg in sorted({c["segment"] for c in comps.values()}):
    d = os.path.join(S, f"mpc-{seg}"); os.makedirs(d, exist_ok=True)
    sc = {u: c for u, c in comps.items() if c["segment"] == seg}
    rp = []
    for u in sc:
        if u not in J: continue
        j, p, c = J[u], ph[u], sc[u]
        line = OPEN_REPOST.format(month=datetime.date.fromisoformat(j["reposted_since"]).strftime("%B")) if j["reposted_since"] != "-" else OPEN_FRESH
        rp.append({"company_linkedin_url": u, "company_name": c["company_name"], "job_url": j["job_url"], "job_posted": j["job_posted"],
                   "posting_open": j["posting_open"], "switched_to_other_posting": j["switched_to_other_posting"], "reposted_since": j["reposted_since"],
                   "open_role": j["open_role"], "open_role_clean": p["role"], "jd_phrase": p["phrase"],
                   "phrase_source": "full job description" if j["description"] else "Blitz ai_summary", "open_line": line, "launch_note": out_note(c)})
    R = {r["company_linkedin_url"]: r for r in rp}
    L = []
    for l in leads:
        if l["segment"] != seg: continue
        r = R.get(l["company_linkedin_url"])
        st = l["status"]
        if st == "launch set" and r and r["launch_note"] != "-": st = r["launch_note"]
        L.append({**l, "open_role": r["open_role"] if r else "-", "open_role_clean": r["open_role_clean"] if r else "-",
                  "jd_phrase": r["jd_phrase"] if r else "-", "open_line": r["open_line"] if r else "-", "job_url": r["job_url"] if r else sc[l["company_linkedin_url"]]["job_url"],
                  "job_posted": r["job_posted"] if r else "-", "posting_open": r["posting_open"] if r else "-", "status": st})
    per = collections.Counter(l["company_linkedin_url"] for l in L if l["status"] == "launch set")
    with open(os.path.join(d, f"{D}-companies.csv"), "w", newline="") as f:
        cols = ["company_name", "company_linkedin_url", "vertical", "open_role", "job_url", "job_posted", "kept_postings", "in_live_campaign", "leads_launch_set", "launch_note"]
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for u, c in sorted(sc.items(), key=lambda x: -per.get(x[0], 0)):
            w.writerow({**{k: c[k] for k in cols[:8]}, "leads_launch_set": per.get(u, 0), "launch_note": out_note(c)})
    with open(os.path.join(d, f"{D}-jobs.csv"), "w", newline="") as f:
        sj = [r for r in jobs if r["company_linkedin_url"] in sc]; w = csv.DictWriter(f, fieldnames=list(sj[0].keys())); w.writeheader(); w.writerows(sj)
    with open(os.path.join(d, f"{D}-role-phrases.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rp[0].keys())); w.writeheader(); w.writerows(rp)
    with open(os.path.join(RAW, f"leads-raw-{seg}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)
    print(seg, "companies", len(sc), "jobs", len(sj), "phrases", len(rp), "leads", len(L), collections.Counter(l["status"] for l in L).most_common())
