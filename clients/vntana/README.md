# VNTANA

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** https://www.vntana.com/
- **Contact:** ashley@vntana.com
- **Slack channel ID:** C0BA8RZKFF1
- **Tracking client ID:** `5e0a22cf-6efb-432d-bc3c-6eb914440f13`

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

