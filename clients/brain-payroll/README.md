# Brain Payroll

## Profile

- **Status:** active
- **Package tier:** Standard
- **Website:** https://www.brainpayroll.co.uk/
- **Contact:** Raxit Shah <raxit.shah@brainpayroll.co.uk>
- **Slack channel ID:** C0BSBQ9UQUC
- **Tracking client ID:** `0a09f3c7-9a9b-4f57-bbec-e2fbf0dc6780`
- **HeyReach workspace ID:** 157376 (connected)
- **Last synced:** 2026-09-17 via `get_client` + `list_sourcing_configs`

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| UK recruitment agencies & bureaus running umbrella/contractor payroll (51-1,000) | UK Staffing Agencies & Payroll Bureaus servicing umbrella companies - 51-1,000 | UK Recruitment/Staffing Agencies & payroll bureaus servicing umbrella companies | draft | 1 | 0 | - |
| UK & ROI payroll bureaus & practices advertising payroll roles (last 30-60d) | UK & ROI Payroll Bureaus / Accountancy Practices - 11-500, hiring payroll staff | UK & ROI Payroll Bureaus / Accountancy Practices offering payroll services | draft | 1 | 0 | - |
| UK Payroll Bureaus & Accountancy Practices - Boutique/Mid Bureaus: 11–200 - Custom | UK Payroll Bureaus & Accountancy Practices - Boutique/Mid Bureaus: 11–200 | Accounting & Bookkeeping, Professional Services, Payroll Services | draft | 1 | 0 | [link](https://app.clay.com/workspaces/770250/workbooks/wb_0tkdesfZ4Ycz9Vip5vk) |
| UK Payroll Bureaus & Accountancy Practices — Enterprise (201+) - Custom | UK Payroll Bureaus & Accountancy Practices — Enterprise (201+) | Accounting & Bookkeeping, Professional Services, Payroll Services | draft | 1 | 0 | [link](https://app.clay.com/workspaces/770250/workbooks/wb_0tkdeqt5AJeNNm6a8FZ) |

Config UUIDs (all module `custom`, granularity `company`, refresh `static`):

- UK recruitment agencies & bureaus running umbrella/contractor payroll (51-1,000) — `a47f2b39-0aaf-48d4-a1e0-45909b305979` (ICP `02a970d1-210b-42b2-b782-39fca79085e8`)
- UK & ROI payroll bureaus & practices advertising payroll roles (last 30-60d) — `cb081b3d-9e0c-44ce-aa5e-364cc4d8a249` (ICP `1e31365a-c678-4a0e-800b-2d84ccade31d`)
- UK Payroll Bureaus & Accountancy Practices - Boutique/Mid Bureaus: 11–200 - Custom — `b790b5bd-eb5b-4e68-a807-5c674138dd1a` (ICP `c925995c-20a4-4013-bbc9-42a5d3e3e889`)
- UK Payroll Bureaus & Accountancy Practices — Enterprise (201+) - Custom — `7806e67e-a2e9-4fff-91a3-5982cbde52b5` (ICP `228a37d3-9100-42f9-9f5e-98254ee4f463`)

## Sourced data in this repo

- `sourcing/2026-09-17-combined-universe-companies.csv` — **1,442 ICP-qualified target
  companies**, the combined target-company universe spanning **all four sourcing configs**
  (`a47f2b39-0aaf-48d4-a1e0-45909b305979`, `cb081b3d-9e0c-44ce-aa5e-364cc4d8a249`,
  `b790b5bd-eb5b-4e68-a807-5c674138dd1a`, `7806e67e-a2e9-4fff-91a3-5982cbde52b5`).
  Pulled 2026-09-17 from four tools, unioned and deduped on LinkedIn company URL:
  **Blitz API** `POST /v2/search/companies` (industry drains + a 38-term payroll keyword
  matrix, GB and IE) and `POST /v2/jobs/search` + `POST /v2/enrichment/company` (payroll-role
  hiring signal, last 90 days); **EXA Websets** `POST /websets/v0/websets` (12 company-entity
  queries incl. BACS/CIPP/FCSA accreditation framings), resolved through Blitz
  `domain-to-linkedin`; and **AI Ark** `POST /v1/companies` `lookalikeDomains` seeded by the
  LinkedIn URL of each already-qualified bureau/practice. 27,333 raw records → 17,039 unique
  → 1,442 qualified. Segment split: accountancy practices 1,306 / payroll bureaus 49 /
  recruitment-umbrella 45 / umbrella-contractor 42. Geography GB 1,285 / IE 157. The
  `icp_confidence` column is load-bearing: **291 `high`** carry explicit payroll-provider
  wording, **1,151 `medium`** are confirmed UK/IE practices of 11+ staff whose payroll
  service line is *inferred, not verified*. Feeds all four segments' campaigns.
  Query, funnel and health warnings: `2026-09-17-combined-universe-companies.query.md`.
- `sourcing/2026-09-17-combined-universe-rejected.csv` — 15,597 rejected companies with the
  reason each failed (size, not-a-provider, geography, DNC, competitor, professional body).
  Kept as the audit trail behind the number above, so a future session can re-judge a
  rejection rule without re-running the whole harvest.

No `-leads.csv` yet — this is a company-level universe only; no prospect-level pull has been
run for this client, so the `linkedin_url`-keyed leads standard does not apply to these files.
Company rows follow the equivalent company pattern via `company_linkedin_tag` + `domain`.

## History

- **2026-09-17** — **Built the combined ICP-fit target-company universe across all four
  sourcing configs: 1,442 qualified companies** (`sourcing/2026-09-17-combined-universe-companies.csv`).
  This is a *new* universe for every segment — no `sourcing/` tree existed and all four
  configs read 0 companies in `tracking_clients`. Used four tools rather than one because
  no single source covers this ICP: Blitz for firmographic and keyword drains, Blitz jobs
  for the client's own stated hiring signal ("advertising vacancies within payroll services
  teams"), EXA Websets for accreditation-directory framings (BACS/CIPP/FCSA) that taxonomy
  queries cannot express, and AI Ark lookalikes to close the Ireland gap — Blitz returned
  only 94 Irish accounting companies against 5,007 British, and AI Ark lifted the Irish pool
  from 167 to 1,018. Qualification enforced the ICP's real test — *does this company run
  payroll for other organisations* — rather than merely mentioning payroll, which is why
  payroll/HCM software vendors (Brain Payroll's own competitors), in-house payroll teams at
  end employers, professional bodies, and recruiters who staff accountancy roles were all
  rejected; the client's 64-row DNC list was applied on normalised domain and name. Two
  qualifier bugs were caught mid-build and fixed: substring matching made `rti` match
  "expertise" (~200 false positives) and competitor-name matching against description text
  rejected ~220 real practices for saying "Xero Gold Partner". **The binding constraint is
  the ICP's 11-employee floor** — 12,279 of 17,039 harvested companies are 1-10 staff, so
  the UK micro-practice long tail is excluded by the ICP itself, not by tooling; whether to
  sell to sole practitioners is a commercial call for the client. Also recorded that
  `icp_confidence: medium` (1,151 rows) is *inferred* — payroll is near-universal at
  accountancy practices but was not verified per company. Session: client session for
  brain-payroll.
- **2026-09-17** — Resynced Profile + Sourcing configs from `tracking_clients`
  (`get_client` + `list_sourcing_configs`). Values matched what was already on
  record, but the README was missing three sections required by the repo
  standard (`Last synced`, `Sourced data in this repo`, `History`), so those
  were added and the config UUIDs / ICP UUIDs written in for cross-referencing.
  Also restored the en-dashes in two config names that had been flattened to
  hyphens, so the names now match `tracking_clients` verbatim. Session: client
  session for brain-payroll.
- **2026-08-24** — Folder created during repo initialization (commit `d28d7e3`);
  profile and sourcing-config table synced from `tracking_clients`.
