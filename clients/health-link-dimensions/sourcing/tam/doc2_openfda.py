"""Doc 2 Campaign 6/7 trigger counts from openFDA (free, no key).
Drugs: GET https://api.fda.gov/drug/drugsfda.json, applications with a submission dated 2025-11-01..2026-11-18; submissions filtered
client-side: ORIG approvals (NDA type 1 = NME, BLA ORIG = novel biologic) and SUPPL approvals with submission_class_code EFFICACY
(new indication / population = label expansion). Devices: /device/510k.json (decision_date), /device/pma.json (original PMAs,
supplement_number empty), De Novo = 510k records with decision_code DENG? (De Novo has no openFDA endpoint; counted from 510k
'DEN' K-numbers). Writes 2026-11-18-doc-2-openfda.json."""
import json, urllib.request, urllib.parse, collections, time
def get(path, params):
    q = urllib.parse.urlencode(params, safe=":[]+\"")
    for a in range(5):
        try: return json.load(urllib.request.urlopen("https://api.fda.gov" + path + "?" + q, timeout=120))
        except urllib.error.HTTPError as e:
            if e.code == 404: return {"results": [], "meta": {"results": {"total": 0}}}
            time.sleep(2 ** a)
    return {"results": []}
LO, HI = "20251101", "20261118"
apps, skip = [], 0
while True:
    r = get("/drug/drugsfda.json", {"search": f"submissions.submission_status_date:[{LO}+TO+{HI}]", "limit": 1000, "skip": skip})
    apps += r.get("results", []); skip += 1000
    if skip >= r.get("meta", {}).get("results", {}).get("total", 0) or not r.get("results"): break
print("applications with activity in window", len(apps))
ev = []
for a in apps:
    num = a.get("application_number", ""); spons = a.get("sponsor_name")
    brand = sorted({p.get("brand_name") for p in a.get("products", []) if p.get("brand_name")})
    for s in a.get("submissions", []):
        d = s.get("submission_status_date", "")
        if not (LO <= d <= HI) or s.get("submission_status") != "AP": continue
        t, cls = s.get("submission_type"), s.get("submission_class_code")
        if num.startswith("ANDA"): continue
        if t == "ORIG" and (cls in ("TYPE 1", "TYPE 1/4") or num.startswith("BLA")):
            kind = "novel"
        elif t == "ORIG":
            kind = "new_nda_other"
        elif t == "SUPPL" and cls == "EFFICACY":
            kind = "efficacy_supplement"
        else: continue
        ev.append({"month": d[:6], "date": d, "kind": kind, "application": num, "sponsor": spons, "brands": brand,
                   "class": cls, "class_desc": s.get("submission_class_code_description")})
by = collections.defaultdict(collections.Counter)
for e in ev: by[e["month"]][e["kind"]] += 1
out = {"window": [LO, HI], "drug_events": ev, "drug_by_month": {m: dict(c) for m, c in sorted(by.items())}}
for m, c in sorted(by.items()): print(m, dict(c))
# devices
dev = {}
for name, path, field, extra in [("510k", "/device/510k.json", "decision_date", ""), ("pma_original", "/device/pma.json", "decision_date", "+AND+supplement_type:\"\"")]:
    pass
def monthly(path, field, extra=""):
    r = get(path, {"search": f"{field}:[{LO}+TO+{HI}]{extra}", "count": field})
    c = collections.Counter()
    for x in r.get("results", []): c[x["time"][:6]] += x["count"]
    return dict(sorted(c.items()))
dev["510k_all"] = monthly("/device/510k.json", "decision_date")
dev["510k_substantially_equivalent"] = monthly("/device/510k.json", "decision_date", "+AND+decision_code:SESE")
dev["denovo_DEN"] = monthly("/device/510k.json", "decision_date", "+AND+k_number:DEN*")
dev["pma_all_incl_supplements"] = monthly("/device/pma.json", "decision_date")
dev["pma_original_or_panel_track"] = monthly("/device/pma.json", "decision_date", "+AND+_missing_:supplement_number")
out["device_by_month"] = dev
for k, v in dev.items(): print(k, v, sum(v.values()))
json.dump(out, open("2026-11-18-doc-2-openfda.json", "w"), indent=1)

# ---- device detail: per-record pulls so we can filter to US applicants and drop the 10,000+ companies (Campaign 8) ----
LARGE = ["medtronic", "covidien", "abbott", "stryker", "boston scientific", "becton", "bd ", "c.r. bard", "zimmer", "biomet",
         "edwards lifesciences", "intuitive surgical", "baxter", "hill-rom", "ge healthcare", "ge medical", "siemens", "varian",
         "philips", "olympus", "smith & nephew", "smith and nephew", "teleflex", "dexcom", "resmed", "align technology",
         "dentsply", "solventum", "3m", "cook ", "b. braun", "johnson & johnson", "ethicon", "depuy", "biosense", "auris"]
def pull(path, field):
    rows, skip = [], 0
    while True:
        r = get(path, {"search": f"{field}:[{LO}+TO+{HI}]", "limit": 1000, "skip": skip}); rows += r.get("results", []); skip += 1000
        if skip >= r.get("meta", {}).get("results", {}).get("total", 0) or not r.get("results"): break
    return rows
k = pull("/device/510k.json", "decision_date"); p = pull("/device/pma.json", "decision_date")
def is_large(n): n = (n or "").lower() + " "; return any(x in n for x in LARGE)
mon = collections.defaultdict(collections.Counter); apps = collections.defaultdict(set)
for x in k:
    m = x["decision_date"].replace("-", "")[:6]; us = x.get("country_code") == "US"; den = x.get("k_number", "").startswith("DEN")
    kind = "denovo" if den else "510k"
    mon[m][f"{kind}_all"] += 1
    if us and not is_large(x.get("applicant")):
        mon[m][f"{kind}_us_non_large"] += 1; apps[m].add((x.get("applicant") or "").lower())
for x in p:
    if x.get("supplement_number"): continue
    m = x["decision_date"].replace("-", "")[:6]; mon[m]["pma_original_all"] += 1
    if not is_large(x.get("applicant")): mon[m]["pma_original_non_large"] += 1; apps[m].add((x.get("applicant") or "").lower())
out["device_detail_by_month"] = {m: dict(c, distinct_us_non_large_applicants=len(apps[m])) for m, c in sorted(mon.items())}
for m, c in sorted(out["device_detail_by_month"].items()): print(m, c)
json.dump(out, open("2026-11-18-doc-2-openfda.json", "w"), indent=1)
