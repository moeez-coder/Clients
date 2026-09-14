# <Client Name>

<!--
Template for a new client folder. Copy this file to clients/<client-slug>/README.md,
fill it in from the tracking_clients MCP server (get_client, list_sourcing_configs),
then delete this comment block. See /CLAUDE.md at the repo root for the full
documentation/referencing standard this template implements — every section below
is required, not optional.
-->

## Profile

- **Status:** <active | paused | ...>
- **Package tier:** <Standard | Custom | ...>
- **Website:** <url>
- **Contact:** <name> <<email>>
- **Slack channel ID:** <C...>
- **Tracking client ID:** `<uuid from tracking_clients>`
- **Last synced:** <YYYY-MM-DD> via `get_client` + `list_sourcing_configs`

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| <config name> | <icp> | <market> | <draft/ready/...> | <n> | <n> | [link](<url>) or `-` |

## Sourced data in this repo

<!--
One line per file under sourcing/. Update in the same commit that adds the
file. This includes Clay-sourced pulls, not just direct API calls — a Clay
workbook link is a pointer to where the config lives, not a substitute for
exporting what's in it. Every -leads.csv must have `linkedin_url` (the
prospect's full LinkedIn profile URL) as its first column and unique key.
-->

- `sourcing/<config-slug>/<YYYY-MM-DD>-companies.csv` — <row count> companies from **<config name>** (config `<uuid>`), pulled via <tool + endpoint/subroutine>
- `sourcing/<config-slug>/<YYYY-MM-DD>-leads.csv` — <row count> prospects from **<config name>** (config `<uuid>`), pulled via <tool + endpoint/subroutine>, keyed by `linkedin_url`

## History

<!--
Reverse-chronological log. One entry per meaningful change to this folder:
profile resyncs, new sourcing pulls, config edits. State the reasoning, not
just the action — a future session should understand *why* without asking.
-->

- **<YYYY-MM-DD>** — Folder created; profile synced from `tracking_clients`.
