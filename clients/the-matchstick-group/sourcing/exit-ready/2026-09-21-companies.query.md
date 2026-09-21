# Query — Exit Ready, 2026-09-21

**Campaign 5** — segment: PE-backed medtech/diagnostics platforms, $100M-$1B, held 3+ years,
post-roll-up or in exit prep.

**Tool:** ColdIQ Marketplace API, `POST /v1/companies/search`, `provider: "fullenrich"`.

**Filter used:**
```json
{"industries": ["Medical Equipment Manufacturing"], "countries": ["US"], "min_employees": 250, "max_employees": 3000, "limit": 100}
```

**What this verifies vs. does not:** headcount range as a $100M-$1B revenue proxy and industry match
only. Does **not** verify PE ownership, 3+ year hold period, 2+ un-consolidated add-ons, a banker
engagement, or exit-focused finance hires — none of those are firmographic filters available in this
marketplace; they require deal-intelligence sources (PitchBook, deal press) per company.

**Result:** 51 unique companies (new, on top of an earlier smaller pull that is superseded/merged
into this file).

**TAM/SAM read:** Medium. Proposed contact depth once prospects are pulled: 2-3 per company
(CEO/CCO/VP Marketing, sponsor operating partner as secondary path per the brief).

**Cost:** ~1,163 credits (~$16.62).
