# Qualifier agent — Brain Payroll

Turns `../sourcing/2026-09-17-combined-universe-companies.csv` (2,492 companies) into a
per-company verdict file, `../sourcing/2026-09-17-combined-universe-verdicts.csv`.

It exists because the universe build could only get so far on firmographics. 2,021 of its
2,492 rows carry `icp_confidence: medium` — confirmed UK/IE accountancy practices of 11+
staff where **payroll is a near-universal service line but was never actually verified**.
Verifying it is a per-company research job, and this is the thing that does it.

## Why two tiers rather than one agent per company

One LLM sub-agent per company would be 2,492 agents to answer a question that, for most
rows, a single site-scoped search settles outright. So the work is split:

| Tier | What | Scope | Cost |
|---|---|---|---|
| **1 — evidence** | Site-scoped search of each company's **own** domain for a payroll service page, via ColdIQ's EXA proxy. Deterministic, parallel, resumable. | every company | ~1.47 ColdIQ credits each (~3,660 total, ~$52) |
| **2 — adjudication** | LLM sub-agents, one per shard, read the Tier-1 pack and apply `rubric.md`. | the ambiguous remainder | agent time |

On the first 25 companies Tier 1 alone found a payroll page on the company's own domain for
21 of them, with the exact URL and a verbatim quote. Tier 2 is therefore aimed at what is
left: empty packs, contradictions, competitor and end-employer calls, acquisitions.

## Running it

`COLDIQ_API_KEY` must be in the environment.

```bash
python3 manager.py status                      # where the pipeline is up to
python3 manager.py evidence                    # Tier 1, whole universe (resumable)
python3 manager.py evidence --limit 200        # a slice, to sanity-check first
python3 manager.py evidence --only-medium      # just the unverified rows
python3 manager.py shard --size 60             # Tier 2 inputs + a brief per shard
python3 manager.py shard --only-unresolved     # only companies Tier 1 could not settle
python3 manager.py merge                       # fold verdicts into the verdicts CSV
```

`evidence` is **resumable** — it reads what is already in `work/evidence.jsonl` and collects
only the rest, so an interrupted run costs nothing extra. Use `--restart` to force a clean
sweep.

### Dispatching Tier 2

`shard` writes, per shard, a `shard-NNN.json` (the company packs) and a
`shard-NNN.brief.txt` (the instruction). Hand each brief to a sub-agent — in Claude Code,
one `Agent` call per shard, run concurrently. Each writes
`work/verdicts/shard-NNN.verdicts.json`. Then `merge`.

Sub-agents must not be given the whole universe: the shard is the unit of work, and a
sub-agent that invents verdicts to fill its shard is worse than one that returns `LIKELY`
with `evidence_quality: none`. `rubric.md` says so explicitly, and it is worth keeping that
line in any future edit.

## Files

| Path | What |
|---|---|
| `rubric.md` | The decision rule. Hard disqualifiers, segment definitions, evidence standard, output schema. Derived from the client brief in `tracking_clients`. |
| `manager.py` | The orchestrator. `evidence` / `shard` / `merge` / `status`. |
| `work/evidence.jsonl` | Tier-1 output, one JSON object per company. Regenerable — not the source of truth. |
| `work/shards/` | Tier-2 inputs and briefs. |
| `work/verdicts/` | Tier-2 outputs, one JSON array per shard. |

`work/` is regenerable scratch and is **git-ignored**. The verdicts CSV in `../sourcing/`
is the durable artifact.

## First run — 4 shards, 260 companies (2026-09-17)

| | |
|---|---|
| QUALIFIED | 185 (every one carries a real evidence URL on the company's own domain) |
| LIKELY | 39 |
| DISQUALIFIED | 36 — **13.8%** |

The disqualification rate is the headline: these are all companies the firmographic pass
had already accepted. What the sub-agents caught that no keyword filter could:

- **Six direct competitors** posing as accountancy practices — ANNA Money, Capium, Nomi,
  kpi.com, Sargent-Disc, and Dext. The Tier-1 search made several look *more* qualified,
  because a payroll-software vendor's product page reads exactly like a payroll service page.
- **Network head offices**, which are duplicates at the wrong level of the hierarchy: PKF
  Global, Russell Bedford International, Clarkson Hyde Global. Payroll is delivered by
  legally independent member firms, several of which are separately in the same list.
- **Live acquisitions the firmographics missed** — Critchleys → Gravita, Raffingers →
  Xeinadin, McBrides → DJH, Nicklin → DJH. Their domains now 301 to the acquirer.
- **Adjacent-but-wrong**: the Financial Reporting Council (the regulator), Kaplan and Mercia
  (training), Accountex (a trade show), AccountingFirms (a directory), KBS Corporate (an M&A
  broker whose site is full of payroll-sector deal news, which is exactly why it looked like
  a bureau).
- **Geography errors** that survived the HQ filter: Sonstige Software (Germany),
  Intelligent Outsourcing (Philippines), AACSL (Lagos).

It also surfaced intel the firmographic pass could not:

- **Competitor-in-situ displacement targets** — Bishop Fleming runs client payroll on
  **IRIS**; Shaw Gibbs has just migrated to **Paycircle** and is publicly repositioning
  payroll as "a growth lever, not a loss leader". These are arguably the best leads in the file.
- **Roll-ups change who buys.** Sumer Group (HW Fisher, Monahans, Carpenter Box, Cowgills,
  EQ, Scrutton Bland, Simmons Gainsford, Jerroms), Kinbrook (Duncan & Toplis, Old Mill),
  Dains (HURST, William Duncan, HSKS Greenhalgh). Payroll-software buying may now sit at
  group level rather than firm level, which changes both targeting and contact depth.
- **CIPP Payroll Assurance Scheme** accreditations: Kreston Reeves, Burgess Hodgson.

## Known gotchas

- **ColdIQ blocks the default Python user-agent.** `Python-urllib` is refused at the
  Cloudflare edge with a bare `403` and no body, which reads exactly like a bad API key.
  `manager.py` sets its own UA; keep that if you refactor.
- **A `site:` query can still return off-domain pages.** `collect_one` drops any result
  whose URL does not contain the company's own domain — an aggregator page describing a firm
  is not evidence that the firm offers payroll.
- **Tier 1 finding no page is not a disqualification.** Small practices often have no
  crawlable payroll page. That is what the `LIKELY` verdict is for.
- **A wrong domain silently returns a different company's payroll page.** Source APIs
  sometimes attach a domain belonging to another entity entirely — observed live: an
  accountancy practice carrying `mail.co.uk` (a German email provider), another carrying
  `bms.com` (Bristol Myers Squibb), a third carrying a borough council's site, and several
  carrying `scoreapp.com` (a shared third-party landing-page platform). Because Tier-1
  evidence is domain-scoped, this manufactures a *confident false* QUALIFIED. `collect_one`
  now sets `domain_matches_company`: at least one distinctive token of the company name must
  appear in the fetched title/text. It checks the CONTENT, not the domain string, so
  legitimately abbreviated domains (`hwca.com` for Haines Watts, `om.uk` for Old Mill) pass.
  Where it fails, the shard pack carries an `evidence_warning` telling the sub-agent to find
  the real website rather than trust the pack. 36 of the first 1,323 packs tripped it.
- **ColdIQ's two credit readings disagree.** `GET /v1/me/credits` and the
  `X-ColdIQ-Credits-Remaining` response header have reported very different balances. Check
  both before a bulk run.
