# We Are DNA

## Profile

- **Status:** active
- **Package tier:** Custom (`clientType: core`)
- **Billing:** 10160 monthly. tracking_clients stores no currency for `billingAmount`, so it can't be confirmed as £ or $ from the record.
- **Website:** https://wearedna.co.uk
- **Contact:** John Tarrant <john@wearedna.co.uk>. The ICP form also names mary@wearedna.co.uk for reports and invoices.
- **Slack channel ID:** C0CE71ZARLZ
- **HeyReach workspace:** `172307` (heyreachConnected: true). No HeyReach MCP connector in the 2026-11-12 session served this workspace. 16 connectors answered `list_workspaces`, each with another client's workspace, and 13 returned 401. Reach it through tracking_clients' `gtm_sheet_*` HeyReach tools, which use the client's own key, or add a connector for 172307. Never use another client's connector.
- **Staff:** campaign strategist Moeez; infrastructure John Paul; closer Rueban; GTM engineer `-` (unassigned); sourcing engineer `-` (unassigned).
- **Booking link:** `-` (empty in tracking_clients)
- **DNC:** `dncList` is empty (0) and `dncSkipped` is false. **The ICP form says a DNC file was uploaded (`b35224647da9-Do_Not_Contact_List.csv`), but it was never loaded into tracking_clients.** This has to be fixed before any list goes into HeyReach.
- **Infrastructure:** `{}` (empty). `callTranscript` and `notes` are empty.
- **Created in tracking_clients:** 2026-11-02 (`createdBy: sales`)
- **Tracking client ID:** `f5ff426b-c514-4a64-91b0-0e141a6a0669`
- **Last synced:** 2026-11-12 via `get_client` + `list_sourcing_configs` + `list_icp_configs` + `list_campaigns` + `list_campaign_docs`

**Who they are:** a Bristol creative agency, trading since 2010. They work across three pillars: Employer Branding, Employee Engagement, and Marketing Solutions, using their BrandShift™ method. **They are not a recruitment agency** and charge no placement fees. Deal value is about $45k and the sales cycle is about 12 weeks (ICP form).

## Context files

These are verbatim copies of tracking_clients fields, each with its source in a header comment.

- `context/client-brief.md`: `clientBrief`, generated before the ICP form existed, so most ICP fields are `[MISSING]`
- `context/icp-form.md`: `icpForm`, the client's own answers (submitted 2026-11-10), rendered as Q&A
- `context/client-description.md`: `clientDescription`
- `context/caller-notes.md`: `callerBriefing` + `callerFaqs`

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - |

None exist in tracking_clients as of 2026-11-12 (`list_sourcing_configs` count 0; `list_icp_configs` []).

## Campaign docs

| Date | Doc | tracking_clients id | Status |
|---|---|---|---|
| - | - | - | - |

## Sourced data in this repo

- `-`: no snapshots yet.

## History

- **2026-11-12**: Folder created from `clients/_TEMPLATE/README.md`. Profile synced from `tracking_clients`, and the brief, ICP form, description and caller notes were saved to `context/`. tracking_clients has no ICP configs, sourcing configs, campaigns or campaign docs yet. Started because Moe opened a per-client session to build We Are DNA's first campaign doc (10 campaigns: 5 open-role MPC segments plus 5 more). Gaps found: the uploaded DNC file was never loaded, no HeyReach connector serves 172307, the billing currency isn't recorded, and no GTM engineer is assigned. (session_013MzxQi4mQ4Mn8EAPSoHocN)
