# US ICP qualification at scale — 2026-09-16

Qualifies the **United States** slice of the VNTANA universe against the client's ICP,
using cheap-model agents calibrated earlier the same day (see
`2026-09-16-icp-agent-calibration.query.md`, which must be read first — it establishes
why the prompt looks the way it does).

**Status: 5,106 of 5,227 US companies classified. One batch of 120 (`b039`) was still
running when this was committed and is not yet included.** The counts below will move
by up to 120 rows when it lands.

## Scope
Source: Supabase `companies`, `country in (US, USA, United States)`, `is_dnc=false`,
`exclusion_reason is null`, deduped on the `universe` view's key (domain → linkedin_url →
name, preferring client/IMTS/lookalike sources). **5,227 distinct US companies.**

**Deliberately NOT taken from the `addressable` view.** That view carries an
`employees >= 201 OR employees IS NULL` floor. Measured against the client's own 363
verdicts that floor is wrong: 40% of the companies the client rates `Yes` have under 200
employees (they are US arms of foreign manufacturers), and the floor would drop 688 US
companies here. The floor should be reconsidered repo-wide — flagged, not changed.

## Pipeline
| Stage | What | Cost |
|---|---|---|
| 0 | Blitz `/v2/enrichment/company` on every row (`company_linkedin_url`) | API only |
| 1 | Deterministic industry filter | free |
| 2 | Text-only Haiku triage, 120 accounts/agent, no web research | ~780 tok/account |
| 3 | Web verification of UNSURE — **not yet run** | — |

**Blitz enrichment:** 4,843 of 5,227 returned a description; 5,223 returned a size band;
**only 83 (1.6%) returned revenue.**

**Stage 1 is effectively a no-op on this dataset** — it drops 12 of 5,227 (0.2%). It
removed 9% of the IMTS trade-show list, but this universe came from Blitz manufacturing
queries, so nearly every row carries manufacturing keywords. Kept for auditability.
Its keyword rule was **removed** after it produced false drops: "University" matched in
founder biographies (Merrill Steel, Morgan Auto Group), "museum"/"magazine" matched in
passing mentions, wrongly dropping Ventrac, a real machinery manufacturer. Only the
industry rule survives, and only when the company's own text shows no manufacturing signal.
Validated at **100% recall** against 346 client-rated companies.

**Stage 2 prompt** is `clients/vntana/icp-triage-spec-t2.md`, derived from the calibrated
v2 spec with the web-research method replaced by text-only judgement and three added
traps that had each already caused a wrong `NO` in the calibration holdout:
semiconductor *component* makers are in scope (only capital equipment is out); a JV or
national arm carrying a manufacturer's name is not a distributor; service bureaus and
contract manufacturers are `UNSURE`, never `NO`.

Text-only triage was calibrated on its own blind 80-account holdout (no overlap with the
calibration 60, and five companies removed because they appeared in the spec's examples):
**96.2% recall**, 18% escalation load.

Two client rules applied mid-run, both from the repo owner:
- **Vehicle OEMs are out** — components and dealer-network parts only. This correctly
  rejects Tesla, GM, Ferrari, Rivian, Harley-Davidson and the Toyota/Honda/BMW/
  Mercedes national arms.
- Independent dealers, resellers and pure systems integrators are out.

## Results (5,106 of 5,227)
| Verdict | Count | Share |
|---|---|---|
| FIT | 2,433 | 48% |
| UNSURE | 945 | 19% |
| NO | 1,728 | 34% |

945 UNSURE includes **381 rows where Blitz returned no description at all** — a missing
input, not a judgement, and marked as such in `agent_reason`.

FIT by headcount: 1,000+ → 203 · 500-999 → 186 · 200-499 → 492 · 50-199 → 799 ·
under 50/unknown → 668.

**~34% of the US universe was never sellable.** The rejections are auto dealership groups,
Caterpillar/John Deere equipment dealers, systems integrators, steel job shops, building
products and contractors. `Motor Vehicle Manufacturing` is the largest single industry
bucket in the US set (1,145 rows) and splits almost entirely into dealerships and vehicle
OEMs — both out of scope. These were all inside the "addressable" count.

## A bug that nearly corrupted the write-back — read this before reusing the method
Each agent was asked to echo the company id (`cid`) beside its verdict. **1,352 of 4,233
rows (32%) came back with the wrong id** — models mis-transcribe long numeric keys across
long lists.

The verdicts themselves were *not* wrong. Checking each reason against the company at its
batch **position** versus the company at the agent's echoed id settles it:

| position | agent's reason | company at position | company at agent's cid |
|---|---|---|---|
| 53 | "Caterpillar equipment dealer" | Butler Machinery ✔ | Mac Valves |
| 54 | "pneumatic valves manufacturer" | Mac Valves ✔ | Paul Mueller |
| 89 | "industrial tools distributor" | PTSolutions ✔ | Tooling Tech Group |

The reason always matches the **position**. So the join key is batch position, and the
agent-echoed `cid` is discarded entirely. Joining on the echoed id would have mislabelled
about a third of the US universe with another company's verdict — plausibly enough that
nobody would have caught it.

**Never have an agent echo a primary key. Key on position and carry the id yourself.**

Residual: the *reason text* still drifts occasionally even where the verdict is right
(Yaskawa Drives returned an irrigation-equipment reason). Every row whose echoed id
disagreed with its position is marked `reason_trust = low-recheck` and gets priority in
stage 3.

## The revenue tier is NOT resolved
The calibration recommended computing YES/NEAR from a structured revenue field instead of
asking the agent. **That field does not exist in practice** — revenue is populated for 10
of 5,769 US rows in Supabase, and Blitz returns it for 1.6% (null even for Parker Hannifin
at $19.9B; only US mega-cap public companies like 3M and Caterpillar come back).

**Clay does return it, free.** `find-and-enrich-company` includes `annual_revenue` in the
base record with no paid data point consumed (`enrichments: []`) — Royal Products came back
`25M-75M`, matching the client's own $50-100M/Near-ICP rating; Parker `10B-100B`. But
`CLAY_API_KEY` is a scoped webhook-write key (api.clay.com returns 401/403 or "deprecated
API endpoint"), so lookups only work through the MCP at one company per call and ~8k
tokens per response. 4,834 accounts ≈ 38M tokens — not viable. A 200-300 account
shortlist is.

Interim rule, validated on the client's 363: **≥500 employees ⇒ YES tier**, ~1% error
(≥500 covers 32% of client `Yes` and 1% of client `Near`). Below 500 the tier is left
open — 40% of client `Yes` sit under 200 employees, so headcount decides nothing there.

**Decision pending with the repo owner:** which slice gets Clay revenue enrichment.

## Files
- `2026-09-16-us-icp-triage.csv` — one row per US company, with verdict, confidence,
  reason, `reason_trust`, Blitz headcount/size band, and the Supabase `company_id`.
- `clients/vntana/icp-triage-spec-t2.md` — the exact prompt used.

Supabase write-back (`agent_verdict`, `agent_model`, `agent_run`, `agent_checked_at`)
goes via the Supabase MCP. **PostgREST writes with the publishable key silently fail** —
a PATCH returns HTTP 200 with an empty body and changes nothing, because RLS is enabled
with no policies. Verified by reading the row back. Do not trust that 200.
