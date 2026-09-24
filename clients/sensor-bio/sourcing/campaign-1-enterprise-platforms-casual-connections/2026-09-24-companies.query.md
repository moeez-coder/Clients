# Query — Campaign #1 - Enterprise & Platforms (Casual Connections) (2026-09-24)

**Purpose:** Raw target universe (TAM), pulled **before qualification**, per user request ("complete target universe of Sensor Bio, before qualification"). This is a firmographic-match pull only — no ICP free-text qualifier or signal scoring has been applied yet.

**Tool:** Blitz API, `POST /v2/search/companies` (direct HTTPS call, `x-api-key` header — the `Blitz-API` MCP tool only searches Blitz's own docs, it does not proxy live requests).

**Filter used:**
```json
{
  "company": {
    "keywords": {"include": ["digital health", "remote patient monitoring", "health tech", "AI healthcare", "healthtech platform"]},
    "employee_range": ["51-200", "201-500"],
    "hq": {"country_code": ["US"]}
  },
  "max_results": 25
}
```

Filter maps to the ICP config `eb764c7c-13f0-4b7c-905b-816df3b7cae1` ("Campaign #1 - Enterprise & Platforms (Casual Connections)") in `tracking_clients`: US digital health / health tech / AI-in-healthcare / RPM platform companies, 51–500 employees. Used `keywords.include` (searched across description/specialties/NAICS-SIC/Crunchbase-G2 categories) rather than `industry.include` since this ICP spans several LinkedIn industry buckets (Hospital & Health Care, Computer Software, Medical Device, etc.) with no single clean industry match.

**Blitz-reported TAM size:** `total_results` = **4,305** companies matching this filter (indicative only — see the same Blitz accuracy caveat noted in the sibling query file for the Clinical & Health Systems pull).

**Update — 2026-09-24, same day:** re-ran to full completion per follow-up request ("I want the full universe completely"). Paginated all 173 pages (cursor → `null`) via a backgrounded shell loop. Final count: **4,302 unique companies** (vs. the 4,305 `total_results` estimate — same minor drift noted in the sibling query file). Full set saved to `2026-09-24-companies-FULL.csv`; the original `2026-09-24-companies.csv` (1,000-row sample) is left in place for reference/diff purposes.

**Overlap with the Clinical & Health Systems pull (same date):** 55 companies appear in both segment CSVs (e.g. large health systems that also show up under the digital-health keyword search) — expected given some accounts qualify for both Sensor Bio ICPs; not deduped across segments in these per-segment files.

**Not yet applied:** the ICP's free-text qualifier (funded digital health/RPM/AI health platform needing raw physiological data, excluding consumer fitness apps and companies with proprietary FDA-cleared sensor hardware) — that step has not been run against this list.
