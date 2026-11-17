# 2026-11-17 TAM sizing: proposed C7 "Multiple Open Roles"

**Client:** GigWorx (`94da4a2f-8f90-4bc0-87e6-22ff98fafd6a`)
**Proposed campaign:** C7 - Multiple Open Roles. Any ICP-fit Michiana company with multiple open jobs; target the people there. Not yet a `tracking_clients` campaign or sourcing config: per the campaign doc standard it needs a doc and client approval first.
**Segment:** new segment (job-signal across all ICP verticals). It overlaps C1 (3+ hourly roles) and C4 (5+ hourly roles), which gated on job counts but started from HQ-located companies; C7 starts from where the jobs are posted.
**Asked by:** the repo owner, 2026-11-17: "create a new campaign that takes open jobs as signal... what will be the count of companies, do the sizing". Mid-session they asked for complete job coverage, using Apify through GTM Sheets for job boards.
**Scope:** sizing only. No people pulled, nothing pushed to HeyReach.

## Part 1: LinkedIn jobs (Blitz), done

### Jobs: `2026-11-17-c7-blitz-jobs.csv` (10,249 unique postings)
Tool: **Blitz API `POST /v2/jobs/search`**, cursor-paged until `cursor: null` (every town fully exhausted; pulled = `total_results`).

```json
{"job": {"location": {"city": {"include": ["<town>"]}, "country_code": {"include": ["US"]}},
         "date_posted": {"last_days": 60}},
 "max_results": 50}
```
Run once per town: South Bend 4,107; Mishawaka 2,484; Elkhart 2,167; Goshen 1,087; Nappanee 93; Wakarusa 31; Notre Dame 549 (10,518 rows, 10,249 unique URLs).

Towns left out on purpose: Bristol, Middlebury, Osceola, Granger, Lakeville, Millersburg, New Carlisle, North Liberty, Dunlap, Walkerton. `job.location` takes no state, and these names mostly match other states (e.g. Bristol: 4,541 jobs in 90 days, mostly CT/PA/TN/VA). Indeed (Part 2) covers them with the state attached.

### Companies: `2026-11-17-c7-blitz-hiring-companies.csv` (1,398 companies)
Tool: **Blitz API `POST /v2/company/tam-by-jobs`**, same filter per town, cursor-paged to the end. It gives firmographics (industry, size, HQ) for every company behind the jobs above. Job counts per company come from the jobs file.

Columns added in this session (`classify.py`, copied here):
- `icp_bucket`: from the LinkedIn industry. `manufacturing`, `warehousing_logistics`, `retail` and `hospitality_fb_events` are the four approved verticals (campaign doc `4d41ad80-0451-4524-bf83-819a4418be7b`). `construction_held` is out unless Mathew asks. `excl_staffing` (Staffing and Recruiting, HR Services, Executive Search), `excl_dealer` (car dealerships, by industry or name) and `out_of_icp` are excluded.
- `hourly_jobs_60d`: postings whose title matches the hourly/shift regex in `classify.py` and not the salaried/CDL/clinical regex. This is a keyword heuristic: expect a few misses both ways.
- `jobs_30d`, `distinct_titles_60d`, `hourly_distinct_titles_60d`, `cities`, `sample_titles`, `latest_job_url`.

### Result (ICP-fit = four verticals, 11+ employees)
| Bar | Companies |
|---|---|
| ICP-fit hiring at all | 473 |
| 2+ postings (any role) | 314 |
| 3+ postings (any role) | 225 |
| **2+ hourly postings** | **184** (retail 66, manufacturing 58, hospitality/F&B 37, warehousing 23) |
| 3+ hourly postings | 126 |
| 5+ hourly postings | 73 |

Excluded from those counts: 154 staffing companies, 9 dealerships and 689 out-of-ICP companies (health care, schools and so on). Construction with 2+ hourly postings: 12 more, held. Sanity check on location: the small out-of-region-HQ companies in the 2+ hourly set were eyeballed and are real Michiana sites (PEI-Genesis South Bend, Bull Moose Tube Elkhart, Alloy Fasteners "Alloy Indiana").

**Clay** was tried for the count (`search-companies` with `jobs.count(job_still_open = true and location contains (...)) >= 2`). Its job-location match is token-based ("IN" matched India) and returned SpaceX, Novartis and CGI with no total count, so it can't size a two-county area. It was not used.

## Part 2: Indeed jobs (Apify via GTM Sheets), in progress
GTM Sheets workbook **GigWorx C7 - Multiple Open Roles (sizing)** (`b8b23680-230f-4c31-a58d-8692c1368df4`, folder Clients / GigWorx). Tables:
- `1. Jobs - Indeed (Apify)` (`b38a1682-3222-42b0-8dce-c2411598940c`): actor `memo23/apify-indeed-cheerio-ppr`, 17 towns, `radius=0`, deep search, employer posts only, cap $15. Started 09:57 UTC; still running with 0 rows at 11:15 UTC.
- `1b. Jobs - Indeed (split by town x job type)` (`212d9278-428a-4129-b4c1-b4407dbf8e53`): same actor, 37 search URLs (4 big towns × job type + 13 small towns), cap $8. Started 10:23 UTC; still running.
- `1c. Jobs - Indeed (fast actor, split runs)` (`70ebdabf-fb7b-4c28-8aca-6d1cba3f8623`): actor `valig/indeed-jobs-scraper` (max 1,000 per run; an all-jobs search stops at about 500 results). 24 runs, cap $0.50 each: all jobs in 10 towns (South Bend, Mishawaka, Elkhart, Goshen, Nappanee, Middlebury, Bristol, Granger, New Carlisle, Wakarusa, each "<town>, IN" at the actor's default radius); South Bend and Elkhart posted in the last 14 days; keyword runs around South Bend/Elkhart (warehouse, production, assembly, cashier, cook, housekeeper, laborer, part time, temporary). 10,048 rows landed by 11:15 UTC.
- `0. Test - Indeed Nappanee` (103 rows) and `0. Preview - Indeed South Bend (50 jobs)`: previews only.
- `2. Companies - LinkedIn jobs (Blitz, 60d)` (`1c02028c-d32c-410b-a241-24599b242d8b`): the 314 ICP-fit companies with 2+ postings from Part 1, loaded by webhook, with a `Signal tier` column (A 5+ hourly, B 3-4, C 2, D 2+ jobs but under 2 hourly).

The Indeed merge (dedupe on Indeed job key, Indiana + target towns only, last 60 days, employers matched to LinkedIn by domain, name or Blitz `POST /v2/enrichment/domain-to-linkedin`, then `POST /v2/enrichment/company` for industry and size) lands as a separate commit with its own History entry.
