# Query — 2026-10-02 discrete-manufacturer check on the agency-clients list

**Ask (repo owner):** "out of these companies check which are discrete manufacturers". "These companies" = the 2,997 client brands in `2026-09-28-agency-clients.csv`. VNTANA's ICP requires a **discrete** manufacturer (not process: chemicals, food, pharma), per `tracking_clients` `get_client` icpForm and clientBrief.

**Output:** `2026-10-02-agency-clients-discrete.csv`, the same 2,997 brands with every column from the 2026-09-28 file plus `is_discrete_manufacturer` (yes / partly / no / unknown), `manufacturing_type` (discrete / mixed / process / not_manufacturer / unknown), `what_they_make`, `mfg_confidence`, `mfg_evidence_url` and `mfg_note`. Sorted discrete-first, then by `pitch_priority`. The 2026-09-28 file is untouched (append-only). **Segment:** same new CAD-to-render-agencies segment, no `tracking_clients` config (UUID `-`).

## Method

1. **Scope:** the 2,024 brands whose 2026-09-28 `physical_product_maker` was `yes` or `unknown`. The 973 tagged `no` (restaurants, media, telecom, software, etc.) are carried over as `not_manufacturer` and were **not re-checked**; their `mfg_note` says so.
2. **Web evidence: EXA `POST /search`**, one call per brand: query `"<likely_company or client_name> company — what it manufactures"`, `category: company`, `numResults: 2`, `contents.highlights` (query "what products does this company design and manufacture", 3 sentences × 2). Evidence came back for 2,022 of 2,024, at $14.15.
3. **Classification:** 10 parallel Claude (Sonnet) subagents, ~203 brands each, labelled each brand from the web evidence (general knowledge used only to interpret it):
   - *discrete* = countable assembled units built from a BOM, typically CAD-designed (machinery, vehicles, tools, electronics/appliances, furniture, fixtures, doors/windows/faucets, medical devices, footwear/apparel, toys, sporting goods).
   - *process* = formula/batch/continuous (food, beverages, chemicals, paints, pharma, cosmetics liquids, fuels, resin, paper, metals, cement, fertilizer, fabric).
   - *mixed* = material share of both (conglomerates, e.g. 3M, Tata, Abbott, Baxter).
   - *not_manufacturer* and *unknown* as named.
   Every one of the 2,024 rows came back and joined by exact `client_name`.
4. **ICP re-check:** P1 rows whose `what_they_make` names aircraft/jets/aerospace/defense were downgraded P1 → P3 (Bombardier, Cirrus Aircraft, HondaJet). Honda, Kawasaki and Mitsubishi Heavy Industries matched the regex but aren't aerospace-primary, so they keep P1.

## Result

| is_discrete_manufacturer | brands |
|---|---|
| yes (discrete) | **1,164** |
| partly (mixed) | 56 |
| no: process | 511 |
| no: not a manufacturer | 1,197 |
| unknown | 69 |

**Discrete × pitch priority:** P1 275 · P2 284 · P3 392 · SKIP 201 · EXCLUDE 12 (DNC/existing customers, still excluded). **The working pitch list is discrete + P1/P2 = 559 brands.** Discrete confidence: 664 high, 368 medium, 132 low.

201 discrete brands sit in SKIP, because the 2026-09-28 pass had `vntana_segment` = unknown for most of them. They're real discrete makers the first pass couldn't place; worth a look before discarding.

## Caveats

- Classification is model judgement over 2 web snippets per brand, not verified firmographics. Re-check `mfg_confidence = low` rows.
- **Name collisions:** EXA sometimes returned a different company with the same name. Several large brands came out `unknown` this way (e.g. Coach, Corona, Dove, Amazon Basics), and Lincoln, smart and Sanderson are low confidence. The agents flagged these in `mfg_note`.
- One agent (batch 0, the most-cited big brands) read full evidence for its first 24 rows and leaned more on general knowledge for the rest.
- Borderline calls (tyres, ceramic tile, roofing, carpet tile, precast concrete, packaging) split between discrete and process by agent; treat them as judgement calls.
- Size and segment columns still come from the 2026-09-28 pass. Only manufacturing type was re-checked here.
- Scripts: `2026-09-28-scripts/exa_mfg.py` + `build_discrete.py` (the folder name keeps the segment's first pull date).
