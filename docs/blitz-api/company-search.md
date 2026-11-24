# Blitz API — Company Search (`POST /v2/search/companies`)

Pulled verbatim from Blitz's OpenAPI spec (`/openapi/api-reference/v2.openapi.json`
in the Blitz-API MCP's docs filesystem) on 2026-09-24 — do not hand-edit this
file from memory; re-pull the same way if Blitz's schema drifts. This exists
because an earlier session guessed filter param names (`employee_count_min`,
`country`) and got a `200` with silently-wrong results — the API doesn't
validate unknown fields away, it just ignores them.

Base URL: `https://api.blitz-api.ai`. Auth: `x-api-key` header,
`BLITZ_API_KEY` session env var. Call directly over HTTPS — the `Blitz-API`
MCP tool only searches Blitz's own docs, it does not proxy live requests.

## Top-level request body

| Field | Type | Default | Notes |
|---|---|---|---|
| `company` | object | — | Company search criteria (see below) |
| `cursor` | string \| null | `null` | Pagination cursor. `null` = first page; a `null` cursor in the *response* means end of results. |
| `max_results` | number | `10` | 1–50 |

## `company.*` fields

All filters combine with **AND**; multiple values within one filter's
`include`/`exclude` list combine with **OR**.

| Field | Type | Notes |
|---|---|---|
| `name.include` / `name.exclude` | `string[]` | Keyword match on company name |
| `industry.include` / `industry.exclude` | `enum<string>[]` | **Exact match only** — 534 canonical values, see `company-search-industries.txt` in this folder. A near-miss (e.g. `"Software"` instead of `"Software Development"`) silently returns 0 results, it does not error. |
| `type.include` / `type.exclude` | `enum<string>[]` | `Educational`, `Educational Institution`, `Government Agency`, `Nonprofit`, `Partnership`, `Privately Held`, `Public Company`, `Self-Employed`, `Self-Owned`, `Sole Proprietorship` |
| `employee_range` | `enum<string>[]` | Exact bucket match: `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1001-5000`, `5001-10000`, `10001+` |
| `employee_count.min` / `.max` | `number` | Free-form range on LinkedIn employee count (0–980000 min, 0–1000000 max). `0` = unset. **Use this OR `employee_range`, not made-up param names like `employee_count_min`.** |
| `min_linkedin_followers` | `number` | 0–10,000,000 |
| `revenue.min` / `.max` | `number` (USD) | 0–9.01e15. Matched as range *intersection* against the company's revenue band. |
| `web_traffic.min` / `.max` | `number` (monthly visits, est.) | 0–2.15e9 |
| `ad_spend.min` / `.max` | `number` (USD/month on Google Ads, est.) | 0–1e12 |
| `total_funding.min` / `.max` | `number` (USD) | 0–2,147,483,647 |
| `last_funding_amount.min` / `.max` | `number` (USD) | 0–2,147,483,647 |
| `last_funding_year.min` / `.max` | `number` | 1800–2026 |
| `last_funding_type.include` / `.exclude` | `enum<string>[]` | `Series unknown`, `Pre seed`, `Seed`, `Series A`–`Series D`, `Series E-J`, `Grant`, `Angel`, `Private equity`, `Debt financing`, `Non equity assistance`, `Post IPO equity`, `Undisclosed`, `Post IPO debt`, `Product crowdfunding`, `Equity crowdfunding`, `Corporate round`, `Convertible note`, `Secondary market`, `Initial coin offering`, `Post IPO secondary` |
| `lead_investors.include` / `.exclude` | `string[]` | Keyword match on lead investor name |
| `naics_code.include` / `.exclude` | `string[]` | Exact NAICS code match |
| `sic_code.include` / `.exclude` | `string[]` | Exact SIC code match |
| `keywords.include` / `.exclude` | `string[]` | Matched across company description, specialties, NAICS/SIC descriptions, and Crunchbase/G2 categories. A phrase matches if all its tokens are found within any one of those fields. |
| `founded_year.min` / `.max` | `number` | Year range |
| `hq.city.include` / `.exclude` | `string[]` | Keyword match, HQ city |
| `hq.state.include` / `.exclude` | `string[]` | Keyword match, HQ state/province |
| `hq.country_code` | `string[]` | 2–3 letter ISO country codes (**no `include`/`exclude` split — flat array**; note this differs from the pattern used everywhere else in this schema) |
| `hq.continent` | `enum<string>[]` | `Africa`, `Antarctica`, `Asia`, `Europe`, `North America`, `Oceania`, `South America` |
| `hq.sales_region` | `enum<string>[]` | `NORAM`, `LATAM`, `EMEA`, `APAC` |

## Example request

```json
{
  "company": {
    "industry": { "include": ["Software Development"] },
    "employee_count": { "min": 50, "max": 200 },
    "hq": { "country_code": ["US"] }
  },
  "max_results": 20,
  "cursor": null
}
```

## Related endpoints sharing the same `company` filter object

Per Blitz's own docs: **Find People** (`POST /v2/search/people`) accepts the
exact same `company` filter object shown above, plus a `people` filter
object — no need to chain Company Search → Employee Finder if you need
people directly. See the `Blitz-API` MCP docs-search tool for that schema
when needed (query: "find people top-level parameters").
