"""Write the 2026-11-25 Ops & Plant Director wave (expanding segment mpc-operations-plant).
Inputs ($RAW): dir-leads-raw.csv (pull_directors_ops.py), jd-dir.jsonl + phr2/ (new companies), and the 11-24 role phrases for
companies that already had one. Writes ../mpc-operations-plant/2026-11-25-role-phrases.csv and $RAW/dir-leads-raw-built.csv
(-> tools/leads.py normalize -> ../mpc-operations-plant/2026-11-25-leads.csv).  Usage: RAW=/path python3 build_directors_ops.py"""
import csv, json, os, glob, datetime, collections
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, ".."); RAW = os.environ["RAW"]
from sequence import OPEN_FRESH, OPEN_REPOST
OUT = {}  # companies outside the ICP found while writing phrases: url fragment -> note (filled after review)
if os.path.exists(os.path.join(HERE, "directors_ops_exclusions.json")): OUT = json.load(open(os.path.join(HERE, "directors_ops_exclusions.json")))
old = {r["company_linkedin_url"]: r for r in csv.DictReader(open(os.path.join(S, "mpc-operations-plant", "2026-11-24-role-phrases.csv")))}
jd = [json.loads(l) for l in open(os.path.join(RAW, "jd-dir.jsonl"))]; ids = json.load(open(os.path.join(RAW, "phr2", "ids.json")))
ph = {}
for f in glob.glob(os.path.join(RAW, "phr2", "out_*.json")):
    for o in json.load(open(f)): ph[ids[o["id"]]] = o
comps = {c["company_linkedin_url"]: c for c in csv.DictReader(open(os.path.join(S, "mpc-operations-plant", "2026-11-24-companies.csv")))}
rp = {}
for j in jd:
    u = j["company_linkedin_url"]; p = ph[u]
    line = OPEN_REPOST.format(month=datetime.date.fromisoformat(j["reposted_since"]).strftime("%B")) if j["reposted_since"] != "-" else OPEN_FRESH
    rp[u] = {"company_linkedin_url": u, "company_name": comps[u]["company_name"], "job_url": j["job_url"], "job_posted": j["job_posted"],
             "posting_open": j["posting_open"], "switched_to_other_posting": j["switched_to_other_posting"], "reposted_since": j["reposted_since"],
             "open_role": j["open_role"], "open_role_clean": p["role"], "jd_phrase": p["phrase"],
             "phrase_source": "full job description" if j["description"] else "Blitz ai_summary", "open_line": line,
             "launch_note": next((v for k, v in OUT.items() if k in u), "-")}
for u, r in old.items():
    if u not in rp: rp[u] = {**r, "launch_note": r["launch_note"]}
with open(os.path.join(S, "mpc-operations-plant", "2026-11-25-role-phrases.csv"), "w", newline="") as f:
    rows = list(rp.values()); w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
L = []
for l in csv.DictReader(open(os.path.join(RAW, "dir-leads-raw.csv"))):
    r = rp.get(l["company_linkedin_url"]); st = l["status"]
    if st == "launch set" and (not r or r["launch_note"] != "-"): st = r["launch_note"] if r else "removed: no role phrase"
    L.append({**l, "open_role": r["open_role"] if r else "-", "open_role_clean": r["open_role_clean"] if r else "-", "jd_phrase": r["jd_phrase"] if r else "-",
              "open_line": r["open_line"] if r else "-", "job_url": r["job_url"] if r else "-", "job_posted": r["job_posted"] if r else "-",
              "posting_open": r["posting_open"] if r else "-", "status": st})
with open(os.path.join(RAW, "dir-leads-raw-built.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(L[0].keys())); w.writeheader(); w.writerows(L)
print("phrases", len(rp), "leads", len(L), collections.Counter(x["status"] for x in L).most_common())
