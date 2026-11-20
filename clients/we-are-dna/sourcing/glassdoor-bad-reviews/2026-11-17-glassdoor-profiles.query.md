# Glassdoor company lookup: 2026-11-17

**Client:** We Are DNA (tracking_clients `f5ff426b-c514-4a64-91b0-0e141a6a0669`)
**Segment:** `glassdoor-bad-reviews`. This expands the existing segment from the preview/test pulls to the full input list. It is not a new segment.
**Purpose:** find which ICP companies have a poor Glassdoor profile (the "bad reviews" signal) before any review or lead pulls. This follows the 2026-11-17 handoff in the client README History. Reviews, leads, campaigns, doc 1, HeyReach and Campaign 6 were not touched; they wait for Moe.

## Tool
- Apify actor `kaix/glassdoor-company-scraper`, called directly via the Apify REST API
  (`POST /v2/acts/kaix~glassdoor-company-scraper/runs`) with the session's Apify token (env `Apify_API_KEY`; the brief said `APIFY_API_TOKEN`).
- Driver: `run_lookup.py` (`runall`, then `assemble`). The run log, with every run id, status, item count and cost, is `2026-11-17-glassdoor-lookup-runs.json`.

## Input
- `2026-11-17-glassdoor-lookup-input.csv`: 29,489 companies in 6 batches, largest size band first. Batch 1 has 5,000 rows, as do batches 2 to 5, and batch 6 has 4,489.
- The `search_query` column is the Glassdoor search term.
- Actor input for every run:
  `{"searchQueries": [...], "maxSearchResults": 3, "compactMode": false, "includeRatings": true, all other include* false, "maxPhotos": 0}`

## Spend control
- **Price check before the run:** the actor's pay-per-event price on our tier (SILVER) is **$0.0001 per company profile**, plus $0.00005 per actor start. This is lower than the $0.0002 assumed in the handoff, so the price had not risen.
- **Runs:** the actor takes about 7 s per query, so each batch was split into 500-query runs.
  - Each run had `maxTotalChargeUsd=0.16`. That is the most 500 queries × 3 profiles can cost, so a cap could never cut a run short.
  - The worst case for the whole job was $9.45, against the **$10 total hard cap**.
  - `runall` refuses to launch anything that could take the total past $10.
- **Smoke test:** the first 50 queries of batch 1 (run `qpVI8dpA69sxnflfc`) returned the same shape as the preview output (`inputSource`, `ratings.*`, `reviewCount`, `headquarters`, `website`, `employerId`). It cost $0.0105.
- **Actual cost (sum of Apify `usageTotalUsd` over all 60 runs): $2.7987.** All 60 runs SUCCEEDED, returning 27,993 profile objects.

## Raw output (append-only)
| File | Profile objects |
|---|---|
| `2026-11-17-glassdoor-profiles-raw-b1.jsonl.gz` | 7,429 |
| `2026-11-17-glassdoor-profiles-raw-b2.jsonl.gz` | 6,347 |
| `2026-11-17-glassdoor-profiles-raw-b3.jsonl.gz` | 5,220 |
| `2026-11-17-glassdoor-profiles-raw-b4.jsonl.gz` | 3,960 |
| `2026-11-17-glassdoor-profiles-raw-b5.jsonl.gz` | 3,043 |
| `2026-11-17-glassdoor-profiles-raw-b6.jsonl.gz` | 1,994 |

## Scoring
```
python -I select_and_score.py --input 2026-11-17-glassdoor-lookup-input.csv \
  --out 2026-11-17-glassdoor-profiles.csv 2026-11-17-glassdoor-profiles-raw-b*.jsonl.gz
```
- Selection rule v2 (unchanged from the preview, generalised to the full file).
  - A candidate qualifies on a domain match or shared name tokens.
  - A UK HQ wins first, then the most reviews.
  - Confidence:
    - **high:** domain match, or a strong name match with UK HQ and 30+ reviews.
    - **medium:** a strong name match with UK HQ and under 30 reviews.
    - **low:** any other qualifying candidate.
    - **none:** nothing qualified.
- **Bar:** overall < 3.5 OR culture & values < 3.3 OR senior leadership < 3.3, each needing 30+ reviews. Medium matches can't pass by definition.
- The decline test needs review dates, so it is recorded as `needs reviews` on every row.
- Output `2026-11-17-glassdoor-profiles.csv` has **29,489 rows**, one per input company.

## Results
**Match confidence:** high 2,264 · medium 10,007 · low 2,546 · none 14,672 (50% none).

**Pass the profile bar:** 1,796. Of these, 1,384 are high confidence and 412 are low. The bar_rating test failed 1,411 companies and the bar_subrating test failed 1,749.

| Batch | high | medium | low | none | pass |
|---|---|---|---|---|---|
| 1 | 1,697 | 1,507 | 495 | 1,301 | 1,196 |
| 2 | 335 | 2,708 | 472 | 1,485 | 298 |
| 3 | 103 | 2,652 | 396 | 1,849 | 116 |
| 4 | 46 | 1,924 | 395 | 2,635 | 68 |
| 5 | 37 | 913 | 479 | 3,571 | 64 |
| 6 | 46 | 303 | 309 | 3,831 | 54 |

Passes by sector × size band (high-confidence passes in brackets):

| Sector | 51-200 | 201-500 | 501-1000 | 1001-5000 | Total |
|---|---|---|---|---|---|
| Retail, hospitality | 246 (163) | 180 (151) | 106 (92) | 173 (154) | 705 (560) |
| Manufacturing, engineering | 96 (40) | 66 (48) | 43 (37) | 74 (66) | 279 (191) |
| Health, care, vet | 82 (42) | 54 (39) | 34 (30) | 65 (62) | 235 (173) |
| Financial services | 148 (99) | 119 (105) | 78 (63) | 76 (62) | 421 (329) |
| Law, accounting | 57 (45) | 40 (32) | 32 (28) | 27 (26) | 156 (131) |
| Total | 629 (389) | 459 (375) | 293 (250) | 415 (370) | 1,796 (1,384) |

## Things that look wrong / need a human decision
1. **Low-confidence passes are mostly not the ICP company.** 372 of the 412 have a non-UK HQ. Examples: Jem Systems UK matched JEM Systems in Phoenix AZ, and Magentus matched the Australian parent. Treat only the 1,384 high-confidence passes as usable without review.
2. **The same Glassdoor employer was picked for several input companies.** 575 rows share an employer id with another row, and 131 of them pass.
   - Some are the same company under different names (Gordon Murray / Gordon Murray Group / Murray Group).
   - Some are wrong high-confidence matches: Christie's (auction house) matched Christies Care Ltd.
   - These need dedupe or a check before leads are built.
3. **Input quality:**
   - Three input rows have `.` as the search term (all `none`).
   - 98 search queries are duplicated in the input (e.g. Xeinadin, Holiday Inn London).
   - The README's size-band counts are slightly off. The actual counts are 51-200: 20,597, 201-500: 5,264, 501-1000: 1,893 and 1001-5000: 1,735. The README has 20,600 / 5,256 / 1,894 / 1,734. Both total 29,489.
4. **More profiles than the preview:** batch 1 returned about 1.5 profiles per query (2.1 in the first runs), against 1.2 in the preview. Cost was still well under the cap.
5. **Smaller companies match poorly:** batches 4 to 6 (smaller companies) are 53 to 85% `none`, and very few reach 30 reviews. So the "bad Glassdoor" signal mostly exists for the 201+ employee bands.

## Run ids
| Batch | Rows | Run id | Status | Items | Cost (USD) |
|---|---|---|---|---|---|
| 1 | 0-50 | `qpVI8dpA69sxnflfc` | SUCCEEDED | 104 | 0.0105 |
| 1 | 50-500 | `liPO6EEzLoPfw6iw3` | SUCCEEDED | 811 | 0.0811 |
| 1 | 500-1000 | `sDD5vKdpSGDAkN0h7` | SUCCEEDED | 787 | 0.0788 |
| 1 | 1000-1500 | `ieTR6uAhjv0ubF1yd` | SUCCEEDED | 741 | 0.0741 |
| 1 | 1500-2000 | `ieYQe4hoXGHy3bF1W` | SUCCEEDED | 726 | 0.0717 |
| 1 | 2000-2500 | `6gFj6ucEbAdma18ib` | SUCCEEDED | 768 | 0.0761 |
| 1 | 2500-3000 | `wfcpkENz7Ycd24e91` | SUCCEEDED | 710 | 0.0711 |
| 1 | 3000-3500 | `2vwPrqJvM32U3L4T0` | SUCCEEDED | 696 | 0.0697 |
| 1 | 3500-4000 | `NoWsQdMQl6gSuP9W8` | SUCCEEDED | 653 | 0.0653 |
| 1 | 4000-4500 | `GYakNgjPkhhpagIzC` | SUCCEEDED | 734 | 0.0735 |
| 1 | 4500-5000 | `CTSUFSz5PQjDr2bxQ` | SUCCEEDED | 699 | 0.0699 |
| 2 | 0-500 | `MEEasNatmRvwlAu8C` | SUCCEEDED | 646 | 0.0645 |
| 2 | 500-1000 | `VMWNPI82GyT6VOICw` | SUCCEEDED | 693 | 0.0693 |
| 2 | 1000-1500 | `Y7jqfswMUMX6QCgCb` | SUCCEEDED | 640 | 0.0640 |
| 2 | 1500-2000 | `ac4TxtKcYUUN7iPFO` | SUCCEEDED | 677 | 0.0678 |
| 2 | 2000-2500 | `Q4YrkNn6VsNYFg5Ww` | SUCCEEDED | 622 | 0.0623 |
| 2 | 2500-3000 | `eWcVuZvLiYRc8GVyu` | SUCCEEDED | 625 | 0.0625 |
| 2 | 3000-3500 | `nkCA00MOouslDsKxd` | SUCCEEDED | 588 | 0.0589 |
| 2 | 3500-4000 | `QAAmIJKlaaJBrd8kd` | SUCCEEDED | 644 | 0.0644 |
| 2 | 4000-4500 | `WJ300KfVeVtwW4Ej1` | SUCCEEDED | 607 | 0.0608 |
| 2 | 4500-5000 | `wwDosIgVoa7EgfXQd` | SUCCEEDED | 605 | 0.0606 |
| 3 | 0-500 | `8IebmiIXfe6gomEr6` | SUCCEEDED | 574 | 0.0575 |
| 3 | 500-1000 | `XTLufX1ZpIBzb3hmp` | SUCCEEDED | 550 | 0.0551 |
| 3 | 1000-1500 | `uLLgkHDF7CKkf9TkD` | SUCCEEDED | 530 | 0.0531 |
| 3 | 1500-2000 | `QkwxoeNvUBYbY1aEQ` | SUCCEEDED | 554 | 0.0555 |
| 3 | 2000-2500 | `sg4coDeDcebQbMYEy` | SUCCEEDED | 510 | 0.0511 |
| 3 | 2500-3000 | `qeKkdqR5NalCL80O4` | SUCCEEDED | 498 | 0.0499 |
| 3 | 3000-3500 | `7SGdwfeaLtqDzsOPc` | SUCCEEDED | 487 | 0.0488 |
| 3 | 3500-4000 | `G1CtvelsqC7QMIqS2` | SUCCEEDED | 521 | 0.0522 |
| 3 | 4000-4500 | `TsZetpzNYmjjnUnvy` | SUCCEEDED | 503 | 0.0500 |
| 3 | 4500-5000 | `2IaBfLCkt6XjYlFun` | SUCCEEDED | 493 | 0.0494 |
| 4 | 0-500 | `ZAWd2yP2gabydtGFo` | SUCCEEDED | 444 | 0.0442 |
| 4 | 500-1000 | `DNh3iYvpgvT85P2sk` | SUCCEEDED | 433 | 0.0434 |
| 4 | 1000-1500 | `0PWFdgCj2SLt1wdsk` | SUCCEEDED | 411 | 0.0412 |
| 4 | 1500-2000 | `4q79AWXwVqZPcSpFm` | SUCCEEDED | 437 | 0.0437 |
| 4 | 2000-2500 | `F3aCjmbBVieiKqMP5` | SUCCEEDED | 407 | 0.0408 |
| 4 | 2500-3000 | `1q39agpGpNqdwqf5x` | SUCCEEDED | 382 | 0.0383 |
| 4 | 3000-3500 | `q5Y0rmORiVh8xtpHz` | SUCCEEDED | 403 | 0.0404 |
| 4 | 3500-4000 | `dojvtsh8S3auexQiM` | SUCCEEDED | 364 | 0.0365 |
| 4 | 4000-4500 | `I4ecZpYrbKhIDh5bX` | SUCCEEDED | 343 | 0.0344 |
| 4 | 4500-5000 | `V7GT1hhUk21gXi6Qj` | SUCCEEDED | 336 | 0.0337 |
| 5 | 0-500 | `xaE8GTW7fnaPUgJd5` | SUCCEEDED | 340 | 0.0341 |
| 5 | 500-1000 | `MpmmAF0KocqzsnMK6` | SUCCEEDED | 403 | 0.0403 |
| 5 | 1000-1500 | `V1TcMq3hhdN9DhQ8r` | SUCCEEDED | 337 | 0.0333 |
| 5 | 1500-2000 | `GaK3sO9oXNQMMCLVo` | SUCCEEDED | 323 | 0.0324 |
| 5 | 2000-2500 | `wnuHxjSzZnYFpVjdC` | SUCCEEDED | 288 | 0.0289 |
| 5 | 2500-3000 | `eExauObsUz6AaxO6J` | SUCCEEDED | 292 | 0.0293 |
| 5 | 3000-3500 | `7zaT3ELUgYpxa1NFe` | SUCCEEDED | 302 | 0.0303 |
| 5 | 3500-4000 | `pHJpiqkRXqVQXzQg6` | SUCCEEDED | 283 | 0.0284 |
| 5 | 4000-4500 | `4jg8kU4BpoVxsLeB6` | SUCCEEDED | 235 | 0.0236 |
| 5 | 4500-5000 | `oEsIxIzHTwWUjCsHs` | SUCCEEDED | 240 | 0.0241 |
| 6 | 0-500 | `C1qNdQlIFfjbFjOLo` | SUCCEEDED | 256 | 0.0257 |
| 6 | 500-1000 | `i6pR4EQG64thvFEDm` | SUCCEEDED | 220 | 0.0221 |
| 6 | 1000-1500 | `eC1Ps5tzqIwzV5anA` | SUCCEEDED | 234 | 0.0235 |
| 6 | 1500-2000 | `qxBdgmR5xsJI4EJkw` | SUCCEEDED | 257 | 0.0258 |
| 6 | 2000-2500 | `SfBabpqLT2BesKOEN` | SUCCEEDED | 217 | 0.0216 |
| 6 | 2500-3000 | `dDDrbj5g8xr4NHvtg` | SUCCEEDED | 183 | 0.0184 |
| 6 | 3000-3500 | `etptkcjUMWz6ZiFV4` | SUCCEEDED | 209 | 0.0210 |
| 6 | 3500-4000 | `qOa8u7YJ7G7RlTUsx` | SUCCEEDED | 204 | 0.0203 |
| 6 | 4000-4489 | `ugREko0WTZgLzbvFx` | SUCCEEDED | 214 | 0.0215 |
