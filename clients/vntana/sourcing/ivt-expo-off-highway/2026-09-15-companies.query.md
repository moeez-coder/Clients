# Query — 2026-09-15 companies snapshot (iVT Expo — Off-Highway Vehicle Technology, new segment)

**Tool:** Blitz API `POST /v2/search/companies`
**Purpose:** First company pull for VNTANA's iVT Expo config (previously 0 companies sourced). ICP targets off-highway vehicle OEMs/component suppliers (agricultural, construction, mining machinery), US/Canada, 501+ employees.

**Request body (paginated, 6 pages × 50 = 300 results, cursor not exhausted — 1,623 total matches, this is a partial pull):**

```json
{
  "company": {
    "industry": {
      "include": [
        "Motor Vehicle Manufacturing",
        "Motor Vehicle Parts Manufacturing",
        "Agriculture; Construction; Mining Machinery Manufacturing",
        "Automotive"
      ]
    },
    "employee_range": ["501-1000", "1001-5000", "5001-10000", "10001+"],
    "hq": { "country_code": ["US", "CA"] }
  },
  "max_results": 50
}
```

**Result:** 300 raw, 282 unique after dedup. 1,623 total matches — partial pull; re-run with a saved cursor to expand further.

**Note:** this filter is broader than the ICP's actual "off-highway vehicle" niche (it includes general Motor Vehicle/Automotive manufacturers) since Blitz's industry taxonomy has no off-highway-specific value — expect a meaningful fraction of on-highway/passenger-vehicle companies mixed in that don't actually fit. Not yet vetted at company or lead level.
