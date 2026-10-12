# Teleion

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** https://www.teleion.com/
- **Contact:** ryan@teleion.com
- **Slack channel ID:** C0BRE4T0W1X
- **Tracking client ID:** `5072d422-da5b-44db-adab-b5c2f8d67a2f`
- **Last synced:** 2026-10-12 via get_client + list_sourcing_configs

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| US banks & fintechs announcing new partner programs or hiring BaaS/partnership leads | US Regulated Financial Services Compliance Ops - 201-5,000, launching fintech/embedded finance programs | Financial Services | draft | 1 | 0 | - |
| US banks & fintechs posting AI Risk, Model Risk or AI Governance Lead roles | US Regulated Financial Services Compliance Ops - 201-5,000, hiring AI/model risk governance leads | Financial Services | draft | 1 | 0 | - |
| US banks & payments companies posting Payments, Treasury or Card Operations Analyst roles | US Regulated Financial Services Compliance Ops - 201-5,000, hiring payments/treasury analysts | Financial Services | draft | 1 | 0 | - |
| US banks & fintechs posting Marketing Compliance / Content Review / Marketing Legal roles | US Regulated Financial Services Compliance Ops - 201-5,000, hiring marketing compliance reviewers | Financial Services | draft | 1 | 0 | - |
| US banks, credit unions & fintechs posting 2+ BSA/AML/KYC analyst roles (60-90d) | US Regulated Financial Services Compliance Ops - 201-5,000, hiring BSA/AML analysts | Financial Services | draft | 1 | 0 | - |
| 1,000+ employee tech/financial services/healthcare firms showing ticket & case volume growth without ops hiring | Cross-Industry Enterprises (Tech, Financial Services, Healthcare) - 1,000+, rising volume with flat ops headcount | Cross industry, Technology, Financial Services and Healthcare | draft | 1 | 0 | - |
| 1,000+ employee FS/healthcare/tech firms with M&A, strategy pivot or IPO in last 12-18 months | Financial Services, Healthcare & Technology Enterprises - 1,000+, mid-integration or recently public | Financial Services, Healthcare and Technology, companies mid merger integration or recently public | draft | 1 | 0 | - |
| 1,000+ employee manufacturing, tech & healthcare firms with 500+ active vendors or heavy contract labor use | Manufacturing, Technology & Healthcare Enterprises - 1,000+ employees, 500+ vendors or contractor-heavy | Manufacturing, Technology and Healthcare, large distributed vendor and contractor ecosystems | draft | 1 | 0 | - |
| Retail/consumer companies 1,000+ with leadership publicly tied to a named operational goal | Retail & Consumer Enterprises - 1,000+ employees, public performance commitment | Retail and Consumer, companies with a public reset or margin recovery goal | draft | 1 | 0 | - |
| FS & retail merchants, $20M+ revenue, multi-channel acceptance with no single payments owner | Merchants & Payment Platforms with Complex Acceptance Mix - $20M+ revenue, multi-channel | Financial Services and Retail, merchants and payment platforms with complex acceptance mix | draft | 1 | 0 | - |
| AI Governance & Production - Enterprise - Custom | AI Governance & Production - Enterprise | Technology, Financial Services, Healthcare (payer/provider AI lawsuits), Retail, Manufacturing | draft | 3 | 0 | [link](https://app.clay.com/workspaces/770250/workbooks/wb_0tk9mb4fYtChbjBBEpu) |

## Sourced data in this repo

- `clients/teleion/sourcing/fs-compliance-ops-signals-recheck/2026-10-12-companies.csv` — 1,654 rows (31 with a signal), Blitz API `POST /v2/jobs/company` (90-day job postings), pulled 2026-10-12. Spans three configs: BSA/AML (`d17cad6a-b9ee-4b07-91d5-8273c0e3dc6a`, P3), AI/Model Risk (`b3dd9cc8-7eab-4774-96d0-f5e2dc03aed3`, P5), BaaS/partnership (`41e54db9-f4f8-47b5-b976-72a2ac5ad09c`, P2). Query, rules and caveats in `2026-10-12-companies.query.md`; raw API responses in `2026-10-12-blitz-company-jobs-raw.jsonl.gz`.
- `clients/teleion/sourcing/all-icps-job-signals-expansion/2026-10-12-companies.csv` — 243 rows (all with a signal), Blitz API `POST /v2/company/tam-by-jobs` + `POST /v2/jobs/company`, pulled 2026-10-12. Eight configs: `d17cad6a-b9ee-4b07-91d5-8273c0e3dc6a`, `b3dd9cc8-7eab-4774-96d0-f5e2dc03aed3`, `41e54db9-f4f8-47b5-b976-72a2ac5ad09c`, `f3e11468-68f8-4555-9c9f-5dd919d87d9e`, `1a436fdd-d5f2-426b-826f-781b2087e8ac`, `91734597-7a99-4eca-b725-68428e2bc9c1`, `fc9333cd-94d4-4296-b494-4c28df2573da`, `19d6f7c2-bfe4-406d-914c-f119ee83ef4b`. Filters, code-to-config table and caveats in `2026-10-12-companies.query.md`.

## History

- **2026-10-12** — Expanding existing segments across eight of the eleven configs (no new config-slug): sourced new accounts showing job-based signals for the BSA/AML, AI/model-risk, BaaS/partnership, payments/treasury, marketing-compliance, AI-governance, M&A-integration and vendor/contract-labor configs. Why: user asked to find the signals across all of Teleion's ICPs, not only the FS pool in the Clay export; contacted accounts, the export's accounts and the DNC were excluded. Result: 243 accounts (7 tier A, 101 tier B, 135 tier C). Three configs (ticket volume, retail operational goal, merchants/payments owner) have no job-visible signal and still need web research; P1 and P4 still not run. TAM/SAM read: enterprise configs are a large universe (hundreds of matches per code), FS configs small, so contacts-per-company depth is left to the user's own people sourcing. — session `moeez-coder/Clients`, branch `claude/charming-brahmagupta-a5ccvz`.
- **2026-10-12** — Expanding existing segments (no new config-slug): re-checked the 1,666 not-yet-contacted accounts from the user's Clay export against the job-based signals P2/P3/P5 via Blitz Jobs API. Why: the 152 signalled accounts in that export were already contacted, so the next call list has to come from the rest. Result: 31 accounts with a signal (26 P3-only, 3 P5-only, 1 P2-only, 1 P3+P5), none above tier B. P1 (enforcement) and P4 (SEC filings) not yet run; DNC match not yet run. TAM/SAM read: small pool (about 1,650 accounts in the 201-5,000 band), so contacts-per-company depth deferred — user is sourcing people and phones separately. — session `moeez-coder/Clients`, branch `claude/charming-brahmagupta-a5ccvz`.
- **2026-10-12** — Session started for Teleion (client `5072d422-da5b-44db-adab-b5c2f8d67a2f`); re-pulled `get_client` + `list_sourcing_configs`: no drift (still 11 draft configs, 0 companies sourced). User supplied a Clay export of 1,860 FS target accounts with signals (P1–P5) to analyze for cold-caller prospecting; analysis only so far, nothing sourced or stored yet. — session `moeez-coder/Clients`, branch `claude/charming-brahmagupta-a5ccvz`.
- **2026-09-15** — Initialized session for Teleion; resynced Profile + Sourcing configs table from `tracking_clients` (`get_client`, `list_sourcing_configs`). Sourcing configs grew from 6 to 11 rows since the last snapshot in this repo (5 new Financial Services Compliance Ops segments added 2026-09-11) — table updated to match. No CSVs pulled yet. — session `moeez-coder/Clients` orchestrator, branch `claude/busy-meitner-kix5ao`.

