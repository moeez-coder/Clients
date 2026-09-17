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

None yet — no `sourcing/` tree exists for this client. All four configs report
`company_count` 0 and `lead_count` 0 in `tracking_clients` as of the last sync,
so the absence here is consistent with the source of truth, not a documentation
gap. The two Clay workbooks linked above are where the boutique/mid and
enterprise configs live; nothing has been exported from them into this repo yet.

## History

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
