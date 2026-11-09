# Sensor Bio

## Profile

- **Status:** active
- **Package tier:** Standard
- **Website:** https://sensorbio.com/
- **Contact:** Bryan Bulte <bryan@sensorbio.com>
- **Slack channel ID:** C0B0GNSV9PW
- **Tracking client ID:** `6bccf18a-474b-419b-bd3a-8e1e575a0caf`
- **Last synced:** 2026-09-21 via `get_client` + `list_sourcing_configs`

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| Sensor Bio - Clinical & Health Systems - Custom | Sensor Bio - Clinical & Health Systems | Health Systems, Hospitals, Population Health, Remote Patient Monitoring, Preventive Care/Preventive Medicine, Healthcare IT | draft | 1 | 0 | [link](https://app.clay.com/workspaces/770250/workbooks/wb_0tj12fz2s8za9gtjYAP) |
| Campaign #1 - Enterprise & Platforms (Casual Connections) | Campaign #1 - Enterprise & Platforms (Casual Connections) | Digital Health, Health Tech, HealthTech Platforms, AI in Healthcare, Medical Devices, Clinical Research, Life Sciences, Remote Patient Monitoring | draft | 1 | 0 | [link](https://app.clay.com/workspaces/770250/workbooks/wb_0thxmfsYqr7sJhfp2vD) |

## Sourced data in this repo

- `sourcing/heyreach-outreach/2026-09-21-leads.csv` — 2,868 unique prospects contacted so far across all 13 Sensor Bio HeyReach campaigns (workspace `131981`), pulled via `mcp__Sensor_Bio__get_conversations_v2` (all pages, 2,878 conversation records deduped by `linkedin_url`). This is a cross-campaign outreach snapshot, not tied to a single sourcing config — filed under its own `heyreach-outreach` folder since it reflects HeyReach conversation history rather than a Clay/Blitz/AI Ark sourcing pull.

## History

- **2026-09-21** — Session initialized for Sensor Bio; resynced Profile from `tracking_clients` (`get_client` + `list_sourcing_configs`, no drift from what was on file). Pulled a consolidated CSV of all 2,868 prospects reached out to so far via HeyReach (all 13 campaigns, `get_conversations_v2` across full workspace history) per user request; saved to `sourcing/heyreach-outreach/2026-09-21-leads.csv` and delivered to the user.
