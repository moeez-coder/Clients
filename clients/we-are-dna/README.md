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
| 2026-11-12 | [`campaign-docs/2026-11-12-doc-1.md`](campaign-docs/2026-11-12-doc-1.md): 10 campaigns (5 open-role MPC + 5 trigger) | `fed8e905-ea1c-4a91-ade7-0da0f7f732a6` | `client_review` (sent 2026-11-12; [portal](https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=fed8e905-ea1c-4a91-ade7-0da0f7f732a6)) |

## Sourced data in this repo

- No company or lead snapshots yet. Full pulls wait until the client approves doc 1.
- `sourcing/tam/2026-11-12-tam-read.query.md` with `tam_counts.py`/`tam_counts.json` (Blitz API `POST /v2/search/companies` + `POST /v2/jobs/search`, count-only, `max_results: 1`), `tam_samples.py`/`tam_samples.json` (Blitz `POST /v2/jobs/search`, 25 most recent postings per segment), and `2026-11-12-clay-sample-seg4.json` (Clay MCP `search-companies`, 20 rows). This is the TAM/SAM read for doc 1's five open-role segments, pulled 2026-11-12. No config exists yet (config UUID `-`). 145 Blitz records used.

## History

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
