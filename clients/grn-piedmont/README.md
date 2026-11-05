# GRN Piedmont

Executive recruiting firm (Global Recruiters of Piedmont, part of the Global
Recruiters Network). Performance-based, direct-hire search for mid-sized
manufacturing, fire & life safety and government (GSA contract holder). Full
brief: [`client-brief.md`](client-brief.md); onboarding form answers:
[`onboarding-form.md`](onboarding-form.md) (both mirrored from `tracking_clients`).
Analysis, proposed segments and open questions: [`client-analysis.md`](client-analysis.md).
Campaign plan (5 campaigns, draft): [`campaign-plan-2026-11-05.md`](campaign-plan-2026-11-05.md),
uploaded to tracking_clients as campaign doc `cae47cc4-0801-44e6-ad15-9a2f0840f766`.

## Profile

- **Status:** active
- **Package tier:** Custom (client type: core)
- **Website:** https://grnpiedmont.com
- **Contact:** Harvey Eden <heden@grnpiedmont.com> (also on Slack: Chris Missler <cmissler@grnpiedmont.com>, per client brief)
- **Slack channel ID:** C0CF3JM25EC
- **HeyReach workspace ID:** 172413 (connected)
- **Smartlead client ID:** -
- **GTM engineer / campaign strategist:** moeez@algoacquisition.ai
- **Closer:** rueban@algoacquisition.ai
- **Sourcing engineer:** -
- **Infrastructure handler:** -
- **Billing:** $13,000 monthly
- **DNC count in tracking_clients:** 0 (the brief references a client-supplied DNC file, `Do_Not_Contact_List.xlsx`, not yet loaded)
- **Created in tracking_clients:** 2026-11-02
- **Tracking client ID:** `3abc2243-889c-4177-a75a-3ac680766d20`
- **Last synced:** 2026-11-05 via `get_client` + `list_sourcing_configs` (+ `list_icp_configs`, `list_campaigns`, `get_client_notes`)

## Sourcing configs

No sourcing configs exist in `tracking_clients` as of 2026-11-05 (`list_sourcing_configs` returned `count: 0`). `list_icp_configs` and the client's `list_campaigns` entries are also empty.

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - |

## Sourced data in this repo

- None yet. No `sourcing/` tree exists.

## History

- **2026-11-05** — Wrote the campaign plan `campaign-plan-2026-11-05.md` and uploaded it to tracking_clients via `create_campaign_doc` (doc `cae47cc4-0801-44e6-ad15-9a2f0840f766`, title "GRN Piedmont Campaign Ideas", status `draft`, hidden from the client). Why: the user asked for a GRN campaign doc modelled on the Nextwo RaaS Campaign Ideas doc. The plan has five signal-led LinkedIn campaigns: (1) The Seat That Won't Close, (2) New Site, New Leaders, (3) Fire & Life Safety Leaders, (4) The Rehire Question, (5) Owner Succession. Contacts per company follow TAM: fire & life safety is narrow, so 3–4; manufacturing is wide, so 1–2. The repo file mirrors the doc as uploaded; the tracking_clients doc becomes the live version once the client comments. Session: claude/adoring-allen-9w90ht.
- **2026-11-05** — Added `onboarding-form.md` (verbatim Typeform answers from `get_client.icpForm`, submitted 2026-11-03) and `client-analysis.md`. Why: the user asked for a thorough client analysis based on the onboarding form. Main findings: three segments proposed (fire & life safety first, as a narrow segment at 3–4 contacts per company; signal-led manufacturing, as a wide segment at 1–2 contacts per company; HR-leader persona track; government parked). Launch blockers: the DNC xlsx is not loaded (`dncCount` 0), there are no LinkedIn senders yet (`list_client_accounts` 0; 5+5 seats submitted to infra on 2026-11-05) and no onboarding call is on record. Sources were `get_client` and `get_client_meetings`; `get_client_experience` is blocked by the MCP firewall. Session: claude/adoring-allen-9w90ht.
- **2026-11-05** — Folder created from `clients/_TEMPLATE/README.md`; Profile synced from `tracking_clients` `get_client`, and the client brief mirrored to `client-brief.md`. Why: first session for this client (onboarded in tracking_clients 2026-11-02), set up before any segment is opened. `tracking_clients` holds no sourcing configs, ICP configs or campaigns yet. The brief names three target verticals (mid-sized manufacturing, fire & life safety, HR-leadership-need companies), all at 201–1,000 employees in EST/CST US time zones, with C-suite/VP/Owner titles and no Manager/Director. Those are candidate segments, none opened. Session: claude/adoring-allen-9w90ht. The sync was done over direct HTTP to the tracking-clients MCP endpoint because the connector wasn't attached to the session.
