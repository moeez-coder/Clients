# Repository standards (read this before touching anything here)

This repo is Algo Acquisition's sourcing-data working layer (see `README.md` for
the structure). It is worked on by many separate sessions over time — usually
one session per client, sometimes an orchestrator session like this one doing
maintenance across all clients. Nothing here should ever be "in the air": every
file, number, and folder must be traceable to a source, a date, and a reason.
These rules exist so that traceability survives across sessions that don't share
context with each other.

This file is auto-loaded as project instructions in every session opened
against this repo — you are reading it because the harness put it in front of
you before your first action, not because you went looking for it. Treat it
that way: nothing below is optional context, it overrides default behavior.

## Initialization protocol — when a session starts

The repo owner's normal way of starting a per-client session is a single
line like *"this session is for `<client>`"* — no other setup. Treat that
line as the initialization directive and, before doing anything else the
message asks for:

1. Resolve `<client>` to its folder slug under `clients/`. If it doesn't
   exist yet, create it from `clients/_TEMPLATE/README.md` — don't invent an
   ad hoc structure.
2. Resync that client's Profile and Sourcing-configs table from
   `tracking_clients` (`get_client`, `list_sourcing_configs`) immediately —
   before reading further into whatever else the message asks, since
   everything after depends on this being current.
3. Read the client's existing **History** section for prior reasoning/context
   left by earlier sessions — don't re-derive decisions that are already on
   record.
4. Scope all work for the rest of the session to `clients/<slug>/` unless the
   user explicitly asks for something repo-wide.
5. Confirm back in one line what client/config you're now scoped to before
   moving on, so drift between what the user meant and what got loaded shows
   up immediately instead of at the end of a session.

If a session is *not* told a specific client (e.g. this is the orchestrator
doing repo-wide maintenance), this protocol doesn't apply — go straight to
"Session responsibilities" below instead.

## System-level change control

"The overall system" means anything that governs *every* client, not just
one: this file (`CLAUDE.md`), the root `README.md`, `clients/_TEMPLATE/**`,
and `.claude/**` (hooks/settings). These are load-bearing for every session
that will ever run here, including ones with no shared memory of this
conversation.

- **Any change to these requires the repo owner's explicit approval, given
  in that session's own conversation, before the change is made.** A broad
  standing instruction, an inferred preference, or Auto Mode's normal bias
  toward not stopping to ask does **not** count — this is the deliberate
  exception to that bias. Propose the change and stop; don't edit or commit
  it on your own judgment, even if it looks like a small fix or an obvious
  improvement to the standard.
- This applies regardless of which session notices the gap — a per-client
  session that spots a hole in the standard should raise it to the user and
  keep working its own client folder, not patch the system files itself.
- It does **not** apply to anything under `clients/<slug>/**` for the client
  a session is actually scoped to — maintaining that, per the standard
  below, is routine work and needs no special sign-off. It also doesn't
  apply when the user's own message in the current conversation *is* the
  request to change a system file (as with the standards this file already
  documents) — that message is the explicit approval.

## Golden rules

1. **`tracking_clients` MCP is the source of truth**, not this repo. Never
   hand-edit a client's Profile or Sourcing-configs table without first
   re-pulling it (`get_client`, `list_sourcing_configs`) — this repo's copy can
   drift, the MCP server can't.
2. **Every artifact is traceable.** A CSV snapshot, a README edit, a config
   change — each must show *what* produced it, *when*, with *what tool/query*,
   and *why*. If you can't answer all four, don't commit it yet.
3. **Snapshots are append-only.** Never overwrite a dated `*-companies.csv` /
   `*-leads.csv` file. A new pull is a new dated file, even same-day (append
   `-2`, `-3`, ... on a second same-day pull).
3a. **Anything pulled via an API or Clay lands in the repo, in a readily
   accessible format.** If a session calls Blitz, AI Ark, Prospeo, Clay
   (`mcp__Clay__*`), or any other sourcing tool and gets back
   companies/people/enrichment results, that data does not stay only in chat
   output, a temp file, or the third-party tool's own UI — it gets written to
   `sourcing/<config-slug>/<date>-companies.csv` or `-leads.csv` (plain CSV,
   one row per record, header row with clear column names) so any future
   session or human can open it directly, no API replay or Clay login
   required. The Clay workbook link in the README stays as a pointer to where
   the config lives and keeps growing/enriching — it is not a substitute for
   the CSV export of what's in it as of the pull date. No sourcing tool gets
   a free pass on this.
3b. **Every prospect-level (`-leads.csv`) record is keyed by LinkedIn URL.**
   The prospect's LinkedIn profile URL is the unique identifier across every
   tool, snapshot, and session — not an internal ID from Blitz/AI Ark/Clay,
   not email or name (both can collide or change). Every `-leads.csv` must
   have a `linkedin_url` column (the full profile URL,
   `https://www.linkedin.com/in/...`), and it should be the first column.
   Use it to dedupe within and across snapshots for the same config, and to
   cross-reference a prospect between a `-leads.csv` and its parent
   `-companies.csv` row. (Companies already follow the equivalent pattern via
   `company_linkedin_tag` / a standardised domain — keep using that.)
4. **No silent blanks.** If a field has no value (no Clay workbook, no contact
   email), write `-` explicitly. An empty cell reads as "not checked yet"; a
   `-` reads as "checked, none exists."
5. **Commits are the audit log.** Write them to be read later, out of context,
   by someone who wasn't in this session.

## Required sections in every `clients/<slug>/README.md`

Follow `clients/_TEMPLATE/README.md` for the exact layout. In short:

- **Profile** — as today, plus a `**Last synced:**` line (date + which MCP
  calls confirmed it, e.g. `2026-09-14 via get_client + list_sourcing_configs`).
- **Sourcing configs** table — mirrored verbatim from `tracking_clients` at
  sync time. Don't hand-adjust `company_count`; re-sync instead.
- **Sourced data in this repo** — one line per snapshot file already in this
  folder's `sourcing/` tree: file path, row count, config name **and its
  tracking_clients UUID**, the tool that produced it, and the pull date (the
  filename already carries the date, but call it out in prose too since this
  section is the audit index humans and future sessions scan first).
- **History** — reverse-chronological log. One entry per meaningful change to
  this folder: date, what happened, why (one sentence), and what
  session/commit did it. This is the "reasoning" record — the *why*, not just
  the *what* the diff already shows.

## Every time you add a sourcing snapshot

1. Pull the data with the tool the config calls for (see "Sourcing tools"
   below) — record the exact query/filters used.
2. Save the CSV as `sourcing/<config-slug>/<YYYY-MM-DD>-companies.csv` (or
   `-leads.csv`). Never overwrite an existing dated file.
3. If the query had more than a trivial filter or two, save it next to the CSV
   as `<YYYY-MM-DD>-companies.query.md` (or `.json`) — a one-time chat
   explanation is not a durable record; a future session re-reading this repo
   needs the query on disk to reproduce or extend the pull.
4. Update the client's README **in the same commit**: add the row to "Sourced
   data in this repo" and a "History" entry stating tool, row count, and the
   purpose (which ICP/segment/campaign this feeds).
5. Commit with the convention below.

## Commit message convention

```
<client-slug>: <action> — <config-slug> (<tool>, <row-count> rows)
```
Example: `s3-partners: add 2026-09-14 companies snapshot — short-side-blind-spot-salesnav (Blitz API, 42 companies)`

For non-snapshot changes (profile resync, config edit), drop the row count:
`vntana: resync profile + sourcing configs from tracking_clients`

## Cross-referencing rules

- Always give both the human name and the `tracking_clients` UUID for a
  client or config, at least once in the README (the table can use names
  only; the "Sourced data" and "History" sections must carry the UUID).
- Always name the source tool and, where relevant, the exact endpoint (e.g.
  `Blitz API /v2/search/companies`, `AI Ark API POST /v1/companies`, a named
  Clay subroutine).
- Always link the Clay workbook when one exists; write `-` when it doesn't —
  never leave the cell blank.

## Sourcing tools — check status before assuming a tool is live

Confirm the relevant API key is actually present in *this* session's
environment before using a tool (`env | grep -i <NAME>_API_KEY`) — session
environments are fixed at provisioning, so a key added to the environment
config after a session started won't appear until a fresh session is spun up.
As of the last check (2026-09-14):

- **Blitz API** — confirmed live (`BLITZ_API_KEY` present). Call directly over
  HTTPS; the `Blitz-API` MCP tool only searches Blitz's own docs, it does not
  proxy live requests.
- **AI Ark API** — confirmed live (`AIARK_API_KEY` present). No MCP tool at
  all for this one (not even docs) — call directly. Rate limit 5 req/s.
- **Prospeo API** — key reported added to the cloud environment but not yet
  visible in a session's env as of 2026-09-14; re-check
  (`env | grep -i PROSPEO`) before relying on it, and update this file plus
  the root `README.md` once confirmed.
- **Clay** — `mcp__Clay__*` tools, live.
- Any config brief mentioning DiscoLike, EXA, or Sales Navigator names a tool
  not wired into these sessions — run those steps wherever they *are*
  connected and bring the resulting export back here, cited the same way.

## Session responsibilities

**Any session working a specific client**, at the start: follow the
Initialization protocol above, then diff the client's `README.md` against
`tracking_clients` (`get_client`, `list_sourcing_configs`,
`get_sourcing_companies`/`get_sourcing_leads`) and resync if it's drifted.
**During the session, not just at the end:** re-check each rule above before
every commit, not only once at wrap-up — a session that pulls three
snapshots should document and commit each one against this standard as it
goes, not batch the documentation into one pass at the end where something
gets missed. At the end: every new file is referenced in the README, every
change has a History entry, everything is committed — don't leave the
working tree holding undocumented work.

**This orchestrator session's ongoing job**: periodically audit that every
client folder still matches this standard — README present with all four
sections, every CSV referenced, no unexplained drift from `tracking_clients` —
and fix or flag anything that slipped through a per-client session.
