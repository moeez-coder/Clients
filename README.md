# Clients

Sourcing-data workspace for Algo Acquisition's cold outbound campaigns. One folder per client under `clients/`, holding the client's profile, active ICPs/sourcing configs, and any sourced company/lead data that has been exported out of the sourcing pipeline (Clay, job scrapers, DiscoLike, Sales Navigator, etc.) into version control.

## Structure

```
clients/<client-slug>/
  README.md          Client profile + sourcing configs (ICP, market, status, Clay workbook link)
  sourcing/
    *.csv             Exported company/lead lists for configs that have sourced data
```

## Conventions

- **Client folders** are named as a lowercase, hyphenated slug of the client's name in the tracking system (e.g. `s3-partners`, `vntana`).
- **Sourcing configs** are the individual ICP-targeted sourcing runs tracked per client (one client can run several in parallel, e.g. different segments or markets). Each config's `company_count` reflects how many companies have actually landed in the tracking system as of this snapshot — most sourcing still lives in each config's linked Clay workbook until it's pulled in here.
- **`sourcing/*.csv`** files are point-in-time exports. When you pull a fresh export for a config, overwrite the corresponding CSV (or add a dated variant if you need to keep history) rather than appending in place.
- New clients: add a folder following this same pattern (`README.md` + `sourcing/`), and pull the client's profile from the `tracking_clients` MCP server as the source of truth.
- `algoacquisition/` is Algo's own internal/test workspace, not an external client — kept here for consistency since it's tracked the same way.

## Source of truth

Client and campaign metadata lives in the `tracking_clients` MCP server (client profiles, ICP configs, sourcing configs, campaign status). This repo is a working export layer on top of it for sourcing data specifically — re-sync a client's `README.md` from the MCP server if its configs change.
