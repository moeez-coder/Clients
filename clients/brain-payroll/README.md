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

- `sourcing/2026-09-17-combined-universe-companies.csv` — **2,492 ICP-qualified target
  companies**, the combined target-company universe spanning **all four sourcing configs**
  (`a47f2b39-0aaf-48d4-a1e0-45909b305979`, `cb081b3d-9e0c-44ce-aa5e-364cc4d8a249`,
  `b790b5bd-eb5b-4e68-a807-5c674138dd1a`, `7806e67e-a2e9-4fff-91a3-5982cbde52b5`).
  Pulled 2026-09-17 from **six tools**, unioned and deduped on LinkedIn company URL then on
  domain: **Blitz API** `POST /v2/search/companies` (industry drains + a 38-term payroll
  keyword matrix, GB and IE) and `POST /v2/jobs/search` + `POST /v2/enrichment/company`
  (payroll-role hiring signal, last 90 days); **EXA Websets** `POST /websets/v0/websets`
  (12 company-entity queries incl. BACS/CIPP/FCSA accreditation framings), resolved through
  Blitz `domain-to-linkedin`; **AI Ark** `POST /v1/companies` `lookalikeDomains` seeded by
  the LinkedIn URL of each already-qualified bureau/practice; **Prospeo**
  `POST /search-company` (industry/keyword × GB+IE × headcount 11+ — the single biggest
  contributor, see below); and **DiscoLike** via the **ColdIQ** proxy
  `GET /v1/discolike/discover` (natural-language ICP text, 3 queries). 51,357 raw records →
  29,096 unique → 2,492 qualified. Segment split: accountancy practices 2,229 / payroll
  bureaus 112 / umbrella-contractor 82 / recruitment-umbrella 69. Geography GB 2,295 /
  IE 197. The `icp_confidence` column is load-bearing: **471 `high`** carry explicit
  payroll-provider wording, **2,021 `medium`** are confirmed UK/IE practices of 11+ staff
  whose payroll service line is *inferred, not verified*. Feeds all four segments'
  campaigns. Includes a **`description`** column — the company's own description of itself,
  from its LinkedIn About or website (2,467 of 2,492 populated; the 193 gaps left by the
  source APIs were filled via ColdIQ `POST /v1/company/enrich` in batches of 50). Query,
  funnel and health warnings: `2026-09-17-combined-universe-companies.query.md`.
- `sourcing/2026-09-17-combined-universe-rejected.csv` — 26,604 rejected companies with the
  reason each failed (size, not-a-provider, geography, DNC, competitor, professional body,
  wealth manager, foreign TLD). Kept as the audit trail behind the number above, so a future
  session can re-judge a rejection rule without re-running the whole harvest.

- `sourcing/2026-09-17-combined-universe-leads.csv` — **2,056 decision-maker prospects**
  across 1,270 companies, keyed by `linkedin_url` (first column, unique — 2,056 distinct
  URLs for 2,056 rows). Pulled 2026-09-17 via **Prospeo** `POST /search-person`, two passes
  over the company domains in batches of 50: payroll-title holders (`person_job_title`
  CONTAINS "payroll") and practice leadership (managing partner, practice manager, MD, FD,
  CFO, client services director, owner/founder). Contact depth follows the repo's inverse-TAM
  rule — **2 per accountancy practice** (large segment), **4 per bureau/umbrella/recruitment-
  umbrella** (small segment). Seniority gated to the brief's own list (C-Suite, Director,
  Head, Manager, Partner, Founder/Owner, VP): Partner 749, Manager 586, Founder/Owner 302,
  C-Suite 257, Director 102, Head 62. 83% carry a verified (masked) work email. Each row
  carries its company's `company_verdict` from the qualifier agent so Clay can filter to
  confirmed buyers.
- `sourcing/2026-09-17-combined-universe-verdicts.csv` — **all 2,492 companies adjudicated**
  by the qualifier agent: **1,395 QUALIFIED** (every one carrying a payroll-service URL on
  the company's own domain), 757 LIKELY, **340 DISQUALIFIED (13.6%)** — all of them rows the
  firmographic pass had accepted. Qualified by segment: accountancy practices 1,188, payroll
  bureaus 114, umbrella/contractor 76, recruitment-umbrella 17. Produced by 36 LLM sub-agents
  over Tier-1 website evidence; see `qualifier-agent/README.md` for the method and what it
  caught.

Historical note: no `-leads.csv` existed — this is a company-level universe only; no prospect-level pull has been
run for this client, so the `linkedin_url`-keyed leads standard does not apply to these files.
Company rows follow the equivalent company pattern via `company_linkedin_tag` + `domain`.

## History

- **2026-09-17** — Pulled the **decision-maker layer**: 2,056 prospects across 1,270
  companies (`sourcing/2026-09-17-combined-universe-leads.csv`), keyed by `linkedin_url` per
  the repo standard, via Prospeo `POST /search-person`. Two passes — payroll-title holders
  and practice leadership — with contact depth set inversely to segment size as the campaign
  standard requires. A first pass let through 210 people tagged `Entry` seniority (Payroll
  Specialist, Clerk, Officer, Analyst); the brief bars junior roles outright and title-string
  exclusions had missed those variants, so the gate now uses Prospeo's own seniority field
  with the title list as backup. Two Prospeo findings recorded: `match_mode: CONTAINS` is
  required for substring title matching (the default is exact, which silently returns
  NO_RESULTS), and a company whose recorded domain was `linkedin.com` would have returned
  **LinkedIn Corp employees** as its buying committee — Prospeo rejected the batch with
  INVALID_FILTERS, which is how that defect surfaced. Also built `qualifier-agent/push_to_clay.py`
  to push qualified companies and prospects to their Clay webhooks: one JSON object per
  request as that source expects, rate-limited, with sent-state tracking because the webhook
  source has **no upsert** and a re-run would duplicate every row. Session: client session
  for brain-payroll.
- **2026-09-17** — Added a **`description`** column to the universe CSV (2,467 of 2,492
  populated) and built the **qualifier agent** in `qualifier-agent/`. The agent exists to
  settle the open question the universe build left behind: 2,021 rows are `icp_confidence:
  medium`, meaning a confirmed UK/IE practice of 11+ staff whose payroll service line was
  *assumed* rather than verified. It is deliberately two-tier rather than one sub-agent per
  company — 2,492 LLM agents to answer a question a single site-scoped search usually
  settles would be indefensible. Tier 1 searches each company's **own domain** for a payroll
  service page via ColdIQ's EXA proxy (~1.47 credits each, resumable, parallel); on the
  first 25 companies it confirmed 21 outright with an exact URL and verbatim quote. Tier 2
  shards whatever is left to LLM sub-agents that apply `qualifier-agent/rubric.md` — the
  judgment calls: competitor vs customer, bureau vs end employer, acquisitions. Two
  operational findings recorded in the tool: ColdIQ rate-limits **per account, not per
  connection**, so 14 workers merely converted throughput into 429s (it rate-limited an
  unrelated credits call) — the manager now runs a single global token bucket tuned by
  `COLDIQ_RPS` rather than by worker count; and a transient API failure is now re-queued by
  `--retry-failed` rather than being silently cached as a result. Session: client session
  for brain-payroll.
- **2026-09-17** — **Extended the universe from 1,442 to 2,492 companies (+73%) by adding the
  three sourcing tools the first pass had skipped** — Prospeo, ColdIQ and DiscoLike. Prospeo
  turned out to be the strongest single source for this ICP: Blitz returns 459 UK accounting
  companies at 11+ employees, Prospeo returns **2,430** on the same filter (and 163 Irish
  against Blitz's 94 total), because Blitz's coverage of this sector is weighted to
  1-10-employee micro-practices that the ICP excludes. **ColdIQ turned out not to be a data
  source at all but a metered unified proxy over ~60 B2B providers** (Apollo, LimaData,
  TheirStack, Icypeas, LinkupAPI, PredictLeads, and DiscoLike/AI Ark/Prospeo themselves) —
  666 endpoints, documented at `GET /openapi.json`; it is also how DiscoLike is reachable,
  which is why the earlier direct attempt at `api.discolike.com` 404'd. DiscoLike's
  natural-language `icp_text` search is well suited to this niche but costs ~111 credits per
  100 records, so only 3 calls were made pending clarification of a **contradiction in its
  credit reporting** (the balance endpoint says 166 remaining, the response header says
  ~16,400). High-confidence rows rose 291 → 471. A third dedupe bug surfaced and was fixed:
  keying only on LinkedIn URL left 910 duplicate pairs where one firm holds two LinkedIn
  pages after a rebrand or merger, so a second domain-keyed pass now collapses them; a
  wealth-manager/IFA filter was also added after firms like Craven Street Wealth qualified on
  a passing "our accountants" mention. Session: client session for brain-payroll.
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
