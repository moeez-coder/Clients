# ACQ Recruitment

> **Internal client.** ACQ Recruitment is Algo Acquisition's own recruitment branch (`isAlgo: true`), not a paying client. It is a separate tracking_clients record from `clients/algoacquisition/` (`35bee65b-…`). Don't merge the two.
>
> **Direction of outreach matters here.** The stored `clientBrief`, `callerBriefing` and `callerFaqs` in tracking_clients describe ACQ selling *to employers* (Head of HR, Talent, founders). The Oct26 campaign below goes the **opposite way**: it is **candidate outreach to individual engineers** for one open role. Don't apply the employer-side brief, titles or TAM logic to this campaign. Its source of truth is [`context/2026-10-22-dave-slack-brief.md`](context/2026-10-22-dave-slack-brief.md).

## Profile

- **Status:** active (isApproved: true, internal / isAlgo: true)
- **Package tier:** `-` (blank in tracking_clients)
- **Website:** https://acqrecruitment.com
- **Contact:** Dave <dave@algoacquisition.ai>
- **Campaign strategist:** moeez@algoacquisition.ai
- **Slack channel ID:** C0CB2R4T2NS (`#internal-acq-recruitment`)
- **HQ / notes:** 128 City Road, London EC1V 2PU. Staffing and Recruiting, 11-50 employees. linkedin.com/company/acq-recruitment
- **Platform connections:** heyreachConnected: true, but `heyreachWorkspaceId` is **blank** in tracking_clients (flagged). Instantly, Smartlead and PlusVibe are not connected. DNC skipped (`dncSkipped: true`, empty list).
- **Infrastructure:** 5 LinkedIn seats, 20 VA seats (none connected), submitted to infra 2026-10-21
- **Tracking client ID:** `dc3cb189-fee3-4b7f-8f31-f4e1989e46c7`
- **Last synced:** 2026-10-22 via `get_client` + `list_sourcing_configs` (+ `list_icp_configs`, `get_campaign`, `get_campaign_sequence`)

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| Senior SWE \| LinkedIn profiles \| Oct26 test | Senior Software Engineer \| Payments & Webhooks \| EE/SEA/ME | Software Engineering (individual contributors, recruitment outreach) | draft | 1 | 0 (lead_count 0) | `-` |

Config detail (tracking_clients):
- Sourcing config `b3c476b6-b91a-4bc1-a59d-fce2e11d0acf`, module **Custom** (`dd10c77c-109c-42e0-bc9a-a34ee0844fad`, granularity `company`), refresh `static`, `platform_leads_enabled: true`, empty module_config, no Clay table or webhook.
- ICP config `641353d8-6568-44cf-b03b-6d26c78aec74`, segment `07da4d2a-7032-42e1-a15e-656075e8ec0b`, geos Eastern Europe / Southeast Asia / Middle East. Persona `3d8b2584-d867-4010-a812-ceae5667c0e6` (senior): Senior Software Engineer, Senior Backend Engineer, Senior Full Stack Engineer. The free-text qualifier mirrors the Dave brief.
- Repo folder: `sourcing/senior-swe-linkedin-profiles-oct26/` (people-level `-leads.csv`, `linkedin_url` first, no email enrichment).

## Campaigns (tracking_clients)

- **Senior SWE | Con Req | EE/SEA/ME | Oct26**, campaign `664d8455-7756-4dd2-aec0-2320032d60f3`. LinkedIn, status `creation`, step 18, identity Client, not approved. Linked to sourcing config `b3c476b6-…` / persona `3d8b2584-…` and to HeyReach campaign `674915`.
- **Build decision (Moe, 2026-10-22, this session):** a **single campaign** with a connection request, then **one message** (Dave's body), then **one short follow-up**. No Vertical Launch quadset, no InMail / Open Profile branch, no webhooks.
- **Sequence**, identical in tracking_clients (`set_campaign_sequence`, passed the rules gate) and HeyReach (`update_campaign_sequence`, re-read with `get_campaign_sequence`):
  1. Connection request, day 0, **blank (no note)**, withdrawn after 21 days. Blank keeps it inside "connection request only", and 9 of the 14 senders have no Sales Nav, so they would hit free-account note limits.
  2. Message on accept, +1 day: Dave's body verbatim, sender name via `{MY_FIRST_NAME}` (tracking_clients: `{{module.standard.sender_first_name}}`). The fallback is the same text.
  3. Message, +3 days, if no reply: "Hey, just bumping this up in case it got buried. The Senior Software Engineer role is still open, happy to answer any questions. You can apply here: https://dashboard.algoacquisition.ai/careers/tech-ops-specialist" (213 chars).
  - A reply at either message exits the sequence.
- The earlier 4-step draft (a 289-char note plus two bumps) was replaced by this.

### HeyReach (ACQ workspace, `mcp__ACQ_Hey_Reach__*`)

- Campaign `674915` "Senior SWE | Con Req | EE/SEA/ME | Oct26". **DRAFT**, never started (`startedAt: null`), 0 leads. List `1052180` (same name). `organizationUnitId 169955`. Exclude-from-lead/company-blacklist is on; exclude-in-other-campaigns is off.
- Senders: all **14** ACQ LinkedIn accounts are attached (`get_all_linked_in_accounts`, 2026-10-22). Auth is valid on all of them, and 5 have Sales Nav (254189, 257294, 259349, 261476, 262781). Daily connection-request limits: 6 accounts at 25 (254189, 257294, 260688, 261309, 261476, 262781) and 8 at 3, so about **174 requests a day** across the pool.

## Sourced data in this repo

- `-` (no snapshots yet)

## History

- **2026-10-22**: Campaign `664d8455-7756-4dd2-aec0-2320032d60f3` / HeyReach `674915` set to the build Moe chose: one campaign, blank connection request, then Dave's body on accept (+1d), then one short bump (+3d). Written to tracking_clients via `set_campaign_sequence` (valid) and to HeyReach via `update_campaign_sequence`, and verified with `get_campaign_sequence`. Why: Moe asked for "a single campaign starting with connection request only", with "just one message and then … a short message" as the follow-up. This replaces the 4-step draft and the Vertical Launch quadset. Campaign is still DRAFT with 0 leads; sourcing comes next. Per-client ACQ Recruitment session.
- **2026-10-22**: Folder created from `clients/_TEMPLATE/README.md`. Profile, sourcing config, ICP and Oct26 campaign synced from tracking_clients (client `dc3cb189-fee3-4b7f-8f31-f4e1989e46c7`, sourcing config `b3c476b6-b91a-4bc1-a59d-fce2e11d0acf`, ICP `641353d8-6568-44cf-b03b-6d26c78aec74`, campaign `664d8455-7756-4dd2-aec0-2320032d60f3`). Dave's Slack brief saved verbatim to `context/`. Why: Dave asked on 2026-10-22 for candidate outreach to Senior SWEs in EE/SEA/ME to be running by 2026-10-23. This opens a **new segment**: people-level candidate sourcing, which is the opposite direction from the employer-side brief stored on the client. Drift noted: the campaign already carries `heyreachCampaignId 674915`, and `heyreachWorkspaceId` is blank. Per-client ACQ Recruitment session.
