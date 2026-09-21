# Query — NewCo Countdown, NewCo Leadership, 2026-09-21

**Campaign 3** — segment: newly separated medtech/diagnostics businesses, $250M+ carved-out revenue,
0-12 months past close.

**Tool:** ColdIQ Marketplace API, `POST /v1/companies/search`, `provider: "fullenrich"`.

**Filter used:**
```json
{"industries": ["Medical Equipment Manufacturing"], "countries": ["US"], "min_employees": 250, "max_employees": 5000, "limit": 100}
```

**Known gap — founding-year proxy dropped:** the original filter attempt added `min_founded_year: 2022`
as a proxy for "newly separated." FullEnrich returned **HTTP 400** on that combination (rejected, not a
soft miss) — the parameter is accepted by the OpenAPI schema but this provider path does not support it
in combination with `industries`. Dropped it rather than substitute a different provider, since no
provider in this marketplace has an actual "spun off from parent on date X" field; `year_founded` is
returned per-row in the CSV so this can still be eyeballed, but it is **not a reliable proxy** — a
company founded in 2022 is far more often an ordinary young company than a carve-out. Every row here
needs manual verification (press release / close-date search) before being called a newco at all —
this pull only confirms scale + industry, nothing about separation status or timing.

**Result:** 99 unique companies. TAM/SAM read: cannot be assessed honestly until the newco/non-newco
split is done manually — treat this list as an unfiltered candidate pool, not a qualified segment.

**Cost:** ~1,163 credits (~$16.62).
