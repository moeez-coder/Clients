# Agency persona sizing (2026-11-18)

- **What:** count-only sizing of agency campaigns segmented by Christopher Martin's persona deck (`context/agency-personas-cwm.md`). No full pull. Counts with `max_results: 1`, plus small fit samples and one capped `tam-by-people` company list.
- **Client:** Health Link Dimensions, tracking_clients `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`.
- **Config:** none (`-`). tracking_clients has 0 sourcing configs; none created here.
- **Segment status:** expands the existing agency segment (doc 1 segment 5, sized 2026-11-09 at 3,317) into persona campaigns. Not a new config-slug.
- **Session:** claude.ai/code session_013MzxQguARXeFKghchjnaJ4.

## 1. Campaign-count decision: 3 campaigns, not 4

Moe's starting point was 4 campaigns, one per persona. The counts say 4 equal campaigns is wrong:

- **Investment is too thin to run alone.** Inside health-specialist agencies only **6 companies / 40 people** have investment or programmatic titles, and most of them are at CMI Media Group. Health agencies mostly do not buy media in-house; that sits in holdco media agencies (and Publicis Health Media, an HLD client, is one of them).
- **Investment and Planning and Activation are the same department and the same buyer of HLD's product.** Both live in the media team, both care about the Provider Insight Report's digital-ID match, and the deck's Advocates rows for the two are word for word identical.

**Recommendation:**

| # | Campaign | Persona(s) from the deck | Levels inside it |
|---|---|---|---|
| 1 | Leadership | Leadership | Influencers (C-suite, founders), Decision Makers (MD, GM, EVP, Group President, head of strategy) |
| 2 | Data and Analytics | Data and Analytics | all 3 levels |
| 3 | Media (Investment + Planning and Activation) | Investment, Planning and Activation | all 3 levels, with two copy angles routed by title: investment titles get the CPM / match-rate / transparent-economics angle, planning titles get the precision / new-tactics / DSP-coverage angle |

**Levels are copy tiers inside each campaign, not separate campaigns.** The Advocates level is about 102 people across all personas (45 D&A, 12 investment, 45 planning). A standalone Advocates campaign would be small, and the Advocates rows are only identical for Investment and Planning (which are merged anyway); Leadership's and D&A's Advocates want different things ("make me look smart", "documented data workflow"). Leadership gets no Advocates tier: generic associate-director titles belong to the functional personas.

## 2. Company universe

Blitz `POST /v2/search/companies`, exact enum labels from `docs/blitz-api/company-search-industries.txt` (branch `origin/claude/stoic-hypatia-yxvmmu`).

Final (core) filter, 260 companies:

```json
{"company": {
  "industry": {"include": ["Advertising Services", "Marketing and Advertising", "Marketing Services"]},
  "employee_range": ["51-200", "201-500", "501-1000", "1001-5000"],
  "hq": {"country_code": ["US"]},
  "keywords": {
    "include": ["pharmaceutical marketing", "pharma marketing", "pharmaceutical advertising", "pharma advertising",
                "medical communications", "life sciences marketing", "life sciences communications", "HCP marketing",
                "HCP", "biopharma", "healthcare communications", "health and wellness communications", "pharmaceutical", "pharma"],
    "exclude": ["staffing", "SEO", "hospital marketing", "dental marketing", "senior living"]},
  "name": {"exclude": ["Publicis Health Media", "EVERSANA", "Relevate Health", "HealthLink Dimensions", "Health Link Dimensions",
                       "Throtle", "DeepIntent", "PulsePoint", "OptimizeRx", "IQVIA", "Komodo"]}},
 "max_results": 1}
```

How it was tightened (all counts `max_results: 1`):

| Variant | Count | Note |
|---|---|---|
| 2026-11-09 read (6 broad health keywords, 11+ emp) + client exclusions | 3,336 | baseline |
| tight health-marketing phrases, 11+ emp | 2,187 | top results are general holdco networks (VML, McCann, Omnicom, TBWA, Grey) |
| same, 11 to 5,000 emp, `staffing` excluded | 2,154 | 1,570 of these are 11-50 emp |
| pharma-specific keywords (above), 11 to 5,000 emp | 782 | 519 are 11-50 emp |
| **pharma keywords, 51 to 5,000 emp (final)** | **260** | 161 / 58 / 22 / 22 by band |

Why each cut:
- **5,001+ dropped:** those are general networks (VML 30k, Omnicom, TBWA, IPG Mediabrands, McCann), whose employee counts would swamp the persona counts. Their health units (Omnicom Health, Publicis Health, FCB Health, McCann Health, Ogilvy Health) have their own pages and stay in.
- **11-50 dropped:** sample S3 (20 companies) was about 1 fit in 20: training, PR, video and branding shops with no media or data team.
- **Name exclusions:** HLD's existing clients, HLD itself (an HLD employee showed up in a planning sample), and identity/adtech vendors that are competitors or partners rather than buyers (Throtle, DeepIntent, PulsePoint and similar).

**Fit sample (S4, 20 companies, core universe, 51-200 band):** 12 fit, 1 borderline, 7 noise (60% fit). Every row with its verdict is in `2026-11-18-agency-universe-sample-companies.csv`.
- Fit: Reverba Global, MedTrix, The Bloc, Synchrony Group, PIXACORE, PRECISIONeffect, closerlook (Avalere Health), DDB Health New York, Navisync, JUICE Pharma, Calcium+Company, Deerfield Group.
- Borderline: Health Monitor Network (pharma point-of-care publisher).
- Noise: Continuum Clinical (trial recruitment), FCB Health Brazil (non-US), Signal Theory, Brand Institute, Cramer, Sullivan Higdon & Sink (general or non-media), Throtle (competitor, now excluded).
- Earlier exploratory samples (not in the CSV, broader filters): top-25 by size was 13 fit / 2 borderline / 10 noise; a 25-row 51-200 sample on the broader keywords was 9 / 2 / 14.

**Read:** about 260 Blitz companies, about 155 real health agencies. Small TAM.

## 3. Title map per persona

Blitz `POST /v2/search/people` (keyword match on current job title, US-located people, company filter = core universe above). `job_level` is a Blitz enum (`C-Team`, `VP`, `Director`, `Manager`).

| Persona | Title include (keyword) |
|---|---|
| Data and Analytics | Analytics, Measurement, Data Science, Data Scientist, Data Strategy, Data Analyst, Attribution, Insights, Marketing Science, Decision Science |
| Investment | Media Investment, Investment, Programmatic, Media Buying, Media Buyer, Biddable, Trading, Activation Economics, Supply Partnerships, Media Partnerships |
| Planning and Activation | Media Planning, Media Planner, Activation, Omnichannel, Omni-channel, HCP Media, Media Strategy, Media Director, Media Supervisor, Channel Planning, Connections Planning, Paid Media, Engagement Planning |
| Leadership, Influencers | CEO, Chief Executive, `[President]` (exact), President and CEO, President & CEO, Chief Strategy / Media / Operating / Growth / Innovation / Commercial Officer, Founder, Co-Founder |
| Leadership, Decision Makers | Managing Director, General Manager, Executive Vice President, EVP, Head of Strategy, SVP Strategy, Group President, Office Lead |

| Level | `job_level` |
|---|---|
| Influencers (C-suite / SVP / VP) | `C-Team`, `VP` |
| Decision Makers (VP / MD / Director) | `Director` (Leadership DM: `C-Team`, `VP`, `Director` with the MD/GM/EVP titles) |
| Advocates (Associate Director / Manager) | `Manager` |

Excluded from every persona: Intern, Assistant, Coordinator, Recruiter, Talent, Human Resources, Finance, Accounting, Legal, Facilities, Media Relations, Public Relations, Social Media, Sales Activation. Leadership also excludes functional and non-buyer words (Analytics, Programmatic, Account, Creative, Client, Business Development, Sales, Medical Director, Production and others; full list in `persona_counts.py`).

**Overlap handling.** Persona title filters are mutually exclusive by priority: Data and Analytics, then Investment, then Planning and Activation, then Leadership. Each later persona excludes the earlier ones' title words (for example "SVP Programmatic" counts in Investment, not Leadership; "Director, Data & Media Activation" counts in D&A). Levels within a persona are split by `job_level`, which does not overlap. So the people counts below add up without double counting. A **company** can appear in more than one campaign (different people at the same agency); that is intended multi-threading and is shown separately.

Exact request bodies for every cell: `2026-11-18-persona_counts.json` (written by `persona_counts.py`).

## 4. Counts

US people, core universe (Blitz `total_results`):

| Persona | Influencers | Decision Makers | Advocates | Total people | Distinct companies* |
|---|---|---|---|---|---|
| Data and Analytics | 49 | 65 | 45 | 159 | 45 |
| Investment | 10 | 18 | 12 | 40 | 6 |
| Planning and Activation | 31 | 81 | 45 | 157 | 39 |
| Leadership | 188 | 351 | - | 539 | 140 |
| **All** | | | | **895** | **147** |

\* Blitz `POST /v2/company/tam-by-people`, same filters, paged to the end per level. Company list with the persona levels found at each: `2026-11-18-agency-persona-companies.csv`.

- Investment's 6 companies: CMI Media Group, Spectrum Science, Deerfield Group, BioPharm Communications, InStep Health, interTrend. Five of the six also have planning people, so the merged Media campaign covers **40 companies, 197 people**.
- Only **62 of the 147** companies have any functional persona (D&A, Investment or Planning). The other 85 are reachable through Leadership only.

**Sensitivity, not added to the totals:** health-practice people inside general ad and media agencies (any size, no company keyword filter, job description mentions pharma / pharmaceutical / HCP / healthcare clients / health clients / life sciences): D&A 108, Investment 23, Planning 123. This is where most health media buying actually sits (holdco media agencies). It is the place to grow the Media campaign if Moe wants it bigger, but it means prospecting inside holdcos that compete with or own HLD clients (Publicis Health Media), so it is Moe's call.

**Title noise seen in samples** (`2026-11-18-agency-persona-title-samples-leads.csv`, 45 people, pulled before the final filter was locked):
- Leadership DMs: mostly right (MDs, Group Presidents, EVP Strategy), some miss (EVP Head of People, EVP Customer Experience). Assume about 70% fit.
- D&A: clean (Business Insights, Analytics, Data Strategy).
- Investment: clean, but dominated by CMI Media Group.
- Planning: two misses (Media Relations, Social Media Account Director) were found and are now excluded.

## 5. Contacts per company (inverse TAM rule)

The whole agency TAM is small (about 155 real agencies), so depth goes up. Within that, the functional pools are the smallest and get the most contacts per company; Leadership is the widest pool and gets the fewest.

| Campaign | Companies | People available | Contacts per company | Why |
|---|---|---|---|---|
| Leadership | 140 | 539 | 2 (1 C-suite or founder + 1 MD/GM/EVP/strategy lead) | widest pool; 2 senior people is enough to start a thread |
| Data and Analytics | 45 | 159 | up to 4 (1 influencer, 2 decision makers, 1 advocate) | small pool; take nearly everyone |
| Media (Investment + Planning) | 40 | 197 | up to 5 (investment and planning, all 3 levels) | smallest pool per persona; CMI Media Group will hit the cap |

Expected leads after caps and title cleanup: Leadership about 250, D&A about 130, Media about 130. Total about 510 people.

At the 62 companies with functional personas, one agency could get up to 11 contacts across the 3 campaigns. Stagger them (functional campaigns first, Leadership 2 to 3 weeks later at the same company) so an agency is not hit by all three at once.

## 6. Records used

Blitz, summed from each response's `fair_usage.records_used`:

| Step | Records |
|---|---|
| Universe variants, band counts, 4 company samples (25 + 25 + 20 + 20), 1 `tam-by-people` probe | 109 |
| Persona counts, Leadership re-cuts, 45 title-sample people, schema probes, one aborted run (12) | 78 |
| Final persona counts (`persona_counts.py`) | 15 |
| `tam-by-people` company lists, 4 personas (`persona_companies.py`, 450 hard cap) | 345 |
| **Total** | **547** (no single step over 500) |

Clay: not used (0 credits). Note: the Blitz key is shared; `records_remaining` fell by more than this session's own usage, so other sessions were drawing on it at the same time.

## 7. Uncertain or noisy

- Blitz counts are indicative (CLAUDE.md). The 60% company fit rate means about 40% of the 260 still need a qualifier at pull time.
- Leadership DM (351) is the softest number: "Managing Director" and "EVP" at PR-led health agencies are included.
- `job_level` buckets are Blitz's own; "Associate Director" may land in `Director`, so Advocates may be undercounted and Decision Makers overcounted a little.
- Parris's pharma/med device persona deck is still not received; this file covers agencies only.
- HLD's full client list is still missing (DNC is 0 in tracking_clients). Only the 3 named clients are excluded.

## 8. TAM expansion options (added later on 2026-11-18, Moe asked for a larger TAM)

Same method: Blitz `POST /v2/search/companies`, `max_results: 1` for counts, then 10 to 15-row fit samples per option. Exact bodies and sample rows: `2026-11-18-agency-tam-expansion.json`; script: `agency_tam_expansion.py`. All options keep the same client, HLD and vendor name exclusions. The slices are built so they don't overlap (different industry, size band or keyword set), so they add up.

| Option | Filter change | Added companies (Blitz) | Sample fit | Est. real agencies added |
|---|---|---|---|---|
| Core (sections 2 to 4) | ad/marketing industries, pharma keywords, 51 to 5,000 emp | 260 | 12/20 | ~155 |
| A. Broader health keywords | same industries and sizes, adds "healthcare marketing", "healthcare advertising", "health communications", "healthcare media", "life sciences", "medical marketing", "HCP engagement", "healthcare agency" (only companies that miss the pharma keywords) | +318 | 5/15 (Woven Health, Havas Health Network, Razorfish Health, Pivot Design, linqd) | ~105 |
| B. Health agencies filed under pharma or biotech industry | `Pharmaceutical Manufacturing`, `Pharmaceuticals`, `Biotechnology Research`, `Biotechnology` + agency keywords, 11 to 5,000 emp, CRO/CDMO/pharmacy/infusion excluded | +106 (89 pharma, 17 biotech) | 8/15 (IPG Health Medical Communications, BOLDSCIENCE, Propel Health, Caudex, Atlantis Health, Evolution Health, AREA 23 on Hudson, Trio) | ~50, mostly med comms |
| C. 5,001+ employees | core filter, big bands only | +15 | mix of health networks and general networks | ~7 |
| D. Health PR firms | `Public Relations and Communications Services` + pharma keywords, 51+ | +47 | ~half health-relevant (BCW, Ruder Finn, MMC/RXMOSAIC, PAN, Coyne) | ~25, Leadership campaign only (no media teams) |
| E. Small agencies | core filter, 11 to 50 emp | +519 | ~1-2/20 (earlier sample S3) | ~40, very noisy |

**Not recommended as "agencies"** (sampled, kept out):
- Hospitals and health care industries + agency keywords: 1,368, almost all hospitals and public agencies.
- Data / consulting / IT / media industries + agency keywords: 1,073. Pharma commercial-analytics consultancies (Precision AQ, ProcDNA, P360) and HCP media platforms (Doceree, HMP Global, Definitive Healthcare). These are a different segment and some are HLD competitors or partners.
- Healthcare market research (103: Konovo, Adelphi, Spherix, M3). Possible separate segment (they buy HCP panel data), but not agencies.

**Recommended expanded TAM:** core + A + B + C = **699 companies, about 315 real health agencies**, roughly double the core. Adding D (PR, Leadership only) and E (small agencies, qualifier required) gives **1,265 companies, about 380 real**. Fit falls from 60% (core) to about 30% to 45%, so a qualifier prompt at pull time is required, not optional.

Records used for this section: 100 Blitz (8 counts, 92 sample rows). Session total: 647.

## 9. Cross-check with DiscoLike and Exa (added later on 2026-11-18, Moe asked to use both)

### DiscoLike (`https://api.discolike.com/v1`, key `DISCOLIKE_API_KEY`)

Parameters taken from DiscoLike's own OpenAPI spec (`/v1/openapi.json`), not guessed.

1. **`GET /count`** (free), category `ADVERTISING_AND_MARKETING`, country `US`. Exact params: `2026-11-18-discolike-counts.json`.
   - any US ad/marketing business: 1,292,949
   - + health phrases on the website: 64,086; with 11+ employees: 13,881; with 51+ employees: 1,787
   - + health phrases AND a media/programmatic/omnichannel phrase, 11+: 5,195
   - These match any mention of the phrase anywhere on the site, so they are loose upper bounds, not a TAM.
2. **`GET /discover`** (lookalike), the useful one. `icp_text` describing US pharma/health marketing agencies with media, HCP or data work; `negate_icp_text` for hospitals, practices, staffing, CROs, manufacturers, SEO/web shops; seed domains cmimediagroup.com, realchemistry.com, klick.com, digitashealth.com, fingerpaint.com; HLD clients, HLD and adtech vendors hard-excluded; US; 11+ employees; `relevance=BALANCED`; `max_records=600`. Exact params: `2026-11-18-discolike-discover-request.json`.
   - **Returned the full 600** without reaching the relevance stop, so there are more beyond 600.
   - Fit by rank (eyeballed): ranks 1-150 about 90% real health agencies, around 300 about 70%, around 450 about 50%, around 560 about 35%. **About 400 real agencies in the 600.**
   - Size mix: 392 at 11-50, 143 at 51-200, 45 at 201-500, 20 at 501+.
   - It finds health media agencies Blitz missed entirely, e.g. Evolvics, Underscore, SSCG Media Group, AbelsonTaylor, Heartbeat, GSW, RevHealth.
   - All 600 rows: `2026-11-18-discolike-agency-lookalike-companies.csv`. Cost: 600 records, $1.50 (account spend went 15.54 to 17.04).

### Exa (`POST https://api.exa.ai/search`, `category: company`, 100 results per query)

6 queries (exact bodies in `2026-11-18-exa-search-requests.json`): US healthcare ad agency for pharma brands; pharma media agency programmatic HCP; independent health and wellness comms agency; medical communications agency; healthcare marketing data and analytics agency; omnichannel HCP engagement agency.
- 414 unique domains; **79 also in the DiscoLike 600**.
- Exa has no US or size filter. In a 40-row random sample about 17 were real US health agencies (about 43%); the rest were India/UK med comms, analytics vendors, contract sales and adtech. About 180 real agencies in the 414.
- One hit is Publicis Health Media (HLD client), so the Exa list needs the same exclusions.
- All rows: `2026-11-18-exa-agency-search-companies.csv`. Cost: $0.58.

### Blitz capture check (25 Blitz records)

30 random DiscoLike agencies (51+ employees, top 300 ranks) checked by name in Blitz (`2026-11-18-blitz-capture-check-companies.csv`):

| Where the agency sits in Blitz | Count |
|---|---|
| In the 260 core universe | 9 (30%) |
| Caught by expansion option A (broader keywords) | 4 |
| In Blitz as Advertising Services, but its description misses every keyword | 5 (Good Apple, SOLVE(D), emagineHealth, MissionOne Media, Circa Healthcare) |
| In Blitz under PR (option D) or pharma (option B) | 4 (JPA Health, Greenough, PAN, Evolution Health) |
| Not found in Blitz by name, or name matched a different company | 8 |

So the Blitz keyword filter catches about 30% of real health agencies (core) and about 55-60% with expansions A + B + D. The gap is mostly keyword misses, not missing data.

### What this does to the TAM

- **Capture-recapture** on the two independent lists (about 400 real in DiscoLike, about 180 real in Exa, about 75 real in both): 400 x 180 / 75 = **about 1,000 US health-focused agencies with 11+ employees**. This method undercounts when both tools favour the same well-known agencies, so treat 1,000 as a floor (range 1,000 to 1,200).
- About 35% of them have 51+ employees: **about 350 to 500 at 51+**, against about 155 real in the Blitz core. Blitz alone was seeing roughly a third of the market.
- **Recommendation:** use DiscoLike `/discover` as the company source for this segment (it ranks by fit and its top half is clean), run it past 600 to the relevance stop, then send those domains to Blitz/Clay for the persona people. Use Exa only to top up names DiscoLike misses.

Spend for this section: DiscoLike $1.50 (600 records; counts free), Exa $0.58, Blitz 25 records (session total 672).
