# Glassdoor bad-review campaign: ICP company pool (2026-11-17)

- **What:** every UK-HQ company with 201+ employees in doc 1's five sectors, from Blitz, with DNC and Campaign 6 companies marked excluded. This is stage 1 of the campaign's funnel (1 Companies → 2 Glassdoor ratings/reviews → 3 bad-review companies → 4 leads). **No Glassdoor scraping has happened yet.**
- **Client:** We Are DNA, tracking_clients `f5ff426b-c514-4a64-91b0-0e141a6a0669`.
- **Config / campaign:** none yet in tracking_clients (UUID `-`). Scope: **Campaign-specific: Glassdoor bad-review outreach** (set by Moe's brief of 2026-11-17, which defines the campaign).
- **Segment:** **new segment** (a reputation signal across all five sectors), not an expansion of Campaign 6.
- **Session:** session_013MzxQfnKsdVbThAsX3zi7V.

## Why these firmographics

- **Sectors:** doc 1's five (health/care/vet, retail/hospitality, manufacturing/engineering, law/accounting, financial services), which Moe approved on 2026-11-12. Blitz industry labels (legacy + current names) are copied verbatim from `../tam/tam_counts.py` `SEGMENTS`, so this pool lines up with the doc 1 TAM read.
- **UK HQ** (`hq.country_code: ["GB"]`): the ICP form's geography.
- **201+ employees:** below that, few UK employers have enough Glassdoor reviews for a rating to mean anything, and a "minimum review count" rule would drop most of them anyway. The form's floor is 51; 51–200 is left out deliberately. Which size bands actually get scraped is a cost decision for Moe (see below).

## Exact query

`pull_companies.py` (Blitz API `POST /v2/search/companies`), one query per sector × size band, `max_results: 25`, paged until the response cursor is null:

```json
{"company": {"industry": {"include": ["<sector labels from tam_counts.py>"]},
             "employee_range": ["<band>"], "hq": {"country_code": ["GB"]}},
 "max_results": 25, "cursor": null}
```

Bands: `201-500`, `501-1000`, `1001-5000`, `5001-10000`+`10001+`. Every slice is far under Blitz's 50k cap, and each slice's row count matched its `total_results` exactly (per-slice counts are in the run log below and in `gd_counts.json`, from `gd_counts.py`, a count-only pre-check).

Raw responses: `2026-11-17-companies-blitz-raw.jsonl.gz` (one line per record with its segment and band; `gzip -9` after the pull). `build_companies.py` turns that into `2026-11-17-companies.csv` and reproduces it byte for byte.

**Blitz records used: 11,869** (11,854 for the pull, 15 for the count pre-check). Blitz fair usage showed 13.59M records remaining.

## Exclusions (rows kept with a `status`, not deleted)

| Rule | How matched | Rows |
|---|---|---|
| DNC (`context/dnc-list.csv`, 143 companies from tracking_clients) | domain (host without `www.`) or normalised name | 58 |
| Campaign 6 (all 280 candidates in `../pe-investment-triggers/2026-11-16-companies-qualified.csv` plus every company in `2026-11-16-3-leads.csv`) | company LinkedIn slug or normalised name | 82 |
| **ICP (`status = icp`)** | | **11,714** |

- Domain matching catches DNC subsidiaries that share a parent domain (e.g. several Gallagher brokers, RSM UK units, Medivet branches). That is intended: the DNC names the group.
- A few Campaign 6 **name** matches are generic ("George and Dragon", "Bounce", "Cornerstone") and may be different companies. Left excluded: over-excluding is the safe direction.
- The other 85 DNC companies didn't match because they're outside these sectors or under 201 employees.

`public_sector = yes` (name or company type: NHS, council, police, university, ministry, etc.): **695 of the ICP rows**. Flagged, not dropped. Recommendation: leave them out of the scrape (Glassdoor outreach to NHS trusts is a different sale, and doc 1 excludes NHS bodies by default); Moe decides.

## Result (ICP rows, private sector, 11,019)

| Size band | Companies |
|---|---|
| 201-500 | 5,809 |
| 501-1000 | 2,090 |
| 1001-5000 | 1,937 |
| 5001-10000 | 408 |
| 10001+ | 775 |

By first sector: retail/hospitality 3,220; manufacturing/engineering 2,741; financial services 2,317; health/care/vet 1,999; law/accounting 742.

## Known noise (eyeballed a random sample)

- Blitz domains are sometimes wrong: `bit.ly`, a security vendor's domain on a wealth manager, `toyota.co.uk` on a dealer group. **599** private ICP rows have a blank or link-shortener domain. So Glassdoor resolution must not rely on domain alone: match on name, check against domain where it looks real, and flag low-confidence matches.
- Some records are junk (e.g. a "10001+" investment firm with no domain). The Glassdoor lookup will drop most of these (no employer page or too few reviews).

## Clay

Clay was **not** run for this pool, contrary to the usual Clay + Blitz pairing. Clay's MCP `search-companies` returns 20 rows a page with no total, so pulling ~11.9k companies through it isn't practical in this session, and Blitz's slices were exhaustive (each slice returned its full `total_results`). If Moe wants Clay coverage, run it on the slice chosen for scraping and merge on company LinkedIn URL.

## Run log

```
1-health-care-medical 201-500 1205 | 501-1000 461 | 1001-5000 524 | 5001+ 395
2-retail-hospitality 201-500 1666 | 501-1000 613 | 1001-5000 609 | 5001+ 392
3-manufacturing-engineering-automotive-defence 201-500 1472 | 501-1000 514 | 1001-5000 504 | 5001+ 316
4-law-accounting-top100 201-500 409 | 501-1000 163 | 1001-5000 141 | 5001+ 77
5-financial-services 201-500 1235 | 501-1000 442 | 1001-5000 449 | 5001+ 267
records_used 11854
```
