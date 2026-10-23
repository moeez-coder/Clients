"""Raw Blitz JSONL -> dated -leads.csv / -companies.csv for Security and Data Bench (C&G).

Usage: python3 build_csv.py <raw_dir> <date> [--per-company N]
Steps (all recorded in the .query.md):
  1. Normalise LinkedIn URL (https://www.linkedin.com/in/<slug>), dedupe on it.
  2. Persona title guard: the current matched title must be one of the seven persona roles
     (CIO, CTO, CISO, VP Engineering, VP of Data, Head of Data, Head of IT) and not a
     field/advisory/fractional/deputy variant. Rows failing the guard are dropped, counted by reason.
  3. Company join: lead's company_linkedin_url must be in the Blitz company sweep (same firmographic
     filter), which drops leads whose matched job is at a company outside the filter.
  4. Per-company cap (default 3), ranked by role priority so each company keeps its top tech leaders.
"""
import csv, json, re, sys
from collections import Counter, defaultdict

ROLE_RULES = [  # (role, regex) in priority order for the per-company cap
    ("CIO", r"\bCIO\b|chief information officer"),
    ("CTO", r"\bCTO\b|chief technology officer"),
    ("CISO", r"\bCISO\b|chief information security officer"),
    ("VP Engineering", r"\b(s?vp|evp|vice president)\b[\s,of-]*\b(software\s+)?engineering\b"),
    ("VP of Data", r"\b(s?vp|evp|vice president)\b[\s,of-]*\bdata\b"),
    ("Head of Data", r"\bhead of data\b"),
    ("Head of IT", r"\bhead of (it|information technology)\b"),
]
REJECT = [
    ("field/partner-facing", r"\bfield cto\b|\bcto\s*[-–,]\s*(channels|alliances|partners)|\bsolutions engineering\b|\bsales engineering\b"),
    ("fractional/advisory/consultant", r"\bfractional\b|\badvis(or|ory)\b|\bconsultant\b|\bconsulting\b|\bvirtual (ciso|cio|cto)\b|\bvciso\b"),
    ("deputy/assistant/associate", r"\bdeputy\b|\bassistant\b|\bassociate (vp|vice president)\b|\bavp\b"),
    ("in residence/former/board", r"\bin residence\b|\bformer\b|\bex-|\bboard (member|advisor)\b"),
]
PRIO = {r: i for i, (r, _) in enumerate(ROLE_RULES)}


def norm_li(u, kind="in"):
    if not u:
        return None
    m = re.search(rf"linkedin\.com/{kind}/([^/?#\s]+)", u.strip(), re.I)
    return f"https://www.linkedin.com/{kind}/{m.group(1).lower()}" if m else None


def classify(title):
    t = (title or "").strip()
    for reason, rx in REJECT:
        if re.search(rx, t, re.I):
            return None, reason
    for role, rx in ROLE_RULES:
        if re.search(rx, t, re.I):
            return role, None
    return None, "not a persona role"


def dash(v):
    return "-" if v in (None, "", []) else v


def main(raw, date, cap):
    companies = {}
    for line in open(f"{raw}/blitz_companies.jsonl"):
        c = json.loads(line)
        k = norm_li(c.get("linkedin_url"), "company")
        if k:
            companies[k] = c
    seen, kept, drops = set(), [], Counter()
    for line in open(f"{raw}/blitz_people.jsonl"):
        p = json.loads(line)
        li = norm_li(p.get("linkedin_url"))
        if not li:
            drops["no linkedin url"] += 1; continue
        if li in seen:
            drops["duplicate linkedin url"] += 1; continue
        seen.add(li)
        exps = p.get("experiences") or []
        exp = next((e for e in exps if e.get("job_is_current")), exps[0] if exps else {})
        role, why = classify(exp.get("job_title"))
        if not role:
            drops[f"title guard: {why}"] += 1; continue
        ck = norm_li(exp.get("company_linkedin_url"), "company")
        co = companies.get(ck)
        if not co:
            drops["company not in firmographic sweep"] += 1; continue
        loc = p.get("location") or {}
        kept.append({
            "linkedin_url": li, "first_name": dash(p.get("first_name")), "last_name": dash(p.get("last_name")),
            "full_name": dash(p.get("full_name")), "job_title": dash(exp.get("job_title")), "persona_role": role,
            "job_start_date": dash(exp.get("job_start_date")),
            "person_city": dash(loc.get("city")), "person_state": dash(loc.get("state_code")),
            "person_country": dash(loc.get("country_code")),
            "company_name": dash(co.get("name")), "company_domain": dash(co.get("domain")),
            "company_linkedin_url": ck, "company_industry": dash(co.get("industry")),
            "company_size": dash(co.get("size")), "company_hq_state": dash((co.get("hq") or {}).get("state")),
            "source": "blitz", "source_endpoint": "Blitz API POST /v2/search/people",
        })
    by_co = defaultdict(list)
    for r in kept:
        by_co[r["company_linkedin_url"]].append(r)
    final = []
    for ck, rows in by_co.items():
        rows.sort(key=lambda r: (PRIO[r["persona_role"]], r["job_start_date"] == "-", r["job_start_date"]))
        final += rows[:cap]
        drops["per-company cap"] += max(0, len(rows) - cap)
    final.sort(key=lambda r: (r["company_name"].lower(), PRIO[r["persona_role"]]))
    cols = list(final[0].keys())
    with open(f"{date}-leads.csv", "w", newline="") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(final)
    lead_cos = Counter(r["company_linkedin_url"] for r in final)
    ccols = ["company_linkedin_url", "company_name", "company_domain", "company_industry", "company_size",
             "company_type", "founded_year", "hq_city", "hq_state", "leads_in_snapshot", "source"]
    with open(f"{date}-companies.csv", "w", newline="") as f:
        w = csv.DictWriter(f, ccols); w.writeheader()
        for ck, c in sorted(companies.items(), key=lambda kv: (kv[1].get("name") or "").lower()):
            hq = c.get("hq") or {}
            w.writerow({"company_linkedin_url": ck, "company_name": dash(c.get("name")),
                        "company_domain": dash(c.get("domain")), "company_industry": dash(c.get("industry")),
                        "company_size": dash(c.get("size")), "company_type": dash(c.get("type")),
                        "founded_year": dash(c.get("founded_year")), "hq_city": dash(hq.get("city")),
                        "hq_state": dash(hq.get("state")), "leads_in_snapshot": lead_cos.get(ck, 0),
                        "source": "Blitz API POST /v2/search/companies"})
    print(json.dumps({"companies_in_sweep": len(companies), "raw_people": len(seen) + drops["duplicate linkedin url"] + drops["no linkedin url"],
                      "leads_final": len(final), "companies_with_leads": len(lead_cos),
                      "leads_per_company": dict(sorted(Counter(lead_cos.values()).items())),
                      "roles": dict(Counter(r["persona_role"] for r in final)), "drops": dict(drops)}, indent=1))


if __name__ == "__main__":
    a = sys.argv[1:]
    cap = int(a[a.index("--per-company") + 1]) if "--per-company" in a else 3
    main(a[0], a[1], cap)
