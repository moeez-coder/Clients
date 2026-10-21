# Query — 2026-10-21 companies snapshot, QUALIFIED stage (deep-catalog manufacturers)

Follows `2026-10-21-companies-wide.csv` (58,009; see its `.query.md`). Config `82d47d88-32b2-4dd8-8307-b12ac530aaf7`, campaign 6 "The Long Tail Nobody Photographed or Rendered" (`294e5e85…`). Owner instruction: "cast a wider net and then qualify the companies against it." Output: `2026-10-21-companies-qualified.csv`, **1,105 companies**, one row each, tiered. **New segment, first qualified list.**

## Funnel
| Stage | Method | In -> out |
|---|---|---|
| 0. Wide pool | Blitz + Prospeo + DiscoLike + EXA + AI Ark (partial), deduped | -> 58,009 |
| 1. Rule gates | Regex over name/industry/description/keywords: matches one of six product-family patterns (pumps & valves, hydraulics/fluid, fasteners/components, power transmission, industrial tools, electrical/automation) **or** has a missing-image site phrase; manufacturing evidence; not dealer/distributor/reseller-shaped; >=51 employees | -> 34,722 |
| 2. Candidate cut | A = catalog/missing-image signal (4,649); B = no signal, >=500 employees, US/CA/GB/IE/AU/NZ (1,228) | -> 5,877 |
| 3. Classification | 16 Claude (Sonnet) subagents x ~368 each judged type / product family / catalog depth / channel / keep Y-M-N from name, domain, industry, size, signals and description. Alignment checked on index + 12-char name echo: 0 misaligned (1 null-name row, N) | 5,877 -> 1,413 Y/M (Y 566 / M 847) |
| 4. Catalog evidence | EXA `POST /search`, `includeDomains:[own domain]`, query "<name> online product catalog number of products SKUs part numbers image coming soon distributor portal", 5 results, highlights; 1,395 had name+domain, 1,285 returned own-site pages; $8.99 | -> 1,395 |
| 5. Extraction | 10 Claude (Sonnet) subagents x ~140, each in its own scratch folder: stated SKU/product/part count (only if literally in evidence), quote, catalog type, configurator, missing-image text, depth. **Every stated-count quote is machine-checked as a (whitespace-normalised) substring of the evidence: 0 failures** | 1,395 rows |
| 6. Tiering + exclusions | Dropped: 278 whose site evidence read as shallow range, 11 distributor/reseller, 1 DNC (name+domain-brand match), 18 without usable domain/name | -> **1,105** |

## Tiers (`tier`)
- **L1_stated_1000plus (138)**: own site states >=1,000 products/SKUs/part numbers/variants/configurations; count + exact quote in `sku_count_stated` / `sku_count_quote`. Only rows where the "1,000+ SKUs" qualifier is proven. (`L1_placeholder_images_seen`, 2: site text shows "image coming soon" style text.)
- **L2_deep_catalog_evidenced (699)**: own site shows a large online catalog and/or distributor portal but publishes no count. Plausible, not proven.
- **L3 (113)**: catalog claimed but no channel evidence (16), or classifier said deep and EXA returned nothing for the domain (97).
- **L4_low_confidence (153)**: classifier Y/M but no deep-catalog evidence either way.

## Findings / caveats
- 780 of the 1,105 were already in the repo from earlier VNTANA pulls (`prev_sourced_in_repo`); check double-contacting. 730 are in US/CA/GB/IE/AU/NZ; many others are Chinese/Asian catalog makers. Filter on `country`.
- electrical_automation dominates (408), then fasteners (161), pumps/valves (149), power transmission (125), hydraulics/fluid (118), tools (109), other (36).
- "Stated count" is the company's own marketing wording ("over 90,000 standard parts", "20,000 products in 200,000 variants"), not an audited SKU count. Missing-image prevalence itself is **not verified** here (only 2 rows with literal placeholder text in the evidence); the campaign's "{{number}} products showing image coming soon" must be measured per prospect before sending.
- Size: Blitz headcount; 51-200 firms are not automatically under a revenue floor; no revenue gate applied (sparse).
- DNC list (21 domains, identical to `tracking_clients` dncList) matched by name tokens + domain-brand; 1 removed. Kenvue/Neutrogena question from earlier is not relevant to this segment.
- **AI Ark incomplete**: HTTP 402 "not enough credit" after ~966 companies (catalog 166, flow 800 of 3,635; fasteners/electrical/tools/power transmission 0). Top-up and re-run the keyword pull to extend the wide pool.
- Classification and extraction are model judgement over short text; spot-check before outreach. No contacts pulled (company list only).

## Spend
EXA $10.71 discovery + $8.99 catalog evidence; DiscoLike ~ $20 (month-to-date $46.29 per `GET /v1/usage` vs $26.28 recorded at the 2026-10-07 pull); Prospeo credits not measured; Blitz flat-rate; Claude subagents x 26. Scripts: `2026-10-21-scripts/` (API keys are read from environment, none stored).
