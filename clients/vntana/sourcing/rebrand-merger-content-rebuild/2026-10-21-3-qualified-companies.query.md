# Rebrand, Merger, Content Rebuild — qualified companies (2026-10-21, pull 3)
Client VNTANA `5e0a22cf-6efb-432d-bc3c-6eb914440f13`; campaign `62cbf47f-1722-426a-a249-ed838420cd55`; sourcing config `98e470eb-7d7d-446c-b9e6-d78e059b7c5e`. **Expanding existing segment** `rebrand-merger-content-rebuild` — a filtered view of `2026-10-21-2-companies.csv` (no new sourcing calls; companies only, no contacts). Same-day third snapshot.

## Owner criteria (2026-10-21)
- **Qualified** = discrete manufacturer (not a process or materials manufacturer) whose products are either many SKUs or very complex SKUs. Only two verdicts: Qualified / Not Qualified; this file lists Qualified only.
- **Headcount 200+.** Revenue is *not* a filter (owner: "revenue is not that big of a deal"), so the earlier $250M floor was dropped and companies below it with 200+ employees were re-admitted.

## Steps
1. Pool: every row of the 2,756-row file with employee_count >= 200, plus tier-E rows (carried from the 2026-10-15 run, 1,001+ headcount band, count unknown). Rows with no headcount at all (872: unmatched in Prospeo or unknown size) cannot be confirmed at 200+ and were left out.
2. Quick triage by Prospeo industry label: dropped 294 rows labelled chemicals, oil/gas/mining, paper, semiconductors, wholesale, construction, biotech, software, utilities, telecom, services, finance, etc. -> 651 left.
3. Qualifier: 17 Haiku agents (40 rows each, no web access, spec `SPEC_Q.md`) judged each company from the name, domain, industry label, event and headline plus the model's own knowledge. Result: 485 Qualified, 166 Not Qualified.
4. Final headcount check removed 4 Qualified rows whose Prospeo employee_count was under 200 (ESCO Technologies 136, Komori 55, Graham 15, Favelle Favco 3 — likely Prospeo data errors, revisit if wanted).

## Result
**481 Qualified companies** (`2026-10-21-3-qualified-companies.csv`). By source tier: 226 revenue >= $250M, 6 straddling $250M, 25 no revenue and 1,000+ employees, 12 no revenue and 500-999, 127 below $250M revenue or under 500 employees (all 200+), 85 from the 2026-10-15 run (headcount unknown, 1,001+ band). Columns add `industry`, `makes` and `qualifier_reason`.

## Limits
- Verdicts are a small model's judgement from names and headlines; it was permissive (75% Qualified). Expect some process-industry or few-SKU firms to slip through and some borderline cases either way.
- The triage used Prospeo's industry label, which can be wrong; a mislabelled discrete manufacturer would have been dropped without review.
- 872 companies with no headcount were excluded and could contain qualifying firms.
- The underlying events still carry the extraction noise noted in `2026-10-21-2-companies.query.md`.
