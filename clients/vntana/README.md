# VNTANA

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** https://www.vntana.com/
- **Contact:** ashley@vntana.com
- **Slack channel ID:** C0BA8RZKFF1
- **Tracking client ID:** `5e0a22cf-6efb-432d-bc3c-6eb914440f13`
- **Last synced:** 2026-09-14 via `list_icp_configs` (config/persona detail); `list_sourcing_configs` not re-pulled since 2026-09-09 — company/campaign counts in the table below may be stale, re-sync before trusting them for a new build.

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| VNTANA Casual Connections Sourcing | VNTANA Casual Connections - Senior Stakeholders | Industrial Equipment/Machinery, Manufacturing, Construction Equipment, Agricultural Machinery, Industrial Pumps & Valves, Heavy-duty Trucks, Mining Equipment, Industrial Automation, Hydraulics & Pneumatics, Power Transmission, Industrial Tools, Process Equipment | draft | 0 | 0 | - |
| iVT Expo - Off-Highway Vehicle Sourcing | iVT Expo - Off-Highway Vehicle Technology | Off-Highway Vehicle OEMs, Off-Highway Component Suppliers, Agricultural Machinery, Construction Equipment, Mining Equipment | draft | 1 | 0 | - |
| IMTS 2026 - Precision Components Sourcing | IMTS 2026 - Precision Components, Instruments & Consumables | Precision Component Manufacturers, Precision Instruments, Tooling & Consumables Suppliers, Machine Tool Accessories | draft | 1 | 0 | - |
| IMTS 2026 - Machine Tools, Automation & Robotics Sourcing | IMTS 2026 - Machine Tools, Automation & Robotics | Machine Tool Manufacturers, Robotics & Automation Equipment Manufacturers, CNC Machining Center Builders, Industrial Automation, Robotics | draft | 1 | 0 | - |
| Industrial Mfg PLM/CAD | Industrial Mfg PLM/CAD | Industrial Equipment/Machinery, Manufacturing, Mining, Construction Equipment, Agricultural Machinery, Industrial Pumps & Valves, Heavy-duty Trucks, Mining Equipment, Industrial Automation, Hydraulics & Pneumatics, Power transmission, Industrial Tools, Process Equipment | draft | 3 | 284 (this repo, via Blitz) | [link](https://app.clay.com/workspaces/770250/workbooks/wb_0thwk77HpkCSnu3tHS3) |
| VNTANA B2B eCommerce OEMs | VNTANA B2B eCommerce OEMs | Industrial Pumps & Fluid Control, Heavy Equipment, Hydraulics & Pneumatics, Engines and Power Transmission Equipment Manufacturing, Electric Power Transmission, Control and Distribution, Industrial Tools, Process Equipment, Construction Equipment, Construction Hardware Manufacturing | ready | 1 | 99 | - |
| VNTANA Aftermarket OEMs | VNTANA Aftermarket OEMs | Construction Equipment, Agricultural Machinery, Industrial Pumps & Valves, Heavy-duty Trucks, Communications Equipment Manufacturing, Mining Equipment, Material Handling, Industrial Automation, Agriculture, Construction, Mining Machinery Manufacturing, Retail Building Materials and Garden Equipment, Wholesale Building Materials | ready | 1 | 99 | - |

## Sourced data in this repo

- `sourcing/b2b-ecommerce-oems/2026-09-10-companies.csv` — 99 companies from **VNTANA B2B eCommerce OEMs** (config `ce119be1-eb15-4eaa-b01d-3d8570c7ebda`)
- `sourcing/aftermarket-oems/2026-09-10-companies.csv` — 99 companies from **VNTANA Aftermarket OEMs** (config `4cf01c51-4158-4108-aada-9fddc6ef5a48`)
- `sourcing/industrial-mfg-plm-cad/2026-09-14-companies.csv` — 284 companies (deduped from 300 pulled) for **Industrial Mfg PLM/CAD** (config `eed58f1d-7df7-4e87-9120-d578ba9f89c0`), sourced via the Blitz API `/v2/search/companies` endpoint using this ICP's segment filters: US/Canada HQ, 1,001+ employees, industries mapped to Blitz's normalized taxonomy (Industrial Machinery Manufacturing, Automation Machinery Manufacturing, Industrial Automation, Agriculture/Construction/Mining Machinery Manufacturing, Engines and Power Transmission Equipment Manufacturing, Electric Power Transmission Control and Distribution, Metal Valve Ball and Roller Manufacturing, Commercial and Service Industry Machinery Manufacturing, Fabricated Metal Products, Mining and Metals). 903 total companies matched this filter in Blitz; this is the first page pulled (6×50 results). Re-run with the same filter and a fresh cursor to pull more.
- `sourcing/open-check-combined-personas/2026-09-14-leads.csv` — 46 contact-level leads sourced via Blitz API's `/v2/search/people`, scoped to the 412 unique companies already sourced across the Industrial Mfg PLM/CAD, B2B eCommerce OEMs, and Aftermarket OEMs configs (via `company.linkedin_url`), filtered to a persona combining all of VNTANA's ICP segments (Director/VP/C-Team in marketing, digital, product, aftermarket, or eCommerce functions). **Pushed live to the "US & Europe \| Open Check \| LLA" HeyReach campaign (`580599`, currently PAUSED)** via `add_leads_to_campaign`.
  - Started from 150 raw candidates across 3 of 9 company batches, later expanded to all 9 batches (412 companies); went through several manual quality passes before pushing: dropped a retired profile, dropped generic executives with no real marketing/digital/aftermarket connection (a Chief Compliance Director, board members, country managers, etc. that only matched on the coarse `job_level`/`job_function` filter), dropped one person at an off-topic Veralto business unit (life sciences/diagnostics, not the industrial side), and dropped 18 companies that turned out to be marketing/consulting agencies, a recruiting firm, a CAD-software reseller (GoEngineer and its subsidiary Cad Micro), and a parts-catalog SaaS vendor (RevolutionParts) rather than actual manufacturers — all miscategorized under industrial-sounding LinkedIn industries in the original company sourcing.
  - **Left in as a judgment call, not resolved**: Caterpillar equipment dealers (LiftOne, Fabick Cat, Altorfer Cat, Peterson Cat, Weisiger Group) — these are dealers/distributors, not manufacturers, but VNTANA's Aftermarket OEMs ICP explicitly touches dealer/distributor networks, so they may still be relevant for a dealer-parts-catalog angle. Worth a second look before the next batch.
  - **Recommendation**: the underlying company CSVs (`industrial-mfg-plm-cad`, `b2b-ecommerce-oems`, `aftermarket-oems`) likely have similar agency/reseller/service-provider contamination that wasn't caught before this pass — worth a cleanup sweep.

## HeyReach campaigns (HeyReach Vertical Launch structure)

Per CLAUDE.md's per-client campaign build standard, VNTANA has run the HeyReach Vertical Launch quadset twice:

| Tag | Con Req | Con Acc | Open Check | Open Profile | Acc webhook | Open webhook |
|---|---|---|---|---|---|---|
| **LLA** (pre-existing) | `553401` PAUSED | `580597` PAUSED | `580599` PAUSED | `580600` DRAFT | `68960` → Con Req, active | `74541` → Open Check, active (Clay URL ending `...a4e35d65...`) |
| **General** (2026-09-15, this repo) | `601750` PAUSED | `601751` DRAFT | `601752` PAUSED | `601753` DRAFT | **pending** — no Connection-Accepted webhook URL supplied yet | `78850` → Open Check `601752`, active (Clay URL ending `...5316754a...`) |

"General" is tagged as such (not a numbered vertical) per the repo owner's convention: a quadset drawing from the combined TAM/SAM across all of VNTANA's ICP segments (rather than one specific campaign/segment) is named `General`, not `Vertical N`.

**Still open on the General quadset:** the Con Req (`601750`) Acc webhook (`CONNECTION_REQUEST_ACCEPTED`) has no URL yet — ask the repo owner for the Connection-Accepted Clay webhook URL, then `create_webhook` scoped to campaign `601750` and verify with `get_webhook_by_id` before this quadset is considered complete. Con Acc (`601751`) and Open Profile (`601753`) are intentionally left in DRAFT (terminal campaigns, no webhook needed) until leads flow in from Clay.

## History

- **2026-09-15** — Built the "General" HeyReach Vertical Launch quadset (4 lists, 4 campaigns cloned from the existing LLA quadset as template, 8 valid sender accounts — excludes Ben Conway `217013`, whose LinkedIn auth is invalid). Con Req (`601750`) and Open Check (`601752`) started then paused to unlock webhook eligibility; Open webhook (`78850`, `VIEWED_PROFILE`) created and verified scoped to Open Check. Acc webhook still pending a Connection-Accepted Clay URL from the repo owner. Session: this one (see commit history for the exact commit).
- **2026-09-14** — Sourced 46 contact-level leads via Blitz API `/v2/search/people` across companies already in this repo, filtered to a combined VNTANA persona; pushed live into the pre-existing LLA quadset's Open Check campaign (`580599`) after several manual quality corrections (see "Sourced data in this repo" above for the full list of what was dropped and why).
- **2026-09-14** — Sourced 284 companies for the Industrial Mfg PLM/CAD config via Blitz API `/v2/search/companies` (US/Canada, 1,001+ employees, mapped industry taxonomy); first page of 903 total matches.
- **2026-09-09/10** — Repo scaffold created; VNTANA folder seeded from `tracking_clients`, existing B2B eCommerce OEMs and Aftermarket OEMs company exports (99 each, DiscoLike-sourced) added from data already present in the tracking system.
