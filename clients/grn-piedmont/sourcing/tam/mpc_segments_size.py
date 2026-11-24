"""Segment table for the GRN Piedmont MPC split (2026-11-24). Reads 2026-11-24-mpc-segments-jobs.csv (kept postings only)
and the live campaign's files, writes 2026-11-24-mpc-segments-companies.csv (one row per company, segment flags) and
2026-11-24-mpc-segments-size.json (the table). No API calls.  Usage: python3 mpc_segments_size.py"""
import csv, json, os, collections, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); LIVE = os.path.join(HERE, "..", "recruitment-specific-open-roles")
DATE = "2026-11-24"; TODAY = datetime.date(2026, 11, 24)
jobs = [r for r in csv.DictReader(open(os.path.join(HERE, f"{DATE}-mpc-segments-jobs.csv"))) if r["status"] == "kept"]
for r in jobs: r["age"] = (TODAY - datetime.date.fromisoformat(r["date_posted"])).days
# Prolonged vacancy, strong form: a role first posted 60+ days ago and reposted in the last 30 days (reposts are the
# "removed: repost (first seen ...)" rows). 32 of 40 sampled were still open, vs 6 of 40 for age alone (posting-check CSV).
allrows = list(csv.DictReader(open(os.path.join(HERE, f"{DATE}-mpc-segments-jobs.csv"))))
latest = {}
for r in allrows:
    if r["status"].startswith("removed: repost"):
        k = (r["company_linkedin_url"], r["title"].lower()); latest[k] = max(latest.get(k, ""), r["date_posted"])
for r in jobs:
    l = latest.get((r["company_linkedin_url"], r["title"].lower()))
    r["reposted_prolonged"] = r["age"] >= 60 and bool(l) and (TODAY - datetime.date.fromisoformat(l)).days < 30

# live campaign: companies with a launch-set lead in 734516 (11-16) or 756466 (11-23), and those leads
live_leads = collections.defaultdict(set)
for f in ("2026-11-16-leads.csv", "2026-11-23-leads.csv"):
    for r in csv.DictReader(open(os.path.join(LIVE, f))):
        if r.get("status", "launch set") == "launch set": live_leads[r["company_linkedin_url"].lower().rstrip("/")].add(r["linkedin_url"])
live_pulled = {r["company_linkedin_url"].lower().rstrip("/") for f in ("2026-11-16-companies.csv", "2026-11-23-companies.csv")
               for r in csv.DictReader(open(os.path.join(LIVE, f)))}

comp = {}
for r in jobs:
    c = comp.setdefault(r["company_linkedin_url"], {"company_name": r["company_name"], "company_linkedin_url": r["company_linkedin_url"],
        "vertical": r["segment_vertical"], "families": collections.Counter(), "postings": 0, "titles": set(), "oldest": 0, "newest": 999,
        "prolonged_postings": 0, "reposted_prolonged": 0})
    c["families"][r["role_family"]] += 1; c["postings"] += 1; c["titles"].add(r["title"].lower())
    c["oldest"] = max(c["oldest"], r["age"]); c["newest"] = min(c["newest"], r["age"])
    if r["age"] >= 60: c["prolonged_postings"] += 1
    if r["reposted_prolonged"]: c["reposted_prolonged"] += 1

def flags(c):
    f = set(c["families"])
    if c["vertical"] == "fire-life-safety": f = {"fire-life-safety"}
    else: f |= {"vertical:" + c["vertical"]}
    if c["prolonged_postings"]: f.add("overlay:prolonged-60-120d")
    if c["reposted_prolonged"]: f.add("overlay:prolonged-reposted")
    if c["vertical"] != "fire-life-safety" and len(c["titles"]) >= 3: f.add("overlay:multi-opening-3plus")
    return f

SEGS = ["executive", "operations-plant", "engineering-quality", "supply-chain-purchasing", "ehs-maintenance", "fire-life-safety",
        "overlay:prolonged-60-120d", "overlay:prolonged-reposted", "overlay:multi-opening-3plus"] + sorted({"vertical:" + c["vertical"] for c in comp.values() if c["vertical"] != "fire-life-safety"})
table = {}
for s in SEGS:
    cs = [c for c in comp.values() if s in flags(c)]
    if s == "overlay:prolonged-60-120d": post = sum(c["prolonged_postings"] for c in cs)
    elif s == "overlay:prolonged-reposted": post = sum(c["reposted_prolonged"] for c in cs)
    elif s in ("executive", "operations-plant", "engineering-quality", "supply-chain-purchasing", "ehs-maintenance", "fire-life-safety"):
        post = sum(c["families"][s] for c in cs)
    else: post = sum(c["postings"] for c in cs)
    contacted = [c for c in cs if c["company_linkedin_url"] in live_leads]
    table[s] = {"companies": len(cs), "postings": post,
                "companies_already_in_live_campaign": len(contacted),
                "companies_pulled_live_but_no_lead": sum(1 for c in cs if c["company_linkedin_url"] in live_pulled and c["company_linkedin_url"] not in live_leads),
                "net_new_companies": len(cs) - len(contacted),
                "live_leads_at_these_companies": sum(len(live_leads[c["company_linkedin_url"]]) for c in contacted),
                # never pulled by the live campaign at all: the only companies where Blitz has not already been asked for the persona
                "never_pulled_companies": sum(1 for c in cs if c["company_linkedin_url"] not in live_pulled),
                # refill rate: companies whose oldest posting in the window is under 30 days old (first seen this month), not live
                "first_seen_last_30d_not_live": sum(1 for c in cs if c["oldest"] < 30 and c["company_linkedin_url"] not in live_leads)}
table["_all_companies"] = {"companies": len(comp), "postings": len(jobs),
                           "companies_already_in_live_campaign": sum(1 for u in comp if u in live_leads),
                           "net_new_companies": sum(1 for u in comp if u not in live_leads),
                           "never_pulled_companies": sum(1 for u in comp if u not in live_pulled),
                           "first_seen_last_30d_not_live": sum(1 for u, c in comp.items() if c["oldest"] < 30 and u not in live_leads)}
json.dump(table, open(os.path.join(HERE, f"{DATE}-mpc-segments-size.json"), "w"), indent=1)
with open(os.path.join(HERE, f"{DATE}-mpc-segments-companies.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["company_name", "company_linkedin_url", "vertical", "role_families", "kept_postings", "distinct_titles",
                                   "prolonged_postings_60_120d", "reposted_prolonged_roles", "oldest_posting_days", "newest_posting_days", "segments",
                                   "in_live_campaign", "live_leads_contacted"])
    for c in sorted(comp.values(), key=lambda c: -c["postings"]):
        w.writerow([c["company_name"], c["company_linkedin_url"], c["vertical"], "; ".join(f"{k}:{v}" for k, v in c["families"].most_common()),
                    c["postings"], len(c["titles"]), c["prolonged_postings"], c["reposted_prolonged"], c["oldest"], c["newest"], "; ".join(sorted(flags(c))),
                    "yes" if c["company_linkedin_url"] in live_leads else "no", len(live_leads.get(c["company_linkedin_url"], ()))])
print(f"{'segment':34} {'cos':>5} {'posts':>6} {'live':>5} {'new':>5} {'never':>5} {'new30d':>6} {'liveLeads':>9}")
for s, v in table.items():
    print(f"{s:34} {v['companies']:5} {v['postings']:6} {v['companies_already_in_live_campaign']:5} {v.get('net_new_companies','-'):>5} {v.get('never_pulled_companies','-'):>5} {v.get('first_seen_last_30d_not_live','-'):>6} {v.get('live_leads_at_these_companies','-'):>9}")
