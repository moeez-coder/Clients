# Query — New Leader, Old Portfolio, 2026-09-21

**Campaign 4** — segment 4(a): multi-BU device/diagnostics companies, $250M-$3B revenue, 3+ distinct
product brands into overlapping hospital call points. (Segment 4(b) — PE-backed roll-up platforms,
$100M-$1B — was not separately queried this pass; see Open items below.)

**Tool:** ColdIQ Marketplace API, `POST /v1/companies/search`, `provider: "fullenrich"`.

**Filter used:**
```json
{"industries": ["Medical Equipment Manufacturing"], "countries": ["US"], "min_employees": 700, "max_employees": 15000, "limit": 100}
```

**What this verifies vs. does not:** headcount range is a scale proxy for $250M-$3B revenue (not a
direct revenue filter — this provider's revenue fields were unreliable in testing). It does **not**
verify "3+ distinct product brands" or the "role change 30-75 days ago" trigger — those require a
brand-portfolio check and a LinkedIn role-change date check per company, done separately.

**Result:** 44 unique companies from this pull. This exact universe was also reused for campaign 7
(Portfolio Without a Throughline) — see that segment's note; not double-counted as new sourcing there.

**Segment 4(b) not sourced this pass:** PE-backed roll-up platforms, $100M-$1B, 2+ un-consolidated
add-ons, is a distinct filter (ownership + M&A history, not industry+headcount) that was not run in
this session due to the credit budget running out (balance hit ~$16 remaining after this call). Flagged
as an open item.

**Cost:** ~1,163 credits (~$16.62).
