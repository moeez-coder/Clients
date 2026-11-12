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
  - Infrastructure: john.paul@algoacquisition.com
  - Closer: vince@algoacquisition.ai
  - Sourcing engineer: `-` (unassigned)
- **Slack channel ID:** C0CEBCSU53R
- **HeyReach workspace:** `172772`, named "twoHundred" (heyreachConnected: true).
  - **This session has no HeyReach MCP connector for 172772** (checked 2026-11-06). 24 HeyReach connectors respond and map to other clients' workspaces; none matched "two". 5 connectors return 401.
  - Reads go through tracking_clients' stored key (`gtm_sheet_list_heyreach_campaigns`, `get_client_stats`).
  - Instantly, Smartlead and PlusVibe are not connected. masterInboxWorkspaceId is `-`.
- **Infrastructure:** not submitted to infra (`infrastructure` is `{}`).
- **Booking link:** `-` (blank). `replyWorkflowN8nId`: no campaigns exist yet.
- **Gaps in tracking_clients:** these are recorded, not filled by guessing.
  - `callTranscript` is empty.
  - SDR defaults (headline, about, position, location, banner) are empty.
  - `sampleReportUrl` is empty.
- **DNC:** `dncList` is empty (0 entries) and `dncSkipped` is false. **But the ICP form says the client uploaded a DNC file:** `31a7eb95d165-Do_Not_Contact_twoHundred_enriched.xlsx`.
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

| # | Campaign | session id | Lead list (sourcing config) | ICP config |
|---|---|---|---|---|
| C1 | The CPO and CSCO Table | `094e9b70-89e2-414f-b48b-8eb7d9ae45e3` | `b81f2795-76e8-4f63-a8d0-3f0d53cabf6e` | `94a6a632-88eb-43cb-8401-9b286033fa17` |
| C2 | Beyond the Expo Hall | `a767b822-f1d5-422b-acba-e536d54882b4` | `c659923d-b864-4572-a5f9-6034425882a9` | `b359767a-463a-4e85-abe5-7b625be7f013` |
| C3 | New in the Seat | `919f494a-06d5-439f-9f3c-7181367c75a6` | `82f47ea4-d434-444c-830f-4fffa6d5c2fe` | `92d229b6-875a-43ab-9f50-2749bd6913f9` |
| C4 | Entering the Nordics | `51e55b6c-f97f-4a5a-9109-4bd7f730598d` | `a42149fc-d3ac-44d4-86e6-aa5a856d1827` | `35d03c8c-ab82-4053-8e9c-55e9cb1ebb01` |
| C5 | The CISO Room | `0637bac6-5e24-41be-b829-25350eb83b25` | `3b6c78bc-ec87-4bd4-b6b6-4a0d89936f4c` | `ee1bb78d-8fd4-4826-a689-3e0a07844836` |
| C6 | Nordic CIO Pulse | `aad8be08-a118-420c-b11c-7c1581c9baf4` | `52e26a7a-c209-42d5-b3e4-a81548a2a5f8` | `4b955c4a-326c-495c-beab-da078d093bf9` |
| C7 | Finance and People Leaders | `fe3ef189-38f6-42ab-ae9a-712517eace39` | `d3ebc835-ae65-4777-a770-650a0ef0f417` | `0694d62b-8932-4f8c-8dc9-c9467de0cec6` |
| C8 | Open Roles, Field and Event Marketing | `c8b08608-897e-4ec0-8568-fc26c2525827` | `41d63fbf-1b66-44d1-ba91-2ad0b2def817` | `99443fa9-fbcf-450e-bcfe-89a57e40b5a1` |
| C9 | Open Roles, Country and Sales Leadership | `f7d16968-870a-4477-90d9-1cc32d3fd0bc` | `25cf23a0-bd3d-4d32-a8aa-9f91fb131150` | `01f08a0f-2a51-426f-9aad-7c0f8b128671` |
| C10 | Open Roles, ABM, Demand and Partner Marketing | `65ed1c2f-4a4e-4b3e-9fe5-9b7502d6c97f` | `55fb215f-cad1-4d8b-890a-72f366e81b38` | `f9c2c642-d732-420c-bf3f-7b90812be327` |

## HeyReach state (2026-11-06)

- Workspace 172772 "twoHundred": **0 campaigns** (`gtm_sheet_list_heyreach_campaigns`). Last 7 days: zero activity, with 0 connections and 0 messages sent (`get_client_stats`).
- **0 LinkedIn seats** in tracking_clients (`list_client_accounts`: no client accounts, no Virtual SDRs, no sync rows). There are no senders to audit yet: auth, Sales Nav, limits and cooldowns are all n/a.
- **Not checked yet:** lists and blacklist. These need a HeyReach connector for 172772, and none is available in this session.

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

## Sourced data in this repo

- `-`: no snapshots yet.

## History

- **2026-11-12**: Sent a sender-setup reminder to John Paul (infra), cc Dave, in **#gtm-john** (`C0BUMA50B4M`). Moe asked for a shorter version, then for cc at the end and no Nordic mention. The final message is https://algoacquisitiongroup.slack.com/archives/C0BUMA50B4M/p1794485486267889. Earlier versions in #gtm-john (p1794485411896349, p1794485427712619) are to be deleted by hand.
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
