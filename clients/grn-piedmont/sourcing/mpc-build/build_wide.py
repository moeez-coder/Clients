"""Write the 2026-11-26 size-expansion wave into the 5 MPC segment folders (Moe: "add 51 - 5000").
Inputs ($RAW): wide-companies.json + wide-leads-raw.csv (pull_wide_leads.py), wide-jd.jsonl (fetch_jds.py),
$PHR/ids.json + out_NN.json + flags_NN.json (Claude sub-agents, Moe's JD-phrase prompt).
Per segment ../mpc-<segment>/:
  2026-11-26-companies.csv     every new company assigned to the segment, size band, leads_launch_set (0 stays in), launch_note
  2026-11-26-jobs.csv          kept postings at those companies (from ../tam/2026-11-26-mpc-wide-jobs.csv)
  2026-11-26-role-phrases.csv  per company with a launch lead: posting, open check, role, JD phrase, open line
  $RAW/wide-leads-built-<segment>.csv -> tools/leads.py normalize -> 2026-11-26-leads.csv
Companies the sub-agents flagged as outside the ICP (flags_NN.json: id -> reason) are kept in the files with
launch_note "removed: <reason>" and their leads are marked removed, so the drop-off is visible.
Usage: RAW=/path PHR=phr-wide python3 build_wide.py"""
import csv, json, os, glob, datetime, collections
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, ".."); RAW = os.environ["RAW"]; D = "2026-11-26"
PHR = os.path.join(RAW, os.environ.get("PHR", "phr-wide"))
from sequence import OPEN_FRESH, OPEN_REPOST
comps = {c["company_linkedin_url"]: c for c in json.load(open(os.path.join(RAW, "wide-companies.json")))}
J = {j["company_linkedin_url"]: j for j in map(json.loads, open(os.path.join(RAW, "wide-jd.jsonl")))}
ids = json.load(open(os.path.join(PHR, "ids.json")))
ph, flag = {}, {}
for f in glob.glob(os.path.join(PHR, "out_*.json")):
    for o in json.load(open(f)): ph[ids[str(o["id"])]] = o
for f in glob.glob(os.path.join(PHR, "flags_*.json")):
    fl = json.load(open(f))
    for k, v in (fl.items() if isinstance(fl, dict) else ((x["id"], x["reason"]) for x in fl)): flag[ids[str(k)]] = "removed: " + v.rstrip(".")
leads = list(csv.DictReader(open(os.path.join(RAW, "wide-leads-raw.csv"))))
jobs = [r for r in csv.DictReader(open(os.path.join(S, "tam", f"{D}-mpc-wide-jobs.csv"))) if r["status"] == "kept"]
tot = collections.Counter()
for seg in sorted({c["segment"] for c in comps.values()}):
    d = os.path.join(S, f"mpc-{seg}"); sc = {u: c for u, c in comps.items() if c["segment"] == seg}; R = {}
    for u in sc:
        if u not in J or u not in ph: continue
        j, p = J[u], ph[u]
        line = OPEN_REPOST.format(month=datetime.date.fromisoformat(j["reposted_since"]).strftime("%B")) if j["reposted_since"] != "-" else OPEN_FRESH
        R[u] = {"company_linkedin_url": u, "company_name": sc[u]["company_name"], "size_band": sc[u]["size_band"], "job_url": j["job_url"],
                "job_posted": j["job_posted"], "posting_open": j["posting_open"], "switched_to_other_posting": j["switched_to_other_posting"],
                "reposted_since": j["reposted_since"], "open_role": j["open_role"], "open_role_clean": p["role"], "jd_phrase": p["phrase"],
                "phrase_source": "full job description" if j["description"] else "Blitz ai_summary", "open_line": line, "launch_note": flag.get(u, "-")}
    L = []
    for l in leads:
        if l["segment"] != seg: continue
        r = R.get(l["company_linkedin_url"]); st = l["status"]
        if st == "launch set":
            if not r: st = "removed: no role phrase"
            elif r["launch_note"] != "-": st = r["launch_note"]
        L.append({**l, "open_role": r["open_role"] if r else "-", "open_role_clean": r["open_role_clean"] if r else "-",
                  "jd_phrase": r["jd_phrase"] if r else "-", "open_line": r["open_line"] if r else "-",
                  "job_url": r["job_url"] if r else sc[l["company_linkedin_url"]]["job_url"], "job_posted": r["job_posted"] if r else "-",
                  "posting_open": r["posting_open"] if r else "-", "status": st})
    per = collections.Counter(l["company_linkedin_url"] for l in L if l["status"] == "launch set")
    cols = ["company_name", "company_linkedin_url", "size_band", "vertical", "open_role", "job_url", "job_posted", "kept_postings", "in_live_campaign"]
    with open(os.path.join(d, f"{D}-companies.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols + ["leads_launch_set", "launch_note"]); w.writeheader()
        for u, c in sorted(sc.items(), key=lambda x: -per.get(x[0], 0)):
            w.writerow({**{k: c[k] for k in cols}, "leads_launch_set": per.get(u, 0), "launch_note": flag.get(u, "-")})
    sj = [r for r in jobs if r["company_linkedin_url"] in sc]
    with open(os.path.join(d, f"{D}-jobs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(sj[0].keys())); w.writeheader(); w.writerows(sj)
    with open(os.path.join(d, f"{D}-role-phrases.csv"), "w", newline="") as f:
        rows = list(R.values()); w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(RAW, f"wide-leads-built-{seg}.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)
    c = collections.Counter(l["status"] for l in L); tot[seg] = c["launch set"]
    print(seg, "companies", len(sc), "w/ launch", len(per), "jobs", len(sj), "phrases", len(R), "leads", len(L), c.most_common(6))
print(dict(tot), sum(tot.values()))
