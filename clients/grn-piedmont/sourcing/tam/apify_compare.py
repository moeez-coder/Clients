"""Apify job-board signal vs Blitz jobs: coverage test (2026-11-24, approved by Moe).
Input: $APIFY_CSV (GTM Sheets export of table 1a3119fc-23ee-42e3-a466-56c778e5cd3f: actor LzsIpToRTUZSnqjbS, Indeed + LinkedIn,
Charlotte NC 100 mi, hoursOld 168, maxItems 600, cap $5) and 2026-11-24-mpc-segments-jobs.csv (Blitz, 120 days, all statuses).
Writes 2026-11-24-apify-charlotte-jobs.csv (every Apify row + leadership flag + match to Blitz) and prints the comparison.
Company match = normalised name (lowercase, legal suffixes and punctuation stripped). Usage: APIFY_CSV=path python3 apify_compare.py"""
import csv, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "recruitment-specific-open-roles"))
from spec import TITLE_NOISE, COMPANY_NOISE
SUF = r"\b(inc|llc|l l c|lp|ltd|corp|corporation|co|company|incorporated|group|holdings|usa|us|the)\b"
def nm(s): s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower()); s = re.sub(SUF, " ", s); return re.sub(r"\s+", " ", s).strip()
LEAD = re.compile(r"\b(manager|director|vp|vice president|head|chief|president|controller|general manager|plant leader|site leader)\b", re.I)
NOTLEAD = re.compile(r"\b(supervisor|assistant|associate|coordinator|specialist|lead\b|technician|engineer i|sales|account|store|restaurant|project manager)\b", re.I)
rows = [{k.lstrip("﻿"): v for k, v in r.items()} for r in csv.DictReader(open(os.environ["APIFY_CSV"], encoding="utf-8-sig"))]
blitz = list(csv.DictReader(open(os.path.join(HERE, "2026-11-24-mpc-segments-jobs.csv"))))
B_all = {nm(r["company_name"]) for r in blitz}
B_kept = {nm(r["company_name"]) for r in blitz if r["status"] == "kept"}
B_week = {nm(r["company_name"]) for r in blitz if r["date_posted"] >= "2026-11-17"}
SIZE_ICP = {"201 to 500", "501 to 1,000"}
out = []
for r in rows:
    t, c = r["Title"], r["Company"]; n = nm(c)
    lead = bool(LEAD.search(t)) and not NOTLEAD.search(t) and not TITLE_NOISE.search(t) and not COMPANY_NOISE.search(c)
    out.append({**r, "leadership_title": "yes" if lead else "no", "size_in_icp": "yes" if r["Company Size"] in SIZE_ICP else ("unknown" if r["Company Size"] in ("", "Decline to state") else "no"),
                "in_blitz_120d_any": "yes" if n in B_all else "no", "in_blitz_120d_kept": "yes" if n in B_kept else "no", "in_blitz_same_week": "yes" if n in B_week else "no"})
with open(os.path.join(HERE, "2026-11-24-apify-charlotte-jobs.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader()
    for r in out: w.writerow({k: (v if v not in ("", None) else "-") for k, v in r.items()})
L = [r for r in out if r["leadership_title"] == "yes"]
print("apify rows", len(out), "boards", collections.Counter(r["Job Board"] for r in out), "leadership-title rows", len(L))
cos = lambda rs: {nm(r["Company"]) for r in rs}
print("companies all", len(cos(out)), "with a leadership posting", len(cos(L)))
for lab, rs in (("leadership", L),):
    C = cos(rs)
    print(lab, "companies", len(C), "in Blitz 120d (any status)", len(C & B_all), "in Blitz kept", len(C & B_kept), "in Blitz same week", len(C & B_week))
    sz = collections.Counter(r["size_in_icp"] for r in {nm(r["Company"]): r for r in rs}.values()); print(" size (Indeed-stated)", sz)
    icp = {nm(r["Company"]): r for r in rs if r["size_in_icp"] == "yes"}
    print(" ICP-size companies", len(icp), "of which in Blitz kept", len(set(icp) & B_kept), "| by board", collections.Counter(r["Job Board"] for r in icp.values()))
    for k, r in sorted(icp.items()):
        print("   ", "BLITZ" if k in B_kept else ("blitz-removed" if k in B_all else "APIFY-ONLY"), "|", r["Company"][:40], "|", r["Title"][:50], "|", r["Job Board"], "|", r["Location"][:25])
