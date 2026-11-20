# Signal read for doc 1 revision: campaigns 1–5 re-signalled (2026-11-13)

- **Why:** on 2026-11-12, John Tarrant (We Are DNA) emailed after the doc went out:
  - Leading with an open role makes DNA look like a "low end high street recruiter". Their buyers get bombarded by recruitment agencies and despise them.
  - DNA sells to the C-suite and the level just below, who won't know what the open roles are.
- **Decision:** Moe said "replace the signals with other signals", then "proceed with the 5 sector mapping". The five sectors stay the same, but each now has a board-level, public signal. The personas move up to C-suite, director level or partner level.
- **Client:** We Are DNA `f5ff426b-c514-4a64-91b0-0e141a6a0669`. **Doc:** `fed8e905-ea1c-4a91-ade7-0da0f7f732a6`.
- **Supersedes:** the open-role signal in `2026-11-12-tam-read.query.md`. Its firmographic base counts (UK HQ 201+ per sector) are still used below.

## New signal per campaign

| # | Campaign | Signal | Source | Measured? | Contacts / company |
|---|---|---|---|---|---|
| 1 | Buy-and-Build Groups, Health/Care/Vet/Dental | acquired sites in the last 12 months, or an announced buy-and-build strategy | acquisition news and trade press | **No.** Estimate: a few hundred of the 2,585 companies at 201+ (Blitz 2026-11-12) | 3 (CEO → People Director) |
| 2 | People Costs on the Board Agenda, Retail & Hospitality | labour costs, turnover or retention named in the annual report, results or a trading update in the last 12 months, or a customer rebrand | RNS, annual reports, rebrand news | **No.** Estimate: several hundred of the 3,280 companies at 201+ | 2 (CEO/COO + top people leader) |
| 3 | Closing the Gap, Manufacturing/Engineering | median gender pay gap ≥15% in the 2025 data | gov.uk GPG service | **Yes:** 229 of 1,144 | 2 |
| 4 | Mergers and New Leadership, Top 100 Law & Accounting | merger, acquisition or PE deal, or a new managing partner, senior partner or CEO, in the last 12 months; secondary hook is GPG ≥15% | rankings, deal and leadership news, GPG | **Partly.** GPG: 36 of 66 law/accounting employers. Main signal estimated at 40–60 a year | 3 |
| 5 | Closing the Gap, Financial Services | median GPG ≥15%, or a Women in Finance Charter target | GPG; HM Treasury Charter signatory list | **Yes:** 346 of 537 (GPG only; Charter list not yet pulled) | 2 |

The contacts-per-company rule is inverse to pool size. The GPG pools are medium (229–346), so 2. The buy-and-build and law/accounting pools are small, so 3.

## Gender pay gap read (the measured part)

- **Source:** `https://gender-pay-gap.service.gov.uk/viewing/download-data/2025`. This is public, needs no key, and covers every GB employer with 250+ staff. It's the 2025 reporting year, 11,202 employers in total.
- **Method:** `gpg_signal.py`, run as `python3 -I gpg_signal.py <downloaded csv>`.
  - Sector is assigned by SIC prefix: health 86/87/88/75; retail and hospitality 47/55/56; manufacturing 10/11/2x/30/33; law and accounting 691/692; financial services 64/65/66.
  - Signal = `DiffMedianHourlyPercent` ≥ 15.
- **Output:** `2026-11-13-gpg-signal-companies.csv`, 3,796 employers across the five sectors. One row per employer with the median and mean gap, female top quartile, size and a link to the employer's GPG page. `gpg_signal_15pct` = yes/no.
- **Counts:**
  - health/care/vet: 1,107 employers, 125 with the signal
  - retail/hospitality: 1,035, 102
  - manufacturing/engineering: 1,144, 229
  - law/accounting: 66, 36
  - financial services: 537, 346
- **Cost:** £0. No Blitz or Clay records used.
- **Caveats:**
  - SIC codes are self-declared. A group's code may not match its trading sector, so check by eye at sourcing time.
  - GPG rows are legal entities, not LinkedIn companies. Match them to company LinkedIn pages at sourcing.
  - The `{gap}` variable in campaigns 3 and 5 comes from `median_gap_pct`.

## Still to do before sourcing (after client approval)

- Size campaigns 1, 2 and 4's main signal properly, using news, RNS and deal-data searches.
- Pull the HM Treasury Women in Finance Charter signatory list (campaign 5).
- Get the client's decision on whether to quote the GPG figure. The doc's "Before launch" section asks.
