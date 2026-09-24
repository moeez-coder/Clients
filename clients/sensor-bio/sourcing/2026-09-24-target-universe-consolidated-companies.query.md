# Query — Consolidated target universe (2026-09-24)

**Purpose:** Single deduped CSV of all potential target companies across both Sensor Bio ICPs, per user follow-up request ("one consolidated CSV of all potential target companies").

**Superseded — see `2026-09-24-target-universe-FULL-companies.csv` instead.** This file was the first pass (1,945 companies, built from 1,000-row samples of each segment). Per follow-up requests ("I want the full universe completely" / "Include companies pull from clay as well"), it was superseded same-day by the FULL file below, which uses complete Blitz enumeration plus a Clay supplement. Left in place for reference/diff purposes only — do not treat as current.

---

## FULL universe (superseding pull, same day)

**File:** `sourcing/2026-09-24-target-universe-FULL-companies.csv` — **21,138 unique companies**.

**Source 1 — Blitz API, fully paginated to completion:**
- `sourcing/sensor-bio-clinical-health-systems-custom/2026-09-24-companies-FULL.csv` — 16,999 companies (all 681 pages, cursor → `null`)
- `sourcing/campaign-1-enterprise-platforms-casual-connections/2026-09-24-companies-FULL.csv` — 4,302 companies (all 173 pages, cursor → `null`)

**Source 2 — Clay (`mcp__Clay__search-companies` / `load-more-search-results`), fully paginated to completion:**
Two DSL queries, each paginated to `hasMore: false` (confirmed via `get-current-workspace`: connected to the live `algoacqusition` workspace, `770250` — the same workspace as Sensor Bio's Clay workbooks):
- Clinical & Health Systems: `industry in ("Hospitals and Health Care")` + `employee_count` 201–5000 → **100 companies, exhausted after 5 pages**
- Enterprise & Platforms: `description contains "digital health"` + `employee_count` 51–500 → **100 companies, exhausted after 5 pages**

200 raw Clay results total. Clay's DSL has **no HQ/country filter** (`hq_country`, `country`, `state`, `locality`, `headquarters_country` all rejected as unknown fields — only `industry`, `employee_count`, `annual_revenue`, `total_funding_amount_range_usd`, `type`, `description`, `domain`, `name` appear to be real filterable fields) — results span many countries (UAE, Brazil, Saudi Arabia, India, etc. dominate) and were filtered to US HQ client-side after the fact. Of 200 raw Clay results, **63 were US-HQ'd**; of those, **22 were net-new** (not already present in the Blitz pull) and were added — see `source` column (`Blitz API`, `Clay`, or `Blitz API + Clay` where both tools surfaced the same company).

*(Earlier note in this file said Clay pagination never terminates — that was based on stopping after only 3 pages per query. Continuing both queries to completion showed `hasMore` does resolve to `false`, just later than Blitz's per-page density suggested. Correcting the record here rather than deleting the wrong claim.)*

Deduped by `company_linkedin_tag` across both sources and both ICP segments. 55 companies matched both Blitz segment pulls; `icp_segments` lists all matching segment names (`|`-separated) for any company appearing in more than one.

**Not yet applied:** the ICP qualifier/scoring step for either segment — this is still the raw pre-qualification universe.
