# Elite Technical (tracking_clients: "Elite Technical ")

> An IT and engineering staffing firm (contract and direct hire) based in Heathrow, Florida, with a large DC Metro footprint. It has 34 years in business, 400+ clients and 4,500+ placements, is woman-owned (WOSB/WBENC) and holds a DoD Top Secret facility clearance. The client's context from tracking_clients is saved verbatim in [`context/`](context/):
> - [ICP form](context/icp-form.md), submitted 2026-10-22
> - [caller briefing and FAQs](context/caller-briefing.md)
> - [DNC list](context/dnc-list.csv), 160 rows
>
> - [client brief](context/client-brief.md) and [client description](context/client-description.md), first present in tracking_clients at the 2026-11-05 resync
>
> tracking_clients still has no call transcript.

## Profile

- **Status:** active (isApproved: true, isAlgo: false), created 2026-10-22 by `sales`
- **Package tier:** Standard
- **Website:** https://elitetechnical.com (set in tracking_clients as of the 2026-11-05 resync; it was blank on 2026-10-29)
- **Billing:** $5,000 monthly (`billingAmount` / `billingFrequency`), client type `core`
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
  - `callTranscript` is empty. (`website`, `clientBrief` and `clientDescription` were filled in tracking_clients between 2026-10-29 and 2026-11-05.)
  - SDR defaults (headline, about, position, location, banner) are empty.
- **DNC:** `dncList` has 160 entries and `dncSkipped` is false. All 160 are historical clients scraped from `elitetechnical.com/for-business/clients-served/`. Every row has the status "Review before outreach; exclude pending account-owner confirmation". **No row has a domain** (`Company Domain (verify)` is blank on all 160), so exclusion has to match on company name.
  - By industry: Aerospace & Defense 53; Commercial Enterprise/Financial/Media 43; Health Care/Medical Device 21; Systems Integrators 16; Emerging Technology 14; Federal & State Governments 13.
  - None of the five "dream companies" in the ICP form (AeroVironment, TransMedics, Varonis, Tenable, Commvault) is on the DNC list.
- **Tracking client ID:** `254dc33b-4f9f-4712-9b6b-eca49c5a5ffc`
- **Last synced:** 2026-11-05 via `get_client` + `list_sourcing_configs`

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| USAspending awards (60d) + Blitz/Clay — Cleared Talent Fed Contracts | Cleared Talent for New Federal Contracts | Government Contractors, IT Services, Engineering, Defense, Research | ready | 1 | 0 (leads live in this repo; see note) | `-` |
| TheirStack/Coresignal live postings (30d) + Blitz contacts — C8 Role Behind the Posting | The Role Behind the Posting | Technology, Financial Services, Health Care, Defense and Space | draft | 1 | 0 | `-` |
| TheirStack remote/hybrid tech roles + Blitz TA contacts — C9 Candidate Fraud | Candidate Fraud in Technical Hiring | Technology, Financial Services, Health Care, Defense and Space | ready | 1 | 0 (2,633 leads live in this repo; source was Blitz, not TheirStack) | `-` |
| Job-change (90d) senior IT/Eng via Clay/Blitz — C10 New Seat Fresh Team | New Seat, Fresh Team | Technology, Financial Services, Health Care, Defense and Space | draft | 1 | 0 | `-` |
| Eng hiring surge/program news + Blitz contacts — C2 Program Ramp | Engineers for the Program Ramp | Defense and Space Mfg, Aerospace Components, Engineering Services, Defense Electronics | draft | 1 | 0 | `-` |
| Open security eng roles + Blitz contacts — C3 Security Talent | Hiring Security Talent Without the Fraud Risk | Computer and Network Security, Software Development, Data Infrastructure | draft | 1 | 0 | `-` |
| Blitz jobs (30d software eng postings) + hiring managers — Recruiter Software Eng | Recruiter Open Roles — Software Engineering | Technology, Financial Services, Health Care, Other (any industry posting software roles) | draft | 1 | 0 | `-` |
| Blitz jobs (30d IT/security postings) + hiring managers — Recruiter IT & Security | Recruiter Open Roles — IT Infrastructure & Support | Financial Services, Health Care, Technology, Other (any industry posting IT roles) | draft | 1 | 0 | `-` |
| Blitz jobs (30d hardware eng postings) + hiring managers — Recruiter Hardware Eng | Recruiter Open Roles — Electrical, Controls & Embedded Engineering | Defense and Space, Aerospace, Manufacturing, Medical Devices, Engineering Services, Other | draft | 1 | 0 | `-` |
| Blitz jobs (30d cybersecurity postings) + hiring managers — Recruiter Cybersecurity | Recruiter Open Roles — Cybersecurity | Any industry posting cybersecurity roles (Technology, Financial Services, Health Care, Defense, Other) | draft | 1 | 0 | `-` |
| Blitz jobs (30d data & AI postings) + hiring managers — Recruiter Data & AI | Recruiter Open Roles — Data & AI | Any industry posting data & AI roles (Technology, Financial Services, Health Care, Other) | draft | 1 | 0 | `-` |
| Blitz jobs (30d cloud/DevOps postings) + hiring managers — Recruiter Cloud & DevOps | Recruiter Open Roles — Cloud & DevOps | Any industry posting cloud/DevOps roles (Technology, Financial Services, Health Care, Other) | draft | 1 | 0 | `-` |
| Blitz jobs (30d enterprise apps postings) + hiring managers — Recruiter ERP & Apps | Recruiter Open Roles — Enterprise Applications (ERP/CRM) | Any industry posting enterprise application roles (Health Care, Financial Services, Manufacturing, Technology, Other) | draft | 1 | 0 | `-` |
| Blitz jobs (30d mech/mfg/quality postings) + hiring managers — Recruiter Mech & Mfg | Recruiter Open Roles — Mechanical, Manufacturing & Quality Engineering | Manufacturing, Aerospace & Defense, Medical Devices, Industrial, Energy, Engineering Services, Other | draft | 1 | 0 | `-` |

The 8 recruiter rows (created 2026-11-05) are mirrored verbatim from `list_sourcing_configs`. Two still carry names from the superseded 3-segment build: "Recruiter IT & Security" now feeds IT Infrastructure & Support, and "Recruiter Hardware Eng" now feeds Electrical, Controls & Embedded. Their ICPs were renamed but the configs were not. All 8 show `company_count`/`lead_count` 0, because the leads live in this repo (`sourcing/recruiter-open-roles-*`) and in HeyReach, not in tracking_clients.

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
| 9 | Candidate Fraud in Technical Hiring | `413dfae6-ff9e-4335-9e9f-73ff347f9b9c` (**running**) | `935c0326-200a-464d-88e0-b6a0952cf95e` / `dd9eca26-6774-4301-9aa2-fbbd89c69a2c` | `78d2a5a3-2dc4-49be-afa1-43d44235a0b5` | `695765` / `1086162` (**LIVE 2026-11-02, 2,513 leads, US-wide**) | A | - |
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
  - Status: **IN_PROGRESS since 2026-10-30 17:18 UTC**. It had 140 leads at start and **221 after the 2026-11-02 top-up**. Same 11 senders, schedule and exclusions.
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

## GTM Sheets

Folder **Clients / Elite Technical** (`b87ff0a8-59d1-4093-af63-b9e38440ed60`), at https://dashboard.algoacquisition.ai/gtm-sheet#/gtm-sheet?folder=b87ff0a8-59d1-4093-af63-b9e38440ed60.

There is **one workbook per recruiter campaign** (CLAUDE.md "GTM Sheets build standard per campaign"), each linked to its tracking_clients campaign. Each has three tables:
- **1. Companies:** `<date>-companies.csv`, every hiring company that passed the filters, with `Leads Selected`
- **2. Jobs:** `<date>-jobs.csv`, one posting per company, derived from `leads.csv`
- **3. Leads:** `selected_for_launch = yes`, with `Status` and a Push to HeyReach column

They are loaded by `gtm-sheets/build_gtm_payloads.py` and then `gtm-sheets/push_rows.py`. Every table's server row count matches its CSV.

| Campaign (workbook) | Workbook id | Companies / Jobs / Leads table ids | Rows (C / J / L) | HeyReach |
|---|---|---|---|---|
| Software Eng | `068a6922-d3a1-468b-b1d6-6873845ff1dd` | `6bae1b09-…` / `9e7c4384-…` / `caaeb0a7-6e5f-4c8f-b4fc-0de4422d7862` | 1,047 / 866 / 4,836 | `710042` |
| IT Support | `98e95f3e-86e3-45a9-bc21-fae9490184b8` | `60458d32-…` / `9809c3ab-…` / `96dcb4cb-5894-46d7-9c5d-f556277dacea` | 1,268 / 912 / 2,817 | `710044` |
| Cybersecurity | `62fe0343-bbee-4bab-ab5d-a66916b7f0e6` | `b94c9eea-…` / `e9943b46-…` / `7f2af1a9-5912-43d0-8e33-0f26b078c2df` | 617 / 450 / 1,500 (98 marked removed) | `710103` |
| Data & AI | `8f124457-0723-4382-b0a9-829e540d4418` | `aeea816e-…` / `0702058b-…` / `8d884a27-36ef-483e-97b2-3953ed4ac5cd` | 1,258 / 805 / 2,837 | `710104` |
| Cloud & DevOps | `930522ac-94b4-4de1-9fa6-93c4d6171e89` | `4fd1e259-…` / `d660f218-…` / `95ce8880-7d27-4d69-83d9-5b7a321cc922` | 567 / 239 / 406 | `710105` |
| ERP & Apps | `65b767bc-592f-41aa-a4dc-19460150d298` | `2af8d2a4-…` / `ff90ec1e-…` / `e960a576-282a-4b82-b7fe-bb8b55406a64` | 534 / 230 / 513 | `710107` |
| Elec & Controls | `d1331512-09bb-4c2e-92f3-39294d72af45` | `6e70c771-…` / `2b57837d-…` / `c0b0ba42-6bf5-483b-a1a9-e78161b556a6` | 973 / 607 / 2,859 | `710046` |
| Mech & Mfg | `9e0def87-9083-4100-a173-e56219a8297d` | `9bbcad93-…` / `05d12cb2-…` / `9a536d62-bda8-46d4-a812-7d59ce7a1912` | 1,090 / 759 / 3,675 | `710108` |

- **Push to HeyReach:**
  - Inputs: `linkedin_url` / `first_name` / `last_name` / `company_name` (cleaned) / `position` / `location`.
  - Custom fields: `open_role`, `open_role_with_article`, `company_name`, `jd`.
  - Auto-run is off, with `run_if` Status = "launch set". **It has not been run.** HeyReach refuses leads into a DRAFT campaign. Leads already in a HeyReach list are only updated, and HeyReach keeps LinkedIn's first name regardless.
- **Jobs caveat:** the raw Blitz `/v2/jobs/company` pulls (up to 5 jobs per company, `pull8_<seg>.json`) were never committed. So the Jobs table holds only the posting that drove each company's leads, one per company. Showing every matched posting would need a fresh Blitz pull.
- Each tracking_clients recruiter campaign's `clay_table_url` points to the folder URL above.
- The first build (one combined workbook `d3e065f2-…` with 8 tables) was deleted on 2026-11-05 when this structure replaced it.
- Webhook URLs are not stored in the repo. Get them from `gtm_sheet_get_table`.

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
- `sourcing/cleared-talent-federal-contracts/2026-11-02-companies.csv`: 77 companies from the 12-month award match, with an include/exclude `decision` per company. 38 have contacts and 30 are excluded. Pulled 2026-11-02.
  - Source: USAspending/war.gov award recipients matched to Blitz `POST /v2/search/companies`, then filtered to $100M–$1B revenue, target regions, the DNC list and the ICP.
  - Same ICP config `d286c219-…` and lead list `f52caf59-…`.
- `sourcing/cleared-talent-federal-contracts/2026-11-02-leads.csv`: 174 prospects at 47 companies, keyed by `linkedin_url`, from Blitz `waterfall-icp-keyword`, 2026-11-02. 83 are flagged `selected_for_launch`.
  - Details: `2026-11-02-leads.query.md`.
- `sourcing/cleared-talent-federal-contracts/2026-11-02-heyreach-c1b.csv`: the 83 leads pushed into running campaign `695698`, 2026-11-02. Two job changes were then removed, which leaves 81 live.
- `sourcing/candidate-fraud-technical-hiring/2026-11-02-companies.csv`: 1,733 companies with open remote or hybrid technical roles, 2026-11-02.
  - Belongs to ICP config **Candidate Fraud in Technical Hiring** `935c0326-200a-464d-88e0-b6a0952cf95e`, lead list `78d2a5a3-2dc4-49be-afa1-43d44235a0b5`.
  - Source: Blitz `POST /v2/company/tam-by-jobs`, filtered to $100M–$1B, 501–10,000 employees, target states and the DNC list.
- `sourcing/candidate-fraud-technical-hiring/2026-11-02-leads.csv`: 1,867 TA leaders and recruiting managers, keyed by `linkedin_url`, from Blitz `waterfall-icp-keyword`, 2026-11-02. **1,458 are selected, at 1,014 companies (2 per company).** Same config and UUIDs.
  - Details: `2026-11-02-leads.query.md`.
- `sourcing/candidate-fraud-technical-hiring/2026-11-02-2-companies.csv` and `2026-11-02-2-leads.csv`: the **US-wide expansion** (region filter removed per Moe), 2026-11-02.
  - 1,376 new companies and 1,531 prospects. **1,175 are selected, at 797 companies.**
  - Same config `935c0326-…`, lead list `78d2a5a3-…`, tool (Blitz `tam-by-jobs` + `waterfall-icp-keyword`) and cap.
  - Details and the filter-impact table: `2026-11-02-2-leads.query.md`.

- `sourcing/recruiter-open-roles-cybersecurity/2026-11-05-leads.csv` (+ `-companies.csv`): **1500 selected leads at 450 companies** (1481 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — Cybersecurity** `4c0c3fb1-cd38-41e4-9aa2-7ea5d3e37b75`, lead list `578098d3-e9c9-46d4-ad50-4eccde29e95c`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.
- `sourcing/recruiter-open-roles-data-ai/2026-11-05-leads.csv` (+ `-companies.csv`): **2837 selected leads at 805 companies** (2787 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — Data & AI** `78751c5e-06e7-4a67-9a77-816332575d17`, lead list `23583ae2-8ac2-4c35-9d3c-36b6905c338d`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.
- `sourcing/recruiter-open-roles-cloud-devops/2026-11-05-leads.csv` (+ `-companies.csv`): **406 selected leads at 239 companies** (365 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — Cloud & DevOps** `47337ded-24ef-49cf-9929-918508139019`, lead list `20fa81f6-6e8d-435c-bc2a-bd1b87655fa1`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.
- `sourcing/recruiter-open-roles-enterprise-apps/2026-11-05-leads.csv` (+ `-companies.csv`): **513 selected leads at 230 companies** (500 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — Enterprise Applications (ERP/CRM)** `b216733d-1138-4c1d-af43-93bb20b36a2c`, lead list `fac25c58-8e0c-4e81-aa3c-c1e6ad096017`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.
- `sourcing/recruiter-open-roles-it-support/2026-11-05-leads.csv` (+ `-companies.csv`): **2817 selected leads at 912 companies** (2799 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — IT Infrastructure & Support** `4a3c91bb-5d0a-48a5-9bf6-c43210f67742`, lead list `8ebe4aaa-4274-4ab5-bb4e-624207494122`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.
- `sourcing/recruiter-open-roles-electrical-controls/2026-11-05-leads.csv` (+ `-companies.csv`): **2859 selected leads at 607 companies** (2848 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — Electrical, Controls & Embedded Engineering** `11db2394-cd9e-4e55-8d49-782962272f97`, lead list `164e8069-adfa-4864-98f7-120d3c82c5fa`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.
- `sourcing/recruiter-open-roles-mechanical-mfg/2026-11-05-leads.csv` (+ `-companies.csv`): **3675 selected leads at 759 companies** (3672 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — Mechanical, Manufacturing & Quality Engineering** `ec056c9a-f579-4e4a-a56e-108e29256509`, lead list `e47ff0ce-c3a6-4620-b76f-502cc332ed84`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.
- `sourcing/recruiter-open-roles-software-eng/2026-11-05-leads.csv` (+ `-companies.csv`): **4836 selected leads at 866 companies** (4835 hiring managers), each tied to a live 30-day posting, 2026-11-05.
  - ICP config **Recruiter Open Roles — Software Engineering** `cde7d704-2497-45b6-a1f6-7da87fbfdc75`, lead list `779a36ad-e82b-41a9-b84f-56e3ea506b2d`.
  - Tools: Blitz `tam-by-jobs` + `jobs/company` + `waterfall-icp-keyword`. Details: `2026-11-05-leads.query.md`.

## History

- **2026-11-05**: Added `2026-11-05-client-overview.pdf`, a client overview for Moe covering the profile and ICP, live HeyReach results, campaign inventory, list-building method, capacity and open items. Stats were pulled live with `get_overall_stats` (workspace 170370):
  - all campaigns: 658 connection requests, 65 accepted (9.9%), 1 reply
  - C1: 73 requests, 6.8% accepted
  - C1b: 170 requests, 5.3% accepted
  - C9: 415 requests, 12.3% accepted

- **2026-11-05**: **GTM Sheets restructured to one workbook per campaign, each with Companies → Jobs → Leads tables** (Moe: "Have a different workbook for each campaign … one sheet with the jobs as well and then companies from which those jobs are. We will use GTM Sheets to display all of the working. Add this into the SOPs as well").
  - 8 new workbooks were created, each linked to its tracking_clients campaign, with 24 tables in total. Ids are in **GTM Sheets** above.
  - Rows loaded: 7,354 companies, 4,868 jobs and 19,443 leads. Every table's server count matches its CSV.
  - New derived files `sourcing/recruiter-open-roles-*/2026-11-05-jobs.csv` hold one posting per company, built from each `leads.csv`. They are not a new API pull.
  - The Cybersecurity Leads table marks the 98 freshness-check removals in `Status`, and its Push column skips them.
  - The old combined workbook `d3e065f2-…` was deleted.
  - The standard was added to the repo `CLAUDE.md` as "GTM Sheets build standard per campaign". Moe's message was the explicit approval for that system-file change.
  - It was **not** added to the brain repo SOPs (`AdmiralGeneralBaba/algoacquisition-brain`): the auto-mode classifier refused attaching that repo.

- **2026-11-05**: **Paused the last non-recruiter campaign and prepped Cybersecurity as the first recruiter launch** (Moe: "Pause all that are not recruiters"; "Use the most fitting recruitment section first").
  - Paused HeyReach `695700` "US | C1 Cleared Talent Fed Contracts | Moe v2". It was IN_PROGRESS with 106 leads: 85 finished, 11 in progress, 0 pending. It uses the same list `1082101` as C1 v1. After this, no Elite HeyReach campaign is IN_PROGRESS.
  - **Cybersecurity was chosen as the most fitting segment.** Three of Joseph's five dream companies are security vendors (Varonis, Tenable, Commvault). The ICP form names Director of Cybersecurity as a target title and "cybersecurity initiatives" as a buying signal. Elite's DoD Top Secret facility clearance also fits best here.
  - **Reconciling HeyReach list `1118017` against `leads.csv`:**
    - all 1,500 selected leads are present; the 4 apparent misses are the same profiles with percent-encoded URLs
    - all four custom fields match on every lead
  - **Freshness check.** HeyReach has already pulled live LinkedIn data. 350 `companyName` values differ from the expected company:
    - 32 have no company yet
    - 196 plus 31 (checked by hand) are aliases or renames, and are kept
    - **91 are at a different company**: a job change, or a side role (advisory board, investor, member, founder) listed as their current position. They are removed, following the C9 precedent.
  - **First names.** HeyReach overwrote our cleaned first names with LinkedIn's display names in 40 cases. Re-importing with a clean `firstName` was tested and does **not** override this. **7** would render broken in `{first_name}` (an emoji, "Dr.", "A", "Sandoval,", hidden Unicode characters, a name with a trailing comma, "Beverly J (SN)"), so they are removed too. The other 33 are names people chose themselves ("Tracy T.", "Dr. Curtis") and are kept.
  - The 98 removals are listed in `sourcing/recruiter-open-roles-cybersecurity/2026-11-05-heyreach-removed.csv`.
  - **Blocked:** the auto-mode classifier refused `delete_leads_from_list_by_profile_url`. The 98 are therefore **still in the list**, and the campaign was **not started**: the list can't be edited after start. Leads intended for launch: 1,402.
  - The GTM Sheets Cybersecurity table still holds all 1,500 rows. Its push column is not needed for this launch, because the leads are already in the list.
  - Repo data issue found along the way: 3 rows in this segment's `leads.csv` have `first_name = Dr`. They were not edited, because snapshots are append-only.

- **2026-11-05**: **All 8 recruiter open-role segments built in GTM Sheets** on Moe's ask ("Make all of these in gtm-sheets").
  - New workbook `d3e065f2-…` in the Elite Technical client folder, with one table per segment (ids in **GTM Sheets** above).
  - 19,443 rows were loaded from the repo CSVs by `gtm-sheets/push_leads_to_gtm_sheet.py` via each table's inbound webhook. Each server-side row count matches the repo's `selected_for_launch = yes` count exactly.
  - Each table is linked to its lead list.
  - Each table has a **Push to HeyReach** column wired to its DRAFT campaign with the four custom vars. It has not been run.
  - tracking_clients `clay_table_url` is set on all 8 recruiter campaigns.
  - Why webhook tables: they load directly from files in the shell. That avoids the per-100-lead token cost of the earlier `add_leads_to_list_v2` agent uploads, and avoids pasting CSVs through chat.
  - Seen while listing HeyReach campaigns: **`695700` "US | C1 Cleared Talent Fed Contracts | Moe v2" is IN_PROGRESS**. It is not recorded anywhere in this README and was not part of the 2026-11-05 pause. It was flagged to Moe and not touched.

- **2026-11-05**: **Resynced Profile and Sourcing configs from tracking_clients** (`get_client` + `list_sourcing_configs`) at the start of a new session (Initialization protocol).
  - Drift found: `website` is now set (https://elitetechnical.com), and `clientBrief` and `clientDescription` are now filled. They are saved verbatim as `context/client-brief.md` and `context/client-description.md`. `callTranscript` is still empty. The DNC list is unchanged at 160.
  - Added the 8 recruiter open-role sourcing configs to the table. tracking_clients now has 14 configs.

- **2026-11-05**: **Paused all live Elite campaigns** on Moe's instruction ("Pause those that are running currently"), to make room for the recruiter open-role campaigns.
  - Paused in HeyReach:
    - C1 `693168`: 106 leads, 73 finished
    - C1b `695698`: 221 leads, 170 finished
    - C9 `695765`: 2,513 leads, 1,808 still pending
  - tracking_clients campaigns `46e24967-…` (C1) and `413dfae6-…` (C9) were moved to **paused**.
  - Moe chose to launch the best-fit recruiter segments first: **Software Engineering, IT Infrastructure & Support, and Cybersecurity**, 9,153 leads in total. The other five recruiter campaigns stay in draft with their leads in the repo only.
  - Note: at the time of pausing, C9 showed `excludeInOtherCampaigns: false` and `excludeContactedFromSenderInOtherCampaign: true`, which differs from the settings it was created with. This was not changed here.

- **2026-11-05**: **8 new segments: recruiter-specific open-role campaigns**, on Moe's instructions:
  - the "open-role sequence" (Talent Edge/Alcor, 19.4% reply)
  - "recruiter specific in the name"
  - "don't limit it per the company"
  - "keep segments as many as needed"

  The sequence is a connection request, then message 1 two days after connecting and the next two messages two days apart. Each campaign is one role family. Each lead is a hiring manager tied to a live 30-day posting at a $100M–$1B, 501–10,000-employee US company, with no per-company cap. A talent fallback (Head of Talent / Talent Director / VP People) is used only when no hiring manager is found.
  - Custom vars: `open_role`, `open_role_with_article`, `company_name`, `jd`. The `jd` phrase is model-written from each posting's summary, and all were checked against their postings.
  - **19,443 leads** in all, across:
    - Cybersecurity: 1500 leads. tracking_clients `b8e4cb3d-6475-42a0-8df2-0e28d8b95965`; HeyReach DRAFT `710103` / list `1118017`
    - Data & AI: 2837 leads. tracking_clients `8bacac47-ccdb-4355-986b-ea741c0f2ae6`; HeyReach DRAFT `710104` / list `1118018`
    - Cloud & DevOps: 406 leads. tracking_clients `990afbc9-4d56-47bf-b6b2-c557bc6faee0`; HeyReach DRAFT `710105` / list `1118019`
    - Enterprise Applications (ERP/CRM): 513 leads. tracking_clients `65c82e90-5454-4b09-a566-8350c6570bf1`; HeyReach DRAFT `710107` / list `1118020`
    - IT Infrastructure & Support: 2817 leads. tracking_clients `5565a579-3839-4fa6-a667-62e43719b2ff`; HeyReach DRAFT `710044` / list `1118014`
    - Electrical, Controls & Embedded Engineering: 2859 leads. tracking_clients `36bf2aef-1098-499c-91c2-6eaf5eadad42`; HeyReach DRAFT `710046` / list `1118016`
    - Mechanical, Manufacturing & Quality Engineering: 3675 leads. tracking_clients `f99ad2d7-39c9-451b-a769-f517460b19f7`; HeyReach DRAFT `710108` / list `1118021`
    - Software Engineering: 4836 leads. tracking_clients `a42dd5f3-3ea3-421e-ac47-b09899fc2125`; HeyReach DRAFT `710042` / list `1117915`
  - All 8 HeyReach campaigns use all 11 senders and the 7-day NY schedule.
  - An earlier 3-segment, 1-per-company build from the same day was superseded before it was committed or loaded. Its tracking_clients and HeyReach records were repurposed: IT & Security became IT Infrastructure & Support, and Hardware became Electrical & Controls.
  - The 3-segment build's empty HeyReach lists `1117916` and `1117917` are unused.

- **2026-11-02**: **Campaign 9 expanded to the whole US.** This is an expanding existing segment.
  - Moe removed the DC/East/Midwest region filter for this campaign, so West Coast companies are now included.
  - It added 1,175 leads at 797 companies, for 2,633 leads at 1,811 companies in total.
  - Biggest filters: revenue outside $100M–$1B (36% of hiring companies), and no TA leader findable in Blitz (39% of the companies that remained).
- **2026-11-02**: **Campaign 9 went live.** HeyReach `695765` started at 12:12 UTC with **2,513 leads**, on Moe's go-ahead (relaying that Joseph told him to proceed as he sees fit).
  - All 2,629 unique leads were loaded through the HeyReach MCP. The freshness check removed 116 job changes and side-role profiles; they are listed in `sourcing/candidate-fraud-technical-hiring/2026-11-02-heyreach-removed.csv`.
  - tracking_clients campaign `413dfae6-ff9e-4335-9e9f-73ff347f9b9c` is now **running**, lead list `78d2a5a3-…` is **ready**, and the ICP geos are set to the US-wide scope.

- **2026-11-02**: **New segment: Campaign 9 "Candidate Fraud in Technical Hiring" sourced, with 1,458 leads at 1,014 companies.**
  - Moe asked for a campaign from the Oct 26 doc that can produce 1,000+ leads. C9 has the widest TAM, and its copy has no per-lead variables.
  - The trigger is open remote or hybrid technical roles, found with Blitz tam-by-jobs (30-day core titles, then 90-day wider titles). That gave 1,733 companies after the revenue, industry and DNC filters.
  - The large TAM means 2 contacts per company: a TA leader and a recruiting manager.
  - Leads go into the **draft** HeyReach list `1086162` (campaign `695765`). It is **not started**, because Joseph's approval covers Campaign 1 only.
  - Details: `sourcing/candidate-fraud-technical-hiring/2026-11-02-leads.query.md`.

- **2026-11-02**: **C1b topped up with 81 leads at 38 companies.** This is an **expanding existing segment**.
  - Both live campaigns had 0 pending leads, and Moe said "Push those to the campaigns".
  - The 12-month award match (2,562 recipients matched to Blitz) was filtered to 77 companies by revenue, region, novelty and the DNC list. A manual ICP review then excluded 30: universities, health systems, nonprofits, construction general contractors, and awards that are only maintenance or data purchases.
  - 83 contacts went into `695698`. The freshness check removed 2 job changes, which needed a brief pause and resume. The campaign is IN_PROGRESS with 221 leads.
  - The TAM is still small (about 47 qualifying companies in this batch), so we keep 2–3 contacts per company.
  - Details: `2026-11-02-leads.query.md`.

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
