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
3b. **Every prospect-level (`-leads.csv`) record is keyed by LinkedIn URL —
   this is *why* every pull gets stored, not just a formatting rule.** The
   whole point of 3a landing every pull on disk is to make deduplication
   possible: without the file, there's nothing to check a new pull against.
   The prospect's LinkedIn profile URL is the unique identifier across every
   tool, snapshot, config, and session for that client — not an internal ID
   from Blitz/AI Ark/Clay/Prospeo, not email or name (both can collide or
   change). Every `-leads.csv` must have a `linkedin_url` column (the full
   profile URL, `https://www.linkedin.com/in/...`), and it should be the
   first column. Use it to dedupe:
   - within and across snapshots for the *same* config (a re-pull growing
     the same segment),
   - and **across a client's other configs/segments** too — since this
     agency pursues every segment for a client (see "Campaign build
     standard" below), the same prospect can legitimately surface in more
     than one segment's pull, and it's worth knowing that rather than
     discovering it downstream. Before or after a new `-leads.csv` lands,
     check it against that client's other existing `-leads.csv` files for
     `linkedin_url` overlap, and note anything meaningful in the pull's
     History entry (e.g. "N of these also appear in `<other config-slug>`").
   Also use `linkedin_url` to cross-reference a prospect between a
   `-leads.csv` and its parent `-companies.csv` row. (Companies already
   follow the equivalent pattern via `company_linkedin_tag` / a standardised
   domain — keep using that, unchanged, for company-level dedup.)
4. **No silent blanks.** If a field has no value (no Clay workbook, no contact
   email), write `-` explicitly. An empty cell reads as "not checked yet"; a
   `-` reads as "checked, none exists."
5. **Commits are the audit log.** Write them to be read later, out of context,
   by someone who wasn't in this session.

## Campaign build standard per client

Clients aren't one ICP. Most have several segments in play at once, and this
agency reaches out across every segment worth pursuing for a client — not
just whichever one happened to get sourced first. That shapes how sourcing
and campaign work gets scoped and recorded:

- **Segment = sourcing config.** Each `sourcing/<config-slug>/` folder is one
  segment. A brand-new config-slug appearing means a new segment is being
  opened up; a new dated CSV inside an *existing* config-slug means that
  segment is being expanded or refreshed. Say explicitly which one it is in
  the pull's History entry ("new segment" vs "expanding existing segment") —
  that distinction is exactly the kind of thing this repo exists to keep
  visible instead of buried in someone's memory of a session.
- **Outreach depth *per company* follows TAM/SAM, inversely — but total
  volume is never the thing being cut.** When deciding how many contacts to
  pull per company for a segment: a **small** TAM/SAM (few target companies
  in the segment) means reach out to **more** people at each one; a
  **large** TAM/SAM (many target companies) means reach out to **fewer**
  people at each one, because there are more companies to spread across, not
  because the segment should be pursued more conservatively overall. **We
  always want more people reached, not less** — when genuinely unsure how
  many contacts to pull, per company or in total, err toward more. Record
  the TAM/SAM read and the per-company contact count that decision produced
  in the pull's History entry or its `.query.md` file — that number should
  never show up unexplained.
- **The full build for a client/segment has three parts**, and all three
  should end up traceable in this repo, not just remembered:
  1. **Implement the campaign(s) already defined for the client in
     `tracking_clients`.** That MCP server holds the client's actual
     configured campaign/sequence per segment (`get_campaign`,
     `get_campaign_sequence`) — build it out for real wherever it needs to
     run (HeyReach, Clay, etc.), don't leave it sitting as tracked metadata
     only.
  2. **Run the HeyReach Vertical Launch structure** (4 campaigns + 2
     webhooks) per segment/vertical — condensed steps further below so this
     doesn't require re-invoking the skill just to recall them.
  3. **Run a Casual Connections campaign on behalf of the client** — see the
     `anthropic-skills:casual-connections-campaign` skill. This one is new
     and deliberately not final: improve it as real runs surface what
     actually works, the same way this repo's own standards evolve.

The skill roster for this workflow is expected to keep growing — don't treat
the list above as fixed. Check what's actually available (the skills listing
surfaced to the session) rather than assuming only these exist.

## Required sections in every `clients/<slug>/README.md`

Follow `clients/_TEMPLATE/README.md` for the exact layout. In short:

- **Profile** — as today, plus a `**Last synced:**` line (date + which MCP
  calls confirmed it, e.g. `2026-09-14 via get_client + list_sourcing_configs`).
- **Sourcing configs** table — mirrored verbatim from `tracking_clients` at
  sync time, plus a **Scope** column (`General` or `Campaign-specific: <name>`)
  that isn't in `tracking_clients` — set it from the scope decision made
  before that config's data was pulled (see "Sourcing protocol" below). Don't
  hand-adjust `company_count`; re-sync instead.
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
3a. For a new `-leads.csv`: check its `linkedin_url` values against that
   client's other existing `-leads.csv` files (this is the dedup this repo's
   storage exists to enable — see 3b above). Note any overlap in the History
   entry rather than silently dropping or silently keeping duplicates.
4. Update the client's README **in the same commit**: add the row to "Sourced
   data in this repo" and a "History" entry stating tool, row count, the
   purpose (which ICP/segment/campaign this feeds), and any cross-segment
   overlap found in step 3a.
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

## HeyReach Vertical Launch — condensed reference

Full skill: `anthropic-skills:heyreach-vertical-launch`. Condensed here so a
session doesn't have to re-invoke the skill just to recall the steps — if
anything here looks like it's drifted from the actual skill, re-read the
skill before relying on this section.

**4 campaign types, in dependency order:**

| # | Type | Sequence | Feeds |
|---|---|---|---|
| 1 | Con Req | single `CONNECTION_REQUEST`, withdraws unaccepted after 25 days | fires `CONNECTION_REQUEST_ACCEPTED` — this is what the **Acc webhook** scopes to |
| 2 | Con Acc | 3-message `MESSAGE` sequence (`{message1}`/`{message2}`/`{message3}`, 3-day then 1-day delays) | terminal — receives leads from Clay once accepted, no webhook |
| 3 | Open Check | `CHECK_IS_OPEN_PROFILE` → `VIEW_PROFILE` | fires `VIEWED_PROFILE` — this is what the **Open webhook** scopes to |
| 4 | Open Profile | single `INMAIL` (`{subject}`/`{inmail}`) | terminal — receives leads from Clay once confirmed open-profile, no webhook |

**The trap:** each webhook scopes to the *check/request* campaign, not the
*message-sending* campaign whose name matches the event — Acc webhook → Con
Req campaign; Open webhook → Open Check campaign. Getting this backwards is
a real bug that has happened (Vertical 3).

**Open Check needs senders with active Sales Navigator.** `CHECK_IS_OPEN_PROFILE`
only works from a LinkedIn account that has an active Sales Nav seat —
assign a sender pool without one to Open Check and the campaign won't launch
out of DRAFT (Step 3's start-then-pause fails). Confirm Sales Nav status for
the sender pool at Step 0, before Step 2 assigns senders — if the pool
lacks Sales Nav coverage, flag it and ask rather than assigning senders that
will make Open Check un-launchable.

**Default templates to clone** (Vertical 1's canonical campaigns, unless
told to clone from a different vertical): Con Req `567452`, Con Acc
`554375`, Open Check `567476`, Open Profile `557771`.

**Naming:** `{Region} | {Type} | Vertical {N} |Moe {version}`, applied to
both the campaign and its dedicated list. One list per campaign type — never
shared across types, never reused from another vertical.

**Steps:**

0. **Gather inputs — ask, don't guess:** vertical id + region prefix,
   version label, sender pool (LinkedIn account IDs) **with each account's
   Sales Navigator status confirmed**, and both Clay webhook URLs (Connection
   Accepted, Open Profile/Viewed Profile).
1. **Create 4 lists** (`create_empty_list`, `USER_LIST`), one per type,
   named per convention.
2. **Create 4 campaigns** (`create_campaign_from_template`) — first 100
   sender IDs from the pool go to every campaign (hard API cap, confirmed no
   workaround; anything beyond 100 gets added manually in the UI
   afterward). **Open Check gets only senders with active Sales Navigator**
   (see above) — don't assign it the same unfiltered pool as the other
   three if the pool includes non-Sales-Nav accounts. Verify each cloned
   sequence immediately with `get_campaign_sequence`.
3. **For Con Req and Open Check only:** `start_campaign` then immediately
   `pause_campaign`, and confirm `startedAt` is non-null via `get_campaign`.
   This is the only way to make a DRAFT campaign webhook-eligible —
   `create_webhook` 404s on a campaign that's never been started. Con
   Acc/Open Profile stay in DRAFT; they don't need this. A campaign's list
   can't be changed once it's ever been started (even paused, even empty) —
   the list must be right *before* this step. A `500` from `start_campaign`
   is a known transient platform issue: retry once, and if it still fails,
   tell the user to start that one manually in the UI and continue with
   whatever else can be completed rather than blocking the whole build.
4. **Create 2 webhooks** (`create_webhook`): Acc webhook
   (`CONNECTION_REQUEST_ACCEPTED`) scoped to Con Req's campaign ID; Open
   webhook (`VIEWED_PROFILE`) scoped to Open Check's campaign ID. Verify each
   immediately with `get_webhook_by_id` — this is exactly where the
   Vertical 3 bug slipped through.
5. **Report back:** all 4 campaigns (id/name/list/sender count/sequence
   verified), both webhooks (id/event/scoped campaign/active), and anything
   incomplete (senders beyond 100 to add manually, a campaign stuck in
   DRAFT pending manual start, a webhook not yet attached).

No delete-campaign tool exists — only pause; a wrongly-created campaign gets
paused and flagged for manual deletion in the UI. `delete_webhook` requires
deactivating it first (`update_webhook`, `isActive: false`).

## Sourcing protocol — tool order, scope, and what to pull

- **Tool priority is cost order — cheapest first, escalate only when needed.**
  For any sourcing pull, try tools in this order and move to the next only
  when the current one can't cover what's needed (missing companies/people,
  weak match quality, no LinkedIn found) — don't reach for a pricier tool by
  default just because it's more capable:
  1. **Clay** (`mcp__Clay__*`)
  2. **Blitz API**
  3. **Prospeo API**
  4. **AI Ark API**
  Check "Sourcing tools" below for whether a given tool is actually live in
  *this* session before planning to use it.
- **LinkedIn is the only identifier we need — don't spend on email
  enrichment.** A sourcing pull only needs each prospect's `linkedin_url`
  (and each company's `company_linkedin_tag`/domain) — skip any step that
  enriches for email unless a specific campaign explicitly requires outbound
  email. This keeps cost down and matches LinkedIn URL already being the
  required unique key for prospect records (see 3b above).
- **Two sourcing scopes exist — ask which one before pulling, don't infer
  it:**
  - **General** — a larger, broader audience for the client, not tied to any
    one campaign's exact requirements.
  - **Specific** — narrower, built to one campaign's exact targeting
    criteria, pulled only when that particular campaign actually needs it.
  - Default posture is to **ask the user which scope they want** before
    starting a pull. Once decided, record it — in the config's row/History
    entry, e.g. "General" or "Campaign-specific: `<campaign name>`" — so a
    future session understands why that pull's breadth was chosen without
    having to ask again.

## Sourcing tools — check status before assuming a tool is live

Confirm the relevant API key is actually present in *this* session's
environment before using a tool (`env | grep -i <NAME>_API_KEY`) — session
environments are fixed at provisioning, so a key added to the environment
config after a session started won't appear until a fresh session is spun up.
As of the last check (2026-09-14):

- **Clay** — `mcp__Clay__*` tools, live.
- **Blitz API** — confirmed live (`BLITZ_API_KEY` present). Call directly over
  HTTPS; the `Blitz-API` MCP tool only searches Blitz's own docs, it does not
  proxy live requests.
- **Prospeo API** — key reported added to the cloud environment but not yet
  visible in a session's env as of 2026-09-14; re-check
  (`env | grep -i PROSPEO`) before relying on it, and update this file plus
  the root `README.md` once confirmed.
- **AI Ark API** — confirmed live (`AIARK_API_KEY` present). No MCP tool at
  all for this one (not even docs) — call directly. Rate limit 5 req/s.
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
