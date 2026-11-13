"""Gender pay gap signal read for We Are DNA doc 1 revision (2026-11-13).

Source: UK government gender pay gap service, 2025 reporting year (snapshot 2025, filed by April 2026),
https://gender-pay-gap.service.gov.uk/viewing/download-data/2025 (public, free, every GB employer with 250+ staff).
Usage: python3 -I gpg_signal.py <path-to-downloaded-gpg2025.csv>
Writes 2026-11-13-gpg-signal-companies.csv (one row per employer in the five doc-1 sectors) and prints counts.
Sector = any SIC code with the prefixes below. Signal = median hourly gap >= 15%.
"""
import csv, sys, os
SEG = {"1-health-care-vet": ("86", "87", "88", "75"), "2-retail-hospitality": ("47", "55", "56"),
       "3-manufacturing-engineering": ("10", "11", "2", "30", "33"), "4-law-accounting": ("691", "692"),
       "5-financial-services": ("64", "65", "66")}
rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8-sig")))
out = []
for r in rows:
    sics = [s.strip() for s in r["SicCodes"].replace("\n", ",").split(",") if s.strip()]
    segs = [k for k, p in SEG.items() if any(s.startswith(x) for s in sics for x in p)]
    if not segs: continue
    try: med = float(r["DiffMedianHourlyPercent"])
    except ValueError: med = None
    out.append({"employer_name": r["EmployerName"], "company_number": r["CompanyNumber"] or "-", "sic_codes": ";".join(sics),
                "segments": ";".join(segs), "median_gap_pct": med if med is not None else "-",
                "mean_gap_pct": r["DiffMeanHourlyPercent"] or "-", "female_top_quartile_pct": r["FemaleTopQuartile"] or "-",
                "employer_size": r["EmployerSize"] or "-", "filed_late": r["SubmittedAfterTheDeadline"] or "-",
                "gpg_signal_15pct": "yes" if (med is not None and med >= 15) else "no", "gpg_link": r["CompanyLinkToGPGInfo"] or "-"})
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "2026-11-13-gpg-signal-companies.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for k in SEG:
    s = [o for o in out if k in o["segments"].split(";")]
    print(k, "employers:", len(s), "signal (median>=15%):", sum(o["gpg_signal_15pct"] == "yes" for o in s))
print("total rows written:", len(out))
