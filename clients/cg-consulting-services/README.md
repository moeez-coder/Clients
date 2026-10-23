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
| Security and Data Bench - Clay (firmographic + title search) | Security and Data Bench | Technology, Financial Services and Education | draft | 1 | 0 (lead_count 0) | `-` |

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

- **Security and Data Bench**, campaign `c8855ae2-5c95-419b-8d8e-000c13cc757a`. LinkedIn, status `creation`, step 18, identity `-`, not approved, approval not sent, unclaimed. Linked to sourcing config `09be87f3-…`, persona `e399896d-…` and HeyReach campaign `677893`.
- Campaign notes: the copy comes from the C&G LinkedIn Campaign Plan (Ali, sent to Jon 2026-10-19, **not yet approved by Jon**). Angle: AI, data and security roles are the hardest technical seats to fill this year; privately held so pricing stays fair; onshore team. Copy is static except the first name. **The ManpowerGroup 2026 stat still needs verifying before launch.**
- **Sequence in tracking_clients:** only in the freeform `linkedInSequence` text. The structured `sequenceJsonb` is **empty** (`steps: []`), so nothing has gone through `set_campaign_sequence` or the rules gate yet. The freeform version has a connection-request **note** ("We help tech teams fill security, data and engineering roles with a 100% onshore recruiting team. Most of our clients have stayed with us for over 15 years. Would like to connect.") followed by messages 1 to 3.
- **Reply handling:**
  - `replyWorkflowN8nId` is blank, `replyWorkflowSetup: false` and `bookingLink` is blank.
  - The HeyReach workspace does have 3 workspace-wide `hr-inbox` webhooks to `dashboard.algoacquisition.ai/api/hr-inbox/webhook/4ca09bb2-…`: EVERY_MESSAGE_REPLY_RECEIVED (92790), MESSAGE_SENT (92791) and INMAIL_SENT (92792). All are active and apply to all campaigns.
  - So replies reach the dashboard inbox, but **nobody is named as owning replies yet**.

### HeyReach (workspace 169110)

- **Campaign `677893`** "Security and Data Bench", status **PAUSED**, 0 leads.
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

- `-` (no snapshots yet)

## History

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
