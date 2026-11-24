# What GTM Sheets can do (read 2026-11-24)

Plain-language list for Moe, read from `gtm_sheet_overview`, `gtm_sheet_apify_actors`, `gtm_sheet_signals` and the GTM Sheets tool descriptions on the tracking_clients MCP. GTM Sheets is Algo Acquisition's own table app (dashboard.algoacquisition.ai/gtm-sheet). Size today: 65 folders, 178 workbooks, 399 tables, about 7.8M rows.

## Data providers (keys set)

| Provider | Key set | What it is used for |
|---|---|---|
| Blitz | yes | Default for Find companies and Find people; companies hiring for a role; companies employing a persona; every enrichment column (email, person, company, decision-maker waterfall, employee finder, company jobs, domain to LinkedIn and back, country / department split) |
| GetLeads | yes | Companies and people with work emails and phones; **free counts**; the only provider for phone-number columns. No state filter on company search |
| ColdIQ | yes | "Complete TAM" search across ColdIQ's own data and 40+ providers (people, companies, lookalikes, hiring companies); enrich person / company / email / phone |
| DiscoLike | yes | Company lookalikes (up to 10 seed domains) or a plain-English description, website phrases, revenue band |
| Exa | yes | AI web search for companies from a description (up to 100 per search) |
| HarvestAPI | yes | LinkedIn person lookups (`harvest_person` enrichment) |
| Apify | yes | Run any Apify actor into a table (see below) |
| Findymail | yes | Work email column |
| Spider Cloud | yes | Web search and page reads for AI columns |
| OpenRouter | yes | Models for AI columns (hit its $1,000 cap on 2026-11-16; check before relying on AI columns) |
| AI Ark | **no** | - |
| Signalbase | **no** | Job-change / recently-hired people (free counts) once a key is set |

## Apify actors ready to run

Google Maps scraper (and Maps extractor, email extractor, reviews); LinkedIn Jobs scraper (curious_coder, bebity); **Indeed scraper**; HarvestAPI LinkedIn profile search and profile scraper (no cookies); LinkedIn profile posts; Leads Finder ($1.5 per 1,000 leads, Apollo alternative); mass LinkedIn profile scraper with email; Google Search results; Website Content Crawler and Web Scraper; Contact Details scraper; Facebook / Instagram / TikTok / YouTube / X scrapers; our own `algoacquisition/my-actor`. Each run has a dollar cap (default $10, max $50; $25 a day per actor, $60 a day for all Apify).

## Signals (scheduled pulls that add new rows)

A table can carry a signal: a provider plus settings that re-run on a schedule and add only new rows (deduped on a field). Live today:
- **Indeed + LinkedIn open roles, daily** (actor `LzsIpToRTUZSnqjbS`) for Talent Edge: London (3,249 rows, about 200 new a day) and New York (4,291 rows). Search terms, excluded agencies and excluded title words are all settings. The same pattern would give GRN a daily open-leadership-role feed for NC/SC or Eastern/Central manufacturers.
- **LinkedIn post engagers, weekly** (HarvestAPI) for "Engagement | Joe & David".

## Functions (reusable multi-step workflows)

- **Open Profile Inmail Flow**: cleans company and first names, finds website and LinkedIn, scores buying signals, writes the InMail and subject (27,911 calls).
- **Connection Accepted Flow**: from a HeyReach connection-accepted webhook, cleans names, finds the company, summarises it, builds 7 buying signals and writes messages 1 to 3 (7,781 calls).
- **TAM lead check**: free rules, no AI: is this lead a real decision maker at the TAM company? Outputs Keep and Reason (19,833 calls).

## Column types

- **AI columns**: any OpenRouter model, prompt with `{{Column}}` references and the client's ICP (`{{@client.icp}}`), optional web access via Spider, text or JSON output, or a saved agent.
- **Enrichment columns**: the Blitz / ColdIQ / Findymail / GetLeads / HarvestAPI lookups above, plus free `enrich_person` from our own Enrich Person database.
- **Lookup** (e.g. against a DNC table), **send** (write rows into another table, one per item of a list), **formula** (JavaScript per row, free), **field** and **merge** (read JSON / first non-empty).
- **HeyReach push**: push each row as a lead into a HeyReach campaign with custom fields, gated by `run_if`.
- Every runnable column takes auto-run, `run_if` and a delay.

## Other useful parts

- Each client gets a folder with an **Exclusion list** workbook built from their DNC; company and people searches into that client's tables leave those companies out automatically.
- Tables can be filled from a webhook (how this repo loads its CSVs), CSV import, Find companies / Find people (with a free preview or count first), or an Apify run.
- CSV export with a download link; usage reporting per teammate (cells run, AI cost, Spider credits).
