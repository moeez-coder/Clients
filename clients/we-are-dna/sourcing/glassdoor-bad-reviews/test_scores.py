"""Glassdoor bad-review test (We Are DNA), 2026-11-17: per-employer scores from the 5 x 20 review pull.
Stdlib only. Reads 2026-11-17-test-company-lookup.csv (selected rows) and 2026-11-17-test-reviews.csv,
writes 2026-11-17-test-company-scores.csv. "-" in the inputs means empty; sub-ratings of 0 were already
written as "-" (Glassdoor's "not rated") and are ignored in averages.
share_uk_location is over reviews with a known location; reply_rate_on_negative is "-" when no review has overall <= 2."""
import csv, os, re
from collections import OrderedDict
HERE = os.path.dirname(os.path.abspath(__file__))
LOOKUP = os.path.join(HERE, "2026-11-17-test-company-lookup.csv")
REVIEWS = os.path.join(HERE, "2026-11-17-test-reviews.csv")
OUT = os.path.join(HERE, "2026-11-17-test-company-scores.csv")
SUBS = ["culture_values", "senior_leadership", "career_opportunities", "work_life_balance",
        "comp_benefits", "diversity_inclusion"]
UK_RE = re.compile(r"\b(england|scotland|wales|northern ireland|united kingdom|uk|london|manchester|birmingham|"
                   r"leeds|liverpool|glasgow|edinburgh|cardiff|belfast|bristol|sheffield|newcastle|nottingham|"
                   r"leicester|coventry|bradford|southampton|portsmouth|reading|aberdeen|swansea|knightsbridge)\b", re.I)
THEMES = OrderedDict([  # label -> keyword regex (case-insensitive, matched against cons text)
    ("management/leadership/communication", r"manag|leader|communicat"),
    ("career/progression/promotion", r"career|progress|promot"),
    ("workload/hours/weekends/work-life", r"workload|hours|weekend|work[- ]life|overtime"),
    ("pay/salary", r"\bpay|\bpaid|salar|wage"),
    ("training/onboarding/induction", r"train|onboard|induct"),
    ("culture/toxic/morale", r"cultur|toxic|morale"),
    ("recognition/appreciation", r"recogni|apprecia|valued"),
    ("staffing/understaffed", r"staffing|understaff|short[- ]staff"),
])

def val(x): return None if x in ("", "-") else x
def avg(xs):
    xs = [float(x) for x in xs if val(x) is not None]
    return f"{sum(xs) / len(xs):.2f}" if xs else "-"
def share(n, d): return f"{n / d:.2f}" if d else "-"

selected = {r["employer_id"]: r for r in csv.DictReader(open(LOOKUP, newline="")) if r["selected"] == "yes"}
by_emp = OrderedDict()
for r in csv.DictReader(open(REVIEWS, newline="")):
    by_emp.setdefault(r["employer_id"], []).append(r)

rows = []
for emp, rs in by_emp.items():
    sel = selected.get(emp, {})
    dates = sorted(r["posted_at"][:10] for r in rs if val(r["posted_at"]))
    neg = [r for r in rs if val(r["rating_overall"]) and float(r["rating_overall"]) <= 2]
    locs = [r["reviewer_location"] for r in rs if val(r["reviewer_location"])]
    counts = {t: sum(1 for r in rs if val(r["cons"]) and re.search(p, r["cons"], re.I)) for t, p in THEMES.items()}
    top = sorted((t for t in counts if counts[t]), key=lambda t: -counts[t])[:3]
    row = OrderedDict(company=rs[0]["company"], employer_id=emp,
                      glassdoor_overall_rating=sel.get("overall_rating", "-"),
                      glassdoor_review_count=sel.get("review_count", "-"),
                      reviews_pulled=len(rs), oldest_review_date=dates[0] if dates else "-",
                      newest_review_date=dates[-1] if dates else "-",
                      avg_overall_pulled=avg(r["rating_overall"] for r in rs))
    for s in SUBS:
        row[f"avg_{s}"] = avg(r[f"rating_{s}"] for r in rs)
    row["share_reviews_overall_le_2"] = share(len(neg), len(rs))
    row["share_uk_location"] = share(sum(1 for l in locs if UK_RE.search(l)), len(locs))
    row["employer_reply_rate"] = share(sum(1 for r in rs if r["employer_replied"] == "yes"), len(rs))
    row["reply_rate_on_negative"] = share(sum(1 for r in neg if r["employer_replied"] == "yes"), len(neg))
    row["top_cons_themes"] = "; ".join(f"{t} ({counts[t]})" for t in top) or "-"
    rows.append(row)

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)
print(f"wrote {len(rows)} rows to {OUT}")
