# Claude Code list build for C1–C6: method (2026-11-12)

**What:** `2026-11-12-companies.csv` is the segment-labelled company universe behind the Claude Code-built lead lists for campaigns C1–C6. `2026-11-12-cc_build.py` is the exact script that produced the per-campaign `../c*/2026-11-12-3-leads.csv` files.
**Why:** The repo owner asked to set GigWorx up in HeyReach "using the leads from Claude Code for now". That follows the recommended split in `../list-build-comparison/2026-11-12-comparison.md`: build and judge the list in Claude Code, then review it in GTM Sheets.
**Config:** GigWorx - Michiana shift employers (`184a0f39-d738-4f8f-a908-3c97d71dd4cf`). The per-campaign leads go to C1–C6 (config UUIDs in the client README).

## Steps
1. **Candidates (1,596 companies).**
   - Sources: the 2026-11-05 Blitz `POST /v2/search/companies` universe (4,378 companies, re-pulled with descriptions) and the `tam-by-jobs` hiring-signal companies.
   - Excluded: rows tagged out-of-ICP or staffing competitor by keyword, and rows with no company LinkedIn URL.
2. **Segment labels.**
   - Claude Code subagents read each company's name, industry, description and size.
   - Labels: RV, MFG, WH, FB, RETAIL_BIG, RETAIL_SMALL, HOSP or NO.
   - Results: RV 138, MFG 408, WH 73, FB 45, RETAIL_BIG 12, RETAIL_SMALL 192, HOSP 263, NO 464.
   - Each label row was validated against the input by number and name. 1 row was rejected as a mismatch, so the CSV has 1,595 rows.
3. **Campaign plan.**
   - C3: RV.
   - C5: MFG, WH, FB or retail with 1–50 employees.
   - C1: MFG with 51+ employees.
   - C2: WH, FB or RETAIL_BIG.
   - C6: HOSP.
   - C4 (added on top): any of the above with 51+ employees.
4. **Hiring-signal gates** (Blitz `POST /v2/jobs/company`).
   - Search: hourly titles, last 60 days, `job.location.city.include` set to the Michiana towns.
   - Gates: C1 needs 3+ open hourly roles; C2 needs a seasonal/temp posting or 5+ roles; C4 needs 5+; C6 needs a hospitality role. C3 and C5 have no gate (their copy falls back to a question-only CTA).
   - Planned → passed the gate: C1 203 → 12, C2 56 → 12, C3 138 → 138, C4 384 → 17, C5 467 → 467, C6 263 → 2.
5. **People** (Blitz `POST /v2/search/waterfall-icp-keyword`).
   - Title tiers are set per campaign (see `TIERS` in the script).
   - Person location is restricted to the 10 Michiana cities.
   - **Per-company depth follows TAM/SAM, inversely:**
     - C5 has a large SAM (467 owner-run companies), so 1 owner per company.
     - C4 has a small SAM (17), but HR needs 2 per company.
     - C1, C2, C3 and C6: up to 3 per company at 51+ employees, 1 at under 50.
6. **Dedupe** by `linkedin_url` across campaigns. Priority: C4 > C3 > C6 > C1 > C2 > C5. 170 raw → 166 unique.
7. **Email** (Blitz `POST /v2/enrichment/email`).
   - 97 found; 8 were dropped because the email's domain didn't match the company domain. That leaves 89 kept.
   - No email was typed by hand. A blank in the CSV is `-`, meaning checked and none found.
8. **Copy:** Message 1 comes from the approved campaign doc (`4d41ad80-0451-4524-bf83-819a4418be7b`).
   - The `signal` variant names the role taken from the job title (cleaned by `clean_role`).
   - The `question-only` variant is used when there's no posting.
   - Post-fixes: "Marc A." → "Marc", and C6's role_title is "housekeeper" to match its message (the oldest posting was a Cook role, but the message uses the hospitality posting).

API calls: jobs 660, waterfall 648, email 166. Responses were cached on disk, so a re-run replays them for free.

## Result (leads per campaign)
| Campaign | Leads | With email | HeyReach list |
|---|---|---|---|
| C1 Hourly Roles That Won't Close | 17 | 9 | 1148941 |
| C2 Peak Season Crews | 14 | 8 | 1148942 |
| C3 RV Corridor Ramps | 85 | 40 | 1148943 (84 loaded) |
| C4 Try Before You Hire | 4 | 4 | 1148944 |
| C5 Owner on the Floor | 43 | 28 | 1148945 |
| C6 Hospitality, Food and Event Crews | 3 | 0 | 1148946 |

## Known limits
- Blitz people coverage is thin for small Michiana firms. For example, C5's 467 companies yielded only 43 owners.
- C4 and C6 are too small to run as they are. The fix is wider people sources (Sales Nav export, Clay) or a looser gate.
- One C3 lead (`linkedin.com/in/ashleybontrager`, Ember RV) came back from Blitz with no name. Its email reads `ashley.lehman@`, which doesn't match the URL slug. HeyReach skips leads with no first name, so it was not loaded. It is held in GTM with Status `Hold - no name`.
