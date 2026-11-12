---
name: listbuild
description: Use when someone wants a cold-outbound or prospecting contact list for a vertical or ICP (director-plus people at companies in given industries, countries and revenue band) built from Blitz, Clay and DiscoLike, when they say "build a list", "TAM", "tech-map this vertical", or ask to run listbuild. Self-contained: the code ships inside this skill folder and runs from any project.
---

# listbuild: cheapest-first exhaustive list build

## Overview
This skill folder contains the whole pipeline. It layers data providers from cheapest to most expensive
(Blitz -> Clay -> DiscoLike), deduplicates on LinkedIn URL and on name+company, excludes prior prospects, guards
titles, and classifies company fit. The requester's project folder is the **workspace**: `config/`, `.env` and
`out/` live there; the code stays here. **Preview first; the requester approves the sample before any run.**

All commands below use `SKILL` = this skill's base directory (shown when the skill loads) and run **from the
workspace** (the requester's project folder).

## Inputs to collect (everything else is automatic)
1. API keys for Blitz, Clay, DiscoLike, unless `.env` in the workspace already has them.
2. Industries as exact LinkedIn/Clay labels, HQ countries (ISO-2), revenue floor (USD),
   seniority (`director_plus` | `vp_plus` | `manager_plus`).
3. Prior-contact CSVs to exclude (any export with a LinkedIn column). Optional DiscoLike budget in USD (default 0).

## Workflow
1. **Setup (once per workspace, ~1 min)**
   `python "SKILL/scripts/setup.py" --blitz KEY --clay KEY --discolike KEY`
   Installs dependencies, writes `.env`, copies defaults, runs the tests, checks each key read-only. Rerun without keys
   to re-check. If a key check fails, stop and tell the requester.
2. **Config**: `python "SKILL/scripts/listbuild.py" new-icp --name <slug> --industries "<label>" ... --countries US GB --revenue-min 1000000 --seniority director_plus`
   Slug: `<vertical>_<geos>` in snake_case. Read the printed notes: catch-all labels become a candidates layer; unmapped
   labels mean a misspelling; "related labels" are suggestions to confirm with the requester, never add them silently.
3. **Preview (free, ~1 min)**: `python "SKILL/scripts/listbuild.py" --icp config/<slug>.yaml preview --seeds "<prior1.csv>" ...`
   `--sample N` = Blitz rows in total (default 60) spread evenly across HQ countries (not proportionally) plus up to
   20 Clay rows; the first 25 print, all go to `out/<slug>/preview.csv` with `title_check` and `in_prior_list` columns. Show the requester the sizing block and the
   sample. If the sample is wrong, edit `config/<slug>.yaml` and preview again. **Stop here until they approve.**
4. **Run** (tell the requester to run it in their own terminal window; it is resumable and takes 20 min to a few hours):
   `python "SKILL/scripts/listbuild.py" --icp config/<slug>.yaml run --seeds "<prior1.csv>" ... --discolike-cap-usd 0`
   Cap 0 prints the DiscoLike estimate and spends nothing; set a dollar cap only after the requester approves the
   printed estimate and the account balance covers it.
5. **Deliver** from `out/<slug>/`: `<slug>_<date>_partNN.csv` (main list), `*_consulting_candidates_*` (catch-all
   industries, needs review), `*_unverified_*` (company industry unknown), `cost_report.md`, `consolidate.log`.

## Quick reference
| Need | Command (prefix `python "SKILL/scripts/listbuild.py"`) |
|---|---|
| Sizing, sample, prior-list overlap, no spend | `--icp config/x.yaml preview --seeds ...` |
| Whole build, no paid pull | `--icp config/x.yaml run --seeds ... --discolike-cap-usd 0` |
| Only some stages / redo a stage | `run --stages blitz merge export` / `run --force --stages fit export` |
| Add a label the generator does not know | extend `LEGACY_LABELS` / `DISCOLIKE_BUCKETS` in `SKILL/listbuild/icp_gen.py` |

## Rules that came from real failures
- **Catch-all LinkedIn labels are never core.** "Business Consulting and Services", "Strategic Management Services",
  "Professional Services" and similar hold energy engineers and executive-search firms. The generator moves them to a
  keyword-gated candidates layer (about 30% precise). Say so to the requester at step 2.
- **Never spend before the estimate.** DiscoLike cannot exclude (its exclusion lists are ignored), so paid rows overlap
  the free layers by ~40%. The estimate prints cost per net-new contact; the requester sets the cap. If preview shows the
  DiscoLike balance overdrawn or below the cap, run with cap 0 and tell the requester to top up first.
- **Spend truth is the billing log** (`GET /usage -> billing_events`), not the balance field; other processes may share the key.
- **Every run attempts all three providers, every time.** Never disable a provider or edit the config to dodge a limit.
  Preview and the run's pre-flight report each provider's quota and balance up front; if a limit is hit mid-run the
  stage stops, the run continues with the other providers, and the closing "PROVIDER LIMITS HIT" list says exactly
  what is missing and which stages to rerun once the limit clears. Relay that list to the requester verbatim.
- **Clay quota is shared and finite** (1M results per period). Never lower `quota_reserve` below 150k.
- **Clay's "Staffing and Recruiting" / "Marketing Services" rows include some product companies** LinkedIn mislabels;
  the fit stage keeps them because the label is core. Mention it if the requester wants agencies only.
- **Seniority is title-based and vertical-blind.** In recruitment firms "Partner", "Talent Partner" and "Head of <desk>"
  are often fee-earner titles; in agencies "Art Director" is mid-level. Show these in the sample and let the requester
  decide; tighten `SKILL/listbuild/seniority.py` (test first) only on their say-so.
- **Low-RAM machines freeze long sweeps.** A stage sitting at 0 CPU means memory pressure: close browsers, rerun the
  same command. Never run the sweep inside a Claude Code background shell; it gets killed under memory pressure.

## Common mistakes
| Symptom | Cause | Fix |
|---|---|---|
| Consultancies in the main list | catch-all label under `fit.core_industries` | regenerate the config; keep them keyword-gated |
| Prior prospects reappear | LinkedIn slug changed | `consolidate` purges on name+company too; confirm `--seeds` was passed |
| Blitz shard marked `oversized` | >50k rows in one filter combination | add a dimension to `SHARD_DIMS` or accept partial |
| `HTTP 402` from Clay | quota exhausted | the run continues without Clay and lists it in the closing notices; rerun the clay stage after the reset date |
| A sub-director title exported | title-guard gap | add the case to `SKILL/tests/test_seniority.py`, fix `seniority.py`, rerun `run --force --stages consolidate-final export` |

Provider facts, stage table and ledger schema: `SKILL/README.md`.
