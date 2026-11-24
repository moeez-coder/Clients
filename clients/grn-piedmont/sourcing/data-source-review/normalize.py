"""Turn every raw pull (raw/*.json, raw/*.csv) into one sample CSV per source x slice, in one shape,
keyed by company LinkedIn URL (canonical https://www.linkedin.com/company/<slug>) or bare domain.
Also writes 2026-11-24-union-<slice>.csv: one row per distinct company across sources, with a
`sources` column and `in_blitz_tam` (match against ../general-tam/2026-11-24-companies.csv on LinkedIn slug or domain).
Field completeness is measured on these files (see score.py)."""
import csv, json, os, re
from common import *
D = "2026-11-24"
COLS = ["company_linkedin_url", "company_domain", "company_name", "slice", "source", "industry", "size",
        "employees", "revenue", "hq_city", "hq_state", "ownership_type", "description", "signal_data"]
ETCT = set(ET_CT_STATES)

def li_full(u):
    n = norm_li(u); return f"https://www.{n}" if n else "-"

def row(**k):
    r = {c: k.get(c) for c in COLS}
    for c in COLS:
        v = r[c]
        if v is None or (isinstance(v, str) and not v.strip()): r[c] = "-"
        else: r[c] = re.sub(r"\s+", " ", str(v)).strip()[:400]
    r["company_domain"] = norm_domain(r["company_domain"]) or "-"
    r["company_linkedin_url"] = li_full(r["company_linkedin_url"])
    return r

S = {}  # (source, slice) -> rows
def add(src, sl, r): S.setdefault((src, sl), []).append(r)

# Blitz
for f, sl in (("blitz-mfg.json", "mfg"), ("blitz-fls.json", "fls")):
    for key, blk in json.load(open(os.path.join(HERE, "raw", f))).items():
        if key == "fls-kw-anyind": continue  # 1,452 rows: keyword with no industry gate, kept in raw only (noise check)
        for x in blk["results"]:
            hq = x.get("hq") or {}
            add("blitz", sl, row(company_linkedin_url=x.get("linkedin_url"), company_domain=x.get("domain"), company_name=x.get("name"),
                slice=sl, source="Blitz /v2/search/companies", industry=x.get("industry"), size=x.get("size"),
                employees=x.get("employees_on_linkedin"), revenue=x.get("revenue_range"), hq_city=hq.get("city"),
                hq_state=hq.get("state"), ownership_type=x.get("type"), description=x.get("about")))
# Clay REST (mfg, 50 rows: plan cap) + Clay MCP (fls, page 1 of 20)
for x in json.load(open(os.path.join(HERE, "raw", "clay.json")))["mfg"]["results"]:
    loc = (x.get("location") or "").split(",")
    add("clay", "mfg", row(company_linkedin_url=x.get("linkedin_url"), company_domain=x.get("domain"), company_name=x.get("name"), slice="mfg",
        source="Clay REST query-mode", industry=x.get("industry"), size=x.get("size"), revenue=x.get("annual_revenue"),
        hq_city=loc[0] if loc else None, hq_state=loc[-1] if len(loc) > 1 else None, ownership_type=x.get("type"), description=x.get("description")))
for x in csv.DictReader(open(os.path.join(HERE, "raw", "clay-mcp-fls-page1.csv"))):
    loc = x["locality"].split(",")
    add("clay", "fls", row(company_linkedin_url=x["company_linkedin_url"], company_domain=x["domain"], company_name=x["company_name"], slice="fls",
        source="Clay MCP search-companies", industry=x["industry"], size=x["size"], employees=x["employee_count"], revenue=x["annual_revenue"],
        hq_city=loc[0], hq_state=loc[-1] if len(loc) > 1 else None))
# Prospeo
P = json.load(open(os.path.join(HERE, "raw", "prospeo.json")))
for key, sl in (("mfg", "mfg"), ("fls-kw", "fls")):
    for w in P[key]["results"]:
        x = w["company"]; loc = x.get("location") or {}; rr = x.get("revenue_range") or {}
        jp = x.get("job_postings")
        add("prospeo", sl, row(company_linkedin_url=x.get("linkedin_url"), company_domain=x.get("domain"), company_name=x.get("name"), slice=sl,
            source="Prospeo /search-company", industry=x.get("industry"), size=x.get("employee_range"), employees=x.get("employee_count"),
            revenue=x.get("revenue_range_printed") or (f"{rr.get('min')}-{rr.get('max')}" if rr else None), hq_city=loc.get("city"),
            hq_state=loc.get("state"), ownership_type=x.get("type"), description=x.get("description_ai") or x.get("description"),
            signal_data=(f"job_postings: {str(jp)[:200]}" if jp else None)))
# ColdIQ (AI Ark DB). mfg-v2 = HQ-constrained pass; fls-kw = exhaustive US pull filtered to ET/CT here.
C = json.load(open(os.path.join(HERE, "raw", "coldiq.json")))
for key, sl in (("mfg-v2", "mfg"), ("fls-kw", "fls")):
    for x in C[key]["results"]:
        if sl == "fls" and x.get("state") not in ETCT: continue
        add("coldiq", sl, row(company_linkedin_url=x.get("linkedin_url"), company_domain=x.get("domain"), company_name=x.get("name"), slice=sl,
            source="ColdIQ /v1/companies/search (ai-ark-companies)", industry=x.get("industry"), employees=x.get("employees"),
            revenue=x.get("revenue"), hq_city=x.get("city"), hq_state=x.get("state"), description=x.get("description")))
# DiscoLike
DL = json.load(open(os.path.join(HERE, "raw", "discolike.json")))
for key in ("mfg", "fls"):
    for x in DL[key]["results"]:
        soc = x.get("social_urls"); soc = soc if isinstance(soc, list) else re.findall(r"https?://[^'\" ,\]]+", str(soc))
        li = next((s for s in soc if "linkedin.com/company" in s), None); a = x.get("address") or {}
        add("discolike", key, row(company_linkedin_url=li, company_domain=x.get("domain"), company_name=x.get("name"), slice=key,
            source="DiscoLike GET /v1/discover", industry=",".join(list((x.get("industry_groups") or {}).keys())[:2]), size=x.get("employees"),
            revenue=x.get("revenue_range"), hq_city=a.get("city"), hq_state=a.get("state"), description=x.get("description")))
# Exa (company category): name + url only
for q in json.load(open(os.path.join(HERE, "raw", "exa.json")))["queries"]:
    if q["category"] != "company": continue
    for x in q["results"]:
        u = x["url"]; li = u if "linkedin.com/company" in u else None
        add("exa", q["segment"], row(company_linkedin_url=li, company_domain=None if li else u, company_name=x["title"], slice=q["segment"],
            source="Exa /search category=company", description=f"query: {q['query']}"))

# Blitz TAM (parent session file) for unique-coverage matching
tam_li, tam_dom = set(), set()
for x in csv.DictReader(open(os.path.join(HERE, "..", "general-tam", "2026-11-24-companies.csv"))):
    if norm_li(x["company_linkedin_url"]): tam_li.add(norm_li(x["company_linkedin_url"]))
    if norm_domain(x["company_domain"]): tam_dom.add(norm_domain(x["company_domain"]))

def key(r):
    return norm_li(r["company_linkedin_url"]) or ("dom:" + r["company_domain"] if r["company_domain"] != "-" else "name:" + r["company_name"].lower())

for (src, sl), rows in sorted(S.items()):
    seen, out = set(), []
    for r in rows:
        if key(r) in seen: continue
        seen.add(key(r)); out.append(r)
    S[(src, sl)] = out
    with open(os.path.join(HERE, f"{D}-{src}-{sl}-sample.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, COLS); w.writeheader(); w.writerows(out)
    print(f"{src:10s} {sl}: {len(out)} rows")

# union per slice: merge on LinkedIn slug, then domain
for sl in ("mfg", "fls"):
    U, by_li, by_dom = [], {}, {}
    for (src, s2), rows in S.items():
        if s2 != sl: continue
        for r in rows:
            li, dom = norm_li(r["company_linkedin_url"]), r["company_domain"] if r["company_domain"] != "-" else ""
            u = by_li.get(li) if li else None
            u = u or (by_dom.get(dom) if dom else None)
            if u is None:
                u = dict(r, sources=set()); U.append(u)
            u["sources"].add(src)
            for c in COLS:
                if u[c] == "-" and r[c] != "-": u[c] = r[c]
            if li: by_li[li] = u
            if dom: by_dom[dom] = u
    for u in U:
        li, dom = norm_li(u["company_linkedin_url"]), u["company_domain"]
        u["in_blitz_tam"] = "yes" if (li and li in tam_li) or (dom != "-" and dom in tam_dom) else "no"
        u["sources"] = "|".join(sorted(u["sources"]))
    with open(os.path.join(HERE, f"{D}-union-{sl}.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, ["company_linkedin_url", "company_domain", "company_name", "sources", "in_blitz_tam"] + COLS[3:]
                           , extrasaction="ignore"); w.writeheader(); w.writerows(U)
    print("union", sl, len(U))
