"""Load Doc 1 C1-3 GTM Sheets funnel tables (1 Companies, 2 Leads) from the repo CSVs via each table's webhook.
Usage: python3 -I load_gtm.py <date> <hooks.txt> [--dry]
hooks.txt lines: '<c1|c2|c3> <companies|leads> <webhook_url>' (kept OUTSIDE the repo: webhook URLs can write to tables).
Leads come from <date>-<camp>-leads.csv (launch set first, then hold, then removed). 'also_in' lists the other C1-3
campaigns holding the same LinkedIn URL. Companies come from <date>-<camp>-companies.csv with leads_launch_set /
leads_hold recounted from the final leads file; companies with 0 leads are kept so the drop-off shows.
A webhook load APPENDS: never re-run against a table that already has rows."""
import csv, json, os, sys, time, urllib.request, collections
HERE = os.path.dirname(os.path.abspath(__file__)); D, HOOKS = sys.argv[1], sys.argv[2]; DRY = "--dry" in sys.argv
N = {"c1": "c1-ceo", "c2": "c2-people", "c3": "c3-ta"}; LBL = {"c1": "C1 CEO", "c2": "C2 People", "c3": "C3 TA"}
hooks = {(a, b): c for a, b, c in (l.split() for l in open(HOOKS) if l.strip())}
leads = {c: list(csv.DictReader(open(os.path.join(HERE, f"{D}-{n}-leads.csv")))) for c, n in N.items()}
where = collections.defaultdict(set)
for c, L in leads.items():
    for r in L:
        if r["status"] == "launch set": where[r["linkedin_url"]].add(c)
def post(url, rows):
    for i in range(0, len(rows), 1000):
        req = urllib.request.Request(url, json.dumps(rows[i:i + 1000]).encode(), {"Content-Type": "application/json"}, method="POST")
        for a in range(4):
            try: print("  ", urllib.request.urlopen(req, timeout=180).read()[:80].decode()); break
            except Exception as e:
                if a == 3: sys.exit(f"FAILED at {i}: {e}")
                time.sleep(2 ** (a + 2))
order = lambda s: 0 if s == "launch set" else 1 if s.startswith("hold") else 2
for c in N:
    L = sorted(leads[c], key=lambda r: (order(r["status"]), r["company_name"]))
    for r in L: r["also_in"] = ", ".join(LBL[x] for x in sorted(where[r["linkedin_url"]] - {c})) or "-"
    cnt = collections.Counter((r["company_linkedin_url"], r["status"] == "launch set", r["status"].startswith("hold")) for r in L)
    C = list(csv.DictReader(open(os.path.join(HERE, f"{D}-{N[c]}-companies.csv"))))
    for r in C:
        r["leads_launch_set"] = cnt[(r["company_linkedin_url"], True, False)]; r["leads_hold"] = cnt[(r["company_linkedin_url"], False, True)]
    C.sort(key=lambda r: -int(r["leads_launch_set"]))
    print(c, "companies", len(C), "leads", len(L), "launch set", sum(r["status"] == "launch set" for r in L))
    if not DRY:
        post(hooks[(c, "companies")], C); post(hooks[(c, "leads")], L)
