# Query — 2026-09-17 combined target-company universe (all four segments)

**Client:** Brain Payroll UK Limited (`0a09f3c7-9a9b-4f57-bbec-e2fbf0dc6780`)
**Output:** `2026-09-17-combined-universe-companies.csv` — **1,442 ICP-qualified companies**
**Audit trail:** `2026-09-17-combined-universe-rejected.csv` — 15,597 rejected rows, each with its reason

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

**Union: 27,333 raw records → 17,039 unique companies** (deduped on canonicalised LinkedIn
company URL, falling back to domain).

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
| Unique companies harvested | 17,039 |
| − below 11 employees (out of ICP size band) | −12,279 |
| − not a payroll provider (no bureau/practice/umbrella evidence) | −2,705 |
| − HQ outside GB/IE | −261 |
| − recruiter that *recruits* accountants rather than providing payroll | −177 |
| − professional/membership body | −99 |
| − on the client's DNC list | −36 |
| − foreign ccTLD contradicting the HQ field (AI Ark mis-geocoding) | −7 |
| − competitor (payroll/HCM vendor) | −11 |
| **Qualified** | **1,442** |

## Output breakdown

| Segment (→ config it feeds) | Rows |
|---|---|
| `accountancy-practice-payroll` → Boutique/Mid 11–200 + Enterprise 201+ configs | 1,306 |
| `payroll-bureau` → Boutique/Mid + Enterprise configs | 49 |
| `recruitment-umbrella-contractor-payroll` → UK recruitment agencies running umbrella/contractor payroll (51–1,000) | 45 |
| `umbrella-contractor-payroll` → same config, non-recruitment umbrellas | 42 |

Geography: **GB 1,285 / IE 157.** Tier: boutique-mid (11–200) 1,358 / enterprise (201+) 84.

`icp_confidence` splits the list honestly:
- **high (291)** — explicit payroll-provider language ("payroll bureau", "managed payroll",
  "outsourced payroll", "umbrella company").
- **medium (1,151)** — confirmed UK/IE accountancy practices of 11+ staff, where payroll is a
  near-universal service line but **this pull did not find explicit payroll wording**. These
  are ICP-plausible and worth outreach, but the payroll service line is inferred, not verified.
  Anyone wanting a verified-only list should filter to `icp_confidence == high`.

## TAM/SAM read and outreach depth

Per the repo's campaign-build standard, contact depth is set inversely to segment size:

- `accountancy-practice-payroll` (1,306 companies) — **large** SAM → **2 contacts per company**
  (the payroll decision-maker plus the practice owner/partner).
- `payroll-bureau`, `umbrella-contractor-payroll`, `recruitment-umbrella-contractor-payroll`
  (136 companies combined) — **small** SAM → **4 contacts per company**, since at a bureau the
  payroll function *is* the business and the buying committee is wider.

## Health warnings for the next session

1. **The 11+ size floor is what caps this list, not the tools.** 12,279 of 17,039 harvested
   companies are 1-10 employees — the UK accountancy/bookkeeping long tail is overwhelmingly
   micro-practices. If Brain Payroll will sell to sole practitioners, relaxing that floor
   roughly multiplies the universe by nine, and that is a commercial decision for the client.
2. **`icp_confidence: medium` is inferred, not verified** (see above). Verifying it needs a
   website-content pass over ~1,150 domains, which this pull did not do.
3. **Ireland is under-covered by Blitz.** Blitz returned only 94 Accounting companies for IE
   against 5,007 for GB. AI Ark lookalikes lifted the IE pool from 167 to 1,018 and the final
   IE count to 157, but Irish coverage remains the weakest part of this universe.
4. **AI Ark filter parameters do not work on this key.** Only `lookalikeDomains` narrows the
   result set — `countries`, `industries`, `descriptionKeywords`, `staffRange` and every
   variant tried were silently ignored, returning the full 72.5M-company baseline. It is
   usable as a lookalike engine only. (This differs from the VNTANA notes, which describe
   description-keyword and revenue filtering; either the API or the plan has changed.)
5. **Blitz `max_results` caps at 50, not 25** as CLAUDE.md states. Passing 51+ returns a
   422 naming the limit. Flagged for the repo owner — CLAUDE.md is a governed system file.
6. **Two qualifier bugs were found and fixed during this build; both are easy to repeat.**
   (a) Substring matching made `rti` match "expe**rti**se"/"prope**rti**es" and `cis` match
   "pre**cis**e", inflating a draft list by ~200 false positives — all term matching is now
   word-boundary anchored. (b) Matching competitor names against a company's *description*
   rejected ~220 genuine practices for saying "Xero Gold Partner" or "Sage certified";
   competitor tests now match company identity (name/domain) only.
