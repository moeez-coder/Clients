# Clients

Sourcing-data workspace for Algo Acquisition's cold outbound campaigns. One folder per client under `clients/`, holding the client's profile, active ICPs/sourcing configs, and dated snapshots of any sourced company/lead data pulled out of the sourcing tools below into version control.

## Structure

```
clients/<client-slug>/
  README.md                        Client profile + sourcing configs (ICP, market, status, Clay workbook link)
  sourcing/
    <config-slug>/
      <YYYY-MM-DD>-companies.csv    Company-level export for that sourcing config, snapshotted on the pull date
      <YYYY-MM-DD>-leads.csv        Contact-level export for that sourcing config, when available
```

## Conventions

- **Client folders** are a lowercase, hyphenated slug of the client's name in the tracking system (e.g. `s3-partners`, `vntana`).
- **Sourcing configs** are the individual ICP-targeted sourcing runs tracked per client (one client can run several in parallel — different segments or markets). Each config's `company_count` in its README table reflects how many companies had landed in the tracking system as of the last sync — most sourcing still lives in each config's linked Clay workbook, or hasn't been pulled from the sourcing tools yet.
- **Dated snapshots**: every time you pull a fresh export for a config, add it as a new `<YYYY-MM-DD>-companies.csv` / `<YYYY-MM-DD>-leads.csv` file under that config's folder rather than overwriting the previous pull — this keeps a history of how a list grew or changed over time. The most recent date is the current list.
- New clients: add a folder following this same pattern (`README.md` + `sourcing/`), and pull the client's profile from the `tracking_clients` MCP server as the source of truth.
- `algoacquisition/` is Algo's own internal/test workspace, not an external client — kept here for consistency since it's tracked the same way.

## Sourcing tools available to this repo

Company/lead data going into `sourcing/` can come from any of these, per config:

- **Blitz API** (`https://api.blitz-api.ai`, auth via `x-api-key`, key in the `BLITZ_API_KEY` session env var) — the primary live sourcing API. Agency Premium plan. Endpoints: `/v2/search/companies`, `/v2/search/people`, `/v2/search/employee-finder`, `/v2/search/waterfall-icp-keyword` / `waterfall-icp`, `/v2/jobs/search` + `/v2/jobs/company`, `/v2/enrichment/*` (email, phone, company, domain↔linkedin), `/v2/company/tam-by-jobs`. Call it directly over HTTPS — the `Blitz-API` MCP tool in this session only searches Blitz's documentation, it does not proxy live requests.
- **Clay** (`mcp__Clay__*`) — company/contact find-and-enrich tools plus this workspace's configured custom subroutines.
- Sourcing configs whose brief mentions Prospeo, DiscoLike, EXA, or Sales Navigator name tools not wired into this session; run those steps wherever they are connected and bring the resulting export back here.

## Source of truth

Client and campaign metadata lives in the `tracking_clients` MCP server (client profiles, ICP configs, sourcing configs, campaign status). This repo is a working export layer on top of it for sourcing data specifically — re-sync a client's `README.md` from the MCP server if its configs change, and re-pull `get_sourcing_companies` / `get_sourcing_leads` for a config once data lands there (both were empty for leads across every config checked as of the last sync).
