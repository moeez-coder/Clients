# twoHundred (tracking_clients: "twoHundred")

> twoHundred is a Copenhagen-based business, founded 2017. It runs invitation-only executive communities and events: CxO Forums of 20–50 executives and Roundtables of 7–12. The attendees are C-level leaders from the top 200 enterprises in Denmark, Sweden, Norway, Finland and the Netherlands. There are communities for CIO, CISO, CFO, CHRO and CSCO/CPO. Revenue comes from **commercial partners**: B2B technology vendors who sponsor or take part. **Outreach targets those vendors, not the executive attendees.** The client's context from tracking_clients is saved verbatim in [`context/`](context/):
> - [ICP form](context/icp-form.md), submitted 2026-11-04 (the client's own answers)
> - [client brief](context/client-brief.md), generated before the ICP form existed, so most of its ICP section is `[MISSING]`/`[INFERRED]`
> - [client description](context/client-description.md)
> - [caller briefing and FAQs](context/caller-briefing.md)
>
> tracking_clients has no call transcript.

## Profile

- **Status:** active (isApproved: true, isAlgo: false), created 2026-11-04 by `sales`
- **Package tier:** Core (`clientType: core`)
- **Deal (from `notes`):** $13,000 for the quarter. $6,500 was paid 2026-11-04 and $6,500 is due 2026-12-02 (`billingAmount` 6500, `billingFrequency` quarterly).
- **Volume target: 40 qualified meetings promised, with a guarantee to work free until delivered.** Together with the "reach more people, not fewer" stance, this argues for a wide TAM. The ICP form gives the deal value as $25,000 and the sales cycle as 6 weeks.
- **Website:** tracking_clients has `https://twohundredgroup.com/`, and the ICP form gives the same. Moe gave the domain as `twohundred.dk` (2026-11-06), which matches the contact email.
  - Checked 2026-11-06: `https://twohundred.dk` and `https://www.twohundred.dk` both redirect to `https://twohundredgroup.com/` (HTTP 200).
  - These are the same company. twohundredgroup.com is the canonical site and twohundred.dk is the email/legacy domain. Moe to confirm which one tracking_clients should hold. No change has been made there.
- **Contact:** Christian Peter Sandvei <cps@twohundred.dk>. tracking_clients stores the name with a leading space (`" Christian Peter Sandvei"`); it is trimmed here. The ICP form also asks for a Slack invite for rd@twohundred.dk.
- **Address (ICP form):** Hilmar Baunsgaards Boulevard 15, 2300 Copenhagen, Denmark
- **Staff:**
  - GTM engineer and campaign strategist: moeez@algoacquisition.ai
  - Infrastructure: john.paul@algoacquisition.com (tracking_clients `infrastructureEmployeeId`)
  - **SDR / LinkedIn senders: John, john@algoacquisition.com (Slack `U0AJFP48EKS`).** Per Moe on 2026-11-12, he is the right person for anything SDR-related, not John Paul.
  - Closer: vince@algoacquisition.ai
  - Sourcing engineer: `-` (unassigned)
- **Slack channel ID:** C0CEBCSU53R
- **HeyReach workspace:** `172772`, named "twoHundred" (heyreachConnected: true).
  - **This session has no HeyReach MCP connector for 172772** (checked 2026-11-06). 24 HeyReach connectors respond and map to other clients' workspaces; none matched "two". 5 connectors return 401.
  - Reads go through tracking_clients' stored key (`gtm_sheet_list_heyreach_campaigns`, `get_client_stats`).
  - Instantly, Smartlead and PlusVibe are not connected. masterInboxWorkspaceId is `-`.
- **Infrastructure:** not submitted to infra (`infrastructure` is `{}`).
- **Booking link (2026-11-13):** https://meetings.hubspot.com/christian-peter-sandvei/account-meeting. It was blank on 2026-11-06. `replyWorkflowN8nId`: no campaigns exist yet.
- **Gaps in tracking_clients:** these are recorded, not filled by guessing.
  - `callTranscript` is empty.
  - SDR defaults (headline, about, position, location, banner) are empty.
  - `sampleReportUrl` is empty.
- **DNC (updated 2026-11-13):** `dncList` now holds **53 companies** (repo copy `context/dnc-2026-11-13.csv`), so the gap below is closed. Earlier state: `dncList` was empty (0 entries) and `dncSkipped` was false. **But the ICP form says the client uploaded a DNC file:** `31a7eb95d165-Do_Not_Contact_twoHundred_enriched.xlsx`.
  - That file never reached `dncList`. This is a gap to fix, not "no DNC".
  - It almost certainly holds existing/past partners. The form names Oracle, Palo Alto Networks, SAP, Workday, Wonderful, Wiz and Zscaler as past partners, and the brief adds Ivalua.
  - **No sourcing pull should go to HeyReach until that file is loaded.**
- **Tracking client ID:** `6de16a2e-b5af-4380-acad-685a519744b5`
- **Last synced:** 2026-11-06 via `get_client` + `list_sourcing_configs` (+ `list_icp_configs`, `list_campaigns`)

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| C1 CPO/CSCO Table: Clay + Blitz (supply chain & procurement vendors) | C1 The CPO and CSCO Table | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C2 Beyond the Expo Hall: Clay + Blitz (Nordic/NL event sponsors) | C2 Beyond the Expo Hall | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C3 New in the Seat: Clay + Blitz (job changes, last 6 months) | C3 New in the Seat | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C4 Entering the Nordics: Clay + Blitz (expansion news, last 9 months) | C4 Entering the Nordics | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C5 CISO Room: Clay + Blitz (cybersecurity vendors) | C5 The CISO Room | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C6 Nordic CIO Pulse: Clay + Blitz (enterprise IT vendors) | C6 Nordic CIO Pulse | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C7 Finance and People Leaders: Clay + Blitz (finance and HR software vendors) | C7 Finance and People Leaders | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C8 Open Roles Field/Event Marketing: Blitz jobs + Clay hiring managers | C8 Open Roles, Field and Event Marketing | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C9 Open Roles Country/Sales Leadership: Blitz jobs + Clay hiring managers | C9 Open Roles, Country and Sales Leadership | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |
| C10 Open Roles ABM/Demand/Partner Marketing: Blitz jobs + Clay hiring managers | C10 Open Roles, ABM, Demand and Partner Marketing | Nordics + NL; see ICP config | draft | 1 | 0 | `-` |

Mirrored from `list_sourcing_configs` on 2026-11-12. All 10 configs use the Custom module, are static, have `campaign_split: false` (one campaign per list, so a split has no meaning), and have no Clay table yet. `company_count` and `lead_count` are both 0.

## Campaigns (tracking_clients, new system)

All 10 were created 2026-11-12 from approved doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51` and are linked to it (`doc_signed: true`). Every campaign is LinkedIn, identity Client, and has a validated 4-step sequence (`set_campaign_sequence`: connection request, then 3 DMs at day 0, 4 and 9). All are in status `creation`.

| # | Campaign | session id | Lead list (sourcing config) | ICP config | HeyReach campaign / list |
|---|---|---|---|---|---|
| C1 | The CPO and CSCO Table | `094e9b70-89e2-414f-b48b-8eb7d9ae45e3` | `b81f2795-76e8-4f63-a8d0-3f0d53cabf6e` | `94a6a632-88eb-43cb-8401-9b286033fa17` | `729831` / `1152302` |
| C2 | Beyond the Expo Hall | `a767b822-f1d5-422b-acba-e536d54882b4` | `c659923d-b864-4572-a5f9-6034425882a9` | `b359767a-463a-4e85-abe5-7b625be7f013` | `729835` / `1152307` |
| C3 | New in the Seat | `919f494a-06d5-439f-9f3c-7181367c75a6` | `82f47ea4-d434-444c-830f-4fffa6d5c2fe` | `92d229b6-875a-43ab-9f50-2749bd6913f9` | `729836` / `1152308` |
| C4 | Entering the Nordics | `51e55b6c-f97f-4a5a-9109-4bd7f730598d` | `a42149fc-d3ac-44d4-86e6-aa5a856d1827` | `35d03c8c-ab82-4053-8e9c-55e9cb1ebb01` | `729837` / `1152309` |
| C5 | The CISO Room | `0637bac6-5e24-41be-b829-25350eb83b25` | `3b6c78bc-ec87-4bd4-b6b6-4a0d89936f4c` | `ee1bb78d-8fd4-4826-a689-3e0a07844836` | `729838` / `1152310` |
| C6 | Nordic CIO Pulse | `aad8be08-a118-420c-b11c-7c1581c9baf4` | `52e26a7a-c209-42d5-b3e4-a81548a2a5f8` | `4b955c4a-326c-495c-beab-da078d093bf9` | `729840` / `1152311` |
| C7 | Finance and People Leaders | `fe3ef189-38f6-42ab-ae9a-712517eace39` | `d3ebc835-ae65-4777-a770-650a0ef0f417` | `0694d62b-8932-4f8c-8dc9-c9467de0cec6` | `729841` / `1152312` |
| C8 | Open Roles, Field and Event Marketing | `c8b08608-897e-4ec0-8568-fc26c2525827` | `41d63fbf-1b66-44d1-ba91-2ad0b2def817` | `99443fa9-fbcf-450e-bcfe-89a57e40b5a1` | `729842` / `1152313` |
| C9 | Open Roles, Country and Sales Leadership | `f7d16968-870a-4477-90d9-1cc32d3fd0bc` | `25cf23a0-bd3d-4d32-a8aa-9f91fb131150` | `01f08a0f-2a51-426f-9aad-7c0f8b128671` | `729843` / `1152315` |
| C10 | Open Roles, ABM, Demand and Partner Marketing | `65ed1c2f-4a4e-4b3e-9fe5-9b7502d6c97f` | `55fb215f-cad1-4d8b-890a-72f366e81b38` | `f9c2c642-d732-420c-bf3f-7b90812be327` | `729844` / `1152317` |

## HeyReach state (2026-11-13)

- Workspace 172772 "twoHundred" now has **10 DRAFT campaigns**, one per tracking_clients campaign (ids in the Campaigns table). Each has its own empty list. All were created 2026-11-13 with `gtm_sheet_create_heyreach_campaign` and linked with `link_platform_campaign`. **None has been started.**
- **Senders:** all 9 VSDR accounts are on all 10 campaigns (`set_campaign_senders add_all_available`, 9 per campaign): Delosjene Encarnado, Joanna Marie Alipio, Brett Magat, Ralph John Taboada, Eianne Maurice Tantiado, Shiela Mae Inoc, Milca Lavarias, Marjorie Paulo, plus account `182761` (put on at creation). All are `heyreach_connected: true` and `sales_nav_connected: false`.
- **Sequence:** connection request (withdrawn after 25 days), then M1, M2 after 4 days, M3 after 5 days. Every DM has a fallback for empty variables, and weekend sending is on.
  - **M1 delay is saved as 3 hours.** We asked for 1 hour, but HeyReach stored 3.
  - **Variables:** `{FIRST_NAME}`, `{company_name}` and the custom fields (`event_name`, `event_city`, `expansion_short`, `country`, `category_short`, `community`, `open_role`, `open_role_with_article`, `jd`). Clay must push these exact field names.
- **C1 to C7:** the connection request is blank, as approved.
- **C8 to C10 (open roles):** the API rejects a connection note that uses `{company_name}` or `{open_role}`. HeyReach wants a note fallback, and the tool can't set one ("The fallback message is invalid in the Connection request action"). The saved notes use only `{FIRST_NAME}`, with the role family written in plain text (e.g. "saw the field marketing opening on your team"). **To get the approved `{open_role}` / `{company_name}` note back, edit it in the HeyReach UI and add a fallback there.**
- **Not checked yet:** the workspace blacklist. There is still no HeyReach connector for 172772 in this session.

## ICP form vs. brief

The ICP form (2026-11-04) is the client's own answer. The brief was written without it.

| Topic | Brief said | ICP form says | Verdict |
|---|---|---|---|
| Who we target | Vendors/commercial partners, not attendees (inferred) | Implicitly vendors: titles are vendor GTM roles; pains are "B2B technology companies struggle to reach C-level…" | **Confirms** |
| Industries | Enterprise software across HR/finance/security/supply chain/martech, IT services, consulting (inferred) | `Technology`, `Consulting` | **Confirms**, but narrower. There is no martech or sustainability segment. |
| Company size | `[MISSING]` | 501–1,000, 1,001–5,000, 5,001–10,000, 10,000+ employees; revenue over $20M | **Fills the gap**: 501+ employees and >$20M revenue |
| Geography | Vendors with Nordic/NL GTM relevance, HQ unclear | EMEA; focus on Sweden, Denmark, Norway, Finland, Netherlands | **Mostly confirms.** The dream companies are mostly US-HQ, so this means global vendors that sell into the Nordics/NL, with contacts located in (or covering) those countries. |
| Titles | VP Marketing, VP Sales, Head of Partnerships, CMO, CRO, Head of Events/Field Mktg, ABM, Country Manager, MD Nordics, VP BD, Demand Gen | 25 titles, all field/regional/partner/ABM/demand marketing or sales leadership, plus Country Manager, MD, GM, CRO, CMO | **Confirms, with differences.** The form adds Regional/Nordic/EMEA *sales* leadership and partner marketing. It drops "Head of Partnerships", "Head of Events" and "VP BD". |
| Seniority | VP / Director / Head / C-suite | C-level, VP, Director. Avoid individual contributors (AEs, marketing specialists) | **Confirms** |
| Dream companies | Workday, Ivalua named as partners | GEP, Infor, Manhattan Associates, Flexport, e2open | **New, and pointed.** All five are supply-chain/procurement vendors, so the CSCO/CPO community is the client's top priority. |
| Signals | Nordic expansion, sponsoring similar events, new Nordic leadership hires (inferred) | Same three: event sponsorship (esp. Nordics/NL), Nordic/NL expansion, hiring field marketing / sales leadership | **Confirms** |
| Tone | Polished, premium, understated | Friendly/Casual + Consultative | **Contradicts** the brief's guess. Use the client's tone. |
| Offer / CTA | `[MISSING]` | A free tailored executive engagement plan for 2027; ask for a 20-minute call; Nordic CIO Pulse 2026 research (with Nord-IQ) as a hook | **Fills the gap** |
| Proof | Workday, Ivalua | 80+ events a year, 1,500+ executives; Oracle, Palo Alto Networks, SAP, Workday, Wonderful, Wiz, Zscaler | **Fills the gap** (also the likely DNC) |
| Exclusions | `[MISSING]` | DNC xlsx uploaded, but not in `dncList` | **Gap still open.** See DNC above. |

## Campaign docs

| Doc | tracking_clients doc id | Status | Shared with client | Repo copy |
|---|---|---|---|---|
| twoHundred Campaign Ideas (10 campaigns) | `a4c10f55-28e7-420e-9040-d8fe8a80ee51` | **configs_created** (approved by twoHundred 2026-11-12 09:03 UTC; 10 campaigns built 11:44 to 11:49 UTC) | yes, [portal](https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=a4c10f55-28e7-420e-9040-d8fe8a80ee51) | [`campaigns/2026-11-06-campaign-ideas.md`](campaigns/2026-11-06-campaign-ideas.md) |

A dashboard-created empty doc `6752b493-460c-4f6d-835f-d3e5a5d5f849` ("Nov 6, 2026") existed briefly. By 11:30 it no longer appeared in `list_campaign_docs`, so it was removed from the dashboard (not by this session).

## GTM Sheets

Folder **Clients / twoHundred** (`2bef52d8-773d-46f7-a1ce-80e964c8dc6f`): https://dashboard.algoacquisition.ai/gtm-sheet#/gtm-sheet?folder=2bef52d8-773d-46f7-a1ce-80e964c8dc6f

The layout follows CLAUDE.md "GTM Sheets build standard per campaign":
- One workbook per campaign, linked to its tracking_clients campaign and named after its HeyReach campaign, without the "| Moe v1" label.
- The tables run from widest to narrowest.
- Every table is a webhook table loaded from the repo CSVs with `gtm-sheets/build_rows.py` and `gtm-sheets/push_rows.py`.
- Each Leads table is linked to its lead list.
- Each Leads table has a **Push to HeyReach** column wired to its DRAFT campaign and custom fields, with auto-run off and run_if `Status = "launch set"`. **None has been run.**

Webhook URLs can write to their tables, so they are not stored here. Get them from `gtm_sheet_get_table`.

| # | Workbook | Workbook id | Tables (ids) | Push custom fields | Rows (2026-11-13) |
|---|---|---|---|---|---|
| C1 | EU \| CPO and CSCO Table | `31a3b2d8-476e-4050-9211-28b78f77fea0` | 1. Companies `d55b5692-332c-4897-ba82-279d146f74f0` · 2. Leads `0fe4a8a3-be04-48dd-a7df-dcf69647c5fd` | none | **57 / 75**, matching the CSVs |
| C2 | EU \| Beyond the Expo Hall | `44762757-2785-41fe-adb7-138f620279be` | 1. Companies `39dee59e-6b17-45b9-992d-03645d4be3df` · 2. Events `625e5158-4ee0-46a6-8822-8efd5c6242d6` · 3. Leads `7c0d36a9-bd3f-4760-843f-22f27fb19e2b` | event_name, event_city | 0 (not sourced — needs Clay/web) |
| C3 | EU \| New in the Seat | `9c570e1a-aea8-4b29-ba1d-b690dd240e4a` | 1. Companies `5fd30b12-26f8-4427-9746-9010e21cf436` · 2. Leads `a4eee010-0bec-4f39-94c5-a9c9069894d4` | none | 52 / 54 |
| C4 | EU \| Entering the Nordics | `3881ea7f-c534-4fd1-a5a7-21041c7404f6` | 1. Companies `8c7965db-38c6-49e0-877e-a50716568456` · 2. Leads `d3657225-aade-4505-b7b7-fdf95e67a343` | expansion_short, country | 0 (not sourced — needs Clay/web) |
| C5 | EU \| The CISO Room | `9f42bf55-e178-4f24-aaee-114f1bf667ae` | 1. Companies `e2eeb8f0-ba3b-4b94-91fd-9c3b29523694` · 2. Leads `983e9dce-5cfd-4aa6-820a-6c3cd24a87f3` | none | 230 / 451 |
| C6 | EU \| Nordic CIO Pulse | `8a4d4698-866c-4651-b25a-b8200d8dbcb8` | 1. Companies `ca7b16ae-5e10-4292-8476-c0980d5d9966` · 2. Leads `e5076df4-c667-4709-9ac2-890b1c5ba6a8` | category_short | 606 / 887 |
| C7 | EU \| Finance and People Leaders | `bc567d3e-925f-40a1-852c-f85164f2f7ec` | 1. Companies `78b80375-e422-4980-aea5-8a1a16a02f80` · 2. Leads `dfb1ebbb-1cb5-4581-9b7b-efde774ddcdd` | community | 259 / 500 |
| C8 | EU \| Open Roles Field & Event Mktg | `975206e5-77fe-460e-a885-a88725ab2370` | 1. Companies `a19ca4cc-88c9-4e2b-a508-02fde75c7407` · 2. Jobs `7513b2f5-b486-4328-ab11-6424c435154c` · 3. Leads `a193164f-fffb-4f08-a6f5-e466dd4a1189` | open_role, open_role_with_article, jd | 6 / 6 / 10 |
| C9 | EU \| Open Roles Country & Sales Lead | `33ac4fe5-1d28-46ab-9af6-378cce264efa` | 1. Companies `b743148f-1ff6-4c4c-be4f-ccf014f3df61` · 2. Jobs `4a0f88f5-4d0f-420c-abeb-c44d456badea` · 3. Leads `3ce5a309-fb59-4c8c-83b0-037b02378c45` | open_role, open_role_with_article, jd, country | 36 / 36 / 70 |
| C10 | EU \| Open Roles ABM Demand Partner | `6b3e059b-3cd3-49fa-9b04-ad9e64c6567b` | 1. Companies `eeca528d-d95d-4819-9ff0-bab8c91b720c` · 2. Jobs `f3ce1075-f7d6-4f6a-8301-a548c0a51c6a` · 3. Leads `083ae857-32ef-459e-b408-7becce7b219e` | open_role, open_role_with_article, jd | 8 / 8 / 14 |

**Notes:**
- In C4 and C9 the variable `country` lives in a column called "Target Country", because GTM Sheets treats "Country" and "country" as the same name. The lead's own country column there is "Lead Location".
- HeyReach still shows the campaigns with the "| Moe v1" label: renaming needs the UI (see History 2026-11-13).

## Sourced data in this repo

- `sourcing/c1-cpo-csco-table/2026-11-13-companies.csv`: **57 companies**, 24 of them with 0 leads (kept so the drop-off shows). Config "The CPO and CSCO Table" (`b81f2795-76e8-4f63-a8d0-3f0d53cabf6e`), campaign `094e9b70-89e2-414f-b48b-8eb7d9ae45e3`. Blitz API `/v2/search/companies` plus `/v2/enrichment/company`, pulled 2026-11-13. Query: `2026-11-13-leads.query.md`.
- `sourcing/c1-cpo-csco-table/2026-11-13-leads.csv`: **75 leads** at 33 companies, keyed on `linkedin_url`. Same config. Blitz API `/v2/search/employee-finder`, pulled 2026-11-13.
- `sourcing/c3-new-in-the-seat/`: **52 companies / 54 leads**, config `82f47ea4-d434-444c-830f-4fffa6d5c2fe`, campaign `919f494a-06d5-439f-9f3c-7181367c75a6`. Blitz `/v2/search/people` (recent-hire). 2026-11-13.
- `sourcing/c5-ciso-room/`: **230 companies / 451 leads**, config `3b6c78bc-ec87-4bd4-b6b6-4a0d89936f4c`, campaign `0637bac6-5e24-41be-b829-25350eb83b25`. Blitz TAM + Find People. 2026-11-13.
- `sourcing/c6-nordic-cio-pulse/`: **606 companies / 887 leads**, config `52e26a7a-c209-42d5-b3e4-a81548a2a5f8`, campaign `aad8be08-a118-420c-b11c-7c1581c9baf4`. Blitz TAM + Find People. 2026-11-13.
- `sourcing/c7-finance-people-leaders/`: **259 companies / 500 leads**, config `d3ebc835-ae65-4777-a770-650a0ef0f417`, campaign `fe3ef189-38f6-42ab-ae9a-712517eace39`. Blitz TAM + Find People. 2026-11-13. `community` (CFO/CHRO) not yet classified per lead.
- `sourcing/c8-open-roles-field-event-mktg/`: **6 companies / 6 jobs / 10 leads**, config `41d63fbf-1b66-44d1-ba91-2ad0b2def817`, campaign `c8b08608-897e-4ec0-8568-fc26c2525827`. Blitz jobs + employee-finder. 2026-11-13.
- `sourcing/c9-open-roles-country-sales-lead/`: **36 companies / 36 jobs / 70 leads**, config `25cf23a0-bd3d-4d32-a8aa-9f91fb131150`, campaign `f7d16968-870a-4477-90d9-1cc32d3fd0bc`. Blitz jobs + employee-finder. 2026-11-13.
- `sourcing/c10-open-roles-abm-demand-partner/`: **8 companies / 8 jobs / 14 leads**, config `55fb215f-cad1-4d8b-890a-72f366e81b38`, campaign `65ed1c2f-4a4e-4b3e-9fe5-9b7502d6c97f`. Blitz jobs + employee-finder. 2026-11-13.
- `sourcing/c2-beyond-the-expo-hall/` and `sourcing/c4-entering-the-nordics/`: **sizing notes only, not sourced** — their event/expansion signals need Clay/web verification, which was unavailable this session. See each `2026-11-13-SIZING-ONLY.md`.
- `context/dnc-2026-11-13.csv`: the client DNC, **53 companies and domains**. It was exported from tracking_clients `dncList` on 2026-11-13; the client had now loaded it from their uploaded xlsx.

## History

- **2026-11-13**: **Sized and sourced C3 and C5 to C10** (Moe: "size them and actually source them"). All via the Blitz API on the flat plan, no extra spend. Each applied the 53-company DNC and kept only Nordic/NL-based or Nordic/EMEA-titled GTM leaders.
  - **C5 CISO Room:** 230 companies, 451 leads (3/company). **C7 Finance & People Leaders:** 259 / 500 (3/company). **C6 Nordic CIO Pulse:** 606 / 887 (2/company, widest segment). These three are the largest, in that order.
  - **C3 New in the Seat:** 52 / 54, using Blitz `is_recent_hire` (90-day) as the new-in-role signal.
  - **C8/C9/C10 open roles:** Blitz job search (Nordic postings, last 60 days) then employee-finder for the hiring manager above the role; 10, 70 and 14 leads. The `open_role`/`jd` variables are derived per company from the posting.
  - **C2 and C4 not sourced:** their event-sponsorship and expansion-news signals need Clay or web verification, and the Clay MCP was down this session. Sizing notes written instead (base universe ~16,700 Nordic GTM leaders before the signal filter).
  - **Loaded into GTM Sheets:** every sourced segment's rows were pushed through the table webhooks; counts to be reconfirmed with `gtm_sheet_get_workbook` (the tracking_clients MCP was briefly disconnected at write time).
  - **Open item:** C7 `community` (CFO vs CHRO) is not yet set per lead; fallback copy covers it until a classification step runs.
- **2026-11-13**: **Set up all 10 campaigns in GTM Sheets** (Moe: "Set all of these campaigns up in gtm sheets").
  - **Workbooks:** 10 in folder Clients / twoHundred, one per campaign, each linked to its tracking_clients campaign. There are 23 tables in all; ids are in **GTM Sheets**.
  - **Table layout:** every campaign has a Companies table first and a Leads table last. C2 has an Events table in between (its signal), and C8 to C10 have a Jobs table in between.
  - **Rows:** only C1 has data. 57 companies and 75 leads were loaded from the 2026-11-13 CSVs through the table webhooks, and the server counts match. C2 to C10 are empty until each one is sourced.
  - **Push to HeyReach:** every Leads table has the column, wired to its campaign's custom variables, with auto-run off. Nothing has been pushed.
  - **Lead lists:** every Leads table is linked to its lead list.
  - **Scripts added:** `gtm-sheets/build_rows.py` (new) and `gtm-sheets/push_rows.py` (copied from elite-technical).
- **2026-11-13**: **Opened a new segment: sourced C1 "The CPO and CSCO Table"** (config `b81f2795-76e8-4f63-a8d0-3f0d53cabf6e`, campaign `094e9b70-89e2-414f-b48b-8eb7d9ae45e3`). It produced 57 qualified companies and 75 leads, using the Blitz API.
  - **Request:** Moe, "Source the data for one and make it live".
  - **Why C1:** the client's dream accounts are all supply chain and procurement vendors, and the C1 copy only uses standard variables.
  - **TAM/SAM and depth:** the TAM/SAM is small (57 companies), so we take up to 5 contacts per company, as the doc says.
  - **DNC:** applied (53 domains, loaded by the client since the last check). Workspace dedupe: no existing leads.
  - **Cost:** about 3,700 Blitz records on a flat plan, so no extra spend.
  - **Full query:** `sourcing/c1-cpo-csco-table/2026-11-13-leads.query.md`.
  - **Not live yet:** the leads are not yet in HeyReach and the campaign has not been started. This waits on Moe's `campaign_thinking` and his go-ahead to start.
- **2026-11-13**: Set up all 10 HeyReach campaigns in workspace 172772 (Moe: "The sender accounts are set up. Proceed with the setting up of campaigns inside of heyreach").
  - **Built:** 10 DRAFT campaigns (729831, 729835 to 729838, 729840 to 729844), each with its own list. Each carries the approved doc copy, converted to HeyReach variable syntax with a fallback per message. Each is linked to its tracking_clients campaign, and all 9 senders are on every campaign. Details are in "HeyReach state".
  - **Why drafts:** none can go live yet. Still missing:
    - Moe's `campaign_thinking` (all 10 campaigns are in `creation`)
    - the DNC list
    - leads, since nothing has been sourced
    - the Forum overview and booking link
    - Sales Nav on every sender
  - **Fixed along the way:** C8 to C10's first sequence save failed on the connection-note fallback. They were re-saved on the same campaign ids, with notes that use only `{FIRST_NAME}`.
  - **Not done:** the "exclude leads in other campaigns" setting has no tool, so set it in the UI.
- **2026-11-12**: Sent a sender-setup reminder to John Paul (infra), cc Dave, in **#gtm-john** (`C0BUMA50B4M`). Moe asked for a shorter version, then for cc at the end and no Nordic mention. then for the correct John. **The final message is https://algoacquisitiongroup.slack.com/archives/C0BUMA50B4M/p1794485549422449**, tagging John (`john@algoacquisition.com`, Slack `U0AJFP48EKS`). Earlier versions in #gtm-john (p1794485411896349, p1794485427712619, p1794485486267889) and the group DM are to be deleted by hand.
  - **Why:** HeyReach workspace 172772 has no LinkedIn accounts, infrastructure was never submitted, and there are no client accounts or VSDRs.
  - **Earlier copy:** the same message went first to a new group DM (`C0CH4BWE5KL`, p1794485320760809). Moe asked for that one to be deleted and the reminder sent to the GTM/John channel instead. The Slack connector has no delete tool, so the DM copy has to be deleted by hand in Slack.
- **2026-11-12**: Built all 10 campaigns from the approved doc in tracking_clients (Moe: "set up the campaign from the document and bring them to make live position"). Each one has its own ICP config (one segment and one persona), its own lead list and its own new-system campaign. The ids are in the Campaigns table.
  - **Sequences:** saved with `set_campaign_sequence`, all passing validation. Variables follow the rules namespace: `{{module.standard.first_name|company_name}}` and `{{module.custom.*}}` for event_name, event_city, expansion_short, country, category_short, community, open_role, open_role_with_article and jd. Campaigns 1 to 7 send the connection request blank (no note), which the validator accepts.
  - **Copy kept elsewhere:** the open-role fallback copy and the CTA variants are stored in each campaign's `linkedin_sequence` text and notes, not in the structured sequence. The sequencer is dumb, and Clay assembles fallbacks upstream.
  - **Doc status:** set to `configs_created`.
  - **Tool issue:** `create_campaigns_from_plan` was refused because the server asks for `confirm:true`, a field the tool schema doesn't expose on either connector. So the 30 objects were created one by one (`create_icp_config`, `create_sourcing_config`, `create_campaign`). Flag this to whoever maintains the MCP.
  - **Lead lists:** `campaign_split: false` on all 10, chosen without asking because each list feeds exactly one campaign.
  - **Sourcing mode:** this makes sourcing campaign-specific (one list per campaign), which answers the open "general vs campaign-specific" question by default.
  - **Not done, and why:**
    - `send_campaign_for_approval` needs `campaign_thinking` in the operator's own words, and the tool forbids writing it for him, so all 10 stay in `creation` until Moe supplies it.
    - No HeyReach campaigns exist yet: there are no senders in workspace 172772.
    - No leads exist yet: nothing has been sourced, and the DNC is not loaded.

- **2026-11-12**: twoHundred **approved** campaign doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51` in the portal (`signed_name: twoHundred`, `signed_at: 2026-11-12T09:03:30Z`), confirmed by `list_campaign_docs` and `get_campaign_doc`. They made no text changes and left no new comments. The 4 earlier threads stay open in the UI, each with our reply.
  - **Still not supplied:** the Forum overview link or PDF that we asked for.
  - **Next, per the tool's workflow:** build the 10 campaigns with `create_campaign` and `campaign_doc_id`, then set the doc to `configs_created`. Not started; waiting on Moe.

- **2026-11-12**: Re-sent campaign doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51` to twoHundred (`send_campaign_doc_to_client`, Moe: "Send it"). Status is back to `client_review`, and the portal link was posted to the client's Slack (`notified_client.ok: true`).
  - **Slack note:** summarised the changes (partners excluded, CIO Pulse link in, Forum-overview offer) and asked for the Forum overview as a link or PDF.
  - **Next:** the client approves (then build the campaigns), comments again (`internal_review`), or sends the Forum overview link.

- **2026-11-12**: Resolved twoHundred's 4 portal comments on campaign doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51` (status `internal_review`) with `review_campaign_doc`: 35 tracked edits, all accepted, plus a reply on each comment. `replace_markdown` was not used, so the client's comment threads stay visible. The comments and how each was resolved are in `campaigns/2026-11-06-campaign-ideas.client-comments.md`.
  - **What changed in the plan:**
    - All partners are excluded.
    - Partner names may be used in messages.
    - The CIO Pulse link `https://hubs.ly/Q04DzhC10` was checked and now replaces `{pulse_link}`.
    - **The offer changed:** the client says a tailored plan is only possible after a call, so messages now offer an overview of the 2027 Forum events up front, and roundtables and the tailored plan come from the call. This also replaces the open-role campaigns' bespoke one-pagers.
  - **Waiting on the client:** the Forum overview link or PDF, requested in the reply to comment #7.
  - **Not re-sent yet:** waiting for Moe's go-ahead, because `send_campaign_doc_to_client` posts in the client's Slack.
  - **Attribution:** the tracking_clients connector in this session wrote these edits as `mcp:dave@algoacquisition.com`. The comment author is "Algo Acquisition".

- **2026-11-06**: Removed the "Lead magnet:" line from all 10 campaigns (Moe: "remove the lead magnet section for now"). Then sent doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51` to the client with `send_campaign_doc_to_client`.
  - **Result:** status `client_review`, shared with the client, and the portal link was posted to twoHundred's Slack channel (`notified_client.ok: true`).
  - **Before replacing:** Moe had edited the doc at 11:27, but that change only set sharing. The text matched the repo copy and there were no comments, so `replace_markdown` lost nothing.
  - **Still in the doc:** the offers inside the messages (engagement plan, CIO Pulse, open-role one-pagers) and the matching Before launch items. Only the per-campaign Lead magnet field was removed.
  - **Next:** wait for the client's comments (status flips to `internal_review`), then revise and re-send.

- **2026-11-06**: Campaign doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51` expanded from 7 to 10 campaigns (`update_campaign_doc` replace_markdown). The doc had no comments or suggestions to lose, and the dashboard copy matched the repo before the replace. It is still a draft and not shared.
  - **Why:** Moe asked for 3 open-role campaigns in the MPC format: the open posting is the hook, the connection note names the role, and Message 1 offers one ready-made thing that fits the seat. This mirrors Elite Technical's "we have a candidate who fits that pretty closely" copy, `clients/elite-technical/campaigns/2026-11-05-recruiter-open-role-copy.json`.
  - **What fills the "candidate" slot:** twoHundred has no candidates to place, so the slot becomes a ready-made executive programme for the hire:
    - Campaign 8: an events programme
    - Campaign 9: a first-90-days plan for the country
    - Campaign 10: a target-account roundtable plan
  - **The three new campaigns** are all sent to the hiring manager above the open seat, never the seat itself:
    - **8. Open Roles, Field and Event Marketing**
    - **9. Open Roles, Country and Sales Leadership**
    - **10. Open Roles, ABM, Demand and Partner Marketing**
  - **Campaign 4 changed** from "Building the Nordic Team" (hiring signal) to "Entering the Nordics" (office, entity or partner news). Otherwise it would compete with 8–10 for the same companies.
  - **New rules:** a one-campaign-per-company priority order (open roles first), with fallback copy for empty `{open_role}` and `{jd}`.
  - **Before launch:** the three one-pagers must exist before 8–10 can launch.

- **2026-11-06**: Campaign doc "twoHundred Campaign Ideas" uploaded to the dashboard (`create_campaign_doc`, doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51`). It is a draft and not shared with the client. The repo copy is `campaigns/2026-11-06-campaign-ideas.md`.
  - **Why:** Moe asked for a campaigns doc "like we have created before". It follows the format of the GigWorx and GRN Piedmont "Campaign Ideas" docs: shared section, then ICP / Persona / Lead list / Messaging per campaign, a yes-reply and Before launch.
  - **The 7 campaigns:**
    1. CPO and CSCO Table (supply chain/procurement vendors, the dream list)
    2. Beyond the Expo Hall (Nordic/NL event sponsors)
    3. New in the Seat (new regional leaders)
    4. Building the Nordic Team (hiring Nordic commercial leadership)
    5. CISO Room
    6. Nordic CIO Pulse (research hook)
    7. Finance and People Leaders (CFO/CHRO)
  - **Contacts per company:** follows segment size inversely. Narrow segments get 4–5 contacts per company, wide segments 2–3. The segment sizes are estimates; no sourcing has run.
  - **Open points (in the doc's Before launch):** DNC still not loaded, the partner-exclusion decision, permission to name partners in messages, a shareable CIO Pulse, senders and the booking link.
  - **Nothing created** in tracking_clients configs/campaigns or HeyReach.

- **2026-11-06**: Folder created from `clients/_TEMPLATE/README.md`. Profile synced from tracking_clients (`get_client`, `list_sourcing_configs`, `list_icp_configs`, `list_campaigns`: all empty), and context saved to `context/`.
  - **Why:** this is the first per-client session for twoHundred. It follows the orchestrator's hand-off and Moe's "this session is for twoHundred".
  - **Domains:** checked that twohundred.dk redirects to twohundredgroup.com.
  - **HeyReach:** workspace 172772 has 0 campaigns and 0 seats, and this session has no direct connector for it.
  - **Flagged for Moe:** the client's uploaded DNC xlsx is missing from `dncList`, and tracking_clients' website should be confirmed.
  - **Nothing created** in tracking_clients or HeyReach. The segment/TAM proposal is waiting for Moe's OK.
