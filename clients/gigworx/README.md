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

- `sourcing/michiana-shift-employers/2026-11-05-companies.csv`: 4,378 companies with 11+ employees headquartered in 17 St. Joseph and Elkhart County towns, tagged with `icp_bucket` (628 manufacturing, 196 warehousing and logistics, 228 retail, 191 construction, 357 hospitality, events and facilities, 14 staffing competitors, 713 with unknown industry, 2,051 out of ICP). Config **GigWorx - Michiana shift employers** (`184a0f39-d738-4f8f-a908-3c97d71dd4cf`). Pulled 2026-11-05 via Blitz API `POST /v2/search/companies`. Used for market sizing; nothing was pushed anywhere.
- `sourcing/michiana-shift-employers/2026-11-05-hiring-signal-companies.csv`: 140 companies with 462 hourly or production job postings in South Bend, Mishawaka, Elkhart, Goshen and Nappanee in the last 60 days, from the same config (`184a0f39-d738-4f8f-a908-3c97d71dd4cf`). Pulled 2026-11-05 via Blitz API `POST /v2/company/tam-by-jobs`. Only 32 of the 140 are headquartered in Indiana.
- `sourcing/michiana-shift-employers/2026-11-05-companies.query.md`: exact queries, bucket rules and known limits for both files.

## Analysis

- `campaign-ideas.md`: GigWorx Campaign Ideas, six signal-led LinkedIn campaigns, modelled on the Nextwo RaaS campaign-ideas doc. Uploaded to `tracking_clients` as campaign doc `4d41ad80-0451-4524-bf83-819a4418be7b` (draft, not shared with the client). Sent to the client on 2026-11-05 (status `client_review`). Which campaigns run is decided on the pre-launch call.
- `client-analysis.md`: full analysis of the onboarding form, ICP, market size, competitors and messaging, plus the questions for the pre-launch call (2026-11-05).

## History

- **2026-11-05** — At the repo owner's request, sent campaign doc `4d41ad80-0451-4524-bf83-819a4418be7b` (all six campaigns) to the client with `send_campaign_doc_to_client`. Status is now `client_review` and the doc is visible in the client portal. The Slack notification went to the client's channel (`C0CDR13H0MV`) with a short note: pick the campaigns on the pre-launch call, and the notes at the end list what to confirm. Session: branch `claude/stoic-hawking-utkftq`.

- **2026-11-05** — Wrote `campaign-ideas.md` in the layout of the Nextwo RaaS campaign-ideas doc the repo owner supplied as the model. It has six signal-led campaigns: Hourly Roles That Won't Close, Peak Season Crews, RV Corridor Ramps, Try Before You Hire, Owner on the Floor, and Construction and Event Crews (the last one only if Mathew confirms "Other").
  - Each campaign offers the comped first shift and stays within the client's claim limits: no pricing, no conversion fee, no fill-rate figures and no non-local client names.
  - The repo owner reviewed the draft and asked for every campaign to stay in, so the choice can be made on Mathew's pre-launch call.
  - Uploaded to `tracking_clients` with `create_campaign_doc` as doc `4d41ad80-0451-4524-bf83-819a4418be7b`: draft, not shared with the client. No campaign configs were created.
  - Session: branch `claude/stoic-hawking-utkftq`.

- **2026-11-05** — Repo owner asked for a thorough client analysis based on the onboarding form. Read the full Typeform answers, brief, caller briefing and FAQs, campaign and campaign-plan doc from `tracking_clients`. Sized the market with Blitz, which opens a **new segment** for config `184a0f39-d738-4f8f-a908-3c97d71dd4cf` (first pull; nothing pushed to Clay or HeyReach).
  - **Market size:** the configured core (manufacturing, warehousing, retail, 11+ employees) is **1,052 companies by headquarters, 329 of them with 51+ employees**. The brief had guessed 300–800.
  - **Headquarters search misses most hirers:** 108 of 140 local hourly hirers are headquartered out of state, so the lead list must filter on where the person works, not company headquarters.
  - **Contacts per company** (inverse to market size): 3–4 at 51+ employees and 1–2 at 11–50, about 2,200 contacts in total.
  - Wrote `client-analysis.md`. Its pre-launch call agenda comes first: a suppression list, local proof, and the "Other" industries.
  - Session: branch `claude/stoic-hawking-utkftq`, commit `db664ff`.

- **2026-11-05** — Created the folder from `clients/_TEMPLATE/README.md` and synced the profile, ICP, sourcing config and campaign from `tracking_clients` (client `94da4a2f-8f90-4bc0-87e6-22ff98fafd6a`). This is the first per-client session for GigWorx, which was onboarded on 2026-11-02 with one draft config and one campaign still in creation. The `tracking_clients` connector wasn't loaded in this session, so the sync went straight to its HTTP MCP endpoint (`tracking-clients.onrender.com/mcp`, JSON-RPC `tools/call`) using the same tools. Session: branch `claude/stoic-hawking-utkftq`.
