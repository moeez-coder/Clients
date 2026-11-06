# SOP: Open Role Moe MPC

> **What it is:** a recruiter-client LinkedIn campaign whose entry point is a **live open job**. We find companies currently hiring for a role family the client places. We reach the **hiring manager** for that role (or a talent leader as fallback) and open with the specific role: "saw the {Open_Role} opening at {Company_Name}".
>
> **Status:** v1, written 2026-11-05 from the first full run (C&G Consulting Services, 4 segments). Source session: `session_013MzxQhz38kzePny7FphVBL`. Worked example: `clients/cg-consulting-services/` (README History 2026-11-05, `sourcing/recruiter-open-role-*`). Improve this SOP as real runs show what works, and log each change at the bottom.
>
> **Not verified against the brain repo.** `AdmiralGeneralBaba/algoacquisition-brain` has an MPC skill (`Internal/Campaign-Types/Recruitment/MPC-Campaign/mpc-campaign-skill.md`) that could not be read from this session. Reconcile the two when someone has access, and record what changed.

---

## 1. When to use it

- The client is a **recruitment/staffing agency**, and the ICP form names role families they place (e.g. Biostats, Regulatory Affairs, Software Engineer).
- There are enough live postings in those role families for a campaign. Size it first (§4, step 1).
- It runs **alongside** the client's other campaigns, not instead of them. Each role family is its own segment.

## 2. Inputs: ask, don't guess

Collect these before running anything. Record each in the client README History, and **don't re-ask anything already recorded there**.

| Input | Example (C&G) |
|---|---|
| Segments: role families, one campaign each | LS Clinical & Data / LS Regulatory & Quality / LS Medical Affairs / Tech Eng, Security & Data |
| Job-title keywords per segment | Biostatistician, Statistical Programmer, Clinical Data Manager, … |
| Hiring-manager titles per segment (waterfall tier 1) | Head/Director/VP of Biostatistics, Clinical Data Management, … |
| Fallback tier (all segments) | Head of Talent, Talent Director, Director of Talent Acquisition, VP People |
| Excluded titles | Sales, Warehouse, Intern |
| Industries per segment (exact Blitz enum labels) | LS: Pharmaceutical Manufacturing, Biotechnology Research, … |
| Firmographics | US HQ, 51–5,000 employees, `is_agency: false` |
| Geo priority | Northeast (DC→Boston) first |
| Contacts per company (TAM/SAM read, §5) | 3 for small LS pools, 1 for the large Tech pool |
| Record budget and stop line | ~15–25k Blitz records approved; stop and ask above 40k |
| DNC file | the client's `Non_Connect` upload from the ICP form |

## 3. Sequence (HeyReach)

- **One HeyReach campaign per segment.** This is *not* the Vertical Launch quadset. Each campaign has its own list, with **exclude-in-other-campaigns ON**, and "Recruiter" in the campaign name.
- **Connection request *with* a note.** This is a deliberate exception to the org's blank-request rule (Moe, 2026-11-05):
  > Hi {FIRST_NAME}, saw the {Open_Role} opening at {Company_Name}. Figured it was worth connecting given the space you're in.
- **Messages 1–3 at +2, +2 and +2 days.**

**Full copy (verbatim from Moe, 2026-11-05). Used by Talent Edge (Finance & Accounting) and Alcor (Recruiters), 19.4% reply rate. Only the role family changes between clients and segments.**

**Connection request**

> Hi {FIRST_NAME}, saw the {Open_Role} opening at {Company_Name}. Figured it was worth connecting given the space you’re in.

**Message 1 (2 days after connecting)**

> Hey {FIRST_NAME}, thanks for connecting. Saw {COMPANY} has a {Open_Role} role listed, looks like you need someone with {JD}.
>
> Not sure if that’s a fresh one or something you’ve had open for a bit, but either way we have a candidate who fits that pretty closely.
>
> Want us to send their profile over so you can take a look?

**Message 2 (2 days later)**

> Hey {FIRST_NAME}, following up on this, didn’t want it to get buried.
>
> If there’s an {Accounting or Finance / engineering} open role that has been sitting open for a while, we can send over a profile that fits what you need. Even roles that have been open a while tend to still be live.
>
> Worth a quick look, even just to compare against who you already have in the pipeline?

**Message 3 (2 days later)**

> No worries if the timing’s off, {FIRST_NAME}. {Finance / Engineering} roles sometimes get filled quietly or just sit for a while without much movement.
>
> If you have a role open we’ll send a profile over and you can skim it whenever. If not, no hard feelings and we’ll leave it there.
>
> Just let us know either way.

**Before building, note:**
- `{Accounting or Finance / engineering}` (message 2) and `{Finance / Engineering}` (message 3) are the **role-family slots**. Fill them per segment and record the wording in the client README.
- `{COMPANY}` and `{Company_Name}` are the same value (`company_name`).
- `{JD}` has to fit "looks like you need someone with {JD}". Blitz's `ai_summary` is a two-sentence job description, not a phrase, so it reads badly here. Generate a short "someone with …" phrase per row (e.g. a GTM Sheets AI column over `jd_summary`). Review it before any push.

- Variables map to lead columns:
  - `{Open_Role}` = `open_role`
  - `{JD}` = `jd_summary`
  - `{Company_Name}` = `company_name`

## 4. Steps

Do one segment at a time, and **commit each segment before starting the next** (CLAUDE.md). Run the smaller segments first and the large one last.

### Step 1: size each segment (about 1 record per call)

`POST /v2/jobs/search` with `max_results: 1` reads `total_results`. Run it once for all US jobs and once restricted to Northeast HQ (`company.hq.state.include`). Widen the title keywords first, because Blitz title matching is keyword-based:
- every word must appear, in any order, as whole words
- no stemming
- `VP` is not expanded to `Vice President`

So list each variant separately ("Statistician", "Statistical Programmer", "SAS Programmer", …).

### Step 2: pull open jobs

- Endpoint: `POST /v2/jobs/search`, cursor-paged at up to **50 per page**, with a **5,000-job cap per query**. 1 record per result.
- Filters:
  - `job.title.include/exclude`
  - `job.location.country_code.include ["US"]`
  - `job.date_posted.last_days 30`
  - `company.{is_agency:false, industry.include, size.include, hq.country_code.include}`
- **Large segment over the cap:** pull all Northeast-HQ jobs first (`hq.state.include` with the full state names), then fill the remaining cap with the most recent non-Northeast jobs (`hq.state.exclude`).
  - Use "District of Columbia", not "Washington", which would also match Washington State.

### Step 3: pull hiring companies

- **Use `POST /v2/company/tam-by-jobs`** with the same filters. It returns distinct companies with HQ state, size, industry and `matched_jobs`, at 1 record per company. It has no total count, so you have to page through it.
- **Use `POST /v2/enrichment/company` instead** for a capped segment's non-Northeast part. Run it per company seen in the pulled jobs, which is cheaper than paging the whole non-Northeast TAM.
- For each company, the **most recent** matching posting becomes `open_role` (its title) and `jd_summary` (its `ai_summary`).

### Step 4: find people by waterfall

- Endpoint: `POST /v2/search/waterfall-icp-keyword`, one call per hiring company:
  - `company_linkedin_url`
  - `cascade` with tier 1 = hiring manager titles and tier 2 = fallback titles
  - each tier has `exclude_title` and `location.country_code ["US"]`
  - `max_results` = contacts per company
- Each result carries `icp`, the tier that matched. Record it as `waterfall_tier`.
- **LinkedIn URLs only, no email enrichment.**
- Clean `last_name`: strip credential suffixes after a comma (e.g. "Quinn, CCDM" becomes "Quinn").

### Step 5: dedupe (flag it, never drop it)

Match on a normalised LinkedIn URL (lowercase, URL-decoded, no query string or trailing slash, `www.linkedin.com`) against:

1. **Every live HeyReach list of the client.** Use the repo's wave/push files when they exactly reproduce the list; otherwise read the list. The result goes in the column `in_heyreach_list_<id>`.
2. **Every other `*-leads.csv` for the client**, including segments built earlier in this run. The result goes in the column `dupe_of`.
3. **Process segments in a fixed order**, so a person stays `live_eligible=yes` only in the first segment where they appear.

Expect heavy overlap when a segment's persona matches an existing campaign. On C&G, Tech had 410 of 1,267 leads already in Security and Data Bench.

### Step 6: write files and commit

- Location: `clients/<slug>/sourcing/<segment-slug>/`, with segment slug `recruiter-open-role-<family>`.
- Files:
  - `<date>-jobs.csv`
  - `<date>-companies.csv`
  - `<date>-leads.csv`, with `linkedin_url` as the first column
  - `<date>-leads.query.md`, holding:
    - the exact request bodies
    - the record counts from `fair_usage.records_used`
    - the TAM/SAM read
    - contacts per company
- Leads columns:
  - `linkedin_url, first_name, last_name, title, waterfall_tier, company_name, company_linkedin_url`
  - `open_role, job_url, job_posted, jd_summary`
  - `hq_state, northeast`
  - `in_heyreach_list_<id>, dupe_of, live_eligible`
  - Use `-` for checked-but-empty cells.
- In the same commit, update the README (a "Sourced data" row per file and a History entry: "new segment", tool, rows, TAM/SAM, contacts per company), then commit with `<client>: add <date> leads snapshot — <segment-slug> (Blitz API, N rows)`.
- **Reusable code:** `clients/cg-consulting-services/sourcing/open_role_spec.py` (filters), `pull_open_roles.py` (resumable pull with record tally) and `build_open_roles.py` (CSVs and dedupe). Copy them into the new client's `sourcing/` and change only the spec.

### Step 7: build GTM Sheets (one workbook per campaign)

Moe's rule: **every campaign gets its own workbook, and it holds the open jobs and companies as well as the leads**, so the whole build is visible.

1. `gtm_sheet_open_client_folder`, which opens `Clients / <client>`.
2. `gtm_sheet_create_workbook`, named `<Client> | Recruiter | Open Role | <Segment>`. In the description, say where the data came from and that it's review-only.
3. `gtm_sheet_import_csv` **three times** into new tables: **Leads**, **Companies** and **Open Jobs**.
   - Use `url` = the raw GitHub file **pinned to the commit SHA**, with `auto_run: false`, so no rows pass through chat.
   - The URL only works while the repo's raw files are publicly reachable. If they aren't, use the brain SOP's shell route to the dashboard MCP.
   - Check that each `inserted` count equals the CSV's row count.
4. Record the workbook and table ids in the client README.

### Step 8: tracking_clients

1. `create_icp_config`, **one per segment**:
   - `name`: `Recruiter | Open Role | <Segment>`
   - `market`: the industries
   - sizes and geos
   - custom signal: "live US job posting (last 30 days) for …"
   - persona: hiring manager titles plus the fallback
2. `create_sourcing_config` on that segment: `static` refresh, named after where the leads come from.
   - **Ask the user for `campaign_split` before calling.** It can't be changed afterwards. Default suggestion: `false`, because each list feeds one campaign.
3. `gtm_sheet_update_table` with `lead_list` on each Leads table. This is a label only. **Don't `route_lead_list` or ingest until the push is approved.**
4. Record every UUID in the README Sourcing configs and in each `.query.md`.

### Step 9: hard gates before HeyReach

- [ ] The user has reviewed each workbook. Look for adjacent-title noise and public bodies picked up by Education/Finance industry labels.
- [ ] The client's **DNC file is loaded** (`update_client_dnc` and/or the HeyReach blacklist), and leads are checked against it.
- [ ] The role-family wording for messages 2–3 is chosen per segment and saved in the client README.
- [ ] A short `{JD}` phrase exists for every lead and has been reviewed.
- [ ] Only `live_eligible=yes` leads go in.

Only then: build one HeyReach campaign per segment (§3) and push.

## 5. TAM/SAM → contacts per company (inverse rule, CLAUDE.md)

| Pool | Example | Contacts per company |
|---|---|---|
| Small (≈100–600 hiring companies) | LS Clinical & Data 126, Medical Affairs 141, Reg & Quality 523 | **3** (2–3 for mid-size) |
| Large (thousands; jobs hit the 5,000 cap) | Tech: 15,296 jobs → 1,479 companies after the cap | **1** hiring manager, Northeast first |

Record the read and the resulting number in each `.query.md`.

## 6. Cost reference (C&G run, 2026-11-05)

| Segment | Jobs | Companies | Leads | Blitz records |
|---|---|---|---|---|
| LS Clinical & Data | 297 | 126 | 273 | 696 |
| LS Regulatory & Quality | 1,286 | 523 | 999 | 2,809 |
| LS Medical Affairs | 438 | 141 | 338 | 917 |
| Tech Eng, Security & Data | 5,000 | 1,479 | 1,267 | 7,747 |
| **Total** | | | **2,877** | **12,169** |

**Rule of thumb:** records ≈ jobs + companies + leads. About 92% of LS companies and 86% of Tech companies returned at least one person.

## 7. Known pitfalls

- **IT services firms:** leave "IT Services and IT Consulting" out of Tech industries. It's mostly staffing/outsourcing shops, i.e. the client's competitors. `is_agency:false` only drops confirmed agencies.
- **Short title tokens:** "QA"/"QC" are safe only because the LS industry filter is there. Don't reuse them for Tech.
- **Adjacent tier-1 matches:** e.g. "Director, Product Management – Data Products" matched "Director Data Management". Review the sheet before any push.
- **README edits by script:** anchor on text that really exists, and chain `&& git commit`. Two snapshot commits in the first run went in without their README rows because a substring anchor missed.
- **Generated files:** don't commit `__pycache__/` (or other generated files) when you `git add` a sourcing folder.

---

## Change log

- **2026-11-05**: §3 now has the full Open-role sequence copy (verbatim from Moe), plus notes on the role-family slots and the `{JD}` phrase.
- **2026-11-05**: v1 from the C&G run. Named "Open Role Moe MPC" at Moe's request.
