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
- `sourcing/sensor-bio-clinical-health-systems-custom/2026-09-24-companies.csv` — 1,000 companies (sample of a ~17,014-company Blitz-estimated TAM — see query file) from **Sensor Bio - Clinical & Health Systems** (config `5df66ff4-9081-4c57-b885-652712731028`, ICP `f007b949-38ad-4e03-adb7-e1e33f65baef`), pulled via Blitz API `POST /v2/search/companies` (industry: Hospitals/Hospitals and Health Care, employee_range 201–5000, HQ US). **Firmographic match only — no ICP qualifier applied yet.**
- `sourcing/campaign-1-enterprise-platforms-casual-connections/2026-09-24-companies.csv` — 1,000 companies (sample of a ~4,305-company Blitz-estimated TAM — see query file) from **Campaign #1 - Enterprise & Platforms (Casual Connections)** (config `08e0c5dc-2a67-43c5-bbaa-99fa7cd8339b`, ICP `eb764c7c-13f0-4b7c-905b-816df3b7cae1`), pulled via Blitz API `POST /v2/search/companies` (keywords: digital health/RPM/health tech/AI healthcare/healthtech platform, employee_range 51–500, HQ US). **Firmographic match only — no ICP qualifier applied yet.**

## History

- **2026-09-21** — Session initialized for Sensor Bio; resynced Profile from `tracking_clients` (`get_client` + `list_sourcing_configs`, no drift from what was on file). Pulled a consolidated CSV of all 2,868 prospects reached out to so far via HeyReach (all 13 campaigns, `get_conversations_v2` across full workspace history) per user request; saved to `sourcing/heyreach-outreach/2026-09-21-leads.csv` and delivered to the user.
- **2026-09-24** — Pulled the **complete pre-qualification target universe** for both Sensor Bio ICPs, per user request ("complete target universe... before qualification"). Used Blitz API company search directly (the Blitz-API MCP tool only searches docs, not live data) against each ICP's firmographic filters. Blitz reports the full TAM at 17,014 companies for Clinical & Health Systems and 4,305 for Enterprise & Platforms (both configs are *existing* segments being expanded, not new); saved a 1,000-company sample of each (max practical in one session — full enumeration would need ~680 more paginated calls per segment) to their respective `sourcing/<config-slug>/2026-09-24-companies.csv`, with query filters documented in the matching `.query.md`. Explicitly no qualifier/scoring step run — this is the raw universe only, as requested. Also produced a consolidated, deduped `sourcing/2026-09-24-target-universe-consolidated-companies.csv` across both segments per follow-up user request.
