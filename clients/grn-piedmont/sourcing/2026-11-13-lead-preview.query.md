# GRN Piedmont lead preview, 2026-11-13

**Why:** the repo owner asked for a lead preview across the five campaigns in the "GRN Piedmont Campaign Ideas" doc (tracking_clients campaign doc `cae47cc4-0801-44e6-ad15-9a2f0840f766`), so the campaigns with the most leads could be set up first.

**Tool:** tracking_clients `gtm_sheet_find_people` / `gtm_sheet_find_companies`, provider Blitz (default). Every query below was a count (`count_only: true`) except the two company previews that returned rows, which are saved next to this file.

**Shared filters:** person and company in the US (`countries: ["US"]`), company size `201-500` and `501-1000`. Blitz can't filter by time zone, so these counts cover the whole US. The Eastern/Central limit still has to be applied.

"Manufacturing industries" below means Blitz industries `Manufacturing`, `Industrial Machinery Manufacturing`, `Machinery Manufacturing`, `Chemical Manufacturing` and `Plastics Manufacturing`.

| Campaign | Query | Result |
|---|---|---|
| 5 Owner Succession | People: titles Owner, Founder, President, CEO, Chief Executive Officer (exclude Vice President, VP, Assistant) at manufacturing-industry companies | **3,132 people**, before the founder-led/family-owned and 15+ year tenure filters, which Blitz can't apply |
| 3 Fire & Life Safety Leaders | People: titles Owner, President, CEO, COO, CFO, VP Operations, Vice President of Operations, CHRO, VP Human Resources (exclude Assistant) at companies with keywords fire protection, fire sprinkler, fire alarm, fire suppression, life safety | **3,066 people** (noisy: the keyword match pulls in manufacturers and security-only firms) |
| 3 Fire & Life Safety Leaders | Companies: same keywords | 1,823 companies |
| 3 Fire & Life Safety Leaders | Companies: tighter keywords fire sprinkler, fire alarm, fire suppression | **334 companies**. 10 shown, saved in `fire-life-safety-leaders/2026-11-13-companies.csv`. Several aren't core F&LS contractors (security monitoring, MEP engineering, product manufacturers), so the Claygent core-business check in the doc is needed |
| 4 The Rehire Question | People: CHRO, Chief Human Resources Officer, Chief People Officer, VP Human Resources, Vice President of Human Resources, VP People at manufacturing-industry companies | 237 people |
| 4 The Rehire Question | People: HR Director, Director of Human Resources, Human Resources Director, same companies (the approved exception) | 696 people. Total about 933 before the "no VP-level HR leader" rule |
| 1 The Seat That Won't Close | Companies: manufacturing industries, all US 201-1000 | 8,729 companies (base pool) |
| 1 The Seat That Won't Close | Companies: same, plus `hiring.job_titles` Plant Manager, General Manager, Director of Operations, Engineering Manager, Quality Manager, Supply Chain Manager, Controller, HR Manager | Blitz returned no total (`null`). 3 shown, saved in `seat-that-wont-close-preview/2026-11-13-companies.csv`. The 60+ day / repost signal needs Claygent |
| 2 New Site, New Leaders | Not counted | The signal (new site, acquisition, ERP rollout in the last 9 months) can only be found by Claygent / news search. No Blitz filter exists |

**Decision:** the two largest measurable pools, Campaign 5 (about 3,132) and Campaign 3 (about 3,066), were set up first as drafts in tracking_clients and HeyReach. Campaign 4 (about 933) is third. Campaigns 1 and 2 can't be sized until a signal run.

**Per-company depth (CLAUDE.md TAM/SAM rule):** the doc sets it, and this preview supports it. Fire & life safety is a small TAM (334 companies on the tight keywords), so up to 3-4 contacts per company. Manufacturing is a large TAM (8,729 companies), so 1-2 contacts per company.

Blitz counts are indicative (see the CLAUDE.md accuracy warning).
