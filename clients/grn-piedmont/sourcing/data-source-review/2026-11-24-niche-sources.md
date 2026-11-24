# GRN Piedmont: niche / unique data sources review

**Date:** 2026-11-24
**Scope:** niche sources beyond associations, trade-show exhibitor lists, NAM/state manufacturer associations, ThomasNet and state Commerce expansion announcements (another reviewer covers those).
**Slices tested:** (a) NC + SC manufacturers, 201-1,000 employees; (b) fire and life safety (F&LS) firms in Eastern/Central time-zone states.
**Method:** free public pages and public government endpoints only (curl, WebSearch, WebFetch). No paid APIs, nothing committed.

## Headline

1. **OSHA ITA Form 300A data is the best free manufacturer source found.** It is a free bulk CSV with establishment name, company name, EIN, address, 6-digit NAICS and **annual average employees**. For NC + SC NAICS 31-33 (CY2024 file), it has 3,165 manufacturing sites. 611 of them report 201-1,000 employees (385 NC, 226 SC). Sample pulled.
2. **The Texas State Fire Marshal company registry can be downloaded in full.** One public lookup call returns every active registration: 3,151 rows, 2,103 distinct names, and 1,666 names holding fire alarm (ACR) and/or sprinkler (SCR) registrations. This is the complete legal universe of TX alarm and sprinkler firms. Sample pulled, joined to OSHA headcount.
3. The other state licence registries (NC, SC, FL, GA) work for one-off lookups but have no bulk export. The way to get each full list is a public-records request.
4. **For an F&LS buyer/target list, PE roll-up acquisition feeds (Pye-Barker above all) are the most useful niche signal.** Pye-Barker made 57 acquisitions in 2025 and 22 in H1 2026.

## Source tables

Legend for fields: Y = present, N = absent, P = partial.

### 1. State fire-protection contractor licence registries

| Source | What it is | URL | Free/paid | Access | Size | Fields (name / domain / LinkedIn / headcount / state / NAICS) | ICP precision guess | Signal value | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **Texas Dept of Insurance, State Fire Marshal (SFMO) company registrations** | Every company registered to sell, install or service fire alarms (ACR), sprinklers (SCR-G general, SCR-U underground, SCR-D dwelling), extinguishers (ECR) and fireworks | https://appscenter.tdi.texas.gov/reports/p/sfmo (JSON backend `POST /reports/p/searchSFMOCompanyLicenses`, body `{}` returns all) | Free | Public lookup. An empty search returns the full active list as JSON in one call (1.26 MB) | **Tested 2026-11-24:** 3,151 registration rows, 2,696 org ids, 2,103 distinct names. ACR 1,416; ECR 895; SCR 715 (G 414, U 296, D 5); fireworks ~84. 1,666 names hold ACR and/or SCR. 201 hold both alarm and sprinkler | Y / N / N / N / Y (address, county, branches) / N | High for "is a F&LS firm", but about half the names are not F&LS-named. Registrants include in-house self-performers (Tesla, Walmart, universities, hospitals) and general electrical/security firms. 863 of 1,666 carry a fire/sprinkler/alarm/safety/security keyword | Licence expiry dates and new registrations show market entry. Branch offices show footprint. The employee-list endpoint (`getSFMOCompanyDetails`) gives licensed technician counts per firm, a size proxy (not pulled) | **Wire in.** Complete, free, structured. Repeat monthly and diff for new entrants |
| NC State Board of Examiners of Plumbing, Heating and Fire Sprinkler Contractors | Licensed fire sprinkler contractors (FS classes) | https://www.nclicensing.org/ to https://public.nclicensing.org/Public/Search | Free | Search portal only. No bulk export seen. A public-records list request to the board (919-875-3612) is the route | Not measured | Y / N / N / N / Y / N | High for sprinkler contractors. Includes plumbing/HVAC licensees, so filter by FS class | Low (static) | Worth a records request. Not scrapeable at volume without risk |
| NC Board of Examiners of Electrical Contractors (fire alarm / low voltage, "FA/LV" class) | Fire alarm installers are licensed as limited electrical contractors | https://www.ncbeec.org/ to https://arls-public.ncbeec.org/Public/Search | Free | Search portal (same vendor platform as above). No export seen | Not measured | Y / N / N / N / Y / N | Medium. The FA/LV class also covers security/AV integrators | Low | Records request alongside the sprinkler board |
| SC LLR Contractor's Licensing Board (burglar / fire alarm / sprinkler) | SC licenses fire sprinkler contractors and alarm businesses through the CLB, not the State Fire Marshal | https://llr.sc.gov/clb/pub.aspx ; lookup https://verify.llronline.com/LicLookup/LookupMain.aspx | Free | Lookup portal plus an LLR **Licensee List Request Form** for bulk lists (contact Contact.CLB@llr.sc.gov) | Not measured | Y / N / N / N / Y / N | High | Low | **Request the bulk list.** It is the official route and it is free or cheap |
| Florida DFS, State Fire Marshal, Bureau of Fire Prevention, Regulatory Licensing | Fire Protection System Contractors I-V, fire equipment dealers | https://myfloridacfo.com/division/sfm/bfp/regulatory-licensing | Free | "Public Portal" search. No bulk download found. Counties (for example Lee County) publish PDF contractor lists | Not measured | Y / N / N / N / Y / N | High | Low | Records request if FL becomes a priority |
| Georgia Office of Insurance and Safety Fire Commissioner | Fire sprinkler contractor Certificates of Competency, fire suppression licensing | https://oci.georgia.gov/ ("Licensed Professionals Search", Citizenserve portal) | Free | Portal search only | Not measured | Y / N / N / N / Y / N | High | Low | Records request |

### 2. Certification listings

| Source | What it is | URL | Free/paid | Access | Size | Fields | ICP precision | Signal value | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| UL Product iQ, alarm service categories (UUFX central station; also UUJS, UUKA) | UL-listed fire alarm service companies, by location | https://productiq.ulprospector.com | Free with one-time registration | Login web search. **The curl probe returned 403 (bot-blocked) on 2026-11-24.** No export documented | Not measured. Nationally this is the certified central-station and alarm-service population, likely in the low thousands of locations | Y / N / N / N / Y / N | Very high for fire alarm integrators and monitoring companies | Low | Manual: a human logs in and exports per state. Good precision, poor scale |
| FM Approvals Approval Guide | Mostly approved *products*. Lists few installers | https://www.approvalguide.com/ | Free with registration | 403 to curl | - | Manufacturer names | Low for contractors | - | Skip for contractors. Possible use for F&LS *equipment manufacturers* (which also fall under GRN's manufacturing segment) |
| NICET | Individual technician certification (fire alarm, sprinkler layout, ITM) | https://www.nicet.org/ | Free | Individual verification only. No firm list | - | Person level | - | Low | Skip as a company source |

### 3. Government open data on manufacturers with headcount

| Source | What it is | URL | Free/paid | Access | Size | Fields | ICP precision | Signal value | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **OSHA Injury Tracking Application (ITA), Form 300A summary data** | Every establishment with 250+ employees, plus establishments with 20-249 employees in designated high-hazard industries (manufacturing and construction included), must file annually | https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data (redirects to /itadata). File used: https://www.osha.gov/sites/default/files/ITA_300A_Summary_Data_2024_through_12-31-2025.zip | Free | Bulk ZIP/CSV (24 MB zip, 87 MB CSV). **Needs a browser User-Agent. The default curl UA gets a CloudFront 403** | **Tested:** 398,620 establishments nationally (CY2024). NC+SC NAICS 31-33: 3,165 sites (2,110 NC, 1,055 SC). **201-1,000 employees: 611 sites (385 NC, 226 SC)**. 73 sites over 1,000. 2,313 distinct EIN/companies. 535 companies whose summed NC+SC headcount is 201-1,000. A CY2025 partial file (through 2026-08-31) also exists | Y (establishment + company name, EIN) / N / N / **Y (annual average employees, total hours)** / Y (full address) / **Y (6-digit NAICS)** | High for "manufacturer in NC/SC with X staff at the site". **Caveat: it is establishment level.** 337 of the 611 band sites belong to an EIN/company with 3+ reporting sites nationally, so many sit inside enterprises far over 1,000 staff (JBS, Lennox). A parent-size check (LinkedIn headcount via Clay/Blitz) is needed. 18% of NC/SC mfg rows have no EIN | Year-over-year headcount change per site is a growth/shrink signal. Injury rate (DAFW cases / hours) is a plant-ops pain signal for EHS and plant-manager searches | **Wire in (top pick for the manufacturing segment).** Annual refresh. Join to Clay/Blitz for domain, LinkedIn and parent size |
| EPA ECHO facility search | Regulated facilities (CAA/CWA/RCRA/TRI) | https://echodata.epa.gov/echo/echo_rest_services.get_facilities | Free, no key | REST API. **Tested:** `p_st=NC&p_ncs=332&p_act=Y` returned QueryRows 431 (NC fabricated-metal facilities alone) | Large (tens of thousands of NC/SC facilities) | Y / N / N / **N** / Y / Y | Medium. Facility, not company. No headcount | Enforcement and penalties as a "plant under pressure" signal for EHS/ops leadership searches | Secondary. Use as a signal overlay, not a list source |
| EPA TRI facility (Envirofacts) | Toxic release reporters (larger manufacturers) | https://data.epa.gov/efservice/tri_facility/state_abbr/NC/JSON | Free | REST. **Tested, 200** | NC TRI reporters number in the hundreds | Y + **parent_co_name + parent D&B number** / N / N / N / Y / Y (in TRI forms) | Medium-high for mid/large plants. Parent company field helps the roll-up OSHA lacks | Low | Secondary. Useful only to fill parent company |
| SAM.gov entity registrations | Federal contractor registrations | https://sam.gov/ (Entity API needs a free api.data.gov key) | Free with key | API / monthly extract | Large | Y / P (URL) / N / N (public extract has no employee count) / Y / Y | Medium. Biased to gov contractors | Defense/federal work as a growth hint | Skip for now. No headcount, and the key requires sign-up |
| Census County Business Patterns | Establishment **counts** by NAICS x size class | https://api.census.gov/data/2022/cbp | Free | API (302 redirect without a key in this session on 2026-11-24) | Counts only | No company names | - | TAM sizing only | Use only to size TAM and sanity-check OSHA coverage |

### 4. Signal sources (WARN, incentives)

| Source | What it is | URL | Free/paid | Access | Recency | Fields | Signal value | Verdict |
|---|---|---|---|---|---|---|---|---|
| NC WARN notices | Plant closings and mass layoffs (100+ employee employers) | https://www.commerce.nc.gov/data-tools-reports/labor-market-data-tools/workforce-warn-reports (2026 summary list + interactive dashboard + 2014-2025 archive) | Free | Web page / dashboard | 2026 report live | Company, county, date, affected count (per summary) | **Strong for exec search:** restructuring brings leadership change and turnaround hires (COO, plant manager, CHRO) | Wire in as a monthly signal |
| SC WARN reports (SC DEW / SCWorks) | Same for SC | e.g. https://scworks.org/sites/scworks/files/2026%20South%20Carolina%20WARN_Report%2008282026.pdf | Free | PDF, republished cumulatively every few weeks | Latest found 2026-08-28: 35 notices, 4,489 workers YTD | Company, county, date, workers, closure/layoff | Same as NC. Low volume (~35/yr) means hand review | Wire in (parse the PDF) |
| NC JDIG / One NC / rural Building Reuse grants | State incentive awards with job counts | JDIG annual report https://www.commerce.nc.gov/annual-report-job-development-investment-grant-jdig/open ; Governor press releases | Free | Press releases + annual PDF | Rolling (for example ProVia JDIG 2026-08-25) | Company, county, jobs, investment | Strong growth signal (new plant means new plant leadership). **Overlaps the other reviewer's "NC/SC Commerce expansion announcements"** | Leave to the other reviewer. Note only that the rural Building Reuse grants name smaller manufacturers that JDIG misses |
| SC Coordinating Council for Economic Development awards | SC equivalent | sccommerce.com | Free | Press releases / council minutes | Rolling | Company, county, jobs | Same, and same overlap | Leave to the other reviewer |

### 5. Industry directories and rankings

| Source | What it is | URL | Free/paid | Access | Size | Fields | ICP precision | Verdict |
|---|---|---|---|---|---|---|---|---|
| IndustryNet / Manufacturers' News (MNI) | Manufacturer directory with employee ranges | https://www.industrynet.com/ | Paid for export (free browse) | 403 to curl 2026-11-24 | Claims ~500k US plants | name / web / - / range / state / SIC-NAICS | High | Skip (paid, blocked). OSHA ITA covers the same ground for free with real headcount |
| Kompass, MacRAE's | Legacy B2B directories | kompass.com, macraesbluebook.com | Paid export | Web | Large | Similar | Medium | Skip |
| NC MEP / SC MEP (SCMEP) client lists | Extension partnership clients | ncmep.org, scmep.org | Free (case studies only) | Web | Tens of named case studies | Name only | High but tiny | Mine case studies only for messaging proof, not for a list |
| Inc. 5000 (filter mfg, NC/SC) | Fastest-growing private companies | https://www.inc.com/inc5000 | Free browse | 403 to curl. Needs a manual export or browser | Typically a few dozen NC/SC manufacturers per year | name / web / - / employees / state / industry | High fit plus a growth signal | Manual quarterly grab. A good "rapid growth" tag |
| Business journal "largest manufacturers" lists (Charlotte, Triad, Triangle, Greenville) | Ranked lists by local headcount | bizjournals.com Book of Lists | Paid (subscription) | Login | 25-100 per list | name / - / - / local employees / city | High | Skip unless a subscription exists |
| SDM 100 / SDM Top Systems Integrators (2026) | Ranked security dealers and integrators (Pye-Barker #3 SDM 100; TSI ranked by revenue) | https://sdmmag.com/articles/105352-sdm-100-top-100-security-dealers-of-2026 ; https://www.sdmmag.com/2026-TSI-Rankings | Free to read | Web/PDF | 100 + ~100 | name / HQ / revenue / growth | Medium. Security-heavy, with some fire alarm | Grab once as an "F&LS large-account" list. Mostly over-size for 201-1,000 targeting |
| Sprinkler Age / Fire Protection Contractor top-contractor lists | AFSA magazine | - | Members | - | - | - | - | Not tested (AFSA covered by the other reviewer) |

### 6. Other niche finds

| Source | What it is | URL | Free/paid | Access | Size | Signal value | Verdict |
|---|---|---|---|---|---|---|---|
| **PE roll-up acquisition feeds (Pye-Barker, also Summit Fire & Security, Sciens Building Solutions, Fortis, Impact Fire, API Group)** | Each acquired firm is a just-acquired F&LS company (integration hires) and each platform is a buyer needing branch/GM/ops leaders | Pye-Barker news https://pyebarkerfs.com/ ; trade press securitysales.com, securityinfowatch.com | Free | Press releases / trade press | Pye-Barker: 57 acquisitions in 2025, 22 in H1 2026, 100+ in two years. CB Insights counts 141 | **Very high.** Post-acquisition leadership turnover is a classic exec-search trigger. Platforms are repeat buyers | **Wire in.** Monthly Exa or press-release sweep per platform. Store acquired-company name, state, date |
| OSHA ITA keyword cut for F&LS (same file as above) | Fire/sprinkler-named establishments, NAICS 238220/238210/561621 etc., in ET/CT states | same OSHA file | Free | Bulk CSV | **Tested:** 489 establishments, 209 companies (keyword match on name). Headcount per firm (Pye-Barker 30+145 sites, Century Fire 10 sites / 899, Davis-Ulmer 1,386, Wayne Automatic 732) | Headcount for F&LS firms, which no licence registry gives | Use as the headcount join for the licence registries (done for TX in sample 2). Not written as its own CSV, to keep to the two-file limit |
| NFPA 25 ITM provider networks (for example BuildingReports, The Compliance Engine) | Inspection reporting platforms used by AHJs | thecomplianceengine.com | Platform for AHJs | Not public lists | - | - | Not usable as a list. Skip |

## Ranked top 5 worth wiring in

1. **OSHA ITA 300A (manufacturing segment).** Free, bulk, real headcount, 6-digit NAICS, full address. It covers 611 NC/SC manufacturing sites in the 201-1,000 band, plus every reporting state for the ET/CT expansion. The essential next step is a parent-company size check, since about 55% of band sites belong to multi-site enterprises. Refresh annually. A CY2025 partial file is already out.
2. **Texas SFMO company registry (F&LS segment).** Complete legal universe in one free call: 1,666 alarm/sprinkler registrant names. Monthly diff gives a "new entrant / new branch" signal. Pair it with the OSHA ITA join for headcount (52 of the top 300 matched).
3. **PE roll-up acquisition feeds (F&LS).** The highest-intent F&LS trigger for leadership hiring. Small and steady (~5-10 deals a month across platforms).
4. **NC + SC WARN notices (both segments, signal).** Free, low volume, high relevance for turnaround and replacement leadership searches. NC has a dashboard. SC needs PDF parsing.
5. **SC LLR CLB bulk Licensee List Request + NC sprinkler and FA/LV board records requests (F&LS, Carolinas).** These are the official complete Carolinas F&LS universes. They need a one-time form or records request, not scraping, so they are slower but definitive.

Honourable mentions: UL Product iQ alarm-service listings (best precision for fire alarm integrators, but login and manual), Inc. 5000 manual grab (growth tag), EPA TRI parent-company field (fills the OSHA parent gap).

## Sample CSVs pulled (this folder)

| File | Rows | Source | Filter | Notes |
|---|---|---|---|---|
| `2026-11-24-niche-osha-ita-ncsc-mfg-sample.csv` | 300 (of 611 in slice) | OSHA ITA 300A CY2024 | state in NC, SC; NAICS 31-33; annual_average_employees 201-1,000; sorted by employees descending, top 300 | **Establishment level.** `company_name` is the filer's company name. `hq_city` is the site city, not HQ. `domain` is `-` (not in source). EIN in notes |
| `2026-11-24-niche-tdi-tx-fls-licensees-sample.csv` | 300 (of 1,666 alarm/sprinkler registrant names) | TX SFMO registry + OSHA ITA CY2024 headcount join | licence type ACR or SCR-*; F&LS-named firms first (863 of 1,666), then by OSHA-matched headcount descending, then registration count | `employees` is the summed OSHA ITA site headcount where the normalized name matched (52 rows). Otherwise `-`. Matches are name-based and unverified, and a floor (sites under 20 staff do not file). `hq_city/state` is the registry address. `naics` comes from the OSHA match, else `-` |

## Reproduction (queries)

- OSHA: download the ZIP above with a browser User-Agent. Filter `state in (NC,SC)`, `naics_code[:2] in (31,32,33)`, `201 <= annual_average_employees <= 1000`. Company rollup key = EIN, else company_name.
- OSHA F&LS cut: states in the ET/CT list. Name regex `\b(FIRE|SPRINKLER|SUPPRESSION|LIFE SAFETY)\b`. NAICS in 238220, 238210, 561621, 561990, 811310, 238290, 541350, 238990.
- TDI: `POST https://appscenter.tdi.texas.gov/reports/p/searchSFMOCompanyLicenses` with JSON body `{}` and headers `Content-Type: application/json`, `Accept: application/json`. Licence type = prefix of `agyLicNbrDisplay` (ACR alarm, ECR extinguisher, SCR-G/U/D sprinkler, FW* fireworks, HCR hydrostatic).

## URLs fetched or probed (2026-11-24)

- https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data (403 with default UA, 200 with browser UA, redirects to /itadata)
- https://www.osha.gov/sites/default/files/ITA_300A_Summary_Data_2024_through_12-31-2025.zip (200, 23.9 MB)
- https://appscenter.tdi.texas.gov/reports/p/sfmo (200), /reports/resources/js/tdi-sfmoLic-includes.js (200), /reports/p/searchSFMOCompanyLicenses (POST 200, 3,151 rows)
- https://llr.sc.gov/clb/pub.aspx (200), https://verify.llronline.com/LicLookup/LookupMain.aspx (302)
- https://www.nclicensing.org/ (200), https://www.ncbeec.org/ (200)
- https://echodata.epa.gov/echo/echo_rest_services.get_facilities?output=JSON&p_st=NC&p_ncs=332&p_act=Y&responseset=1 (200)
- https://data.epa.gov/efservice/tri_facility/state_abbr/NC/rows/0:2/JSON (200)
- https://api.census.gov/data/2022/cbp (302 without key)
- https://productiq.ulprospector.com/en (403), https://www.approvalguide.com/ (403), https://www.industrynet.com/ (403), https://www.inc.com/inc5000 (403)
- https://www.commerce.nc.gov/data-tools-reports/labor-market-data-tools/workforce-warn-reports (200)
- https://dew.sc.gov/ (200). SC WARN PDFs located via search (latest 2026-08-28)
- https://www.myfloridacfo.com/division/sfm/bfp/regulatory-licensing (via search), https://oci.georgia.gov/ (200)
- https://www.nicet.org/ (200), https://sam.gov/ (200)
- Web searches: TDI SFMO licensee lists, NC sprinkler board, SC LLR CLB, FL SFM licensing, GA OCI, UL Product iQ UUFX, SDM 100 2026, Pye-Barker acquisitions 2026, SC WARN 2026, NC JDIG 2026
