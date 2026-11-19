# Health Link Dimensions

## Profile

- **Status:** active
- **Package tier:** Custom (`clientType: core`), $8,500/month billed monthly
- **Website:** https://healthlinkdimensions.com
- **Contact:** Robert Haglund <rhaglund@healthlinkdimensions.com> (ICP form also lists mgraham@healthlinkdimensions.com for Slack)
- **Slack channel ID:** C0CD0RXFBS4
- **HeyReach workspace:** `170993` (`heyreachConnected: true`)
- **Staff:** campaign strategist Moeez; infrastructure John Paul; closer Rueban; GTM engineer `-` (unassigned); sourcing engineer `-` (unassigned)
- **Booking link:** https://healthlinkdimensions.chilipiper.com/me/algoacquistion-algoacquistion (set in tracking_clients since the last sync; was empty)
- **DNC list:** 210 entries, uploaded 2026-11-19 with `update_client_dnc` (merge into an empty list): 198 unique accounts from `context/2026-11-12-dnc-accounts.csv` (199 rows, Ionis Pharma listed twice) plus the 12 named contacts from `context/2026-11-12-dnc-named-contacts.csv`. The named contacts carry their agency in `agency_note`, not `company`, so their agencies stay open.
- **Infrastructure:** `{"vaSeatCount": 10}` (changed from `{}` since the 2026-11-09 sync)
- **Created in tracking_clients:** 2026-10-26 (by sales)
- **Tracking client ID:** `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`
- **Last synced:** 2026-11-18 (Doc 2 sizing session) via `get_client` + `list_sourcing_configs`: 0 configs; one drift, the booking link is now set. DNC is still 0 entries in tracking_clients. Previous sync: 2026-11-18 (earlier session).

## Context files

Verbatim copies of tracking_clients `get_client` fields, pulled 2026-11-09. Each file carries a source header.

- `context/client-brief.md` (`clientBrief`). Generated from the client description alone, before the ICP form arrived. Many fields are marked MISSING/INFERRED.
- `context/icp-form.md` (`icpForm`). The client's own Typeform answers, submitted 2026-11-04. Raw JSON.
- `context/client-description.md` (`clientDescription`)
- `context/caller-briefing.md` (`callerBriefing`)
- `context/caller-faqs.md` (`callerFaqs`)
- `callTranscript` and `notes` are empty in tracking_clients, so there is no file for them.

## Campaign docs

| Doc | tracking_clients doc id | Status | Repo copy |
|---|---|---|---|
| HealthLink Dimensions Campaign Plan, Doc 1 (10 campaigns) | `1f2e4277-1a09-445e-8684-75cc542ab003` | `client_review` (re-sent 2026-11-18; agency Campaigns 5 and 10 replaced by persona campaigns as tracked changes) | `campaign-docs/2026-11-09-doc-1.md` |
| HealthLink Dimensions Campaign Plan, Doc 2 (12 persona campaigns, replaces Doc 1) | `fa54bc2b-ddcf-4fdd-9c71-ed512635f9c9` | `draft`, hidden from the client. Sizes and copy fixes added 2026-11-19. Moe said to skip client approval for the first two launches | `campaign-docs/2026-11-18-doc-2.md` (updated in place 2026-11-19, matches the tracking_clients doc) |

Internal discussion drafts (not in tracking_clients, not sent to the client):

- `campaign-docs/2026-11-16-mql-campaign-ideas.md`: 5 MQL campaign ideas for Moe to choose from.

Portal link: https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=1f2e4277-1a09-445e-8684-75cc542ab003

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| C1 Brand Marketing: Blitz people search + GTM Rx fit (2026-11-19) (`0c33f341-8d76-4a55-a79b-e49956afa7aa`) | C1 Pharma Brand Marketing (Doc 2) (`767826c6-f927-42c6-ba50-b7e6c4e7bd6c`) | Pharma / Biotech | ready | US \| Pharma \| C1 Brand Marketing \| v1 (`7c26af94-1a44-405c-b1e9-45bdf3258931`, running, HeyReach `747212`) | `-` (leads are in GTM, not ingested) | `-` (GTM Sheets workbook `11915594-8092-4954-95e1-ff4dcaeebd78`) |

Synced 2026-11-19 via `create_icp_config`, `create_sourcing_config`, `create_campaign`, `link_platform_campaign` and `move_campaign`, all called in this session.
- **Segment and persona:** segment `5caf1726-edab-4915-a146-c302386e5e67`, persona `071da678-c28f-4c94-be23-2575a93e9843`.
- **Lead list:** static, with `campaign_split: false` (Moe: "No split").
- **Client approval:** none. The client has not approved Doc 2, and Moe skipped approval for the first launches.

## Sourced data in this repo

**Campaign 1: Pharma Brand Marketing (Doc 2).** New segment. Lead list *C1 Brand Marketing: Blitz people search + GTM Rx fit (2026-11-19)* (`0c33f341-8d76-4a55-a79b-e49956afa7aa`), created after the pull when Moe asked for the campaign to be live in tracking_clients. Tool: Blitz API `POST /v2/search/people`. Pulled 2026-11-19. Full method: `sourcing/c1-brand-marketing/2026-11-19-leads.query.md`.

- `sourcing/c1-brand-marketing/2026-11-19-leads.csv`: 733 leads. Pull 1, at Doc 2's original cap of 2 per company (5 at 10001+).
- `sourcing/c1-brand-marketing/2026-11-19-companies.csv`: 412 companies. These went to the GTM *Rx Brand Fit* check, and 119 passed.
- `sourcing/c1-brand-marketing/2026-11-19-fit-company-slugs.txt`: 117 fit companies (119, minus 2 removed by hand).
- `sourcing/c1-brand-marketing/2026-11-19-launch-leads.csv`: 235 pull-1 leads at the fit companies. These were the first leads loaded.
- `sourcing/c1-brand-marketing/2026-11-19-leads-2.csv`: 477 leads. Pull 2, at a cap of 5/10. Superseded and never loaded.
- `sourcing/c1-brand-marketing/2026-11-19-leads-3.csv`: 432 leads. Pull 3, at 5 per company. **This is the live list** in GTM *C1 People* and HeyReach campaign `747212`.
- `sourcing/c1-brand-marketing/2026-11-19-blitz-people-cache.json`: 2,582 matched people at the fit companies, before the cap.
- Script: `sourcing/tam/c1_leads_pull.py`. Blitz records used: 3 × 3,618.

**Campaign 9: Agency Leadership (Doc 2).** New segment, no lead list yet (config `-`). Tool: Blitz API `POST /v2/search/people`. Pulled 2026-11-19. Method: `sourcing/c9-agency-leadership/2026-11-19-leads.query.md`.

- `sourcing/c9-agency-leadership/2026-11-19-leads.csv`: 821 leads at 350 agencies. Cap 10, the small-pool case under Moe's rule.
- `sourcing/c9-agency-leadership/2026-11-19-companies.csv`: 351 agencies. These are going through the GTM *Agency Fit* check.
- `sourcing/c9-agency-leadership/2026-11-19-blitz-people-cache.json`: 896 matched people.
- Script: `sourcing/tam/c9_leads_pull.py`. 899 Blitz records used.

**Before Doc 2:** no lead or company snapshots were pulled for doc 1, because a pull could only happen after the client approved it. The sizing read is on disk:

- `sourcing/tam/2026-11-09-tam-read.query.md`: the TAM/SAM read for the 5 doc-1 segments, with no config yet (config `-`).
  - Blitz API `POST /v2/search/companies` and `POST /v2/jobs/search`, counts only with `max_results: 1`, 15 records used.
  - Clay MCP `search-companies`: a 20-row fit sample for segment 1.
  - Pulled 2026-11-09.
- `sourcing/tam/tam_counts.py` and `sourcing/tam/tam_counts.json`: the script and its exact request bodies and results.
- `sourcing/tam/2026-11-09-clay-sample-seg1.json`: the Clay sample, with a fit verdict per company.
- `sourcing/tam/2026-11-18-agency-persona-sizing.query.md`: agency persona sizing (3 recommended campaigns: Leadership, Data and Analytics, Media), config `-`, Blitz API, pulled 2026-11-18, 547 records.
  - `sourcing/tam/2026-11-18-agency-persona-companies.csv`: 147 rows, companies with persona people found, from Blitz `POST /v2/company/tam-by-people`.
  - `sourcing/tam/2026-11-18-agency-universe-sample-companies.csv`: 40 rows, company fit samples with verdicts, from Blitz `POST /v2/search/companies`.
  - `sourcing/tam/2026-11-18-agency-persona-title-samples-leads.csv`: 45 rows, people title samples keyed by `linkedin_url`, from Blitz `POST /v2/search/people`.
  - `sourcing/tam/2026-11-18-discolike-agency-lookalike-companies.csv`: 600 rows, DiscoLike `GET /discover` lookalike of US health agencies (request in `2026-11-18-discolike-discover-request.json`, counts in `2026-11-18-discolike-counts.json`), pulled 2026-11-18, $1.50.
  - `sourcing/tam/2026-11-18-exa-agency-search-companies.csv`: 414 rows, Exa `POST /search` (`category: company`, 6 queries in `2026-11-18-exa-search-requests.json`), pulled 2026-11-18, $0.58.
  - `sourcing/tam/2026-11-18-blitz-capture-check-companies.csv`: 30 rows, DiscoLike agencies checked by name in Blitz `POST /v2/search/companies`, 25 records.
  - `sourcing/tam/dl.py`, `dl_counts.py`, `dl_discover.py`, `exa.py`, `capture.py`: the scripts (they read/write JSON in the working directory).
  - `sourcing/tam/agency_tam_expansion.py` + `2026-11-18-agency-tam-expansion.json`: TAM expansion options (counts and 75 sample company rows), 100 more Blitz records.
  - `sourcing/tam/persona_counts.py` + `2026-11-18-persona_counts.json`, `sourcing/tam/persona_companies.py` + `2026-11-18-persona_companies.json`: scripts with exact request bodies and results.
- `sourcing/tam/2026-11-18-doc-2-sizing.query.md`: **Campaign Doc 2 sizing**, all 12 campaigns (doc `fa54bc2b-ddcf-4fdd-9c71-ed512635f9c9`), config `-`, pulled 2026-11-18. Blitz API (about 5,560 records), Prospeo (11 credits), DiscoLike `/count` (free), Exa ($0.047), Clay (1 query), openFDA (free); AI Ark returned 403. Count-only; the CSVs below are capped list outputs and samples, not lead pulls.
  - `sourcing/tam/2026-11-18-doc-2-fit-sample-companies.csv`: 50 rows, pharma and device company fit samples with verdicts, from Blitz `POST /v2/search/companies`.
  - `sourcing/tam/2026-11-18-doc-2-title-samples-leads.csv`: 54 rows, persona title samples keyed by `linkedin_url`, from Blitz `POST /v2/search/people`.
  - `sourcing/tam/2026-11-18-doc-2-hiring-companies.csv`: 1,098 rows, companies with matching US job posts in the last 30/90 days per campaign, from Blitz `POST /v2/company/tam-by-jobs`, with a DNC/client flag.
  - `sourcing/tam/2026-11-18-doc-2-persona-companies.csv`: 2,492 rows, pharma (Campaigns 1-5) and device (Campaign 7, capped at 900) companies with persona people and their counts, from Blitz `POST /v2/company/tam-by-people`.
  - `sourcing/tam/2026-11-18-doc-2-agency-wide-persona-companies.csv`: 773 rows, agencies in the wider DiscoLike + Blitz universe with persona people, health flag and DNC flag, from Blitz `POST /v2/company/tam-by-people`.
  - `sourcing/tam/2026-11-18-doc-2-large-device-bu-companies.csv`: 137 rows, Campaign 8 persona estimates per company and business unit, from Blitz `POST /v2/search/people`.
  - `sourcing/tam/2026-11-18-doc-2-fda-drug-approvals.csv`: 393 rows, openFDA `drug/drugsfda` novel approvals and efficacy supplements, 2025-11-01 to 2026-11-18.
  - Scripts `sourcing/tam/doc2_*.py`, `dnc.py`, `prospeo_probe.py` and their raw JSON outputs `2026-11-18-doc-2-*.json`. The file list is in section 12 of the query file.

- `sourcing/tam/2026-11-19-ctgov-phase3-sponsors-companies.query.md`: ClinicalTrials.gov Phase 3 sponsors, config `-`, pulled 2026-11-19, ClinicalTrials.gov API v2 `GET /api/v2/studies` (free). Near-launch list for Doc 2 Campaigns 1 to 5 and early warning for Campaign 6.
  - `sourcing/tam/2026-11-19-ctgov-phase3-sponsors-companies.csv`: 384 rows, one per lead sponsor, with a DNC/client flag (14 flagged).
  - `sourcing/tam/2026-11-19-ctgov-phase3-trials.csv`: 898 rows, one per trial.
  - Script `sourcing/tam/ctgov_phase3.py`. Also in GTM Sheets: workbook "ClinicalTrials.gov Phase 3 sponsors (2026-11-19)", table "Phase 3 sponsors" (384 rows).

## History

- **2026-11-19**: **Campaign 9 (Agency Leadership) pull, in progress** (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`, session `session_013MzxQeLxrp2aPyVTnp1YUd`). New segment. C9 follows C1, per Moe's "make one live first and then make the other one".
  - **Pull:** Blitz people search over the 351 health agencies left after the DNC filter in the sizing universe. 896 people found, 821 leads at a cap of 10 (small pool).
  - **GTM:** *C9 Companies* rebuilt as a webhook table (`002ab742-560f-4cca-8bcd-cbd7c057ae24`) with Blitz enrichment and the *Agency Fit* AI check. 350 agencies posted.
  - **C9 People (`04b15d47-589f-40a8-8a6f-aed331fc1a8c`):** got the same fixes as C1: raw lookup paths, Research gated on agency fit, and message columns that require the research outputs.
  - **Next:** HeyReach campaign, push and tracking_clients registration.
- **2026-11-19**: **Campaign 1 (Pharma Brand Marketing) launched: GTM Sheets + HeyReach + tracking_clients** (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`, doc `fa54bc2b-ddcf-4fdd-9c71-ed512635f9c9`, session `session_013MzxQeLxrp2aPyVTnp1YUd`). New segment. Moe: "Do one at a time and make one live first", so C1 goes first and C9 follows.
  - **Structure (Moe chose this over the 4-campaign Vertical Launch):** one HeyReach campaign, *US | Pharma | C1 Brand Marketing | v1* (`747212`, list `1189465`).
    - All 8 HLD senders.
    - A blank connection request, withdrawn after 25 days.
    - `{message1}` 3 hours after acceptance (HeyReach raised the 1 hour we set), `{message2}` 3 days later, `{message3}` 4 days after that. The sequence stops on reply.
    - Mon–Fri, 08:00–17:30 Eastern.
    - The messages are written per lead in GTM Sheets before the push, so no Clay webhooks are needed.
  - **GTM workbook** *HLD C1 Pharma Brand Marketing* (`11915594-8092-4954-95e1-ff4dcaeebd78`):
    - **C1 Companies** (`34dbef44-6cbe-4540-8630-bde48ca16280`, webhook table): Blitz company enrichment, the exclusion-list lookup, and *Rx Brand Fit* (`openai/gpt-6.1-terra` with web access). 119 of 412 passed.
    - **C1 People** (`7576f0ac-3f74-45f7-bb07-7c04c0d754bf`): a lookup into Companies, and *Research* (gpt-6.1-terra with web, gated on Company Fit = yes). Research picks the person's level, a personalisation tier, a line and the best question for their level, using the persona deck worries.
    - **Messages 1, 2 and 3** in C1 People are written by `anthropic/claude-opus-5.5`. *Push to HeyReach* sends `message1`, `message2` and `message3` as custom fields, and only fires when all three exist.
    - **C1 People Inbox** (`18181eef-20e2-438a-9419-75c84f0eff79`): a webhook intake that de-dupes on LinkedIn URL and forwards new leads to C1 People.
  - **HeyReach company blacklist:** 256 entries, built from the 198 DNC accounts, the known clients, the legacy MedImmune and Zeneca pages and cleaned name variants. tracking_clients DNC was merged to 217, adding the known clients and the legacy AstraZeneca pages; before this the GTM Exclusion list refill had dropped the known clients. The campaign excludes both the lead and company blacklists.
  - **Cap: Moe, "10 if less number of people are found and 5 if more".** C1 is a large pool (2,582 people at 117 companies), so the cap is 5 per company. Live list: 432 leads.
  - **Slips, fixed:**
    - People-level fields first read computed columns through the lookup, which come back empty, so Research was skipped. Message 3 only required First Name, so it was drafted without research for about 370 rows (wasted Opus spend, about $2).
    - Fix: re-pointed the fields to the raw record paths, made all message columns require the research outputs, and re-ran everything.
  - **Launched:** HeyReach `747212` started 2026-11-19 12:55 UTC (IN_PROGRESS). The first lead was pushed and its custom fields checked in HeyReach, then the rest were pushed as their messages finished.
  - **tracking_clients:** Moe said "Make it live in tracking clients aswell". This session created the ICP config, segment, persona, lead list and campaign (IDs in the Sourcing configs table), linked HeyReach `747212` and moved the campaign to **running**.
  - **Housekeeping:** the old launch session `session_013MzxQg3nJX88Ucm6tmv4To` was archived. It had the old copy and never built anything.
- **2026-11-19**: **Campaigns 1 and 9 rewritten: no connection note, no open-role hook** (doc `fa54bc2b-ddcf-4fdd-9c71-ed512635f9c9`, client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`, session `session_013MzxQeLxrp2aPyVTnp1YUd`).
  - **Moe:** "Open role i think is not a good relevancy point in case of this client." He asked for Message 1 to read "{First Name}, Thanks for connecting. [something to personalise with] [a genuine question]", and for the connection request message to be removed.
  - **What changed:**
    - Connection requests now go out blank.
    - Message 1 is the thanks, a personalisation line and a question, with three tiers. Campaign 1 uses a brand event, then a Phase 3 readout, then the person's brand. Campaign 9 uses a client win, then agency news, then the agency's health focus.
    - The pitch (Provider Insight Report for Campaign 1, a client-ready HCP audience brief for Campaign 9) moved to Message 2.
    - Hiring is no longer a trigger for these two campaigns; the "new hire" closers are gone.
  - **Applied** in tracking_clients (40 tracked edits, all accepted, still a hidden `draft`) and in `campaign-docs/2026-11-18-doc-2.md`. Campaigns 2 to 8 and 10 to 12 still use the hiring-signal copy, and the doc says so.
  - **Launch session** `session_013MzxQg3nJX88Ucm6tmv4To` was told to use this copy.

- **2026-11-19**: **DNC uploaded; ClinicalTrials.gov sponsors pulled; Doc 2 updated with sizes; Moe skips client approval for the first launches** (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`, session `session_013MzxQeLxrp2aPyVTnp1YUd`).
  - **Moe's decision:** "We will skip the approval for now." The first two live campaigns go out without the client signing Doc 1 or Doc 2. Recommended pair: Campaign 1 (Pharma Brand Marketing) and Campaign 9 (Agency Leadership). The HeyReach build is handed to a new session, because the HealthLink Dimensions HeyReach connector only appeared mid-session.
  - **DNC (Moe: "Take the DNC from the Slack chat and upload it"):**
    - tracking_clients `update_client_dnc` (merge), 210 entries: 198 accounts and 12 named contacts.
    - GTM Sheets "Exclusion list" workbook: 203 company rows (the 198 DNC accounts, plus AstraZeneca, Alexion, Allergan, Kite Pharma and EVERSANA as known clients). The table did not refill itself after the tracking_clients update, so the rows were inserted by hand.
    - The 12 named contacts are a separate "DNC named contacts (person only)" table, so their agencies (WPP, Omnicom, VML, 22Squared, Havas, Publicis) are not blocked.
    - AstraZeneca, a known client, is not on the Slack DNC list. It is excluded in our lists, but HLD should confirm it.
  - **ClinicalTrials.gov:** Moe asked whether the MeetLife / MX Life Sciences clinical-trials scraping was relevant to HLD. It is, as a near-launch and new-indication signal (not for investigators). 898 Phase 3 trials and 384 sponsors; files and GTM Sheets table are listed under Sourced data.
  - **Doc 2 updated** in tracking_clients (22 tracked edits, all accepted, still a hidden `draft`) and in the repo copy:
    - sizes for all 12 campaigns
    - contacts per company, with higher caps at the largest pharma companies
    - the ClinicalTrials.gov near-launch rule (Campaigns 1 to 5) and early warning (Campaign 6)
    - fact-check fixes: IMAAVY's wAIHA indication is approved; SEPHIENCE is at "over 90%" of centers
    - launch order changed to Campaigns 1 and 9 first
  - **Correction to the 2026-11-18 sizing:** the DNC matcher missed "SOLVE(D), a division of IPG Health" (and would have missed "Ionis Pharmaceuticals"). `dnc.py` is fixed, and the corrected agency numbers are in section 14 of the sizing query file. Investment is now 31 people at 12 agencies, Planning 271 at 91, D&A 226 at 91, and Leadership 938 at 352.
  - **Process slip, caught and reverted:** a re-run of `doc2_export_csv.py` overwrote the dated `2026-11-18-doc-2-hiring-companies.csv`. It was restored from git before commit (append-only rule).

- **2026-11-18**: **Campaign Doc 2 sized, all 12 campaigns** (doc `fa54bc2b-ddcf-4fdd-9c71-ed512635f9c9`, client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`, config `-`). File: `sourcing/tam/2026-11-18-doc-2-sizing.query.md`. Session `session_013MzxQeLxrp2aPyVTnp1YUd`.
  - **Why:** Moe asked for sizing of every segment in Doc 2, using all tools and cross-checking between them. This is for Doc 2, not Doc 1.
  - **Segments:** Campaigns 1 to 8 are new segments (pharma personas, triggers, device). Campaigns 9 to 12 expand the existing agency segment.
  - **Results (post-DNC people; contacts per company from the inverse TAM rule):**
    - Brand 3,618 people at 441 companies, 2 per company.
    - Media/Omni 1,351 at 186, 3 per company.
    - Comm Ops 1,551 at 411, 2 per company.
    - D&A 2,829 at 282, 2 per company.
    - Market Access 2,388 at 272, 3 per company. It is far above 150, so keep it separate and do not merge into Campaign 3.
    - Big pharma (50+ persona people) gets a higher cap.
    - About 2,840 pharma leads in the full universe, about 470 a month from 30-day hiring.
    - New Indication: 2 to 4 qualifying events a month, so keep it small.
    - Specialist device: about 2,700 real companies, about 225 leads a month on triggers.
    - Large device: 22 companies, about 3,440 persona people, about 190 leads in the first wave.
    - Agencies on the wider DiscoLike universe: Leadership about 1,000 people at 353 agencies; Investment 38 at 13 (too small alone, kept separate per Moe); Planning 293 at 92; D&A 250 at 92. About 970 agency leads.
  - **DNC impact:**
    - Pharma: -19% of people, mostly AbbVie, Gilead, Takeda and AstraZeneca.
    - Agencies on the Blitz core: -26%. Investment fell from 40 to 5 people because of CMI Media Group.
    - Named contacts: 0 to 3 people.
    - "Verve Therapeutics" was a false-positive match against the DNC adtech "Verve" and is not removed.
    - Publicis Health, Deerfield Group and Bausch + Lomb are flagged for Moe.
  - **J&J/PTC fact-check:**
    - ICOTYDE psoriasis approval: true. Its PsA Phase 3 data at ACR 2026: true.
    - RYBREVANT FASPRO head and neck approval (2026-11-05): true.
    - IMAAVY wAIHA "under review": false, it was approved 2026-08-24, so the copy needs fixing.
    - IMAAVY Sjögren's Phase 3: true.
    - CAPLYTA acquisition: true.
    - SEPHIENCE "all centers prescribing": unclear, PTC says over 90%.
    - PTC Fabry (ST-920) acquisition: true, closed around September 2026.
  - **Tools:**
    - AI Ark returns 403 (plan or billing).
    - Clay MCP gives no totals.
    - Prospeo person search is exact-title only.
  - **Spend:** under $1 cash, plus about 5,560 Blitz plan records.
  - **Profile:** resynced; the booking link drifted (it is now set).
  - **Not done, on purpose:** no doc edit or send, no configs, no HeyReach, no client message.

- **2026-11-18**: **Campaign doc 2 created as a hidden draft** (`create_campaign_doc`, doc `fa54bc2b-ddcf-4fdd-9c71-ed512635f9c9`, "HealthLink Dimensions Campaign Plan, Doc 2", status `draft`, `shared_with_client: false`). Moe said not to send it to the client. Repo copy: `campaign-docs/2026-11-18-doc-2.md`, the same markdown that was submitted. Session `session_013MzxQeqnTt4RM93i4VniUQ`.
  - **Why:** Moe asked for a new doc built from the persona approach rather than further edits to doc 1.
  - **Sources:** both persona decks (`context/agency-personas-cwm.md`, `context/pharma-personas-pab.md`), Parris's Doc 2 draft (`context/2026-11-13-tailored-campaigns-doc2-pab.md`), the 16 Nov call notes and the DNC list.
  - **Structure (12 campaigns):**
    - Pharma personas 1 to 5: Brand Marketing; Media/Omnichannel; Commercial Ops + Field Sales, merged because their pains and triggers match; Data & Analytics; Market Access.
    - 6: New Indication / New Specialty trigger. This is Parris's J&J and PTC accounts turned into a reusable trigger.
    - 7: Specialist device, doc 1 Campaigns 3 and 8 merged.
    - 8: Large device by business unit (Parris's Campaign B).
    - 9 to 12: Agency Leadership, Investment, Planning and Activation, Data and Analytics, with copy unchanged from doc 1.
  - **Signals and seniority:** doc 1's trigger campaigns (Launch, Funding, New Leader) became signal variants inside each persona campaign. Seniority levels are copy tiers, not separate campaigns.
  - **Offer:** the Provider Insight Report, teased in the message and shown on the call (16 Nov decision). The call to action is left as a question, because Robert wants a calendar link instead.
  - **Copy changes from Parris's draft:** his "best of luck" was replaced to follow the no-"best" rule. The brand facts are his and are flagged to be verified the week each message is sent.
  - **Medical Affairs** is left as an open question: the persona deck includes it, but the Doc 2 draft excludes it.
  - **Open:**
    - Pharma sizing is not run yet; the doc says "being counted". Moe has not approved the Blitz count calls.
    - Agency and device sizes are pre-DNC.
    - Contacts per company: 2 for pharma personas (large TAM), 3 for Market Access, and agency counts unchanged.

- **2026-11-18**: **Client documents from Slack saved to `context/`** (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`, session `session_013MzxQeqnTt4RM93i4VniUQ`). Moe asked for them to be analysed for new campaigns. All three came from Slack #client-health-link-dimensions-algoacquisition.
  - `context/pharma-personas-pab.md`: Parris's Pharma personas deck (posted 2026-11-17), verbatim. It covers 7 functional teams (Brand Marketing, Commercial Ops, Media/Omnichannel, Data & Analytics, Market Access, Medical Affairs, Field Sales), each at 3 levels with 8 attributes, and maps the teams to Profile, Enrich, Engage and Pulse.
  - `context/2026-11-13-tailored-campaigns-doc2-pab.md`: Parris's "Tailored Campaign Plan, Doc 2" (posted 2026-11-13), verbatim. It has three account-level campaigns: J&J Innovative Medicine, large HCP-facing device companies, and PTC Therapeutics.
  - `context/2026-11-12-dnc-accounts.csv` (199 accounts) and `context/2026-11-12-dnc-named-contacts.csv` (12 people, header plus a footnote row): Robert's DNC list (posted 2026-11-12, `Do_Not_Call_List_Updated_Exclusions_CWM.xlsx`).
    - This list was supplied six days ago, but the Profile above still says DNC is 0 because tracking_clients has not been updated.
    - Checked against the agency persona universe: about 10 of the 147 agencies are on the DNC (CMI Media Group, Fingerpaint, GSW/Syneos Health, Health Monitor, Hibbert, InStep, Publicis Health entities, MJH, Vaniam), so the agency sizes in doc 1 are overstated.

- **2026-11-18**: **Agency persona campaigns written into doc 1, replacing Campaigns 5 and 10** (doc `1f2e4277-1a09-445e-8684-75cc542ab003`, client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`). File: `campaign-docs/2026-11-18-doc-1-agency-persona-campaigns.md`. Session `session_013MzxQeqnTt4RM93i4VniUQ`.
  - **Why:** Moe asked for one campaign per persona from Christopher's deck (`context/agency-personas-cwm.md`) and the 16 Nov call, with each persona messaged on its own terms.
  - **4 campaigns, not 3.** Moe kept Investment as its own campaign, which overrides the sizing entry below. Sizes come from that sizing run:
    - A Leadership: 539 people at 140 agencies, 2 per agency.
    - B Investment: 40 at 6, up to 5 per agency.
    - C Planning and Activation: 157 at 39, up to 5 per agency.
    - D Data and Analytics: 159 at 45, up to 4 per agency.
    - Each campaign's signal is an open role or a new client win.
  - **Doc ops (all via `review_campaign_doc`, author "Algo Acquisition"):**
    - Accepted the client's copy changes 1 to 38.
    - Tracked-deleted paragraphs 122 to 149 (Campaign 5) and 245 to 268 (Campaign 10).
    - Updated the intro paragraph [2] to say "Twelve campaigns" and "Campaigns 1 to 4", and pointed to the persona campaigns.
    - Inserted the persona section as one tracked insert after paragraph 275, before the offers section. It is plain text, not heading-formatted.
  - **Doc state:** `client_review`, so the client can already see the tracked changes. It was not re-sent.

- **2026-11-18**: **Agency persona campaigns sized** (expanding the existing agency segment, doc 1 segment 5; no config, config `-`). File: `sourcing/tam/2026-11-18-agency-persona-sizing.query.md`.
  - **Campaign count: 3, not 4.** Leadership; Data and Analytics; Media (Investment + Planning and Activation merged). Investment alone is only 6 companies / 40 people inside health agencies, and its Advocates row is identical to Planning's. Levels are copy tiers inside each campaign, not separate campaigns.
  - **Universe:** Blitz `POST /v2/search/companies`, ad/marketing industries + pharma keywords, US, 51 to 5,000 emp, excluding Publicis Health Media, EVERSANA, Relevate Health, HLD itself and identity/adtech vendors: 260 companies, 60% fit in a 20-company sample (about 155 real).
  - **People (Blitz `POST /v2/search/people`, US):** Leadership 539 at 140 companies; Data and Analytics 159 at 45; Media 197 at 40 (Investment 40 at 6, Planning 157 at 39). Title filters are mutually exclusive by priority, so no person is double counted.
  - **Contacts per company (inverse rule, small TAM):** Leadership 2, Data and Analytics up to 4, Media up to 5. Expected about 510 leads in total.
  - **Records:** 547 Blitz records (no step over 500); Clay 0.
  - **TAM expansion (Moe asked for a larger TAM):** recommended core + broader health keywords + health agencies filed under pharma/biotech + 5,001+ health networks = 699 companies (about 315 real, up from about 155). With health PR firms and 11-50 agencies: 1,265 (about 380 real). Fit drops to 30-45%, so a qualifier is required. 100 more Blitz records (session total 647). Details in section 8 of the query file.
  - **DiscoLike + Exa cross-check (Moe asked to use both):** DiscoLike lookalike returned 600 US health agencies (about 400 real, list not exhausted); Exa 414 (about 180 real); 79 in both. Capture-recapture puts the market at about 1,000+ US health agencies with 11+ employees, about 350 to 500 at 51+. Blitz's core keyword filter only catches about 30% of them (mostly keyword misses). Recommended DiscoLike as the company source for this segment. Spend: DiscoLike $1.50, Exa $0.58, Blitz 25 records. Section 9 of the query file.
  - **Why:** Moe wants the agency campaigns segmented by Christopher Martin's persona deck. **Not done, on purpose:** no configs, no full pull, no HeyReach, no client message. Moe decides next steps.
  - Profile resynced from tracking_clients (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`): no drift, still 0 sourcing configs. Session: claude.ai/code session_013MzxQguARXeFKghchjnaJ4.

- **2026-11-18**: Added `context/2026-11-16-client-call-notes.md` (from Fathom recording 203556039) and `context/agency-personas-cwm.md`.
  - The personas file is the verbatim text of Christopher Martin's "Agency_Personas_HLD_CWM.pptx", emailed 2026-11-16, Gmail thread `1a1e5719af1fc633`. The .pptx itself is not committed.
  - **Why:** the call replaced generic freebies with persona-specific offers and the Provider Insight Report, and Moe wants the agency campaigns segmented by persona. A new session is sizing those persona campaigns.

- **2026-11-16**: **MQL campaign ideas drafted for discussion with Moe.** Nothing was built.
  - **Moe's question:** "what could be an MQL (marketing qualified lead) campaign? Something that will increase the reply ratio."
  - **File:** `campaign-docs/2026-11-16-mql-campaign-ideas.md`. It has 5 ideas, each with segment, asset, connection request, Message 1, MQL definition and handoff:
    1. a one-question reach poll
    2. specialty counts
    3. a first-launch checklist
    4. a client-ready audience one-pager for agencies
    5. email engagement benchmarks
  - **Why:** the client's doc 1 comments 1, 2, 4, 6 and 12 say the copy sells too much and asks for too much. These ideas ask for one word in Message 1, and none uses the free data review as the hook.
  - **Recommended to Moe:** Idea 1 across all segments first, with Idea 4 for agencies and Idea 2 for pharma, biotech and device.
  - **Not done, on purpose:** no edit to doc `1f2e4277-1a09-445e-8684-75cc542ab003`, no configs, no lead pulls and no client message, until Moe picks an idea and says go.
  - **Resync:** profile resynced from tracking_clients (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`). The only drift was infrastructure, now `{vaSeatCount: 10}`.

- **2026-11-16**: **Offers section in doc 1 reworded as potential offers for the client's feedback** (Moe: "the offer and the freebie are all potential offer and freebie which the client has to give their thoughts on").
  - **How:** our own tracked insert (change 39) was rejected and replaced with a reworded insert after paragraph 275, via `review_campaign_doc`.
  - **New wording:** the section is now headed "Potential offers and freebies (for your feedback)". Every item is labelled "Potential guarantee" or "Potential freebie".
  - **What it asks the client:** keep, change or drop each item; add their own offers; and give their view on the freebie-first versus guarantee-first split.
  - **Doc state:** 39 open changes and 15 open comments. Not re-sent.

- **2026-11-13**: **Offers section drafted for the bottom of doc 1, not yet applied.**
  - **Contents:** a general guarantee offer and a free offer per segment: pharma and biotech, medical device, and agencies. Hospitals and health plans are listed as future segments.
  - **Basis:** healthlinkdimensions.com claims, read on 2026-11-13.
  - **Why:** the client called the first draft "very generic". Moe asked for KPI-led guarantee and freebie offers, generalised by segment rather than by campaign.
  - **Status:** saved as `campaign-docs/2026-11-13-doc-1-offers-section.md`. The first attempt failed on a platform-wide connector outage, which also blocked child session `session_013MzxQfSmtfQiwfMbjouvPq`. **Applied later on 2026-11-13** in this session as one tracked insert after the last "Before launch" bullet (paragraph 275). The doc now has 39 open changes and 15 open comments. It has not been re-sent to the client.
  - **Approval needed:** HLD must approve every guarantee term.

- **2026-11-13**: **Doc 1 revised for the agency campaigns using the client's own copy** (`review_campaign_doc`, doc `1f2e4277-1a09-445e-8684-75cc542ab003`).
  - **Status:** `internal_review`, since the client left 15 comments on 2026-11-11.
  - **Moe's instruction:** wherever the client supplied full replacement copy, apply it.
  - **Campaign 5** (agencies, open roles) and **Campaign 10** (agencies, account wins): the connection request and messages 1 to 3 were replaced word for word with the client's text (comments 8 to 11 and 13 to 16). That is 38 tracked changes, applied with `review_campaign_doc` rather than `replace_markdown`, so no comments are lost.
  - **Replies posted** on comments 4 to 6 and 8 to 16.
  - **Still open, because the client did not supply copy:**
    - comments 1 and 2: the free-data-review offer and a "too salesy" Message 1, which affect campaigns 1 to 4 and 6 to 9
    - comment 3: med device should reach titles beyond HCPs (campaigns 3 and 8)
    - comment 12, second half: a separate sequence for newly appointed agency leaders in campaign 10
  - **Doc not yet re-sent.** `campaign-docs/2026-11-09-doc-1.md` stays the as-sent version.

- **2026-11-09**: **Campaign doc 1 sent to the client** (`send_campaign_doc_to_client`, on Moe's explicit instruction: "Make the doc and send it to the client").
  - Status is now `client_review` and the doc is shared in the portal. The Slack notification went to C0CD0RXFBS4 (`notified_client.ok: true`).
  - **Next:** wait for the client's comments. When the status becomes `internal_review`, respond with `review_campaign_doc`, not `replace_markdown`.
  - **Nothing created** in ICP, sourcing or campaign configs, or in HeyReach.
- **2026-11-09**: **Campaign doc 1 created** (`create_campaign_doc`, doc `1f2e4277-1a09-445e-8684-75cc542ab003`, "HealthLink Dimensions Campaign Plan, Doc 1"). The repo copy is `campaign-docs/2026-11-09-doc-1.md`, with the same markdown that was submitted.
  - **Campaigns 1 to 5 are MPC (open-role) campaigns**, one per ICP-form segment.
    - The connection note and the Message 1 opener follow the SOP copy verbatim.
    - The "candidate" slot becomes the client's own offer, a free HCP data review, following the twoHundred non-recruiter precedent.
    - Each message goes to the leader above the open seat.
    - `{jd_phrase}` maps to the JD Phrase AI column described in the SOP, Step 7a.
  - **Campaigns 6 to 10 are trigger variants of segments 1 to 5:**
    - 6: FDA approval or PDUFA date
    - 7: funding or M&A
    - 8: FDA device clearance
    - 9: a new leader in their first 90 days
    - 10: agency account wins
    - Their copy follows the campaign-plan-builder format: a connection note with proof, then Message 3 opening with "Asking because".
  - **Contacts per company follow the inverse rule.**
    - The MPC pools are small, about 60 to 250 hiring companies per 90 days. So segments 1 to 4 get 3 to 4 contacts per company, agencies get 2, triggers 6 to 8 get 3, trigger 9 gets 1 (the new leader only) and trigger 10 gets 2.
    - The read behind this is in `sourcing/tam/2026-11-09-tam-read.query.md`.
  - **New segments.** The TAM read for each one:
    - Blitz company TAM: 3,090, 22,169 (noisy), 5,508, 553 and 3,317.
    - 90-day matching postings: 205, 264, 272, 337 and 1,862 (the agency figure is not filtered to health).
  - **The client's ICP form and the brief disagree.**
    - The ICP form's segments differ from the brief's: there are no hospitals, health plans or CME. Moe chose the ICP form.
    - The brief's segments 1 (pharma) and 4 (agencies) map to doc segments 1, 2, 4 and 5. The device segment appears only in the ICP form.
  - **Flagged in the doc's "Before launch" section:**
    - The DNC and client-list exclusions are empty. The Clay sample already hit 3 existing clients: EVERSANA, Incyte and Allergan/AbbVie.
    - Reply owner and booking link are still needed.
    - The client needs to approve use of the "11 of 15 largest pharma" claim, which is website-sourced.
  - **HeyReach:** no connector for workspace 170993 is visible in this session. Moe says he added a "healthkit" connector, but it does not show up here; a fresh session should pick it up. It is needed only for the post-approval dedupe.
  - **Not done:** the MPC SOP (`docs/sops/open-role-moe-mpc.md`) and the shared tooling still live on unmerged branches. They were read only, not copied.
- **2026-11-09**: Moe answered the three questions that were blocking campaign doc 1.
  - **MPC = "Most Placeable Candidate"**, the open-jobs campaign. Confirmed against the SOP `docs/sops/open-role-moe-mpc.md`, which is on branch `origin/claude/cg-open-role-campaigns` and not on main. Its worked example is C&G, and its proven copy runs at a 19.4% reply rate for Talent Edge and Alcor.
  - **Non-recruiter precedent:** twoHundred (branch `origin/claude/twohundred-init`, doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51`, campaigns 8–10).
    - The live posting is the hook, and the message goes to the hiring manager above the open seat.
    - Since the client has no candidates, the "candidate" slot becomes one ready-made deliverable.
  - **Campaigns 6–10** are trigger-based variants of segments 1–5.
  - **Segments** follow the client's own ICP form (submitted 2026-11-04), not the earlier auto-generated brief. The five segments:
    1. Specialty pharma and commercial biotech
    2. Pre-launch and newly launched biotech
    3. Specialist med device
    4. Large pharma brand/data teams
    5. HCP agencies with media or programmatic arms
  - **Dropped for now:** the brief's hospitals, health plans and CME segments. They appear in the brief only, not in the client's form.
- **2026-11-09**: Folder created from `clients/_TEMPLATE/README.md`. Profile synced from tracking_clients (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`), and brief, ICP form, description and caller notes saved to `context/`. This is the first session for the client: it starts campaign doc 1 (10 campaigns, the first 5 being one MPC campaign per segment). The orchestrator resolved Moe's "healthkit" to this client, which is the only "health" match in `list_clients`. Session: claude.ai/code session_013MzxQeqnTt4RM93i4VniUQ.
