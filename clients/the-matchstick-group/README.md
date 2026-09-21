# The Matchstick Group

## Profile

- **Status:** active
- **Package tier:** Custom
- **Website:** `-` (not set in `tracking_clients`; the client record's name is the domain, `thematchstickgroup.com`)
- **Contact:** Melissa Wildstein <melissa.wildstein@thematchstickgroup.com>
- **Slack channel ID:** C0C1SDJMJ0G
- **Tracking client ID:** `45047afb-2d5a-4bfd-ac3d-caa290bdd568` (name in `tracking_clients`: `thematchstickgroup.com`)
- **HeyReach workspace:** 161333 (MI integration 4046) · **Master Inbox workspace:** 2986
- **Smartlead client ID:** `-` (none)
- **Booking link:** `-` (none set)
- **GTM engineer:** umair@algoacquisition.ai · **Campaign strategist:** ali.rehman@algoacquisition.ai · **Closer:** joe@algaocquisition.ai
- **Last synced:** 2026-09-21 via `get_client` + `list_sourcing_configs`

**What they sell:** a medtech marketing, brand and demand agency — naming, brand architecture,
identity, messaging, websites, launch campaigns and full marketing engines for medical device and
diagnostics companies, and for the private equity firms that own them. Not a staffing or recruitment
firm, which makes this a non-standard client relative to most of this repo.

## Sourcing configs

| Config | ICP | Market | Status | Campaigns | Companies sourced | Clay workbook |
|---|---|---|---|---|---|---|
| newco-countdown-sponsor-side | PE firms, medtech portfolio, carve-out/divestiture strategy | US | not sourced (see note) | Campaign 1 | 0 | `-` |
| before-the-buyer-arrives-seller-side | Medtech/diagnostics parents, $250M+, separation-announced | US | draft (companies only) | Campaign 2 | 94 | `-` |
| newco-countdown-newco-leadership | Newly separated medtech/diagnostics, $250M+ carved-out revenue | US | draft (companies only) | Campaign 3 | 99 | `-` |
| new-leader-old-portfolio | Multi-BU device/diagnostics, $250M-$3B, 3+ brands | US | draft (companies only) | Campaign 4 | 44 | `-` |
| exit-ready | PE-backed medtech/diagnostics platforms, $100M-$1B, 3+ yr hold | US | draft (companies only) | Campaign 5 | 51 | `-` |
| import-without-a-playbook | US subsidiaries of non-US medtech/diagnostics parents | DE/JP/IL/KR/CH/FR/SE/NL (HQ) | draft (companies only) | Campaign 6 | 27 | `-` |
| portfolio-without-a-throughline | Same universe as new-leader-old-portfolio (reused, not resourced) | US | draft (companies only) | Campaign 7 | 44 (reused) | `-` |

**None of these seven configs exist in `tracking_clients` yet** — this table is this repo's own
tracking of the sourcing work, not a mirror of a `tracking_clients` record. Create them there before
building anything in HeyReach, per CLAUDE.md "Campaign build standard per client" part 1.

**Campaign 1 (`newco-countdown-sponsor-side`) has zero companies sourced.** Tried three approaches
via ColdIQ's marketplace API (`fullenrich` keyword search, `ai-ark-companies` industry filter,
`linkupapi-search` industry+keyword filter) — none returned real PE firms with medtech portfolios;
keyword search returned generic mega-caps (Oracle, Abbott), the industry-tagged providers returned
zero rows. This segment's defining signal ("stated carve-out/divestiture strategy," deal sizes
$200M-$2B) is a deal-intelligence fact, not a firmographic filter any provider in this marketplace
exposes. Per the campaign brief's own sourcing list, this needs 8-K filings, PE portfolio pages,
MedTech Dive, MassDevice, or the Lawrence Evans weekly digest — a different, likely manual or
web-research-driven pull, not this pipeline.

## Sourced data in this repo

All pulled via **ColdIQ Marketplace API** (`api.coldiq.com`), `POST /v1/companies/search`, on
2026-09-21. Provider routing per segment is recorded in each `.query.md` (mostly `fullenrich`, pinned
after `auto` and cheap-tier providers `ai-ark-companies`/`linkupapi-search`/`theirstack` returned
zero or irrelevant rows on these filters — see each `.query.md` for what was tried). Apollo (also
proxied by ColdIQ) was evaluated and found non-functional on this account at time of pull:
`/v1/apollo/organizations/search` returned `502 Provider temporarily unavailable` on every attempt,
`/v1/apollo/people/search` returned `200` with zero results on every attempt (miss, refunded). No
`tracking_clients` sourcing config exists for any of these yet — see "Sourcing configs" above.

- `sourcing/before-the-buyer-arrives-seller-side/2026-09-21-companies.csv` — 94 companies for
  **Before the Buyer Arrives — Seller Side** (config not yet in `tracking_clients`), ColdIQ/FullEnrich.
- `sourcing/newco-countdown-newco-leadership/2026-09-21-companies.csv` — 99 companies for
  **NewCo Countdown — NewCo Leadership** (config not yet in `tracking_clients`), ColdIQ/FullEnrich.
- `sourcing/new-leader-old-portfolio/2026-09-21-companies.csv` — 44 companies for
  **New Leader, Old Portfolio** — segment 4(a) only, segment 4(b) not sourced (config not yet in
  `tracking_clients`), ColdIQ/FullEnrich.
- `sourcing/exit-ready/2026-09-21-companies.csv` — 51 companies for **Exit Ready** (config not yet in
  `tracking_clients`), ColdIQ/FullEnrich.
- `sourcing/import-without-a-playbook/2026-09-21-companies.csv` — 27 companies for
  **The Import Without a Playbook** (config not yet in `tracking_clients`), ColdIQ/FullEnrich — sources
  non-US parent companies, not verified US subsidiaries; see `.query.md` caveat.
- `sourcing/portfolio-without-a-throughline/2026-09-21-companies.csv` — 44 companies for
  **Portfolio Without a Throughline**, reused verbatim from `new-leader-old-portfolio`'s pull (same
  segment, no new API call) — see that folder's `.query.md`.
- `sourcing/newco-countdown-sponsor-side/` — **does not exist.** Zero companies sourced; see
  "Sourcing configs" above for why.

Every row also carries a `campaign` column (the campaign name) and a `sourcing_reasoning` column
(why the firmographic filter matched, and explicitly which parts of the segment's actual trigger this
pull does *not* verify) — added per-row so the CSV is self-explanatory without this README. The full
558-row set (all six sourced segments) was also pushed to the client's Clay webhook
(`pull-in-data-from-a-webhook-ca51b955-705d-436b-9a90-db07743f715b`) on 2026-09-21, one POST per
company row, each carrying the same `campaign` and `sourcing_reasoning` fields — see History.

**No prospect-level (`-leads.csv`) data has been pulled yet.** Companies only, per explicit
instruction this session; people sourcing is scoped separately and requires the repo owner's
go-ahead before it runs.

## Campaign definitions in this repo

- `campaigns/2026-09-21-medtech-gtm-campaign-set-v2.md` — seven medtech GTM campaigns (segment,
  persona, trigger, angle, connection note and three-message sequence each), supplied verbatim by the
  repo owner in-session on 2026-09-21. Strategy input, not tool-sourced data. Not yet created in
  `tracking_clients` and not yet built in HeyReach.

## History

- **2026-09-21** — Folder created from `clients/_TEMPLATE/README.md`; profile synced from
  `tracking_clients` (`get_client` + `list_sourcing_configs`, 0 configs). Saved the v2 medtech GTM
  campaign set (7 campaigns) supplied by the repo owner. Reason: this client had no folder at all
  despite being an active client since 2026-09-10, so the campaign strategy had nowhere traceable to
  live; the campaigns define the segments that every future sourcing config here will map to, so they
  need to be on disk before any pull happens rather than after. Nothing was created in
  `tracking_clients` or HeyReach in this session — the document records what is still outstanding.
- **2026-09-21** — Sourced companies for six of the seven v2 campaigns via **ColdIQ Marketplace API**
  (`/v1/companies/search`), 558 total rows across six `sourcing/<config-slug>/2026-09-21-companies.csv`
  files (campaign 7 reused campaign 4(a)'s pull rather than re-querying an identical filter). Campaign 1
  (sponsor-side PE firms) produced zero results — its defining signal is a deal-intelligence fact
  (carve-out/divestiture strategy) that no firmographic provider in this marketplace filters on;
  flagged for a different sourcing approach (8-K/press/deal-news) rather than forced through this
  pipeline. Reason for the approach: the user asked for "as large as possible" a dataset and to try
  ColdIQ's cheaper providers before the expensive ones — `ai-ark-companies` and `linkupapi-search`
  were tried first per segment and returned zero usable rows on these industry-filter queries (both
  appear not to support this marketplace's `industries` taxonomy the way `fullenrich` does), so the
  session fell back to `fullenrich`, which is what actually produced every populated row. Apollo
  (proxied by ColdIQ, the tool named alongside ColdIQ in the original ask) was tested directly and
  found non-functional on this account at the time — organizations search 502'd, people search
  returned zero results on every query — so no Apollo-sourced row exists in this pull; see "Sourced
  data in this repo" for the exact evidence. Exploration/diagnosis calls against the ColdIQ API before
  settling on this approach consumed roughly 4,000 of the account's ~12,000-credit balance; the
  productive pulls above cost roughly 5,940 credits (~$85), leaving the account at ~1,154 credits
  (~$16) — not enough left this session to source campaign 4(b) (PE-backed roll-up platforms) or to
  begin prospect-level sourcing. Added a `campaign` and `sourcing_reasoning` column to every company
  row (the latter states what the firmographic filter actually confirmed and what it does *not*, e.g.
  brand count, hold period, separation-announcement date — none of which any available provider
  exposes as a filter) and pushed the full 558-row set to the client's Clay webhook, one POST per
  company, on the user's explicit instruction. Person-level (`-leads.csv`) sourcing was intentionally
  held back — the user asked for companies first, prospects only after explicit go-ahead — so no
  `linkedin_url`-keyed leads file exists yet for any of these six configs. Session: see git log.
