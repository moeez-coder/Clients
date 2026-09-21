# Query — NewCo Countdown, Sponsor Side, 2026-09-21

**Campaign 1** — segment: PE firms with a medtech portfolio, stated carve-out/divestiture strategy,
healthcare/industrials practice, $200M-$2B EV deals.

**Prior attempt (same date, ColdIQ Marketplace API) produced zero results** — see the History entry
and the note in "Sourcing configs" in this README dated 2026-09-21: `fullenrich` keyword search
returned generic mega-caps, `ai-ark-companies`/`linkupapi-search` industry filters returned zero rows.

**This attempt: Blitz API, direct HTTPS (not via ColdIQ).** `POST https://api.blitz-api.ai/v2/search/companies`.

**Key schema fix that unblocked this:** company filters must be nested under a `"company"` key in the
request body (`{"company": {...}, "max_results": N}`) — passing them at the top level (as the docs'
own condensed examples suggested) is accepted with `200` but silently ignored, returning an
unfiltered, popularity-sorted result set (Forbes, Accenture, Infosys, P&G — total_results stuck at
~4.98M regardless of filter values). This is a real trap worth flagging for future Blitz sessions in
this repo: a 200 with plausible-looking but totally generic results is not evidence the filter worked.

**Filter used:**
```json
{
  "company": {
    "industry": {"include": ["Venture Capital and Private Equity Principals", "Venture Capital and Private Equity"]},
    "keywords": {"include": ["healthcare", "medical device", "medtech"]},
    "employee_range": ["11-50", "51-200", "201-500", "501-1000"],
    "hq": {"country_code": ["US"]}
  },
  "max_results": 25
}
```
Industry values taken from Blitz's normalized industry taxonomy (case-sensitive; confirmed via docs
search, not guessed) — `"Venture Capital and Private Equity"` / `"...Principals"`.

**What this verifies vs. does not:** confirms the firm is tagged as a PE/VC investor on LinkedIn with a
healthcare/medtech keyword hit in its "about"/specialties text (e.g. Riverside Partners, Versant
Ventures came back). It does **not** verify the carve-out/divestiture strategy, the $200M-$2B EV deal
band, or a current/recent medtech separation — none of those are firmographic filters Blitz (or any
other provider tried this session) exposes. Every row needs manual verification against 8-K filings,
the firm's own portfolio page, MedTech Dive, MassDevice, or the Lawrence Evans digest before outreach,
exactly per the campaign brief's own sourcing list.

**Result:** 43 companies (2 pages via cursor pagination, `max_results` capped at 25/page).

**TAM/SAM read:** Small, matching the campaign brief's own note ("this list is small and the
relationships are long — do not run it for volume"). Per CLAUDE.md's inverse rule this argues for
**more contacts per company** once prospects are pulled — the brief already anticipates this.

**Cost:** Blitz API is unlimited/flat-monthly on this account (`records_remaining: 14,070,717` at
time of pull) — effectively $0 marginal cost for this pull, unlike the ColdIQ/credit-metered pulls
for the other six segments.
