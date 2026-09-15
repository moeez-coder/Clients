# Teleion

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** https://www.teleion.com/
- **Contact:** ryan@teleion.com
- **Slack channel ID:** C0BRE4T0W1X
- **Tracking client ID:** `5072d422-da5b-44db-adab-b5c2f8d67a2f`
- **Last synced:** 2026-09-15 via get_client + list_sourcing_configs

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

_No CSV snapshots yet. TAM estimate below is a scoping figure (company counts only), not a sourcing pull — no `-companies.csv`/`-leads.csv` produced._

## TAM estimate (free tools) — 2026-09-15

Pulled via **Blitz API** (`BLITZ_API_KEY`, called directly over HTTPS — confirmed live, no Prospeo/AI Ark firmographic overlap needed for a company-count-only estimate). Two endpoint types used:
- **`POST /v2/company/tam-by-jobs`** for the 5 hiring-signal configs — distinct companies matching job-title filters, paginated to exhaustion (cursor `null`).
- **`POST /v2/search/companies`** for the 6 firmographic configs — single call, `total_results` field in the response.

All queries scoped to `hq.country_code`/`job.location.country_code` = `US`. This is a **firmographic/hiring-keyword base count**, not a qualified TAM — it has not been filtered for the ICP's behavioral signal (e.g. "flat ops headcount," "M&A in last 12-18mo," "500+ vendors," "$20M+ revenue," "no single payments owner"), since Blitz's free filters don't expose those directly. Treat these as upper-bound sourcing pools to run the client's qualifier prompts against, not final account counts.

| Config | Method / filters | TAM |
|---|---|---|
| US banks & fintechs — BaaS/partnership leads | tam-by-jobs; title: Partnerships, Banking as a Service, BaaS, Embedded Finance; industry: Banking/Financial Services/Capital Markets/Investment Banking/Credit Intermediation; employee 201-5,000; jobs posted last 180d | **391** |
| US banks & fintechs — AI Risk/Model Risk/AI Governance leads | tam-by-jobs; title: AI Risk, Model Risk, AI Governance; same industry/employee/window | **152** |
| US banks & payments — Payments/Treasury/Card Ops analysts | tam-by-jobs; title: Payments Analyst, Treasury Analyst, Card Operations Analyst, Payments Operations; same industry/employee/window | **282** |
| US banks & fintechs — Marketing Compliance/Content Review/Marketing Legal | tam-by-jobs; title: Marketing Compliance, Content Review, Marketing Legal, Advertising Compliance; same industry/employee/window | **59** |
| US banks/credit unions/fintechs — 2+ BSA/AML/KYC analyst postings | tam-by-jobs; title: BSA Analyst, AML Analyst, KYC Analyst, BSA/AML, Anti-Money Laundering; `job.min_per_company: 2`; same industry/employee; jobs posted last 90d | **63** |
| Cross-Industry Enterprises (Tech/FS/Healthcare) 1,000+ | search/companies; industry: Computer Software/IT Services/Financial Services/Banking/Capital Markets/Hospital and Health Care; employee 1,001-10,000+ | **948** |
| FS/Healthcare/Tech Enterprises 1,000+ (M&A/IPO signal) | search/companies; same industry/employee filter as above — M&A/IPO/strategy-pivot signal not filterable via Blitz, base pool only | **948** |
| Manufacturing/Tech/Healthcare Enterprises 1,000+ | search/companies; industry: Manufacturing/Industrial Automation/Industrial Machinery/Computer Software/IT Services/Hospital and Health Care; employee 1,001-10,000+ | **623** |
| Retail & Consumer Enterprises 1,000+ | search/companies; industry: Retail/Retail Apparel and Fashion/Consumer Goods/Supermarkets/Food and Beverage Retail; employee 1,001-10,000+ | **187** |
| Merchants & Payment Platforms (FS & retail, $20M+ revenue) | search/companies; industry: Financial Services/Banking/Retail/Retail Apparel and Fashion/Consumer Goods; employee 51-10,000+ (no revenue filter available in Blitz Company Search — headcount used as proxy floor) | **4,075** |
| AI Governance & Production — Enterprise | search/companies; industry: Computer Software/IT Services/Financial Services/Banking/Hospital and Health Care/Retail/Manufacturing; employee 1,001-10,000+ | **1,164** |

**Not yet run:** AI Ark API (`AIARK_API_KEY`, confirmed live) and Prospeo API (`PROSPEO_API_KEY`, now present in this session's env — CLAUDE.md's Sourcing tools note that it wasn't yet visible as of 2026-09-14 is outdated) were not used for this pass; Blitz alone was sufficient for a company-count TAM. Flagging the Prospeo status drift to the repo owner separately since updating that note is a system-file change (CLAUDE.md).

## History

- **2026-09-15** — Initialized session for Teleion; resynced Profile + Sourcing configs table from `tracking_clients` (`get_client`, `list_sourcing_configs`). Sourcing configs grew from 6 to 11 rows since the last snapshot in this repo (5 new Financial Services Compliance Ops segments added 2026-09-11) — table updated to match. No CSVs pulled yet. — session `moeez-coder/Clients` orchestrator, branch `claude/busy-meitner-kix5ao`.
- **2026-09-15** — Ran a free-tools TAM scoping pass across all 11 sourcing configs using Blitz API (`/v2/company/tam-by-jobs` for the 5 hiring-signal configs, `/v2/search/companies` for the 6 firmographic configs). Results in "TAM estimate" above. This is a firmographic/keyword base count to size the sourcing pools, not a qualified account list — no CSV produced, no company_count updated in `tracking_clients`. — session `moeez-coder/Clients` orchestrator, branch `claude/busy-meitner-kix5ao`.

