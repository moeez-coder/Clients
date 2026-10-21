# Query — 2026-10-21 modeled missing-image estimates for all 1,000 companies (deep-catalog-manufacturers)

Config `82d47d88-32b2-4dd8-8307-b12ac530aaf7`, campaign 6. **Expanding existing segment** (derived from `2026-10-21-companies-qualified-2.csv` + `2026-10-21-catalog-audit.csv`; no new pull). **Why:** owner asked for an estimate for every account so Message 1's `{number}` has a value everywhere. Script: `2026-10-21-scripts/estimate_missing.py`.

**These are ESTIMATES, not counts.** Nothing here was measured as missing images except `observed_placeholder_in_sample = yes` (33 companies, 6-page sample).

## Method
`est_missing = sku_count_used x gap_rate`, rounded to 2 significant figures.
1. **`sku_count_used`**, in priority order: (a) sitemap product-style URLs (>=50) and/or the count the company states on its own site; when both exist and are within 3x, their mean (confidence `high`), otherwise the lower one; (b) one source only (`medium`); (c) neither (540 companies): **modeled** as the median measured count among companies in the same product family and size band (fallback: size band) (`low`). Stated counts capped at 1,000,000 ("N million configurations" are variants, not imaged SKUs). Sitemap URLs may include non-SKU pages and can overstate.
2. **`gap_rate` scenarios**: low 2.7% = pooled share of sampled product pages with a real placeholder in the audit (103 of 3,881; a floor because 6-page samples under-detect); **mid 5% and high 10% are ASSUMPTIONS**, not measured. Replace with VNTANA's scorecard benchmarks when Ashley provides them.
3. `copy_phrase` = "roughly" + the mid estimate, to be used only with hedged wording ("roughly", "an estimated"), never as a flat count.

## Result
Confidence: high 29, medium 431, low 540. Median mid estimate 64 products; 90th percentile 390; largest are c3controls and Interpower (capped counts), then Magna-Power (stated 400,000 configurations), SKF and Lincoln Industrial (shared SKF sitemap of 286,162 URLs).

## Caveats
- 54% of rows are `low` (modeled from peers): treat as ballpark only; for those, prefer the no-number copy variant.
- The mid and high rates are not evidence-based. A wrong rate scales every number; do not send a specific figure until the benchmark is sourced.
- Parent/subsidiary sharing (SKF/Lincoln) and configuration counts inflate some rows; spot-check before any individual send.
