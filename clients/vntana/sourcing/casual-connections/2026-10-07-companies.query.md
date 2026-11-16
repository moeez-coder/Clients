# Casual Connections, from Ashley — hand-picked founders/CEOs/GMs list (2026-10-07)
Client VNTANA `5e0a22cf-6efb-432d-bc3c-6eb914440f13`. tracking_clients campaign **"Casual Connections, from Ashley"** `34299ef0-93d5-48d6-9f70-bf66e094050b` (status `creation`, LinkedIn only, sender = Ashley's own profile, no HeyReach campaign yet); sourcing config **"Hand-picked founders/CEOs/Presidents/GMs at industrial manufacturers (no trigger)"** `aa644575-d5c1-4b1a-8540-dcdbe165a121` (draft, 0 companies in tracking_clients); ICP `cc11c80b-854d-4ca9-912f-5478cdb44b09`. **Expanding existing segment** folder `casual-connections` (the older config `dbb5b88a-d5f8-46fa-9611-c9f29598b4d6`, 741 companies, 2026-09-15 files, is a different sourcing config for the same idea).

## Steps
1. Universe: `icp-universe-na-weu/2026-09-29-companies.csv` universe_status=IN (32,792; headcount >200, no fashion/apparel), HQ in US/CA/GB/CH/NO/EU27, tagged to a target vertical, fit_level RULE_VERTICAL/FIT/CLIENT_VERDICT -> 12,150 companies.
2. Hand-picking score: +2 core campaign vertical (construction/ag/mining, cranes/material handling, trucks/trailers, HVAC, power equipment, hydraulics/power transmission, pumps/valves), +1 other target vertical (automation, machine tools, robotics, packaging/process, components), +3/+2/+1 for a verified 50+/unpublished/under-50 dealer network (campaign 10 tiers), +3/+2 client IMTS verdict Yes/Near-ICP, +2 for 501-5,000 employees (+1 for 201-500), +1 multi-vertical, +1 rule-based vertical. Top 1,800 taken.
3. People: Blitz `POST /v2/search/employee-finder` (`x-api-key`, UA curl/8.5.0), `job_level` C-Team + VP, `job_function` General Business & Management, person country US/CA/GB/CH/NO/EU27, <=2 pages x 50 -> 3,529 rows, 1,800 companies searched, 1 call errored.
4. Title filter (current role at that company only): founder/co-founder/company owner (tier founder_owner), CEO/Managing Director/President/Geschäftsführer (ceo_president_md), General Manager/division or business-unit head (gm_division_head). Excludes VP/deputy/assistant/PA-to, functional chiefs, "App/Product/Process Owner". 837 companies had one.
5. Manufacturer check: Haiku web agents on the top 510 (34 batches planned). **WebFetch was rate-limited for most agents, so only 21 batches ran and most answers are "unverified".** Rules used: agent-verified non-manufacturers (dealer/distributor/services/consumer) excluded; otherwise earlier campaign-10 qualification (OEM verified; DEALER/FINANCE excluded); everything else kept and flagged `manufacturer_check=unverified`.
6. One contact per company (CEO/president preferred; next two senior contacts in `other_senior_contacts`), ranked by score. Top 400 = `primary` (the hand-picked list); remainder = `reserve`.
7. Copy: the 5 options from the campaign record, assigned round-robin within each vertical so each option is tested in each segment (`copy_option`); `connection_note` and `follow_up` are rendered with first name and cleaned company name (legal suffixes stripped). Two touches only, no link, no pitch.

## Result
- 814 companies / 814 contacts: 400 primary + 414 reserve. Primary: 286 verified manufacturers, 114 unverified; seniority CEO/President/MD 342, founder/owner 57, GM/division head 1; US 220, DE 41, IT 23, FR 19, GB 19, CH 13.
- Copy option split in primary: 1:86, 2:83, 3:80, 4:77, 5:74.

## Limits
- Division heads are barely represented (1): employee-finder's General Business & Management function rarely tags them. A division-head pull needs a different title search.
- 114 primary companies are not web-verified as manufacturers; Blitz/LinkedIn data can be wrong about founders vs. current CEO. Eyeball before launch.
- Contacts are US/CA/UK/CH/NO/EU27 (the universe geography); no geography was specified for this campaign.
- The older 741-company `casual-connections` pull and the dealer campaign's contacts were not de-duplicated against this list beyond one-person-per-company.
