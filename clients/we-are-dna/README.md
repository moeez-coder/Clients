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
- **Last synced:** 2026-11-17 via `get_client` + `list_sourcing_configs` + `list_campaigns` + `list_campaign_docs` (doc 1 still `client_review`, 2 open comments, 221 open changes; no change since 2026-11-16)

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

Webhook URLs are not stored in the repo. Get them from `gtm_sheet_get_table`. A webhook load appends rows, so re-running it duplicates them.

## Campaign docs

| Date | Doc | tracking_clients id | Status |
|---|---|---|---|
| 2026-11-12 | [`campaign-docs/2026-11-12-doc-1.md`](campaign-docs/2026-11-12-doc-1.md): 10 campaigns (5 open-role MPC + 5 trigger) | `fed8e905-ea1c-4a91-ade7-0da0f7f732a6` | `client_review` (re-sent 2026-11-13 after John's open-role feedback; 221 open suggested changes and 2 open comments as of 2026-11-17, pending the client's accept/reject; [portal](https://dashboard.algoacquisition.ai/#/portal/campaigns?doc=fed8e905-ea1c-4a91-ade7-0da0f7f732a6)) |
| 2026-11-16 | [`campaign-docs/2026-11-16-mql-concepts-discussion.md`](campaign-docs/2026-11-16-mql-concepts-discussion.md): internal discussion of 5 MQL (reply-first) concepts, not a campaign doc | `-` (not in tracking_clients) | internal discussion, nothing built or sent |

## Sourced data in this repo

- `sourcing/glassdoor-bad-reviews/2026-11-17-companies.csv`: 11,854 UK-HQ companies, 201+ employees, in doc 1's five sectors; 11,714 `icp`, 58 excluded as DNC, 82 excluded as Campaign 6; 695 ICP rows flagged `public_sector`. **Glassdoor bad-review campaign** (stage 1 of its funnel; no tracking_clients config or campaign yet, UUID `-`). From Blitz API `POST /v2/search/companies` (11,854 records), pulled 2026-11-17. Raw responses `2026-11-17-companies-blitz-raw.jsonl.gz`; query and method `2026-11-17-companies.query.md` (scripts `gd_counts.py`, `pull_companies.py`, `build_companies.py`).
- `sourcing/tam/2026-11-13-signal-read.query.md` with `gpg_signal.py` and `2026-11-13-gpg-signal-companies.csv`: 3,796 employers (250+ staff) in the five doc-1 sectors from the gov.uk gender pay gap 2025 data, with a `gpg_signal_15pct` flag. This backs campaigns 3–5's new signal, pulled 2026-11-13. No config yet (config UUID `-`). Cost £0.
- `sourcing/pe-investment-triggers/2026-11-16-pe-deal-news.csv`: 1,119 UK PE deal articles published since 2026-08-18, each kept or dropped with a reason. **Campaign 6, Fresh Investment** (doc `fed8e905-…`; no config yet, UUID `-`). From the Exa API `POST /search` (news) with structured summaries. Pulled 2026-11-16.
- `sourcing/pe-investment-triggers/2026-11-16-companies-qualified.csv`: 280 candidate companies, 112 qualified (Exa `/contents` check plus `2026-11-16-manual-review.csv`), with leads found per company. Campaign 6, config `-`, pulled 2026-11-16. The pre-qualification list is `2026-11-16-companies.csv` (273).
- `sourcing/pe-investment-triggers/2026-11-16-3-leads.csv`: 491 prospects keyed by `linkedin_url` (439 launch set; 65 companies at 5+). Adds 5 companies after the deal window was loosened to 12 months. From Blitz API `POST /v2/search/waterfall-icp-keyword` (19 records). Campaign 6, config PE investment triggers lead list `71717207-0948-4eb9-898a-ef086122741d` (created after the pull, 2026-11-16), pulled 2026-11-16. This is the current snapshot loaded in GTM Sheets.
- `sourcing/pe-investment-triggers/2026-11-16-2-leads.csv`: 472 prospects keyed by `linkedin_url` (421 launch set, 51 removed with reasons; 63 companies with 5+). Expansion pass on Moe's ask for at least 5 per company. From Blitz API `POST /v2/search/waterfall-icp-keyword` (451 records). Campaign 6, config `-`, pulled 2026-11-16. Supersedes the first pull for loading into GTM Sheets.
- `sourcing/pe-investment-triggers/2026-11-16-leads.csv`: 149 prospects keyed by `linkedin_url` (117 launch set, 32 removed with reasons). From Blitz API `POST /v2/search/waterfall-icp-keyword` (149 records). Campaign 6, config `-`, pulled 2026-11-16. Query and method: `2026-11-16-leads.query.md`. Full pulls wait until the client approves doc 1.
- `sourcing/tam/2026-11-12-tam-read.query.md` with `tam_counts.py`/`tam_counts.json` (Blitz API `POST /v2/search/companies` + `POST /v2/jobs/search`, count-only, `max_results: 1`), `tam_samples.py`/`tam_samples.json` (Blitz `POST /v2/jobs/search`, 25 most recent postings per segment), and `2026-11-12-clay-sample-seg4.json` (Clay MCP `search-companies`, 20 rows). This is the TAM/SAM read for doc 1's five open-role segments, pulled 2026-11-12. No config exists yet (config UUID `-`). 145 Blitz records used.

## History

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
