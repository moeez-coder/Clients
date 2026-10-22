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

- **Senior SWE | Con Req | EE/SEA/ME | Oct26**, campaign `664d8455-7756-4dd2-aec0-2320032d60f3`. LinkedIn, status `creation`, step 18, identity Client, not approved. Linked to sourcing config `b3c476b6-…` / persona `3d8b2584-…`. **`heyreachCampaignId: 674915`** is already set, although the orchestrator handoff said no HeyReach campaign was linked. Verify it in HeyReach before building anything new.
- Stored sequence (`sequence_jsonb`), 4 steps:
  1. `connection_request`, day 0: short note (289 chars with the raw `{{module.standard.sender_first_name}}` token, about 260 once rendered). This fits a Premium/Sales Nav 300-char note but **not** a free account's ~200-char cap.
  2. `dm`, +1 day: Dave's full body, verbatim.
  3. `dm`, +3 days: generic bump with the apply link.
  4. `dm`, +4 days: last nudge with the apply link.
- The InMail variant (subject "Senior Software Engineer role") is noted as **not built yet**.

## Sourced data in this repo

- `-` (no snapshots yet)

## History

- **2026-10-22**: Folder created from `clients/_TEMPLATE/README.md`. Profile, sourcing config, ICP and Oct26 campaign synced from tracking_clients (client `dc3cb189-fee3-4b7f-8f31-f4e1989e46c7`, sourcing config `b3c476b6-b91a-4bc1-a59d-fce2e11d0acf`, ICP `641353d8-6568-44cf-b03b-6d26c78aec74`, campaign `664d8455-7756-4dd2-aec0-2320032d60f3`). Dave's Slack brief saved verbatim to `context/`. Why: Dave asked on 2026-10-22 for candidate outreach to Senior SWEs in EE/SEA/ME to be running by 2026-10-23. This opens a **new segment**: people-level candidate sourcing, which is the opposite direction from the employer-side brief stored on the client. Drift noted: the campaign already carries `heyreachCampaignId 674915`, and `heyreachWorkspaceId` is blank. Per-client ACQ Recruitment session.
