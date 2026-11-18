# TAM read: Casual Connections, Bristol wave 1 (2026-11-18)

**Why this file exists:** CLAUDE.md's campaign doc standard says the TAM read has to be committed under `sourcing/tam/` before the campaign goes into a doc.
- Moe decided on 2026-11-18 that Casual Connections **replaces Campaign 4** (Mergers and New Leadership, Top 100 Law and Accounting) in doc 1 (`fed8e905-ea1c-4a91-ade7-0da0f7f732a6`).
- Doc 1 isn't edited until another session's doc edits finish (Moe's instruction).
- Session: session_013MzxQfxb1tFTNdnVAHYrw5.

## Signal

- **There is no time-bound trigger.** The qualifier is **shared city**: the company's HQ is in Bristol, which is where DNA is based and John founded it.
- **Tool:** Blitz `POST /v2/search/companies`, field `hq_city`, already pulled on 2026-11-17 into `../glassdoor-bad-reviews/2026-11-17-companies.csv` and `-2-companies.csv`. Matched on `hq_city` containing "Bristol".
- **Recency window:** none. It's a static attribute, so the pool doesn't refill by itself. The next waves extend the geography instead: the rest of the South West (about 1,040 more companies), then national.

## Counts (measured, not estimated)

| Step | Count | Source |
|---|---|---|
| Companies in DNA's TAM (private sector, 51 to 5,000 staff, five sectors, DNC and Campaign 6 excluded) | 29,489 | `../glassdoor-bad-reviews/2026-11-17-glassdoor-lookup-input.csv` |
| Of those, Bristol HQ | **312** | Blitz `hq_city` (joined on company LinkedIn URL) |
| South West HQ (city regex, indicative) | about 1,354 | same |
| Reachable C-suite contacts per company (preview, 20 largest Bristol companies) | **0.95** usable (19 of 45 found; 4 companies had none) | Blitz `POST /v2/search/waterfall-icp-keyword` + Clay `search-contacts`, `../casual-connections/2026-11-18-preview.query.md` |
| Expected wave-1 contacts | about 300 (312 x 0.95, plus a second contact at 201+ staff) | estimate from the measured yield |

- **The bar:** 312 companies clears the standard's 200 to 300+ threshold.
- **Eyeballed:** the 19 preview contacts are real C-suite at real Bristol employers (Burges Salmon, TLT, Somerset Bridge, Turtle Bay, Vertical Aerospace and others).
- **Known leaks, removed in the build:** charities and CICs, "Owner" self-labels, and group-level CEOs of global parents.

## Capacity

- **Senders:** two, John Tarrant and Eoin Rodgers (Moe, 2026-11-18). At about 100 invitations a week each, that's about 200 a week.
- **Wave 1:** about 1.5 to 2 weeks of sends, which leaves room to read acceptance before wave 2.
- **Neither account is in HeyReach 172307 yet.**

## Cost of this read

£0 new. It reuses the 2026-11-17 Blitz pulls plus the preview's 54 Blitz records, 1 Clay search and $0.007 of Exa, which are already logged.
