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

**What's in this CSV:** the first **1,000 companies** (40 pages × 25, cursor-paginated, deduped by `company_linkedin_tag` — all 1,000 came back unique) returned by that filter, in Blitz's default result order (not obviously sorted by any qualification signal). This is a **sample of the 17,014-company TAM**, not the full enumeration — pulling the complete set would take ~680 more paginated calls. Re-run with the same filter and `cursor` continuation (see raw page files, not committed) to pull further.

**Not yet applied:** the ICP's free-text qualifier (multi-site system running/planning continuous monitoring or population health programs, no existing in-house sensor solution, etc.) — that step (company qualifier prompt, per `anthropic-skills:icp-qualification-new`) has not been run against this list.
