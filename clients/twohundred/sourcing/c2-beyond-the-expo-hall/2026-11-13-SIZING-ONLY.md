# C2 Beyond the Expo Hall: sizing only, NOT sourced yet (2026-11-13)

**Not sourced.** The gating signal is "sponsored, exhibited at or spoke at a Nordic/NL B2B tech or executive event in the last 12 months." Blitz has no event-sponsorship data, and the Clay MCP was disconnected this session (503). Without that signal, any lead list would be the whole vendor universe with empty `event_name`/`event_city`, so no leads were written.

## Sizing (Blitz)
- Base universe = vendors in the five community categories (software, IT services, security, data, finance, HR), 501+ employees, with a Nordic/NL GTM leader: **~16,700 Nordic GTM leaders across several thousand vendors** (`/v2/search/people`, `/v2/company/tam-by-people`).
- The event filter would cut this to a much smaller set, probably a few hundred companies, but that number can't be known without the event research.

## To source it
1. Verify the event signal per company (Clay/Claygent over sponsor pages, speaker lists, press releases, or an events dataset), returning `event_name`, `event_city`, `event_month` + source URL.
2. Keep only companies with a verified event, then pull 2-3 Nordic/NL marketing and country leaders each (as in C5/C7).
