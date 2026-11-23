"""Doc 1 Campaigns 1-3 (Employer Reputation) company list, We Are DNA, 2026-11-23.
Input: ../glassdoor-bad-reviews/2026-11-17-glassdoor-profiles.csv. Keeps match_confidence=high AND passes_profile_bar=yes
(1,384), re-checks DNC (../../context/dnc-list.csv, domain + exact name) and Campaign 6 (../pe-investment-triggers/
2026-11-16-companies-qualified.csv, company LinkedIn + exact name), and adds the copy variables:
  sector_peers: neutral plural per sector (SECTOR_PEERS below)
  theme: the company's weakest Glassdoor sub-rating among senior leadership, culture and values, career opportunities,
         work-life balance (compensation is never a theme). Ties go in that order. Mapped to the doc's theme words.
  c3_eligible: yes for 201+ staff (Campaign 3 uses only these).
Usage: python3 build_companies.py 2026-11-23  -> <date>-companies.csv"""
import csv, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); D = sys.argv[1]
SECTOR_PEERS = {"Health, care, vet": "UK health and care providers", "Retail, hospitality": "retailers and hospitality groups",
    "Manufacturing, engineering": "manufacturers and engineering firms", "Law, accounting": "law and accounting firms",
    "Financial services": "financial services firms"}
THEMES = [("senior_leadership", "communication from leadership"), ("culture_values", "culture and values"),
          ("career_opportunities", "career progression"), ("work_life_balance", "workload and work-life balance")]
def dom(u): return (u or "").lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].strip()
dnc = list(csv.DictReader(open(os.path.join(HERE, "../../context/dnc-list.csv"))))
dnc_dom = {dom(r["company_domain"]) for r in dnc if dom(r["company_domain"]) not in ("", "-")}
dnc_name = {r["company_name"].strip().lower() for r in dnc}
c6 = list(csv.DictReader(open(os.path.join(HERE, "../pe-investment-triggers/2026-11-16-companies-qualified.csv"))))
c6_li = {r["company_linkedin_url"].rstrip("/").lower() for r in c6 if r["company_linkedin_url"] not in ("", "-")}
c6_name = {r["company_name"].strip().lower() for r in c6}
out = []
for r in csv.DictReader(open(os.path.join(HERE, "../glassdoor-bad-reviews/2026-11-17-glassdoor-profiles.csv"))):
    if r["match_confidence"] != "high" or r["passes_profile_bar"] != "yes": continue
    scores = [(float(r[k]), k, t) for k, t in THEMES if r[k] not in ("", "-")]
    best = min(scores, key=lambda s: (s[0], [k for k, _ in THEMES].index(s[1]))) if scores else None
    excl = "-"
    if dom(r["blitz_domain"]) in dnc_dom or r["company_name"].strip().lower() in dnc_name: excl = "DNC"
    elif r["company_linkedin_url"].rstrip("/").lower() in c6_li or r["company_name"].strip().lower() in c6_name: excl = "Campaign 6"
    out.append({"company_name": r["company_name"], "company_domain": r["blitz_domain"], "company_linkedin_url": r["company_linkedin_url"],
        "sector": r["sector"], "size_band": r["size_band"], "c3_eligible": "no" if r["size_band"] == "51-200" else "yes",
        "glassdoor_name": r["glassdoor_name"], "glassdoor_employer_id": r["selected_employer_id"], "review_count": r["review_count"],
        "overall_rating": r["overall_rating"], "senior_leadership": r["senior_leadership"], "culture_values": r["culture_values"],
        "career_opportunities": r["career_opportunities"], "work_life_balance": r["work_life_balance"],
        "theme_source": best[1] if best else "-", "theme": best[2] if best else "-",
        "sector_peers": SECTOR_PEERS[r["sector"]], "excluded": excl})
dup = collections.Counter(r["glassdoor_employer_id"] for r in out)
for r in out: r["shared_glassdoor_employer"] = "yes" if dup[r["glassdoor_employer_id"]] > 1 else "no"
with open(os.path.join(HERE, f"{D}-companies.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), collections.Counter(r["excluded"] for r in out), "c3", sum(r["c3_eligible"] == "yes" for r in out))
print(collections.Counter(r["theme"] for r in out)); print("shared employer rows", sum(r["shared_glassdoor_employer"] == "yes" for r in out))
