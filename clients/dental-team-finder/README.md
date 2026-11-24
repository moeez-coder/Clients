# Dental Team Finder

## Profile

- **Status:** active (approved, not archived)
- **Package tier:** Solo (clientType `solo`). 6 months paid in full ($3,391 via Whop, 16 Nov 2026).
- **Website:** https://dentalteamfinder.com
- **Contact:** Keith McLachlan <keith@dentalteamfinder.com>
- **Booking link:** https://calendly.com/keithmclachlan
- **Slack channel ID:** `C0CM0LD8M4Y`
- **Tracking client ID:** `75ad60f0-a5fa-4a41-816b-bbe5ee2fb69f`
- **HeyReach workspace:** `176441` (heyreachConnected: true). In sessions this is the HeyReach connector `mcp__57f97f59-7397-4cf1-a06a-f55f6c2f241d__*`, the connector whose `list_workspaces` returns `176441 Dental Team Finder` (checked 2026-11-24). Instantly, Smartlead and PlusVibe are not connected; masterInboxWorkspaceId `-`.
- **Staff:** campaign strategist moeez@algoacquisition.ai; infrastructure john.paul@algoacquisition.com; GTM engineer `-`; sourcing engineer `-`; closer `-`.
- **Infrastructure:** 5 LinkedIn seats, 10 VA seats, submitted to infra 2026-11-23.
- **DNC list:** empty in tracking_clients (`-`).
- **What they do:** dental-only recruiting and consulting. Outreach targets commercial leaders (CEO, CRO, VP Sales/Marketing, Directors and Regional Managers of Sales) at dental manufacturers, dental AI/software, supply/distribution and DSO groups with corporate commercial teams. US and Canada, 51 to 1,000 staff, $5M+ revenue. Dream accounts: Overjet, Pearl, VideaHealth, Align Technology.
- **Hard client rule:** Keith reviews and approves all copy before anything is sent.
- **Last synced:** 2026-11-24 via `get_client` + `list_sourcing_configs` + `list_campaign_docs` + `list_campaigns` (tracking_clients), and HeyReach `get_all_campaigns` (workspace 176441).

## Sourcing configs

No sourcing configs exist in `tracking_clients` (`list_sourcing_configs` count 0, 2026-11-24). Per the campaign doc standard, none are created until Keith approves the campaign doc.

| Config | ICP | Market | Scope | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - | - |

## Campaign docs

| Doc | tracking_clients id | Status | Shared | Signed | Repo copy |
|---|---|---|---|---|---|
| Nov 23, 2026: "Dental Team Finder: First 3 Campaigns" | `d239cd9e-918f-4798-be92-0500ea42e87e` | `client_review` (0 open comments, 0 open suggestions) | yes | not yet | `campaign-docs/2026-11-23-first-3-campaigns.md` |

The doc's three campaigns, all sending from Keith's own LinkedIn account:
1. **Is That Role Still Open? (Most Placeable Candidate)** – one campaign per candidate Keith supplies; job-post scrape (LinkedIn + Indeed), hiring manager via Sales Navigator, offer = free anonymised candidate profile.
2. **Keith's Network, Relationship First** – Keith's 1st-degree connections at dental companies in target titles; offer = virtual coffee.
3. **Dental Commercial Team Health Check** – Sales Navigator search of target titles at in-range dental companies plus the 4 named accounts, recently funded first; offer = free 30-minute consultation (normally $350).

**Gap against the 2026-11-13 campaign doc standard (flag, not fixed):** the doc has no `### Signal and data` section per campaign (no measured company/contact counts, no `sourcing/tam/` record in this repo) and no closing `## Offers for your feedback` section. It is already with the client, so any revision needs the owner's call and must go through `review_campaign_doc`, not `replace_markdown`.

## Campaigns

- **tracking_clients:** none (`list_campaigns` count 0, 2026-11-24).
- **HeyReach workspace 176441:** none (`get_all_campaigns` totalCount 0, all statuses, 2026-11-24).

### HeyReach schedules

No HeyReach campaigns exist yet, so no schedule has been set. When campaigns are built, each one gets all 7 days enabled before `start_campaign` (CLAUDE.md HeyReach schedule rule), with its days, window and timezone recorded here. Proposed default per Moe's 2026-11-24 batch instruction: **08:00–18:00 America/Chicago (US Central)**. Reasoning: prospects are US and Canada nationwide; Central sits in the middle, so 08:00–18:00 CT covers 09:00–19:00 Eastern to 06:00–16:00 Pacific, and Keith himself is in Rockdale, Texas (Central). Owner to confirm when the first campaign is built.

## Sourced data in this repo

None yet. `sourcing/` is empty; no pulls have been run for this client.

## History

- **2026-11-24** – Folder created from `clients/_TEMPLATE/README.md` (Initialization protocol); profile synced from `tracking_clients` client `75ad60f0-a5fa-4a41-816b-bbe5ee2fb69f`. Recorded the campaign doc the desktop session `session_013MzxQgZ1iGZgsFQPeR8Q71` ("Dental Team Finder setup") created and sent to Keith (doc `d239cd9e-918f-4798-be92-0500ea42e87e`, created 2026-11-23 by mcp:dave@algoacquisition.com, status `client_review`, unsigned); that work had never reached this repo, so its markdown is now committed under `campaign-docs/`. Noted the doc predates/misses the 2026-11-13 Signal-and-data and Offers sections. No sourcing configs or campaigns exist in tracking_clients. Identified the HeyReach connector for workspace 176441 (`mcp__57f97f59-…`). Session `session_013MzxQgtCdKkx5iJDyoFT42`.
- **2026-11-24** – Applied Moe's 2026-11-24 approval (orchestrator batch) that every IN_PROGRESS HeyReach campaign runs 7 days a week, 08:00–18:00 in the prospects' main timezone. Result: **no change made**. HeyReach workspace 176441 has 0 campaigns of any status, so nothing was paused, rescheduled or resumed. Recorded the proposed window (08:00–18:00 America/Chicago) above for when campaigns are built. No campaign or doc was created this session, so no task-board entry was needed under the task log rule. Session `session_013MzxQgtCdKkx5iJDyoFT42`.
