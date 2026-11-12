# Query — 2026-09-15 companies snapshot (Casual Connections, new segment)

**Tool:** Blitz API `POST /v2/search/companies`
**Purpose:** First company pull for VNTANA's Casual Connections config (previously 0 companies sourced). Used the same core industrial-machinery industry set as Industrial Mfg PLM/CAD, but widened to match this ICP's broader geo (US, Canada, UK, Germany, Australia) and broader size band (501+ employees, matching the ICP's `company_sizes: 501-1000, 1001-5000, 5001-10,000, 10,000+`).

**Request body (paginated, 8 pages × 50 = 400 results, cursor not exhausted — 2,645 total matches, this is a partial pull):**

```json
{
  "company": {
    "industry": {
      "include": [
        "Industrial Machinery Manufacturing", "Machinery Manufacturing", "Machinery",
        "Automation Machinery Manufacturing", "Industrial Automation",
        "Agriculture; Construction; Mining Machinery Manufacturing",
        "Engines and Power Transmission Equipment Manufacturing",
        "Electric Power Transmission; Control; and Distribution",
        "Metal Valve; Ball; and Roller Manufacturing",
        "Commercial and Service Industry Machinery Manufacturing",
        "Fabricated Metal Products", "Mining and Metals"
      ]
    },
    "employee_range": ["501-1000", "1001-5000", "5001-10000", "10001+"],
    "hq": { "country_code": ["US", "CA", "GB", "DE", "AU"] }
  },
  "max_results": 50
}
```

**Result:** 400 raw, 372 unique after dedup. 2,645 total companies match this filter — this is a partial pull (first 400); re-run with a saved cursor to expand further.

**Not yet vetted at company level** for the agency/reseller/service-provider contamination documented in the Industrial Mfg PLM/CAD segment's history — only leads actually pushed to a campaign have been individually checked.
