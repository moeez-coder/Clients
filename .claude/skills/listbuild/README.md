# listbuild — cheapest-first, exclusion-aware multi-provider list builder

Builds an exhaustive director-plus contact list for one ICP by layering data providers from cheapest to most
expensive (Blitz -> Clay -> DiscoLike), deduplicating on LinkedIn URL and on name+company, excluding prior
prospects, guarding titles, and classifying company fit. One YAML config per vertical; one output folder per run.

## Teammate quick start
```
pip install -r requirements.txt
copy .env.example .env                       # fill in the three API keys
python -m pytest -q                          # 110+ tests, all green

python -m listbuild new-icp --name staffing_us_gb --industries "Staffing and Recruiting" --countries US GB --revenue-min 1000000
python -m listbuild --icp config/staffing_us_gb.yaml preview            # free: sizing, cost, quota, 60 sample contacts
python -m listbuild --icp config/staffing_us_gb.yaml run --seeds prior_prospects.csv --discolike-cap-usd 0
```
Outputs land in `out/staffing_us_gb/`: `<name>_<date>_partNN.csv` (main list), `*_consulting_candidates_*`
(catch-all industries, review before use), `*_unverified_*` (company industry unknown), `cost_report.md`, `preview.csv`.

`run` is resumable: rerun the same command after any interruption. It always attempts all three providers, reports
each provider's quota and balance before starting, prints the DiscoLike estimate and spends nothing unless
`--discolike-cap-usd` is set, and ends with a list of any provider limits hit and the stages to rerun. The Claude Code
skill (`SKILL.md` here; `python scripts/build_skill.py --install` packages it into `~/.claude/skills/listbuild/`) drives the same commands.

## Stages (all idempotent)
| Stage | What | Cost |
|---|---|---|
| seed | prior CSVs -> exclusion keys (LinkedIn URL and first+last+domain, every name variant kept) | 0 |
| blitz | people search sharded under the 50k/query cap, 20 workers | 0 (flat plan) |
| clay | people search into a side ledger, split on `query_limit`, stops at the quota reserve | 0 (quota) |
| merge | side ledger folded in with full dedupe | 0 |
| companies / companies-kw | Blitz company search: authoritative industry per company; keyword gate for catch-all labels | 0 |
| domains | name join + Blitz company enrichment for rows lacking a domain | 0 |
| consolidate | late-exclusion purge, same-person slug collapse, title guard, QA counts | 0 |
| discolike-estimate / -fetch | free counts + 40-row sample -> estimate; blind pull by country x seniority up to the cap | paid |
| fit | core industry = fit; catch-all + keywords = candidate; else unfit/unknown | 0 |
| export | three CSV sets + cost report | 0 |

## Provider facts that shaped the design (verified live 2026-09-22..25)
| | Blitz | Clay public API | DiscoLike |
|---|---|---|---|
| Cost | 1 record/result against a flat allowance | search is credit-free; 1M results per period, shared | $0.0035/new contact; free `/contacts/count`; 90-day cache |
| Caps | 50/page, 50,000/query -> shard | 500/run, stateful iterator; deep iterators time out ~150k | 10,000/call, offset <= 10,000 |
| Returns domain | yes (~2% null) | no (name only) | yes |
| Revenue filter | numeric | bucket enum | none (post-filter) |
| Exclusion | none | companies only | **ignored** (domains and persona ids) |
| Industry | 534 LinkedIn labels, legacy + current both present | LinkedIn labels | 53 buckets |

Lessons baked into the code: dedupe on name+company as well as LinkedIn URL (slugs change); catch-all LinkedIn
labels are never core (keyword gate ~30% precise); DiscoLike "thin company" pulls re-buy the person you already
hold, blind pulls with an employee floor are ~60% net-new; refresh name keys after domain back-fill; read spend
from the billing log, never the balance field.

## Ledger (`out/<name>/ledger.sqlite`)
`contacts` (key = `li:<normalised url>` or `alt:<sha1 first|last|domain>`), `companies` (industry, keyword_fit),
`excluded`, `shards` (resumable cursors), `spend`, `paid_unqualified`, `kv`. Every page commits.

## Adding a vertical
`new-icp` maps LinkedIn labels to Blitz (adds legacy variants) and DiscoLike buckets from tables in
`listbuild/icp_gen.py`; extend those tables when a label is reported as unmapped. Countries and seniority sets live there too.
