# S3 Partners

## Profile

- **Status:** active
- **Package tier:** Standard
- **Website:** https://www.s3partners.com/
- **Contact:** Michael King <michael.king@s3partners.com>
- **Slack channel ID:** C0AVC57R2BV
- **Tracking client ID:** `846e54da-91e5-4d41-91e5-ce8970cdde4b`
- **HeyReach workspace:** `131833` (S3 Partners)
- **Last synced:** 2026-11-24 via get_client + list_sourcing_configs (no drift from the previous copy)

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| S3 Partners - Sell-Side Equity Finance (Normal - Option 5) | Equity Broker-Dealers | Broker-Dealers, Prime Brokerage, Equity Sales & Trading, Stock Loan/Securities Finance | draft | 0 | 0 | - |
| S3 Partners - Buy-Side Crowding (Normal - Option 5) | Short-Side Blind Spot (Long/Short Equity Hedge Funds) | Financial Services, Investment Banking | draft | 1 | 0 | - |
| Campaign #1 - Equity Broker-Dealers | Equity Broker-Dealers | Broker-Dealers, Prime Brokerage, Equity Sales & Trading, Stock Loan/Securities Finance | draft | 1 | 0 | [link](https://app.clay.com/workspaces/770250/workbooks/wb_0thwlphdeV2wfwCgEXV) |
| Short-Side Blind Spot (Long/Short Equity Hedge Funds) - Sales Nav - static | Short-Side Blind Spot (Long/Short Equity Hedge Funds) | Financial Services, Investment Banking | draft | 0 | 7 | - |
| Short-Side Blind Spot (Long/Short Equity Hedge Funds) - AI Scrapers - evergreen | Short-Side Blind Spot (Long/Short Equity Hedge Funds) | Financial Services, Investment Banking | draft | 0 | 0 | - |

## Sourced data in this repo

- `sourcing/short-side-blind-spot-salesnav/2026-09-10-companies.csv` — 7 companies from **Short-Side Blind Spot (Long/Short Equity Hedge Funds) - Sales Nav - static** (config `ccdd21a0-6b77-4dbe-9686-27aab6d8a8c2`)

## HeyReach campaigns (workspace 131833)

As of 2026-11-24. The 8 active senders are 195299 Adalia Desmonda, 195315 Trini Gea, 195342 Ignatius Budiani, 195384 Alexander Edward, 230739 Luke Valdes (the only Sales Navigator seat), 249216 Kim Cruz, 256357 Myrjean Alisoso and 256469 Eugene Dosdos.

Three accounts are left out because HeyReach shows them `isActive: false`, although their auth is valid: 234426 Jason Eduria, 241273 Kirky Palamos and 273883 Glaiza Gabia.

No campaign here has a `CHECK_IS_OPEN_PROFILE` (Open Check) step. No HeyReach tool reads a campaign's schedule, so "not recorded" means nobody wrote it down before.

| Campaign id | Name | Status | Senders before → after (2026-11-24) | Schedule |
|---|---|---|---|---|
| 500979 | Campaign #1 - Equity Broker-Dealers | IN_PROGRESS | 8 → 8 (already full) | before: not recorded. After: 7 days, 08:00–18:00, America/New_York |
| 698428 | Campaign #1 - Equity Broker-Dealers 8.0 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 695689 | Campaign #1 - Equity Broker-Dealers 2.2 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 686459 | Campaign #1 - Equity Broker-Dealers 2.1 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 678510 | Campaign #1 - Equity Broker-Dealers 7.0 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 667574 | Campaign #1 - Equity Broker-Dealers 6.0 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 656163 | Campaign #1 - Equity Broker-Dealers 5.0 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 651004 | Campaign #1 - Equity Broker-Dealers 4.0 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 636692 | Campaign #1 - Equity Broker-Dealers 3.0 | PAUSED | 8 → 8 (already full) | not recorded (paused, not touched) |
| 624786 | Campaign #1 - Equity Broker-Dealers 2.0 | PAUSED | 6 (no 256357, 256469) → 8 | not recorded (paused, not touched) |
| 589390 | Normal - Option 5 - 07/09/2026 | PAUSED | 4 (195299, 195315, 195342, 195384) → 8 | not recorded (paused, not touched) |
| 500484 | DB-02/07/2026 TDA (Only USA) | PAUSED | 4 (same four) → 8 | not recorded (paused, not touched) |
| 498893 | DB-02/07/2026 (No USA) TDA | PAUSED | 4 (same four) → 8 | not recorded (paused, not touched) |
| 498497 | Campaign #1 | PAUSED | 4 (same four) → 8 | not recorded (paused, not touched) |
| 443619 | DR - 13/05/2026 | PAUSED | 4 (same four) → 8 | not recorded (paused, not touched) |
| 454881 | AI Scraper // TTV (broad) - 03/06/2026 | FINISHED | 4, out of scope | not recorded |
| 451891 | AI Scraper - 26/05/2026 | FINISHED | 4, out of scope | not recorded |

## History

- **2026-11-24:** Initialization resync with `get_client` and `list_sourcing_configs`; the Profile and Sourcing-configs table matched. Added the Last synced line and the HeyReach workspace id. Then, under the two changes Moe approved on 2026-11-24 in the orchestrator session (all active senders on all campaigns; every IN_PROGRESS campaign 7 days a week), re-confirmed by the owner in this session before any change:
  - **Senders:** `update_campaign_accounts` set all 8 active senders on 624786, 589390, 500484, 498893, 498497 and 443619 (6 or 4 senders before, see the table). The 9 other non-finished campaigns already had all 8. Factual-accuracy guard: all 6 sequences were read with `get_campaign_sequence`. Five use per-lead `{message1}`–`{message3}` variables with generic fallbacks. 498497's fixed copy says "reaching out from S3 Partners" with no person's name or signature, so none of them speaks as one specific sender. The per-lead copy generated upstream for the variable campaigns was not inspected. No campaign has an Open Check step. The three inactive accounts were left out.
  - **Schedule:** the only IN_PROGRESS campaign, 500979, was paused, then set with `update_campaign_schedule` to all seven days, 08:00–18:00 America/New_York, and resumed. `get_all_campaigns` confirmed IN_PROGRESS afterwards. Before: not recorded anywhere (no tool reads it). The window is the batch default, since none was on record. The timezone is US Eastern because the prospects are mainly US equity broker-dealers, centred on New York. Paused campaigns' schedules were not changed.
  - No campaign or doc was created, so no task-log entry was needed. Session: claude.ai/code session_013MzxQhNwX53AWNpP9po5dg.

