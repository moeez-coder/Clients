"""MPC segment sizing for GRN Piedmont (2026-11-24, Moe: "create more segments of the MPC campaign, based on the client's ICP").

One fresh 120-day pull of every matching leadership posting, run per VERTICAL (industry-label group) so each posting carries
its industry group (Blitz job results carry no company industry). Then each posting is put in exactly one ROLE FAMILY by
title (precedence below), filtered with the same noise/DNC gates as the live campaign (../recruitment-specific-open-roles/spec.py),
and written to 2026-11-24-mpc-segments-jobs.csv. mpc_segments_size.py turns that file into the segment table.

Blitz API POST /v2/jobs/search, cursor-paged at 50. Same firmographics as the live campaign (../tam/tam_counts.py):
201-1,000 employees, US HQ outside the 13 Mountain/Pacific/AK/HI states, is_agency false, US job location, FULL_TIME.
Raw pages go to $RAW (scratchpad, not committed); request bodies + first-page total_results to 2026-11-24-mpc-segments-pull.json.
Resumable: a (vertical, chunk) with a .done marker is skipped.  Usage: RAW=/path python3 mpc_segments_pull.py
"""
import csv, json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "recruitment-specific-open-roles"))
from tam_counts import MFG, FLS_IND, FLS_KW, FLS_ROLES, jobs_body, post
from spec import TITLE_NOISE, COMPANY_NOISE, FLS_GATE, DNC

RAW = os.environ.get("RAW") or os.path.join(HERE, "raw-mpc"); os.makedirs(RAW, exist_ok=True)
DATE = "2026-11-24"; DAYS = 120

# ---- verticals: every one of the 68 MFG labels in exactly one group (asserted below)
VERT = {
 "food-beverage": ["Animal Feed Manufacturing", "Baked Goods Manufacturing", "Beverage Manufacturing", "Dairy Product Manufacturing",
                   "Food and Beverage Manufacturing", "Food Production", "Fruit and Vegetable Preserves Manufacturing", "Meat Products Manufacturing"],
 "aerospace-defense": ["Aviation and Aerospace Component Manufacturing", "Defense and Space Manufacturing"],
 "plastics-packaging-paper": ["Artificial Rubber and Synthetic Fiber Manufacturing", "Packaging and Containers", "Packaging and Containers Manufacturing",
                   "Plastics", "Plastics and Rubber Product Manufacturing", "Plastics Manufacturing", "Rubber Products Manufacturing",
                   "Paper and Forest Product Manufacturing", "Paper and Forest Products"],
 "metals-fabrication": ["Architectural and Structural Metal Manufacturing", "Boilers; Tanks; and Shipping Container Manufacturing",
                   "Construction Hardware Manufacturing", "Cutlery and Handtool Manufacturing", "Fabricated Metal Products",
                   "Metal Valve; Ball; and Roller Manufacturing", "Primary Metal Manufacturing", "Spring and Wire Product Manufacturing",
                   "Turned Products and Fastener Manufacturing"],
 "chemicals": ["Agricultural Chemical Manufacturing", "Chemical Manufacturing", "Chemical Raw Materials Manufacturing", "Chemicals",
                   "Paint; Coating; and Adhesive Manufacturing", "Soap and Cleaning Product Manufacturing"],
 "machinery-automation": ["Agriculture; Construction; Mining Machinery Manufacturing", "Automation Machinery Manufacturing",
                   "Commercial and Service Industry Machinery Manufacturing", "Engines and Power Transmission Equipment Manufacturing",
                   "HVAC and Refrigeration Equipment Manufacturing", "Industrial Automation", "Industrial Machinery Manufacturing", "Machinery",
                   "Machinery Manufacturing", "Metalworking Machinery Manufacturing"],
 "building-materials": ["Abrasives and Nonmetallic Minerals Manufacturing", "Building Materials", "Clay and Refractory Products Manufacturing",
                   "Glass; Ceramics and Concrete Manufacturing", "Glass Product Manufacturing", "Lime and Gypsum Products Manufacturing",
                   "Wood Product Manufacturing"],
 "electrical-electronics": ["Appliances; Electrical; and Electronics Manufacturing", "Electrical and Electronic Manufacturing",
                   "Electrical Equipment Manufacturing", "Electric Lighting Equipment Manufacturing", "Household Appliance Manufacturing",
                   "Measuring and Control Instrument Manufacturing"],
 "transportation-equipment": ["Motor Vehicle Manufacturing", "Motor Vehicle Parts Manufacturing", "Railroad Equipment Manufacturing",
                   "Railroad Manufacture", "Transportation Equipment Manufacturing"],
 "general-other-mfg": ["Manufacturing", "Mechanical Or Industrial Engineering", "Furniture and Home Furnishings Manufacturing",
                   "Household and Institutional Furniture Manufacturing", "Office Furniture and Fixtures Manufacturing", "Textile Manufacturing"],
}
_all = [l for v in VERT.values() for l in v]
assert sorted(_all) == sorted(MFG) and len(_all) == len(set(_all)), set(MFG) ^ set(_all)

# ---- title keywords (Blitz: every word, whole words, any order, no stemming). Union of all families; local regex assigns one.
H = lambda fams, hs=("Director", "Head", "VP", "Vice President"): [f"{h} {f}" for f in fams for h in hs]
TITLES = sorted(set(
    ["Chief Executive Officer", "CEO", "President", "General Manager", "Chief Operating Officer", "COO", "Chief Financial Officer", "CFO",
     "Chief Human Resources Officer", "CHRO", "Corporate Controller", "Plant Controller", "[Controller]", "Director Finance",
     "Director Human Resources", "HR Director", "Managing Director"]
    + ["Plant Manager", "Plant Director", "Operations Manager", "Production Manager", "Manufacturing Manager", "Site Leader",
       "Continuous Improvement Manager"] + H(["Operations", "Manufacturing", "Production"])
    + ["Engineering Manager", "Quality Manager", "Chief Engineer"] + H(["Engineering", "Quality"])
    + ["Supply Chain Manager", "Purchasing Manager", "Procurement Manager", "Materials Manager", "Sourcing Manager", "Logistics Manager",
       "Planning Manager"] + H(["Supply Chain", "Purchasing", "Procurement", "Logistics"], ("Director", "VP"))
    + ["EHS Manager", "HSE Manager", "Safety Manager", "Maintenance Manager", "Reliability Manager", "Facilities Manager"]
    + H(["EHS", "Safety", "Maintenance"], ("Director",))))
CHUNKS = [TITLES[i:i + 45] for i in range(0, len(TITLES), 45)]

# ---- one family per posting, first match wins
FAMILY = [
 ("executive", re.compile(r"\b(chief|ceo|coo|cfo|chro|cto|president|general manager|managing director|vp|svp|evp|vice president|"
                          r"controller|finance|human resources|hr)\b", re.I)),
 ("ehs-maintenance", re.compile(r"\b(ehs|hse|eh&s|safety|environmental|maintenance|reliability|facilit\w*)\b", re.I)),
 ("supply-chain-purchasing", re.compile(r"\b(supply chain|purchas\w*|procure\w*|materials?|sourcing|logistics|planning)\b", re.I)),
 ("engineering-quality", re.compile(r"\b(engineer\w*|quality)\b", re.I)),
 ("operations-plant", re.compile(r".", re.I)),
]
def family(t): return next(f for f, rx in FAMILY if rx.search(t))
norm = lambda u: re.sub(r"/+$", "", (u or "").split("?")[0]).lower().replace("http://", "https://")

if __name__ == "__main__":
    groups = {v: (labels, None) for v, labels in VERT.items()}; groups["fire-life-safety"] = (FLS_IND, FLS_KW)
    log = json.load(open(os.path.join(HERE, f"{DATE}-mpc-segments-pull.json"))) if os.path.exists(os.path.join(HERE, f"{DATE}-mpc-segments-pull.json")) else {"queries": {}, "records_used": 0}
    for g, (labels, kw) in groups.items():
        # F&LS also gets the live campaign's own F&LS title list (Branch/Service/Project/Inspection Manager etc.), as on 2026-11-16
        for ci, titles in enumerate(CHUNKS + ([FLS_ROLES] if g == "fire-life-safety" else [])):
            key = f"{g}/chunk{ci}"; out = os.path.join(RAW, key.replace("/", "__") + ".jsonl")
            if os.path.exists(out + ".done"): continue
            b = jobs_body(titles, DAYS, labels, kw); b["max_results"] = 50; cur = None; n = 0; tot = None
            with open(out, "w") as f:
                while True:
                    b["cursor"] = cur; r = post("/v2/jobs/search", b)
                    if r.get("_error"): raise SystemExit(f"{key}: {r}")
                    if tot is None: tot = r.get("total_results")
                    log["records_used"] += (r.get("fair_usage") or {}).get("records_used", 0)
                    for x in r.get("results") or []: f.write(json.dumps({**x, "_vertical": g}) + "\n"); n += 1
                    cur = r.get("cursor")
                    if not cur or not r.get("results"): break
            b.pop("cursor", None)
            log["queries"][key] = {"total_results_first_page": tot, "pulled": n, "body": b}
            open(out + ".done", "w").write(str(n)); print(key, tot, n, flush=True)
            json.dump(log, open(os.path.join(HERE, f"{DATE}-mpc-segments-pull.json"), "w"), indent=1)

    # ---- build the postings file
    rows, seen = [], {}
    for p in sorted(os.listdir(RAW)):
        if not p.endswith(".jsonl"): continue
        for line in open(os.path.join(RAW, p)):
            x = json.loads(line); g = x["_vertical"]; t = (x.get("title") or "").strip(); c = x.get("company_name") or ""
            u = norm(x.get("company_linkedin_url")); fam = family(t)
            why = "kept"
            if not u or "/company/" not in u: why = "removed: no company LinkedIn page"
            elif DNC.search(c): why = "removed: client DNC list"
            elif COMPANY_NOISE.search(c): why = "removed: company outside ICP (name)"
            elif TITLE_NOISE.search(t): why = "removed: title not a placed role"
            elif g == "fire-life-safety" and not (FLS_GATE.search(c) or FLS_GATE.search(t)): why = "removed: not fire & life safety"
            k = (x.get("url") or "") or (u, t.lower(), (x.get("date_posted") or "")[:10])
            k2 = (u, t.lower(), (x.get("date_posted") or "")[:10])
            if k in seen or k2 in seen:
                continue  # exact same posting returned by two title chunks: not a row at all
            seen[k] = seen[k2] = 1
            loc = x.get("location") or {}
            rows.append({"segment_vertical": g, "role_family": "fire-life-safety" if g == "fire-life-safety" else fam,
                         "title_family": fam, "title": t or "-", "company_name": c or "-", "company_linkedin_url": u or "-",
                         "job_city": (loc.get("city") if isinstance(loc, dict) else None) or "-",
                         "date_posted": (x.get("date_posted") or "-")[:10], "job_url": x.get("url") or "-",
                         "jd_summary": re.sub(r"\s+", " ", x.get("ai_summary") or "-"), "status": why})
    # repost of the same title at the same company on a later day: keep the oldest date (that is when the vacancy opened)
    rows.sort(key=lambda r: r["date_posted"])
    first = {}
    for r in rows:
        if r["status"] != "kept": continue
        k = (r["company_linkedin_url"], r["title"].lower())
        if k in first: r["status"] = f"removed: repost (first seen {first[k]})"
        else: first[k] = r["date_posted"]
    with open(os.path.join(HERE, f"{DATE}-mpc-segments-jobs.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(len(rows), "postings;", collections.Counter(r["status"].split(" (")[0] for r in rows).most_common())
    print("records used:", log["records_used"])
