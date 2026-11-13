# GRN Piedmont

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** https://grnpiedmont.com
- **Contact:** Harvey Eden <heden@grnpiedmont.com>. Chris Missler is also on Slack.
- **Slack channel ID:** C0CF3JM25EC
- **HeyReach workspace:** 172413 ("GRN Piedmont")
- **Booking link:** https://calendly.com/grnpiedmont/introductory-business-conversation
- **Tracking client ID:** `3abc2243-889c-4177-a75a-3ac680766d20`
- **Last synced:** 2026-11-13 via `get_client` + `list_sourcing_configs`. The two lead lists below were created this session.

## Campaign doc

The client reviews campaign copy in **"GRN Piedmont Campaign Ideas"** (tracking_clients campaign doc `cae47cc4-0801-44e6-ad15-9a2f0840f766`):
- It covers five LinkedIn campaigns.
- It was sent back to the client on 2026-11-13 and its status is `client_review`. It is **not approved yet.**
- Portal: https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=cae47cc4-0801-44e6-ad15-9a2f0840f766

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| Owner Succession - Blitz (US manufacturers 201-1000, owners/CEOs) | Owner Succession | Founder-led or family-owned US manufacturers | draft | 1 | 0 | `-` |
| Fire & Life Safety Leaders - Blitz (US F&LS 201-1000, C-level/VP) | Fire & Life Safety Leaders | US fire & life safety companies | draft | 1 | 0 | `-` |

## Campaigns (tracking_clients + HeyReach)

Both campaigns are **drafts**. No leads are loaded and nothing has started.

**Campaign 5: Owner Succession**
- tracking_clients campaign `250a7100-07e0-487d-97c0-8a204d97a276`
- ICP `6f0de60e-7db4-47ab-a578-c956a08f23b6`, segment `65577b4c-1785-4ad5-a74f-287fa6c899dd`, persona `7f34cf91-f4e0-4a1f-ba18-ee7cd2073cd3`
- Lead list `88fe680f-eae0-40c5-b147-1edf40579466`
- HeyReach campaign `730731`, list `1153575`, named "US | Owner Succession | GRN Piedmont v1"
- Preview: about 3,132 leads
- Custom vars: `years_in_role`, `ownership`

**Campaign 3: Fire & Life Safety Leaders**
- tracking_clients campaign `f1138ab0-daa4-42a1-8a7c-ca27965623ea`
- ICP `4961f767-e4e3-4783-a9fd-6a7be6fdd01d`, segment `b0604d63-bf74-459e-b33a-35bf69177a67`, persona `51597574-ce32-4aa3-806d-3556c3d5c5a4`
- Lead list `e8538474-8bd8-4479-8878-5899efe1ccf4`
- HeyReach campaign `730732`, list `1153576`, named "US | Fire & Life Safety Leaders | GRN Piedmont v1"
- Preview: about 3,066 leads, 334 companies on the tight keywords
- Custom vars: none in the base copy

**HeyReach setup (both campaigns)**
- Sequence: a connection request with no note, withdrawn after 25 days.
- Message 1 goes 3 hours after acceptance, Message 2 four days later, Message 3 five days after that (day 4 and day 9 in the doc).
- Fallbacks drop the custom variables.
- Each sequence was read back from the create response.
- `{FIRST_NAME}` / `{COMPANY}` are used in HeyReach. In tracking_clients they are `{{module.standard.first_name}}` / `{{module.standard.company_name}}`.
- Only the placeholder sender `182881` is attached, because HeyReach requires at least one. The schedule is HeyReach's default (weekend sending on).
- The HeyReach id is linked with `link_platform_campaign`, and `set_campaign_sequence` passed validation.

**Open before launch:**
- The client hasn't approved the doc.
- The DNC list (on the client record) isn't loaded into HeyReach.
- Senders aren't decided. The plan is Harvey's account only for Campaign 5 and all 10 accounts for Campaign 3, with a daily limit still to come from the client; we recommended 25 connection requests per day.
- The schedule needs setting to Eastern/Central business hours.
- Campaign 3's open-role Message 1 variant is not in HeyReach. It needs a second campaign or a per-lead message variable.
- Campaign 5's `years_in_role` and `ownership` values need a Claygent pass.
- Campaigns 1, 2 and 4 are not built yet.

## GTM Sheets

One workbook per campaign (CLAUDE.md "GTM Sheets build standard per campaign"). Folder: Clients / GRN Piedmont (`5b185300-2443-46b3-9a4d-b50cb54f4368`). Webhook URLs are not stored in the repo; get them from `gtm_sheet_get_table`.

**Campaign 5, Owner Succession:** workbook **US | Owner Succession | GRN Piedmont v1** `7ec67abc-807a-48e9-8958-9a10cf87156c`, linked to campaign `250a7100-…`. Rows: 0 so far (structure only).

| Table | id | Purpose |
|---|---|---|
| 1. Companies | `5e1a202a-af24-4c8e-894f-fe912aa9eb65` | US manufacturers 201-1,000, all states (Blitz count 8,729; the states filter was removed on the repo owner's instruction), with Ownership Check and Leads Produced columns so the drop-off is visible |
| 2. Ownership & Tenure Check | `64dc0c5e-9534-4ddb-b587-67cd692cec44` | Founder-led / family-owned check, top leader, years in role, Qualifies + Reason |
| 3. Leads | `1e0c689d-681d-435f-aaf5-6ac009b2290e` | Keyed by LinkedIn URL; `Status` ("launch set" / "removed: <reason>"); **Push to HeyReach** to `730731` with custom fields `ownership` and `years_in_role`, auto-run off, `run_if` Status = "launch set". Linked to lead list `88fe680f-…` |

## Sourced data in this repo

- `sourcing/2026-11-13-lead-preview.query.md`: lead-count preview for all five campaigns (Blitz counts via tracking_clients `gtm_sheet_find_people` / `gtm_sheet_find_companies`), 2026-11-13.
- `sourcing/fire-life-safety-leaders/2026-11-13-companies.csv`: 10 preview companies for **Fire & Life Safety Leaders - Blitz (US F&LS 201-1000, C-level/VP)** (config `e8538474-8bd8-4479-8878-5899efe1ccf4`).
  - Pulled 2026-11-13 via tracking_clients `gtm_sheet_find_companies` (Blitz preview, keywords fire sprinkler / fire alarm / fire suppression).
  - A sample only, not the full 334.
- `sourcing/seat-that-wont-close-preview/2026-11-13-companies.csv`: 3 preview companies for Campaign 1, The Seat That Won't Close (config `-`, none created yet).
  - Pulled 2026-11-13 via tracking_clients `gtm_sheet_find_companies` (Blitz preview with the `hiring` filter).

## History

- **2026-11-13**: **GTM Sheets workbook built for Campaign 5, Owner Succession** (repo owner: "Set this up in sheets", after confirming Campaign 5 is the only campaign with no client feedback).
  - Workbook `7ec67abc-…` with three webhook tables (Companies, Ownership & Tenure Check, Leads), ids above. The Leads table's Push to HeyReach column is wired to `730731` with auto-run off.
  - Pool for the Eastern/Central states: 3,700 companies (Blitz count, `gtm_sheet_find_companies`, same industries and sizes as the preview, `states` = the 38 Eastern/Central states + DC).
  - No rows loaded yet: pulling the companies and their owners costs about 7,400 Blitz credits, so the pull waits on the repo owner's go-ahead.
  - Later the same day the repo owner said "Remove the states filter". The pool is now all US states: 8,729 companies (the national count from `sourcing/2026-11-13-lead-preview.query.md`). The doc still says Eastern and Central time zones, so that limit now has to come from somewhere else (a Companies-table HQ State filter or the HeyReach schedule), or the doc needs updating with the client.
  - Session: `claude/grn-feedback-incorporation-lnmmb0`.
- **2026-11-13**: Folder created. The profile was synced from `tracking_clients` (`get_client`, `list_sourcing_configs`; there were no configs or campaigns before this session).
  - The client's 8 wording comments from 2026-11-12 on the campaign doc `cae47cc4-…` were applied as written and answered, and the doc was sent back (status `client_review`).
  - The repo owner asked to preview leads and set up the campaigns with the most leads in HeyReach and tracking_clients.
  - Preview (see `sourcing/2026-11-13-lead-preview.query.md`):
    - Campaign 5 Owner Succession: about 3,132
    - Campaign 3 Fire & Life Safety: about 3,066
    - Campaign 4 Rehire: about 933
    - Campaigns 1 and 2: can't be sized without a signal run
  - **New segments** Owner Succession and Fire & Life Safety Leaders were built as drafts: ICP config, lead list, campaign config, structured sequence and HeyReach campaign for each. IDs are above.
  - They were set up before client approval, at the repo owner's request. Nothing is started or loaded.
  - Per-company depth follows the doc: up to 3-4 contacts per company for fire & life safety (small TAM, 334 companies), 1-2 for manufacturing (large TAM, 8,729 companies).
  - Earlier rounds of client feedback on the doc (2026-11-10 and 2026-11-11) were handled in the same session without repo changes.
  - Session: `claude/grn-feedback-incorporation-lnmmb0`.
