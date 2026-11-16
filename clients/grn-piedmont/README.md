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
- **Last synced:** 2026-11-16 via `get_client` + `list_sourcing_configs` + `list_campaigns` + `list_campaign_docs`

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

| Campaign "Recruitment Specific Campaign" | `ed2f167f-5cea-4b2e-833b-20b2aafe26e0` (HeyReach 734516, lead list 1169425) | see History |

Campaign 6 and the offers section were added to the campaign doc on 2026-11-16 as tracked suggestions; the text is in `campaign-docs/2026-11-16-campaign-6-recruitment-specific.md`.

## GTM Sheets

Workbook **US | Recruiter | Recruitment Specific Open Roles | Moe v1** `4086bd52-c75b-460e-959b-280a5bc93722`, in Clients / GRN Piedmont (folder `5b185300-2443-46b3-9a4d-b50cb54f4368`), linked to campaign `ed2f167f-5cea-4b2e-833b-20b2aafe26e0`.

| Table | ID | Rows | Loaded from |
|---|---|---|---|
| 1 Companies | `370b9f00-8bb2-4a97-975a-87f507a5a5d8` | 1,161 | `2026-11-16-companies.csv` |
| 2 Jobs | `a87d6fbd-ce5c-4023-bc8c-37098f1ccb69` | 4,426 | `2026-11-16-jobs.csv` |
| 3 Leads | `7f4b15ab-96a3-423c-a063-06d2f686fa60` | 1,563 | `2026-11-16-leads.csv` + `2026-11-16-role-phrases-2.csv`; linked to lead list `fe214099-0834-40b6-9b18-d4517ecd03f1`; Push to HeyReach column -> 734516, `run_if` Status = launch set |

Loaded with `gtm-sheets/load_tables.py` (webhook URLs passed as arguments, not committed). `Job Title Open` and `Job Description` are plain data, not an AI column: the GTM Sheets OpenRouter key hit its $1,000 total cap on 2026-11-16, so the phrases were written by Claude sub-agents and saved to the repo.

## Sourced data in this repo

- `sourcing/recruitment-specific-open-roles/2026-11-16-jobs.csv` — 4,426 job postings (3,347 kept, the rest marked removed with a reason) for the **Recruitment Specific Campaign** lead list, Blitz API `POST /v2/jobs/search`, last 120 days, pulled 2026-11-16
- `sourcing/recruitment-specific-open-roles/2026-11-16-companies.csv` — 1,161 companies with a kept posting, one open role each, with a `leads_launch_set` count (246 produced no lead and stay in the file), derived from the jobs pull, 2026-11-16
- `sourcing/recruitment-specific-open-roles/2026-11-16-leads.csv` — 1,563 prospects (1,559 launch set) at 915 companies, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-16, keyed by `linkedin_url`. Query record: `2026-11-16-leads.query.md`
- `sourcing/recruitment-specific-open-roles/2026-11-16-role-phrases.csv` — 914 rows, one per company with a launch lead: cleaned role title (`{Job_Title_Open_}`) and job-description phrase (`{Job_Description}`), written 2026-11-16 by Claude sub-agents from the Blitz posting title + `ai_summary`; `launch_note` removes 9 companies (22 leads) whose role is outside what GRN places. Not an API pull.
- `sourcing/recruitment-specific-open-roles/2026-11-16-role-phrases-2.csv` — 914 rows, same companies and role titles as `-role-phrases.csv`, with `jd_phrase` rewritten after Moe's feedback that the first set did not read naturally. Shape now follows his two working examples: "<specialty> <function> experience with <specifics>". This is the file the Leads table and HeyReach use.
- `sourcing/tam/2026-11-16-jobs-sample.csv` — 250 job postings (50 newest per role family), sizing sample for the Recruitment Specific campaign (no config yet), Blitz API `POST /v2/jobs/search`, pulled 2026-11-16
- `sourcing/tam/2026-11-16-sample-leads.csv` — 36 rows (35 prospects + 1 no-match placeholder) at 14 sampled companies, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-16, keyed by `linkedin_url`
- `sourcing/tam/2026-11-16-clay-sample-companies.csv` — 40 companies (2 queries x 20), Clay MCP `search-companies` fit check, pulled 2026-11-16
- `sourcing/tam/tam_counts.json` + `tam_counts.py`, `tam_sample.py`, `2026-11-16-tam-read.query.md` — count-only TAM read and its exact queries

## History

- **2026-11-16** — Recruitment Specific Campaign built, **not yet started**. Moe gave the three messages verbatim, set the 120-day window, said to use Blitz, to add it to the client doc, and to create it and make it live ahead of client sign-off; campaign thinking is his sentence. Created: ICP config, lead list (`campaign_split: false`, chosen because one list feeds one campaign), campaign `ed2f167f-5cea-4b2e-833b-20b2aafe26e0`, HeyReach 734516 (blank connection request, Message 1 one day after acceptance, then +2 and +2 days, 10 senders), GTM Sheets workbook. Launch set is 1,541 of 1,563 (4 titles outside persona, 22 at 9 companies whose role GRN does not place). About 900 leads were pushed to HeyReach list 1169425 with the first phrase set before Moe rejected the wording; the push was stopped, the phrases rewritten (`-role-phrases-2.csv`) and the Leads table rebuilt (first two Leads tables deleted). Re-push and start are on hold until the GRN Piedmont HeyReach connector is authenticated and a check confirms the custom fields overwrite. Open points: the copy says "Hey" and "I have a candidate" and does not name GRN Piedmont, against the client's doc comments; GRN has not confirmed candidates on hand; the GTM Sheets OpenRouter key is at its $1,000 cap, so no AI column ran. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — **New segment:** `recruitment-specific-open-roles` leads snapshot, 1,563 prospects (Blitz API only, on Moe's instruction "Use Blitz for sourcing"). Feeds the Recruitment Specific Campaign. Scope: Campaign-specific. Window 120 days (Moe). TAM/SAM: 1,161 hiring companies, large, so 2 contacts per company for manufacturing and 4 for the 25 fire & life safety companies. Overlap check: 18 of these also appear in `sourcing/tam/2026-11-16-sample-leads.csv` (same-day sizing sample); no other lead files exist. 5,990 Blitz records. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — TAM read for a new **Recruitment Specific** (open role / MPC) campaign. Moe asked for it on the Trillium Construction "Recruitment Specific Campaign" messaging and set the window to 120 days. Blitz counts: 3,870 matching manufacturing leadership postings in 120 days (855 in 30) at 201 to 1,000 employee Eastern/Central manufacturers, 556 fire & life safety postings before a noise gate. TAM/SAM read: manufacturing large, 2 contacts per company; F&LS small, 3 to 4. Scope: Campaign-specific. Full read in `sourcing/tam/2026-11-16-tam-read.query.md`. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — Folder created from `clients/_TEMPLATE/README.md`; profile, sourcing configs, campaigns and campaign doc synced from `tracking_clients`. The client was onboarded 2026-11-02 and had a doc and two campaigns already, but no folder in this repo.
