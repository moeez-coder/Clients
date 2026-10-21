# Query — 2026-10-21 companies snapshot, WIDE stage (deep-catalog manufacturers)

**Segment:** new segment, first pull. **tracking_clients config:** `82d47d88-32b2-4dd8-8307-b12ac530aaf7`; ICP `cc641d39…`; campaign "6. The Long Tail Nobody Photographed or Rendered" (`294e5e85…`).
**Ask (repo owner):** "Find me list of companies for this" then "Use all necessary tools. Cast a wider net and then qualify the companies against it."
**Target:** manufacturers with deep configurable catalogs or very high-volume consumable parts (1,000+ SKUs / 50+ variants per family), sold via web catalog or distributor/dealer portal: pumps & valves, hydraulics, power transmission, fluid control, fasteners & components, industrial tools, electrical & automation components.

## Sources (58,009 unique companies after dedupe on company LinkedIn URL / registrable domain; 57,301 with LinkedIn)
| Tool | Endpoint | Run | Rows |
|---|---|---|---|
| Blitz API | `POST /v2/search/companies` | 216 slices: 6 groups (flow, fasteners, electrical, tools, power transmission, catalog keywords) x 6 employee bands x 6 country groups | 60,546 raw |
| Prospeo API | `POST /search-company` | NAICS groups (pumps/valves/fluid, fasteners/hardware, tools, power transmission, electrical/automation) x 8 headcount bands, plus keyword x industry slices | 18,861 raw |
| DiscoLike API | `GET /v1/discover` | site `phrase_match` for missing-image phrases ("image coming soon", "no image available", ...) across 12 categories x 5 geo groups, plus catalog phrases ("part number", "add to cart", "distributor portal", "download cad", ...); employee_range 51+ | 6,550 raw |
| EXA | `POST /search` | 116 discovery queries (11,062 results, $10.71) -> 5,446 domains, 4,102 new, 3,649 resolved via Blitz `/v2/enrichment/*` | 3,649 net-new |
| AI Ark API | `POST /v1/companies` | keyword WORD-mode on DESCRIPTION/SEO/KEYWORD x industries, 51+ employees. **Stopped by HTTP 402 "not enough credit" after ~966 companies** (catalog 166, flow 800 of 3,635; fasteners/electrical/tools/power transmission got 0). Needs a top-up to complete. | ~966 |
| Repo | 2026-10-07 dealer-network wide pool | 19,273 flow/hydraulics/power-equipment rule matches re-used | n/a |

## Columns
`catalog_signals` = flags from sources (e.g. `site_image_placeholder_phrase` = DiscoLike saw a missing-image phrase on the company's own site; `site_catalog_phrase`; `catalog_text_*`; `blitz:<group>`). `candidate_group`: A = catalog/image-gap signal, B = no signal but >=500 employees in US/CA/GB/IE/AU/NZ, `-` = did not pass the rule gates. Wide is unvetted by design (includes distributors, dealers, non-targets). Blitz `total_results` not trusted; counts are rows returned.

## Next stages (separate dated files)
Rule gates (vertical or image signal, manufacturing evidence, not dealer-shaped, >=51 employees) -> 5,877 candidates -> Claude classification (16 subagents, ~368 each) -> EXA per-domain catalog evidence -> extraction with verbatim-quote verification -> tiering -> `…-companies-qualified.csv`.
