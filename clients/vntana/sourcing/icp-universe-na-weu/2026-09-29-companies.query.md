# VNTANA — complete ICP universe, North America + Western Europe (2026-09-29)

**Client:** VNTANA (`tracking_clients` id `5e0a22cf-6efb-432d-bc3c-6eb914440f13`)
**Config:** `icp-universe-na-weu` — **new segment folder**, not yet a `tracking_clients` sourcing config (UUID `-`). It is the
cross-segment universe that the approved campaigns (1, 3, 5, 6, 7, 9, 10 — see `clients/vntana/icp-approved-campaigns-2026-09-29.md`)
draw from, not a single segment.
**Pulled / scored:** 2026-09-29, by the orchestrating Claude Code session on branch `claude/initialize-u03yyd`.

## The request, verbatim
> "Using all available sources find me the complete universe companies that VNTANA may target. Do no include fashion and apparel."

Refined in the same conversation: scope **"Industrial + a few more"**; geography **"NA + Western Europe"**; ICP taken **from the
approved campaigns**; **"keep the filters as loose as possible"**; **"headcount has to be above 200"**.

## Files
| File | Rows | What it is |
|---|---|---|
| `2026-09-29-companies.csv` | 46,907 | every company any source returned, one row each, `universe_status` IN / OUT with the reason |
| `2026-09-29-client-yes-below-headcount-floor.csv` | 69 | client "Yes" companies (IMTS verdicts) that the 200-headcount rule removed — for manual add-back |
| `2026-09-29-triage-spec-t3.md` | – | the exact prompt every Haiku triage agent read |

**Result: 32,792 IN / 14,115 OUT.**

IN by country: US 19,093 · DE 3,692 · GB 1,757 · IT 1,655 · FR 1,537 · CA 1,065 · ES 939 · NL 777 · CH 453 · SE 368 · AT 359 ·
BE 278 · DK 241 · FI 200 · PT 177 · NO 104 · IE 59 · LU 38.

IN by how it got in (`fit_level`): RULE_VERTICAL 11,887 · FIT (agent) 7,275 · INDUSTRY_LABEL 5,114 · NO_DESCRIPTION 4,390 ·
UNSURE (agent) 4,057 · CLIENT_VERDICT 69.
OUT: EXCLUDED_TRIAGE 7,689 · EXCLUDED_RULE 4,607 · EXCLUDED_HEADCOUNT 944 · EXCLUDED_PRIOR 475 · EXCLUDED_GEOGRAPHY 398 · EXCLUDED_FASHION 2.

## Sources and exact queries
Geography = 18 HQ countries: US, CA + DE, GB, IT, FR, NL, SE, CH, AT, ES, IE, BE, LU, DK, NO, FI, PT (the last seven were added
in a second pass the same day after the first pass was found to have left them out). Mexico was **not** pulled.

1. **Blitz API `POST /v2/search/companies`** (header `x-api-key`), paginated by `cursor`, `max_results` 50:
   `{"company":{"industry":{"include":[<one>]},"employee_range":["201-500","501-1000","1001-5000","5001-10000","10001+"],"hq":{"country_code":[<one>]}}}`
   run for every (industry × country) pair. Industries (33 LinkedIn labels): Industrial Machinery Manufacturing, Machinery
   Manufacturing, Machinery, Automation Machinery Manufacturing, Industrial Automation, Agriculture; Construction; Mining Machinery
   Manufacturing, Commercial and Service Industry Machinery Manufacturing, Engines and Power Transmission Equipment Manufacturing,
   HVAC and Refrigeration Equipment Manufacturing, Metalworking Machinery Manufacturing, Metal Valve; Ball; and Roller Manufacturing,
   Fabricated Metal Products, Turned Products and Fastener Manufacturing, Spring and Wire Product Manufacturing, Cutlery and Handtool
   Manufacturing, Boilers; Tanks; and Shipping Container Manufacturing, Motor Vehicle Parts Manufacturing, Motor Vehicle
   Manufacturing, Transportation Equipment Manufacturing, Aviation and Aerospace Component Manufacturing, Electrical Equipment
   Manufacturing, Appliances; Electrical; and Electronics Manufacturing, Measuring and Control Instrument Manufacturing, Robotics
   Engineering, Robot Manufacturing, Mechanical Or Industrial Engineering, Plastics Manufacturing, Rubber Products Manufacturing,
   Packaging and Containers Manufacturing, Shipbuilding, Manufacturing, Computer Hardware Manufacturing, Electric Lighting Equipment
   Manufacturing. Pass 1 (11 countries): 1,065 calls, 39,741 rows. Pass 2 (7 countries): 237 calls, 1,611 rows.
2. **AI Ark API `POST /api/developer-portal/v1/companies`** (headers `X-TOKEN`, `User-Agent: curl/8.5.0`), 100/page:
   `account.location.any.include=[<country name>]`, `account.employeeSize={"type":"RANGE","range":[{"start":201,"end":1000000}]}`, plus
   either (a) `industry.any.include` = the same 33 labels in AI Ark's lower-case/comma form, or (b) one of 13 product-keyword groups
   on the description (`keyword.any.include.sources=[{"mode":"WORD","source":"DESCRIPTION"}]`): construction/ag/mining, cranes &
   material handling, trucks/trailers/bodies, HVAC & hydronics, pumps/valves/flow, hydraulics/pneumatics/power transmission,
   tools/tooling/machines, components/fasteners/consumables, electrical/automation, packaging/process, power equipment,
   robotics/metrology, aerospace/marine/RV. Pass 1: 17,585 rows; pass 2: 1,137 rows.
3. **Blitz API `POST /v2/enrichment/company`** — for the 62 repo records that had a LinkedIn URL but no country; 56 resolved (all US).
4. **Prior repo work, merged in (not re-pulled):** `sourcing/2026-09-16-us-icp-triage.csv` (5,227 US companies with t2 verdicts),
   `sourcing/2026-09-15-imts-exhibitors-enriched.csv`, `sourcing/dealer-brand-consistency/2026-09-28-companies.csv` (campaign 10
   tiers), and the client's own verdicts in `sourcing/2026-09-15-imts-client-icp-verdicts.csv` (matched by exact name).

Clay, EXA and DiscoLike were not used for this pull: Clay's `country` field is not filterable and it costs ~1k tokens/record;
EXA returns web pages not company entities; DiscoLike is over its monthly cap ($202.19 spent against a $99 limit).

**Merge/dedup key:** normalised `linkedin.com/company/<slug>`; else `d:<domain>`; else `n:<name>`; plus a domain back-match so a
company reached via LinkedIn in one source and domain in another collapses to one row. `sources` records every source that hit it.

## Rules, in the order they are applied
1. **Geography** — HQ country (vendor's own `hq` field) must be one of the 18 above. Otherwise OUT/EXCLUDED_GEOGRAPHY.
2. **Headcount > 200** — the company-stated LinkedIn **size band** decides (lower bound ≥ 201). The LinkedIn member count
   (`employees_on_linkedin`) is used **only when no band exists**: it undercounts badly — ~25,000 companies in a 201+ band showed
   fewer than 200 LinkedIn members in the first merge. Otherwise OUT/EXCLUDED_HEADCOUNT. `headcount_basis` says which applied.
3. **Client verdict** — any company the client itself marked "Yes" or "Near-ICP" that passes 1–2 is IN (CLIENT_VERDICT), whatever
   the rules below say (e.g. Quintus Technologies was a keyword false-exclusion).
4. **Prior US triage** — t2 FIT/UNSURE verdicts from 2026-09-16 are kept (IN). t2 NO verdicts were **re-read under t3**
   because t3's scope is wider (HVAC, aerospace, trucks/RV, consumables now in); those with no description stay OUT/EXCLUDED_PRIOR.
5. **Keyword screen** (regex over name + industry + description): exclusion hits with no vertical hit → OUT/EXCLUDED_RULE
   (dealer/retail 1,022+, food/bev/pharma/chem, fashion/apparel, medical, building products, services, consumer electronics,
   semiconductor capex, furniture, rail); vertical hits with no exclusion → IN/RULE_VERTICAL (tag in `verticals`); both → agent triage.
6. **Core industrial LinkedIn industry** with no keyword hit (Machinery, Industrial Machinery, Automation Machinery, Fabricated Metal,
   Motor Vehicle Parts, Electrical Equipment, Shipbuilding, Commercial Machinery, Measuring & Control, Metalworking, Transportation
   Equipment, Engines & Power Transmission, HVAC, Valves, Fasteners, Springs, Handtools, Boilers & Tanks, Ag/Construction/Mining
   Machinery, Aerospace Components, Robots, Industrial Automation) → IN/INDUSTRY_LABEL, no model cost.
7. **Mixed buckets** (Motor Vehicle Manufacturing, generic Manufacturing, Appliances/Electronics, Plastics, Packaging, Computer
   Hardware, Lighting, Rubber, Mechanical/Industrial Engineering, and AI Ark keyword hits in non-manufacturing industries):
   with a description → Haiku agent triage (16,123 companies); without one → IN/NO_DESCRIPTION (loose filter).

## Agent triage (step 7)
- 110 batches × ≤150 companies, one company per line, each read by a `general-purpose` subagent on **Haiku** with only the Read
  and Write tools, against `2026-09-29-triage-spec-t3.md`. Output `{"i","v","r"}` keyed on **line position**, never on an
  agent-echoed id. Verdicts: F 5,214 · U 2,882 · N 8,027 (raw, before the adjustments below).
- **A first wave was discarded.** 20 agents given 250-row single-line JSON files could not read them whole, wrote keyword-matching
  Python instead, and produced nonsense (a John Deere dealership → "food/candy", a university → "industrial mfg"). All of that
  output was thrown away; the batches were rebuilt one-company-per-line with "no code, no Bash" in the prompt and re-run from zero.
  One of those discarded agents also overwrote the session's keyword classifier; it was restored from the session transcript and
  verified to reproduce all 45,138 previous rule results exactly before pass 2 was merged.
- The first pilot batch skipped 48 rows and one parse lost 1; those 49 were re-run as a cleanup batch. **No company is untriaged.**
- **Post-adjustments** (each recorded in `post_adjustment`):
  - N → U when the reason names a contract manufacturer / EMS / service bureau / 3D-printing / integrator (spec trap 3): 146.
  - N → U for Packaging-industry makers unless the reason names food, cosmetics, consumer, distributor, service or print: 247.
  - F/U → N when the reason names medical, fashion/apparel, cosmetics or furniture (hard exclusions): 55.
  - Fashion/luxury LinkedIn industry with no industrial product in the reason → OUT/EXCLUDED_FASHION: 2 (Breguet watches, Saint-Louis
    crystal). Technical-textile makers (Sefar, SAERTEX, Uster, Serge Ferrari…) were checked by hand and correctly stay IN.

## Known limitations — read before using the numbers
- **"IN" is loose by design.** 4,390 NO_DESCRIPTION and 4,057 UNSURE rows are kept because nothing proved them out. Expect
  real noise there; they are the first place to cut if a campaign needs precision.
- **Passenger-car makers** (BMW, Volkswagen, Bugatti…) were mostly judged consumer brands and marked OUT; trucks, trailers, buses,
  RVs and their component suppliers are IN. Revisit if cars should count.
- **Vendor HQ tagging is imperfect.** Some Asian/Indian companies carry a US HQ in Blitz/AI Ark and so appear under US; some US
  subsidiaries carry the parent's HQ (Keyence, Nikon Metrology) and so fall OUT on geography. The country is taken as the vendor gives it.
- **Blitz counts are indicative** (see `clients/vntana/icp-universe-map.md` §6) and its industry tags are noisy — the industry
  label rule (step 6) inherits that noise.
- **210 IMTS records** have no LinkedIn URL, country or headcount in any source; they sit in the CSV as OUT/EXCLUDED_GEOGRAPHY
  ("no HQ country in any source"). The client-"Yes" ones among them are also in the below-floor file.
- **Subsidiaries under the floor:** 69 client-"Yes" companies are removed by the 200 rule, almost all US sales arms of large
  groups (Sandvik, NSK, Leica, HIWIN, WENZEL, SPINNER, Hainbuch) where LinkedIn shows only the local office. The user rule is
  applied literally; the separate file lists them for manual add-back.
- No revenue filter, no contact pull — this is a company universe only. TAM/SAM-driven contacts-per-company is decided per
  campaign when leads are pulled.

## Column guide (`2026-09-29-companies.csv`)
`company_linkedin_url` (dedup key; `-` if none) · `company_name` · `domain` · `country` (ISO-2) · `hq_city` · `linkedin_industry` ·
`size_band` · `employee_count` · `headcount_basis` (size_band / employee_count) · `universe_status` (IN/OUT) · `fit_level` (see
above) · `decision_stage` · `reason` (agent's ≤6-word reason, rule, or prior verdict) · `post_adjustment` · `verticals` (keyword
tags) · `sources` · `prior_us_triage` · `prior_c10_tier` · `client_imts_verdict`. No blank cells: `-` means checked, none exists.
