# Query — New Leader, Old Portfolio, segment 4(b), 2026-09-21

**Campaign 4, segment (b)** — PE-backed device/diagnostics roll-up platforms, $100M-$1B, 2+ add-on
acquisitions not yet consolidated under one brand. Distinct from 4(a) (multi-BU public/large-cap
companies), sourced separately in `2026-09-21-companies.csv`.

**Why this needed a different tool:** "PE-backed" + "has absorbed 2+ acquisitions" is an
ownership/M&A-history fact, not a firmographic filter. Two keyword-search attempts on Blitz
(`"acquisition"`, `"roll-up"`, `"platform company"`, `"add-on"` + industry filter) returned only 4-5
generic hits — individual acquired subsidiaries mentioned in their own "about" text, not the
platform entity itself.

**What worked: AI Ark's lookalike-company search, via ColdIQ** (`POST /v1/ai-ark/companies`,
`lookalikeDomains` param — up to 5 LinkedIn company URLs). Seeded with 3 known PE-backed medtech
CDMO/manufacturing roll-up platforms: Cirtec Medical, Viant Medical, Integer Holdings. This is a
similarity search over AI Ark's company graph, not a keyword match, and it correctly surfaced the
platform-level entities Blitz couldn't find (Phillips Medisize, Cretex Medical, Paragon Medical,
Orchid Orthopedic Solutions, Norwood Medical — all genuine PE-backed medtech manufacturing platforms).

**Pulled:** 5 pages (250 raw results, 241 unique by domain) at ~10.3 ColdIQ credits/page (flat per
call, not per row) — stopped at 5 pages on the user's explicit instruction to leave some AI Ark/ColdIQ
credit balance rather than exhaust it. `totalElements: 10000` in the raw response is a provider-side
cap/sentinel, not a real count of the underlying universe — this is **not** a complete universe pull,
unlike the Blitz-sourced segments in this client folder, which confirmed a real finite `total_results`.

**Post-filter:** kept only rows with 100-5000 employees (proxy for $100M-$1B revenue) → **91 rows**.

**What this verifies vs. does not:** confirms "business-model-similar to a known PE-backed medtech
manufacturing/roll-up platform," nothing more. Does NOT verify actual PE ownership, the specific hold
period, or that 2+ add-ons were absorbed without consolidation — every row needs a
PitchBook/deal-news ownership check before being called qualified.

**Cost:** ~51.5 ColdIQ credits (~$0.74) for the AI Ark pages.
