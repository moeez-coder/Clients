"""Combine the Blitz + Clay preview rows for Doc 1 Campaigns 1-3 (We Are DNA, 2026-11-23) and pick 1 contact per
company per campaign. Rules: UK-located; title must pass personas.classify (tier 1 before tier 2); in C1 a qualified
'Managing Director, <division>' or 'Managing Director - <unit>' is a divisional MD, not the company head, so removed;
a person is kept in one campaign only (first by C1, C2, C3); rows not picked stay visible as 'spare' or 'removed: <reason>'.
Variables {first_name} {company} {sector_peers} {theme} come from the person row and <date>-companies.csv.
Usage: python3 build_preview.py 2026-11-23 -> <date>-preview-combined-raw.csv (then tools/leads.py normalize)."""
import csv, json, os, re, sys, collections
from urllib.parse import unquote
from personas import classify
HERE = os.path.dirname(os.path.abspath(__file__)); D = sys.argv[1]
def norm(u):
    u = unquote(u or "").split("?")[0].rstrip("/").lower()
    return re.sub(r"https?://([a-z]{2,3}\.)?linkedin\.com", "https://www.linkedin.com", u)
sample = list(csv.DictReader(open(os.path.join(HERE, f"{D}-preview-sample.csv"))))
co = {r["company_linkedin_url"]: r for r in sample}
cand = collections.defaultdict(list)   # (camp, company_li) -> rows
for l in open(os.path.join(HERE, f"{D}-preview-blitz-raw.jsonl")):
    d = json.loads(l)
    for rank, p in enumerate(d["response"].get("results", [])):
        per = p.get("person") or p; exp = (per.get("experiences") or [{}])[0]
        cand[(d["campaign"], d["company_linkedin_url"])].append({"linkedin_url": norm(per.get("linkedin_url")),
            "first_name": per.get("first_name") or "-", "last_name": per.get("last_name") or "-", "job_title": exp.get("job_title") or "-",
            "person_country": ((per.get("location") or {}).get("country_code")) or "-", "source": "blitz", "rank": rank})
clay = json.load(open(os.path.join(HERE, f"{D}-preview-clay-raw.json")))
for call in clay["calls"]:
    camps = ["c1", "c2"] if call["campaign"] == "c1c2" else ["c3"]
    for c in call["contacts"]:
        fn, _, ln = re.sub(r"\(.*?\)", "", c["name"]).strip().partition(" ")
        row = {"linkedin_url": norm(c["url"]), "first_name": fn or "-", "last_name": ln.split(" Assoc")[0].strip() or "-",
               "job_title": c["latest_experience_title"], "person_country": "GB" if ("United Kingdom" in (c["location_name"] or "") or "Area" in (c["location_name"] or "")) else "-",
               "source": "clay", "rank": 9}
        for camp in camps: cand[(camp, c["companyIdentifier"])].append(dict(row))
DIV_MD = re.compile(r"managing director\s*[,\-–|]\s*\w|managing director of (?!the group)", re.I)
out, used = [], {}
for camp in ("c1", "c2", "c3"):
    for li, c in [(r["company_linkedin_url"], r) for r in sample if r["campaign"] == camp]:
        rows, seen = [], {}
        for r in cand[(camp, li)]:   # same person = same LinkedIn URL, or same first + last name at this company (slugs differ by tool)
            k2 = (r["first_name"].lower(), (r["last_name"].split() or ["-"])[0].lower())
            hit = seen.get(r["linkedin_url"]) or seen.get(k2)
            if hit:
                if hit["source"] != r["source"]: hit["source"] = "blitz+clay"
                continue
            seen[r["linkedin_url"]] = r; seen[k2] = r; rows.append(r)
        for r in rows:
            t = classify(camp, r["job_title"])
            if r["person_country"] not in ("GB",): r["status"] = "removed: not UK-based"
            elif t.startswith("removed"): r["status"] = t
            elif camp == "c1" and DIV_MD.search(r["job_title"]): r["status"] = "removed: divisional MD, not the company head"
            elif r["linkedin_url"] in used: r["status"] = f"removed: already in {used[r['linkedin_url']]}"
            else: r["status"] = "candidate"; r["tier"] = t
        mds = [r for r in rows if r["status"] == "candidate" and camp == "c1" and re.fullmatch(r"\s*managing director\s*", r["job_title"], re.I)]
        if len(mds) > 1:   # several plain 'Managing Director's at one firm = a rank title (banks, investment firms), not the company head
            for r in mds: r["status"] = "removed: 'Managing Director' is a rank title here (several at this firm)"
        ok = sorted([r for r in rows if r["status"] == "candidate"], key=lambda r: (r["tier"], r["source"] != "blitz+clay", r["rank"]))
        for i, r in enumerate(ok):
            r["status"] = "launch set" if i == 0 else "spare: 2nd+ contact (1 per company)"
            if i == 0: used[r["linkedin_url"]] = camp
        for r in rows:
            r.setdefault("tier", "-")
            out.append({"campaign": camp, **{k: r[k] for k in ("linkedin_url", "first_name", "last_name", "job_title", "person_country", "source", "tier", "status")},
                "company_name": c["company_name"], "company_domain": c["company_domain"], "company_linkedin_url": li, "company_country": "GB",
                "sector": c["sector"], "size_band": c["size_band"], "sector_peers": c["sector_peers"], "theme": c["theme"], "theme_source": c["theme_source"]})
        if not rows:
            out.append({"campaign": camp, "linkedin_url": "-", "first_name": "-", "last_name": "-", "job_title": "-", "person_country": "-", "source": "-", "tier": "-",
                "status": "no contact found", "company_name": c["company_name"], "company_domain": c["company_domain"], "company_linkedin_url": li,
                "company_country": "GB", "sector": c["sector"], "size_band": c["size_band"], "sector_peers": c["sector_peers"], "theme": c["theme"], "theme_source": c["theme_source"]})
with open(os.path.join(HERE, f"{D}-preview-combined-raw.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for camp in ("c1", "c2", "c3"):
    rs = [r for r in out if r["campaign"] == camp]; ls = [r for r in rs if r["status"] == "launch set"]
    cos_ = len({r["company_linkedin_url"] for r in rs})
    print(camp, "companies", cos_, "with a launch-set contact", len(ls), f"({len(ls)/cos_:.0%})", "tier1", sum(r["tier"] == "1" for r in ls),
          "by source", dict(collections.Counter(r["source"] for r in ls)), "persona-matching contacts/company",
          round(sum(1 for r in rs if r["status"] in ("launch set",) or r["status"].startswith("spare")) / cos_, 2))
print(collections.Counter(r["status"] for r in out))
