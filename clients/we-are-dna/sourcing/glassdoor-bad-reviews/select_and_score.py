"""Glassdoor profile lookup (We Are DNA), 2026-11-17 preview: pick one Glassdoor employer per search query
and apply the profile-level "bad reviews" bar. Stdlib only; run with `python -I select_and_score.py`.

Inputs (same folder):
  2026-11-17-preview-lookup-raw.json  list of kaix/glassdoor-company-scraper objects (non-compact,
                                      includeRatings on); each carries `inputSource` = the search query.
  2026-11-17-companies.csv            Blitz companies; joined to queries by exact company_name.
Output:
  2026-11-17-preview-lookup.csv       one row per query, "-" for empty.

Selection rule, per query:
  1. Pool = candidates whose HQ is in the United Kingdom. If none are UK, pool = all candidates
     (the pick is then at best "low" confidence).
  2. Prefer a candidate whose website host (minus www.) equals the Blitz company_domain.
  3. Else the best name match: names normalised (case, punctuation, Ltd/Limited/plc/UK/Group and a few
     generic words dropped) and compared on token overlap; at least one shared token is required.
  4. Ties are broken on the highest reviewCount.
match_confidence:
  high   = domain match, or strong name match with UK HQ and 30+ reviews
  medium = strong name match with UK HQ and under 30 reviews
  low    = anything else (non-UK HQ, weak name overlap)
  none   = no candidate returned
A "strong" name match means the normalised names are equal or one's tokens contain the other's.
"""
import csv, json, os, re, sys
from collections import OrderedDict
from urllib.parse import urlparse

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "2026-11-17-preview-lookup-raw.json")
COMPANIES = os.path.join(HERE, "2026-11-17-companies.csv")
OUT = os.path.join(HERE, "2026-11-17-preview-lookup.csv")

QUERIES = [  # in submission order; the next run (4,677 companies) can derive this from the companies CSV
    "Tempus Services", "Almondine", "European LifeCare Group", "The Endeavour Partnership now Ward Hadaway",
    "Karali Limited", "chaiiwala", "Tesco Marketplace", "SJD Accountancy", "Noble Foods Ltd", "Vesuvius",
    "Billington Foods", "Research at Leicester's Hospitals", "RBS ACCOUNTANTS LTD",
    "Hyatt Regency London – The Churchill", "GAIL's", "British Airways Pensions", "Giraffe World Kitchen",
    "Claridge's", "Pro Formula Uk & Ire", "United Response", "Scottish Autism", "Kinnerton Confectionery",
    "Russell & Bromley", "Vicky Modlin", "PFM UK",
]

MIN_REVIEWS = 30          # below this a profile is too thin to judge
BAR_OVERALL = 3.5         # bar_rating: overall < this
BAR_SUBRATING = 3.3       # bar_subrating: culture_values or senior_leadership < this

# Words dropped before comparing names: legal suffixes, "UK", "Group" and similar non-distinctive words.
NAME_NOISE = {"ltd", "limited", "plc", "uk", "group", "the", "and", "co", "company", "inc", "llc", "holdings"}

# Output column -> key in the scraper's `ratings` object. Star ratings are 1-5 (0 = not rated);
# ceoRating and recommendToFriendRating are 0-1 shares.
STAR_RATINGS = OrderedDict([
    ("overall_rating", "overallRating"),
    ("culture_values", "cultureAndValuesRating"),
    ("senior_leadership", "seniorManagementRating"),
    ("career_opportunities", "careerOpportunitiesRating"),
    ("work_life_balance", "workLifeBalanceRating"),
    ("comp_benefits", "compensationAndBenefitsRating"),
    ("diversity_inclusion", "diversityAndInclusionRating"),
])
SHARE_RATINGS = OrderedDict([("ceo_approval", "ceoRating"), ("recommend_to_friend", "recommendToFriendRating")])


# ---------- helpers ----------
def is_uk(hq):
    return bool(hq) and hq.strip().lower().endswith("united kingdom")

def host(url):
    if not url or url == "-":
        return ""
    if "//" not in url:
        url = "//" + url
    h = (urlparse(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h

def name_tokens(name):
    s = (name or "").lower().replace("’", "'").replace("&", " and ")
    s = re.sub(r"'s\b", "s", s)              # GAIL's -> gails
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return {t for t in s.split() if t not in NAME_NOISE}

def name_match(query, candidate_name):
    """Returns 'strong', 'weak' or None, plus a score for ranking (Jaccard of tokens)."""
    q, c = name_tokens(query), name_tokens(candidate_name)
    shared = q & c
    if not shared:
        return None, 0.0
    score = len(shared) / len(q | c)
    strength = "strong" if (q == c or q <= c or c <= q) else "weak"
    return strength, score

def reviews(obj):
    return obj.get("reviewCount") or 0

def star(v):
    return "-" if v in (None, 0, "") else f"{float(v):.1f}"

def share(v):
    return "-" if v is None else f"{float(v):.2f}"

def yn(b):
    return "yes" if b else "no"

def num(s):
    return None if s == "-" else float(s)


# ---------- selection ----------
def select(query, blitz_domain, candidates):
    """Pick one candidate for the query. Returns (candidate or None, match_confidence).

    Rule v2 (2026-11-17, after the 25-company preview): a candidate qualifies if its website host
    equals the Blitz domain OR its name shares tokens with the query. Among qualifying candidates,
    UK-HQ ones win, then the MOST REVIEWS wins. v1 let a domain match beat review count, which
    picked a 2-review "Gail's Ltd" shell over the real 860-review GAIL's employer.
    """
    if not candidates:
        return None, "none"
    qualified = []
    for c in candidates:
        dom = bool(blitz_domain) and host(c.get("website")) == blitz_domain
        strength, score = name_match(query, c.get("name"))
        if dom or strength:
            qualified.append((is_uk(c.get("headquarters")), reviews(c), dom, strength, c))
    if not qualified:
        return None, "none"   # nothing shares a name token or the domain: no usable candidate
    uk_hq, n_reviews, dom, strength, best = max(qualified, key=lambda t: (t[0], t[1]))
    solid = dom or strength == "strong"
    if uk_hq and solid and n_reviews >= MIN_REVIEWS:
        return best, "high"
    if uk_hq and solid:
        return best, "medium"
    return best, "low"


# ---------- main ----------
def main():
    objs = json.load(open(RAW, encoding="utf-8"))
    by_query = OrderedDict((q, []) for q in QUERIES)
    for o in objs:
        by_query.setdefault(o.get("inputSource"), []).append(o)

    blitz = {}
    for r in csv.DictReader(open(COMPANIES, newline="", encoding="utf-8")):
        blitz.setdefault(r["company_name"], r)   # first row wins on duplicate names

    rows = []
    for q in QUERIES:
        b = blitz.get(q, {})
        domain = (b.get("company_domain") or "").strip().lower()
        domain = "" if domain == "-" else domain
        cands = by_query.get(q, [])
        pick, conf = select(q, domain, cands)
        ratings = (pick or {}).get("ratings") or {}

        row = OrderedDict(query=q, blitz_domain=domain or "-", size_band=b.get("size_band") or "-",
                          sector=b.get("sector") or "-")
        row["selected_employer_id"] = str(pick.get("employerId") or pick.get("id")) if pick else "-"
        row["glassdoor_name"] = (pick or {}).get("name") or "-"
        row["glassdoor_hq"] = (pick or {}).get("headquarters") or "-"
        row["glassdoor_website"] = (pick or {}).get("website") or "-"
        row["review_count"] = str(reviews(pick)) if pick else "-"
        for col, key in STAR_RATINGS.items():
            row[col] = star(ratings.get(key))
        for col, key in SHARE_RATINGS.items():
            row[col] = share(ratings.get(key))
        row["match_confidence"] = conf
        row["candidates_returned"] = str(len(cands))

        enough = pick is not None and reviews(pick) >= MIN_REVIEWS
        overall, culture, lead = num(row["overall_rating"]), num(row["culture_values"]), num(row["senior_leadership"])
        bar_rating = enough and overall is not None and overall < BAR_OVERALL
        bar_sub = enough and ((culture is not None and culture < BAR_SUBRATING) or
                              (lead is not None and lead < BAR_SUBRATING))
        row["bar_rating"] = yn(bar_rating)
        row["bar_subrating"] = yn(bar_sub)
        row["bar_decline"] = "needs reviews"   # trend can't be judged from the profile alone
        row["passes_profile_bar"] = yn(bar_rating or bar_sub)
        rows.append(row)

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # ---------- summary ----------
    print(f"raw objects: {len(objs)}  queries: {len(rows)}  -> {os.path.basename(OUT)}")
    conf = OrderedDict((k, sum(r['match_confidence'] == k for r in rows)) for k in ("high", "medium", "low", "none"))
    print("match_confidence:", ", ".join(f"{k}={v}" for k, v in conf.items()))
    print(f"passes_profile_bar: {sum(r['passes_profile_bar'] == 'yes' for r in rows)}"
          f"  (bar_rating={sum(r['bar_rating'] == 'yes' for r in rows)},"
          f" bar_subrating={sum(r['bar_subrating'] == 'yes' for r in rows)})")
    fmt = "{:<38} {:<34} {:>5} {:>4} {:>4} {:>4} {:<6} {:<4}"
    print(fmt.format("query", "glassdoor_name", "revs", "ovr", "cul", "lead", "conf", "pass"))
    for r in rows:
        print(fmt.format(r["query"][:38], r["glassdoor_name"][:34], r["review_count"], r["overall_rating"],
                         r["culture_values"], r["senior_leadership"], r["match_confidence"], r["passes_profile_bar"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
