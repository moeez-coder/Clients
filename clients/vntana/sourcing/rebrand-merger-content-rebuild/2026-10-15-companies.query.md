# Rebrand, Merger, Content Rebuild — sourcing run (2026-10-15)
Client VNTANA `5e0a22cf-6efb-432d-bc3c-6eb914440f13`. tracking_clients campaign `62cbf47f-1722-426a-a249-ed838420cd55` (status `creation`), sourcing config `98e470eb-7d7d-446c-b9e6-d78e059b7c5e` (draft, 0 companies there), ICP `58e82133-9747-40bf-8056-010b3e510485`. **New segment** (new config-slug folder `rebrand-merger-content-rebuild`).
Trigger per brief: rebrand/name change in the last 6 months, or an acquisition closed in the last 12 months where both sides sell physical product; industrial manufacturers $250M+.

## Steps
1. Signal search: Exa `POST /search` (`category: news`, `numResults` 100, per-result summary) — 72 queries (18 verticals x rebrand / rename / acquisition-completed / brands-combined phrasings). Rebrand window from 2026-04-15, acquisition window from 2025-10-15 -> 7,178 results, 3,814 unique articles.
2. Company match: article title + first 400 chars of summary matched (case-sensitive, distinctive-name rule) against universe companies (`icp-universe-na-weu`, universe_status IN, employee band 501+ as the $250M proxy) -> 1,325 company/article pairs, 368 companies.
3. Event check: 31 Haiku agents, one company per line with up to 3 article summaries (no web; spec `SPEC_E.md`): event = rebrand / brand_consolidation / acquisition_closed / acquisition_pending / none, plus both-sides-physical-product. Kept rebrand, brand_consolidation, acquisition_closed with physical_both = true and event_date inside the window (4 dropped as older) -> **188 companies**.
4. People: Blitz `POST /v2/search/employee-finder` (levels C-Team/VP/Director; Advertising & Marketing + General Business; US/CA/GB/CH/NO/EU27; 3 pages) classified by title (T1 CMO/VP brand/marcom/communications, T2 director brand/communications/marketing communications); up to 4 per company (small TAM -> more people). Gap-fill for companies with none: Prospeo `POST /search-person` by domain (only rows whose company domain matched).
## Result
188 accounts; 219 prospects at 104 companies (84 accounts have no contact yet). Events: acquisition_closed 126, brand_consolidation 37, rebrand 25. Size: 501-1000 = 39 (revenue not verified), 1001+ = 149.
## Messaging columns (for Clay)
Approved copy is rebrand-only. Rows with event_type rebrand/brand_consolidation carry the approved Message 1-3 rendered (`copy_variant=approved_rebrand_copy`). Acquisition rows (149 prospects) carry a **DRAFT variant written from the approved angle text, not approved**. `{{video_link}}` (the 3-minute recorded walkthrough, offer E) and `{{meeting_link}}` are left as placeholders; `video_link` column is `-` per company until the walkthrough is recorded.
## Limits
- Matching is name-based; agents flagged several name collisions (set to none) but some parent/subsidiary matches (e.g. a group event credited to a listed subsidiary) remain judgement calls. Several articles are republished older events; event_date is `-` for 5 companies where no date was given (`event_date_unknown=yes`).
- Revenue $250M+ is proxied by headcount band; 501-1000 rows flagged.
- Exa news coverage is skewed to press-release wires; rebrands announced only on company sites will be missed.
