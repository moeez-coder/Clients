# Health Link Dimensions

## Profile

- **Status:** active
- **Package tier:** Custom (`clientType: core`), $8,500/month billed monthly
- **Website:** https://healthlinkdimensions.com
- **Contact:** Robert Haglund <rhaglund@healthlinkdimensions.com> (ICP form also lists mgraham@healthlinkdimensions.com for Slack)
- **Slack channel ID:** C0CD0RXFBS4
- **HeyReach workspace:** `170993` (`heyreachConnected: true`)
- **Staff:** campaign strategist Moeez; infrastructure John Paul; closer Rueban; GTM engineer `-` (unassigned); sourcing engineer `-` (unassigned)
- **Booking link:** `-` (empty in tracking_clients)
- **DNC list:** 0 entries (`dncSkipped: false`, so not yet supplied rather than waived)
- **Infrastructure:** `{}` (not yet submitted to infra)
- **Created in tracking_clients:** 2026-10-26 (by sales)
- **Tracking client ID:** `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`
- **Last synced:** 2026-11-09 via `get_client` + `list_sourcing_configs` (also `list_icp_configs`, `list_campaign_docs`: both empty)

## Context files

Verbatim copies of tracking_clients `get_client` fields, pulled 2026-11-09. Each file carries a source header.

- `context/client-brief.md` (`clientBrief`). Generated from the client description alone, before the ICP form arrived. Many fields are marked MISSING/INFERRED.
- `context/icp-form.md` (`icpForm`). The client's own Typeform answers, submitted 2026-11-04. Raw JSON.
- `context/client-description.md` (`clientDescription`)
- `context/caller-briefing.md` (`callerBriefing`)
- `context/caller-faqs.md` (`callerFaqs`)
- `callTranscript` and `notes` are empty in tracking_clients, so there is no file for them.

## Campaign docs

| Doc | tracking_clients doc id | Status | Repo copy |
|---|---|---|---|
| `-` | `-` | `-` | `-` |

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| `-` | `-` | `-` | `-` | `-` | `-` | `-` |

No ICP configs, sourcing configs or campaigns exist in tracking_clients as of 2026-11-09. By the tracking_clients rule, none should exist until the client approves a campaign doc.

## Sourced data in this repo

`-` (nothing sourced yet)

## History

- **2026-11-09**: Moe answered the three questions that were blocking campaign doc 1.
  - **MPC = "Most Placeable Candidate"**, the open-jobs campaign. Confirmed against the SOP `docs/sops/open-role-moe-mpc.md`, which is on branch `origin/claude/cg-open-role-campaigns` and not on main. Its worked example is C&G, and its proven copy runs at a 19.4% reply rate for Talent Edge and Alcor.
  - **Non-recruiter precedent:** twoHundred (branch `origin/claude/twohundred-init`, doc `a4c10f55-28e7-420e-9040-d8fe8a80ee51`, campaigns 8–10).
    - The live posting is the hook, and the message goes to the hiring manager above the open seat.
    - Since the client has no candidates, the "candidate" slot becomes one ready-made deliverable.
  - **Campaigns 6–10** are trigger-based variants of segments 1–5.
  - **Segments** follow the client's own ICP form (submitted 2026-11-04), not the earlier auto-generated brief. The five segments:
    1. Specialty pharma and commercial biotech
    2. Pre-launch and newly launched biotech
    3. Specialist med device
    4. Large pharma brand/data teams
    5. HCP agencies with media or programmatic arms
  - **Dropped for now:** the brief's hospitals, health plans and CME segments. They appear in the brief only, not in the client's form.
- **2026-11-09**: Folder created from `clients/_TEMPLATE/README.md`. Profile synced from tracking_clients (client `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`), and brief, ICP form, description and caller notes saved to `context/`. This is the first session for the client: it starts campaign doc 1 (10 campaigns, the first 5 being one MPC campaign per segment). The orchestrator resolved Moe's "healthkit" to this client, which is the only "health" match in `list_clients`. Session: claude.ai/code session_013MzxQeqnTt4RM93i4VniUQ.
