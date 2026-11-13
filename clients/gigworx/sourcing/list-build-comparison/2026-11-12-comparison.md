# List building: GTM Sheets vs Claude Code (head-to-head, 2026-11-12)

**Client:** GigWorx (`94da4a2f-8f90-4bc0-87e6-22ff98fafd6a`). **Campaign used:** C3 RV Corridor Ramps (`020a9904-2e57-4fe1-aa0b-2bc1776603db`).
**Input (same for both):** 50 Elkhart County manufacturers with 51–1,000 employees. They are a seeded random sample (`random.seed(7)`) of the 140 eligible rows in `../michiana-shift-employers/2026-11-05-companies.csv`.
**Process (same for both):**
1. Enrich companies.
2. Filter them against the ICP (builds or supplies the RV/trailer industry).
3. Check the hiring signal (hourly postings in the last 90 days).
4. Find up to 2 plant or production leaders per company.
5. Find their work emails.
6. Write Message 1 from the approved C3 copy, falling back to the question-only CTA when no posting is found.

**Where each run lives:**
- **Claude Code:** Python scripts call the Blitz API directly. Claude made the ICP call in the session. Outputs: `2026-11-12-cc-companies.csv` and `2026-11-12-cc-leads.csv`.
- **GTM Sheets:** workbook "GigWorx - List build test (GTM Sheets vs Claude Code)" (`2e7fb17a-cb99-4a09-97ac-14804e3f0fa7`), table `Companies` (`5f716885-f595-4333-b5ae-beb92bdf8219`). Exports: `2026-11-12-gtm-companies.csv` and `2026-11-12-gtm-leads.csv`.

## Results

| Step | Claude Code | GTM Sheets |
|---|---|---|
| Company enrichment | 50/50, 18 s (Blitz `/v2/enrichment/company`) | 50/50, near-instant (`blitz_company` column) |
| ICP filter | **15 fit**, 12 "maybe" flagged and dropped, 23 no. Claude read every profile; no AI spend. | **14 fit**. The first run returned 0/50 (bug 1 below). After the fix: Gemini 3.8 Flash, about $0.001/row, about 9 min wall-clock (shared queue). |
| Agreement on fits | 12 companies in common. CC only: Cleer Vision Tempered Glass, United Trailers, Postle Aluminum. GTM only: Big Dog Adhesives, Dec-O-Art. | (same) |
| Hiring signal | 1 of 15 with postings (MORryde: 7, e.g. Material Handler) | 1 of 14 (MORryde). Same data source, same result. |
| People | **14 people at 9 companies** via Waterfall ICP (title tiers) | **Waterfall unusable (bug 2).** Fell back to Employee Finder (job level/function, not titles): **12 people at 7 companies** |
| Persona quality | Plant Manager, Production Manager/Supervisor, GM, Director/VP Operations, President | Weaker: includes Quality Manager, EHS/Maintenance Manager, Director of Service Ops, Assistant Project Manager |
| Local to Michiana | 9 of 14 (the Waterfall location filter was set to US only; a city filter fixes this) | 7 of 12 (Employee Finder has no person-location filter in the column) |
| Emails | 8 of 14 found; 1 stale (old employer's domain) | 9 of 12 found; the same stale one |
| Copy | Python template, correct on the first try | Formula column. It first missed the posting signal (bug 3), then worked. |
| Output shape | One row per person, keyed by `linkedin_url`, ready for HeyReach | **One row per company**, with people in P1/P2 columns. Pushing to HeyReach needs one row per lead, so this needs a second table or a send step. |

## Bugs and gotchas found in GTM Sheets during the test

1. **A prompt sees an enrichment column only as its display value.** `{{Company Enrichment}}` in the AI prompt resolved to the company name, not the profile, so every company was judged on its name and 0/50 passed. Fix: pull `description`, `industry` and `specialties` out with field columns first.
2. **The `blitz_waterfall_icp` action is broken.** It sends `cascade[].location.country_code` as a string, and Blitz rejects every call with HTTP 422. This happens with a country set and with none set. Waterfall (title tiers) is the best people tool for this job, and it can't run in GTM Sheets until this is fixed.
3. **A formula also sees an enrichment column only as its display value.** The copy formula couldn't read the job list, so MORryde got the no-signal fallback. Fix: a field column (`jobs.0.title`).
4. **Typed columns reject the repo's `-` convention.** The first insert failed on 6 rows whose Domain was `-`; it needed `invalid: blank`.
5. **There is no fan-out from one company to many people.** The people search returns a JSON list in one cell. Each slot needs its own field columns and its own email column.
6. **AI columns share one queue.** The 50-row ICP check took about 9 min while 940 other AI cells ran.
7. **Elsewhere this session:** `create_campaigns_from_plan` demands `confirm: true` but its schema has no `confirm` field, so it can't be used. Industry and keyword filters on GetLeads people search return 0–27 rows for this market.

## Shortcomings of GTM Sheets compared with Claude Code

- **Tool coverage depends on what the platform wraps, and the wrappers have bugs.** Claude Code calls any endpoint with any parameter; GTM Sheets only exposes the options its actions surface. Waterfall was broken and Employee Finder couldn't filter by person location here, both of which cost persona quality.
- **Company and person are different shapes.** Turning one company into N people takes extra tables or P1/P2/P3 columns, and every enrichment has to be repeated per slot.
- **Hidden data flow.** Prompts and formulas see enrichments as display values. That failure is silent: the run "succeeded" with 0/50 fits.
- **Judgment is per row and costs money.** Each AI cell decides alone, with no view of the batch, so it can't calibrate. It also spends tokens on every row, and in the bulk C1–C6 run it spends them on every *person*, re-researching the same company for each one.
- **Throughput.** The AI queue is shared, so one big run slows everything else.
- **Traceability.** The logic lives in column settings rather than a file, and the result has to be exported to reach the repo audit trail (rule 3a).

## Shortcomings of Claude Code compared with GTM Sheets

- **No shared, living workspace.** The output is a CSV. A teammate can't open it, filter it, change a status and push to HeyReach from one screen, and nothing refreshes by itself.
- **Not repeatable without an operator.** GTM Sheets auto-runs columns on new rows and has scheduled signals. In Claude Code someone has to re-run the scripts. The judgment also lives in the session (Claude reading 50 profiles), which is accurate but doesn't scale to thousands without batching or LLM calls.
- **Narrower web research by default.** The GTM `Qualify` column browses careers pages and Indeed per row. The Claude Code run used Blitz's structured job data, which covers small RV plants poorly (1 of 15). Claude Code can search the web too, but that is manual or extra scripting.
- **Easy to miss guardrails.** The Waterfall location filter in the script was too loose (5 non-local people), and the stale-email check was added afterwards. GTM Sheets' built-in exclusion list and typed columns catch some of this automatically.
- **HeyReach and `tracking_clients` integration** happens through separate calls, not one push column.

## Verdict

- **Discovery, filtering and people selection: Claude Code.** On the same 50 companies it found more and better-matched people (14 at 9 companies versus 12 at 7), and ran in about 40 s of API time. It hit no platform bugs, and its ICP judgment saw the whole batch.
- **Operation after the list exists: GTM Sheets.** It is better for review, status changes, pushing to HeyReach and auto-processing new rows.
- **Recommended split:** build and judge the list in Claude Code, writing a per-person CSV into the repo, then load it into the campaign's GTM Sheets `Leads` table for review and the HeyReach push. Fix GTM bugs 1–3 before using it for discovery.
