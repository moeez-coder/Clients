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

## Part 2: Indeed jobs (Apify via GTM Sheets) and the merged count

GTM Sheets workbook **GigWorx C7 - Multiple Open Roles (sizing)** (`b8b23680-230f-4c31-a58d-8692c1368df4`, folder Clients / GigWorx).

### Indeed runs
- **Used:** `1c. Jobs - Indeed (fast actor, split runs)` (`70ebdabf-fb7b-4c28-8aca-6d1cba3f8623`), actor `valig/indeed-jobs-scraper`, 24 runs at $0.50 cap each (about $0.0001 per job):
  - all jobs, each at the actor's default radius: South Bend, Mishawaka, Elkhart, Goshen, Nappanee, Middlebury, Bristol, Granger, New Carlisle, Wakarusa (all ", IN");
  - last 14 days: South Bend, Elkhart;
  - keyword runs: warehouse, production (both towns), assembly, laborer, temporary (Elkhart), cashier, cook, housekeeper (South Bend), part time (both).
  - 11,213 rows landed. Only **2,096 distinct job keys**: Indeed stops a search at about 500 results, and the overlapping radius searches return the same top results.
  - Of those, 1,010 are in the 17 target towns (state IN) and posted in the last 60 days: `2026-11-17-c7-indeed-jobs.csv`. The rest are outside the two counties (Michigan City, Valparaiso, Warsaw, Fort Wayne, ...) or older.
  - Export: GTM's `export_path` needs dashboard login, so rows came out through `gtm_sheet_export_csv` filtered on `State = IN` and `Published` month (Sep, Oct, Nov). Do not filter on a formula column until it has finished computing: a first export filtered on the `Town` formula returned only the ~2,700 rows computed so far.
- **Still running at commit time, not used:** `1. Jobs - Indeed (Apify)` (`b38a1682-3222-42b0-8dce-c2411598940c`, `memo23/apify-indeed-cheerio-ppr`, 17 towns with deep search, cap $15, started 09:57 UTC) and `1b. Jobs - Indeed (split by town x job type)` (`212d9278-428a-4129-b4c1-b4407dbf8e53`, same actor, 37 URLs, cap $8, started 10:23 UTC). No rows after 75+ minutes. If they land, rerun `merge.py` with their export added.
- Previews: `0. Test - Indeed Nappanee` (memo23, 103 rows) and `0. Preview - Indeed South Bend (50 jobs)`.

**Coverage verdict:** Indeed adds hourly roles LinkedIn misses (e.g. Forest River Inc. with 13 distinct hourly roles on Indeed only, Four Winds Casinos, Lozier, Elkhart Plastics), but this pass is capped by Indeed's ~500-per-search limit. It is a top-up, not a complete Indeed census. More keyword splits would raise it.

### Merge (`merge.py`)
1. Indeed jobs deduped on job key; kept if state IN, town in the 17-town list, posted within 60 days.
2. Indeed employer to company: employer website domain matched to the Blitz companies, else normalised name, else Blitz `POST /v2/enrichment/domain-to-linkedin`; new companies enriched with `POST /v2/enrichment/company` (132 calls) for industry and size.
3. Per company, roles are counted as **distinct job titles** across both boards (the same role posted on LinkedIn and Indeed, or reposted, counts once). Hourly/shift classification uses the same regex as `classify.py`.
4. Same ICP filter as Part 1. 22 Indeed employers had no industry; 15 of them were judged likely fit by hand (Forest River Bus, Masterbilt, Godfrey, Jamil Packaging, Hiler Industries, Tramec, Villa International, Heartland Footwear, Star Nova, AAYS Event Rentals, Rise n Roll Bakery, Papa Vino's, Bennetts, T.J.Maxx, Pet Supplies Plus) and are marked `icp_fit = review`; the other 7 (senior care, county government, landscaping, concrete, a liquor store) are out.

### Result: `2026-11-17-c7-merged-hiring-companies.csv` (1,650 hiring companies)
| Bar (ICP-fit, distinct roles, last 60 days) | Fit | + Review | Total |
|---|---|---|---|
| 2+ open roles of any kind | 308 | 15 | **323** |
| **2+ hourly/shift roles** | **174** | 15 | **189** |
| 3+ hourly/shift roles | 100 | 6 | 106 |
| 5+ hourly/shift roles | 44 | 0 | 44 |

2+ hourly by vertical (fit only): manufacturing 66, retail 54, hospitality/F&B 37, warehousing 17. Seen on: LinkedIn only 84, both boards 77, Indeed only 13.

Why the 2+ hourly number (174) is lower than Part 1's 184: Part 1 counted raw postings; this counts distinct titles, which removes reposts and duplicates. Indeed then adds companies back.

GTM table `3. Companies - merged LinkedIn + Indeed (60d, 2+ roles)` (`931ec6d5-d86b-4bc5-9f3a-25b8455c8b25`) holds the 323 fit + review rows, loaded by webhook. `2. Companies - LinkedIn jobs (Blitz, 60d)` (`1c02028c-d32c-410b-a241-24599b242d8b`) is the earlier LinkedIn-only version.

Known limits: hourly classification is a title regex; a company's LinkedIn and Indeed records can occasionally resolve to two LinkedIn pages (e.g. Lowe's); Blitz job location has no state field, so a few homonym towns may slip in (spot-checked, rare).
