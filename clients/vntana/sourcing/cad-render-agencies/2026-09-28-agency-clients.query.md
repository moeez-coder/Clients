# Query — 2026-09-28 agency-clients snapshot (brands that hire CAD-to-render agencies)

**Ask (repo owner):** a list of the clients of the CAD-to-render agencies in `2026-09-28-companies.csv`, to pitch VNTANA to. Logic: a brand that already pays an agency to turn its CAD into renders, animations or 3D has the exact problem VNTANA automates, plus budget and a CAD library.

**Files:**
- `2026-09-28-agency-clients.csv`: **one row per client brand (2,997)**, ranked by `pitch_priority`. This is the pitch list.
- `2026-09-28-agency-client-links.csv`: **one row per (agency, client) link (3,415)**, each with `evidence_url` + verbatim `evidence_quote`. This is the audit trail behind every brand.
- `2026-09-28-scripts/`: the exact scripts used for this run and the companies snapshot (API keys come from env; none embedded).

**tracking_clients config:** none (new segment, no config UUID yet). **Keying:** these are companies, not people, so rule 3b's `linkedin_url` requirement doesn't apply. `company_linkedin_url` is `-` because it hasn't been resolved yet; resolve it (e.g. AI Ark `keyword` NAME/STRICT, or Blitz `domain-to-linkedin` once a domain is known) before pushing anything into a campaign.

## Method

1. **Agency pool:** agencies from `2026-09-28-companies.csv` with tier A/B, 11+ LinkedIn employees and a known domain → 800 agencies. Micro-freelancers were skipped because they rarely publish client names.
2. **EXA `POST /search`**, one call per agency: `includeDomains: [<agency domain>]`, query "our clients, brands we work with, case studies and portfolio projects", `numResults: 6`, `contents.highlights` (query "names of client companies and brands this studio has worked for", 3 sentences × 2 per URL). 687 of 784 in the first pass returned pages (~$4.81), plus 16 more for the EXA-discovered agencies. Each agency's own description (AI Ark/Blitz `about`) sentences mentioning clients/customers/"worked with"/"trusted by" were added.
3. **Extraction:** 10 parallel Claude (Sonnet) subagents read the evidence packs (743 agencies had evidence) and emitted only brand names **literally present** in the evidence. Knowledge-based additions were forbidden; tool vendors (KeyShot, Blender, SolidWorks…), award bodies, universities and partner ad agencies were excluded. Types: `stated_client`, `case_study` (page or URL slug names the company), `description`.
4. **Off-domain filter:** 48 rows dropped where the evidence URL wasn't on the agency's own domain. Some agencies' listed domain is a social page (facebook, linktr.ee, behance…), so EXA returned unrelated posts; for those, only `description` evidence is kept. **Result: 3,415 links, 493 agencies with ≥1 named client.**
5. **Brand dedupe:** client names normalised (case, accents, legal suffixes stripped) → 2,997 distinct brands. Variants like "Mercedes" and "Mercedes-Benz" still appear separately, since normalisation is conservative.
6. **Classification:** 4 Claude (Sonnet) subagents labelled each brand from general knowledge: `likely_company`, `vntana_segment`, `physical_product_maker`, `size_guess`, `classification_confidence`. **This is model judgement, not verified firmographics.** Low-confidence rows need a check. One subagent's output came back column-shifted (an extra index column and `client_name` dropped); it was remapped mechanically by key, and all 2,997 keys matched.
7. **Priority:**
   - **P1** = industrial equipment/machinery, automotive/mobility, building products/home, medical devices, other manufacturer; size enterprise or mid.
   - **P2** = CPG, consumer durables/electronics, fashion/footwear/apparel, furniture; size enterprise or mid. VNTANA sells here too (Adidas, PUMA, Patagonia…).
   - **P3** = those segments at small/unknown size, **plus** aerospace/defense-primary companies (Airbus, Boeing, General Dynamics…), which are an explicit VNTANA ICP disqualifier. They're downgraded with a note, not dropped.
   - **SKIP** = retailer / not_fit (restaurants, media, telecom, software…) / unknown.
   - **EXCLUDE** = on the `tracking_clients` `dncList` (20 brands incl. Sony, J&J, Kohler, Costco/Kirkland, Puma, Michael Kors, Knoll, Accenture) or an existing VNTANA customer named in the client brief/site (Adidas, Meta, Calvin Klein/Tommy Hilfiger (PVH), Hugo Boss, Armani, Vans (VF)). Matching uses whole company names; an earlier substring pass wrongly hit "Hofstetter Gastechnik" (astec), "Metaxa" (meta) and "Utsav Cotton" (cotton), and that pass was discarded.

## Result

356 P1 (industrial/machinery 111, automotive 102, building products 63, medical devices 41, other manufacturer 39), 581 P2, 619 P3, 1,421 SKIP, 20 EXCLUDE.

**Caveats:** (a) An agency listing a brand doesn't prove a *current* relationship. Case-study pages can be years old. (b) Big names (Toyota, BMW, Siemens) are real but enterprise-hard; the long tail of mid-size P1 manufacturers (e.g. Grundfos, Atlas Copco, Dynapac, Bucher, Balluff, Bürkert, Burckhardt Compression) is closer to VNTANA's stated sweet spot. (c) There's overlap risk with VNTANA's existing industrial pools: dedupe against `aftermarket-oems/`, `industrial-mfg-plm-cad/` etc. before any campaign push. (d) The strongest pitch angle is "your agency is already turning your CAD into renders by hand": the brand plus the agency that did it are both in the CSV.
