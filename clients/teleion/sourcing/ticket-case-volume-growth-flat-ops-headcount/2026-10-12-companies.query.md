# Qualification run — 2026-10-12

- **Client:** Teleion (`5072d422-da5b-44db-adab-b5c2f8d67a2f`)
- **Sourcing config:** "1,000+ employee tech/financial services/healthcare firms showing ticket & case volume growth without ops hiring" (`bfac7bb6-4f3a-48d9-af47-2c850f1aa866`); campaign "Ops Backlog: Scaling Without Adding Headcount" (`e185f231-9723-4f06-b168-e4a657d8e849`)
- **Segment status:** new segment (first CSV for this config-slug). Input: Clay export "Large US Companies, Tech & Health", 11,744 US companies, 1,000+ employees (Hospitals/Health Care 4,727; IT services 1,979; Financial Services 1,857; Software 1,651; other tech 1,530).
- **Criterion:** growing ticket, case, or alert volume, flat or shrinking ops headcount.
- **Tools:** Blitz API `POST /v2/company/tam-by-jobs` (support/customer service/case manager/ops analyst/service desk/help desk/claims/technical support titles; US jobs; last 90d; companies 1,000+ employees; 6,385 companies returned, 1,583 matched the input list by LinkedIn URL); rule-based screen in `scripts/qual.py`. `scripts/pull.py` is the Blitz pull.
- **Rules (first match wins):**
  1. DQ — entity type Government Agency / Educational / Self Employed / Self Owned.
  2. DQ — 5+ open support/ops/case roles in last 90d (proxy: ops headcount growing).
  3. Qualified tier A — description mentions support/tickets/claims/case management/alerts/managed services/etc., or industry is IT Services / Network Security.
  4. Qualified tier B — weaker customer/platform-volume wording.
  5. DQ — no ticket/case/alert signal.
- **Limits:** Blitz `employee_growth` is null for every company, so headcount trend is NOT measured; volume growth is NOT verified per company (no source for it at this scale). "Qualified" = plausible fit to sequence/verify, not confirmed. Zero open roles may reflect missing job coverage. Tier A is the stronger list.
- **Result:** 4,957 qualified (A 3,378, B 1,579), 6,787 disqualified.
- **Contacts per company:** not decided here (no leads pulled).
