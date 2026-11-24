"""QC pass on the Blitz general TAM (2026-11-24-companies.csv) -> 2026-11-24-companies-qc.csv.

No API calls. Adds QC columns, keeps every row (removals are shown, not deleted):
  qc_geo        foreign_signal | verified_et_ct | no_state_unverified
  qc_li_band    LinkedIn employee count band (Blitz employees_on_linkedin)
  qc_noise      first noise rule hit (dealer/auto service, benefit plan/union/chapter, distributor-only,
                gov/edu/nonprofit type, logistics/services, retail) or '-'
  qc_fls        F&LS precision read: fls_specialist | multi_trade_with_fls (MEP contractor with a fire division) | adjacent | not_fls (incl. fire departments, chapters, associations)
  qc_tier       core | review | drop  (+ qc_reason)
  dnc_match_fuzzy  DNC match on name contains/acquisition note, wider than the exact-name dnc_match
Rules were set from an eyeball of random samples (see 2026-11-24-tam-read.query.md, "Quality check").
Usage: python3 qc_tam.py
"""
import csv, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "2026-11-24-companies.csv")
OUT = os.path.join(HERE, "2026-11-24-companies-qc.csv")
assert not os.path.exists(OUT), "append-only"

CCTLD = set("cn in hu ir my ge de it fr es br mx tr uk pl ru ua vn id th pk bd eg za ng ar cl pe nl be ch at se no dk fi cz ro bg gr pt kr jp tw hk sg au nz ca ae sa lk ph ke ma tn dz ir iq jo lb qa kw om by kz uz az am rs hr si sk lt lv ee".split())
FOREIGN_NAME = re.compile(r"(co\.,? ?ltd|pvt\.?|private limited|gmbh|sdn\.? bhd|\bzrt\b|s\.r\.l|ltda|\bs\.a\.\b|\bs\.a\. de c\.v|\bkft\b|sp\. z o\.o|\boy\b|\ba/s\b|\bbv\b|\bjsc\b|\bllp\b|[^\x00-\x7f])", re.I)
US_STATES_ET_CT = True
NOISE = [
    ("dealer/auto service", r"dealership|auto ?group|\bmotors?\b.*\b(sales|service)|chevrolet|chrysler|toyota|honda|nissan|hyundai|\bkia\b|subaru|\bbuick\b|\bgmc\b|\bford\b(?! motor company)|car care|auto (service|repair|body)|collision|repair shop|tire (center|pros|store)|used car|pre-owned|fleet remarketing|rv center|powersports"),
    ("benefit plan/union/chapter", r"benefit plan|welfare (benefit|plan|fund)|retiree|pension plan|401\(?k|union local|\blocal \d{2,}\b|student chapter|alumni"),
    ("school/hospital/church", r"\b(school|hospital|church|university|college|academy)\b"),
    ("distributor/wholesale", r"^(?!.*manufactur).*\b(distributor|distribution|wholesale|wholesaler)\b"),
    ("logistics/services", r"^(?!.*manufactur).*\b(logistics|freight|staffing|consulting|property|properties|real estate)\b"),
    ("retail/restaurant", r"^(?!.*manufactur).*\b(retail store|restaurant|grocery|supermarket|boutique|e-?commerce store)\b"),
]
FLS_CORE = re.compile(r"fire (protection|sprinkler|alarm|suppression|safety|life safety|systems?)|life safety|sprinkler|suppression systems?|fire extinguish", re.I)
FLS_PUBLIC = re.compile(r"fire (department|district|company no|rescue|dept)|volunteer|fire ?fighters|\bchapter\b|association|\bnfpa\b|\bsociety\b", re.I)
FLS_SPECIALIST = re.compile(r"fire|sprinkler|life safety|suppression", re.I)
FLS_ADJ = re.compile(r"security|low voltage|electrical contractor|mechanical contractor|mep\b|integrat", re.I)


def norm(s):
    s = (s or "").lower()
    s = re.sub(r"\b(inc|llc|ltd|co|corp|corporation|company|the|group|holdings)\b\.?", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


dnc = [norm(r["company_name"]) for r in csv.DictReader(open(os.path.join(HERE, "../../context/dnc-list.csv")))]
# SuperHero's DNC note covers its acquisitions (listed on its site, not in the DNC file): flag any 'superhero' name only.


def li(x):
    try: return int(x["employees_on_linkedin"])
    except ValueError: return None


rows = list(csv.DictReader(open(SRC)))
for x in rows:
    text = f"{x['company_name']} {x['about']} {x['specialties']}"
    tld = x["company_domain"].rsplit(".", 1)[-1].lower() if x["company_domain"] != "-" else "-"
    if tld in CCTLD or FOREIGN_NAME.search(x["company_name"]):
        geo = "foreign_signal"
    elif x["hq_state"] != "-":
        geo = "verified_et_ct"
    else:
        geo = "no_state_unverified"
    n = li(x)
    band = "none" if n is None else "0-9" if n < 10 else "10-29" if n < 30 else "30-99" if n < 100 else "100+"
    noise = "-"
    if x["type"] in ("Government Agency", "Educational", "Educational Institution", "Nonprofit"):
        noise = "gov/edu/nonprofit type"
    else:
        for name, pat in NOISE:
            if re.search(pat, text, re.I):
                noise = name; break
    fls = "-"
    if "fire-life-safety" in x["segment"]:
        if FLS_PUBLIC.search(x["company_name"] + " " + x["about"][:150]):
            fls = "not_fls"
        elif FLS_CORE.search(f"{x['company_name']} {x['specialties']} {x['about'][:200]}"):
            fls = "fls_specialist" if FLS_SPECIALIST.search(x["company_name"]) or FLS_CORE.search(x["about"][:120]) else "multi_trade_with_fls"
        else:
            fls = "adjacent" if FLS_ADJ.search(text) else "not_fls"
        if False: fls = "core_fls" if FLS_CORE.search(f"{x['company_name']} {x['specialties']} {x['about'][:200]}") else "adjacent" if FLS_ADJ.search(text) else "not_fls"
    nn = norm(x["company_name"])
    fuzzy = "yes" if any(d and (d == nn or (len(d) > 5 and d in nn)) for d in dnc) or "superhero" in nn else "no"
    if x["dnc_match"] == "yes" or fuzzy == "yes":
        tier, why = "drop", "DNC"
    elif geo == "foreign_signal":
        tier, why = "drop", "foreign signal (ccTLD or foreign legal suffix / non-Latin name) though Blitz tags US HQ"
    elif noise != "-" and not (geo == "verified_et_ct" and n is not None and n >= 30):
        tier, why = "drop", f"noise: {noise}"
    elif noise != "-":
        tier, why = "review", f"noise rule hit ({noise}) but state verified and 30+ on LinkedIn: check by hand"
    elif fls == "not_fls":
        tier, why = "drop", "F&LS keyword hit but not a fire/life-safety business (or a fire department / association)"
    elif geo == "verified_et_ct" and n is not None and n >= 30:
        tier, why = "core", "ET/CT state verified, 30+ on LinkedIn, no noise rule"
    elif geo == "verified_et_ct" or (n is not None and n >= 30):
        tier, why = "review", "one of: state verified or 30+ on LinkedIn, not both"
    else:
        tier, why = "drop", "no HQ state and under 30 on LinkedIn (thin or ghost page)"
    x.update(qc_geo=geo, qc_li_band=band, qc_noise=noise, qc_fls=fls, dnc_match_fuzzy=fuzzy, qc_tier=tier, qc_reason=why)

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("rows", len(rows))
