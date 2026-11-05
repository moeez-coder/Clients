# GigWorx

## Profile

- **Status:** active
- **Package tier:** Solo (clientType `solo`)
- **Website:** https://www.gigworx.com
- **Contact:** Mathew Welsch <mwelsch@gigworx.com>
- **Booking link:** https://meetings.hubspot.com/mathew-welsch
- **Slack channel ID:** C0CDR13H0MV
- **Tracking client ID:** `94da4a2f-8f90-4bc0-87e6-22ff98fafd6a`
- **Campaign strategist:** moeez@algoacquisition.ai (GTM engineer, sourcing engineer, closer: `-`)
- **HeyReach workspace:** `172344` (heyreachConnected: true). In sessions this is the `Gigworks` HeyReach connector (`mcp__Gigworks__*`). Instantly, Smartlead and PlusVibe are not connected. masterInboxWorkspaceId `-`. DNC list: 0 entries (`dncSkipped: false`).
- **What they sell:** On-demand, shift-based W-2 staffing. Businesses post shifts in a web portal, vetted workers claim them in an app, and GigWorx handles payroll, insurance and compliance. They bill only for hours worked, with no subscription or minimums. Live markets are Bozeman/Helena MT, Salt Lake City UT and South Bend–Elkhart IN. Founded in 2018.
- **Offer:** GigWorx comps the client's first shift.
- **Pricing line:** "It depends, book a call." Pay rate plus a transparent markup.
- **Meeting hours:** EDT 08:30–18:00
- **Sales Nav:** no
- **Onboarding form:** submitted 2026-10-29. The client was added to `tracking_clients` on 2026-11-02.
- **Last synced:** 2026-11-05 via `get_client` + `list_sourcing_configs` (+ `list_icp_configs`, `list_campaigns`)

## ICP (from `list_icp_configs`)

**Michiana shift employers** (ICP `e91ece83-dca2-4a4a-8ee3-9c793a1d3bf1`, segment `a710b98b-4a9a-47fa-b062-81002d862bd0`)

- **Market:** Manufacturing, Warehousing & Logistics, Retail
- **Geos:** Saint Joseph County, Indiana; Elkhart County, Indiana
- **Company sizes:** 11-50 through 10000+
- **Titles:** President, Owner, Plant Manager, Operations Manager, Production Manager, Production Supervisor, Warehouse Manager, Human Resources Manager, Human Resources Business Partner, General Manager
- **Seniority:** CXO, VP, Director, Owner/Partner, Experienced Manager, Entry Level Manager
- **Signals:** hiring for hourly/production/warehouse roles, seasonal demand swings, large manufacturing site, short lead time on orders
- **Qualifier:** The business has a physical site in St. Joseph or Elkhart County (South Bend, Mishawaka, Elkhart, Goshen, Nappanee) and staffs hourly, shift-based roles: manufacturing (including RV and RV-supplier plants), warehousing/distribution or retail. Staffing agencies and self-employed are excluded.

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| GigWorx - Michiana shift employers (Clay people search) | Michiana shift employers | Manufacturing, Warehousing & Logistics, Retail | draft | 1 | 0 | `-` |

Config ID `184a0f39-d738-4f8f-a908-3c97d71dd4cf`. Module: Custom (company granularity), static refresh. Lead count 0. Clay table URL and webhook not set yet.

## Campaigns (from `list_campaigns`)

| Campaign | Status | Channel | Identity | HeyReach ID | Approved |
|---|---|---|---|---|---|
| GigWorx - Michiana ops & HR - first shift comped | creation (step 18) | LinkedIn | Client | `-` | no |

Session ID `84fdb583-6cb5-4920-99c7-3004d79e8aca`.

## Sourced data in this repo

- `-`: no snapshots pulled yet.

## History

- **2026-11-05** — Created the folder from `clients/_TEMPLATE/README.md` and synced the profile, ICP, sourcing config and campaign from `tracking_clients` (client `94da4a2f-8f90-4bc0-87e6-22ff98fafd6a`). This is the first per-client session for GigWorx, which was onboarded on 2026-11-02 with one draft config and one campaign still in creation. The `tracking_clients` connector wasn't loaded in this session, so the sync went straight to its HTTP MCP endpoint (`tracking-clients.onrender.com/mcp`, JSON-RPC `tools/call`) using the same tools. Session: branch `claude/stoic-hawking-utkftq`.
