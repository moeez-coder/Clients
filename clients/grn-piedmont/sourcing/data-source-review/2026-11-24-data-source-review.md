# GRN Piedmont: which data sources hold the best data for GRN's ICP (2026-11-24)

- **Asked by:** Moe, 2026-11-24: "which databases contain the highest-quality data for GRN's ICP-fit accounts? Include GTM Sheets' tools; there's Apify as well." In-session he also asked for research into "other unique / niche sources".
- **Client:** GRN Piedmont, tracking_clients `3abc2243-889c-4177-a75a-3ac680766d20`.
- **Session:** claude.ai/code session_013MzxQi5KPqGK6MKrbgk6Nt, branch `claude/grn-icp-data-sources`.
- **What this is not:** a campaign pull or a new segment. Nothing here was pushed to HeyReach or ingested into tracking_clients. The samples exist to measure sources.

## Short answer

| Job | Manufacturing (NC/SC test slice) | Fire & life safety (Eastern/Central) |
|---|---|---|
| **Discovery** | **Blitz** as the base (largest fit count, best fields), plus **DiscoLike** (best precision, 74%; finds fits Blitz misses for under 1 cent each) and **ColdIQ / AI Ark** (cheap second net) | **Blitz + Prospeo + DiscoLike** together (each has under half the fits alone), with the **NFSA contractor directory** as the free universe check |
| **Qualification** | Description classifier on top of the pull (as done here), with Blitz company enrichment for size and HQ; **OSHA ITA** site headcounts to check size | Same classifier: database labels alone are 8% to 24% precise for F&LS |
| **Persona** | **Blitz waterfall**: 14 of 15 test companies had a C-level, VP or Owner contact. Prospeo and ColdIQ untested (needs spend approval, see Open items) | Same |
| **Signals** | **Blitz jobs** (in use), **Apify LinkedIn + Indeed daily signal** gated to the TAM list, **NC/SC Commerce expansion announcements**, **Prospeo `job_postings`** field, WARN notices | Blitz jobs, **PE roll-up acquisition news** (Pye-Barker, Summit, Impact, Hiller and others buy dozens of F&LS firms a year), Exa news |

Three findings matter more than the ranking:
1. **The Blitz general TAM misses about a third of the manufacturing fits.** Of the 508 strict manufacturing fits found by any source, 164 (32%) are not in `../general-tam/2026-11-24-companies.csv`. A 15-row spot check shows real companies (Heritage Home Group, Amarr, SEW-Eurodrive USA, HSM, Tindall, Guilford Performance Textiles). DiscoLike and ColdIQ found most of them.
2. **Fire & life safety at 201 to 1,000 employees is a small universe.** Across every source the union holds 83 strict fits (178 if size or HQ is missing rather than wrong). Exa and the NFSA directory show many more F&LS firms, but 90%+ are under 201 employees. The segment is below the 200 to 300 company bar unless it widens to 51-200 or counts PE platforms' branch leaders.
3. **Clay is effectively off.** The Clay REST key is on a free plan now: 50 results per search and 100 per rolling 30 days (HTTP 402 on 2026-11-24). This also blocks listbuild's Clay layer. The Clay MCP still searches, 20 rows a page.

## Method

**The same ICP slice through every source.** Small enough to pull in full, so overlap is exact:
- **MFG slice:** US manufacturers, HQ in North Carolina or South Carolina, 201 to 1,000 employees. GRN's home region, and a fair test of the 22,367-company manufacturing TAM.
- **FLS slice:** US fire & life safety companies (sprinkler / suppression contractors, alarm / detection integrators, inspection-testing-maintenance providers), HQ in an Eastern or Central state, 201 to 1,000 employees.

Industry labels reuse the 68 manufacturing labels and the F&LS keyword gate from `../tam/tam_counts.py`, so the review and the TAM read agree. Each pull was normalized by `normalize.py` into one shape per source x slice (`2026-11-24-<source>-<slice>-sample.csv`, keyed by company LinkedIn URL, else domain). The per-slice unions (`2026-11-24-union-<slice>.csv`) merge on LinkedIn slug, then domain.

**Precision (does the company fit?).** Three checks, all must pass (`score.py`):
- **Type:** an agent classifier with written rules (`classify/RULES.md`) read name, industry and description for all 1,859 union rows. MFG: `yes` = makes products in its own plants (not a distributor, dealer, service shop, engineering firm, contractor, software...). FLS: `core` = sprinkler / alarm / ITM contractor or integrator; `adjacent` = F&LS equipment maker or distributor (reported, not counted as a fit). `unclear` counts as not a fit. Six Haiku agents, one MFG and one FLS batch each; outputs in `classify/out-*.csv`.
- **HQ:** the source's own HQ state is in the slice.
- **Size:** the source's own size bucket is 201-500 or 501-1,000, or its employee count is 150 to 1,500.

"Strict" counts a missing HQ or size as a fail. "Not contradicted" lets a missing value pass. Each source is judged on its own fields: that is the data you would get if you used it alone.

**Unique coverage:** fits whose LinkedIn slug or domain is not in the Blitz general TAM (`../general-tam/2026-11-24-companies.csv`, 22,631 companies, merged from the parent branch), and fits that no other API source in this review returned.

**Domain-only list sources** (Exa, Google Maps, NFSA, FABTECH) were resolved to firmographics with Blitz `POST /v2/enrichment/domain-to-linkedin` then `POST /v2/enrichment/company` (`resolve_domains.py`, `2026-11-24-domain-resolution.csv`: 507 domains, 411 resolved), then scored on the same rules.

**Field completeness:** share of rows with a value for company LinkedIn URL, size (bucket or count), revenue, HQ state and ownership type.

## Results: manufacturing (NC/SC, 201 to 1,000)

Union of all API sources: 916 companies, **508 strict fits**. Blitz returns 64% of them, ColdIQ 32%, DiscoLike 29%, Prospeo 21%, Clay and Exa 6% each.

| Rank | Source | Rows | Precision (strict) | Fits | Fits not in Blitz TAM | Fits no other source found | LinkedIn / size / revenue / HQ / ownership filled | Signal fields | Spend | Cost per fit |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Blitz** `POST /v2/search/companies` | 546 | 62% | **339** | 0 (it is the TAM) | 256 | 100 / 100 / 90 / 100 / 85% | jobs via `/v2/jobs/search` (separate call) | plan records | plan |
| 2 | **DiscoLike** `GET /v1/discover` | 196 | **74%** | 146 | **103** | 63 | 96 / 100 / 100 / 100 / 0% | none in record | $1.07 (both slices) | **$0.007** |
| 3 | **ColdIQ** (AI Ark DB) `POST /v1/companies/search` | 300 (3 pages of a larger set) | 54% | 161 | **100** | 33 | 100 / 100 / 100 / 100 / 0% | `is_hiring`, workforce growth filters | $1.43 (both slices) | $0.009 |
| 4 | **Prospeo** `POST /search-company` | 161 | 67% | 108 | 53 | 8 | 100 / 100 / 100 / 100 / **100%** | **`job_postings` in 43% of records** | 36 plan credits (both slices) | plan |
| 5 | **OSHA ITA 300A** (free download) | 611 NC/SC sites in 201-1,000 | not scored (site level, no domain) | - | - | - | name, EIN, address, NAICS, **site headcount** | - | free | free |
| 6 | **Exa** `POST /search` (category company) | 98 | 61% type; 20% after Blitz resolve | 20 | 4 | 0 | 1% LinkedIn; nothing else until resolved | news search | $0.13 | $0.007 |
| 7 | **Clay** REST query-mode | 50 (plan cap) | 58% | 29 | 0 | 1 | 100 / 100 / 98 / 100 / 100% | `jobs.exists` filter | free-plan quota | - |
| 8 | **FABTECH 2025 / IMTS 2026 exhibitors** (NC/SC) | 36 / 69 | 3% (FABTECH, after resolve) | 1 | 1 | 0 | none (IMTS: names only) | - | free | - |

Notes:
- **Blitz** is the backbone: most fits, the only source with both ownership type and a working people waterfall, and the job-signal API already in use. Its weakness is labels: 38% of what it returns for this slice is not a manufacturer (distributors, engineering firms, holding companies), and it misses a third of the fits that other sources find.
- **DiscoLike** reads company websites, so its "manufacturing" category is the most accurate (74%). Its count endpoint `GET /v1/count` is free and was used for sizing. No ownership type.
- **ColdIQ** routes to AI Ark's database for $0.0009 per company, with no need to spend the 64 direct AI Ark credits. **Gotcha:** `countries` + bare state names in `locations` silently ignore geography (the first pass came back US-wide, California first). Use `locations: ["North Carolina, United States", ...]` with no `countries`. ColdIQ also has an "unlimited growth" tier covering `search_companies` and `find_people` (1.17M records left this month), so heavier use may cost less than the per-credit price.
- **Prospeo**'s taxonomy is coarse: it rejected 35 of the 68 manufacturing labels (e.g. "Motor Vehicle Parts Manufacturing", "Plastics"), so it returns far fewer rows. Its records are the richest: phone, NAICS, revenue band, type, and live job postings.
- **GetLeads** (GTM Sheets provider) ignores the state filter (5,501 US-wide, warning returned), so it could not be tested on this slice.
- **Trade-show exhibitor lists do not work for GRN manufacturing.** NC/SC exhibitors at FABTECH and IMTS are equipment vendors selling to manufacturers, often US sales arms of foreign parents. VNTANA's 3x result held because its ICP *was* the exhibitors. Details: `2026-11-24-nonapi-sources.md`.
- **OSHA ITA** is the best free non-API source found: 611 NC/SC manufacturing sites at 201 to 1,000 employees, with real site headcount. It is site level, and 337 of the 611 belong to multi-site parents. It needs a name-to-domain join (Blitz) and a parent-size check before use. See `2026-11-24-niche-sources.md`.

## Results: fire & life safety (Eastern/Central, 201 to 1,000)

Union of all API sources: 943 companies, **83 strict fits** (178 not contradicted). Blitz returns 66% of the strict fits, Prospeo 45%, DiscoLike 45%, Exa 23%, ColdIQ 16%, Clay 0%.

| Rank | Source | Rows | F&LS type precision | Precision (strict) | Fits | Fits not in Blitz TAM | Fits no other source found | Fields filled | Spend |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Blitz** (8 contractor labels + F&LS keywords, and the `Fire Protection` label) | 286 | 24% | 20% | 56 (68 not contradicted) | 4 | 42 | 100 / 100 / 87 / 79 / 100% | plan |
| 2 | **Prospeo** (F&LS keywords) | 449 | 8% | 8% | 38 | 17 | 3 | 100% across; `job_postings` 58% | plan credits |
| 3 | **DiscoLike** (website phrases "fire sprinkler / fire alarm / fire suppression") | 240 | 15% | 15% | 37 | 18 | 6 | 96 / 100 / 100 / 100 / 0% | (in the $1.07) |
| 4 | **Exa** (company search, 5 regional queries) | 124 | **81%** | 10% after Blitz resolve | 13 | 0 | 0 | none until resolved | $0.13 |
| 5 | **NFSA contractor directory** (free, one public page) | 147 sampled of 468 ET/CT contractors | **96%** | 7% after resolve | 10 | 1 | 1 | website + address; no size | free |
| 6 | **ColdIQ** (AI Ark, keywords) | 73 | 18% | 18% | 13 | 10 | 1 | no ownership type | (in the $1.43) |
| 7 | **Apify Google Maps** (6 state searches) | 254 distinct | 96% | 4% after resolve | 9 | 2 | 2 | branches, no size | capped $2.00 |
| 8 | **Clay MCP** `search-companies` | 20 (page 1) | 0% | 0% | 0 | 0 | 0 | | - |

Notes:
- **Database labels are poor for F&LS.** A "fire protection" keyword pulls MEP engineering firms, general and mechanical contractors, NFPA itself, universities and software. Every database source needs the description classifier on top. Blitz is least bad.
- **Lists built for F&LS (Exa, NFSA, Google Maps) are 81% to 96% F&LS, but mostly small firms.** They are the right tool if the segment widens to 51 to 200 employees, or for finding branches of PE platforms. NFSA's directory is complete for its members and free (`2026-11-24-nonapi-nfsa-contractors-sample.csv` holds the first 150 rows; the full page holds 468 ET/CT contractor companies).
- **State licence registries are the legal universe.** Texas's fire marshal registry downloads in one call (2,103 firms; about half are F&LS firms). NC, FL and GA need public-records requests; SC has a bulk list request form. See `2026-11-24-niche-sources.md` and `2026-11-24-niche-tdi-tx-fls-licensees-sample.csv`.
- **DNC:** SuperHero Fire Protection (client DNC) came back in Exa's results. Any F&LS pull needs the DNC gate (`../recruitment-specific-open-roles/spec.py` `DNC`).

## Persona reach

| Source | Test | Result |
|---|---|---|
| **Blitz** `POST /v2/search/waterfall-icp-keyword` | 15 companies (10 NC/SC manufacturers found by both Blitz and Prospeo, 5 F&LS), CEO / COO / CFO / CHRO / President / Owner / VP titles, Manager and Director excluded | **14 of 15** companies returned at least one; 70 exec contacts in total. Matches the 2026-11-16 sample (13 of 14). File: `2026-11-24-persona-reach.csv` |
| Prospeo `POST /search-person`, ColdIQ `POST /v1/people/search` | Same 15 companies | **Not run.** The people searches were outside the spend Moe approved, so the run was blocked. `persona_test.py` notes them |
| DiscoLike, Clay, Exa, Apify, lists | - | DiscoLike sells contacts (`GET /v1/contacts`, $0.0035 each) but cannot honour exclusion lists. Clay MCP has `search-contacts`. Exa and the lists hold no people. Apify HarvestAPI profile search is the LinkedIn-native option |

## Signal data per source

| Signal | Source | What it gives | Status |
|---|---|---|---|
| Open leadership roles | Blitz `POST /v2/jobs/search` | title, posting date, company, `ai_summary` | **in use** (Recruitment Specific campaign) |
| Open roles | Prospeo company record `job_postings` | active count + titles, inside the company record, no extra call | 43% of MFG / 58% of F&LS records |
| Open roles, daily | Apify LinkedIn + Indeed actor `LzsIpToRTUZSnqjbS` via GTM Sheets signals | new postings every day, deduped on job URL | running for Talent Edge (London, NY); not set up for GRN |
| Open roles (one-off test) | Apify `curious_coder/linkedin-jobs-scraper` | 149 NC/SC "plant manager / director of operations / VP operations" postings, 30 days | 35 of 148 at 201 to 1,000 employees; 15 from staffing agencies. Needs the TAM gate. `2026-11-24-apify-linkedin-jobs-mfg-sample.csv` |
| New facilities / expansion | NC Commerce + SC Commerce press releases | 39 announcements in 90 days, with jobs and investment; SC releases link company LinkedIn | free. `2026-11-24-signal-expansions-sample.csv` |
| Expansion / news | Exa `POST /search` category news | dated articles | $0.022 per 25 results |
| Rapid growth | ColdIQ (AI Ark) `min_workforce_growth_pct`; Clay `employee_growth_*` | headcount growth filter | available, not tested |
| Ownership change | PE roll-up acquisition announcements (F&LS) | named acquired firms | free via news; strongest F&LS trigger found |
| Layoffs (negative or turnaround) | NC and SC WARN notices | company, county, workers | free |

## Spend (all 2026-11-24, approved by Moe in this session where paid)

| Source | Spend | How read |
|---|---|---|
| Blitz | plan records: 2,314 company-search records, 15 waterfall calls, ~507 domain resolutions + company enrichments | plan, no per-call charge |
| Prospeo | 36 plan credits (14,878 left) | `GET /account-information` before / after |
| ColdIQ | 100.3 credits = $1.43 | `GET /v1/me/credits` before / after; cap was 100 credits |
| DiscoLike | $1.07 | `GET /v1/usage` month-to-date spend before / after |
| Exa | $0.264 | `costDollars` in each response |
| Apify | capped at $2.00 (Google Maps) and $0.50 (LinkedIn Jobs); the tool does not return the actual charge | GTM Sheets `gtm_sheet_apify_run` cap |
| Clay | 50 + 20 results; free-plan quota now used for 30 days | 402 messages |
| AI Ark direct | 0 (tested through ColdIQ instead; 64 credits untouched) | - |

## Exact queries

- **Blitz:** `pull_blitz.py`. MFG: `industry.include` = 68 labels (two halves), `employee_range` 201-500 + 501-1000, `hq.country_code` US, `hq.state.include` NC + SC. FLS: 8 contractor labels + keywords `fire protection`, `fire sprinkler`, `fire alarm`, `fire suppression`, `life safety`, `hq.state.exclude` 13 Mountain/Pacific states; plus `industry: Fire Protection` alone. A keyword-only pull with no industry gate (1,452 rows) was kept in `raw/` as a noise check only.
- **Clay:** `pull_clay.py` (REST, DSL in the file) and one MCP `search-companies` page (`raw/clay-mcp-fls-page1.csv`; the DSL is the FLS query in `pull_clay.py`).
- **Prospeo:** `pull_prospeo.py` (`company_industry`, `company_location_search` "<State>, United States", `company_headcount_range`; FLS `company_keywords`).
- **ColdIQ:** `pull_coldiq.py`, provider pinned to `ai-ark-companies`; both passes are in the file.
- **DiscoLike:** `pull_discolike.py` (`GET /v1/count` then `GET /v1/discover`, `category=MANUFACTURING`, `state=NC,SC`, `employee_range=201,1000`; FLS `phrase_match` x3 + 38 states).
- **Exa:** `pull_exa.py` (12 queries listed in the file).
- **Apify:** GTM Sheets workbook `86aa0b0f-7f46-436c-aca7-7ea23fd34cd3` (GRN folder, research only, no HeyReach column): table `e2db6c26-e71a-402c-b60b-eeff6c3cb4c0` (Google Maps `compass/crawler-google-places`, 6 searches x 50) and table `04dab3d3-b589-4688-b830-00cb624d4315` (`curious_coder/linkedin-jobs-scraper`, 2 LinkedIn search URLs, last 30 days).
- **Lists and niche sources:** `2026-11-24-nonapi-sources.md` and `2026-11-24-niche-sources.md` (URLs fetched, verdicts).

## Recommended source stack for GRN

1. **Discovery, manufacturing:** Blitz `/v2/search/companies` as the base, add DiscoLike `/v1/discover` (category + state + size) and ColdIQ/AI Ark (`locations` "<State>, United States"). Dedupe on LinkedIn slug / domain. On this slice that turns 339 Blitz fits into 508.
2. **Discovery, F&LS:** Blitz + Prospeo + DiscoLike, then the NFSA directory as a completeness check. Decide first whether to widen to 51 to 200 employees. At 201 to 1,000 the segment is about 80 to 180 companies in total.
3. **Qualification:** run the description classifier (`classify/RULES.md`) on every pull; size and HQ from the source, filled by Blitz company enrichment where missing. Use OSHA ITA as the free size cross-check for manufacturers.
4. **Persona:** Blitz waterfall (as now). Compare Prospeo and ColdIQ people search once approved.
5. **Signals:** Blitz jobs (as now); add a GTM Sheets daily Apify LinkedIn + Indeed signal for GRN, gated to the TAM list; NC/SC Commerce announcements; Prospeo `job_postings` as a free first pass; PE roll-up news for F&LS.

## Loosening the ICP filter (Moe, 2026-11-24: "We can always loosen the icp filter if we find close enough companies")

Counted with `loosen_counts.py` (Blitz `POST /v2/search/companies` at `max_results: 1`, 1 plan record per count; DiscoLike `GET /v1/count`, free). Output: `2026-11-24-loosen-counts.json`. All counts are Eastern/Central HQ and use the same F&LS filters as the review.

| F&LS size band | Blitz (contractor labels + F&LS keywords) | Blitz `Fire Protection` label only | DiscoLike (website phrases) | Expected fits at Blitz's 24% type precision |
|---|---|---|---|---|
| 201-1,000 (ICP today) | 264 | 52 | 268 | ~65 (measured: 56-68) |
| **51-200** | **782** | **259** | **798** | **~190** |
| 1,001-5,000 | 61 | 11 | 66 | ~15 |
| 11-50 | 1,822 | 663 | 7,022 | too small for GRN's offer |

Resolved list companies (Exa, NFSA, Google Maps) in ET/CT tell the same story: 69 sit at 51-200 against 36 at 201-1,000.

**Read:** adding the 51-200 band roughly quadruples the F&LS pool, from about 80 fits to about 270, which clears the 200-300 company bar. The "close enough" candidates, in order:
1. **51-200 employees, F&LS core.** Largest gain. The same sources and classifier work: Blitz + Prospeo + DiscoLike + the NFSA directory, which is strongest in this band.
2. **F&LS equipment makers and distributors** (`adjacent`, 67 in the union, e.g. Potter Electric Signal, Peerless Pump, Kidde Fire Systems). They hire plant and engineering leaders, like GRN's manufacturing clients.
3. **1,001-5,000 employees:** about 15 more. These are mostly PE platforms (Pye-Barker, Summit, Impact). Their branch and regional leaders are reachable even though the parent is over the band.

Manufacturing doesn't need loosening: NC/SC alone has 508 fits at 201-1,000. Neighbouring bands are already at hand for later (Blitz TAM `general-tam`, 22,367 companies across Eastern/Central).

## Open items for Moe

- **Persona test for Prospeo and ColdIQ** (same 15 companies): about 15 Prospeo plan credits and a few ColdIQ credits (find_people may fall under ColdIQ's unlimited tier). Needs your go-ahead.
- **Clay REST plan:** the key is on a free plan (50 per search, 100 per 30 days). listbuild's Clay layer will fail until it is upgraded or replaced.
- **Blitz general TAM** (parent branch): 12,510 of its 22,631 rows have no HQ state (`hq_state_verified_et_ct` "no"), and the TAM misses about a third of NC/SC manufacturing fits. Adding DiscoLike + ColdIQ as discovery layers would close most of that gap.
- **F&LS sizing:** widen to 51 to 200 employees, or keep 201 to 1,000 and accept a small list with more contacts per company (the TAM/SAM inverse rule).
