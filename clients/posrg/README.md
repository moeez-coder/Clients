# POSRG

## Profile

- **Status:** active
- **Package tier:** Standard
- **Contact:** Ken Testa <ktesta@posrg.com>
- **Slack channel ID:** C0C0JLSR3HC
- **Tracking client ID:** `bd8a0868-ca61-4b30-859f-e23c52a4c9a9`
- POSRG sells payment terminal / POS hardware into multi-location retail, restaurant, and hospitality chains (fleet exposure reporting, PCI-driven terminal refresh, buyback programs for aging hardware).

## Campaigns

| Campaign | Status | Channel | HeyReach ID |
|---|---|---|---|
| The Fleet Exposure Report | changes_requested | LinkedIn only | 595435 |
| The PCI Time Bomb | implementing (approved) | LinkedIn only | 595354 |
| The Buyback Ambush | changes_requested | LinkedIn only | 595369 |

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| Retail - Custom | Retail | Retail, Restaurants & Food Service, Food & Beverage, Retail Groceries, Hospitality | draft | 1 | 0 | - |
| US & Canada chains (501+) with older-gen payment terminals: PCI/terminal upgrade job posts, PCI fine history, or no refresh in 4+ years | US & Canada Multi-Location Retail, Restaurant & Hospitality Chains - 501+, aging payment terminal fleets | US & Canada multi-location retail, restaurant, and hospitality chains running aging payment terminal fleets | draft | 1 | 0 | - |
| US & Canada chains (501+) announcing POS/self-checkout refresh, new store rollout or POS platform switch (1-4mo) | US & Canada Multi-Location Retail, Restaurant & Hospitality Chains - 501+, POS/self-checkout refresh underway | US & Canada multi-location retail, restaurant, and hospitality chains going through a POS or self-checkout hardware refresh | draft | 1 | 0 | - |

All three sourcing configs are `draft` with 0 companies landed yet — nothing to pull into `sourcing/` for this repo until a config moves to `ready` and gets run.

## ICP notes

- **Retail** (config `fe23deae-30ee-4af0-9984-62a0131e7dc1`): broadest of the three — US/Canada retail, restaurant, food & beverage, grocery, hospitality chains, 501+ employees, IT/Ops/exec personas. Entry signals: 20+ store locations, recent store growth, known POS platform with no refresh in 3+ years, recent IT/Ops leadership change, or any public mention of remodels/self-checkout/hardware modernization.
- **Aging payment terminal fleets** (config `102d2fe3-6e41-4b63-9397-e4e645076d1b`): same geography/size range, adds CISO/Payment Security/Risk & Compliance personas. Entry signals: PCI compliance/terminal upgrade job postings, public PCI breach or fine history, no known POS hardware refresh in 4+ years. $20M+ revenue.
- **POS/self-checkout refresh underway** (config `8aac614e-159e-4fbb-99ab-2c832f142dbf`): same geography/size range as Retail. Entry signals: recently announced or posted jobs for a POS/self-checkout/kiosk refresh, new store rollout, or a POS platform switch (Toast, NCR, Oracle Micros, Clover) in the last 1-4 months. $20M+ revenue.

No client corrections or rejected angles found in Slack yet — all three configs are live/active as configured, none marked superseded.
