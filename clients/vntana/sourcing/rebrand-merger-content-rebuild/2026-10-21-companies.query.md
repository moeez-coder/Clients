# Rebrand, Merger, Content Rebuild — wide company count (2026-10-21)
Client VNTANA `5e0a22cf-6efb-432d-bc3c-6eb914440f13`; campaign `62cbf47f-1722-426a-a249-ed838420cd55`; sourcing config `98e470eb-7d7d-446c-b9e6-d78e059b7c5e`. **Expanding existing segment** `rebrand-merger-content-rebuild` (companies only; no new contacts pulled). Asked: how many industrial manufacturers, $250M+, with a rebrand, brand consolidation, name change, or an acquisition bringing multiple product brands together. Windows: rebrand/rename from 2026-04-15; consolidation and closed deals from 2025-10-15.

## Steps
1. Exa `POST /search` (category news, summaries): 750 queries = 30 industrial verticals x (5 rebrand/rename/consolidation phrasings x 2 date windows + 5 acquisition/merger phrasings x 3 date windows), 100 results each -> 74,949 raw, 32,288 unique articles (incl. the 3,814 from 2026-10-15).
2. Filters: event keyword + industrial keyword + de-junk + title de-dup -> 21,307; then a strong-event-in-headline filter -> **3,227 articles** read by 81 Haiku agents (no web; spec `SPEC_X.md`): subject manufacturer, event (rebrand / rename / brand_consolidation / acquisition_closed / merger_closed / pending / none), counterparty, date, industrial, both-sides-physical for deals.
3. Kept industrial subjects with event inside the window (deals only when both sides physical) -> 714 unique companies.
4. Sizing: Prospeo `POST /search-company` (names filter; second pass with suffix-stripped name variants) -> revenue range, employee count, domain, LinkedIn URL.
5. Merged with the 2026-10-15 universe-matched run (188 companies, sized by headcount band only).

## Count (see `2026-10-21-companies.csv`, `size_tier`)
- **A** revenue range min >= $250M (Prospeo): 218
- **B** revenue range straddles $250M: 14
- **C** no revenue figure but 1,000+ employees: 15
- **E** extra from the 2026-10-15 run, 1,001+ headcount band, not matched in this run: 112
- => **359 companies likely at $250M+ with a qualifying event** (A+B+C+E). Of the 247 from this run's events: 176 acquisition_closed, 40 rebrand, 32 brand_consolidation, 4 merger_closed, 3 rename (a company can have several).
- Size unverified (kept in file, not counted): 220 not found in Prospeo, 7 with 500-999 employees and no revenue, 6 unknown size, 112... (E is counted above). Excluded as too small: 138 under 500 employees, 96 revenue below $250M.

## Limits
- Recall: only the 3,227 headline-strong articles were read; ~8,000 more with the event only in the summary were not. Exa news skews to press-release wires; company-site announcements are underrepresented.
- Precision: events were extracted from titles/summaries by a small model without opening articles; parent/subsidiary and name-collision calls are judgement. Several articles re-report old deals (checked by stated date, not always stated).
- "Acquisition bringing multiple product brands together" is not separately verified — any closed manufacturer-to-manufacturer deal is counted (the 176). A stricter brand-portfolio read would cut that number.
- Prospeo revenue is a banded estimate.
