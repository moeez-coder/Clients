# 2026-10-12 companies snapshot — query record (all-ICP job-signal expansion)

**Client:** Teleion (`5072d422-da5b-44db-adab-b5c2f8d67a2f`)
**Segment status:** expanding existing segments across eight of the eleven configs (no new config-slug); the rows from different configs share one file and `signal_codes` says which config found each account.
**Why:** after the first re-check (`../fs-compliance-ops-signals-recheck/`) the user asked to find the signals across all of Teleion's ICPs, not only the FS compliance pool in the Clay export. The 152 contacted accounts were excluded, as were all 1,860 accounts from that export (already handled).

## Signal codes and config mapping
| Code | Config (`tracking_clients` UUID) | Pull filter (job-title phrases, last 90 days) | Size | Min postings | Pts |
|---|---|---|---|---|---|
| P3 | BSA/AML/KYC roles `d17cad6a-b9ee-4b07-91d5-8273c0e3dc6a` | BSA, AML, money laundering, KYC, OFAC, sanctions, financial crime, bank secrecy | 201-5,000 | 2 | 20 |
| P5 | AI/Model Risk roles `b3dd9cc8-7eab-4774-96d0-f5e2dc03aed3` | model risk/validation, AI governance, responsible AI, AI risk | 201-5,000 | 1 | 10 |
| P2 | BaaS/partnership `41e54db9-f4f8-47b5-b976-72a2ac5ad09c` | BaaS, embedded finance/banking, fintech program/partner, bank partnerships | 201-5,000 | 1 | 30 |
| M1 | Payments/Treasury/Card Ops `f3e11468-68f8-4555-9c9f-5dd919d87d9e` | payments/treasury/card operations, payments/settlement/reconciliation analyst | 201-5,000 | 2 | 15 |
| M2 | Marketing compliance `1a436fdd-d5f2-426b-826f-781b2087e8ac` | marketing/advertising compliance, content review, marketing legal | 201-5,000 | 1 | 20 |
| E1 | AI Governance enterprise `91734597-7a99-4eca-b725-68428e2bc9c1` | AI governance, responsible AI, AI risk/compliance/policy/ethics/assurance | 1,001+ | 1 | 20 |
| E2 | M&A / strategy pivot / IPO `fc9333cd-94d4-4296-b494-4c28df2573da` | post-merger/M&A integration, M&A — **job-title proxy only**, not an announced deal | 1,001+ | 1 | 10 |
| E3 | 500+ vendors / contract labor `19d6f7c2-bfe4-406d-914c-f119ee83ef4b` | vendor/supplier management, contingent workforce, managed services program — **proxy only** | 1,001+ | 2 | 10 |

P3/P5/P2 use the same meaning and points as the user's Clay export. Tier A = 35+, B = 20-34, C = below 20. M1, M2, E1, E2, E3 are new codes defined here; their point values are this session's judgment, not the export's.

## Pull
- Step 1, universe: Blitz API `POST https://api.blitz-api.ai/v2/company/tam-by-jobs`, `max_results` 50, cursor-paginated to the end, one query per code (`2026-10-12-qdefs.py` has the exact filters, `2026-10-12-pull_tam.py` runs them). FS configs filtered to LinkedIn industry Banking or Financial Services; enterprise configs unfiltered by industry. Raw: `2026-10-12-blitz-tam-by-jobs-raw.json.gz` (P3 372, P5 144, P2 34, M1 186, M2 40, E1 892, E2 1,558, E3 338 company rows before filtering).
- Step 2, filter (`2026-10-12-build.py`): US HQ only; drop every company already in the Clay export (LinkedIn URL or domain); drop Teleion's DNC (Amazon, Amazon GREF, Starbucks, Lyft, BECU, Gates Foundation, Microsoft); enterprise codes kept only for Teleion's ICP industries (financial services, insurance, healthcare, tech, retail, manufacturing) — this removes law, staffing, IT-consulting and similar firms.
- Step 3, verify: Blitz `POST /v2/jobs/company` (90 days) for each of 512 candidates, then a stricter regex on the actual job titles and the minimum-postings rule. 243 accounts survived. Raw: `2026-10-12-blitz-company-jobs-raw.jsonl.gz`.

## Not covered
- Config `bfac7bb6-4f3a-48d9-af47-2c850f1aa866` (ticket/case volume growth without ops hiring), `fbed3ab8-049d-48ce-84a1-1b9ad10a0a3a` (retail leadership tied to a named operational goal) and `23db3c31-cd04-4fc1-b4cd-582de610a171` (merchants with no single payments owner): their signals are not visible in job postings and need web/news research.
- P1 (enforcement actions) and P4 (SEC merger/IPO filings) from the Clay export.
- The DNC was matched by company name; domains were not matched.

## Caveats
- `segment` is LinkedIn's industry. "financial services" covers private equity, asset managers and insurers as well as fintechs; the ICP wants banks, credit unions and fintechs, so review those rows.
- `employees` is the LinkedIn headcount, which is not the same measure as the export's.
- E2 hits are often attorney or corporate-development roles, so tier C E2-only rows are weak.
- Title matching is on job titles only, and one role can be posted several times.
