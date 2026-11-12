# Query — 2026-09-15 companies snapshot (Industrial Mfg PLM/CAD, expansion)

**Tool:** Blitz API `POST /v2/search/companies`
**Purpose:** Expand the existing Industrial Mfg PLM/CAD segment (previously 284 companies from the first page) to cover the rest of the ~903 total matches, so the "General" HeyReach quadset has a large combined-TAM/SAM pool to source leads from.

**Request body (paginated via `cursor`, 18 pages × 50 = up to 900 results):**

```json
{
  "company": {
    "industry": {
      "include": [
        "Industrial Machinery Manufacturing",
        "Machinery Manufacturing",
        "Machinery",
        "Automation Machinery Manufacturing",
        "Industrial Automation",
        "Agriculture; Construction; Mining Machinery Manufacturing",
        "Engines and Power Transmission Equipment Manufacturing",
        "Electric Power Transmission; Control; and Distribution",
        "Metal Valve; Ball; and Roller Manufacturing",
        "Commercial and Service Industry Machinery Manufacturing",
        "Fabricated Metal Products",
        "Mining and Metals"
      ]
    },
    "employee_range": ["1001-5000", "5001-10000", "10001+"],
    "hq": { "country_code": ["US", "CA"] }
  },
  "max_results": 50
}
```

**Result:** 900 raw records returned (cursor exhausted at page 15, i.e. the full ~903-match set), 817 unique after dedup by domain/LinkedIn URL, 533 of those not already present in the 2026-09-14 snapshot (284 companies) — those 533 are what's in this file. The other 284 are duplicates of the prior pull and were dropped, not re-saved.

**Known caveat (see VNTANA README "Sourced data" section and History):** this same industry-based filter previously turned out to include some marketing agencies, resellers, and consultancies mixed in with real manufacturers (caught during lead-level QC on the 2026-09-14 Open Check push). That same contamination risk applies to this larger pull and has **not** been re-vetted at the company level — only at the lead level, for the subset of companies that actually produced a lead in the 2026-09-15 people-search pass below.
