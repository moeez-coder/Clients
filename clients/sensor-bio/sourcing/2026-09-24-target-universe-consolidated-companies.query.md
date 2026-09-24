# Query — Consolidated target universe (2026-09-24)

**Purpose:** Single deduped CSV of all potential target companies across both Sensor Bio ICPs, per user follow-up request ("one consolidated CSV of all potential target companies").

**Superseded — see `2026-09-24-target-universe-FULL-companies.csv` instead.** This file was the first pass (1,945 companies, built from 1,000-row samples of each segment). Per follow-up requests ("I want the full universe completely" / "Include companies pull from clay as well"), it was superseded same-day by the FULL file below, which uses complete Blitz enumeration plus a Clay supplement. Left in place for reference/diff purposes only — do not treat as current.

---

## FULL universe (superseding pull, same day)

**File:** `sourcing/2026-09-24-target-universe-FULL-companies.csv` — **21,122 unique companies**.

**Source 1 — Blitz API, fully paginated to completion:**
- `sourcing/sensor-bio-clinical-health-systems-custom/2026-09-24-companies-FULL.csv` — 16,999 companies (all 681 pages, cursor → `null`)
- `sourcing/campaign-1-enterprise-platforms-casual-connections/2026-09-24-companies-FULL.csv` — 4,302 companies (all 173 pages, cursor → `null`)

**Source 2 — Clay (`mcp__Clay__search-companies` / `load-more-search-results`), supplementary:**
Pulled 3 pages (60 companies total: 2 pages / 40 companies for Clinical & Health Systems via `industry in ("Hospitals and Health Care")` + `employee_count` range; 1 page / 20 companies for Enterprise & Platforms via `description contains "digital health"` + `employee_count` range). Clay's DSL has **no HQ/country filter** (`hq_country`, `country` both rejected as unknown fields) — results span many countries and were filtered to US HQ client-side after the fact. Of 60 raw Clay results, **20 were US-HQ'd**; of those, **6 were net-new** (not already present in the Blitz pull) and were added — see `source` column (`Blitz API`, `Clay`, or `Blitz API + Clay` where both tools surfaced the same company).

**Why Clay wasn't fully paginated:** Clay's `search-companies`/`load-more-search-results` never discloses a total result count — `hasMore: true` keeps returning indefinitely with no visible end (unlike Blitz's cursor, which reaches `null`). Pagination is also strictly sequential (each page requires the prior page's `taskId`) and expensive (~10–15K tokens per 20-company page, since Clay returns full company descriptions rather than compact records). Observed US-match yield across the pages pulled was only ~30% (10–11 of ~20 per page), and this repo's own standard already documents Clay's role here: *"Single-company enrichment and Company Competitors; not a bulk sizing tool"* (see `CLAUDE.md` → Sourcing tools). Given no terminable end state and low yield, pagination was capped rather than run unbounded — flagged to the user, who has not yet confirmed whether to extend it further.

Deduped by `company_linkedin_tag` across both sources and both ICP segments. 55 companies matched both Blitz segment pulls; `icp_segments` lists all matching segment names (`|`-separated) for any company appearing in more than one.

**Not yet applied:** the ICP qualifier/scoring step for either segment — this is still the raw pre-qualification universe.
