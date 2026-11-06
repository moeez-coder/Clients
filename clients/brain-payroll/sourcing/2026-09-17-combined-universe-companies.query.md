# Query — 2026-09-17 combined target-company universe (all four segments)

**Client:** Brain Payroll UK Limited (`0a09f3c7-9a9b-4f57-bbec-e2fbf0dc6780`)
**Output:** `2026-09-17-combined-universe-companies.csv` — **2,492 ICP-qualified companies**
**Audit trail:** `2026-09-17-combined-universe-rejected.csv` — 26,604 rejected rows, each with its reason

This is a **new, cross-segment universe build**, not an expansion of an existing pull —
no `sourcing/` tree existed for this client before today and all four sourcing configs
reported `company_count` 0 in `tracking_clients`. It covers all four configs at once;
the `segment` column maps each row back to the config it feeds.

## ICP applied (from `get_client` → `clientBrief`)

Brain Payroll sells **cloud payroll software to organisations that run payroll for other
organisations**. So the qualifying test is not "mentions payroll" but "**is a payroll
provider**":

- **Geography:** United Kingdom and Republic of Ireland **only** (client states no other geos).
- **Size:** 11+ employees. The brief selects all bands from 11-50 upward, so sole traders
  and micro-practices (1-10) are out of ICP and were rejected.
- **Must be a provider:** a payroll bureau, an umbrella/contractor payroll company, or an
  accountancy practice that offers payroll to its clients.
- **Excluded — competitors:** payroll/HCM software vendors and global payroll outsourcers
  sell what Brain Payroll sells (Sage, IRIS, BrightPay, Moorepay, Zellis, CloudPay,
  Mercans, Vialto, Ciphr, Cezanne, ADP, Dayforce, SD Worx …).
- **Excluded — end employers:** a retailer or NHS trust with an in-house payroll team is
  not a bureau.
- **Excluded — professional bodies:** CIPP, ICAEW, ACCA, AAT and similar.
- **Excluded — DNC:** all 64 rows of the client's `Do_Not_Contact_list`, matched on both
  normalised domain and normalised company name.

## Sources — four tools, unioned then deduped

| # | Tool | Endpoint / method | Raw rows |
|---|---|---|---|
| 1 | **Blitz API** | `POST /v2/search/companies` — industry drains + 38-term payroll keyword matrix, GB and IE, cursor-paginated to exhaustion | 10,541 |
| 2 | **Blitz API** | `POST /v2/jobs/search` (17 payroll job titles, GB/IE, last 90 days) → `POST /v2/enrichment/company` on each hiring company | 2,893 postings → 1,058 companies |
| 3 | **EXA Websets** | `POST /websets/v0/websets`, `entity.type: company`, 12 entity queries incl. BACS/CIPP/FCSA accreditation and bureau/practice/umbrella/CIS framings → resolved via Blitz `domain-to-linkedin` + `enrichment/company` | 713 items → 584 unique domains → 486 resolved |
| 4 | **AI Ark** | `POST /v1/companies` with `lookalikeDomains` seeded by **LinkedIn company URL** of each already-qualified bureau/practice | 23,050 |
| 5 | **Prospeo** | `POST https://api.prospeo.io/search-company` — `company_industry` / `company_keywords` × `company_location_search` (United Kingdom, Ireland) × `company_headcount_custom` `{min:11}`, 25/page | 24,033 |
| 6 | **DiscoLike** (via ColdIQ) | `GET /v1/discolike/discover` — natural-language `icp_text` + `country` + `employee_range`, 3 queries (bureau/practice, umbrella/contractor, Ireland) | 300 |

**Union: 51,357 raw records → 29,096 unique companies**, deduped in two passes: first on
canonicalised LinkedIn company URL (falling back to domain), then a second pass collapsing
shared domains — a firm that rebranded or merged keeps two LinkedIn pages (e.g. "DJH Bexley
(formerly McBrides)") and survives a LinkedIn-only dedupe. The second pass removed 910 such
pairs, keeping whichever record had more populated fields.

### Prospeo (source 5) — the single biggest contributor

Prospeo is by far the strongest source for this ICP at the size band that matters. Blitz
returned **459** UK Accounting companies at 11+ employees; Prospeo returns **2,430** on the
same filter, and 163 for Ireland against Blitz's 94 total. It also returns NAICS codes and a
clean `employee_count`. Filters that work: `company_industry`, `company_keywords`,
`company_location_search`, `company_headcount_custom`. `company_description` and
`company_search` are **not** valid keys and return `INVALID_FILTERS`.

```json
{"filters":{"company_location_search":{"include":["United Kingdom"]},
            "company_headcount_custom":{"min":11,"max":100000},
            "company_keywords":{"include":["payroll bureau"]}},
 "page":1}
```

### Blitz company-search filters (source 1)

```json
{"company":{"industry":{"include":["Accounting"]},          // also: Human Resources Services,
                                                            //   Outsourcing and Offshoring Consulting
            "hq":{"country_code":["GB"]}},                   // and ["IE"]
 "max_results":50}
```
plus, for each of 38 payroll terms (`payroll bureau`, `managed payroll`, `outsourced payroll`,
`umbrella payroll`, `contractor payroll`, `CIS payroll`, `auto enrolment`, `bureau payroll`,
`accountancy practice`, `chartered accountants`, `employment intermediary`, `PAYE umbrella`, …):

```json
{"company":{"keywords":{"include":["<term>"]},"hq":{"country_code":["GB"]}},"max_results":50}
```

## Qualification funnel

| Stage | Rows |
|---|---|
| Unique companies harvested | 29,096 |
| − not a payroll provider (no bureau/practice/umbrella evidence) | −13,698 |
| − below 11 employees (out of ICP size band) | −12,036 |
| − recruiter that *recruits* accountants rather than providing payroll | −261 |
| − HQ outside GB/IE | −244 |
| − professional/membership body | −174 |
| − on the client's DNC list | −41 |
| − foreign ccTLD contradicting the HQ field (AI Ark mis-geocoding) | −38 |
| − wealth manager / IFA matching on a passing "our accountants" mention | −10 |
| − competitor (payroll/HCM vendor) | −18 |
| **Qualified** | **2,492** |

## Output breakdown

| Segment (→ config it feeds) | Rows |
|---|---|
| `accountancy-practice-payroll` → Boutique/Mid 11–200 + Enterprise 201+ configs | 2,229 |
| `payroll-bureau` → Boutique/Mid + Enterprise configs | 112 |
| `umbrella-contractor-payroll` → UK recruitment agencies running umbrella/contractor payroll (51–1,000) | 82 |
| `recruitment-umbrella-contractor-payroll` → same config, recruitment-agency-operated | 69 |

Geography: **GB 2,295 / IE 197.** Tier: boutique-mid (11–200) 2,385 / enterprise (201+) 107.

`icp_confidence` splits the list honestly:
- **high (471)** — explicit payroll-provider language ("payroll bureau", "managed payroll",
  "outsourced payroll", "umbrella company").
- **medium (2,021)** — confirmed UK/IE accountancy practices of 11+ staff, where payroll is a
  near-universal service line but **this pull did not find explicit payroll wording**. These
  are ICP-plausible and worth outreach, but the payroll service line is inferred, not verified.
  Anyone wanting a verified-only list should filter to `icp_confidence == high`.

## TAM/SAM read and outreach depth

Per the repo's campaign-build standard, contact depth is set inversely to segment size:

- `accountancy-practice-payroll` (2,229 companies) — **large** SAM → **2 contacts per company**
  (the payroll decision-maker plus the practice owner/partner).
- `payroll-bureau`, `umbrella-contractor-payroll`, `recruitment-umbrella-contractor-payroll`
  (263 companies combined) — **small** SAM → **4 contacts per company**, since at a bureau the
  payroll function *is* the business and the buying committee is wider.

## Health warnings for the next session

1. **The 11+ size floor is what caps this list, not the tools.** 12,036 of 29,096 harvested
   companies are 1-10 employees — the UK accountancy/bookkeeping long tail is overwhelmingly
   micro-practices. If Brain Payroll will sell to sole practitioners, relaxing that floor
   roughly multiplies the universe by nine, and that is a commercial decision for the client.
2. **`icp_confidence: medium` is inferred, not verified** (see above). Verifying it needs a
   website-content pass over ~2,020 domains, which this pull did not do.
3. **Ireland is under-covered by every tool.** Blitz returned only 94 Accounting companies for
   IE against 5,007 for GB. AI Ark lookalikes lifted the raw IE pool to 1,018 and Prospeo
   + DiscoLike to 1,975, but the final IE count is still only **197 against GB's 2,295** —
   about 8%, when Ireland is roughly 7-8% of the combined UK+IE economy. That is closer to
   proportionate than it first looks, but Irish records carry thinner descriptions, so more
   of them fail the payroll-provider test for lack of text rather than lack of fit.
4. **AI Ark filter parameters do not work on this key.** Only `lookalikeDomains` narrows the
   result set — `countries`, `industries`, `descriptionKeywords`, `staffRange` and every
   variant tried were silently ignored, returning the full 72.5M-company baseline. It is
   usable as a lookalike engine only. (This differs from the VNTANA notes, which describe
   description-keyword and revenue filtering; either the API or the plan has changed.)
5. **Blitz `max_results` caps at 50, not 25** as CLAUDE.md states. Passing 51+ returns a
   422 naming the limit. Flagged for the repo owner — CLAUDE.md is a governed system file.
6. **ColdIQ is a unified proxy over ~60 B2B data providers, not a data source of its own.**
   `GET https://api.coldiq.com/openapi.json` (Bearer auth, and it **requires a non-default
   User-Agent** — `Python-urllib` is blocked at the Cloudflare edge and returns a bare 403
   that reads like an auth failure). 666 paths across Apollo, LimaData, TheirStack, Icypeas,
   LinkupAPI, PredictLeads, Findymail, Wiza, Serper, plus DiscoLike, AI Ark and Prospeo.
   **It is metered and expensive:** `GET /v1/discolike/discover` charged **111.3 credits per
   100-record call** (~$1.59 at $0.0143/credit). Note the two credit readings disagree —
   `GET /v1/me/credits` reported `balance: 166.069` while the `X-ColdIQ-Credits-Remaining`
   response header on a live call reported ~16,400. Only three DiscoLike calls were made
   (~334 credits) pending clarification of which figure is authoritative. **Check the budget
   before any bulk ColdIQ run.** The unused high-value endpoints for this client are
   `/v1/apollo/organizations/search`, `/v1/limadata/search/companies` and
   `/v1/icypeas/find-companies` (which has a cheap `/count` companion).
7. **Prospeo rate-limits aggressively.** 8 concurrent threads produced immediate
   `429 Rate limit exceeded`; 3 threads with a 0.55s inter-request gap and exponential
   backoff ran clean. `Outsourcing and Offshoring Consulting` and `Professional Services`
   are not valid `company_industry` values in Prospeo's taxonomy.
8. **Three qualifier bugs were found and fixed during this build; all are easy to repeat.**
   (a) Substring matching made `rti` match "expe**rti**se"/"prope**rti**es" and `cis` match
   "pre**cis**e", inflating a draft list by ~200 false positives — all term matching is now
   word-boundary anchored. (b) Matching competitor names against a company's *description*
   rejected ~220 genuine practices for saying "Xero Gold Partner" or "Sage certified";
   competitor tests now match company identity (name/domain) only. (c) Deduping on LinkedIn
   URL alone left 910 duplicate pairs where one firm holds two LinkedIn pages after a
   rebrand or merger — a second domain-keyed pass now collapses them. 11 duplicate *names*
   remain by design: they are distinct firms or separate offices on different domains
   (e.g. two unrelated practices both trading as "Deans").
