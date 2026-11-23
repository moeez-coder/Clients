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
- **Booking link:** https://bookings.cloud.microsoft/book/WeAreDNA1@wearedna.co.uk/ (set in tracking_clients by 2026-11-16)
- **DNC:** `dncList` now holds **143 companies** (loaded into tracking_clients after 2026-11-12; `dncSkipped` false). Copy at `context/dnc-list.csv`. It includes Pets at Home, Medivet, Dunbia, Aesop and OVO, and 10 names match the GPG list by exact name. Campaign 6's 491 leads were pulled before it was loaded and have **not** been checked against it yet.
- **Infrastructure:** `{"vaSeatCount": 10}`. `callTranscript` and `notes` are empty.
- **Created in tracking_clients:** 2026-11-02 (`createdBy: sales`)
- **Tracking client ID:** `f5ff426b-c514-4a64-91b0-0e141a6a0669`
- **Last synced:** 2026-11-18 via `get_client` + `list_sourcing_configs` + `list_campaigns` + `list_client_accounts` + `get_campaign_senders` (no drift: DNC 143, 1 config, 1 campaign (C6, `creation`); HeyReach 172307 holds only the 10 VA seats, no founder account)

**Who they are:** a Bristol creative agency, trading since 2010. They work across three pillars: Employer Branding, Employee Engagement, and Marketing Solutions, using their BrandShift™ method. **They are not a recruitment agency** and charge no placement fees. Deal value is about $45k and the sales cycle is about 12 weeks (ICP form).

## Context files

These are verbatim copies of tracking_clients fields, each with its source in a header comment.

- `context/client-brief.md`: `clientBrief`, generated before the ICP form existed, so most ICP fields are `[MISSING]`
- `context/icp-form.md`: `icpForm`, the client's own answers (submitted 2026-11-10), rendered as Q&A
- `context/client-description.md`: `clientDescription`
- `context/caller-notes.md`: `callerBriefing` + `callerFaqs`
- `context/dnc-list.csv`: `dncList`, 143 rows (`company_name`, `company_domain`), pulled 2026-11-16

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| PE investment triggers \| Exa news + Blitz waterfall \| 2026-11-16 | Trigger \| Fresh Investment, PE-Backed Growth \| UK five sectors | Health, care, vet, dental; retail and hospitality; manufacturing and engineering; law and accounting; financial services | draft (static, campaign_split false) | UK \| Fresh Investment PE-Backed Growth \| C6 \| Moe v1 | - (leads loaded via GTM Sheets, not the lead list ingest) | - |

Created 2026-11-16 by this session (`create_icp_config`, `create_sourcing_config`): ICP config `23a03003-f8ca-4c13-bee9-05d995a938e4`, segment `48f11ee4-3fc3-46df-8e3d-9e73dd514c9f`, persona `9185c9e9-660d-4114-9833-f38918c90879`, lead list `71717207-0948-4eb9-898a-ef086122741d`. No other configs exist.

## GTM Sheets

Folder **Clients / We Are DNA** (`9a6928d3-0e80-49c3-8934-a8a1692ff121`): https://dashboard.algoacquisition.ai/gtm-sheet#/gtm-sheet?folder=9a6928d3-0e80-49c3-8934-a8a1692ff121

| Workbook | id | Tables (id, rows) | Linked campaign |
|---|---|---|---|
| UK \| Fresh Investment, PE-Backed Growth \| Campaign 6 \| Moe v1 | `851f8ca4-76f6-4f67-8576-1a8ba6524e2d` | 1 PE Deal News `2a56bc61-3fdf-4fb5-bf1e-b1236a0ea6ec` (1,119) · 2 Companies `118a97e4-4b6f-4e77-b37e-d922c2c0572d` (280) · 3 Leads `9aeb67d6-8e49-4ef4-9ff1-8cecb9714733` (491; columns Clean First Name, Clean Company, Push to HeyReach added 2026-11-16, nothing pushed yet) | UK \| Fresh Investment PE-Backed Growth \| C6 \| Moe v1 (`6ce9ac82-8714-4a82-a864-5317bb53fc91`); Leads table linked to lead list `71717207-…` |
| UK \| Glassdoor Bad Reviews \| Moe v1 | `933daaa1-121f-4f4f-b47c-1b3e91ae44ac` | Test A: Glassdoor company lookup (5) `a0ef1342-ab97-4974-bb4c-9e2ec3ce6a54` (12) · Test B: Glassdoor reviews (5 x 20) `7561f3ce-7be1-4bdd-a954-772a3cac1b22` (100) · Preview C: Glassdoor lookup, full settings (25) `57b416c5-a780-42d7-bfdb-e00f9cf77c4a` (29) · Preview C (scored): Glassdoor lookup, 25 companies `2a4e6b5b-3bb2-4a0e-9ca5-d2e399e57869` (25, webhook-loaded from `2026-11-17-preview-lookup.csv`, passing companies first) · 2 Glassdoor company profiles `55c0230b-f042-47c2-927a-243594553677` (29,489, webhook table with readable field columns, loaded 2026-11-17 from `2026-11-17-glassdoor-profiles.csv` by `push_profiles_to_gtm.py`; passing companies first, then high > medium > low > none, then most reviews). Funnel tables 1–4 not built yet. | none yet (no tracking_clients campaign created; link when one exists) |

Webhook URLs are not stored in the repo. Get them from `gtm_sheet_get_table`. A webhook load appends rows, so re-running it duplicates them.

## Campaign docs

| Date | Doc | tracking_clients id | Status |
|---|---|---|---|
| 2026-11-12 (v4 2026-11-20) | [`campaign-docs/2026-11-20-doc-1-v4.md`](campaign-docs/2026-11-20-doc-1-v4.md) (current): **5 campaigns**: Glassdoor reputation 1 to 3, Casual Connections 4, buy-and-build health and care 5. Earlier: [v3](campaign-docs/2026-11-18-doc-1-v3.md) (10 campaigns, as sent 2026-11-18), [v2](campaign-docs/2026-11-18-doc-1-v2.md), [v1](campaign-docs/2026-11-12-doc-1.md) | `fed8e905-ea1c-4a91-ade7-0da0f7f732a6` | `client_review`, shared (v3 sent 2026-11-18 12:48 UTC; v4 pushed 2026-11-20 14:51 UTC by replace_markdown, **not re-sent**; 0 open changes, 0 comments; [portal](https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=fed8e905-ea1c-4a91-ade7-0da0f7f732a6)) |
| 2026-11-20 | [`campaign-docs/2026-11-20-doc-2-v1.md`](campaign-docs/2026-11-20-doc-2-v1.md): **Doc 2**, 5 campaigns moved from doc 1 v3 (6 to 10): retail and hospitality people costs 1, manufacturing GPG 2, financial services GPG 3, PE investment 4, new in seat 5 | `712423f3-4f68-496b-b969-248c5b7ce681` | `draft`, hidden from the client, **not sent** |
| 2026-11-18 | [`campaign-docs/2026-11-18-doc-1-campaign-4-casual-connections.md`](campaign-docs/2026-11-18-doc-1-campaign-4-casual-connections.md): draft replacement for doc 1's Campaign 4 (Casual Connections, Bristol), **not applied** | `fed8e905-ea1c-4a91-ade7-0da0f7f732a6` (target) | waiting for another session's doc 1 edits to finish (Moe) |
| 2026-11-18 | [`campaign-docs/2026-11-18-casual-connections-plan.md`](campaign-docs/2026-11-18-casual-connections-plan.md): internal Casual Connections plan v0 (senders, capacity, wave 1, draft copy, questions), not a campaign doc | `-` (not in tracking_clients) | internal draft for Moe, nothing built |
| 2026-11-16 | [`campaign-docs/2026-11-16-mql-concepts-discussion.md`](campaign-docs/2026-11-16-mql-concepts-discussion.md): internal discussion of 5 MQL (reply-first) concepts, not a campaign doc | `-` (not in tracking_clients) | internal discussion, nothing built or sent |

## Sourced data in this repo

- `sourcing/tam/2026-11-18-casual-connections-tam.query.md`: TAM read for Casual Connections wave 1 (312 Bristol-HQ companies, 0.95 C-suite per company measured). No new pull: it reuses the 2026-11-17 Blitz company pulls and the 2026-11-18 preview. Config `-` (UUID `-`).
- `sourcing/casual-connections/2026-11-18-preview-leads.csv`: **45 rows, 19 `preview`** (26 removed with reasons), keyed by `linkedin_url`. A 20-company preview of Bristol-HQ TAM companies for the **Casual Connections** campaign, config `-` (no tracking_clients config, UUID `-`). From Blitz API `POST /v2/search/waterfall-icp-keyword` (30 records kept) and the Clay MCP `search-contacts` (20 rows), pulled 2026-11-18. Raw `2026-11-18-preview-waterfall-raw.jsonl`, `-blitz-raw.csv`, `-clay-raw.json`, `-combined-raw.csv`; query `2026-11-18-preview.query.md`; scripts `preview_leads.py`, `build_preview.py`.
- `sourcing/glassdoor-bad-reviews/2026-11-17-glassdoor-profiles.csv`: **29,489 rows**, one per lookup-input company, scored with `select_and_score.py` rule v2. Match confidence: high 2,264, medium 10,007, low 2,546, none 14,672. **1,796 pass Moe's profile bar** (1,384 high confidence, 412 low). Glassdoor bad-review campaign, config `-` (no tracking_clients config, UUID `-`). From Apify `kaix/glassdoor-company-scraper` via the Apify REST API (60 runs, run ids and costs in `2026-11-17-glassdoor-lookup-runs.json`), pulled 2026-11-17, **$2.80**. Query record `2026-11-17-glassdoor-profiles.query.md`.
- `sourcing/glassdoor-bad-reviews/2026-11-17-glassdoor-profiles-raw-b1..b6.jsonl.gz`: the raw actor output behind that CSV, one file per input batch (7,429 / 6,347 / 5,220 / 3,960 / 3,043 / 1,994 = 27,993 employer profiles). Same tool, config `-`, and date. Assembled by `run_lookup.py assemble`.
- `sourcing/glassdoor-bad-reviews/2026-11-17-2-companies.csv`: 22,627 UK-HQ companies with **51–200** employees in doc 1's five sectors; 22,570 `icp`, 15 excluded as DNC, 42 as Campaign 6; 319 ICP rows flagged `public_sector`. Glassdoor bad-review campaign, config `-`. Blitz API `POST /v2/search/companies` (22,627 records), pulled 2026-11-17 with `pull_companies.py 2026-11-17 51-200 -2`; raw `2026-11-17-2-companies-blitz-raw.jsonl.gz`.
- `sourcing/glassdoor-bad-reviews/2026-11-17-glassdoor-lookup-input.csv` (from `build_lookup_input.py`): the **29,489-company** stage-2 lookup list: private-sector ICP, 51–5,000 staff (Moe's floor and ceiling), deduped by domain and company LinkedIn, largest first, in 6 batches of 5,000.
- `sourcing/glassdoor-bad-reviews/2026-11-17-preview-lookup-raw.json` / `.csv` with `select_and_score.py`: 25-company preview of the stage-2 Glassdoor lookup at full-run settings (29 employer profiles with ratings; 9 usable, 6 pass Moe's bar). `kaix/glassdoor-company-scraper` via GTM Sheets, ≈$0.006. Glassdoor bad-review campaign, config `-`, pulled 2026-11-17. Method in `2026-11-17-test.query.md` (Preview 2).
- `sourcing/glassdoor-bad-reviews/2026-11-17-test-*` (query `2026-11-17-test.query.md`, script `test_scores.py`): the 5-company Glassdoor preview. 12 employer lookups (`kaix/glassdoor-company-scraper`) and 100 reviews (`kaix/glassdoor-reviews-scraper`) via GTM Sheets `gtm_sheet_apify_run`, with a per-company score file. Glassdoor bad-review campaign, config `-`, pulled 2026-11-17. About $0.01 of Apify.
- `sourcing/glassdoor-bad-reviews/2026-11-17-companies.csv`: 11,854 UK-HQ companies, 201+ employees, in doc 1's five sectors; 11,714 `icp`, 58 excluded as DNC, 82 excluded as Campaign 6; 695 ICP rows flagged `public_sector`. **Glassdoor bad-review campaign** (stage 1 of its funnel; no tracking_clients config or campaign yet, UUID `-`). From Blitz API `POST /v2/search/companies` (11,854 records), pulled 2026-11-17. Raw responses `2026-11-17-companies-blitz-raw.jsonl.gz`; query and method `2026-11-17-companies.query.md` (scripts `gd_counts.py`, `pull_companies.py`, `build_companies.py`).
- `sourcing/tam/2026-11-13-signal-read.query.md` with `gpg_signal.py` and `2026-11-13-gpg-signal-companies.csv`: 3,796 employers (250+ staff) in the five doc-1 sectors from the gov.uk gender pay gap 2025 data, with a `gpg_signal_15pct` flag. This backs campaigns 3–5's new signal, pulled 2026-11-13. No config yet (config UUID `-`). Cost £0.
- `sourcing/pe-investment-triggers/2026-11-16-pe-deal-news.csv`: 1,119 UK PE deal articles published since 2026-08-18, each kept or dropped with a reason. **Campaign 6, Fresh Investment** (doc `fed8e905-…`; no config yet, UUID `-`). From the Exa API `POST /search` (news) with structured summaries. Pulled 2026-11-16.
- `sourcing/pe-investment-triggers/2026-11-16-companies-qualified.csv`: 280 candidate companies, 112 qualified (Exa `/contents` check plus `2026-11-16-manual-review.csv`), with leads found per company. Campaign 6, config `-`, pulled 2026-11-16. The pre-qualification list is `2026-11-16-companies.csv` (273).
- `sourcing/pe-investment-triggers/2026-11-16-3-leads.csv`: 491 prospects keyed by `linkedin_url` (439 launch set; 65 companies at 5+). Adds 5 companies after the deal window was loosened to 12 months. From Blitz API `POST /v2/search/waterfall-icp-keyword` (19 records). Campaign 6, config PE investment triggers lead list `71717207-0948-4eb9-898a-ef086122741d` (created after the pull, 2026-11-16), pulled 2026-11-16. This is the current snapshot loaded in GTM Sheets.
- `sourcing/pe-investment-triggers/2026-11-16-2-leads.csv`: 472 prospects keyed by `linkedin_url` (421 launch set, 51 removed with reasons; 63 companies with 5+). Expansion pass on Moe's ask for at least 5 per company. From Blitz API `POST /v2/search/waterfall-icp-keyword` (451 records). Campaign 6, config `-`, pulled 2026-11-16. Supersedes the first pull for loading into GTM Sheets.
- `sourcing/pe-investment-triggers/2026-11-16-leads.csv`: 149 prospects keyed by `linkedin_url` (117 launch set, 32 removed with reasons). From Blitz API `POST /v2/search/waterfall-icp-keyword` (149 records). Campaign 6, config `-`, pulled 2026-11-16. Query and method: `2026-11-16-leads.query.md`. Full pulls wait until the client approves doc 1.
- `sourcing/tam/2026-11-12-tam-read.query.md` with `tam_counts.py`/`tam_counts.json` (Blitz API `POST /v2/search/companies` + `POST /v2/jobs/search`, count-only, `max_results: 1`), `tam_samples.py`/`tam_samples.json` (Blitz `POST /v2/jobs/search`, 25 most recent postings per segment), and `2026-11-12-clay-sample-seg4.json` (Clay MCP `search-companies`, 20 rows). This is the TAM/SAM read for doc 1's five open-role segments, pulled 2026-11-12. No config exists yet (config UUID `-`). 145 Blitz records used.

## History

- **2026-11-23**: **Build order set by Moe.** Doc 1 **Campaigns 1 to 3** (Employer Reputation: CEO/MD, people leaders, TA leaders) are to be built in tracking_clients, GTM Sheets and HeyReach now. Handed to session_013MzxQfbTXPU4XS6uuyCtrr with a full brief (preview first; no HeyReach push or start without Moe's go; nothing sent to the client; built before John's approval on Moe's call, as with Campaign 6). **Casual Connections (Doc 1 Campaign 4) is on hold** until the client gives two things: approval of the campaign, and the link connecting John's and Eoin's LinkedIn accounts to HeyReach 172307 (neither account is in the workspace yet). (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-20**: **Doc 1 split into two docs (Moe: "Keep the first 5 in the doc 1 and move the rest to another document. Keep all the context in both", then "Don't send anything to the client").**
  - **Doc 1** `fed8e905-…` v4 (`campaign-docs/2026-11-20-doc-1-v4.md`) keeps v3's Campaigns 1 to 5 unchanged: Glassdoor reputation 1 to 3, Casual Connections 4, buy-and-build health and care 5. Pushed with `update_campaign_doc` `replace_markdown` (confirm) after re-checking it had 0 comments and 0 changes. Still `client_review` and shared, since v3 was sent on 2026-11-18, so John sees v4 if he opens the portal. **It was not re-sent and no Slack notification went out.**
  - **Doc 2** `712423f3-4f68-496b-b969-248c5b7ce681` "Doc 2 (Nov 20, 2026)" (`campaign-docs/2026-11-20-doc-2-v1.md`), created with `create_campaign_doc` as `draft`, `shared_with_client: false`, **not sent**. It holds v3's Campaigns 6 to 10, renumbered 1 to 5, with the copy unchanged.
  - **Context kept in both:** the intro, "Across every campaign", "Before launch" and all nine offers. Cross-references were reworded to point between the docs (for example "Doc 1's Campaigns 1 to 3", and the gender pay gap note naming Doc 2's Campaigns 2 and 3). The split was scripted with an exact-match check on every replacement: `campaign-docs/scripts/2026-11-20-split-doc-1.py`.
  - **Gap to fix before Doc 2 goes out:** its five campaigns (like v3's 5 to 10) have no `### Signal and data` section; the signal sits inside `### ICP`. The doc standard requires that section with measured counts. Doc 1's Campaign 5 has the same gap.
  - (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-18**: **Doc 1 v3 sent to the client (status change: re-sent, `client_review`).**
  - **How:** Moe said "send this to the client". Sent with `send_campaign_doc_to_client` at 12:48 UTC; `notified_client.ok` = true, so the portal link was posted in DNA's Slack.
  - **Note posted with the link:** "We've updated the plan. Campaigns 1 to 3 now lead, using about 1,400 employers whose own staff rate them below average, with a different promise for the CEO, the people leader and the talent lead. Campaign 4 is the new Bristol casual connections campaign from John and Eoin. Please let us know which offers at the end you're happy to make."
  - **Next:** answer John's comments with `review_campaign_doc`, never `replace_markdown`. Every guarantee in Offers 4, 5, 8 and 9 needs his sign-off. (session_013MzxQfS4USBg3GQoTHx9Ai)
- **2026-11-18**: **Doc 1 v3: Casual Connections is Campaign 4, replacing Mergers and New Leadership (Law and Accounting) (Moe: "Replace the 7th").**
  - **Change:** I did it in this session rather than the Casual Connections one, because there's no channel to message that session. Built on v2, re-read first: 0 changes, 0 comments. Pushed with `replace_markdown` (confirm). The live doc has 356 paragraphs, matching the file.
  - **New order:**
    - 1 to 3: Glassdoor reputation (CEO/MD, people leaders, TA).
    - 4: Casual Connections, Bristol. Text verbatim from the CC draft.
    - 5 to 8: sector campaigns (buy-and-build health, retail people costs, manufacturing GPG, FS GPG). Law and accounting has no sector campaign now; it's reached through 1 to 3 (131 firms on the Glassdoor list).
    - 9: PE investment (tracking_clients campaign `6ce9ac82-…` still says "C6").
    - 10: New in the Seat.
  - **Other edits:** intro, offer line, gender pay gap reference (now 7 and 8), the one-campaign-per-company rule, and a new "Campaign 4 senders" Before-launch item (John's and Eoin's LinkedIn must be connected).
  - **Not re-sent.** Repo copy `campaign-docs/2026-11-18-doc-1-v3.md`.
  - **The handoff entry below is now done.** The CC session doesn't need to apply its draft. (session_013MzxQfS4USBg3GQoTHx9Ai)
- **2026-11-18**: **Handoff to the Casual Connections session (session_013MzxQfxb1tFTNdnVAHYrw5): Moe says Casual Connections goes in right after Campaign 3 of doc 1.**
  - Doc 1 is now v2 (`campaign-docs/2026-11-18-doc-1-v2.md`):
    - Glassdoor reputation campaigns 1 to 3, then sector campaigns 4 to 8, PE investment 9, New in the Seat 10.
    - The old "Campaign 4" (Mergers and New Leadership, Top 100 Law and Accounting) is now **Campaign 7**.
  - **Paragraph numbers in `campaign-docs/2026-11-18-doc-1-campaign-4-casual-connections.md` are stale.**
  - **Tracked suggestions won't work for this:** a `review_campaign_doc` insert can't create headings or new paragraphs. A test landed as raw text inside a bullet, and I rejected it. Moving a campaign into slot 4 means a `replace_markdown` rewrite built on the v2 file. Moe approved that kind of rewrite for the Glassdoor change.
  - **Check with Moe:** whether Casual Connections still replaces Mergers/Law and Accounting (now 7), or is added as an 11th campaign. Then renumber the campaigns after it, and the intro, "Before launch" and offer references. (session_013MzxQfS4USBg3GQoTHx9Ai)
- **2026-11-18**: **Doc 1 rewritten: the three Glassdoor campaigns replace old Campaigns 8, 9 and 10 and move to the top (Moe's call).**
  - **Why:**
    - Old 8 (Reputation and Retention) used the same signal, now measured: 1,384 companies.
    - Old 9 (Growth, M&A, Rebrands) and old 10 (Careers Site Refresh) had unmeasured signals and overlapped other campaigns.
  - **Why a full rewrite:** a `review_campaign_doc` insert can't create headings. A test insert landed as raw text inside a bullet (change 223), and I rejected it at once. So Moe chose a full rewrite (`update_campaign_doc` `replace_markdown`, confirm) over a tracked in-place swap.
  - **What the rewrite did to doc 1:**
    - It accepted all 221 open tracked changes as final.
    - It removed the client's 2 comments, both test text ("XYZ", "sdijada").
    - Status stays `client_review`, shared, **not re-sent**.
  - **New layout:**
    - Campaigns 1 to 3: employer reputation. 1 is CEO/MD (24-month payback, DHU); 2 is people leaders (a quarter off unwanted turnover, MAN/Glendola); 3 is TA leaders at 201+ (half off agency spend, MAN). Each has a `### Signal and data` section.
    - Old 1 to 7 are now 4 to 10.
  - **Offers:**
    - Offer 4's guarantee is now a quarter within 18 months, and Offer 5's payback is now 24 months (conservative numbers from the offer skill).
    - Offers 8 (reputation snapshot) and 9 (half off agency spend in 18 months) are new.
  - **Repo copy:** `campaign-docs/2026-11-18-doc-1-v2.md`, byte-identical to what was pushed. v1 is kept.
  - **Watch:**
    - Old Campaign 6 (PE) is now **Campaign 9**, but tracking_clients campaign `6ce9ac82-…` and its name still say "C6".
    - Casual Connections was also meant to replace a doc 1 campaign; that choice is still open.
    - Contacts per persona for Campaigns 1 to 3 are not yet measured.
    - The draft `campaign-docs/2026-11-18-glassdoor-persona-campaigns.md` is superseded by v2. (session_013MzxQfS4USBg3GQoTHx9Ai)
- **2026-11-18**: **Casual Connections goes into doc 1 as Campaign 4** (Moe: "add in the 4th place"). It replaces "Mergers and New Leadership, Top 100 Law and Accounting Firms".
  - **Not applied yet:** Moe said to wait, because another session is editing doc 1 now.
  - **Ready to apply:**
    - the section draft: `campaign-docs/2026-11-18-doc-1-campaign-4-casual-connections.md`
    - the TAM record, committed first as the doc standard requires: `sourcing/tam/2026-11-18-casual-connections-tam.query.md`
  - **How it will be applied:** as tracked suggestions via `review_campaign_doc`, with paragraph numbers re-read first. As of today they are [107] to [134].
  - **The doc itself was read only** (`get_campaign_doc`): `client_review`, 221 open changes, 2 client comments.
  - **Flag for Moe:** dropping the old Campaign 4 removes the only campaign aimed specifically at the Top 100 law and accounting firms that John's ICP form asked for. Law and accounting firms are still in Campaigns 6 and 9 and in the Casual Connections pool.
  - **The swapped section has no offer by design**, so `## Offers for your feedback` is unchanged.
  - (session_013MzxQfxb1tFTNdnVAHYrw5)

- **2026-11-18**: **Glassdoor campaigns drafted by persona (internal draft for Moe, nothing sent).** Moe asked for three campaigns on the same Glassdoor company list (the 1,384 high-confidence companies that pass the bar in `sourcing/glassdoor-bad-reviews/2026-11-17-glassdoor-profiles.csv`), each with different messaging per persona, in the doc 1 format.
  - **File:** `campaign-docs/2026-11-18-glassdoor-persona-campaigns.md`.
  - **Format:** each campaign has a connection request and 3 messages, as sent to John in doc 1 `fed8e905-…`.
  - **Campaigns:**
    - A: CEO / MD, 24-month payback, DHU proof.
    - B: People leaders, a quarter off unwanted turnover, MAN and Glendola proof.
    - C: TA leaders at 201+ staff (995 companies), half off agency spend, MAN proof.
  - **Free first step:** the 10-day reputation snapshot, in all three.
  - **Offers:** from the `outcome-led-offer-generation` skill (algoacquisition-brain PR #36, run read-only). Its evidence is the ICP form, wearedna.co.uk case studies (MAN: attrition 20% to under 10% and agency spend £600k+ to under £30k, within a year) and the 12 Nov onboarding call (John ranks cost per hire, attrition and story above time to hire).
  - **Every guarantee needs John's sign-off.** Not in doc 1, tracking_clients or HeyReach.
  - **Contacts per persona:** not measured yet.
  - **Open for Moe:** the approval route (doc 1 tracked suggestions or his own), naming Glassdoor, replacing doc 1 campaign 8, and who builds the snapshot. (session_013MzxQfS4USBg3GQoTHx9Ai)
- **2026-11-18**: **Moe's Casual Connections decisions** (in this session, after the preview):
  - **Senders: John Tarrant and Eoin Rodgers**, each with his own signed note. Neither is in HeyReach 172307 yet, so both accounts must be connected before anything sends.
  - **Wave 1: Bristol-HQ companies** (312; about 300 to 350 C-suite contacts).
  - **Approval: through a campaign doc for John.** Moe then said Casual Connections should **replace one of the campaigns in doc 1** (`fed8e905-…`) rather than go in a new doc. This overrides the brief's "don't touch doc 1" for that one change. Doc 1 is `client_review` and shared, with 221 open changes and 2 client comments, so the swap goes in as tracked suggestions via `review_campaign_doc`, never `replace_markdown`. Which campaign gets replaced is still being asked; Campaign 6 is excluded.
  - **Follow-ups: message 1 only** (the thank-you a day after accept, no pitch). The soft-offer message 2 is dropped.
  - Still open: charities and CICs (excluded for now), and the 7-day window (proposed 08:00 to 18:00 Europe/London).
  - (session_013MzxQfxb1tFTNdnVAHYrw5)

- **2026-11-18**: **Casual Connections campaign started (Moe's ask of 2026-11-18): preview only, nothing built.** This opens a **new segment** `sourcing/casual-connections/`. Scope: **Campaign-specific: Casual Connections (founder-led)**.
  - **Skill:** `anthropic-skills:casual-connections-campaign` is not in this session's skills listing, so the work follows CLAUDE.md plus Moe's brief. Moe has been told.
  - **Resync:** no drift (`get_client`, `list_sourcing_configs`, `list_campaigns`, `list_client_accounts`).
  - **Senders, the blocker:**
    - John Tarrant is DNA's **sole founder** (2010) and has been **Founder & Chair** since 21 Jul 2026.
    - **Eoin Rodgers** joined as **MD** in Jul 2026; he is not a founder. Source: wearedna.co.uk team page and the Worldcom press release, via one Exa search ($0.007).
    - HeyReach 172307 holds **only the 10 VA/SDR seats** (`get_campaign_senders` on C6 lists every workspace account; none available or signed out).
    - So **no founder account is connected**, and the campaign can't send until John's LinkedIn is added.
  - **TAM:** the 29,489-company lookup-input list. Bristol HQ 312 companies; South West about 1,354.
  - **Inverse rule:** a large TAM means **1 to 2 C-suite per company** (tier 1 first, plus a second only at 201+ staff). Capacity is about 100 invites a week per founder account, so the list is pulled in waves, not in bulk.
  - **Proposed wave 1:** Bristol HQ, about 300 to 350 contacts.
  - **Preview:**
    - 20 largest Bristol-HQ companies gave 45 rows and **19 usable** C-suite contacts (0.95 per company).
    - **0 overlap** with Campaign 6's lead files; 0 DNC matches.
    - Clay added CPOs and CFOs that Blitz missed.
    - Blitz's fuzzy title match ("Senior People Partner", "Product Owner") is fixed with strict excludes plus a regex.
    - Charities and CICs slipped through the private-sector flag.
  - **Cost:** Blitz 54 records (24 from a discarded first run), Clay MCP 1 search, Exa $0.007.
  - **Draft copy and plan:** `campaign-docs/2026-11-18-casual-connections-plan.md`.
  - **Waiting on Moe:** sender accounts (John only, or John + Eoin, and who connects them), the wave-1 slice, the approval route (campaign doc for John, or Moe's own approval), follow-up depth, charities, and the schedule (proposed 08:00 to 18:00 Europe/London, 7 days).
  - **Not touched:** Campaign 6, doc 1 and the Glassdoor campaign.
  - (session_013MzxQfxb1tFTNdnVAHYrw5)

- **2026-11-17**: **Full Glassdoor company lookup run, scored and loaded to GTM Sheets.** This followed the paused-lookup handoff below. It **expands** the existing `glassdoor-bad-reviews` segment (Campaign-specific: Glassdoor bad-review outreach).
  - **Tool:**
    - Apify `kaix/glassdoor-company-scraper` via the REST API, using the session token (env `Apify_API_KEY`, not `APIFY_API_TOKEN` as briefed).
    - Settings were Moe's: maxSearchResults 3, full ratings, every other include off.
  - **Price and runs:**
    - The live price was $0.0001 per profile, lower than the $0.0002 assumed.
    - The actor takes about 7 s per query, so the job ran as 60 runs: a 50-row smoke test (`qpVI8dpA69sxnflfc`, shape matched the preview) plus 59 runs of 500 queries.
    - Each run had a $0.16 `maxTotalChargeUsd` cap, for a $9.45 worst case against the $10 hard cap. All 60 runs SUCCEEDED.
    - **Actual spend: $2.7987** (Apify `usageTotalUsd`). All run ids are in `sourcing/glassdoor-bad-reviews/2026-11-17-glassdoor-lookup-runs.json` and the `.query.md`.
  - **Results** (29,489 companies):
    - Match confidence: high 2,264 · medium 10,007 · low 2,546 · none 14,672.
    - **1,796 pass the bar** (1,384 high confidence). By sector: retail and hospitality 705 (560 high), financial services 421 (329), manufacturing and engineering 279 (191), health, care and vet 235 (173), law and accounting 156 (131).
    - By size: 51-200 629, 201-500 459, 501-1000 293, 1001-5000 415.
    - The decline test is `needs reviews` on every row.
  - **GTM Sheets:**
    - Table `55c0230b-f042-47c2-927a-243594553677` was rebuilt as a webhook table, using Preview C (scored) for the layout.
    - 29,489 rows were loaded in 30 POSTs, and the count was verified via `gtm_sheet_get_workbook`.
    - The webhook URL is not committed.
  - **Flagged for Moe:**
    - 372 of the 412 low-confidence passes have a non-UK HQ, so they are probably the wrong company.
    - 575 rows share a Glassdoor employer with another row (131 of them pass). Some are aliases; some are wrong matches, such as Christie's matched to Christies Care.
    - The input has 3 rows with `.` as the search term and 98 duplicate search queries.
    - The size-band counts in the entry below are slightly off. The actual counts are 20,597 / 5,264 / 1,893 / 1,735.
    - Batches 4-6 (small companies) are 53-85% `none`.
  - **Not done, waiting for Moe:** reviews, leads, campaigns, doc 1, HeyReach, Campaign 6.
  - Scripts: `run_lookup.py`, `select_and_score.py` (full-file mode), `push_profiles_to_gtm.py`. (session_013MzxQfS4USBg3GQoTHx9Ai)
- **2026-11-17**: **Full Glassdoor lookup paused for an Apify token (Moe's choice).** `gtm_sheet_apify_run` only takes the company list inline in each call, so 29,489 names would be hand-copied with no check, and GTM table exports need auth this environment lacks. A subagent stopped before submitting anything (**$0 spent**). Moe chose: add `APIFY_API_TOKEN` to the cloud environment, then a **fresh session** runs `kaix/glassdoor-company-scraper` straight from `sourcing/glassdoor-bad-reviews/2026-11-17-glassdoor-lookup-input.csv`, under the $10 cap, writes raw + scored CSVs to the repo, and loads GTM table `55c0230b-…` by webhook.
  - **Next session's settings:** 6 batches as in the input file; `maxSearchResults: 3`, `compactMode: false`, `includeRatings: true`, every other section off; select with `select_and_score.py` rule v2 (UK HQ first, then most reviews); profile bar = overall < 3.5 or culture/leadership < 3.3, 30+ reviews. Cost so far on Apify this campaign ≈ $0.02.
  - **Still open with Moe:** the CLAUDE.md wording for his preview rule; who handles replies; HeyReach window and timezone (7 days required); the review pull for the decline rule and themes; trigger ranking (decline + hiring first?) and fixed vs peer-relative cut-offs.
  - (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-17**: **Glassdoor lookup scope reset by Moe: ICP-form floor (51 staff) with a 5,000-staff ceiling, $10 spend cap** for the company-profile lookup. Moe: "Use the floor from icp form and not what i said and get me the company data for all. have a ceiling". He picked 5,000 staff as the ceiling (dropping 1,183 enterprises over 5,000) and $10 as the total cap.
  - Pulled the 51–200 band from Blitz (22,627 records; **expanding** the new glassdoor-bad-reviews segment). Lookup list after exclusions and dedupe: **29,489 companies** (20,600 at 51–200, 5,256 at 201–500, 1,894 at 501–1,000, 1,734 at 1,001–5,000). Estimated ~$6.85 at $0.0002 per profile.
  - Blitz records this session: 11,869 + 22,627 = **34,496**.
  - **The repo export is blocked:** the GTM Sheets export API needs authentication (401 from the shell), and this environment has no Apify token. So the full raw profiles stay in GTM Sheets for now. Only narrow, filtered scored columns can come back through chat. Asked Moe for a token in the environment's settings; a new session picks it up.
  - (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-17**: **Stage-2 lookup previewed at full-run settings (25 companies, ≈$0.006).** 9 of 25 matched a usable UK employer with 30+ reviews and 6 of those pass Moe's bar; 9 had no Glassdoor candidate. Selection rule changed to v2 (most reviews wins, not domain match) after it picked a 2-review shell for GAIL's. Projection for 4,677 companies: ~1,100 pass on profile alone, lookup ~$1.10. Full lookup **waits for Moe's go** after seeing this preview. (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-17**: **Moe's decisions on the Glassdoor campaign** (in this session, after the 5-company preview):
  - **Bad-review bar (union of two rules):** a company qualifies if (a) its overall Glassdoor rating is < 3.5 with 30+ reviews, OR its last-12-month average is 0.3+ stars below the prior 12 months (15+ reviews in each window); OR (b) its culture & values or senior leadership sub-rating is < 3.3 with 30+ reviews. Complaint themes and "no employer replies to negative reviews" choose the message angle; they don't gate.
  - **Scrape scope:** the **501+ staff** slice of the private-sector ICP pool (5,210 companies; 4,677 after removing duplicate domains, LinkedIn showcase and school pages). Estimated ~$3 lookups + ~$10 reviews at published rates.
  - **Approval route:** the campaign goes **into doc 1** (`fed8e905-…`) as a new campaign for John's approval, with `### Signal and data` and the doc's existing `## Offers for your feedback`.
  - **"sdasdad" deleted** (`delete_campaign`, `5a652828-0cd2-4354-bfe1-7ed4ff8eb1f4`, new system). Checked first: empty sequence, no HeyReach/Smartlead/Instantly link, no doc. It was attached to Campaign 6's lead list `71717207-…` (allocation 1), which is why that config showed `campaign_count: 2`. Campaign 6 and the config are untouched.
  - **Preview first:** per Moe's standing rule, a 25-company preview of the stage-2 lookup at full-run settings (non-compact, ratings only) runs before the 4,677-company lookup.
  - (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-17**: **Moe's standing rule: preview every new process before the full run.** Moe, in this session: "always give a preview of a new process before going full fledged into the run. This is a new process." For this campaign that means the 5-company Glassdoor preview below goes to Moe, and no full lookup or review scrape starts until he has seen it and approved the bar, scope and cap. Proposed for CLAUDE.md as a repo-wide rule (system file, so not edited without Moe's confirmation).

- **2026-11-17**: **Glassdoor 5-company preview run** (the brief's tiny test; spend ≈ $0.01 at the actors' published rates, $1 cap per run).
  - Workbook `933daaa1-121f-4f4f-b47c-1b3e91ae44ac` "UK | Glassdoor Bad Reviews | Moe v1" created in DNA's GTM Sheets folder, not yet linked to a campaign (none exists).
  - Harrods, Coventry Building Society, PZ Cussons, HC-One and Shoosmiths resolved by name to the right Glassdoor employer (UK HQ, most reviews); 7 lookalikes rejected. 20 most recent reviews each.
  - Result: Coventry Building Society 2.6 rating, 55% of recent reviews at ≤2 stars, management/communication the top theme. The other four sit at 3.4–3.6.
  - Learned: name search needs a selection rule; compact mode lacks sub-ratings; 20 reviews can span 6 weeks to 14 months, so trend tests need more per company; reviews are global; reply rates range from 0% to 95%. Details in `sourcing/glassdoor-bad-reviews/2026-11-17-test.query.md`.
  - No Apify key in this environment, so data reaches the repo only through GTM Sheets exports. A subagent did the test export. The full run would need many paged exports, or an Apify token in the environment.
  - Messaging draft v1 for Moe: `campaign-docs/2026-11-17-glassdoor-messaging-draft.md` (themes only, reply-first, no reviewer ever identified).
  - (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-17**: **Glassdoor bad-review campaign: ICP company pool pulled** (Moe's brief of 2026-11-17: scrape Glassdoor reviews for ICP companies with Apify via GTM Sheets, then message the ones with bad reviews about the review themes). This opens a **new segment** (`sourcing/glassdoor-bad-reviews/`). Scope recorded as **Campaign-specific: Glassdoor bad-review outreach**, since the brief defines the campaign.
  - **Pool:** Blitz `POST /v2/search/companies`, UK HQ, 201+ employees, doc 1's five sectors (same industry labels as the doc 1 TAM read). 11,854 companies; 11,714 after DNC (58) and Campaign 6 (82) exclusions; 11,019 private sector. By size: 5,809 at 201-500, 2,090 at 501-1000, 1,937 at 1001-5000, 1,183 at 5001+.
  - **Why 201+:** smaller UK employers rarely have enough Glassdoor reviews to rate. Which bands get scraped is Moe's cost call.
  - **Clay not run** for this pool (MCP pages 20 rows with no total; Blitz slices were exhaustive). Flagged in the `.query.md`; can be added on the scraped slice.
  - **Cost:** 11,869 Blitz records (13.59M fair-usage records remaining). No Apify spend yet.
  - **Apify actor shortlist** (researched from the public Apify store, no runs): reviews `kaix/glassdoor-reviews-scraper` (~$0.05 per 1k reviews, sub-ratings and employer replies, no date filter), backup `zen-studio/glassdoor-scraper` ($0.99 per 1k, date and rating filters, almost no users), fallback `memo23/glassdoor-scraper-ppr` (~$4.75 per 1k, most used). Resolver `kaix/glassdoor-company-scraper` (~$0.20 per 1k companies, name or website search, returns overall rating, review count and sub-ratings, so it doubles as a cheap pre-screen). It doesn't show in GTM Sheets' actor search, so the tiny test will confirm `gtm_sheet_apify_run` accepts it. Glassdoor employer IDs are global: reviews are not UK-only.
  - **Waiting on Moe** before any scraping: bad-review definition, which size bands to scrape and the spend cap, doc route (doc for John or Moe's own approval), "sdasdad".
  - (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-17**: **Resync and branch catch-up** (Moe opened a session for a new Glassdoor bad-review campaign).
  - Merged the default branch `claude/initialize-u03yyd` into this branch (47 commits behind, clean merge) so the current CLAUDE.md rules apply: campaign doc standard, 7-day HeyReach schedule, GTM Sheets standard.
  - **Resync:** no drift beyond the 2026-11-16 resync below (DNC 143, booking link, vaSeatCount 10). Sourcing config `71717207-…` now shows `campaign_count: 2` (Campaign 6 plus "sdasdad").
  - **Second campaign in tracking_clients:** "sdasdad" (`5a652828-0cd2-4354-bfe1-7ed4ff8eb1f4`, status `creation`, step 5, created 2026-11-16 13:19 UTC, no HeyReach id). Looks like test junk; **not deleted**, waiting on Moe.
  - Campaign 6 (`6ce9ac82-…`, HeyReach `735291`) untouched: still `creation`, waiting for Moe's final approval.
  - A parallel session (session_013MzxQhYguH8vDsAXrwvGq7) pushed the DNC copy and the MQL concepts note to this branch while this session was starting; merged, keeping its `context/dnc-list.csv` as committed.
  - (session_013MzxQfnKsdVbThAsX3zi7V)

- **2026-11-16**: **Resync, and MQL campaign discussion opened.**
  - **Resync** (`get_client`, `list_sourcing_configs`, `list_campaign_docs`). Since 2026-11-12, tracking_clients gained:
    - the DNC list (143 companies; copy at `context/dnc-list.csv`)
    - a booking link
    - `infrastructure.vaSeatCount` 10
  - The sourcing config and doc 1 (`client_review`) are unchanged.
  - Campaign 6's 491 leads have 0 exact company-name matches against the DNC list. Domains weren't compared, because the leads CSV has no domain column.
  - **MQL discussion:** Moe asked what a reply-first MQL campaign could look like, to raise reply rates. Five concepts are written up in `campaign-docs/2026-11-16-mql-concepts-discussion.md`. The recommendation is to test the GPG sector benchmark first. Sector benchmarks were computed locally from the GPG CSV (£0).
  - **Nothing was built or sent:** no configs, campaigns, docs, HeyReach changes, client contact or paid sourcing. Campaign 6 was not touched.

- **2026-11-16**: **Campaign 6 staged for launch, not started.** Moe said to set it up in GTM Sheets and go live **without John's (the client's) approval of doc 1**. That is Moe's decision, recorded here. Moe then added: **don't go live without his final approval.** So everything stops before any lead is pushed or the campaign is started.
  - **tracking_clients:**
    - ICP config `23a03003-f8ca-4c13-bee9-05d995a938e4` (segment `48f11ee4-…`, persona `9185c9e9-…`: C-suite, MD, partner, people/finance/ops/commercial/marketing directors).
    - Lead list `71717207-0948-4eb9-898a-ef086122741d` (static). `campaign_split` was set to false (one campaign gets every lead) without asking Moe, because the session was told not to ask further questions; it cannot be changed later.
    - Campaign `6ce9ac82-8714-4a82-a864-5317bb53fc91` "UK | Fresh Investment PE-Backed Growth | C6 | Moe v1", status `creation`. It is linked to doc `fed8e905-…`, and its sequence is the doc's campaign 6 copy (connection note, then 3 DMs at +0/+3/+3 days), passed by `set_campaign_sequence`.
  - **HeyReach (We Are DNA workspace):**
    - Draft campaign `735291` "UK | PE-Backed Growth | C6 | Moe v1" with list `1170661`, linked to the tracking_clients campaign.
    - 10 senders (all signed-in accounts). Withdraw after 25 days.
    - **The connection note has no variables.** HeyReach rejects a note with `{FIRST_NAME}`/`{COMPANY}` because `gtm_sheet_create_heyreach_campaign` can't set a note fallback. The saved note is: "Hi, saw the news about the recent investment, congratulations. We help growing businesses attract and keep the people their plans depend on. Would be good to connect." The doc's personalised note can be put back in the HeyReach UI, with a fallback.
    - Message 1 uses `{FIRST_NAME}`/`{COMPANY}`, with a fallback that has no variables.
  - **GTM Sheets, 3 Leads table:**
    - Added formula columns **Clean First Name** (strips emoji and titles, keeps the first word; Susan Armstrong-Brookes override) and **Clean Company** (drops brackets, " / ..." and Ltd/plc/LLP; 13 named overrides).
    - Added **Push to HeyReach** to campaign 735291: auto-run off, `run_if` Status = "launch set". It maps first name, last name, company and title, plus the custom fields investor and sector.
    - **Nothing has been pushed.** The push guard calls the campaign "LIVE", so the push was held for Moe's go-ahead too.
  - **Remaining before start:**
    - Moe's final approval.
    - Push the 439 launch-set rows and check the HeyReach list count.
    - `start_campaign` (dry run first).
    - Set a UK-hours schedule and daily limits.
    - Load the DNC list. The client's uploaded DNC file is still not in tracking_clients, and no exclusions are applied.
    - Set up reply handling and a booking link.
    - The operator's `campaign_thinking`, if this campaign goes through the approval flow.
  - (session_013MzxQi4mQ4Mn8EAPSoHocN)

- **2026-11-16**: **Campaign 6 deal window loosened to 12 months** (Moe: "loosen deal date"). This **expands an existing segment**.
  - **Why:** the deal date rule was the biggest company-level drop (65 companies). 44 failed nothing else, and 12 of those fall inside 12 months.
  - **Outcome:** 6 rejected on manual review (not PE, out of sector, or a wrong date) and 1 duplicate. **5 added.**
  - **Result:** 115 qualified, 439 launch-set leads, **65 companies at 5+**. 19 Blitz records (campaign total 629).
  - **GTM Sheets:** the Companies and Leads tables were rebuilt, and row counts match (280 / 491).
  - **Doc:** campaign 6's trigger now says "last 12 months", as a tracked suggestion.

- **2026-11-16**: **Campaign 6 leads expanded** (Moe: "expand the leads have at least 5 per company"). This **expands an existing segment**.
  - **Pass:** a 4-tier UK Blitz waterfall, up to 6 per company. Director and Partner titles count as just below the C-suite. Functional heads are used only as flagged top-ups where a company is short.
  - **Result:** 472 leads, 421 launch set. **63 of 110 qualified companies have 5+.** 14 still have none: no confident LinkedIn page, or no UK leaders in Blitz.
  - **Cost:** 451 Blitz records (campaign 6 total 610), plus about $0.05 Exa to correct 4 wrong LinkedIn pages.
  - **GTM Sheets:** the Companies and Leads tables were rebuilt from the new snapshot. Row counts match (280 / 472).
  - **Details:** `sourcing/pe-investment-triggers/2026-11-16-leads.query.md`.

- **2026-11-16**: **Campaign 6 (Fresh Investment, PE-Backed Growth) built in GTM Sheets.** This opens a **new segment**: a trigger across all five sectors.
  - **Why this one:** Moe asked which campaign was safest to launch first. I recommended 6, because it's the client's own ICP-form signal, has no pay gap or client-name risk, and goes to C-suite only. Moe then said "Build campaign 6 in gtm sheets".
  - **Pipeline:**
    - Exa news search found 1,119 UK deal articles since 2026-08-18.
    - These reduce to 273 companies, then 112 qualified after the Exa article check and manual review.
    - Blitz waterfall returned 149 UK leads at 67 companies, max 3 per company (small trigger pool, so the inverse rule gives 3).
    - 117 leads are launch set and 32 are marked removed with reasons.
  - **Workbook:** `851f8ca4-…` with three tables. Row counts match the CSVs (1,119 / 280 / 149).
  - **Cost:** Blitz 159 records, Exa about $4.35.
  - **Tooling problems found:**
    - The GTM Sheets AI web access is out of credits.
    - The GTM Sheets `blitz_waterfall_icp` column sends `countries` as a string, and Blitz rejects it.
    - Both steps were run from the repo instead.
  - **Not done, by rule:** no tracking_clients config or campaign, no HeyReach push. Doc 1 is still in `client_review`, unapproved, and there is no DNC or client list yet. The gates are listed in `sourcing/pe-investment-triggers/2026-11-16-leads.query.md`.

- **2026-11-13**: **Campaigns 6–10 aligned with John's feedback, then doc re-sent.**
  - **Edits:** 14 more tracked suggestions via `review_campaign_doc`, all ok, client comments 1 and 2 kept.
    - Personas moved up to CEO/MD and CPO/People Director/HRD. All Head of TA and Employer Brand Manager tiers removed.
    - Campaign 7 now covers a new CEO or people leader.
    - Campaign 8's signal is now ratings, or turnover disclosed in results or press. The "reposted roles" wording is gone.
    - Campaign 6's "hiring plan" and "hiring push" wording removed.
    - Campaign 10 now targets the people leader plus the CMO.
  - **Send:** after Moe said "Send it back", re-sent via `send_campaign_doc_to_client` with a note. Status **client_review**, Slack notified (`ok`).
  - **Email:** Moe asked for a reply to John's email. The draft is at `comms/2026-11-13-reply-to-john-open-roles.md`. It was not sent from this session.
  - **Pending:** Moe's choice of the 3 campaigns to launch first. My recommendation is 1, 2 and 5, which was put to Moe but the question was interrupted.

- **2026-11-13**: **Campaigns 1–5 re-signalled after client feedback.**
  - **Feedback:** on 2026-11-12, John Tarrant emailed that leading with an open role makes DNA look like a "low end high street recruiter", and that they sell to the C-suite and the level just below, who don't track open roles.
  - **Moe's call:** replace the signals, keep the five sectors ("proceed with the 5 sector mapping"):
    1. Buy-and-build groups (health, care, vet, dental)
    2. People costs or turnover named in results, or a customer rebrand (retail and hospitality)
    3. Gender pay gap of 15% or more (manufacturing)
    4. Mergers, PE deals and new managing partners (Top 100 law and accounting)
    5. Gender pay gap and Women in Finance Charter (financial services)
  - **Personas:** moved to CEO/MD, CPO/HRD/People Director, COO and Managing Partner. Messages no longer mention roles or candidates. Campaigns 3 and 5 quote the company's own pay gap figure (`{gap}`).
  - **Applied** through `review_campaign_doc`: 95 tracked suggestions, all ok. The client's 2 comments are kept. Status remains `internal_review` and the doc has **not** been re-sent.
  - **Also updated:** open-role references in 6, 8, 9, 10 and "Before launch".
  - **Still pending (6–10 pass):** move the 6–10 personas up a level; campaign 8's signal still mentions "roles reposted repeatedly"; campaign 7 should be a new CEO as well as a new people leader.
  - **Data:** see `sourcing/tam/2026-11-13-signal-read.query.md`.

- **2026-11-12**: Doc 1 updated and **sent to the client**, both at Moe's request in this session.
  - **Update:** Moe asked for 5–7 offers at the end of the doc for the client to comment on, some with money, time or money-back claims. I added an "Offers for your feedback" section with 7 offers:
    1. AI visibility audit (the default offer in the messages)
    2. Agency spend review (£500k+/yr, Superdry/boohoo/Pets at Home)
    3. £1m business-case workshop (MAN)
    4. Turnover cut by up to 50% in 12 months, with a guarantee option (Glendola)
    5. Pays for itself in 20 months or money back (DHU)
    6. Careers site audit with a 90-day uplift
    7. Competitor comparison
  - Every figure comes from the client's own ICP form results. The guarantees are framed as proposals for the client to accept or reject.
  - **How it was pushed:** `update_campaign_doc` `replace_markdown` (confirm), safe because the doc had 0 comments and 0 suggestions.
  - **Send:** after Moe said "send it to the client", called `send_campaign_doc_to_client`, which set status **client_review** and `shared_with_client: true`. The Slack notification went out (`notified_client.ok: true`) with a note asking for thoughts on the offers.
  - **Next:** when the client comments (status `internal_review`), respond with `review_campaign_doc`, not `replace_markdown`.

- **2026-11-12**: Campaign doc 1 created in tracking_clients with `create_campaign_doc`: doc `fed8e905-ea1c-4a91-ade7-0da0f7f732a6` ("Nov 12, 2026"), status **draft**, `shared_with_client: false`. The repo copy is `campaign-docs/2026-11-12-doc-1.md`.
  - **Contents:** 10 campaigns. Campaigns 1–5 are open-role MPC, one per approved segment: SOP connection note, then +2/+2/+2 messages, AI visibility audit CTA, and a sector proof point each. Campaigns 6–10 are the approved triggers. UK English, no em or en dashes, every connection note ≤166 chars.
  - **Not sent:** `send_campaign_doc_to_client` waits for Moe's explicit "send" in-session.
  - **Variables needed at build:** `{first_name}`, `{company}`, `{open_role}` (1–5); `{industry}` (8 and 10). Campaigns 1–5 don't use the SOP's `{JD}`/`JD Phrase`, because message 1 is about the hiring load, not a candidate fit.
  - **Note:** the MCP stamped `created_by: mcp:dave@algoacquisition.com`, which is the MCP key's identity, not this session's user.

- **2026-11-12**: TAM/SAM read for doc 1 (`sourcing/tam/2026-11-12-tam-read.query.md`), using Blitz counts and samples plus a Clay fit check, with no full pulls (145 Blitz records). This opens 5 **new segments**:
  - Health & Care, Retail & Hospitality, Manufacturing/Engineering, and Financial Services: about 1,000–3,000 UK companies each are hiring for hook roles in any 90 days. The pools are large, so **2 contacts per company**.
  - Top 100 Law & Accounting: about 200 firms. The pool is small, so **3 per company**.
  - Flags: Medivet and Dunbia appear in the pool and are named in the client's own "client matching" list. Treat them as exclusions until the client confirms. NHS trusts and government bodies are excluded from MPC by default.
- **2026-11-12**: Moe's decisions for doc 1, given in this session (so nobody needs to re-ask):
  - **Framing:** the MPC SOP is adapted for a non-recruiter. The open role is the *signal* of a talent-attraction problem, the persona is the TA/People leader, and volume or hard-to-fill roles are the hook. SOP mechanics are unchanged.
  - **Segments 1–5:** Health, Care & Medical / Retail & Hospitality / Manufacturing, Engineering, Automotive & Defence / Top 100 Law & Accounting / Financial Services, all UK. Technology, construction/property and renewables are held for doc 2.
  - **Campaigns 6–10:** trigger-based: PE investment / new people leader / employer-reputation pain / growth, M&A or rebrand / weak careers site.
  - **Offer:** the AI visibility audit, across all 10 campaigns.

- **2026-11-12**: Folder created from `clients/_TEMPLATE/README.md`. Profile synced from `tracking_clients`, and the brief, ICP form, description and caller notes were saved to `context/`. tracking_clients has no ICP configs, sourcing configs, campaigns or campaign docs yet. Started because Moe opened a per-client session to build We Are DNA's first campaign doc (10 campaigns: 5 open-role MPC segments plus 5 more). Gaps found: the uploaded DNC file was never loaded, no HeyReach connector serves 172307, the billing currency isn't recorded, and no GTM engineer is assigned. (session_013MzxQi4mQ4Mn8EAPSoHocN)
