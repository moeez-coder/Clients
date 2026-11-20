"""Exports the Doc 2 sizing JSON outputs to plain CSVs (CLAUDE.md rule 3a/3b). No API calls."""
import csv, json
from dnc import match
def dncflag(n):
    m = match(n); return "-" if not m else (("review: " if m["review"] else "") + m["dnc_source"])
V = {  # fit verdicts written by hand from name + description, 2026-11-18
 "Neuralink": "noise: device, pre-commercial", "Genetix Biotherapeutics": "fit: marketed gene therapies", "bluebird bio": "fit (duplicate page of Genetix)",
 "Sage Therapeutics": "fit: marketed (Zurzuvae)", "CRISPR Therapeutics": "borderline: Casgevy marketed by Vertex", "nference": "noise: data/AI vendor",
 "PSC Biotech® Corporation": "noise: consulting/services", "Insilico Medicine": "noise: clinical stage", "Servier Pharmaceuticals": "fit: marketed",
 "PhRMA": "noise: trade association", "BlueRock Therapeutics": "noise: clinical stage", "ZO Skin Health, Inc.": "borderline: physician-dispensed skincare",
 "Allogene Therapeutics": "noise: clinical stage", "Deciphera Pharmaceuticals": "fit: marketed (Qinlock)", "Wyss Institute at Harvard University": "noise: research institute",
 "Intercept Pharmaceuticals": "fit: marketed", "Calico Life Sciences": "noise: research", "Altos Labs": "noise: research", "Biosintex Laboratorio": "noise: non-US",
 "Summit Therapeutics, Inc.": "borderline: launch-stage (ivonescimab)", "Moderna": "fit: marketed vaccines", "Precision Medicine Group": "noise: CRO/services (now name-excluded)",
 "Lupin Pharmaceuticals": "fit: marketed brands + generics", "Merz Aesthetics": "fit: HCP aesthetics", "10x Genomics": "noise: research tools (now name-excluded)",
 "Otsuka Pharmaceutical Companies (U.S.)": "fit: marketed", "US Pharmacopeia": "noise: standards body (now name-excluded)", "Adium Argentina": "noise: non-US",
 "Twist Bioscience": "noise: research tools (now name-excluded)", "Legend Biotech": "fit: marketed (Carvykti)",
 "Qure.ai": "borderline: AI imaging software", "InMode": "fit: aesthetic HCPs", "Butterfly Network, Inc.": "fit: point-of-care ultrasound",
 "Anatomage Inc.": "noise: education hardware", "Vive Health": "noise: consumer products", "Kestra Medical Technologies, Inc.": "fit: cardiology",
 "THINK Surgical": "fit: orthopaedic surgeons", "Topcon Healthcare": "fit: eye care", "Synchron": "noise: pre-commercial", "Blackrock Neurotech": "noise: pre-commercial",
 "Accuray": "fit: radiation oncology", "Hydrafacial": "noise: spa/consumer aesthetics", "ATEC Spine": "fit: spine surgeons", "PROCEPT BioRobotics": "fit: urologists",
 "Sol-Millennium Medical Group": "noise: commodity needles/syringes", "Candela Medical": "fit: dermatology", "SCITON": "fit: dermatology/aesthetics",
 "Advanced Bionics": "fit: ENT/audiology", "Heartflow": "fit: cardiology", "Cynosure, LLC.": "fit: dermatology/aesthetics",
}
s = json.load(open("2026-11-18-doc-2-blitz-samples.json"))
with open("2026-11-18-doc-2-fit-sample-companies.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["company_linkedin_url", "company_name", "sample", "employees_on_linkedin", "industry", "domain", "fit_verdict"])
    for k in ["pharma_201_500", "pharma_501_5000", "device_51_200", "device_201_1000"]:
        for x in s[k]["results"]:
            w.writerow([x.get("linkedin_url") or "-", x.get("name"), k, x.get("employees_on_linkedin") or "-", x.get("industry") or "-", x.get("domain") or "-", V.get(x.get("name"), "-")])
c = json.load(open("2026-11-18-doc-2-blitz-counts.json"))
with open("2026-11-18-doc-2-title-samples-leads.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["linkedin_url", "full_name", "job_title", "company_name", "campaign_cell", "source"])
    for k, v in s.items():
        if not k.startswith("people/"): continue
        for x in v["results"]:
            e = (x.get("experiences") or [{}])[0]
            w.writerow([x.get("linkedin_url") or "-", x.get("full_name") or "-", e.get("job_title") or "-", e.get("company_name") or "-", k[7:], "Blitz /v2/search/people"])
    for camp, rows in c.get("resample_after_noise_filter", {}).items():
        for x in rows:
            e = (x.get("experiences") or [{}])[0]
            w.writerow([x.get("linkedin_url") or "-", x.get("full_name") or "-", e.get("job_title") or "-", e.get("company_name") or "-", camp + "/decision_makers (after filter fix)", "Blitz /v2/search/people"])
h = json.load(open("2026-11-18-doc-2-hiring.json"))
with open("2026-11-18-doc-2-hiring-companies.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["company_linkedin_url", "company_name", "campaign", "window", "size", "dnc_or_client"])
    for k, v in h.items():
        if k == "records_used": continue
        camp, win = k.split("/")
        for r in v["rows"]: w.writerow([r["linkedin_url"] or "-", r["name"], camp, win, r["size"] or "-", dncflag(r["name"])])
p = json.load(open("2026-11-18-doc-2-pharma-companies.json"))
with open("2026-11-18-doc-2-persona-companies.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["company_linkedin_url", "company_name", "campaign", "size", "matched_people_us", "dnc_or_client"])
    for k, v in p.items():
        if k == "records_used": continue
        for r in v["rows"]: w.writerow([r["linkedin_url"] or "-", r["name"], k, r["size"] or "-", r["matched_people"], dncflag(r["name"])])
a = json.load(open("2026-11-18-doc-2-agency-companies.json"))
with open("2026-11-18-doc-2-agency-wide-persona-companies.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["company_linkedin_url", "company_name", "persona", "universe_group", "size", "matched_people_us", "health_focused", "dnc_or_client", "about"])
    for k, rows in a.items():
        if k == "records_used": continue
        for r in rows: w.writerow([r["linkedin_url"] or "-", r["name"], k, r["group"], r["size"] or "-", r["people"], "yes" if r["health_text"] else "no", dncflag(r["name"]), r.get("about") or "-"])
L = json.load(open("2026-11-18-doc-2-large-device.json"))
with open("2026-11-18-doc-2-large-device-bu-companies.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["company_linkedin_url", "company_name", "business_unit", "bu_title_weight", "persona_people_company_total", "persona_people_bu_estimate"])
    for k, v in L.items():
        if k == "_meta": continue
        for bu, est in v["bu_persona_est"].items(): w.writerow([";".join(v["linkedin_urls"]), k, bu, v["bu_weight"][bu], v["persona_total"], est])
o = json.load(open("2026-11-18-doc-2-openfda.json"))
with open("2026-11-18-doc-2-fda-drug-approvals.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["application", "date", "month", "kind", "sponsor", "brands", "submission_class"])
    for e in sorted(o["drug_events"], key=lambda e: e["date"]): w.writerow([e["application"], e["date"], e["month"], e["kind"], e["sponsor"], "; ".join(e["brands"]) or "-", e["class"] or "-"])
print("ok")
