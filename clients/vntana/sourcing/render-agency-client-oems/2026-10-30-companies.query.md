# Query — 2026-10-30 companies snapshot (Render campaign accounts: product, category, demo)

**Segment:** **new segment** for sourcing in this repo; accounts come from the existing cad-render-agencies work. **tracking_clients config:** `Industrial OEMs paying an outside render agency, with recent launch / show / PIM project`, UUID **`7166f187-d30d-4d52-86be-79ba8f4f3dbf`** (draft, 1 campaign, 0 companies at pull time); ICP `a7aefe3e-c465-4e61-9ace-bd5c6c4b1632`. **Feeds:** the HeyReach campaigns `693232` (Offer 1 Cost+Speed) and `693233` (Offer 2 Conversion), cloned from the approved "The Render You're Stuck With" (`661048`).
**Ask (repo owner):** "Do research for product and category of each account", and choose the demo link from `https://vntana-store-production.up.railway.app/index.html`.

## Accounts (158)
From `cad-render-agencies/2026-10-07-agency-clients-discrete-2.csv` (brands that appear as clients of CAD-to-render agencies): `is_discrete_manufacturer` yes/partly, `pitch_priority` P1/P2, segment industrial_equipment_machinery, building_products_home or other_manufacturer (owner chose this "industrial render-agency clients" scope over all 601 P1/P2 brands). Dropped: 1 aerospace/defense-primary; 0 on the DNC list. Consumer, fashion, automotive, furniture and medical brands are out of scope.

## Research
1. **EXA `POST /search`** per account (158 calls, $1.11): query "<company> launches new product <what they make>", 6 results, `startPublishedDate 2025-10-01`, highlights; fallback to an undated "flagship product range" query when fewer than 2 results.
2. **4 Claude (Sonnet) subagents x ~40**, each in its own scratch folder, picked `product` (named, recent, only from the evidence), `category` (generic singular noun phrase for "a {category} built from CAD") and a `demo_key`. **Every `product_quote` is machine-checked as a substring of the EXA evidence: 0 failures.** Confidence: high 133, medium 13, low 12 (no product found; same-name company collisions e.g. Magnet, Surya, Tata Cummins).
3. **Demo choice** (`demo_key` -> `demo_link`, all verified HTTP 200 on 2026-10-30): skid_steer -> `/custom/skid-steer-explorer`; crane -> `/custom/tadano-crane-explorer.html`; sunsource -> `/custom/sunsource` (hydraulic/electronic components); hvac_pump -> `/custom/taco-007e.html`; machine_tools -> `/custom/imts`; components -> `/custom/imts-consumables`; parts_catalog -> `/custom/parts`; process -> `/custom/roeslein-adb.html`; viewer (default) -> `/custom/product?uuid=ca4aebfc-...&org=DCicero&workspace=example-files` (custom viewer with camera presets and lighting, the closest match to "pick any angle, change the finish, export the image").

## Company LinkedIn pages
Domain via EXA company search, LinkedIn page via Blitz `/v2/enrichment/domain-to-linkedin`, plus Blitz `POST /v2/search/companies` name search. A first pass resolved some accounts to the wrong entity (Grohe -> Groupe AXOR, Rittal -> Rittal India, Husqvarna -> Husqvarna UK, Tata Cummins -> LinkedIn itself); pages are now accepted only if the page name's tokens are covered by the account's own name or the domain matches, max 3 pages per account (`all_company_pages`). **134 of 158 have a verified page; 24 have none** (company_linkedin_url `-`).

## Columns / readiness
`render_copy_ready = yes` only when a product was found with high/medium confidence, the evidence is dated 2025-10-01 or later or says new/launch, and a company page exists (121 accounts). Otherwise `review`: the approved copy ("congratulations on {product}") needs a recent named product. `leads_found` = contacts in `2026-10-30-leads.csv`.

## Caveats
- Product and category are model reads of short web snippets; spot-check before sending. Some products are loose (e.g. "17 Next-Generation Trucks" for Tata Group, a German phrase for Aker).
- Several accounts are large groups (Siemens, ABB, Bosch, Assa Abloy, Atlas Copco): one named product stands for a very large company.
- Scripts: `2026-10-30-scripts/` (keys read from the environment, none stored). Spend: EXA $1.11; Blitz flat-rate.
