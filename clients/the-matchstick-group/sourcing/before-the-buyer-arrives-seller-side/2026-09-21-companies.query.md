# Query — Before the Buyer Arrives (Seller Side), 2026-09-21

**Campaign 2** — segment: medtech/diagnostics parents, $250M+ revenue, announced
intent to separate / strategic review / active divestiture. New segment (v1 had nothing for this buyer).

**Tool:** ColdIQ Marketplace API, `POST /v1/companies/search`, `provider: "fullenrich"` (pinned; `auto`
routed to FullEnrich on the first pass anyway).

**Filter used:**
```json
{"industries": ["Medical Equipment Manufacturing"], "countries": ["US"], "min_employees": 1000, "limit": 100}
```

**What this filter actually verifies vs. does not:** `industries` + `min_employees` confirms "large
US medtech/diagnostics company" as a scale proxy for "$250M+ revenue" (no direct revenue field was
reliably populated by this provider). It does **NOT** verify the separation/strategic-review trigger
itself — no provider in this marketplace exposes an "announced divestiture" filter. Every row here is
a firmographic candidate only; the 8-K/press-release trigger must be confirmed per-company before
outreach, per the campaign brief's own sourcing note (8-K filings, PE portfolio pages, MedTech Dive,
MassDevice, Lawrence Evans digest).

**Result:** 94 unique companies (by domain), after dedup against an earlier smaller `auto`-routed pull.

**TAM/SAM read:** Large — "medtech/diagnostics parent, $250M+" is a wide net before the separation
trigger narrows it. Per CLAUDE.md's inverse rule, this argues for **fewer contacts per company** once
prospects are pulled (proposed: 2, buying-committee: Corp Dev lead + one of CEO/VP Marketing/Comms).

**Cost:** ~1,163 ColdIQ credits (~$16.62 at `coldiq-standard-v1`, $0.014286/credit).

---

## Update, same day: expanded to full universe via Blitz API

**User asked to "use all tools and give the complete universe of these campaigns."** Re-ran this
segment's industry filter directly against Blitz API (`POST /v2/search/companies`, filters nested
under `"company"` — see campaign 1's query.md for why that nesting matters), fully paginated to
exhaustion (cursor-based, 50/page) rather than a single capped page. Blitz confirmed a **finite total
universe** at this filter (`total_results` in the raw response, not an estimate) and every row of it
was pulled. Merged into the existing ColdIQ-sourced CSV, deduplicated by domain — Blitz found
companies ColdIQ's FullEnrich pass had missed (and vice versa; both sets are kept). This is now the
combined ColdIQ + Blitz universe for this filter, not a sample of it. It is still not the full
*qualified* segment — the same trigger/verification caveats noted above still apply to every row,
Blitz-sourced or ColdIQ-sourced alike.

**Cost:** $0 marginal (Blitz unlimited plan).
