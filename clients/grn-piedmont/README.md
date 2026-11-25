# GRN Piedmont

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** https://grnpiedmont.com
- **Contact:** Harvey Eden <heden@grnpiedmont.com> (also Chris Missler, cmissler@grnpiedmont.com)
- **Slack channel ID:** C0CF3JM25EC
- **Tracking client ID:** `3abc2243-889c-4177-a75a-3ac680766d20`
- **HeyReach workspace ID:** 172413 (connected)
- **Booking link:** https://calendly.com/grnpiedmont/introductory-business-conversation
- **DNC:** 8 rows in tracking_clients (6 companies after the 2 header rows), copied to `context/dnc-list.csv`
- **Last synced:** 2026-11-24 via `get_client` + `list_sourcing_configs` (HeyReach state via the GRN Piedmont connector); campaigns and doc last synced 2026-11-16

Context copied from `get_client` on 2026-11-16: `context/client-brief.md`, `context/icp-form.md`, `context/client-description.md`, `context/caller-briefing.md`, `context/caller-faqs.md`.

## Sourcing configs

| Config | ICP | Market | Scope | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|---|
| Fire & Life Safety Leaders - Blitz (US F&LS 201-1000, C-level/VP) | Fire & Life Safety Leaders | US fire & life safety companies: fire sprinkler and suppression contractors, fire alarm and detection integrators, inspection, testing and maintenance providers | Campaign-specific: Fire & Life Safety Leaders (not set by this session; inferred from the config name, confirm) | draft | 1 | 0 | - |
| Owner Succession - Blitz (US manufacturers 201-1000, owners/CEOs) | Owner Succession | Founder-led or family-owned US manufacturers (industrial, discrete and process) | Campaign-specific: Owner Succession (not set by this session; inferred from the config name, confirm) | draft | 1 | 0 | - |
| Recruitment Specific Open Roles - Blitz jobs search (US mfg + F&LS 201-1000, last 120 days) | Recruitment Specific \| Open Roles | US mid-sized manufacturers and fire & life safety companies with an open leadership or specialist management role | Campaign-specific: Recruitment Specific Campaign | draft | 1 | 0 (leads live in GTM Sheets and HeyReach; not ingested) | - |
| MPC Executive - Blitz jobs search (US mfg 201-1000, last 120 days) | Recruiter \| MPC \| Executive | US mid-sized manufacturers with an open executive role | Campaign-specific: US \| Recruiter \| MPC Executive (set by this session, 2026-11-24) | draft | 1 | 0 (leads live in the repo, GTM Sheets and HeyReach; not ingested) | - |
| MPC Operations & Plant - Blitz jobs search (US mfg 201-1000, last 120 days) | Recruiter \| MPC \| Operations & Plant | US mid-sized manufacturers with an open plant or operations leadership role | Campaign-specific: US \| Recruiter \| MPC Operations & Plant (set by this session, 2026-11-24) | draft | 1 | 0 (leads live in the repo, GTM Sheets and HeyReach; not ingested) | - |
| MPC Engineering & Quality - Blitz jobs search (US mfg 201-1000, last 120 days) | Recruiter \| MPC \| Engineering & Quality | US mid-sized manufacturers with an open engineering or quality leadership role | Campaign-specific: US \| Recruiter \| MPC Engineering & Quality (set by this session, 2026-11-24) | draft | 1 | 0 (leads live in the repo, GTM Sheets and HeyReach; not ingested) | - |
| MPC Supply Chain & Purchasing - Blitz jobs search (US mfg 201-1000, last 120 days) | Recruiter \| MPC \| Supply Chain & Purchasing | US mid-sized manufacturers with an open supply chain, purchasing, logistics or planning leadership role | Campaign-specific: US \| Recruiter \| MPC Supply Chain & Purchasing (set by this session, 2026-11-24) | draft | 1 | 0 (leads live in the repo, GTM Sheets and HeyReach; not ingested) | - |
| MPC EHS & Maintenance - Blitz jobs search (US mfg 201-1000, last 120 days) | Recruiter \| MPC \| EHS & Maintenance | US mid-sized manufacturers with an open EHS, safety, maintenance or facilities leadership role | Campaign-specific: US \| Recruiter \| MPC EHS & Maintenance (set by this session, 2026-11-24) | draft | 1 | 0 (leads live in the repo, GTM Sheets and HeyReach; not ingested) | - |

MPC segment config UUIDs (2026-11-24, all `static`, `campaign_split: false` as on the live list, since one list feeds one campaign):

| Segment | ICP config | Segment | Persona | Lead list (config) | tracking_clients campaign |
|---|---|---|---|---|---|
| Executive | `f92e0720-2d1c-4111-bd84-56eb4f07bdca` | `70228bd6-0264-49dc-b7d3-5417d4b40568` | `d6877bb8-ba38-47ef-a89d-a00d9f96a47b` | `05b28816-06e7-4d7d-9a6d-d9b606f39a68` | `24c67d2e-1f05-45f9-832d-89f3de069502` |
| Operations & Plant | `6082d8b5-887b-4c07-bcba-b1ab14cba5a1` | `77b7c96e-e05d-4707-a213-02a3b9906b7d` | `a871c61d-1711-4a85-8395-3f902ebe1240` | `eeb54cb5-55bf-47ac-b39a-744e747f2609` | `3f5427d0-8ad8-4a01-b04a-af07a55cb817` |
| Engineering & Quality | `197085c0-ac89-43a0-9039-b7f372616693` | `eae02562-d79c-4873-bad1-0297370df230` | `d89be3e0-62f1-4895-ac21-504044b51bff` | `96f04838-dc74-4e52-b109-487f3d7e1688` | `4c7a69fe-ca99-43b5-8ba0-49c3a798f4ad` |
| Supply Chain & Purchasing | `e1a98b56-64e3-4924-a656-860e7e133796` | `906aa9d0-82d4-4e32-b28c-36aacc56b4a0` | `c77d6975-c9dc-4ef0-9661-90e50accd437` | `587aa10e-be86-4618-827c-107e32d25bef` | `b0930608-74ef-4dbb-8d71-e15dbf29fb4d` |
| EHS & Maintenance | `c526196d-cc4f-40f8-b165-4329ab1458d6` | `3b922ddd-1d3b-4818-97ce-f357c6869732` | `427da487-5a53-4bed-a9d5-179eec955f74` | `3007a239-501f-4466-91a4-6944cad264a7` | `208c483d-b704-44d7-9f17-8cca58303d24` |

Config UUIDs: Recruitment Specific Open Roles `fe214099-0834-40b6-9b18-d4517ecd03f1` (ICP config `7cc82211-d388-4996-9bc6-1e0b02fae68e`, segment `e09104c0-8a70-431b-a3fd-8599696c1a56`, persona `f2eb489d-080b-4b70-9394-dd9d12a21ff2`, `campaign_split: false`); Fire & Life Safety Leaders `e8538474-8bd8-4479-8878-5899efe1ccf4`; Owner Succession `88fe680f-eae0-40c5-b147-1edf40579466`.

## Campaigns and campaign docs (tracking_clients, as of 2026-11-16)

| Item | ID | Status |
|---|---|---|
| Campaign doc "GRN Piedmont Campaign Ideas" (Campaigns 1 to 5) | `cae47cc4-0801-44e6-ad15-9a2f0840f766` | client_review, 19 open comment threads |
| Campaign "Fire & Life Safety Leaders" | `f1138ab0-daa4-42a1-8a7c-ca27965623ea` (HeyReach 730732) | creation |
| Campaign "Owner Succession" | `250a7100-07e0-487d-97c0-8a204d97a276` (HeyReach 730731) | creation |

| HeyReach "Recruitment Specific Campaign 2.0" | HeyReach 756466 (list 1211197), wave-2 leads only | **running** since 2026-11-24, 680 wave-2 leads |
| Campaign "Recruitment Specific Campaign" | `ed2f167f-5cea-4b2e-833b-20b2aafe26e0` (HeyReach 734516, lead list 1169425) | **running** since 2026-11-16 08:37 UTC |

Campaign 6 and the offers section were added to the campaign doc on 2026-11-16 as tracked suggestions; the text is in `campaign-docs/2026-11-16-campaign-6-recruitment-specific.md`.

## HeyReach senders and schedules (workspace 172413)

Read 2026-11-24 with the GRN Piedmont HeyReach connector (`get_all_linked_in_accounts`, `get_all_campaigns`, `get_campaign_sequence`). HeyReach has no tool that reads a schedule, so the schedule column only shows what is on record here.

**Sender pool:** 11 accounts. 10 are active with valid sign-in: 182881, 195084, 195243, 195415, 195518, 196127, 203211, 212529, 261055, 278063. **Left out:** 271564 (cmissler17@aol.com, Chris Missler): inactive, sign-in not valid. None of the 11 has Sales Navigator. There is no Open Check campaign in this workspace, so that doesn't block anything.

| HeyReach id | Name | Status | Senders now | Schedule on record | Planned change (Moe's 2026-11-24 batch, **not yet applied**) |
|---|---|---|---|---|---|
| 756466 | Recruitment Specific Campaign 2.0 | IN_PROGRESS | 10 (the full valid pool) | weekdays 07:00-19:00 America/New_York (set 2026-11-23) | senders: none needed; schedule: pause, set 7 days, 07:00-19:00 America/New_York, resume |
| 734516 | Recruitment Specific Campaign | IN_PROGRESS | 7: 182881, 195084, 195243, 195415, 203211, 212529, 195518 | not recorded | pause, senders 7 -> 10 (add 196127, 261055, 278063), set 7 days 08:00-18:00 America/New_York, resume |
| 730732 | US \| Fire & Life Safety Leaders \| GRN Piedmont v1 (doc Campaign 3) | DRAFT | 1: 182881 | not recorded | senders 1 -> 10 (copy speaks as "GRN Piedmont", not one person; the doc allows all accounts for Campaign 3). Schedule left alone: the batch only changes active campaigns |
| 730731 | US \| Owner Succession \| GRN Piedmont v1 (doc Campaign 5) | DRAFT | 1: 182881 | not recorded | **no change, flagged for Moe:** the copy is first person as a senior leader ("a question I ask {ownership} manufacturers"), and the doc says Campaign 5 should send only from Harvey's account. Harvey has no account in this workspace, and 182881 is a managed sender, not Harvey |
| 760469 | US \| Recruiter \| MPC Executive \| Moe v1 (list 1218894) | **IN_PROGRESS since 2026-11-25 11:31 UTC** | 10: the full valid pool | **7 days, 07:00-19:00 America/New_York, set at creation 2026-11-24** (window copied from 756466; Moe decides) | none; leads not pushed yet (needs a start, see History) |
| 760470 | US \| Recruiter \| MPC Ops & Plant \| Moe v1 (list 1218896) | PAUSED (started + paused empty 2026-11-25; goes live on its day, see History) | 10: the full valid pool | **7 days, 07:00-19:00 America/New_York, set at creation 2026-11-24** (window copied from 756466; Moe decides) | none; leads not pushed yet (needs a start, see History) |
| 760471 | US \| Recruiter \| MPC Eng & Quality \| Moe v1 (list 1218897) | PAUSED (started + paused empty 2026-11-25; goes live on its day, see History) | 10: the full valid pool | **7 days, 07:00-19:00 America/New_York, set at creation 2026-11-24** (window copied from 756466; Moe decides) | none; leads not pushed yet (needs a start, see History) |
| 760473 | US \| Recruiter \| MPC Supply Chain \| Moe v1 (list 1218898) | PAUSED (started + paused empty 2026-11-25; goes live on its day, see History) | 10: the full valid pool | **7 days, 07:00-19:00 America/New_York, set at creation 2026-11-24** (window copied from 756466; Moe decides) | none; leads not pushed yet (needs a start, see History) |
| 760475 | US \| Recruiter \| MPC EHS & Maint \| Moe v1 (list 1218899) | PAUSED (started + paused empty 2026-11-25; goes live on its day, see History) | 10: the full valid pool | **7 days, 07:00-19:00 America/New_York, set at creation 2026-11-24** (window copied from 756466; Moe decides) | none; leads not pushed yet (needs a start, see History) |

## GTM Sheets

Workbook **US | Recruiter | Recruitment Specific Open Roles | Moe v1** `4086bd52-c75b-460e-959b-280a5bc93722`, in Clients / GRN Piedmont (folder `5b185300-2443-46b3-9a4d-b50cb54f4368`), linked to campaign `ed2f167f-5cea-4b2e-833b-20b2aafe26e0`.

| Table | ID | Rows | Loaded from |
|---|---|---|---|
| 1 Companies | `370b9f00-8bb2-4a97-975a-87f507a5a5d8` | 1,161 | `2026-11-16-companies.csv` |
| 2 Jobs | `a87d6fbd-ce5c-4023-bc8c-37098f1ccb69` | 4,426 | `2026-11-16-jobs.csv` |
| 3 Leads | `3bfcb40c-0b6d-48e4-8f72-e2105ef426e0` | 1,563 | `2026-11-16-leads.csv` + `2026-11-16-role-phrases-3.csv`; linked to lead list `fe214099-0834-40b6-9b18-d4517ecd03f1`; Push to HeyReach column -> 734516, `run_if` Status = launch set |

| 4 Leads Wave 2 (2.0) | `99a71d70-cb2a-4445-9068-f49d708ccbee` | 699 | `2026-11-23-leads.csv` + phrases; Push to HeyReach 2.0 column -> 756466 |

**MPC segment workbooks (2026-11-24),** one per campaign, all in Clients / GRN Piedmont:
- tracking_clients created the workbooks with the campaigns, already linked. I added the tables.
- Each Leads table is linked to its lead list and has a **Push to HeyReach** column: `auto_run` off, `run_if` Status = launch set plus role, phrase and open line all filled. Custom fields: `Job_Title_Open_`, `Job_Description`, `Company_Name`, `Open_Line`.
- Loaded with `gtm-sheets/load_mpc_segment.py`. Webhook URLs are passed as arguments, not committed.
- Server row counts match the CSVs.

| Workbook | id | 1 Companies | 2 Jobs | 3 Leads | HeyReach |
|---|---|---|---|---|---|
| MPC Executive | `76c64023-3879-45b9-81c1-d43a47b4da18` | `3a3e08bd-8133-44a7-ac75-564fd73425f0` (230) | `77112ae9-05b4-410b-afe4-bd1b5ae62098` (476) | `5f70a475-2dfb-4402-8c03-29700e9068e6` (361) | 760469 |
| MPC Ops & Plant | `5b5178c5-afb7-45e3-8c5d-4710b6f256dd` | `ea352dde-00c4-4898-9c89-dc63d1b40288` (362) | `677ac353-31b0-467b-b5e5-385e65ea345a` (777) | `3f832d3e-865a-4ae5-9fe0-24f2519bf48b` (724) | 760470 |
| MPC Eng & Quality | `3535ae28-d1ce-4a69-bd9a-97c2a9d5158e` | `061419d5-fbb5-4f7b-bf75-f424a486c5f9` (281) | `c465f748-4b84-45e2-8238-67e113f7f0bb` (806) | `703cfddf-5c09-404b-9323-32c32b766407` (593) | 760471 |
| MPC Supply Chain | `11728e44-c543-409f-a5ad-60667593763c` | `186e80b9-c1b4-4429-bafd-b93cd051b802` (177) | `2d541f70-467b-4df4-afb4-b5a43cc40d23` (334) | `200985c4-3abd-40c8-a220-47cdf0e0b4b7` (379) | 760473 |
| MPC EHS & Maint | `cddb05fc-72c8-4767-be2b-b9e5829a764e` | `26d76b99-cd0d-4055-9816-1b99564c0f2b` (206) | `a618c4f6-2dda-4531-8f09-4a622783bb12` (477) | `3f566cc1-5b9f-4de2-b739-7bb8b9b17472` (357) | 760475 |

Apify coverage test workbook `2dc34e83-4191-4b4a-afc4-ede398922778`, table `1a3119fc-23ee-42e3-a466-56c778e5cd3f` (one-off, not a campaign).

Loaded with `gtm-sheets/load_tables.py` (webhook URLs passed as arguments, not committed). `Job Title Open` and `Job Description` are plain data, not an AI column: the GTM Sheets OpenRouter key hit its $1,000 total cap on 2026-11-16, so the phrases were written by Claude sub-agents and saved to the repo.

## Sourced data in this repo

- `sourcing/recruitment-specific-open-roles/2026-11-16-jobs.csv` — 4,426 job postings (3,347 kept, the rest marked removed with a reason) for the **Recruitment Specific Campaign** lead list, Blitz API `POST /v2/jobs/search`, last 120 days, pulled 2026-11-16
- `sourcing/recruitment-specific-open-roles/2026-11-16-companies.csv` — 1,161 companies with a kept posting, one open role each, with a `leads_launch_set` count (246 produced no lead and stay in the file), derived from the jobs pull, 2026-11-16
- `sourcing/recruitment-specific-open-roles/2026-11-16-leads.csv` — 1,563 prospects (1,559 launch set) at 915 companies, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-16, keyed by `linkedin_url`. Query record: `2026-11-16-leads.query.md`
- `sourcing/recruitment-specific-open-roles/2026-11-16-role-phrases.csv` — 914 rows, one per company with a launch lead: cleaned role title (`{Job_Title_Open_}`) and job-description phrase (`{Job_Description}`), written 2026-11-16 by Claude sub-agents from the Blitz posting title + `ai_summary`; `launch_note` removes 9 companies (22 leads) whose role is outside what GRN places. Not an API pull.
- `sourcing/recruitment-specific-open-roles/2026-11-16-role-phrases-2.csv` — 914 rows, same companies and role titles as `-role-phrases.csv`, with `jd_phrase` rewritten after Moe's feedback that the first set did not read naturally. Shape now follows his two working examples: "<specialty> <function> experience with <specifics>". This is the file the Leads table and HeyReach use.
- `sourcing/recruitment-specific-open-roles/2026-11-16-job-descriptions.csv` — 914 rows: full job description of each company's chosen posting, read 2026-11-16 from the public posting page (`linkedin.com/jobs-guest/jobs/api/jobPosting/<id>`, `pull_job_descriptions.py`); 909 found, 433 marked closed ("No longer accepting applications")
- `sourcing/recruitment-specific-open-roles/2026-11-16-job-descriptions-2.csv` — 914 rows: the final posting per company after `rescue_closed.py` swapped a closed posting for another open kept posting where one existed (38 swapped). 519 companies have an open posting, 395 only closed ones
- `sourcing/recruitment-specific-open-roles/2026-11-16-role-phrases-3.csv` — 914 rows: **the file in use.** `jd_phrase` written from the full job description with Moe's own prompt (verbatim in this folder's `jd_phrase_prompt.md`) by 31 Claude sub-agents; 911 from the full description, 3 fall back to the Blitz summary. Carries `posting_open` and, for the 38 swapped companies, the new role and `job_url`
- `sourcing/recruitment-specific-open-roles/2026-11-23-jobs.csv` — 261 postings from the last 8 days (Blitz API `POST /v2/jobs/search`, same filters as 2026-11-16), 46 kept; 181 were at companies already in the 11-16 pull
- `sourcing/recruitment-specific-open-roles/2026-11-23-companies.csv` — 664 companies: 43 new (source A) + 621 wave-1 manufacturing companies re-queried deeper (source B)
- `sourcing/recruitment-specific-open-roles/2026-11-23-leads.csv` — 699 new prospects (680 launch set), Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-23, keyed by `linkedin_url`; none held before. Script: `pull_wave2.py`
- `sourcing/recruitment-specific-open-roles/2026-11-23-job-descriptions.csv` + `2026-11-23-role-phrases.csv` — 34 new companies: full job description (public posting page) and the role title + phrase written with Moe's prompt
- `sourcing/tam/2026-11-16-jobs-sample.csv` — 250 job postings (50 newest per role family), sizing sample for the Recruitment Specific campaign (no config yet), Blitz API `POST /v2/jobs/search`, pulled 2026-11-16
- `sourcing/tam/2026-11-16-sample-leads.csv` — 36 rows (35 prospects + 1 no-match placeholder) at 14 sampled companies, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-16, keyed by `linkedin_url`
- `sourcing/tam/2026-11-16-clay-sample-companies.csv` — 40 companies (2 queries x 20), Clay MCP `search-companies` fit check, pulled 2026-11-16
- `sourcing/tam/tam_counts.json` + `tam_counts.py`, `tam_sample.py`, `2026-11-16-tam-read.query.md` — count-only TAM read and its exact queries
- `sourcing/tam/2026-11-24-mpc-segments-jobs.csv` — 4,555 job postings (2,929 kept, the rest marked removed with a reason), 120 days, Blitz API `POST /v2/jobs/search`, pulled 2026-11-24 for the MPC segment read (no config yet; the live campaign's config is `fe214099-0834-40b6-9b18-d4517ecd03f1`). Each posting has a vertical and one role family. Script `mpc_segments_pull.py`, bodies and totals in `2026-11-24-mpc-segments-pull.json`
- `sourcing/tam/2026-11-24-mpc-segments-companies.csv` — 1,282 hiring companies, one row each: segment flags, repost/prolonged counts, whether they're in the live campaign. Derived from the jobs file (`mpc_segments_size.py`), 2026-11-24
- `sourcing/tam/2026-11-24-mpc-segments-sample-leads.csv` — 143 rows (92 with a LinkedIn URL, 51 `-` placeholders for companies with no match) at 93 sampled companies, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-24, keyed by `linkedin_url`. Reachability sample only, not a launch list (`mpc_segments_sample.py`)
- `sourcing/tam/2026-11-24-mpc-segments-posting-check.csv` — 120 postings checked open or closed on the public LinkedIn posting page, 2026-11-24 (not an API pull)
- `sourcing/tam/2026-11-24-apify-charlotte-jobs.csv` — 600 job postings (392 Indeed, 208 LinkedIn), Apify actor `LzsIpToRTUZSnqjbS` via GTM Sheets table `1a3119fc-23ee-42e3-a466-56c778e5cd3f` (Charlotte NC 100 mi, last 7 days, capped at 600 items), pulled 2026-11-24, coverage test against the Blitz pull (no config; `apify_compare.py`)
- `sourcing/tam/2026-11-24-mpc-segments.query.md` + `-size.json` — the segment read: table, sample results, TAM/SAM, message wording, Apify fit
- `sourcing/mpc-executive/2026-11-24-leads.csv` — 361 rows (107 launch set; the rest are marked removed with a reason, mostly people already in 734516/756466), config **MPC Executive** `05b28816-06e7-4d7d-9a6d-d9b606f39a68`, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-24, keyed by `linkedin_url`. The same folder holds `2026-11-24-companies.csv` (every company assigned to the segment, with leads per company), `-jobs.csv` (its kept postings) and `-role-phrases.csv` (final posting, open/closed, role, JD phrase, open line). Query record: `sourcing/mpc-build/2026-11-24-leads.query.md`
- `sourcing/mpc-operations-plant/2026-11-24-leads.csv` — 724 rows (39 launch set; the rest are marked removed with a reason, mostly people already in 734516/756466), config **MPC Operations & Plant** `eeb54cb5-55bf-47ac-b39a-744e747f2609`, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-24, keyed by `linkedin_url`. The same folder holds `2026-11-24-companies.csv` (every company assigned to the segment, with leads per company), `-jobs.csv` (its kept postings) and `-role-phrases.csv` (final posting, open/closed, role, JD phrase, open line). Query record: `sourcing/mpc-build/2026-11-24-leads.query.md`
- `sourcing/mpc-engineering-quality/2026-11-24-leads.csv` — 593 rows (66 launch set; the rest are marked removed with a reason, mostly people already in 734516/756466), config **MPC Engineering & Quality** `96f04838-dc74-4e52-b109-487f3d7e1688`, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-24, keyed by `linkedin_url`. The same folder holds `2026-11-24-companies.csv` (every company assigned to the segment, with leads per company), `-jobs.csv` (its kept postings) and `-role-phrases.csv` (final posting, open/closed, role, JD phrase, open line). Query record: `sourcing/mpc-build/2026-11-24-leads.query.md`
- `sourcing/mpc-supply-chain-purchasing/2026-11-24-leads.csv` — 379 rows (76 launch set; the rest are marked removed with a reason, mostly people already in 734516/756466), config **MPC Supply Chain & Purchasing** `587aa10e-be86-4618-827c-107e32d25bef`, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-24, keyed by `linkedin_url`. The same folder holds `2026-11-24-companies.csv` (every company assigned to the segment, with leads per company), `-jobs.csv` (its kept postings) and `-role-phrases.csv` (final posting, open/closed, role, JD phrase, open line). Query record: `sourcing/mpc-build/2026-11-24-leads.query.md`
- `sourcing/mpc-ehs-maintenance/2026-11-24-leads.csv` — 357 rows (106 launch set; the rest are marked removed with a reason, mostly people already in 734516/756466), config **MPC EHS & Maintenance** `3007a239-501f-4466-91a4-6944cad264a7`, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-24, keyed by `linkedin_url`. The same folder holds `2026-11-24-companies.csv` (every company assigned to the segment, with leads per company), `-jobs.csv` (its kept postings) and `-role-phrases.csv` (final posting, open/closed, role, JD phrase, open line). Query record: `sourcing/mpc-build/2026-11-24-leads.query.md`

## History

- **2026-11-25**: **MPC segments going live one a day** (Moe: "Go live on a schedule one daily starting with executive", then "live the whole creating and going live i tracking clients daily", then "confirm").
  - **Executive (760469) is live** since 11:31 UTC: started in HeyReach, and tracking_clients `start_campaign` confirms it is running with 10 senders. After a 5-row test (custom fields arrived), its 107 launch-set leads were pushed through GTM Sheets.
  - **The other four:** started and immediately paused at 11:31 UTC with empty lists, so nothing was sent. This was done before Moe clarified the daily plan; HeyReach can't return a started campaign to DRAFT, so they stay PAUSED.
  - **Daily go-live:** a scheduled task fires into this session at 07:52 America/New_York on each day. It pushes that campaign's leads, runs tracking_clients `start_campaign` (which resumes it), checks the list count, and records it here.
    - 11-26 Ops & Plant (39), `trig_01X4bCkgQvXfoy28BsH3qwX9`
    - 11-27 Eng & Quality (66), `trig_016vPFRq5vHEtzfo4sPVDjB2`
    - 11-28 Supply Chain (76), `trig_018vdWe4V6ibvnFbxUhoq1fG`
    - 11-29 EHS & Maintenance (106), `trig_01WUQeHZEoxwjZPZ1Bh6MLNn`
  - The tracking_clients board still shows these campaigns at "creation" (its sync only promotes Approved/Implementing campaigns).
  - Session session_013MzxQhML2MDSCMvFCprgqD.
- **2026-11-24**: **Apify coverage test** (Moe approved).
  - Actor `LzsIpToRTUZSnqjbS` on GRN's titles, Charlotte 100 mi, last 7 days, $5 cap. 600 rows (capped).
  - Only 2 of 257 companies with a leadership posting overlap the Blitz pull. Apify has no industry or size filter, so most of its employers are outside the ICP; about 2 ICP manufacturers in the sample were Apify-only.
  - Recommendation: keep Blitz as the MPC feed. A wider state-level test with a Blitz company match would settle whether Indeed adds enough. Details: `sourcing/tam/2026-11-24-mpc-segments.query.md`.
  - Session session_013MzxQhML2MDSCMvFCprgqD.
- **2026-11-24**: **5 MPC segment campaigns built in HeyReach and GTM Sheets, left in DRAFT** (Moe: "Yes to all 3").
  - **HeyReach** (workspace 172413):
    - Campaigns and lists: 760469/1218894 Executive, 760470/1218896 Ops & Plant, 760471/1218897 Eng & Quality, 760473/1218898 Supply Chain, 760475/1218899 EHS & Maint. Each is linked to its tracking_clients campaign.
    - All 10 valid senders; lead and company blacklists on; exclude-in-other-campaigns, other-account-conversation and sender-in-other-campaign all on.
    - Sequence = the live 756466 copy: blank connection request, then messages at +1, +2 and +2 days. Message 1 uses `{Open_Line}`; messages 2 and 3 use the segment's role-family wording (`sourcing/mpc-build/sequence.py`). Verified with `get_campaign_sequence`.
  - **Schedule:** before, none (new campaigns). After: **7 days, 07:00-19:00 America/New_York**, set at creation. The window is copied from 756466; it's Moe's call to change.
  - **GTM Sheets:** 5 workbooks, each with Companies, Jobs and Leads tables. Ids are in the GTM Sheets section above.
  - **Leads not pushed yet:**
    - A 20-row test push from the Executive table returned "the campaign is a draft and has no lead list to add to" for its 5 launch-set rows. GTM Sheets can only push once a campaign has been started.
    - The SOP step 9 gate (Moe reviews the workbooks) also comes before the push.
    - Nothing reached HeyReach. Next: Moe reviews, then start, push and verify the list counts (107 / 39 / 66 / 76 / 106).
  - **Task log** (Moe's board): 2663bc3b-2d4d-4361-bb52-6499134bd33d, d61b6485-bb1d-422d-bef0-da0233bd81b0, 12972f05-61eb-4f79-a487-46880c651942, bc26be0a-f215-4fa7-9f05-ea6f28cc38bd, e0e1b489-a968-4faa-b557-54b3893e364f.
    - The first attempt went through the shared tracking_clients connector, which logged the 5 tasks under Dave. They couldn't be reassigned ("Only the admin can change owner").
    - Those 5 were retitled DUPLICATE: 2dea823e, 4eaf92f1, 13f602af, aa8e23f0, f7b8c9c4.
  - **Not touched:** the pending sender/schedule batch for 734516/756466/730732; F&LS (folded into 730732, not built here).
  - Session session_013MzxQhML2MDSCMvFCprgqD.
- **2026-11-24**: **5 new MPC segments sourced and created in tracking_clients** (Moe: "Yes to all 3" — the 5-campaign build, EHS & Maintenance as a segment, and the Apify test). **New segments** `mpc-executive`, `mpc-operations-plant`, `mpc-engineering-quality`, `mpc-supply-chain-purchasing`, `mpc-ehs-maintenance`. Scope: Campaign-specific.
  - **Pull:** Blitz `POST /v2/search/waterfall-icp-keyword` on all 1,256 non-F&LS hiring companies from the 11-24 read, 2,415 records. Leads per segment: Executive 107, Ops & Plant 39, Eng & Quality 66, Supply Chain 76, EHS & Maintenance 106, **394 in total** at 189 companies.
  - **Exclusions:** 2,011 people already in 734516/756466 were marked removed. Overlap check (`tools/leads.py overlap`): every overlap with `2026-11-16-leads.csv` / `2026-11-23-leads.csv` is one of those removed rows, and the launch set has 0.
  - **TAM/SAM:** small pool, so the inverse rule applies. Everyone Blitz returns for the persona is taken (up to 5 at new companies, searched to 10 at live ones), about 2.1 per company.
  - **Postings:** open-posting check gave 99 open and 94 closed. Closed postings are kept per Moe's 11-16 instruction; `posting_open` shows which. 5 companies get the repost line.
  - **Phrases:** written with Moe's prompt by sub-agents. 4 companies outside the ICP were removed: a car wash, a fuel distributor, an equipment dealer, and a sales-only role.
  - **tracking_clients:** 5 ICP configs, 5 lead lists (`campaign_split: false`) and 5 campaigns (status creation, linked to campaign doc `cae47cc4`, not client-signed). Ids are in the table under Sourcing configs.
  - **Gate deviation (Moe's call):** the doc standard says no config before client approval of the doc. These were created on Moe's go-ahead, as Campaign 6 was. The client hasn't seen the segments yet, and EHS & Maintenance still needs GRN to confirm.
  - Query record: `sourcing/mpc-build/2026-11-24-leads.query.md`. Session session_013MzxQhML2MDSCMvFCprgqD.
- **2026-11-24**: **MPC segment read** (Moe: "create more segments of the MPC campaign, based on the client's ICP"). Sizing only: no campaign, config, list or workbook created; waiting for Moe's go-ahead.
  - **Pull:** fresh 120-day Blitz `POST /v2/jobs/search`, split by vertical and by role family, 5,388 records. It adds two families the live campaign never searched: EHS/Maintenance, and Logistics/Planning inside Supply Chain. Result: 1,282 hiring companies, 2,929 kept postings.
  - **Finding:** 919 of the 1,282 companies (72%) already have leads in 734516/756466.
    - At those companies the persona is used up: 3 uncontacted C-level/VP/Owner contacts in 30 sampled companies.
    - Of the 363 others, about 245 were queried before with no persona match: 0 of 42 sampled match now.
    - The 118 never pulled answer 57% of the time, at 2.4 contacts each.
    - So about 160 new people now, plus about 100 a month from new postings.
    - No segment clears the 200 to 300 net-new company bar; each would be a rolling, monthly-refill segment.
  - **Prolonged vacancy:** posting age alone fails (34 of 40 postings aged 60+ days are closed). A role first posted 60+ days ago and **reposted** in the last 30 days is open 80% of the time, and 116 companies show it.
  - **Overlap** (`tools/leads.py overlap` on the sample): 48 of these also appear in `sourcing/recruitment-specific-open-roles/2026-11-16-leads.csv`; 12 of these also appear in `sourcing/recruitment-specific-open-roles/2026-11-23-leads.csv`.
  - **Apify feed** (actor `LzsIpToRTUZSnqjbS`): location-radius only, no firmographic filter. The coverage test is proposed, not run.
  - Contacts per company if built: up to 5 manufacturing / 4 F&LS (small pool, inverse rule). Scope: Campaign-specific (MPC segments).
  - Full read: `sourcing/tam/2026-11-24-mpc-segments.query.md`. About 5,480 Blitz records. Session session_013MzxQhML2MDSCMvFCprgqD.
- **2026-11-24**: Session initialized (orchestrator dispatch). Re-synced from `get_client` + `list_sourcing_configs`; no drift in profile or the 3 configs (`fe214099-0834-40b6-9b18-d4517ecd03f1`, `e8538474-8bd8-4479-8878-5899efe1ccf4`, `88fe680f-eae0-40c5-b147-1edf40579466`). Recorded every HeyReach campaign's senders, sequence check and schedule (section above) ahead of Moe's 2026-11-24 batch: all valid senders on all campaigns, 7-day schedules on active campaigns. **Not applied yet.** The approval came relayed through an orchestrator notification, not from Moe in this session, and the HeyReach schedule rule needs the owner's go-ahead at the time to pause live campaigns. Waiting for that go-ahead. Flagged: 730731 Owner Succession (Campaign 5) stays as it is under the factual-accuracy guard; 271564 (Chris Missler) has a broken sign-in. Session session_013MzxQhDJ5FhMvdPeQEAMTM.
- **2026-11-23** — Moe: "Source and Push more leads into the campaign. Until then do 2.0 in heyreach for the performing campaign." **Expanding existing segment** (`recruitment-specific-open-roles`), Blitz only.
  - Performance of 734516 after 7 days: 1,261 connection requests, 98 accepted (7.8%), 59 conversations, 11 replies (18.6%), 2 auto-tagged interested.
  - **2.0:** HeyReach campaign 756466 "Recruitment Specific Campaign 2.0" on new list 1211197, same sequence copied from 734516, 10 senders (7 already on 734516 plus 3 idle accounts: 196127, 261055, 278063; 271564 has a broken sign-in), weekdays 07:00-19:00 Eastern, excludes leads with a conversation on another account and leads the same sender contacted in another campaign. It holds **only new leads**.
  - **Mistake, caught and reversed:** the first push into 2.0 used the wave-1 table, so 104 people already in 734516 landed in 2.0. The push was stopped and 2.0 paused; no action had been taken on them from 2.0. Deleting them from list 1211197 removed them from the campaign (0 leads after). The column was deleted from the wave-1 table.
  - **Wave 2 sourcing (`pull_wave2.py`):** A) new postings in the last 8 days, 43 new companies, 52 leads; B) the 11-16 waterfall capped manufacturing at 2 people per company and 628 companies hit the cap, so 621 of them were re-queried at up to 5, adding 636 new people (TAM/SAM read unchanged; this raises contacts per company from 2 to up to 5 because the pool of hiring companies in the window is used up and the house rule is more people reached). 699 new prospects, 680 launch set; 3 overlap only with the same-day TAM sample. 2,202 Blitz records.
  - Phrases: wave-B leads reuse their company's 11-16 role and phrase; the 34 new companies got job descriptions and phrases with Moe's prompt. 229 of the 680 sit at companies whose posting is closed (kept in, per Moe's earlier instruction).
  - Pushed through GTM Sheets table "4 Leads Wave 2 (2.0)" into 756466. A list check found 681: one wave-1 lead (logan-mcleod-6660734, Element U.S. Space & Defense) had landed from a cell still running when the first push was stopped; removed. 756466 resumed 2026-11-24 with 680 leads, none of them wave-1 people. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — **Recruitment Specific Campaign went live** on Moe's instruction ("Go live tracking clients and hey reach"). HeyReach 734516 started 08:37 UTC (`start_campaign`): IN_PROGRESS, 1,541 leads, 10 senders, lead and company blacklists on. tracking_clients campaign `ed2f167f-5cea-4b2e-833b-20b2aafe26e0` moved creation -> running. All 1,541 launch-set rows show pushed in GTM Sheets table `3bfcb40c-0b6d-48e4-8f72-e2105ef426e0`, with the final phrases and `Company_Name`. Launched before client sign-off on Campaign 6 in the doc; 395 companies' postings were closed at launch (kept in on Moe's instruction). Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — JD phrases redone a third time, now from the **full job description** with the prompt Moe supplied (he rejected the summary-based wording and gave the prompt his other campaigns run). Blitz only returns a two-sentence summary, so the descriptions were read from the public posting pages. Finding: 433 of 914 chosen postings are closed; 38 companies had another open posting and were switched to it. Moe: "run on the closed ones as well", so closed-posting leads stay in the launch set (`Posting Open` column shows which). HeyReach `{COMPANY}` is overwritten by HeyReach with the profile's company name, so the cleaned name is sent as custom field `Company_Name` and the sequence reads that; the wording is unchanged. Verified with the GRN Piedmont HeyReach connector that a re-push overwrites custom fields on leads already in list 1169425. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — Recruitment Specific Campaign built, **not yet started**. Moe gave the three messages verbatim, set the 120-day window, said to use Blitz, to add it to the client doc, and to create it and make it live ahead of client sign-off; campaign thinking is his sentence. Created: ICP config, lead list (`campaign_split: false`, chosen because one list feeds one campaign), campaign `ed2f167f-5cea-4b2e-833b-20b2aafe26e0`, HeyReach 734516 (blank connection request, Message 1 one day after acceptance, then +2 and +2 days, 10 senders), GTM Sheets workbook. Launch set is 1,541 of 1,563 (4 titles outside persona, 22 at 9 companies whose role GRN does not place). About 900 leads were pushed to HeyReach list 1169425 with the first phrase set before Moe rejected the wording; the push was stopped, the phrases rewritten (`-role-phrases-2.csv`) and the Leads table rebuilt (first two Leads tables deleted). Re-push and start are on hold until the GRN Piedmont HeyReach connector is authenticated and a check confirms the custom fields overwrite. Open points: the copy says "Hey" and "I have a candidate" and does not name GRN Piedmont, against the client's doc comments; GRN has not confirmed candidates on hand; the GTM Sheets OpenRouter key is at its $1,000 cap, so no AI column ran. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — **New segment:** `recruitment-specific-open-roles` leads snapshot, 1,563 prospects (Blitz API only, on Moe's instruction "Use Blitz for sourcing"). Feeds the Recruitment Specific Campaign. Scope: Campaign-specific. Window 120 days (Moe). TAM/SAM: 1,161 hiring companies, large, so 2 contacts per company for manufacturing and 4 for the 25 fire & life safety companies. Overlap check: 18 of these also appear in `sourcing/tam/2026-11-16-sample-leads.csv` (same-day sizing sample); no other lead files exist. 5,990 Blitz records. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — TAM read for a new **Recruitment Specific** (open role / MPC) campaign. Moe asked for it on the Trillium Construction "Recruitment Specific Campaign" messaging and set the window to 120 days. Blitz counts: 3,870 matching manufacturing leadership postings in 120 days (855 in 30) at 201 to 1,000 employee Eastern/Central manufacturers, 556 fire & life safety postings before a noise gate. TAM/SAM read: manufacturing large, 2 contacts per company; F&LS small, 3 to 4. Scope: Campaign-specific. Full read in `sourcing/tam/2026-11-16-tam-read.query.md`. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — Folder created from `clients/_TEMPLATE/README.md`; profile, sourcing configs, campaigns and campaign doc synced from `tracking_clients`. The client was onboarded 2026-11-02 and had a doc and two campaigns already, but no folder in this repo.
