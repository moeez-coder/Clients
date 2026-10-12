# 2026-10-12 companies snapshot — query record

**Client:** Teleion (`5072d422-da5b-44db-adab-b5c2f8d67a2f`)
**Segment status:** expanding existing segments (no new config-slug in `tracking_clients`). This folder spans three configs, because the pool was checked against signals P2, P3 and P5 together:
- P3 → `d17cad6a-b9ee-4b07-91d5-8273c0e3dc6a` (2+ BSA/AML/KYC analyst roles, 60-90d)
- P5 → `b3dd9cc8-7eab-4774-96d0-f5e2dc03aed3` (AI Risk / Model Risk / AI Governance Lead roles)
- P2 → `41e54db9-f4f8-47b5-b976-72a2ac5ad09c` (new partner programs / BaaS / partnership leads)

**Why:** user supplied a Clay export (1,860 FS accounts, `Teleion_target_accounts_with_signals`, tier/score/P1-P5) in which the 152 signalled accounts had already been contacted. Request: re-check the remaining accounts against the same five signals. P1 and P4 are not yet checked in this file (see below).

## Input pool
- Export: 1,860 rows. Removed all 152 signalled rows, any row sharing a LinkedIn URL or domain with a signalled row, and duplicate LinkedIn URLs: 1,666 left.
- Removed from output after the pull: Federal Reserve Bank of New York (a regulator, not a prospect) → 1,654 rows.
- Teleion's DNC list (9 entries) has NOT yet been matched against this file.

## Pull
- Tool: Blitz API `POST https://api.blitz-api.ai/v2/jobs/company`, body `{company_linkedin_url, job:{date_posted:{last_days:90}}, max_results:50, cursor}`, paginated up to 6 pages per company. 1,666 calls, 0 errors, 50,630 postings, 1,146 companies with at least one posting.
- Raw responses: `2026-10-12-blitz-company-jobs-raw.jsonl.gz`. Scripts: `2026-10-12-pull_jobs.py` (pull), `2026-10-12-classify.py` (title rules and scoring).

## Signal rules (applied to job title only)
- **P3** (20 pts): 2+ postings whose title matches BSA, AML, bank secrecy, anti-money laundering, KYC, OFAC, sanctions, financial crime(s), CDD/EDD, transaction monitoring, CFT.
- **P5** (10 pts): title matches model risk/validation/governance, AI governance, responsible AI, AI risk, or AI/ML combined with risk/governance/compliance/control.
- **P2** (30 pts, proxy): title matches BaaS, banking-as-a-service, embedded finance/banking, fintech program/partner/relationship, bank partner(ship)s; engineer/developer titles excluded. A first, looser pattern returned mostly sales/BD partnership roles and was discarded.
- **Tier:** A = score 35+, B = 20-34, C = below 20. Same point values as the source export.
- **Not checked:** P1 (enforcement actions) and P4 (merger/charter/IPO filings); `signal_codes` for those are therefore absent, not negative.

## Known caveats
- Some hits are vendors that sell AML/compliance software (for example Solytics Partners), whose roles serve their own product, not an in-house compliance build. Review before calling.
- `pilot_tag` is `-` throughout; the source export's pilot tag is not carried over.
