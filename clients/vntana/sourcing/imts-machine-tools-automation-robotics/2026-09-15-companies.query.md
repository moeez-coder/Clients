# Query — 2026-09-15 companies snapshot (IMTS 2026 — Machine Tools, Automation & Robotics, new segment)

**Tool:** Blitz API `POST /v2/search/companies`
**Purpose:** First company pull for this config (previously 0 companies sourced).

**Request body (same call as the Precision Components query — see that file's `.query.md` for the full body; this file holds the subset tagged `Robotics Engineering` or `Robot Manufacturing`, 12 rows).**

**Note:** small yield (20 combined across both IMTS configs from this query) — Blitz's industry taxonomy doesn't map cleanly onto "machine tool manufacturer" as its own category, so this likely undercounts. Worth broadening in a future pull (e.g. add `keywords.include: ["CNC", "machine tool"]`). Not yet vetted at company or lead level.
