"""Doc 1 C1-3 expansion company list, We Are DNA, 2026-11-25 (Moe's choice: overall < 3.8 OR culture/leadership < 3.6,
on 15+ reviews, high or medium match confidence). Writes ONLY companies not already in 2026-11-23-companies.csv.
Same columns, DNC/Campaign 6 checks and copy variables as build_companies.py (imports its maps), plus `bar` = "x-3.8/3.6".
Usage: python3 build_companies_x.py 2026-11-25 -> <date>-companies.csv"""
import csv, os, sys, collections, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__)); D = sys.argv[1]
OVERALL, SUB, MIN_REVIEWS = 3.8, 3.6, 15
def f(v):
    try: return float(v)
    except: return None
SECTOR_PEERS = {"Health, care, vet": "UK health and care providers", "Retail, hospitality": "retailers and hospitality groups",
    "Manufacturing, engineering": "manufacturers and engineering firms", "Law, accounting": "law and accounting firms",
    "Financial services": "financial services firms"}
THEMES = [("senior_leadership", "communication from leadership"), ("culture_values", "culture and values"),
          ("career_opportunities", "career progression"), ("work_life_balance", "workload and work-life balance")]
import re, difflib
STOP = {"ltd", "limited", "plc", "llp", "group", "uk", "the", "and", "co", "company", "holdings", "international", "services", "b", "corp", "inc"}
def toks(s): return {t for t in re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("&", " ").replace("è", "e")).split() if t not in STOP}
def name_ok(company, gd):
    """Medium matches are name-only, so the names must agree: one token set inside the other (a one-word company name
    must not gain extra words, e.g. Cowshed -> Cowshed Communication), or the joined names >= 0.85 similar (typos)."""
    a, b = toks(company), toks(gd)
    if not a or not b: return False
    if difflib.SequenceMatcher(None, " ".join(sorted(a)), " ".join(sorted(b))).ratio() >= 0.85: return True
    if len(a) == 1 and b != a: return False
    return a <= b or b <= a
def dom(u): return (u or "").lower().replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].strip()
dnc = list(csv.DictReader(open(os.path.join(HERE, "../../context/dnc-list.csv"))))
dnc_dom = {dom(r["company_domain"]) for r in dnc if dom(r["company_domain"]) not in ("", "-")}
dnc_name = {r["company_name"].strip().lower() for r in dnc}
c6 = list(csv.DictReader(open(os.path.join(HERE, "../pe-investment-triggers/2026-11-16-companies-qualified.csv"))))
c6_li = {r["company_linkedin_url"].rstrip("/").lower() for r in c6 if r["company_linkedin_url"] not in ("", "-")}
c6_name = {r["company_name"].strip().lower() for r in c6}
have = {r["company_linkedin_url"].rstrip("/").lower() for r in csv.DictReader(open(os.path.join(HERE, "2026-11-23-companies.csv")))}
out = []; why = collections.Counter()
for r in csv.DictReader(open(os.path.join(HERE, "../glassdoor-bad-reviews/2026-11-17-glassdoor-profiles.csv"))):
    if r["match_confidence"] not in ("high", "medium"): continue
    n = f(r["review_count"]) or 0
    if n < MIN_REVIEWS: why["under 15 reviews"] += 1; continue
    o, cu, sl = f(r["overall_rating"]), f(r["culture_values"]), f(r["senior_leadership"])
    if not ((o is not None and o < OVERALL) or (cu is not None and cu < SUB) or (sl is not None and sl < SUB)): why["above bar"] += 1; continue
    if r["match_confidence"] == "medium" and not name_ok(r["company_name"], r["glassdoor_name"]): why["medium name mismatch"] += 1; continue
    if r["company_linkedin_url"].rstrip("/").lower() in have: why["already in 11-23 list"] += 1; continue
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
        "sector_peers": SECTOR_PEERS[r["sector"]], "excluded": excl, "match_confidence": r["match_confidence"], "bar": "x-3.8/3.6"})
# one Glassdoor employer mapped to several companies: keep only the company whose name matches it exactly; drop the rest
grp = collections.defaultdict(list)
for r in out: grp[r["glassdoor_employer_id"]].append(r)
kept = []
for g in grp.values():
    if len(g) == 1: kept += g; continue
    exact = [r for r in g if toks(r["company_name"]) == toks(r["glassdoor_name"])]
    kept += exact[:1]; why["shared employer dropped"] += len(g) - len(exact[:1])
out = sorted(kept, key=lambda r: r["company_name"].lower())
for r in out: r["shared_glassdoor_employer"] = "no"
with open(os.path.join(HERE, f"{D}-companies.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), dict(why), collections.Counter(r["excluded"] for r in out))
print("confidence", collections.Counter(r["match_confidence"] for r in out), "c3", sum(r["c3_eligible"] == "yes" and r["excluded"] == "-" for r in out))
print(collections.Counter(r["size_band"] for r in out)); print(collections.Counter(r["theme"] for r in out))
print("shared employer rows", sum(r["shared_glassdoor_employer"] == "yes" for r in out))
