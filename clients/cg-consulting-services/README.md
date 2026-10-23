# C&G Consulting Services, Inc. (tracking_clients: "CG")

> A New Jersey staffing firm (Northvale, NJ) placing Life Sciences and Technology talent through contract staffing, direct hire, temp-to-perm and project teams. The client's own context from tracking_clients is saved verbatim in [`context/`](context/): [client brief](context/client-brief.md), [ICP form](context/icp-form.md) (submitted 2026-10-17), [client description](context/client-description.md), [caller briefing](context/caller-briefing.md) and [caller FAQs](context/caller-faqs.md). No call transcript exists in tracking_clients.

## Profile

- **Status:** active (isApproved: true, isAlgo: false)
- **Package tier:** Custom
- **Website:** https://cgcsinc.net/
- **Contact:** Jon McKeever <jon@cgcsinc.net>
- **Staff:** GTM engineer and campaign strategist moeez@algoacquisition.ai; infrastructure john.paul@algoacquisition.com; closer vince@algoacquisition.ai; sourcing engineer `-` (unassigned)
- **Slack channel ID:** C0C9UTECUNA
- **HeyReach workspace:** `169110` (heyreachConnected: true). In sessions this is the HeyReach connector whose campaign IDs resolve in org unit 169110 (`mcp__e83235d5-…__*`). Instantly, Smartlead and PlusVibe are not connected. masterInboxWorkspaceId `-`.
- **Infrastructure:** 5 LinkedIn seats, 5 VA seats, submitted to infra 2026-10-18. The HeyReach workspace actually has **10** sender accounts (see below).
- **LinkedIn health flag:** `linkedinIsBelowRed: true`, but `linkedinRedThreshold` is **null**. The flag is set even though no threshold is configured and no outreach has run. Treat it as unexplained until someone confirms how it is computed. Sender check results are below.
- **DNC:** `dncList` is empty and `dncSkipped: false`. **However, the ICP form has an uploaded do-not-contact file (`bf13fb07587e-Non_Connect`)** that was never loaded into tracking_clients. This must be resolved before any leads go live.
- **Tracking client ID:** `4ca09bb2-25f9-4410-b269-9c8bcb816881`
- **Last synced:** 2026-10-23 via `get_client` + `list_sourcing_configs` (+ `list_icp_configs`, `get_campaign`, `get_campaign_sequence`, `get_campaign_live_status`)

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| Security and Data Bench - Clay (firmographic + title search) | Security and Data Bench | Technology, Financial Services and Education | draft | 1 | 0 (lead_count 0; tracking_clients not yet updated, repo snapshot below) | `-` |

Config detail (tracking_clients):
- Sourcing config `09be87f3-0db4-4e2d-842d-b70af7d29d7c`, module **Custom** (`dd10c77c-109c-42e0-bc9a-a34ee0844fad`, granularity `company`), refresh `static`, `platform_leads_enabled: true`, `distribution_enabled: false`, empty module_config, no Clay table, workbook or webhook.
- ICP config `885e8da7-6318-4ede-b434-68cf84512790` "Security and Data Bench". Segment `2bef2c27-bc86-4fba-8330-e4d3110bc13d`: United States, company sizes 201-500, 501-1000 and 1001-5000, no fixed or custom signals.
- Persona `e399896d-c0c9-47b9-834d-3ea91fe374c5` (VP / Head / C-level): CIO, CTO, CISO, VP Engineering, VP of Data, Head of Data, Head of IT.
- Qualifier: "US software, fintech, banking and insurance, education and education publishing, and retail companies with in-house technology teams, $20M+ revenue. Staffing and recruiting firms excluded."
- **The ICP config is narrower than the ICP form.** The form asks for:
  - company sizes from 51-200
  - minimum revenue of $5M-$20M
  - Healthcare and Consulting verticals as well
  - a Northeast preference, DC to Boston

  The config drops 51-200, sets $20M+, has no Healthcare, Consulting or Life Sciences, and covers the whole US. That fits a technology-only first segment, but it is recorded here so nobody mistakes the config for the full ICP.
- Repo folder when sourcing starts: `sourcing/security-and-data-bench/`.

## Campaigns (tracking_clients)

- **Security and Data Bench**, campaign `c8855ae2-5c95-419b-8d8e-000c13cc757a`. LinkedIn, status **`running`** (since 2026-10-23, set by Moe's instruction), identity `-`, client approval not sent, unclaimed. Linked to sourcing config `09be87f3-…`, persona `e399896d-…` and HeyReach campaign `677893`.
- Campaign notes: the copy comes from the C&G LinkedIn Campaign Plan (Ali, sent to Jon 2026-10-19, **not yet approved by Jon**). Angle: AI, data and security roles are the hardest technical seats to fill this year; privately held so pricing stays fair; onshore team. Copy is static except the first name. **The ManpowerGroup 2026 stat still needs verifying before launch.**
- **Sequence in tracking_clients:** only in the freeform `linkedInSequence` text. The structured `sequenceJsonb` is **empty** (`steps: []`), so nothing has gone through `set_campaign_sequence` or the rules gate yet. The freeform version has a connection-request **note** ("We help tech teams fill security, data and engineering roles with a 100% onshore recruiting team. Most of our clients have stayed with us for over 15 years. Would like to connect.") followed by messages 1 to 3.
- **Reply handling:**
  - `replyWorkflowN8nId` is blank, `replyWorkflowSetup: false` and `bookingLink` is blank.
  - The HeyReach workspace does have 3 workspace-wide `hr-inbox` webhooks to `dashboard.algoacquisition.ai/api/hr-inbox/webhook/4ca09bb2-…`: EVERY_MESSAGE_REPLY_RECEIVED (92790), MESSAGE_SENT (92791) and INMAIL_SENT (92792). All are active and apply to all campaigns.
  - So replies reach the dashboard inbox, but **nobody is named as owning replies yet**.

### HeyReach (workspace 169110)

- **Campaign `677893`** "Security and Data Bench": **LIVE since 2026-10-23 ~16:56 UTC**. 500 loaded, 493 effective after 7 blacklisted. Schedule weekdays 07:00–19:00 ET. The details below are the pre-launch state.
  - It was **already started once**: `startedAt` 2026-10-23T13:13:58Z, then paused, by someone outside this session. A started campaign's list can't be changed, so list `1056840` is now locked to it. The list is `USER_LIST`, has 0 items and is used only by this campaign, so that is fine.
  - Settings: exclude-from-lead/company-blacklist is on; exclude-in-other-campaigns, exclude-has-other-conversations and exclude-contacted-from-sender are off.
  - It is the only campaign in the workspace.
- **Sequence as it stands in HeyReach** (`get_campaign_sequence`, 2026-10-23):
  1. Connection request, day 0, **blank note** (`messages: [""]`), withdrawn after 21 days.
  2. On accept, +1 day: message 1, matching the tracking_clients copy, with `{FIRST_NAME}` (HeyReach syntax) and fallback "Great to connect!".
  3. +3 days if no reply: message 2.
  4. +4 days if no reply: message 3.
  - A reply at any step ends the sequence.
  - **Drift:** HeyReach has a blank connection request, but tracking_clients' freeform copy has a note. Which one is intended still needs to be decided. Only 2 of the 10 senders have Sales Nav, which favours blank, as on ACQ.
- **Senders** (`get_all_linked_in_accounts`, 2026-10-23). All **10** workspace accounts are attached to `677893`:
  - Accounts: 203834, 243652, 249292, 249296, 252010, 261910, 263687, 263737, 264146, 264519.
  - **Auth is valid on all 10**, and none has a search, connection-request, connection-note or InMail cooldown.
  - **Sales Nav** is on only 203834 (Ma. Calianga) and 249292 (Criscele Paderna).
  - Every account shows `isActive: false` and `activeCampaigns: 0`. That fits a paused campaign but should be confirmed before launch.
  - The connection-request limit is 25/day on every account (max 40), about **250 requests a day** across the pool.
  - InMail limit is 8/day on 203834, 249292, 249296 and 261910, and 40 on the rest.

## Sourced data in this repo

- `sourcing/security-and-data-bench/2026-10-23-leads.csv`: **11,594 prospects at 4,618 companies** from **Security and Data Bench - Clay (firmographic + title search)** (config `09be87f3-0db4-4e2d-842d-b70af7d29d7c`), pulled 2026-10-23 via **Blitz API `POST /v2/search/people`** and keyed by `linkedin_url`. 8,393 are within the 3-per-company cap; 3,201 are flagged `within_company_cap=no` and kept. Not yet qualified by Haiku or checked against a DNC list. Query: `2026-10-23-leads.query.md`.
- `sourcing/security-and-data-bench/2026-10-23-companies.csv`: **28,579 companies** (the firmographic universe) from the same config `09be87f3-…`, pulled 2026-10-23 via **Blitz API `POST /v2/search/companies`**. `leads_in_snapshot` links each company to the leads file. Same `.query.md`.
- `sourcing/security-and-data-bench/2026-10-23-2-leads.csv`: the same **11,594 leads**, **Haiku-qualified** (8,332 QUALIFIED, 3,257 NOT_QUALIFIED, 5 PENDING; 6,591 qualified within the cap). Config `09be87f3-0db4-4e2d-842d-b70af7d29d7c`. Produced 2026-10-23 by Claude Haiku 5.5 workflow agents against `2026-10-23-qualification-spec.md`, keyed by `linkedin_url`. Query: `2026-10-23-2-leads.query.md`.
- `sourcing/security-and-data-bench/2026-10-23-2-companies.csv`: the **4,618** lead-bearing companies with Haiku verdicts (**3,668 QUALIFIED**). Config `09be87f3-…`, same run.
- `sourcing/security-and-data-bench/2026-10-23-2-heyreach-wave1.csv`: **500 leads** (500 companies, all Northeast) selected for HeyReach `677893` wave 1. Config `09be87f3-…`.
- `sourcing/security-and-data-bench/2026-10-23-3-leads.csv` / `-companies.csv`: the complete Haiku qualification after re-running 4 incomplete batches. **8,330 of 11,594 leads QUALIFIED, 0 PENDING; 3,668 of 4,618 companies QUALIFIED.** Config `09be87f3-0db4-4e2d-842d-b70af7d29d7c`. Claude Haiku 5.5 workflow agents, 2026-10-23. Notes in `2026-10-23-2-leads.query.md` § Follow-up. **This is the source for future waves.**

## History

- **2026-10-23 ~16:56 UTC**: **HeyReach `677893` resumed on Moe's instruction: LIVE.**
  - Status after the resume: `STARTING`, which tracking_clients `get_campaign_live_status` maps to `running`. 10 senders, weekdays 07:00–19:00 ET.
  - The campaign still reported `totalUsers 500` after the 7 list deletions, so deleting from the list does not remove leads already loaded into the campaign. `stop_lead_in_campaign` returned 404 for all 7.
  - The 7 were added to the **workspace lead blacklist** instead (ids 108273–108279; 5 Matched, 2 still resolving with member ids). Blacklist exclusion is on for this campaign, so they are excluded.
  - **Effective wave 1: 493 leads.**
  - **Lesson for the next wave:** check greeting names and final verdicts *before* the push. Removal after the push only works through the blacklist.
  - Still open: no reply-workflow type is set (1a/2b/2c), the client's `Non_Connect` DNC file is not loaded, Jon hasn't approved the copy, the ManpowerGroup stat is unverified.
  - Per-client CG session.
- **2026-10-23**: **Wave 1 pushed to HeyReach `677893` and checked for parity before resuming.**
  - **Push:** `add_leads_to_campaign_v2`, 5 batches of 100 from `2026-10-23-2-heyreach-wave1.csv`: **500 added, 0 updated, 0 failed**.
  - **Removed:**
    - 1 lead that flipped to NOT_QUALIFIED in `-3` (`siva-krishna-burra-1aa3562b`, ICONIQ). `stop_lead_in_campaign` returned 500 on the paused campaign, so it was deleted from list `1056840`.
    - 6 leads whose LinkedIn-resolved first name would render badly in `{FIRST_NAME}`. HeyReach used its own name over the cleaned one we sent: "Stoyan (Tony)", "Leszek (Les)", "John B.", "Shawn G.A.", "Naresh H.", "Jason T.". Slugs: stoyan-tony-stoyanov-07690a53, lkaldus, jbriii, shawnhouston, nareshsingh, jtordway.
  - **Parity:**
    - **Leads:** list `1056840` has **493** leads, exactly the wave file minus those 7. The two URL differences were only percent-encoding of the same profiles. Every remaining lead is QUALIFIED in `-3`.
    - **Sequence:** matches tracking_clients: blank connection request withdrawn at 21 days, then messages at +1, +3 and +4 days, `{FIRST_NAME}`, "Great to connect!" fallbacks.
    - **Senders:** 10/10 attached, all auth-valid, no cooldowns, 2 with Sales Nav.
    - **Schedule:** weekdays 07:00–19:00 ET. Blacklist exclusions are on, but both blacklists are empty.
    - **tracking_clients:** campaign `running`, `heyreachCampaignId 677893` linked.
  - **Known gaps at launch, Moe's call to go live anyway:** the client's `Non_Connect` file is not loaded; no reply-workflow type is set (replies reach the `hr-inbox` webhooks only); Jon has not approved the copy; the ManpowerGroup stat is not verified.
  - Per-client CG session.
- **2026-10-23**: **Moe: "make it live in tracking clients first."** Changes in tracking_clients:
  - Campaign `c8855ae2-5c95-419b-8d8e-000c13cc757a` moved `creation` → **`running`** via `move_campaign` (mark-running, confirm). This did not resume HeyReach `677893`, which is still PAUSED.
  - The structured sequence was saved with `set_campaign_sequence` and passed the rules gate. It mirrors HeyReach exactly: blank connection request on day 0, then messages 1, 2 and 3 at +1, +3 and +4 days, first name as `{{module.standard.first_name}}`.
  - The freeform `linkedInSequence` was rewritten to match. The old connection-request note was removed, per the org rule that connection requests are always blank (heyreach-campaign-launch-prep skill).
  - Sourcing config `09be87f3-0db4-4e2d-842d-b70af7d29d7c` → `ready`.
  - HeyReach schedule set: weekdays 07:00–19:00, timezone "Eastern Standard Time".
  - `create_reply_workflow` returned **400 "Campaign has no reply workflow type set (need 1a, 2b, 2c)"**. That is Moe's decision; until then replies reach only the workspace-wide `hr-inbox` webhooks.
  - Per-client CG session.
- **2026-10-23**: The 4 incomplete Haiku batches were re-run. All 99 pass, and the result is the new `2026-10-23-3-*` snapshot (8,330 qualified leads, 0 pending); `-2` is unchanged. One wave-1 lead flipped to NOT_QUALIFIED and is to be removed from HeyReach. Per-client CG session.
- **2026-10-23**: **Haiku qualification complete (expanding the existing segment's snapshot, not a new segment).**
  - 99 Claude Haiku 5.5 agents judged 4,618 companies and 11,594 leads individually: 3,668 companies and 8,332 leads qualified. 5 leads came back without a verdict and are marked PENDING.
  - Wave 1 is 500 Northeast leads, one per company, about two days of the 10 senders' ~250 requests a day.
  - **Committed before any lead went into HeyReach.**
  - Per-client CG session.
- **2026-10-23**: **First snapshot, new segment** (Security and Data Bench, config `09be87f3-0db4-4e2d-842d-b70af7d29d7c`).
  - Pulled from Blitz: 28,579 companies and 12,482 raw title matches. After the persona title check and company join, **11,594 leads at 4,618 companies**.
  - **TAM/SAM:** TAM is large (~28.6k companies), so the cap is **3 per company**. Leads over the cap are flagged, not deleted, so total volume isn't cut.
  - **Clay:** its public API is out of quota (402, resets 2027-01-01), so this snapshot is Blitz-only.
  - The first title check was too strict and dropped titles like "Chief Product & Technology Officer" and "VP Platform Engineering"; it was loosened before the build.
  - **Next:** Haiku qualification per company and per person (spec committed), pending Moe's approval of the cost estimate. Nothing is in HeyReach.
  - Per-client CG session.
- **2026-10-23**: Moe asked for **every company and every person to be qualified individually by Haiku agents**. I added `sourcing/security-and-data-bench/2026-10-23-qualification-spec.md`, the rules each agent applies. A company qualifies if it is a US operating company with an in-house tech team in software, fintech/banking, insurance carriers, education companies/publishers or retail, and is not staffing, IT services, government or a university. A person qualifies if they hold one of the persona's seven roles for real and are US-based. Agents run only after the Blitz snapshot is committed and Moe approves the cost estimate. Per-client CG session.
- **2026-10-23**: **Sourcing scope set by Moe: campaign-specific, for "Security and Data Bench"** (his words: "Do sourcing for security and data breach", read as the Bench campaign).
  - Added the pull code under `sourcing/security-and-data-bench/`:
    - `spec.py`: industry labels copied verbatim from the PR #7 Clay and Blitz enums, size 201-5000, revenue $20M+, the persona's seven titles plus their spelled-out variants.
    - `pull_blitz.py`: Blitz `/v2/search/companies` + `/v2/search/people`.
    - `build_csv.py`: URL dedupe, persona title check, company join, per-company cap.
  - Sizing (Blitz, indicative): **~28,850 US companies** and **12,482 title matches**.
  - **Clay public API is out of quota.** It returned 402: 999,988 of 1,000,000 annual results used, resets 2027-01-01. The Clay MCP connector still works but takes at most 10 companies per call, so it can only cross-check, not sweep.
  - The Blitz pull is running; its snapshot will be committed separately.
  - Per-client CG session.
- **2026-10-23**: Folder created from `clients/_TEMPLATE/README.md`. Profile, ICP config `885e8da7-6318-4ede-b434-68cf84512790`, sourcing config `09be87f3-0db4-4e2d-842d-b70af7d29d7c` and campaign `c8855ae2-5c95-419b-8d8e-000c13cc757a` synced from tracking_clients (client `4ca09bb2-25f9-4410-b269-9c8bcb816881`). HeyReach `677893` and its senders were read from workspace 169110.
  - The brief, ICP form, description, caller briefing and FAQs were saved to `context/`.
  - **Slug:** `cg-consulting-services`, not `cg`. "CG" is only the short tracking_clients name, and this matches how other folders are named after the company (e.g. `insurance-technology-services`).
  - **Segment:** this opens the client's first segment, Security and Data Bench: tech leadership at US tech, financial-services, education and retail companies.
  - **Drift recorded above:** the DNC file is in the ICP form but not in tracking_clients; the campaign was already started and paused at 13:13 UTC; the connection-request note is blank in HeyReach but set in tracking_clients; `sequenceJsonb` is empty; `linkedinIsBelowRed` is set with a null threshold; nobody owns replies.
  - Nothing was changed in tracking_clients or HeyReach.
  - Per-client CG session.
