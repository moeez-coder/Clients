"""ClinicalTrials.gov API v2 (free, no key): industry-sponsored Phase 3 trials with at least one US site and a primary
completion date between 2025-11-01 and 2027-06-30. One row per trial, then one row per lead sponsor with DNC/client flags
(dnc.py). Writes 2026-11-19-ctgov-phase3-trials.csv and 2026-11-19-ctgov-phase3-sponsors-companies.csv."""
import csv, json, urllib.request, urllib.parse, collections
from dnc import match
Q = 'AREA[Phase]PHASE3 AND AREA[LeadSponsorClass]INDUSTRY AND AREA[LocationCountry]"United States" AND AREA[PrimaryCompletionDate]RANGE[2025-11-01,2027-06-30]'
F = "NCTId,BriefTitle,LeadSponsorName,Phase,OverallStatus,PrimaryCompletionDate,CompletionDate,Condition,InterventionType,InterventionName,LastUpdatePostDate"
rows, tok = [], None
while True:
    p = {"filter.advanced": Q, "pageSize": "1000", "fields": F, "countTotal": "true"}
    if tok: p["pageToken"] = tok
    r = json.load(urllib.request.urlopen("https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode(p), timeout=120))
    for s in r.get("studies", []):
        ps = s["protocolSection"]; im = ps.get("armsInterventionsModule", {}).get("interventions", [])
        rows.append({"nct_id": ps["identificationModule"]["nctId"], "brief_title": ps["identificationModule"].get("briefTitle", "-"),
            "lead_sponsor": ps["sponsorCollaboratorsModule"]["leadSponsor"]["name"],
            "phase": "/".join(ps.get("designModule", {}).get("phases", [])) or "-",
            "status": ps["statusModule"].get("overallStatus", "-"),
            "primary_completion": ps["statusModule"].get("primaryCompletionDateStruct", {}).get("date", "-"),
            "completion": ps["statusModule"].get("completionDateStruct", {}).get("date", "-"),
            "conditions": "; ".join(ps.get("conditionsModule", {}).get("conditions", [])) or "-",
            "intervention_types": "; ".join(sorted({i.get("type", "") for i in im})) or "-",
            "interventions": "; ".join(dict.fromkeys(i.get("name", "") for i in im)) or "-",
            "last_update": ps["statusModule"].get("lastUpdatePostDateStruct", {}).get("date", "-")})
    tok = r.get("nextPageToken")
    if not tok: break
print("trials", len(rows), "api total", r.get("totalCount"))
rows.sort(key=lambda x: (x["lead_sponsor"].lower(), x["primary_completion"]))
with open("2026-11-19-ctgov-phase3-trials.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["nct_id", "lead_sponsor", "brief_title", "phase", "status", "primary_completion", "completion",
                                      "conditions", "intervention_types", "interventions", "last_update", "dnc_or_client"])
    w.writeheader()
    for x in rows:
        m = match(x["lead_sponsor"]); x["dnc_or_client"] = "-" if not m else (("review: " if m["review"] else "") + m["dnc_source"]); w.writerow(x)
g = collections.defaultdict(list)
for x in rows: g[x["lead_sponsor"]].append(x)
out = []
for sp, ts in g.items():
    types = sorted({t for x in ts for t in x["intervention_types"].split("; ") if t and t != "-"})
    out.append({"sponsor_name": sp, "phase3_trials": len(ts),
        "next_primary_completion": min(x["primary_completion"] for x in ts), "last_primary_completion": max(x["primary_completion"] for x in ts),
        "drug_or_biologic": "yes" if {"DRUG", "BIOLOGICAL"} & set(types) else "no", "intervention_types": "; ".join(types) or "-",
        "conditions_sample": "; ".join(list(dict.fromkeys(c for x in ts for c in x["conditions"].split("; ")))[:6]),
        "interventions_sample": "; ".join(list(dict.fromkeys(i for x in ts for i in x["interventions"].split("; ")))[:6]),
        "nct_ids": "; ".join(x["nct_id"] for x in ts), "dnc_or_client": ts[0]["dnc_or_client"]})
out.sort(key=lambda x: (-x["phase3_trials"], x["sponsor_name"].lower()))
with open("2026-11-19-ctgov-phase3-sponsors-companies.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
print("sponsors", len(out), "dnc/client flagged", sum(1 for x in out if x["dnc_or_client"] != "-"),
      "drug/biologic", sum(1 for x in out if x["drug_or_biologic"] == "yes"))
