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
| `-` | `-` | `-` | `-` | `-` | `-` | `-` |

As of 2026-11-06, `list_sourcing_configs` returns 0 configs, `list_icp_configs` returns `[]` and `list_campaigns` returns 0. Nothing is created yet: the segment breakdown below is waiting for Moe's OK.

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
| twoHundred Campaign Ideas | `a4c10f55-28e7-420e-9040-d8fe8a80ee51` | draft | no | [`campaigns/2026-11-06-campaign-ideas.md`](campaigns/2026-11-06-campaign-ideas.md) |

## Sourced data in this repo

- `-`: no snapshots yet.

## History

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
