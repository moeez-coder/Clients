# ICP agent calibration run — 2026-09-16

**Purpose:** before spending model budget verifying the ~10,700-account `addressable`
universe, measure whether a cheap-model agent can reproduce the client's own ICP
judgement. Calibrate first, scale second.

## Ground truth
`clients/vntana/sourcing/2026-09-15-imts-client-icp-verdicts.csv` — 363 IMTS 2026
exhibitors the client themselves rated. 250 `Yes`, 113 `Near-ICP`. **No `No` rows exist
in that file**, so any agent `NO` on a sampled account is definitionally a miss.

Decoded client rule (inferred from the revenue column, confirmed across all 363 rows):
fit criteria are identical for both tiers — the only difference is size.
`Yes` = $100M+ revenue. `Near-ICP` = $50–100M.

## Sample
Deterministic 60 of 363: sorted by `md5(exhibitor_name + 'seed7')`, first 60 taken,
split into four 15-account batches. Agents received **only** `id`, `company`, `website` —
the client verdict, revenue and group were held back in `answer_key.json`. Blind test.

## Runs
| Run | Spec | Model | Agents |
|---|---|---|---|
| v1 | `clients/vntana/icp-agent-spec-v1.md` | Haiku (cheapest) | 4 × general-purpose, 15 accounts each |
| v2 | `clients/vntana/icp-agent-spec-v2.md` | Haiku (cheapest) | 4 × general-purpose, same 60 accounts |

Agents had WebSearch/WebFetch and were told to open the company's own site.

## Results (n=60, same accounts both runs)
| Metric | v1 | v2 |
|---|---|---|
| Exact match (tier correct) | 17 (28%) | **37 (62%)** |
| In-ICP but wrong tier | 8 (13%) | 17 (28%) |
| **Hard miss (agent said NO)** | **35 (58%)** | **6 (10%)** |
| **Fit-only accuracy** (YES/NEAR collapsed) | **42%** | **90%** |

## What v1 got wrong — all four were spec defects, not model failures
1. **"Assembled from many smaller parts"** rejected component, tooling and consumable
   makers. Killed Parker Hannifin ($19.9B), ATI, Deublin, EROWA, Hainbuch, Royal
   Products, Samchully, Yukiwa, Coval. The client's own groups include *Cutting Tools,
   Tooling & Workholding* (50 companies) and *Shop Support, Components & Consumables*
   (42) — so this defect attacked ~25% of the client's list by construction.
2. **Subsidiary rule absent.** "SPINNER North America" and "SNK America" were read as
   distributors. They are national arms of German/Japanese machine-tool builders.
3. **Metrology confused with the medical-device exclusion.** Killed JEOL, Zygo, WENZEL,
   Werth, Nikon Metrology, Schenck, Navitar, SHINING 3D, VICIVISION — 9 of 35 misses.
4. **Tier leakage:** `NO` returned for low revenue, which should be `NEAR`.

## v2 changes
Core test rewritten to **"manufactures physical industrial products and sells a catalogue
of roughly 200+ SKUs"** — catalogue breadth, not machine size. Explicit in-scope list
(components, tooling, abrasives, metrology, shop support, forgings/castings). Hard
subsidiary rule. Two "commonly misapplied" carve-outs: metrology ≠ medical devices;
abrasives/ceramics/forgings are discrete, not process manufacturing. Two never-rules:
never NO for low revenue, never NO for direct-to-customer.

**Leakage control:** v2's first draft used worked examples drawn from the test set
(Parker Hannifin, Bahco, JEOL, ATI, SPINNER, CUMI, Hainbuch, Royal Products, Coval).
That would have handed the agents nine answers and faked the improvement. The table was
rebuilt from companies **outside** the 60 — SMC, CERATIZIT, Bruker Alicona, Chiron
America, Indo-MIM, Sunnen, 80/20, DATRON, GMN, Kosmek — each verdict verified against the
client's own CSV, and the subsidiary examples swapped to Chiron/Botek. A programmatic
check confirms none of the 60 test companies appears anywhere in v2.

## Remaining v2 errors — what they mean for scaling
**6 hard misses**, none a taxonomy blind spot:
- *xTool, Prusa Research, Formlabs, Bissell Commercial* — prosumer/commercial equipment
  read as consumer. The client counts these as in-ICP. The spec does not distinguish
  "sells to consumers" from "is a consumer-retail company".
- *OnLogic* — agent could not verify catalogue depth or revenue and fell back to `NO`.
  The spec never states what to do under uncertainty. It should say: default to `NEAR`.
- *Quintus Technologies* — capital equipment vendor read as too narrow.

**17 tier errors are 14:3 in one direction — conservative.** Agents downgrade YES→NEAR
because revenue for privately-held foreign parents is not published (WENZEL, EROWA,
SPINNER, SNK, ETXE-TAR, Nagel, Samchully, Werth, ATI, Bahco). Note the client's own
figures in these rows are marked "(est.)" — the client is estimating too.

**Design conclusion:** do not ask the agent for the tier. Ask it only for fit
(FIT / NO), which it does at 90%, and compute YES vs NEAR from a structured revenue
field in the Supabase `companies` table. That removes the dominant error class.

**Confidence is not a usable routing signal:** 5 of the 6 hard misses were returned at
`high` confidence. Do not gate review on self-reported confidence.

## Reproduce
Scratchpad: `verify/` — `ICP_SPEC.md`, `ICP_SPEC_v2.md`, `batch_1..4.json`,
`answer_key.json`, `result_*.json`, `score.py`. Per-account detail for both runs is in
`2026-09-16-icp-agent-calibration.csv` (60 rows).

**Not yet run at scale.** Scaling to the full `addressable` view (10,692 accounts) is a
separate decision and has not been authorised.
