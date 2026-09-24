# Query — Sensor Bio - Clinical & Health Systems (2026-09-24)

**Purpose:** Raw target universe (TAM), pulled **before qualification**, per user request ("complete target universe of Sensor Bio, before qualification"). This is a firmographic-match pull only — no ICP free-text qualifier or signal scoring has been applied yet.

**Tool:** Blitz API, `POST /v2/search/companies` (direct HTTPS call, `x-api-key` header — the `Blitz-API` MCP tool only searches Blitz's own docs, it does not proxy live requests).

**Filter used:**
```json
{
  "company": {
    "industry": {"include": ["Hospitals", "Hospitals and Health Care", "Hospital and Health Care"]},
    "employee_range": ["201-500", "501-1000", "1001-5000"],
    "hq": {"country_code": ["US"]}
  },
  "max_results": 25
}
```

Filter maps directly to the ICP config `f007b949-38ad-4e03-adb7-e1e33f65baef` ("Sensor Bio - Clinical & Health Systems") in `tracking_clients`: US health systems/hospitals, 201–5000 employees.

**Blitz-reported TAM size:** `total_results` = **17,014** companies matching this filter (per Blitz's own count — treat as indicative, not exact; Blitz's `total_results` has disagreed with itself by up to ~6× on identical filters in prior pulls for this repo, see `clients/vntana/icp-universe-map.md` §6, and its industry tagging is noisy).

**Update — 2026-09-24, same day:** re-ran to full completion per follow-up request ("I want the full universe completely"). Paginated all 681 pages (cursor → `null`) via a backgrounded shell loop. Final count: **16,999 unique companies** (one fewer than the 17,014 `total_results` figure — Blitz's own count drifted slightly between the initial estimate and full pagination, consistent with the accuracy caveat above). Full set saved to `2026-09-24-companies-FULL.csv`; the original `2026-09-24-companies.csv` (1,000-row sample) is left in place for reference/diff purposes.

**Not yet applied:** the ICP's free-text qualifier (multi-site system running/planning continuous monitoring or population health programs, no existing in-house sensor solution, etc.) — that step (company qualifier prompt, per `anthropic-skills:icp-qualification-new`) has not been run against this list.
