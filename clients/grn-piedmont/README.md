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

## GTM Sheets

Workbook **US | Recruiter | Recruitment Specific Open Roles | Moe v1** `4086bd52-c75b-460e-959b-280a5bc93722`, in Clients / GRN Piedmont (folder `5b185300-2443-46b3-9a4d-b50cb54f4368`), linked to campaign `ed2f167f-5cea-4b2e-833b-20b2aafe26e0`.

| Table | ID | Rows | Loaded from |
|---|---|---|---|
| 1 Companies | `370b9f00-8bb2-4a97-975a-87f507a5a5d8` | 1,161 | `2026-11-16-companies.csv` |
| 2 Jobs | `a87d6fbd-ce5c-4023-bc8c-37098f1ccb69` | 4,426 | `2026-11-16-jobs.csv` |
| 3 Leads | `3bfcb40c-0b6d-48e4-8f72-e2105ef426e0` | 1,563 | `2026-11-16-leads.csv` + `2026-11-16-role-phrases-3.csv`; linked to lead list `fe214099-0834-40b6-9b18-d4517ecd03f1`; Push to HeyReach column -> 734516, `run_if` Status = launch set |

| 4 Leads Wave 2 (2.0) | `99a71d70-cb2a-4445-9068-f49d708ccbee` | 699 | `2026-11-23-leads.csv` + phrases; Push to HeyReach 2.0 column -> 756466 |

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
- `sourcing/tam/2026-11-24-mpc-segments.query.md` + `-size.json` — the segment read: table, sample results, TAM/SAM, message wording, Apify fit

## History

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
