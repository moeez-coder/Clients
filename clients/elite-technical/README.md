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
| USAspending awards (60d) + Blitz/Clay — Cleared Talent Fed Contracts | Cleared Talent for New Federal Contracts | Government Contractors, IT Services, Engineering, Defense, Research | draft | 1 | 0 | `-` |

Lead list (sourcing config) `f52caf59-e687-4ec4-94de-5d4d2862bc55` was created 2026-10-29: Custom module, static, `campaign_split: false` (Moe's choice: every linked campaign gets every lead), no Clay table or workbook.

ICP config **Cleared Talent for New Federal Contracts** `d286c219-eb64-4aa8-bccf-3a800c3e4d08` was created 2026-10-29:
- segment `16e8421d-b9e3-4c44-a4b9-cb80714bbdad`: 501–10,000 employees, DC Metro then East Coast then Midwest, signal "federal award in prior 60 days"
- persona `df04cee8-a69d-4b48-ac84-6d6e3657417f`: VP/Director, with the client's IT/Eng/TA titles
- the qualifier text holds the $100M–$1B hard filter

## Campaigns (tracking_clients)

**Campaign 1, "Cleared Talent for New Federal Contracts"**: campaign `46e24967-fdc8-4d7e-8c04-0e5e8af84afe`, status `creation`, linked to lead list `f52caf59-…` and persona `df04cee8-…`. The client approved it by email on 2026-10-28; see [context/2026-10-28-campaign-1-approval.md](context/2026-10-28-campaign-1-approval.md).
- The structured 4-step sequence (connection request plus 3 DMs, with `{{module.custom.contract_or_agency}}`) was saved through `set_campaign_sequence` and passed validation. The freeform `linkedin_sequence` also has the manual positive-reply step.
- The HeyReach link can't be set: `link_platform_campaign` supports only Smartlead for new-system campaigns. HeyReach `693168` is recorded in the campaign notes instead.
- **Reply handling** (Moe, 2026-10-29): Algo triages replies in the HeyReach/dashboard inbox and hands interested prospects to Elite (Joseph/Phil/Mike/Jeff) for the personal response, as Joseph's doc asks. No calendar link until a prospect shows interest.
- The other 9 proposed campaigns are **not approved**: Joseph will review them one by one.

### Campaign 1 in HeyReach

- **Campaign `693168`**, "US | C1 Cleared Talent Fed Contracts | Moe v1", status **DRAFT**, created 2026-10-29.
- **List:** `1082101` (USER_LIST), used only by this campaign.
- **Senders (6):** 232663, 263924, 266010, 266511, 267035, 267167. These are the VA accounts with 25/day connection limits. Left out:
  - Mike Gerardo (267224), Elite staff
  - the 4 low-limit accounts
- **Schedule:** Mon–Fri 08:00–17:00 America/New_York.
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

## History

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
