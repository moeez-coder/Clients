# Elite Technical (tracking_clients: "Elite Technical ")

> An IT and engineering staffing firm (contract and direct hire) based in Heathrow, Florida, with a large DC Metro footprint. It has 34 years in business, 400+ clients and 4,500+ placements, is woman-owned (WOSB/WBENC) and holds a DoD Top Secret facility clearance. The client's context from tracking_clients is saved verbatim in [`context/`](context/):
> - [ICP form](context/icp-form.md), submitted 2026-10-22
> - [caller briefing and FAQs](context/caller-briefing.md)
> - [DNC list](context/dnc-list.csv), 160 rows
>
> tracking_clients has no client brief, client description or call transcript.

## Profile

- **Status:** active (isApproved: true, isAlgo: false), created 2026-10-22 by `sales`
- **Package tier:** Standard
- **Website:** `-` in tracking_clients (`website` is blank). The ICP form and caller briefing both give https://www.elitetechnical.com/
- **Contact:** Joseph Monaco <jmonaco@elitetechnical.com>. The ICP form also asks for Slack invites for jjkeller@, pmosca@ and mgerardo@elitetechnical.com.
- **Staff:**
  - GTM engineer and campaign strategist: moeez@algoacquisition.ai
  - Infrastructure: john.paul@algoacquisition.com
  - Closer: rueban@algoacquisition.ai
  - Sourcing engineer: `-` (unassigned)
- **Slack channel ID:** C0CC9P7M8JC
- **HeyReach workspace:** `170370` (heyreachConnected: true). In sessions this is the HeyReach connector `mcp__18d10a27-ea89-4cf6-85b4-c7cc82b76e83__*`, the only connector whose `list_workspaces` returns 170370. Instantly, Smartlead and PlusVibe are not connected, and masterInboxWorkspaceId is `-`.
- **Infrastructure:** not submitted to infra (`infrastructure` is `{}`).
- **Booking link:** `-` (blank)
- **Gaps in tracking_clients:** these are recorded, not filled by guessing.
  - `website`, `clientBrief`, `clientDescription` and `callTranscript` are empty.
  - SDR defaults (headline, about, position, location, banner) are empty.
  - There are no ICP configs, sourcing configs or campaigns.
- **DNC:** `dncList` has 160 entries and `dncSkipped` is false. All 160 are historical clients scraped from `elitetechnical.com/for-business/clients-served/`. Every row has the status "Review before outreach; exclude pending account-owner confirmation". **No row has a domain** (`Company Domain (verify)` is blank on all 160), so exclusion has to match on company name.
  - By industry: Aerospace & Defense 53; Commercial Enterprise/Financial/Media 43; Health Care/Medical Device 21; Systems Integrators 16; Emerging Technology 14; Federal & State Governments 13.
  - None of the five "dream companies" in the ICP form (AeroVironment, TransMedics, Varonis, Tenable, Commvault) is on the DNC list.
- **Tracking client ID:** `254dc33b-4f9f-4712-9b6b-eca49c5a5ffc`
- **Last synced:** 2026-10-29 via `get_client` + `list_sourcing_configs` (+ `list_icp_configs`, `list_campaigns`)

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| `-` (none exist in tracking_clients as of 2026-10-29) | `-` | `-` | `-` | `-` | `-` | `-` |

## Campaigns (tracking_clients)

None. `list_campaigns` returned 0 on 2026-10-29.

### HeyReach (workspace 170370), checked 2026-10-29

- **Campaigns:** 0. **Lists:** 0.
- **Company blacklist:** 0 entries. **Lead blacklist:** 0 entries. **The 160-company DNC list is not loaded into HeyReach.**
- **Webhooks:** three workspace-wide `hr-inbox` webhooks go to `dashboard.algoacquisition.ai/api/hr-inbox/webhook/254dc33b-…`. All are active and cover all campaigns:
  - EVERY_MESSAGE_REPLY_RECEIVED (95980)
  - MESSAGE_SENT (95981)
  - INMAIL_SENT (95982)

  There are no Clay (Acc/Open) webhooks yet.
- **Senders (11).** Every account has `authIsValid: true`. None has a valid Sales Navigator or Recruiter seat, none is active or in a campaign, and none is on a search, connection, note or InMail cooldown.

  | id | Name | Conn-req limit / max | InMail limit / max | Note |
  |---|---|---|---|---|
  | 232663 | Rodalen Villarias | 25 / 40 | 40 / 40 | |
  | 263924 | aileen tiozon | 25 / 40 | 40 / 40 | |
  | 264166 | Paulo Peñera | **3** / 40 | **8** / 40 | low limits, likely still warming |
  | 264348 | Annaly Valdez | **3** / 40 | **8** / 40 | low limits, likely still warming |
  | 265355 | Juvy Putis | **3** / 40 | **8** / 40 | low limits, likely still warming |
  | 265543 | Dezirie Retuerto | **3** / 40 | 40 / 40 | low conn-req limit |
  | 266010 | Charity Calmerin | 25 / 40 | 40 / 40 | |
  | 266511 | Neil Aron Pascual | 25 / 40 | 40 / 40 | |
  | 267035 | James Keven Gallardo | 25 / 40 | 40 / 40 | |
  | 267167 | Cyrylle Booc | 25 / 40 | 40 / 40 | |
  | 267224 | Mike Gerardo | 25 / 40 | 40 / 40 | probably client staff: mgerardo@elitetechnical.com is on the Slack invite list. Confirm before using as a sender |

  That gives about 7×25 + 4×3 = **187 connection requests a day** across the pool at current limits. With no Sales Nav seat on any account, Sales Nav search URLs can't be run from this workspace.

## Sourced data in this repo

`-` (no snapshots yet)

## History

- **2026-10-29**: Folder created and initialized for client `254dc33b-4f9f-4712-9b6b-eca49c5a5ffc`, following the CLAUDE.md init protocol.
  - Synced the profile from `get_client`. `list_sourcing_configs`, `list_icp_configs` and `list_campaigns` all came back empty.
  - Saved the ICP form, caller briefing/FAQs and the 160-row DNC list to `context/` verbatim. The Typeform response token and workflow IDs were left out of the ICP form.
  - Ran a read-only audit of HeyReach workspace 170370. It has 11 valid senders, none with Sales Nav and 4 on low limits; no campaigns or lists; an empty blacklist; and only the hr-inbox webhooks.
  - Why: this is a new client with no repo folder, so everything downstream needs this baseline. Nothing was created or changed in tracking_clients or HeyReach.
  - Next: segment proposal for Moe's sign-off before any ICP, sourcing config or campaign is created.
