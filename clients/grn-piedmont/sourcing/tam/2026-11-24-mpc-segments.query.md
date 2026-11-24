# MPC segment read for GRN Piedmont (2026-11-24)

- **What:** sizing for splitting GRN's one MPC (open-role) campaign into segments, measured before anything is proposed (CLAUDE.md "Campaign doc standard" rule 1). Nothing is created yet: this is the read Moe approves or rejects.
- **Why:** Moe, 2026-11-24: "create more segments of the MPC campaign, based on the client's ICP".
- **Client:** GRN Piedmont, tracking_clients `3abc2243-889c-4177-a75a-3ac680766d20`. Live campaign "Recruitment Specific Campaign" `ed2f167f-5cea-4b2e-833b-20b2aafe26e0` (HeyReach 734516 + 2.0 copy 756466), config `fe214099-0834-40b6-9b18-d4517ecd03f1`.
- **Session:** claude.ai/code session_013MzxQhML2MDSCMvFCprgqD, branch `claude/grn-mpc-segments`.
- **Scope:** Campaign-specific (MPC segments). Not the full company TAM (`claude/grn-full-tam`, `sourcing/general-tam/`) or the data-source comparison (`claude/grn-icp-data-sources`, `sourcing/data-source-review/`).

## Tools and exact queries

1. **Blitz API `POST /v2/jobs/search`**, `mpc_segments_pull.py`, 120-day window. Every request body, its first-page `total_results` and the count pulled are in `2026-11-24-mpc-segments-pull.json`. 23 queries, every one paged to `cursor: null` (pulled = total in all 23), **5,388 records**.
   - Same firmographics as the live campaign (`tam_counts.py`): 201 to 1,000 employees, US HQ outside the 13 Mountain/Pacific/AK/HI states, `is_agency: false`, US job location, `FULL_TIME`, same title excludes.
   - Run once per **vertical**, a partition of the live campaign's 68 manufacturing labels into 10 groups (asserted in the script). Blitz job results carry no company industry, so this is how each posting gets one. Fire & life safety uses the live campaign's 8 contractor labels, its 5 company keywords, its own F&LS title list and the F&LS name/title gate.
   - Titles: one 71-keyword list across 6 role families, including two families the live campaign never searched: **EHS/Maintenance** (EHS, HSE, Safety, Maintenance, Reliability, Facilities) and wider **supply chain** (Logistics, Planning). Each posting is then put in **one** family by title (first match wins: executive, EHS/maintenance, supply chain/purchasing, engineering/quality, operations/plant).
   - Gates reused unchanged from `../recruitment-specific-open-roles/spec.py`: title noise, company noise, client DNC, F&LS gate. A repost (same company and title on a later date) is kept as one posting dated when it was **first** seen.
2. **`mpc_segments_size.py`** (no API calls) builds the segment table: `2026-11-24-mpc-segments-size.json` and `2026-11-24-mpc-segments-companies.csv`. It flags each company against the live campaign's files (`2026-11-16` and `2026-11-23` companies and leads).
3. **`mpc_segments_sample.py`**, seeded so it reproduces:
   - **A.** Blitz API `POST /v2/search/waterfall-icp-keyword` on up to 12 companies per family that are **not** in the live campaign (63 companies). Same tiers and excludes as the live campaign; `max_results` 5 (4 for F&LS).
   - **B.** The same call on 30 random companies that **are** in the live campaign, `max_results` 10, to see how many uncontacted persona contacts remain.
   - **C.** Is the posting still open? 40 postings aged 60 to 120 days and 40 aged under 30 days, read from the public posting page (`linkedin.com/jobs-guest/jobs/api/jobPosting/<id>`). Then 40 roles **first posted 60+ days ago and reposted in the last 30 days**, checking the latest repost.
   - 92 Blitz records. Results: `2026-11-24-mpc-segments-sample-leads.csv` (normalised with `tools/leads.py`) and `2026-11-24-mpc-segments-posting-check.csv`.

**Blitz records used in total: about 5,480.**

## Results (kept postings, 120 days, Eastern/Central, 201 to 1,000 employees)

The headline: **1,282 companies posted a matching role in 120 days; 919 (72%) already have leads in the live campaign.**

Column definitions:
- **Live:** companies that already have launch-set leads in 734516/756466.
- **Net new:** companies not live.
- **Never pulled:** net-new companies the live campaign never queried. The other net-new companies were queried on 11-16 or 11-23 and Blitz returned no persona.
- **New in last 30d:** companies whose first posting is under 30 days old and that aren't live. This is the monthly refill.
- **Live leads:** people already contacted at the live companies.

| Segment | Companies | Postings | Live | Net new | Never pulled | New in last 30d | Live leads |
|---|---|---|---|---|---|---|---|
| Executive (C-suite, President, GM, VP, finance/HR heads) | 353 | 483 | 257 | 96 | 22 | 14 | 648 |
| Operations & Plant | 542 | 772 | 433 | 109 | 5 | 18 | 1,072 |
| Engineering & Quality | 432 | 683 | 347 | 85 | 3 | 19 | 869 |
| Supply Chain & Purchasing (incl. logistics, planning) | 342 | 447 | 268 | 74 | 31 | 11 | 695 |
| EHS & Maintenance (suggestion for GRN to confirm) | 343 | 485 | 232 | 111 | 64 | 12 | 575 |
| Fire & life safety | 26 | 59 | 23 | 3 | 2 | 2 | 49 |
| Overlay: prolonged, age only (posted 60 to 120 days ago) | 888 | 1,647 | 671 | 217 | 62 | 0 | 1,634 |
| **Overlay: prolonged, reposted** (first posted 60+ days ago, reposted in last 30) | **116** | 143 | 94 | 22 | 5 | 0 | 232 |
| Overlay: multi-opening (3+ distinct roles) | 322 | 1,635 | 273 | 49 | 4 | 1 | 744 |
| Vertical: machinery & automation | 263 | 566 | 187 | 76 | 27 | 15 | 394 |
| Vertical: general / other manufacturing | 251 | 580 | 176 | 75 | 26 | 22 | 419 |
| Vertical: food & beverage | 158 | 393 | 116 | 42 | 11 | 7 | 289 |
| Vertical: plastics, packaging & paper | 138 | 261 | 106 | 32 | 8 | 5 | 233 |
| Vertical: aerospace & defense | 129 | 360 | 105 | 24 | 8 | 5 | 284 |
| Vertical: transportation equipment | 106 | 257 | 65 | 41 | 9 | 3 | 159 |
| Vertical: electrical & electronics | 96 | 194 | 62 | 34 | 11 | 10 | 162 |
| Vertical: chemicals | 74 | 189 | 53 | 21 | 12 | 3 | 126 |
| Vertical: building materials | 23 | 34 | 13 | 10 | 2 | 2 | 29 |
| Vertical: metals & fabrication | 18 | 36 | 13 | 5 | 2 | 0 | 32 |
| **All** | **1,282** | **2,929** | **919** | **363** | **118** | **74** | - |

- The role-family and vertical rows overlap with each other: one company can hire in several families. Each posting has exactly one family.
- Metals and building materials are small because Blitz files most fabricators and building-product makers under the broad labels ("Manufacturing", "Machinery Manufacturing"), not because the market is small.

### Reachability sample (tools/leads.py overlap: 48 of the 143 sample rows are in `2026-11-16-leads.csv`, 12 in `2026-11-23-leads.csv`)

| Sample | Companies | With a persona contact | Persona contacts | Already contacted | Uncontacted |
|---|---|---|---|---|---|
| A, net new: queried before with no lead | 42 | **0** | 0 | 0 | 0 |
| A, net new: never pulled | 21 | **12 (57%)** | 29 (2.4 per hit) | 0 | 29 |
| B, live companies | 30 | 30 | 63 | **60** | **3** (at 3 companies) |

- **Live companies are used up for this persona.** Waves 1 and 2 already took up to 5 C-level, VP or Owner contacts per company. At 3 in 30 sampled companies, about 90 uncontacted persona contacts remain across all 919.
- **Net-new companies queried before stay empty.** Blitz had no C-level/VP/Owner for them on 11-16 and still has none.

### Posting still open? (`2026-11-24-mpc-segments-posting-check.csv`)

| Posting set | Sampled | Still open |
|---|---|---|
| Posted under 30 days ago | 40 | 33 (83%) |
| Posted 60 to 120 days ago (age only) | 40 | **6 (15%)** |
| First posted 60+ days ago, reposted in last 30 days | 40 | **32 (80%)** |

Posting age alone does not make a prolonged-vacancy segment: most of those roles are closed. **A repost does.** It is the only form of the ICP form's "prolonged vacancies (60+ days)" signal worth messaging.

## TAM/SAM read and contacts per company

- **Small pool now; small but steady refill.**
  - Inside the ICP and persona, about 118 never-pulled companies are left. At 57% reachable that is about 65 companies and **about 160 people**.
  - Add about 90 uncontacted people at live companies.
  - Refill is about **74 new hiring companies a month** across all families, so about 40 reachable companies and **about 100 people a month**.
- **Contacts per company:** under the inverse rule a small pool means more per company. Use **up to 5** for manufacturing (as wave 2) and 4 for F&LS. That is in practice everyone Blitz returns for the persona: the sample averaged 2.4.
- **No single segment reaches the 200 to 300 company bar on net-new companies.** A segment can only be justified as a **rolling signal that refills monthly**, which the doc standard allows if stated.
- **Not in reach without changing the ICP** (Moe and GRN to decide, not proposed here):
  - Director-level contacts, which the client excludes.
  - 1,001+ or 51 to 200 employees.
  - Mountain/Pacific HQs.
  - Each would widen the pool materially; the full company TAM session (`claude/grn-full-tam`) is the place to size them.

## Role-family wording for messages 2 and 3 (proposed)

The live copy (`campaign-docs/2026-11-16-campaign-6-recruitment-specific.md`) repeats `{Job_Title_Open_}` in messages 2 and 3 instead of a family slot. Per the SOP (`docs/sops/open-role-moe-mpc.md` §3), each segment fills the slot:

| Segment | Message 2 slot ("If there's a ___ role that has been sitting open…") | Message 3 slot ("___ roles sometimes get filled quietly…") |
|---|---|---|
| Executive | senior leadership | Senior leadership |
| Operations & Plant | plant or operations leadership | Plant and operations leadership |
| Engineering & Quality | engineering or quality leadership | Engineering and quality leadership |
| Supply Chain & Purchasing | supply chain or purchasing leadership | Supply chain and purchasing |
| EHS & Maintenance | EHS or maintenance leadership | EHS and maintenance leadership |
| Fire & life safety | branch, service or operations leadership | Fire protection leadership |
| Prolonged (reposted) | same as the role's family. Message 1 swaps "Not sure if that's a fresh one or something you've had open for a bit" for "Looks like it's been reposted a few times since {First_Posted_Month}" | same as family |

## GTM Sheets Apify job-board signal (actor `LzsIpToRTUZSnqjbS`, Indeed + LinkedIn)

Read with `gtm_sheet_signals` (client Talent Edge), 2026-11-24.

**How it runs for Talent Edge:**
- Two daily signals: NY (50 mi) and London.
- Input: one `location` plus a `distance` radius, `hoursOld: 48`, `searchTerms`, `excludeCompanies` (agencies and audit firms), `excludeTitleKeywords`.
- Output: about 200 new postings a day each, deduped on `jobUrl`.

**How it fits GRN:**
- It has **no company-size, industry, HQ-state or agency filter.** GRN's ICP is firmographic (201 to 1,000 employee manufacturers across about 37 Eastern/Central states), so each GRN feed would need:
  - several metro feeds (e.g. Charlotte, Atlanta, Chicago, Detroit, Cleveland, Houston, Greenville-Spartanburg), and
  - a company-match step (Blitz company enrichment or a GTM Sheets company lookup) to drop non-ICP employers.
- Its plus is **Indeed**, which Blitz (LinkedIn postings) doesn't cover. Mid-sized manufacturers do post plant and maintenance roles on Indeed.

**Coverage comparison:** not run yet. It needs a GTM Sheets table and spends Apify credits, and creating anything waits for Moe's go-ahead. Proposed test:
- one run: Charlotte NC, 100 mi, `hoursOld` 168, GRN's titles, cap $5;
- then match its employers against the same week of Blitz postings (this file) to count companies only Apify finds.
