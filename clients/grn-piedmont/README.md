# GRN Piedmont

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** https://grnpiedmont.com
- **Contact:** Harvey Eden <heden@grnpiedmont.com> (also Chris Missler, cmissler@grnpiedmont.com)
- **Slack channel ID:** C0CF3JM25EC
- **Tracking client ID:** `3abc2243-889c-4177-a75a-3ac680766d20`
- **HeyReach workspace ID:** 172413 (connected)
- **Booking link:** https://calendly.com/grnpiedmont/introductory-business-conversation
- **DNC:** 8 rows in tracking_clients (6 companies after the 2 header rows), copied to `context/dnc-list.csv`
- **Last synced:** 2026-11-16 via `get_client` + `list_sourcing_configs` + `list_campaigns` + `list_campaign_docs`

Context copied from `get_client` on 2026-11-16: `context/client-brief.md`, `context/icp-form.md`, `context/client-description.md`, `context/caller-briefing.md`, `context/caller-faqs.md`.

## Sourcing configs

| Config | ICP | Market | Scope | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|---|
| Fire & Life Safety Leaders - Blitz (US F&LS 201-1000, C-level/VP) | Fire & Life Safety Leaders | US fire & life safety companies: fire sprinkler and suppression contractors, fire alarm and detection integrators, inspection, testing and maintenance providers | Campaign-specific: Fire & Life Safety Leaders (not set by this session; inferred from the config name, confirm) | draft | 1 | 0 | - |
| Owner Succession - Blitz (US manufacturers 201-1000, owners/CEOs) | Owner Succession | Founder-led or family-owned US manufacturers (industrial, discrete and process) | Campaign-specific: Owner Succession (not set by this session; inferred from the config name, confirm) | draft | 1 | 0 | - |

Config UUIDs: Fire & Life Safety Leaders `e8538474-8bd8-4479-8878-5899efe1ccf4`; Owner Succession `88fe680f-eae0-40c5-b147-1edf40579466`.

## Campaigns and campaign docs (tracking_clients, as of 2026-11-16)

| Item | ID | Status |
|---|---|---|
| Campaign doc "GRN Piedmont Campaign Ideas" (Campaigns 1 to 5) | `cae47cc4-0801-44e6-ad15-9a2f0840f766` | client_review, 19 open comment threads |
| Campaign "Fire & Life Safety Leaders" | `f1138ab0-daa4-42a1-8a7c-ca27965623ea` (HeyReach 730732) | creation |
| Campaign "Owner Succession" | `250a7100-07e0-487d-97c0-8a204d97a276` (HeyReach 730731) | creation |

## Sourced data in this repo

- `sourcing/tam/2026-11-16-jobs-sample.csv` — 250 job postings (50 newest per role family), sizing sample for the Recruitment Specific campaign (no config yet), Blitz API `POST /v2/jobs/search`, pulled 2026-11-16
- `sourcing/tam/2026-11-16-sample-leads.csv` — 36 rows (35 prospects + 1 no-match placeholder) at 14 sampled companies, Blitz API `POST /v2/search/waterfall-icp-keyword`, pulled 2026-11-16, keyed by `linkedin_url`
- `sourcing/tam/2026-11-16-clay-sample-companies.csv` — 40 companies (2 queries x 20), Clay MCP `search-companies` fit check, pulled 2026-11-16
- `sourcing/tam/tam_counts.json` + `tam_counts.py`, `tam_sample.py`, `2026-11-16-tam-read.query.md` — count-only TAM read and its exact queries

## History

- **2026-11-16** — TAM read for a new **Recruitment Specific** (open role / MPC) campaign. Moe asked for it on the Trillium Construction "Recruitment Specific Campaign" messaging and set the window to 120 days. Blitz counts: 3,870 matching manufacturing leadership postings in 120 days (855 in 30) at 201 to 1,000 employee Eastern/Central manufacturers, 556 fire & life safety postings before a noise gate. TAM/SAM read: manufacturing large, 2 contacts per company; F&LS small, 3 to 4. Scope: Campaign-specific. Full read in `sourcing/tam/2026-11-16-tam-read.query.md`. Session session_013MzxQfShB3KmCf8R7naacT.
- **2026-11-16** — Folder created from `clients/_TEMPLATE/README.md`; profile, sourcing configs, campaigns and campaign doc synced from `tracking_clients`. The client was onboarded 2026-11-02 and had a doc and two campaigns already, but no folder in this repo.
