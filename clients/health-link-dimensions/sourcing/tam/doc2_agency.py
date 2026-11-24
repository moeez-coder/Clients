"""Doc 2 sizing step 4: agency campaigns 9-12 recounted against the DNC, on (a) the Blitz core universe
(persona_counts.company() + DNC agency names) and (b) the wider universe: DiscoLike 600 lookalike + Blitz core 147,
DNC/clients removed, people counted with Blitz POST /v2/search/people filtered by company linkedin_url (50 per call).
Persona title cells are the same as the 2026-11-18 agency sizing (persona_counts.CELLS). Writes 2026-11-18-doc-2-agency.json."""
import csv, json, re
from persona_counts import CELLS, company, NAME_EXCL
from doc2_common import call
from dnc import match
LVL = {"influencers": None, "decision_makers": None, "advocates": None}
DNC_AGENCY_NAMES = ["CMI Media", "Fingerpaint", "GSW", "Syneos", "Health Monitor", "Hibbert", "InStep Health", "NEON",
                    "Vaniam", "Underscore", "Evolution Health", "Quaintise", "Prairie Dog", "Conexiant", "Weinbach", "Cadent",
                    "Unlock Health", "Alloy Marketing", "MediaSpace", "PDQ Communications", "MKC Strategies", "Doceree", "WebMD",
                    "MJH Life Sciences", "Deerfield Agency", "Matrix Medical Communications", "Paradigm Medical Communications",
                    "Rational 360", "Sensified", "Laughlin Constable", "Power Digital", "LionShare", "Rebellion Group"]
out, used = {"core": {}, "wide": {}}, 0
def cnt(body):
    global used
    r = call("/v2/search/people", body); used += r.get("fair_usage", {}).get("records_used", 0)
    if r.get("_error"): print("ERR", r.get("_body"))
    return r.get("total_results") or 0
# (a) core universe, pre and post DNC
for pn, cells in CELLS.items():
    for ln, (inc, exc, lv) in cells.items():
        p = {"job_title": {"include": inc, "exclude": exc}, "job_level": lv, "location": {"country_code": ["US"]}}
        comp_post = dict(company(), name={"exclude": NAME_EXCL + DNC_AGENCY_NAMES})
        out["core"][f"{pn}/{ln}"] = {"post_dnc": cnt({"company": comp_post, "people": p, "max_results": 1})}
        print("core", pn, ln, out["core"][f"{pn}/{ln}"], flush=True)
out["core_name_exclude"] = NAME_EXCL + DNC_AGENCY_NAMES
# (b) wider universe by linkedin_url
def li(u):
    m = re.search(r"linkedin\.com/company/([^/?#]+)", u or ""); return f"https://www.linkedin.com/company/{m.group(1).lower()}" if m else None
dl = list(csv.DictReader(open("2026-11-18-discolike-agency-lookalike-companies.csv")))
core = list(csv.DictReader(open("2026-11-18-agency-persona-companies.csv")))
seen, groups, removed = set(), {"dl_rank_1_300": [], "dl_rank_301_600": [], "blitz_core_not_in_dl": []}, []
for r in dl:
    u = li(r["company_linkedin_url"]); m = match(r["company_name"])
    if m and not m["review"]: removed.append((r["company_name"], m["dnc_source"])); continue
    if u and u not in seen:
        seen.add(u); groups["dl_rank_1_300" if int(r["rank"]) <= 300 else "dl_rank_301_600"].append(u)
for r in core:
    u = li(r["company_linkedin_url"]); m = match(r["company_name"])
    if m and not m["review"]: removed.append((r["company_name"], m["dnc_source"])); continue
    if u and u not in seen: seen.add(u); groups["blitz_core_not_in_dl"].append(u)
out["wide_groups"] = {k: len(v) for k, v in groups.items()}; out["wide_removed_dnc"] = removed
print(out["wide_groups"], "removed", len(removed))
for g, urls in groups.items():
    for pn, cells in CELLS.items():
        for ln, (inc, exc, lv) in cells.items():
            tot = 0
            for i in range(0, len(urls), 50):
                tot += cnt({"company": {"linkedin_url": urls[i:i+50]}, "people": {"job_title": {"include": inc, "exclude": exc},
                            "job_level": lv, "location": {"country_code": ["US"]}}, "max_results": 1})
            out["wide"][f"{g}/{pn}/{ln}"] = tot
        print(g, pn, {ln: out["wide"][f"{g}/{pn}/{ln}"] for ln in cells}, "used", used, flush=True)
out["records_used"] = used
json.dump(out, open("2026-11-18-doc-2-agency.json", "w"), indent=1)
