"""Fold Haiku qualification verdicts into a new dated snapshot (the source snapshot is never edited).

Usage: python3 merge_qualification.py <qual_out_dir> <src_date> <new_prefix>
  e.g. python3 merge_qualification.py $S/qual/out 2026-10-23 2026-10-23-2
Writes <new_prefix>-leads.csv (all leads + company/lead verdicts + reasons, linkedin_url first) and
<new_prefix>-companies.csv (the 4,618 lead-bearing companies + verdict + reason). Aborts if any
company or lead from the source is missing a verdict.
"""
import csv, glob, json, sys
from collections import Counter

out_dir, src, new = sys.argv[1:4]
cv, lv = {}, {}
for p in sorted(glob.glob(f"{out_dir}/batch_*.jsonl")):
    for line in open(p):
        line = line.strip()
        if not line or line.startswith("```"):
            continue
        r = json.loads(line)
        cv[r["company_linkedin_url"]] = (r["company_verdict"], r.get("company_reason", "").strip() or "-")
        for x in r.get("leads") or []:
            lv[x["linkedin_url"]] = (x["lead_verdict"], x.get("lead_reason", "").strip() or "-")

leads = list(csv.DictReader(open(f"{src}-leads.csv")))
missing = [r["linkedin_url"] for r in leads if r["linkedin_url"] not in lv or r["company_linkedin_url"] not in cv]
if missing:
    sys.exit(f"ABORT: {len(missing)} leads without a verdict, e.g. {missing[:3]}")

rows = []
for r in leads:
    c, l = cv[r["company_linkedin_url"]], lv[r["linkedin_url"]]
    lead_ok = l[0] == "QUALIFIED" and c[0] == "QUALIFIED"   # a lead never outranks its company
    rows.append(dict(r, company_verdict=c[0], company_reason=c[1],
                     lead_verdict="QUALIFIED" if lead_ok else "NOT_QUALIFIED",
                     lead_reason=l[1] if c[0] == "QUALIFIED" else "company not qualified"))
# re-rank within company among QUALIFIED leads only, so the cap applies to the people we'd actually send to
by = {}
for r in rows:
    by.setdefault(r["company_linkedin_url"], []).append(r)
for k, rs in by.items():
    q = [r for r in rs if r["lead_verdict"] == "QUALIFIED"]
    q.sort(key=lambda r: int(r["company_rank"]))
    for i, r in enumerate(q, 1):
        r["qualified_rank"] = i
        r["within_company_cap"] = "yes" if i <= 3 else "no"
    for r in rs:
        if r["lead_verdict"] != "QUALIFIED":
            r["qualified_rank"] = "-"
            r["within_company_cap"] = "-"
cols = list(rows[0].keys())
with open(f"{new}-leads.csv", "w", newline="") as f:
    w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)

cos = [c for c in csv.DictReader(open(f"{src}-companies.csv")) if c["company_linkedin_url"] in by]
with open(f"{new}-companies.csv", "w", newline="") as f:
    ccols = list(cos[0].keys()) + ["company_verdict", "company_reason", "qualified_leads"]
    w = csv.DictWriter(f, ccols); w.writeheader()
    for c in cos:
        k = c["company_linkedin_url"]
        w.writerow(dict(c, company_verdict=cv[k][0], company_reason=cv[k][1],
                        qualified_leads=sum(r["lead_verdict"] == "QUALIFIED" for r in by[k])))
ql = [r for r in rows if r["lead_verdict"] == "QUALIFIED"]
print(json.dumps({
    "companies": len(cos), "companies_qualified": sum(cv[c["company_linkedin_url"]][0] == "QUALIFIED" for c in cos),
    "leads": len(rows), "leads_qualified": len(ql), "qualified_within_cap": sum(r["within_company_cap"] == "yes" for r in ql),
    "qualified_by_role": dict(Counter(r["persona_role"] for r in ql)),
    "top_company_nq_reasons": Counter(cv[c["company_linkedin_url"]][1] for c in cos if cv[c["company_linkedin_url"]][0] != "QUALIFIED").most_common(5),
}, indent=1))
