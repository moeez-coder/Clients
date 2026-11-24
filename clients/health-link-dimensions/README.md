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
| HealthLink Dimensions Campaign Plan, Doc 1 (10 campaigns) | `1f2e4277-1a09-445e-8684-75cc542ab003` | `client_review` (sent 2026-11-09) | `campaign-docs/2026-11-09-doc-1.md` |

Portal link: https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=1f2e4277-1a09-445e-8684-75cc542ab003

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| `-` | `-` | `-` | `-` | `-` | `-` | `-` |

No ICP configs, sourcing configs or campaigns exist in tracking_clients as of 2026-11-09. By the tracking_clients rule, none should exist until the client approves a campaign doc.

## Sourced data in this repo

No lead or company snapshots yet. A pull can only happen after the client approves doc 1. The sizing read is on disk:

- `sourcing/tam/2026-11-09-tam-read.query.md`: the TAM/SAM read for the 5 doc-1 segments, with no config yet (config `-`).
  - Blitz API `POST /v2/search/companies` and `POST /v2/jobs/search`, counts only with `max_results: 1`, 15 records used.
  - Clay MCP `search-companies`: a 20-row fit sample for segment 1.
  - Pulled 2026-11-09.
- `sourcing/tam/tam_counts.py` and `sourcing/tam/tam_counts.json`: the script and its exact request bodies and results.
- `sourcing/tam/2026-11-09-clay-sample-seg1.json`: the Clay sample, with a fit verdict per company.

## History

- **2026-11-09**: **Campaign doc 1 sent to the client** (`send_campaign_doc_to_client`, on Moe's explicit instruction: "Make the doc and send it to the client").
  - Status is now `client_review` and the doc is shared in the portal. The Slack notification went to C0CD0RXFBS4 (`notified_client.ok: true`).
  - **Next:** wait for the client's comments. When the status becomes `internal_review`, respond with `review_campaign_doc`, not `replace_markdown`.
  - **Nothing created** in ICP, sourcing or campaign configs, or in HeyReach.
- **2026-11-09**: **Campaign doc 1 created** (`create_campaign_doc`, doc `1f2e4277-1a09-445e-8684-75cc542ab003`, "HealthLink Dimensions Campaign Plan, Doc 1"). The repo copy is `campaign-docs/2026-11-09-doc-1.md`, with the same markdown that was submitted.
  - **Campaigns 1 to 5 are MPC (open-role) campaigns**, one per ICP-form segment.
    - The connection note and the Message 1 opener follow the SOP copy verbatim.
    - The "candidate" slot becomes the client's own offer, a free HCP data review, following the twoHundred non-recruiter precedent.
    - Each message goes to the leader above the open seat.
    - `{jd_phrase}` maps to the JD Phrase AI column described in the SOP, Step 7a.
  - **Campaigns 6 to 10 are trigger variants of segments 1 to 5:**
    - 6: FDA approval or PDUFA date
    - 7: funding or M&A
    - 8: FDA device clearance
    - 9: a new leader in their first 90 days
    - 10: agency account wins
    - Their copy follows the campaign-plan-builder format: a connection note with proof, then Message 3 opening with "Asking because".
  - **Contacts per company follow the inverse rule.**
    - The MPC pools are small, about 60 to 250 hiring companies per 90 days. So segments 1 to 4 get 3 to 4 contacts per company, agencies get 2, triggers 6 to 8 get 3, trigger 9 gets 1 (the new leader only) and trigger 10 gets 2.
    - The read behind this is in `sourcing/tam/2026-11-09-tam-read.query.md`.
  - **New segments.** The TAM read for each one:
    - Blitz company TAM: 3,090, 22,169 (noisy), 5,508, 553 and 3,317.
    - 90-day matching postings: 205, 264, 272, 337 and 1,862 (the agency figure is not filtered to health).
  - **The client's ICP form and the brief disagree.**
    - The ICP form's segments differ from the brief's: there are no hospitals, health plans or CME. Moe chose the ICP form.
    - The brief's segments 1 (pharma) and 4 (agencies) map to doc segments 1, 2, 4 and 5. The device segment appears only in the ICP form.
  - **Flagged in the doc's "Before launch" section:**
    - The DNC and client-list exclusions are empty. The Clay sample already hit 3 existing clients: EVERSANA, Incyte and Allergan/AbbVie.
    - Reply owner and booking link are still needed.
    - The client needs to approve use of the "11 of 15 largest pharma" claim, which is website-sourced.
  - **HeyReach:** no connector for workspace 170993 is visible in this session. Moe says he added a "healthkit" connector, but it does not show up here; a fresh session should pick it up. It is needed only for the post-approval dedupe.
  - **Not done:** the MPC SOP (`docs/sops/open-role-moe-mpc.md`) and the shared tooling still live on unmerged branches. They were read only, not copied.
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
