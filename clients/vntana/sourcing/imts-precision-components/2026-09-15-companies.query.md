# Query — 2026-09-15 companies snapshot (IMTS 2026 — Precision Components, Instruments & Consumables, new segment)

**Tool:** Blitz API `POST /v2/search/companies`
**Purpose:** First company pull for this config (previously 0 companies sourced).

**Request body (1 page, cursor exhausted at 20 total raw results across this query and the Machine Tools/Robotics query below — split by returned `industry` field):**

```json
{
  "company": {
    "industry": { "include": ["Measuring and Control Instrument Manufacturing", "Metalworking Machinery Manufacturing", "Robotics Engineering", "Robot Manufacturing"] },
    "employee_range": ["501-1000", "1001-5000", "5001-10000", "10001+"],
    "hq": { "country_code": ["US", "CA"] }
  },
  "max_results": 50
}
```

**Result:** this file holds the subset tagged `Measuring and Control Instrument Manufacturing` or `Metalworking Machinery Manufacturing` (8 rows) — the small total (20 combined with the Robotics/Machine Tools split) suggests this narrow industry combination under-covers the real precision-components/instruments/consumables market; worth broadening the industry list or adding a keyword filter in a future pull. Not yet vetted at company or lead level.
