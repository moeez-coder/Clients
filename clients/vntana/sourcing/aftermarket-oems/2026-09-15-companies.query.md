# Query — 2026-09-15 companies snapshot (VNTANA Aftermarket OEMs, wide-net expansion)

**Tool:** Blitz API `POST /v2/search/companies`
**Purpose:** Repo owner asked to "cast as wide a net as possible" on this specific segment (Test 1 — Aftermarket 3D Parts Catalog) ahead of a large-volume lead push. This config had been stuck at its original 99-company DiscoLike pull from 2026-06 while every other VNTANA config had since grown into the hundreds/low-thousands — this pull brings it in line and well beyond.

**TAM/SAM note (per CLAUDE.md's outreach-depth rule):** this is now this client's largest single-segment TAM in the repo (16,771 total Blitz matches for the filter below, vs. low hundreds/thousands for every other VNTANA config) — a large TAM/SAM calls for casting wide across companies rather than going deep on contacts per company, which is exactly what "cast as wide a net as possible" asked for. The people-search pass on this pool accordingly used the same 1-2 contact per company ceiling as prior VNTANA rounds, not more.

**Request body (paginated, 200 pages × 50 = 10,000 raw, cursor not exhausted — 16,771 total matches, still a partial pull even at this scale):**

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
        "Communications Equipment Manufacturing",
        "Fabricated Metal Products", "Mining and Metals",
        "Motor Vehicle Manufacturing", "Motor Vehicle Parts Manufacturing",
        "Transportation Equipment Manufacturing", "Railroad Equipment Manufacturing",
        "Retail Building Materials and Garden Equipment", "Wholesale Building Materials",
        "Boilers; Tanks; and Shipping Container Manufacturing",
        "Construction Hardware Manufacturing",
        "Turned Products and Fastener Manufacturing",
        "Spring and Wire Product Manufacturing"
      ]
    },
    "employee_range": ["201-500", "501-1000", "1001-5000", "5001-10000", "10001+"],
    "hq": { "country_code": ["US", "CA", "GB", "DE", "AU", "FR", "IT", "SE", "NL", "MX"] }
  },
  "max_results": 50
}
```

**Filter design, mapped from the client's Test 1 ICP** (`tracking_clients.get_client` icpForm: Construction Equipment, Agricultural Machinery, Industrial Pumps & Valves, Heavy-duty Trucks, Mining Equipment, Material Handling, Industrial Automation) plus the config's own `nl_match` note ("Exclude distributors, process manufacturers, and aerospace/defense"):
- **Industry list** widened beyond the original config's exact industry names to every Blitz-normalized industry a discrete industrial-equipment/parts manufacturer with a dealer/aftermarket channel could plausibly carry (added Communications Equipment, Motor Vehicle/Parts, Transportation Equipment, Railroad Equipment, Building Materials retail/wholesale, Boilers/Tanks, Construction Hardware, Fasteners, Springs/Wire — all adjacent manufacturing categories with real spare-parts/aftermarket businesses).
- **Employee range** widened down to include `201-500` (previous VNTANA pulls started at `501-1000`) — capital-intensive manufacturers can clear the client's $100M+ revenue bar well below 500 employees.
- **Geography** widened to 10 countries (US, CA, GB, DE, AU, FR, IT, SE, NL, MX) — matches or exceeds the geo breadth already used for Casual Connections, appropriate for a segment explicitly asked to be cast as wide as possible.

**Result:** 10,000 raw pulled across two pagination runs (60 pages then 140 more from the returned cursor). Deduped against every company already in this repo (all 8 sourcing configs combined), the client's `tracking_clients.dncList`, and the accumulated bad-company/dealer/agency exclude list. **7,348 net-new companies** written to `2026-09-15-companies.csv` — brings this config's repo total from 99 to 7,447. 16,771 total companies match this filter in Blitz; still a partial pull (10,000 of 16,771 pulled) — a fresh cursor can pull the remaining ~6,771 in a future round.

**Not yet vetted at company level** beyond the DNC/bad-company/dealer-keyword exclude pass — at this volume, a full manual review wasn't feasible; the downstream people-search pass and its own manual scrub (see the leads `.query.md`) is where individual contamination gets caught, same pattern as every prior VNTANA round.
