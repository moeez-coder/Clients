"""Full company TAM for GRN Piedmont from Blitz (General scope), 2026-11-24.

Moe, 2026-11-24: "source out the complete TAM of the clients. firstly using blitz."

Endpoint: Blitz POST /v2/search/companies, cursor-paged at 50 per page, 1 record per company.
Firmographics are the ICP form's, reusing the exact definitions of sourcing/tam/tam_counts.py
(the 2026-11-16 count read), so the pull and that read are comparable:
  - Manufacturing: 69 manufacturing industry labels (sent as two halves, Blitz caps include at 50),
    201-500 + 501-1000 employees, US HQ, HQ state not in the 13 Mountain/Pacific/AK/HI states.
  - Fire & life safety: 8 contractor/security labels + company keyword gate
    (fire protection / fire sprinkler / fire alarm / fire suppression / life safety), same sizes and geo.
Flags (not filters): DNC match by company name, and whether the company is already in the live
Recruitment Specific (MPC) campaign's company files.

Dedupe key: company LinkedIn URL, else domain, else name + HQ city (so records with neither never merge).
Note: the HQ-state exclusion only drops companies whose state is known; hq_state_verified_et_ct says which rows are checked.
Usage: python3 pull_tam_blitz.py   -> 2026-11-24-companies.csv (+ raw/ JSON pages, git-ignored)
       REBUILD=1 python3 pull_tam_blitz.py   rebuilds the CSV from raw/ with no API calls
"""
import csv, datetime, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location("tc", os.path.join(CLIENT, "sourcing/tam/tam_counts.py"))
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)

OUT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "2026-11-24-companies.csv")
assert not os.path.exists(OUT), f"{OUT} exists: snapshots are append-only"
RAW = os.path.join(HERE, "raw"); os.makedirs(RAW, exist_ok=True)


def norm(s):
    s = (s or "").lower()
    s = re.sub(r"\b(inc|llc|ltd|co|corp|corporation|company|the|group|holdings)\b\.?", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


dnc = {norm(r["company_name"]) for r in csv.DictReader(open(os.path.join(CLIENT, "context/dnc-list.csv")))}
mpc = set()
for f in ("2026-11-16-companies.csv", "2026-11-23-companies.csv"):
    for r in csv.DictReader(open(os.path.join(CLIENT, "sourcing/recruitment-specific-open-roles", f))):
        mpc.add((r.get("company_linkedin_url") or "").rstrip("/").lower())

used = 0


def pull(tag, body):
    global used
    if os.environ.get("REBUILD"):  # rebuild the CSV from the saved raw pages, no API calls
        rows, page = [], 0
        while os.path.exists(os.path.join(RAW, f"{tag}-{page:04d}.json")):
            r = json.load(open(os.path.join(RAW, f"{tag}-{page:04d}.json")))
            used += (r.get("fair_usage") or {}).get("records_used", 0)
            rows += r.get("results") or []; page += 1
        print(tag, "rebuilt from raw", len(rows), flush=True)
        return rows
    rows, cursor, page = [], None, 0
    while True:
        b = json.loads(json.dumps(body)); b["max_results"] = 50; b["cursor"] = cursor
        r = tc.post("/v2/search/companies", b)
        if "_error" in r:
            raise SystemExit(f"{tag} page {page}: {r}")
        used += (r.get("fair_usage") or {}).get("records_used", 0)
        res = r.get("results") or []
        json.dump(r, open(os.path.join(RAW, f"{tag}-{page:04d}.json"), "w"))
        rows += res; page += 1
        cursor = r.get("cursor")
        if page % 20 == 0:
            print(tag, page, len(rows), "of", r.get("total_results"), flush=True)
        if not cursor or not res:
            print(tag, "done", len(rows), "total_results said", r.get("total_results"), flush=True)
            return rows


segments = [
    ("mfg-a", "manufacturing", tc.comp_body(tc.MFG[:35])),
    ("mfg-b", "manufacturing", tc.comp_body(tc.MFG[35:])),
    ("fls", "fire-life-safety", tc.comp_body(tc.FLS_IND, tc.FLS_KW)),
]
seen, out = {}, []
for tag, seg, body in segments:
    for x in pull(tag, body):
        key = ((x.get("linkedin_url") or "").rstrip("/").lower() or (x.get("domain") or "").lower()
               or "name:" + norm(x.get("name")) + "|" + norm((x.get("hq") or {}).get("city")))
        if key in seen:
            if seg not in seen[key]["segment"].split(";"):
                seen[key]["segment"] += f";{seg}"
            continue
        hq = x.get("hq") or {}
        row = {
            "company_linkedin_url": x.get("linkedin_url") or "-",
            "company_name": x.get("name") or "-",
            "company_domain": x.get("domain") or "-",
            "segment": seg,
            "industry": x.get("industry") or "-",
            "size": x.get("size") or "-",
            "employees_on_linkedin": x.get("employees_on_linkedin") or "-",
            "revenue_range": x.get("revenue_range") or "-",
            "type": x.get("type") or "-",
            "founded_year": x.get("founded_year") or "-",
            "hq_city": hq.get("city") or "-",
            "hq_state": hq.get("state") or "-",
            "hq_state_verified_et_ct": "yes" if hq.get("state") else "no: Blitz has no HQ state, time zone unchecked",
            "specialties": "; ".join(x.get("specialties") or []) or "-",
            "about": re.sub(r"\s+", " ", (x.get("about") or "-"))[:400],
            "dnc_match": "yes" if norm(x.get("name")) in dnc else "no",
            "in_live_mpc_campaign": "yes" if key in mpc else "no",
            "source_tool": "Blitz POST /v2/search/companies",
            "pulled_on": datetime.date.today().isoformat(),
        }
        seen[key] = row; out.append(row)

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print("rows", len(out), "records used", used)
json.dump({"records_used": used, "rows": len(out)}, open(os.path.join(HERE, "2026-11-24-pull-usage.json"), "w"))
