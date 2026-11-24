"""Score every source x slice on the review's measures. Reads the per-source sample CSVs, the union files and
the classifier verdicts (classify/out-*.csv, rules in classify/RULES.md). Writes 2026-11-24-scores.csv and
2026-11-24-union-<slice>-scored.csv (union + verdict + geo/size checks + fit flag).

Fit (precision numerator), all three must hold:
  type : classifier verdict `yes` (MFG) / `core` (FLS). `adjacent` (F&LS equipment makers) is reported separately.
  geo  : HQ state in NC/SC (MFG) or an Eastern/Central state (FLS), from the source's own HQ field.
  size : 201-500 or 501-1,000 bucket, or an employee count of 150-1,500 when only a count is given
         (LinkedIn employee counts run below true headcount, hence the loose band).
  A missing geo or size value counts as NOT verified (so a source with no size data cannot score full fits);
  `type_precision` shows the type-only rate for those sources.
Unique coverage: fits whose LinkedIn slug / domain is not in the Blitz general TAM
(../general-tam/2026-11-24-companies.csv), and fits no other API source in this review returned."""
import csv, glob, os, re
from common import HERE, ET_CT_STATES, MFG_STATES, norm_domain, norm_li

D = "2026-11-24"
SPEND = {  # USD actually spent on this review's pulls (see the review doc for how each was read)
    "blitz": "plan records (2,314 company records + 15 waterfall calls); no per-call charge",
    "prospeo": "36 plan credits (PRO plan; 14,878 left)",
    "coldiq": 1.43, "discolike": 1.07, "exa": 0.26,
    "clay": "50 + 20 results of the Clay free-plan quota",
}
verdict = {}
for f in glob.glob(os.path.join(HERE, "classify", "out-*.csv")):
    for r in csv.DictReader(open(f)):
        verdict[r["key"]] = (r["verdict"].strip().lower(), r["reason"])


def ukey(r):
    return r["company_linkedin_url"] if r["company_linkedin_url"] != "-" else (
        r["company_domain"] if r["company_domain"] != "-" else "name:" + r["company_name"])


def size_ok(r):
    s = r.get("size", "-")
    if s in ("201-500", "501-1000", "501-1,000"): return "yes"
    if s not in ("-", ""): return "no"
    e = r.get("employees", "-")
    try:
        e = int(float(e))
        return "yes" if 150 <= e <= 1500 else "no"
    except (TypeError, ValueError):
        return "unknown"


def geo_ok(r, sl):
    st = (r.get("hq_state") or "-").strip()
    if st == "-": return "unknown"
    ok = MFG_STATES if sl == "mfg" else ET_CT_STATES
    return "yes" if st in ok else "no"


out_rows = []
for sl in ("mfg", "fls"):
    U = list(csv.DictReader(open(os.path.join(HERE, f"{D}-union-{sl}.csv"))))
    by = {}
    for u in U:
        v, why = verdict.get(ukey(u), ("unclassified", ""))
        u["type_verdict"], u["type_reason"] = v, why
        u["geo_ok"], u["size_ok"] = geo_ok(u, sl), size_ok(u)
        u["fit"] = "yes" if v in ("yes", "core") and u["geo_ok"] == "yes" and u["size_ok"] == "yes" else "no"
        for k in (norm_li(u["company_linkedin_url"]), u["company_domain"] if u["company_domain"] != "-" else None):
            if k: by[k] = u
    with open(os.path.join(HERE, f"{D}-union-{sl}-scored.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, list(U[0])); w.writeheader(); w.writerows(U)
    for f in sorted(glob.glob(os.path.join(HERE, f"{D}-*-{sl}-sample.csv"))):
        src = os.path.basename(f)[len(D) + 1:].rsplit(f"-{sl}-sample.csv", 1)[0]
        if src not in SPEND: continue
        rows = list(csv.DictReader(open(f)))
        n = len(rows)
        if not n: continue
        rec = []
        for r in rows:
            u = by.get(norm_li(r["company_linkedin_url"])) or by.get(r["company_domain"])
            if not u: continue
            # geo / size judged on THIS source's own fields (what you'd get if you used it alone)
            rec.append({"type": u["type_verdict"], "geo": geo_ok(r, sl), "size": size_ok(r),
                        "tam": u["in_blitz_tam"], "only": u["sources"] == src})
        fit = [x for x in rec if x["type"] in ("yes", "core") and x["geo"] == "yes" and x["size"] == "yes"]
        fit_lenient = [x for x in rec if x["type"] in ("yes", "core") and x["geo"] != "no" and x["size"] != "no"]
        typ = [x for x in rec if x["type"] in ("yes", "core")]
        pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "-"
        filled = lambda c: pct(sum(1 for r in rows if r.get(c, "-") not in ("-", "")), n)
        cost = SPEND[src]
        out_rows.append({
            "slice": sl, "source": src, "rows": n,
            "type_precision": pct(len(typ), n),
            "adjacent": sum(1 for x in rec if x["type"] == "adjacent") if sl == "fls" else "-",
            "fits_strict": len(fit), "precision_strict": pct(len(fit), n),
            "fits_not_contradicted": len(fit_lenient), "precision_not_contradicted": pct(len(fit_lenient), n),
            "fits_not_in_blitz_tam": sum(1 for x in fit_lenient if x["tam"] == "no"),
            "fits_only_this_source": sum(1 for x in fit_lenient if x["only"]),
            "li_url": filled("company_linkedin_url"), "domain": filled("company_domain"),
            "size": pct(sum(1 for r in rows if size_ok(r) != "unknown"), n), "revenue": filled("revenue"),
            "hq_state": filled("hq_state"), "ownership_type": filled("ownership_type"),
            "signal_data": filled("signal_data"),
            "spend": cost,
            "usd_per_fit": (f"${cost / len(fit_lenient):.4f}" if isinstance(cost, float) and fit_lenient else "-"),
        })
# ---- Domain-only list sources, scored after Blitz resolution (2026-11-24-domain-resolution.csv) ----
# type: union classifier verdict when the company is in a union; else by construction of the list:
#   Google Maps rows with a fire/sprinkler category, NFSA "Contractor" rows -> core;
#   FABTECH rows -> manufacturer only if Blitz's industry label contains "Manufacturing" (rough; stated in the doc).
res = {r["company_domain"]: r for r in csv.DictReader(open(os.path.join(HERE, f"{D}-domain-resolution.csv")))}
res_li = {norm_li(r["company_linkedin_url"]): r for r in res.values() if norm_li(r["company_linkedin_url"])}
tam_li, tam_dom = set(), set()
for x in csv.DictReader(open(os.path.join(HERE, "..", "general-tam", "2026-11-24-companies.csv"))):
    if norm_li(x["company_linkedin_url"]): tam_li.add(norm_li(x["company_linkedin_url"]))
    if norm_domain(x["company_domain"]): tam_dom.add(norm_domain(x["company_domain"]))
api_keys = {}
for sl in ("mfg", "fls"):
    for u in csv.DictReader(open(os.path.join(HERE, f"{D}-union-{sl}-scored.csv"))):
        for k in (norm_li(u["company_linkedin_url"]), u["company_domain"] if u["company_domain"] != "-" else None):
            if k: api_keys[(sl, k)] = u
LISTS = [("exa+blitz-resolve", "mfg", f"{D}-exa-mfg-sample.csv", "company_domain", 0.26 / 2),
         ("exa+blitz-resolve", "fls", f"{D}-exa-fls-sample.csv", "company_domain", 0.26 / 2),
         ("apify-googlemaps+blitz-resolve", "fls", f"{D}-apify-googlemaps-fls-sample.csv", "company_domain", "apify (see doc)"),
         ("nfsa-directory+blitz-resolve", "fls", f"{D}-nonapi-nfsa-contractors-sample.csv", "domain", 0.0),
         ("fabtech2025+blitz-resolve", "mfg", f"{D}-nonapi-fabtech2025-ncsc-sample.csv", "domain", 0.0)]
for name, sl, f, col, cost in LISTS:
    rows = list(csv.DictReader(open(os.path.join(HERE, f))))
    seen, rec = set(), []
    for r in rows:
        li = norm_li(r.get("company_linkedin_url", ""))
        d = norm_domain(r.get(col, ""))
        rr = (res_li.get(li) if li else None) or res.get(d)
        k = (norm_li(rr["company_linkedin_url"]) if rr else "") or li or d or r.get("company_name")
        if k in seen: continue
        seen.add(k)
        u = api_keys.get((sl, li)) or api_keys.get((sl, d)) or (api_keys.get((sl, norm_li(rr["company_linkedin_url"]))) if rr else None)
        if u: typ = u["type_verdict"]
        elif "googlemaps" in name: typ = "core" if re.search(r"fire|sprinkler", r.get("category", ""), re.I) else "no"
        elif "nfsa" in name: typ = "core" if "contractor" in r.get("notes", "").lower() else "adjacent"
        elif "fabtech" in name: typ = "yes" if rr and "manufactur" in rr["industry"].lower() else "no"
        else: typ = "unclassified"
        g = geo_ok(rr, sl) if rr and rr["found"] == "yes" else "unknown"
        s = size_ok(rr) if rr and rr["found"] == "yes" else "unknown"
        rl = norm_li(rr["company_linkedin_url"]) if rr else ""
        in_tam = (rl and rl in tam_li) or (d and d in tam_dom)
        rec.append({"type": typ, "geo": g, "size": s, "tam": "yes" if in_tam else "no", "api": bool(u), "resolved": bool(rr and rr["found"] == "yes")})
    n = len(rec)
    fit = [x for x in rec if x["type"] in ("yes", "core") and x["geo"] == "yes" and x["size"] == "yes"]
    pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "-"
    out_rows.append({"slice": sl, "source": name, "rows": n,
                     "type_precision": pct(sum(1 for x in rec if x["type"] in ("yes", "core")), n),
                     "adjacent": sum(1 for x in rec if x["type"] == "adjacent") if sl == "fls" else "-",
                     "fits_strict": len(fit), "precision_strict": pct(len(fit), n),
                     "fits_not_contradicted": len(fit), "precision_not_contradicted": pct(len(fit), n),
                     "fits_not_in_blitz_tam": sum(1 for x in fit if x["tam"] == "no"),
                     "fits_only_this_source": sum(1 for x in fit if not x["api"] and x["tam"] == "no"),
                     "li_url": pct(sum(1 for x in rec if x["resolved"]), n) + " (after Blitz resolve)",
                     "domain": "-", "size": pct(sum(1 for x in rec if x["size"] != "unknown"), n) + " (after resolve)",
                     "revenue": "-", "hq_state": "-", "ownership_type": "-", "signal_data": "-",
                     "spend": cost, "usd_per_fit": (f"${cost / len(fit):.4f}" if isinstance(cost, float) and cost and fit else "-")})

with open(os.path.join(HERE, f"{D}-scores.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(out_rows[0])); w.writeheader(); w.writerows(out_rows)
for r in out_rows:
    print(r["slice"], f"{r['source']:10s}", r["rows"], "type", r["type_precision"], "strict", r["fits_strict"], r["precision_strict"],
          "lenient", r["fits_not_contradicted"], r["precision_not_contradicted"], "notTAM", r["fits_not_in_blitz_tam"],
          "only", r["fits_only_this_source"], "| li", r["li_url"], "size", r["size"], "rev", r["revenue"], "st", r["hq_state"],
          "own", r["ownership_type"], "sig", r["signal_data"], r["usd_per_fit"])
print("unclassified:", sum(1 for k in verdict if not k))
