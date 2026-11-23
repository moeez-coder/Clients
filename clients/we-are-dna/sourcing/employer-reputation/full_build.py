"""Doc 1 Campaigns 1-3 FULL build (We Are DNA, 2026-11-23): combine Blitz (<date>-blitz-raw.jsonl) and Clay gap-fill
(<date>-clay-raw.json) into one leads file and one companies file per campaign.
Moe's rules after the preview (2026-11-23): every contact matching the accepted persona at each company (no 1-per-company
cap); the same person may be in more than one campaign. Persona = the doc's Persona section:
  C1 CEO/MD/Managing or Senior Partner (tier 1) and COO/CFO (tier 2) -> launch set
  C2 CPO/People or HR Director (tier 1) and Head of People/HR/People and Culture (tier 2) -> launch set
  C3 Head/Director of TA, Resourcing, Recruitment (tier 1) -> launch set; TA/Resourcing/Recruitment Manager or Lead
     (tier 2) -> 'hold: below doc persona (manager/lead)', kept visible for Moe's call.
Removals stay in the file with a reason: not UK, title not the persona, divisional MD, MD rank title, no name.
Same person = same LinkedIn URL or same first + last name at the company. Variables: clean first name and company
(variables.py), sector_peers and theme (from <date>-companies.csv).
Usage: python3 full_build.py 2026-11-23 [--gaps] ; --gaps only writes <date>-clay-gaps.json (companies with no
launch-set contact after Blitz, per campaign, in batches of 10) for the Clay MCP gap-fill."""
import csv, json, os, re, sys, collections
from urllib.parse import unquote
from personas import classify
from variables import first_name, company
HERE = os.path.dirname(os.path.abspath(__file__)); D = sys.argv[1]
def norm(u):
    u = unquote(u or "").split("?")[0].rstrip("/").lower()
    return re.sub(r"https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", u)
cos = [r for r in csv.DictReader(open(os.path.join(HERE, f"{D}-companies.csv"))) if r["excluded"] == "-"]
CAMPS = {"c1": [r for r in cos], "c2": [r for r in cos], "c3": [r for r in cos if r["c3_eligible"] == "yes"]}
cand = collections.defaultdict(list)
for l in open(os.path.join(HERE, f"{D}-blitz-raw.jsonl")):
    d = json.loads(l)
    for rank, p in enumerate(d["response"].get("results", [])):
        per = p.get("person") or p; exp = (per.get("experiences") or [{}])[0]
        cand[(d["campaign"], d["company_linkedin_url"])].append({"linkedin_url": norm(per.get("linkedin_url")),
            "first_name": per.get("first_name") or "-", "last_name": per.get("last_name") or "-", "job_title": exp.get("job_title") or "-",
            "person_country": ((per.get("location") or {}).get("country_code")) or "-", "source": "blitz", "rank": rank})
cp = os.path.join(HERE, f"{D}-clay-raw.json")
if os.path.exists(cp) and "--gaps" not in sys.argv:
    for call in json.load(open(cp))["calls"]:
        camps = ["c1", "c2"] if call["campaign"] == "c1c2" else [call["campaign"]]
        for c in call["contacts"]:
            fn, _, ln = re.sub(r"\(.*?\)", "", c["name"]).strip().partition(" ")
            loc = c.get("location_name") or ""
            row = {"linkedin_url": norm(c["url"]), "first_name": fn or "-", "last_name": ln.strip() or "-", "job_title": c.get("latest_experience_title") or "-",
                   "person_country": "GB" if ("United Kingdom" in loc or loc.endswith(" Area")) else "-", "source": "clay", "rank": 9}
            for camp in camps: cand[(camp, c["companyIdentifier"])].append(dict(row))
DIV_MD = re.compile(r"managing director\s*[,\-–|]\s*\w|managing director of (?!the group)", re.I)
leads = collections.defaultdict(list); comp_rows = collections.defaultdict(list); gaps = collections.defaultdict(list)
for camp, clist in CAMPS.items():
    for c in clist:
        li = c["company_linkedin_url"]; rows, seen = [], {}
        for r in cand[(camp, li)]:
            k2 = (r["first_name"].lower(), (r["last_name"].split() or ["-"])[0].lower())
            hit = seen.get(r["linkedin_url"]) or seen.get(k2)
            if hit:
                if hit["source"] != r["source"]: hit["source"] = "blitz+clay"
                continue
            seen[r["linkedin_url"]] = r; seen[k2] = r; rows.append(r)
        for r in rows:
            t = classify(camp, r["job_title"]); r["tier"] = t if t in ("1", "2") else "-"
            if r["person_country"] != "GB": r["status"] = "removed: not UK-based"
            elif t.startswith("removed"): r["status"] = t
            elif camp == "c1" and DIV_MD.search(r["job_title"]): r["status"] = "removed: divisional MD, not the company head"
            elif r["first_name"] in ("-", "") or r["last_name"] in ("-", ""): r["status"] = "removed: no name"
            elif camp == "c3" and t == "2": r["status"] = "hold: below doc persona (manager/lead)"
            else: r["status"] = "launch set"
        mds = [r for r in rows if r["status"] == "launch set" and camp == "c1" and re.fullmatch(r"\s*managing director\s*", r["job_title"], re.I)]
        if len(mds) > 1 and any(r["status"] == "launch set" and r not in mds for r in rows) or len(mds) > 3:
            for r in mds: r["status"] = "removed: 'Managing Director' is a rank title here (several at this firm)"
        n_ls = sum(r["status"] == "launch set" for r in rows)
        if n_ls == 0: gaps[camp].append(li)
        for r in rows:
            leads[camp].append({"linkedin_url": r["linkedin_url"], "first_name": r["first_name"], "last_name": r["last_name"],
                "full_name": f'{r["first_name"]} {r["last_name"]}'.strip(), "job_title": r["job_title"], "company_name": c["company_name"],
                "company_domain": c["company_domain"], "company_linkedin_url": li, "person_country": r["person_country"], "company_country": "GB",
                "status": r["status"], "tier": r["tier"], "source": r["source"], "sector": c["sector"], "size_band": c["size_band"],
                "clean_first_name": first_name(r["first_name"], f'{r["first_name"]} {r["last_name"]}'), "clean_company": company(c["company_name"]),
                "sector_peers": c["sector_peers"], "theme": c["theme"], "theme_source": c["theme_source"], "campaign": camp})
        comp_rows[camp].append({**{k: c[k] for k in ("company_name", "company_domain", "company_linkedin_url", "sector", "size_band", "glassdoor_name",
            "review_count", "overall_rating", "senior_leadership", "culture_values", "career_opportunities", "work_life_balance", "theme",
            "sector_peers", "shared_glassdoor_employer")}, "clean_company": company(c["company_name"]), "leads_launch_set": n_ls,
            "leads_hold": sum(r["status"].startswith("hold") for r in rows), "contacts_found": len(rows)})
if "--gaps" in sys.argv:
    out = {camp: [g[i:i + 10] for i in range(0, len(g), 10)] for camp, g in gaps.items()}
    json.dump(out, open(os.path.join(HERE, f"{D}-clay-gaps.json"), "w"), indent=1)
    print({k: (len(gaps[k]), len(v)) for k, v in out.items()}); sys.exit()
NAMES = {"c1": "c1-ceo", "c2": "c2-people", "c3": "c3-ta"}
for camp in CAMPS:
    for kind, rows in (("leads-raw", leads[camp]), ("companies", comp_rows[camp])):
        p = os.path.join(HERE, f"{D}-{NAMES[camp]}-{kind}.csv")
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    ls = [r for r in leads[camp] if r["status"] == "launch set"]
    print(camp, "companies", len(comp_rows[camp]), "with launch set", sum(1 for r in comp_rows[camp] if r["leads_launch_set"]),
          "launch-set leads", len(ls), "hold", sum(r["status"].startswith("hold") for r in leads[camp]),
          "by source", dict(collections.Counter(r["source"] for r in ls)))
