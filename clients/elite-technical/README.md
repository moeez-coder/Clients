# Elite Technical (tracking_clients: "Elite Technical ")

> An IT and engineering staffing firm (contract and direct hire) based in Heathrow, Florida, with a large DC Metro footprint. It has 34 years in business, 400+ clients and 4,500+ placements, is woman-owned (WOSB/WBENC) and holds a DoD Top Secret facility clearance. The client's context from tracking_clients is saved verbatim in [`context/`](context/):
> - [ICP form](context/icp-form.md), submitted 2026-10-22
> - [caller briefing and FAQs](context/caller-briefing.md)
> - [DNC list](context/dnc-list.csv), 160 rows
>
> tracking_clients has no client brief, client description or call transcript.

## Profile

- **Status:** active (isApproved: true, isAlgo: false), created 2026-10-22 by `sales`
- **Package tier:** Standard
- **Website:** `-` in tracking_clients (`website` is blank). The ICP form and caller briefing both give https://www.elitetechnical.com/
- **Contact:** Joseph Monaco <jmonaco@elitetechnical.com>. The ICP form also asks for Slack invites for jjkeller@, pmosca@ and mgerardo@elitetechnical.com.
- **Staff:**
  - GTM engineer and campaign strategist: moeez@algoacquisition.ai
  - Infrastructure: john.paul@algoacquisition.com
  - Closer: rueban@algoacquisition.ai
  - Sourcing engineer: `-` (unassigned)
- **Slack channel ID:** C0CC9P7M8JC
- **HeyReach workspace:** `170370` (heyreachConnected: true). In sessions this is the HeyReach connector `mcp__18d10a27-ea89-4cf6-85b4-c7cc82b76e83__*`, the only connector whose `list_workspaces` returns 170370. Instantly, Smartlead and PlusVibe are not connected, and masterInboxWorkspaceId is `-`.
- **Infrastructure:** not submitted to infra (`infrastructure` is `{}`).
- **Booking link:** `-` (blank)
- **Gaps in tracking_clients:** these are recorded, not filled by guessing.
  - `website`, `clientBrief`, `clientDescription` and `callTranscript` are empty.
  - SDR defaults (headline, about, position, location, banner) are empty.
  - There are no ICP configs, sourcing configs or campaigns.
- **DNC:** `dncList` has 160 entries and `dncSkipped` is false. All 160 are historical clients scraped from `elitetechnical.com/for-business/clients-served/`. Every row has the status "Review before outreach; exclude pending account-owner confirmation". **No row has a domain** (`Company Domain (verify)` is blank on all 160), so exclusion has to match on company name.
  - By industry: Aerospace & Defense 53; Commercial Enterprise/Financial/Media 43; Health Care/Medical Device 21; Systems Integrators 16; Emerging Technology 14; Federal & State Governments 13.
  - None of the five "dream companies" in the ICP form (AeroVironment, TransMedics, Varonis, Tenable, Commvault) is on the DNC list.
- **Tracking client ID:** `254dc33b-4f9f-4712-9b6b-eca49c5a5ffc`
- **Last synced:** 2026-10-29 via `get_client` + `list_sourcing_configs` (+ `list_icp_configs`, `list_campaigns`)

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| USAspending awards (60d) + Blitz/Clay — Cleared Talent Fed Contracts | Cleared Talent for New Federal Contracts | Government Contractors, IT Services, Engineering, Defense, Research | ready | 1 | 0 (leads live in this repo; see note) | `-` |
| TheirStack/Coresignal live postings (30d) + Blitz contacts — C8 Role Behind the Posting | The Role Behind the Posting | Technology, Financial Services, Health Care, Defense and Space | draft | 1 | 0 | `-` |
| TheirStack remote/hybrid tech roles + Blitz TA contacts — C9 Candidate Fraud | Candidate Fraud in Technical Hiring | Technology, Financial Services, Health Care, Defense and Space | draft | 1 | 0 | `-` |
| Job-change (90d) senior IT/Eng via Clay/Blitz — C10 New Seat Fresh Team | New Seat, Fresh Team | Technology, Financial Services, Health Care, Defense and Space | draft | 1 | 0 | `-` |
| Eng hiring surge/program news + Blitz contacts — C2 Program Ramp | Engineers for the Program Ramp | Defense and Space Mfg, Aerospace Components, Engineering Services, Defense Electronics | draft | 1 | 0 | `-` |
| Open security eng roles + Blitz contacts — C3 Security Talent | Hiring Security Talent Without the Fraud Risk | Computer and Network Security, Software Development, Data Infrastructure | draft | 1 | 0 | `-` |

The five draft rows above were created 2026-10-30 from this session's own `create_*` calls, not a re-pull. They are static, `campaign_split: false`, with no Clay table, and none has leads yet.

Lead list (sourcing config) `f52caf59-e687-4ec4-94de-5d4d2862bc55` was created 2026-10-29: Custom module, static, `campaign_split: false` (Moe's choice: every linked campaign gets every lead), no Clay table or workbook.

ICP config **Cleared Talent for New Federal Contracts** `d286c219-eb64-4aa8-bccf-3a800c3e4d08` was created 2026-10-29:
- segment `16e8421d-b9e3-4c44-a4b9-cb80714bbdad`: 501–10,000 employees, DC Metro then East Coast then Midwest, signal "federal award in prior 60 days"
- persona `df04cee8-a69d-4b48-ac84-6d6e3657417f`: VP/Director, with the client's IT/Eng/TA titles
- the qualifier text holds the $100M–$1B hard filter

## Campaigns (tracking_clients)

**Campaign 1, "Cleared Talent for New Federal Contracts"**: campaign `46e24967-fdc8-4d7e-8c04-0e5e8af84afe`, status **`running`** (moved 2026-10-30 via `move_campaign` → mark-running, on Moe's instruction), linked to lead list `f52caf59-…` and persona `df04cee8-…`. The client approved it by email on 2026-10-28; see [context/2026-10-28-campaign-1-approval.md](context/2026-10-28-campaign-1-approval.md).
- The structured 4-step sequence (connection request plus 3 DMs, with `{{module.custom.contract_or_agency}}`) was saved through `set_campaign_sequence` and passed validation. The freeform `linkedin_sequence` also has the manual positive-reply step.
- The HeyReach link can't be set: `link_platform_campaign` supports only Smartlead for new-system campaigns. HeyReach `693168` is recorded in the campaign notes instead.
- **Reply handling** (Moe, 2026-10-29): Algo triages replies in the HeyReach/dashboard inbox and hands interested prospects to Elite (Joseph/Phil/Mike/Jeff) for the personal response, as Joseph's doc asks. No calendar link until a prospect shows interest.
- The other 9 proposed campaigns are **not approved**: Joseph will review them one by one.

### Campaigns 8, 9, 10, 2, 3 — set up as drafts 2026-10-30 (not client-approved)

On 2026-10-30 Moe asked to set up the "top 5" campaigns from the Oct 26 proposal doc (Google Doc `1Xt95ZV3VODh6TKRUEwwn2gfWgzo21DCv_i9yPo9qv-4`, "Elite Technical Outbound Campaigns, 26 October 2026").
- Moe picked campaigns 8, 9, 10, 2 and 3: the next five after Campaign 1 in the doc's suggested launch order.
- **All five are drafts.** No leads are loaded and nothing has started, because Joseph's 2026-10-28 approval says "Do not launch the remaining nine campaigns without separate approval".
- Copy is the Oct 26 doc's text, unchanged and with the default offer. It is in [campaigns/2026-10-30-campaigns-2-3-8-9-10-copy.json](campaigns/2026-10-30-campaigns-2-3-8-9-10-copy.json).
  - The structure matches C1: connection request, message 1 three hours after acceptance, then +7 days and +7 days, each exiting on reply.
  - The doc's "when they say yes" message is a manual reply.
- Each campaign has its own ICP config, segment, persona and lead list. Each qualifier carries the $100M–$1B revenue hard filter, which Joseph said applies to all ten campaigns.
- HeyReach (workspace 170370): every campaign is DRAFT with all 11 senders, the 7-day 08:00–17:00 America/New_York schedule and the same exclusions as C1. Each sequence was read back with `get_campaign_sequence` and matched what was sent.
- Fallback copy drops each custom variable and is only used when a lead lacks the field.

| # | Campaign | tracking_clients campaign | ICP config / persona | Lead list | HeyReach campaign / list | Offer | Custom vars |
|---|---|---|---|---|---|---|---|
| 8 | The Role Behind the Posting | `70e7eda4-c094-45da-8b4e-da6305527261` | `5a45a70c-f5a8-44ff-a41a-aab977a0c3aa` / `8fa09e7c-152b-4d14-bd7f-143faa5b6857` | `82457586-7a88-4943-80b3-5552c1fc2d94` | `695764` / `1086161` | B | role_title, location, key_skills |
| 9 | Candidate Fraud in Technical Hiring | `413dfae6-ff9e-4335-9e9f-73ff347f9b9c` | `935c0326-200a-464d-88e0-b6a0952cf95e` / `dd9eca26-6774-4301-9aa2-fbbd89c69a2c` | `78d2a5a3-2dc4-49be-afa1-43d44235a0b5` | `695765` / `1086162` | A | - |
| 10 | New Seat, Fresh Team | `d2d02a2c-a147-420d-af05-27d76bd19064` | `790aa42b-7e14-4e58-a31a-ae6e529e8b87` / `02cfd049-0147-4a2f-8254-6595d82dfbd3` | `fcd62dbd-f43a-46d0-b07b-2271569412e3` | `695766` / `1086164` | B | new_role |
| 2 | Engineers for the Program Ramp | `549697ad-d2f5-4226-952a-e9999fb6092c` | `7e296131-0361-438b-96b8-74b15d0a421b` / `371a2f2d-eea0-4fa5-884c-f94e5c840c93` | `70f4cd52-6d09-4902-b38b-79af38253826` | `695767` / `1086165` | B | program_or_product, engineering_focus |
| 3 | Hiring Security Talent Without the Fraud Risk | `4dedf327-4b4d-40a0-b284-56beb2be9f29` | `026c3a22-1de1-4f39-820d-1136c14831ad` / `8885ecca-9236-4f83-990a-f1d4d33ffc7a` | `77a81db4-8496-4bdc-a8cb-7e58025f14e5` | `695768` / `1086166` | A | security_focus |

**Before any of these can go live:**
1. Joseph has to approve them.
2. The copy probably needs Joseph's C1 rewrites applied. In C1 he dropped the formal "complimentary assessment", moved the 15-minute ask to the positive reply, and made the tone more conversational.
3. Elite has to confirm the claims: 4,500 vs 3,000 placements, the "400 clients" figure, and IMC wording that doesn't imply guaranteed fraud prevention.
4. Each campaign needs sourcing for its trigger, with leads keyed by `linkedin_url` and the custom vars filled.

### Campaign 1 in HeyReach

- **Campaign `693168`**, "US | C1 Cleared Talent Fed Contracts | Moe v1", status **IN_PROGRESS since 2026-10-30 09:52 UTC**, started on Moe's instruction. It was created 2026-10-29.
  - At start: 72 leads (54 in progress, 18 pending, 0 failed, 0 excluded).
  - The final list is `sourcing/cleared-talent-federal-contracts/2026-10-30-heyreach-launch.csv`: 72 leads at 33 companies, 2–3 per company.
- **List:** `1082101` (USER_LIST), used only by this campaign.
- **Senders (11, all workspace accounts, since 2026-10-30 per Moe):** 232663, 263924, 264166, 264348, 265355, 265543, 266010, 266511, 267035, 267167, and 267224 (Mike Gerardo, Elite staff). Until then the campaign ran on the first 6 only.
- **Schedule:** **7 days a week**, 08:00–17:00 America/New_York, since 2026-10-30 per Moe. Before that it was Mon–Fri.
- **Leads:** 106 as of 2026-10-30, after a +34 push. The record of that push is `2026-10-30-2-heyreach-push.csv`.
- **Campaign `695698`** "US | C1b Fed Contracts 12mo | Moe v1" is for the 12-month award window, with list `1086068`.
  - Status: **IN_PROGRESS since 2026-10-30 17:18 UTC**, with 140 leads. Same 11 senders, schedule and exclusions.
  - Copy is identical to the live campaign except the connection note drops "recent": "congratulations on the {contract_or_agency} award!"
- **Exclusions:** company and lead blacklist on, exclude-in-other-campaigns on, exclude-has-other-conversations on.
- **Sequence**, read back with `get_campaign_sequence` and identical to the client's approved copy:
  1. Connection request with note, `{FIRST_NAME}` + `{contract_or_agency}`, withdrawn after 25 days
  2. On accept, +3h: message 1
  3. +7 days if no reply: message 2
  4. +7 days if no reply: message 3

  Every message exits on reply. The fallbacks drop the agency name ("the recent contract award").
- The positive-reply message (step 5 in the doc) is **manual**. It is not automated.
- **Wave 1 is in list `1082101`: 16 leads, with `contract_or_agency` and `award_id` custom fields set on every one.**
  - Parity was checked with `get_leads_from_list`: 16/16 present, with custom fields.
  - HeyReach's own profile data showed 3 Blitz contacts had **changed jobs** and they were removed: Nathan McFarland (Cadmus), Devin Brown (Tria) and Kameron Turner (Tria).
  - Tria was replaced with Steven Hardesty (VP IT & Quality), confirmed current. Cadmus has no other P1/P2 contact, so it sits out wave 1.
  - The campaign is **still DRAFT**: not started.

### HeyReach (workspace 170370), checked 2026-10-29

- **Campaigns:** 0. **Lists:** 0.
- **Company blacklist:** all 160 DNC company names loaded 2026-10-29 (IDs 83568–83727), matched by name only because the DNC has no URLs or domains. **Lead blacklist:** 0 entries.
- **Webhooks:** three workspace-wide `hr-inbox` webhooks go to `dashboard.algoacquisition.ai/api/hr-inbox/webhook/254dc33b-…`. All are active and cover all campaigns:
  - EVERY_MESSAGE_REPLY_RECEIVED (95980)
  - MESSAGE_SENT (95981)
  - INMAIL_SENT (95982)

  There are no Clay (Acc/Open) webhooks yet.
- **Senders (11).** Every account has `authIsValid: true`. None has a valid Sales Navigator or Recruiter seat, none is active or in a campaign, and none is on a search, connection, note or InMail cooldown.

  | id | Name | Conn-req limit / max | InMail limit / max | Note |
  |---|---|---|---|---|
  | 232663 | Rodalen Villarias | 25 / 40 | 40 / 40 | |
  | 263924 | aileen tiozon | 25 / 40 | 40 / 40 | |
  | 264166 | Paulo Peñera | **3** / 40 | **8** / 40 | low limits, likely still warming |
  | 264348 | Annaly Valdez | **3** / 40 | **8** / 40 | low limits, likely still warming |
  | 265355 | Juvy Putis | **3** / 40 | **8** / 40 | low limits, likely still warming |
  | 265543 | Dezirie Retuerto | **3** / 40 | 40 / 40 | low conn-req limit |
  | 266010 | Charity Calmerin | 25 / 40 | 40 / 40 | |
  | 266511 | Neil Aron Pascual | 25 / 40 | 40 / 40 | |
  | 267035 | James Keven Gallardo | 25 / 40 | 40 / 40 | |
  | 267167 | Cyrylle Booc | 25 / 40 | 40 / 40 | |
  | 267224 | Mike Gerardo | 25 / 40 | 40 / 40 | probably client staff: mgerardo@elitetechnical.com is on the Slack invite list. Confirm before using as a sender |

  That gives about 7×25 + 4×3 = **187 connection requests a day** across the pool at current limits. With no Sales Nav seat on any account, Sales Nav search URLs can't be run from this workspace.

## Sourced data in this repo

All rows below are for ICP config **Cleared Talent for New Federal Contracts** `d286c219-eb64-4aa8-bccf-3a800c3e4d08`. No lead-list UUID exists yet.

- `sourcing/cleared-talent-federal-contracts/2026-10-29-companies.csv`: 33 award-recipient companies, 2026-10-29.
  - Pulled via USAspending `POST /api/v2/search/spending_by_award/` (awards), Blitz `POST /v2/search/companies` (match and revenue) and Clay `search-contacts` (revenue cross-check).
  - The `decision` column records 26 included and 7 excluded, with reasons.
- `sourcing/cleared-talent-federal-contracts/2026-10-29-leads.csv`: 98 prospects at 24 companies, keyed by `linkedin_url`, 2026-10-29.
  - Pulled via Blitz `POST /v2/search/waterfall-icp-keyword` and Clay `search-contacts`.
  - Each row carries its verified award (ID, signed date, USAspending URL), `title_priority`, `revenue_status` and `company_wave_rank`.
- `sourcing/cleared-talent-federal-contracts/2026-10-29-heyreach-wave1.csv`: the 17-lead wave 1 as first planned, one contact per revenue-confirmed company, P1/P2 titles only. **Superseded by `-2`.**
- `sourcing/cleared-talent-federal-contracts/2026-10-29-2-heyreach-wave1.csv`: **the 16 leads actually in HeyReach list `1082101`**, after the job-change parity check below.
- Query, filters, TAM read and cost: `sourcing/cleared-talent-federal-contracts/2026-10-29-leads.query.md`.
- `sourcing/cleared-talent-federal-contracts/2026-10-30-companies.csv`: 43 companies from the **widened** pull, 2026-10-30.
  - Sources: USAspending (all NAICS, ≥$250k, contracts + IDVs) plus DoD awards from war.gov daily announcements (via Exa), then Blitz company match, then Clay revenue check. Same ICP config `d286c219-…` and lead list `f52caf59-…`.
- `sourcing/cleared-talent-federal-contracts/2026-10-30-leads.csv`: 145 prospects at 38 companies, keyed by `linkedin_url`, 2026-10-30.
  - Pulled via Blitz `waterfall-icp-keyword` and Clay `search-contacts`.
  - 76 are flagged `selected_for_launch` (2–3 per company, 34 companies).
  - Method and changes: `2026-10-30-leads.query.md`. Scripts are in `.../scripts/`.
- `sourcing/cleared-talent-federal-contracts/2026-10-30-3-leads.csv`: 301 prospects at 74 companies, keyed by `linkedin_url`, 2026-10-30. **12-month award window**, for C1b.
  - Method: a Blitz `POST /v2/search/companies` sweep ($100M–$1B, 29 states, 19 industries) matched against USAspending `spending_by_award` (12 months, ≥$500k, IT/eng NAICS) and war.gov DoD awards. Contacts came from Blitz `waterfall-icp-keyword`.
  - Same ICP config `d286c219-…` and lead list `f52caf59-…`. 159 are flagged `selected_for_launch`.
  - Details: `2026-10-30-3-leads.query.md`.
- `sourcing/cleared-talent-federal-contracts/2026-10-30-3-heyreach-c1b.csv`: the 141 leads at 62 companies pushed to HeyReach list `1086068`, 2026-10-30. One was then deleted as a job change, which leaves 140 live.

## History

- **2026-10-30**: **Campaigns 8, 9, 10, 2 and 3 were set up as drafts** on Moe's instruction ("set up the top 5 campaigns … from the document that we sent to them"). Moe chose these five, the next ones after C1 in the Oct 26 doc's launch order.
  - These are **5 new segments**, each with its own ICP config, lead list and campaign in tracking_clients. Sequences were saved and validated through `set_campaign_sequence`.
  - In HeyReach, each has a DRAFT campaign and an empty list: `695764`–`695768` and `1086161`–`1086166`.
  - Nothing was sourced or started, because Joseph's approval covers Campaign 1 only. There is no TAM read or per-company contact count yet; that comes with sourcing.
  - IDs are in the table under "Campaigns 8, 9, 10, 2, 3".

- **2026-10-30**: **C1b went live.** This is an **expanding existing segment** for Campaign 1, using a 12-month award window.
  - 141 leads at 62 companies were pushed to list `1086068`. The Blitz-sweep × award-match method is Moe's option 1.
  - The freshness check removed 1 job change (Andrew Heckel).
  - HeyReach `695698` started at 17:18 UTC with 140 leads.
  - The TAM is small (about 150 qualifying companies), so we pull 2–3 contacts per company.
  - The background `blitz_match_12mo.py` matched 2,562 of 3,825 recipients. Those are not yet filtered or pushed.

- **2026-10-30**: Moe widened Campaign 1's award window to 12 months and asked for leads to be pushed as they arrive.
  - Live campaign `693168`:
    - The 34 remaining Director/VP leads were pushed after a freshness check (72 → 106).
    - Paused briefly to switch to all 11 senders and a 7-day New York schedule, then resumed. It is IN_PROGRESS.
  - Created draft campaign `695698` (C1b), list `1086068`, for 12-month-window leads.
  - The 12-month USAspending pull (IT/eng NAICS, ≥$500k) is running.

- **2026-10-30**: **Campaign 1 went live.** HeyReach `693168` started at 09:52 UTC with 72 leads at 33 companies, on Moe's go-ahead.
  - Before starting, list `1082101` was synced to the 2026-10-30 selection:
    - removed DLH, whose award is now outside 60 days
    - removed 4 job-changers flagged by HeyReach, including Steven Hardesty, whose HeyReach record changed overnight
    - fixed a first/last-name swap (Brian Goins)
  - Parity: 72/72 leads, all with `contract_or_agency` set. All 6 senders are auth-valid with no cooldowns.
  - tracking_clients was synced to match (Moe's request):
    - campaign `46e24967-…` moved `creation` → `running`
    - lead list `f52caf59-…` set to `ready`
    - campaign notes updated, and the Claude chat link saved on the campaign
    - **Not done:**
      - Linking HeyReach `693168` to the campaign. The tool refuses HeyReach links for new-system campaigns (only Smartlead works), so `693168` shows as an unlinked platform campaign; link it in the dashboard if the UI allows.
      - Loading the companies into the lead list. The lead list's `company_count` stays 0, the same as the C&G worked example: ingest for the Custom module goes through a Clay table, which this list doesn't have.
  - **Open with Joseph:**
    - tell him 2–3 contacts per company are being messaged at once
    - send the pre-launch confirmations his doc asked for: sender profiles, award source, DNC suppression, reply handling, weekly reporting
- **2026-10-30**: **Expanding existing segment** (Campaign 1) after Moe asked for 1,000 leads.
  - Widened the trigger pull: all NAICS, ≥$250k, IDVs, and DoD awards from war.gov via Exa.
  - Result: 3,172 recipients; 211 in the $100M–$1B band; 43 relevant with an award in 60 days. The final list is 145 leads, of which 76 are selected at 2–3 per company (34 companies).
  - Moe approved 2–3 contacts per company at once, which **departs from Joseph's one-at-a-time rule**; Joseph still needs to be told.
  - **1,000 leads is not reachable inside Campaign 1's definition.** The trigger and revenue band cap it at about 40 companies.
  - Cost: Blitz ~6.6k records, Exa $0.34, Clay 2 searches.
- **2026-10-29**: Created tracking_clients lead list `f52caf59-…` (no split, per Moe) and campaign `46e24967-…`, and saved the sequence. Recorded Moe's reply-handling decision. Launch is still pending.
- **2026-10-29**: Pushed wave 1 to HeyReach list `1082101` and ran sanity checks. The campaign was **not started**; that waits on Moe's go-ahead.
  - The final list is 16 leads (`2026-10-29-2-heyreach-wave1.csv`). 3 stale contacts were swapped out after HeyReach showed job changes; that is about 18% staleness in Blitz contact data, so check current employment before every future push.
  - The sequence copy was checked word for word against the client doc and matches. The longest connection note is 144 characters.
  - The oldest trigger is DLH's award (2026-08-31): it is 59 days old today and leaves the 60-day window tomorrow.
- **2026-10-29**: **New segment: Campaign 1 "Cleared Talent for New Federal Contracts"**, approved by Joseph Monaco on 2026-10-28.
  - Saved the approval doc and email to `context/`.
  - Sourced from scratch: USAspending awards signed in the prior 60 days, then Blitz company match, then a Blitz + Clay revenue cross-check, then Blitz + Clay contacts. LinkedIn URLs only; no emails.
  - Results: 98 leads at 24 companies, and a 17-lead wave 1.
  - **TAM is small** (17 revenue-confirmed companies), so up to 4 contacts per company, but **staggered one per company per wave**. The client's doc forbids sending identical sequences to several contacts at one company at once.
  - DNC: none of the 33 companies matched the 160 DNC names on normalized name or token overlap. The near-misses checked by hand were:
    - IDA vs "United Defense"/"Department of Defense"
    - Manhattan Associates vs "Chase Manhattan"
    - MIL Corp vs "Booz Allen Hamilton", a substring false positive
  - ILC Dover was dropped anyway; its parent, Ingersoll Rand, is on the DNC.
  - Loaded all 160 DNC names into the HeyReach company blacklist.
  - Created ICP config `d286c219-…` in tracking_clients.
  - Created HeyReach list `1082101` and campaign `693168` (DRAFT).
  - Why: this is the client's first approved campaign; build it to their exact spec before launch. Blitz used ~1.7k of 6.2M records; Clay ran 4 searches with no enrichment credits.
- **2026-10-29**: Folder created and initialized for client `254dc33b-4f9f-4712-9b6b-eca49c5a5ffc`, following the CLAUDE.md init protocol.
  - Synced the profile from `get_client`. `list_sourcing_configs`, `list_icp_configs` and `list_campaigns` all came back empty.
  - Saved the ICP form, caller briefing/FAQs and the 160-row DNC list to `context/` verbatim. The Typeform response token and workflow IDs were left out of the ICP form.
  - Ran a read-only audit of HeyReach workspace 170370. It has 11 valid senders, none with Sales Nav and 4 on low limits; no campaigns or lists; an empty blacklist; and only the hr-inbox webhooks.
  - Why: this is a new client with no repo folder, so everything downstream needs this baseline. Nothing was created or changed in tracking_clients or HeyReach.
  - Next: segment proposal for Moe's sign-off before any ICP, sourcing config or campaign is created.
