"""GRN Piedmont general TAM, independent sizing with DiscoLike free count endpoints (2026-11-24).

Both endpoints used here are free (checked: /usage month_to_date_spend and requests unchanged after calls):
  GET /v1/count            company count  (category, country, state/negate_state, employee_range, phrase_match)
  GET /v1/contacts/count   contact count  (filter_industry, filter_country, negate_filter_state, person_country,
                                           employee_range, seniority, title, has_linkedin)
Firmographics mirror the Blitz TAM pull: US HQ, 201-1,000 employees, HQ not in the 13 Mountain/Pacific/AK/HI states.
DiscoLike has its own 53-value category taxonomy (not LinkedIn labels), so the manufacturing TAM is read as
MANUFACTURING plus the adjacent categories a LinkedIn manufacturing label can land in, each counted separately.
Output: dl_counts.json.   Usage: python3 dl_counts.py
"""
import json, os, time, urllib.request, urllib.parse, urllib.error

H = {"x-discolike-key": os.environ["DISCOLIKE_API_KEY"], "User-Agent": "curl/8.5.0"}
NON_ET_CT = ["MT", "ID", "WY", "UT", "CO", "AZ", "NM", "NV", "WA", "OR", "CA", "AK", "HI"]
CATS = ["MANUFACTURING", "AUTOMOTIVE", "DEFENSE_AND_AEROSPACE", "FOOD_AND_BEVERAGE", "CONSUMER_PRODUCTS",
        "MINING_AND_METALS", "COMPUTER_HARDWARE_AND_SEMICONDUCTORS", "FASHION_TEXTILE_AND_APPAREL",
        "BUSINESS_PRODUCTS_AND_SERVICES", "CONSTRUCTION", "SECURITY", "ENGINEERING", "PHARMACEUTICALS",
        "SUPPLY_CHAIN_AND_PROCUREMENT"]
FLS_PHRASES = ["fire protection", "fire sprinkler", "fire alarm", "fire suppression", "life safety"]
EMP = "201,1000"


def get(path, params):
    for a in range(5):
        try:
            u = "https://api.discolike.com/v1" + path + "?" + urllib.parse.urlencode(params)
            r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=90))
            time.sleep(2.2)  # unbilled ops capped at 30 req/min
            return r
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(10 * (a + 1)); continue
            return {"_error": e.code, "_body": e.read()[:300].decode(errors="replace")}
    return {"_error": "retries"}


def comp(cat=None, et_ct=True, phrase=None):
    p = [("country", "US"), ("employee_range", EMP)]
    if cat: p.append(("category", cat))
    if et_ct: p += [("negate_state", s) for s in NON_ET_CT]
    if phrase: p.append(("phrase_match", phrase))
    return p


def contacts(cats, seniority=("executive", "vp"), et_ct=True, title=None):
    p = [("filter_country", "US"), ("person_country", "US"), ("employee_range", EMP), ("has_linkedin", "true")]
    p += [("filter_industry", c) for c in cats]
    p += [("seniority", s) for s in seniority]
    if et_ct: p += [("negate_filter_state", s) for s in NON_ET_CT]
    if title: p.append(("title", title))
    return p


out = {}


def run(key, path, params):
    r = get(path, params)
    out[key] = {"path": path, "params": params, "count": r.get("count", r)}
    print(key, out[key]["count"], flush=True)


if __name__ == "__main__":
    u0 = get("/usage", [])
    out["_usage_before"] = {k: u0.get(k) for k in ("month_to_date_requests", "month_to_date_spend", "month_to_date_records")}
    # sanity: does negate_state work (ET/CT < all-US)?
    run("company/MANUFACTURING/all-us", "/count", comp("MANUFACTURING", et_ct=False))
    for c in CATS:
        run(f"company/{c}/et-ct", "/count", comp(c))
    for ph in FLS_PHRASES:
        run(f"company/ALL/et-ct/phrase:{ph}", "/count", comp(None, phrase=ph))
        run(f"company/CONSTRUCTION/et-ct/phrase:{ph}", "/count", comp("CONSTRUCTION", phrase=ph))
        run(f"company/SECURITY/et-ct/phrase:{ph}", "/count", comp("SECURITY", phrase=ph))
    # persona reach, contacts with a LinkedIn URL
    run("contacts/MANUFACTURING/all-us/exec+vp", "/contacts/count", contacts(["MANUFACTURING"], et_ct=False))
    for c in CATS:
        run(f"contacts/{c}/et-ct/exec+vp", "/contacts/count", contacts([c]))
        run(f"contacts/{c}/et-ct/exec", "/contacts/count", contacts([c], seniority=("executive",)))
    for t in ["CEO", "President", "Owner", "COO", "CFO", "Chief Human Resources Officer", "Vice President"]:
        run(f"contacts/MANUFACTURING/et-ct/title:{t}", "/contacts/count", contacts(["MANUFACTURING"], title=t))
    u1 = get("/usage", [])
    out["_usage_after"] = {k: u1.get(k) for k in ("month_to_date_requests", "month_to_date_spend", "month_to_date_records")}
    print(out["_usage_before"], out["_usage_after"])
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dl_counts.json"), "w"), indent=1)
