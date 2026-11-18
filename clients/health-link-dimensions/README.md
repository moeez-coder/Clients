# Health Link Dimensions

## Profile

- **Status:** active
- **Package tier:** Custom (`clientType: core`), $8,500/month billed monthly
- **Website:** https://healthlinkdimensions.com
- **Contact:** Robert Haglund <rhaglund@healthlinkdimensions.com> (ICP form also lists mgraham@healthlinkdimensions.com for Slack)
- **Slack channel ID:** C0CD0RXFBS4
- **HeyReach workspace:** `170993` (`heyreachConnected: true`)
- **Staff:** campaign strategist Moeez; infrastructure John Paul; closer Rueban; GTM engineer `-` (unassigned); sourcing engineer `-` (unassigned)
- **Booking link:** `-` (empty in tracking_clients)
- **DNC list:** 0 entries (`dncSkipped: false`, so not yet supplied rather than waived)
- **Infrastructure:** `{"vaSeatCount": 10}` (changed from `{}` since the 2026-11-09 sync)
- **Created in tracking_clients:** 2026-10-26 (by sales)
- **Tracking client ID:** `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`
- **Last synced:** 2026-11-18 via `get_client` + `list_sourcing_configs` (0 configs, no drift). Previous sync: 2026-11-16.

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
| HealthLink Dimensions Campaign Plan, Doc 1 (10 campaigns) | `1f2e4277-1a09-445e-8684-75cc542ab003` | `internal_review` (client commented 2026-11-11; agency copy revised 2026-11-13) | `campaign-docs/2026-11-09-doc-1.md` |

Internal discussion drafts (not in tracking_clients, not sent to the client):

- `campaign-docs/2026-11-16-mql-campaign-ideas.md`: 5 MQL campaign ideas for Moe to choose from.

Portal link: https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=1f2e4277-1a09-445e-8684-75cc542ab003

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| `-` | `-` | `-` | `-` | `-` | `-` | `-` |

No ICP configs, sourcing configs or campaigns exist in tracking_clients as of 2026-11-09. By the tracking_clients rule, none should exist until the client approves a campaign doc.

## Sourced data in this repo

No lead or company snapshots yet. A pull can only happen after the client approves doc 1. The sizing read is on disk:

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

## History

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
