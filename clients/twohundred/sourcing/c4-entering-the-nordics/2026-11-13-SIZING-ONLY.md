# C4 Entering the Nordics: sizing only, NOT sourced yet (2026-11-13)

**Not sourced.** The gating signal is "visible signs of entering or expanding in DK/SE/NO/FI/NL in the last 9 months: a new office or entity, a new country lead, a new reseller/partner, or first named Nordic/Dutch customers." The doc explicitly excludes job postings here. Blitz has no expansion-news data, and the Clay MCP was disconnected this session (503), so no leads were written (they would all carry an empty `expansion_short`).

## Sizing (Blitz)
- Base universe is the same shared vendor set as C2: **~16,700 Nordic GTM leaders across several thousand vendors**. The expansion filter would cut this to the companies with a fresh expansion event.
- Partial proxy already in the repo: C3 (new-in-seat Nordic commercial leaders, 54 leads) and C9 (vendors hiring Nordic country/sales leadership, 70 leads) overlap this intent and ARE sourced. A pure C4 expansion-news list still needs the research step below.

## To source it
1. Verify an expansion event per company (Clay/Claygent or a news dataset over the last 9 months), returning `expansion_short` (a 3-8 word phrase) and `country` + source URL.
2. Keep only companies with a verified event, then pull 2-3 EMEA/Nordic sales and marketing leaders each.
