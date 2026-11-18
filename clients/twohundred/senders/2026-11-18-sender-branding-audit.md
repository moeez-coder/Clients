# twoHundred sender branding audit (2026-11-18)

**Client:** twoHundred, tracking_clients `6de16a2e-b5af-4380-acad-685a519744b5`, HeyReach workspace `172772`.
**Why:** on 2026-11-18 all 14 workspace accounts were put on the 5 live campaigns (C1 729831, C5 729838, C7 729841, C6 729840, C11 739441). Only Chavali Praneeth (265480) had been confirmed branded for twoHundred (2026-11-16). This audit checks the other 13 before Moe decides who stays.
**Scope:** read-only. No senders were added or removed, and no campaign was paused or started.

## Sources

- **Account list, ids, emails, connection and Sales Nav state:** `list_client_accounts` and `get_campaign_senders` (C1 `094e9b70-…`, C5 `0637bac6-…`), tracking_clients MCP, 2026-11-18.
- **Profile evidence:** screenshots of each account's HeyReach profile card, pasted by Moe into the session on 2026-11-18. The card shows name, headline, location and current position.
- **What did not work:**
  - HeyReach API: no connector in this session reaches workspace 172772. All 30 HeyReach connectors returned 401 or "Workspace 172772 isn't available for this key" on `get_linked_in_account_by_id`.
  - Public profile URLs: these were not available, so Blitz person enrichment (`/v2/enrichment/person`, which needs a LinkedIn URL) could not be run.
- **Branding standard:** `get_client_sdr_profile` (built 2026-11-09), the same text as tracking_clients `sdrDefault*`:
  - **Headline:** "Enterprise Account Executive @twoHundred | Direct Access to Nordic Top 200 C-Level Buyers | Invitation-Only Executive Communities, Not Leads From a List"
  - **Job title:** Enterprise Account Executive at twoHundred (company page `linkedin.com/company/twohundred-aps`)
  - **Location:** Copenhagen, Capital Region, Denmark

## Verdicts

| Account | HeyReach id | Login email | Current title / company | Headline | Location | Verdict | Evidence | Recommendation |
|---|---|---|---|---|---|---|---|---|
| Chavali Praneeth | 265480 | schavali@gitam.in | `-` (screenshot pending) | `-` | `-` | **branded** (confirmed by Moe 2026-11-16) | Moe's confirmation. Card not yet seen, so it is not yet in use as a reference. | **Keep** |
| Joanna Alipio | 185097 | alipiojoanna@yahoo.com | Legal Project Manager at Reco Legal | twoHundred SDR headline (exact) | New York, US | **partly branded** | Headline is right. Current position is at another agency client (Reco Legal) and the location is New York, not Copenhagen. | Remove until the position and location are changed to twoHundred / Copenhagen. Then keep. |
| Milca Lavarias | 243800 | milkyway101795@gmail.com | Applied Operations at Reco Legal | twoHundred SDR headline (exact) | New York, US | **partly branded** | Same pattern as Joanna. | Remove until fixed. Then keep. |
| Delosjene Encarnado | 182788 | djeneintod0318@gmail.com | Client Operations at Reco Legal | "Client Operations @ReCo.Legal \| 500+ Commercial Contracts Reviewed…" | New York, US | **not branded** (branded for ReCo.Legal) | The whole profile is ReCo.Legal. | **Remove** |
| Marjorie Paulo | 246363 | marjoriepaulo14@gmail.com | (ReCo.Legal) | "Operations Lead @ReCo.Legal \| 500+ Commercial Contracts Reviewed…" | `-` (not shown) | **not branded** (branded for ReCo.Legal) | Headline is ReCo.Legal. | **Remove** |
| Ralph John Taboada | 213851 | ralphjohnmontibanotaboada@gmail.com | Knowledge Operations at Reco Legal | Long ReCo.Legal pitch ("At ReCo.Legal we fixed the part…") | New York, US | **not branded** (branded for ReCo.Legal) | Headline and about are ReCo.Legal copy. | **Remove** |
| Kirky Palamos | 241273 | kirkypalamos18@gmail.com | Missionary at The Church of Jesus Christ of Latter-day Saints | Same as title | `-` | **not branded** (personal profile, never rebranded) | No twoHundred or business content. | **Remove** |
| Christine Joy Ochosa | 251033 | ochosachristinejoy4@gmail.com | Cashier at Sison Bus Stop Restaurant | Same as title | `-` | **not branded** (personal profile, no photo) | No twoHundred content and no headshot. | **Remove** |
| Kimberly Almazan | 203828 | kimberlyjoyalmazan27@gmail.com | `-` | `-` | `-` | **not checked** | No screenshot yet | Hold. Need the profile card. |
| Markim Eniola | 264397 | eniolamarkim@gmail.com | `-` | `-` | `-` | **not checked** | No screenshot yet | Hold |
| Erika Stefani | 182761 | erikastefaniboenari@gmail.com | `-` | `-` | `-` | **not checked** | Recorded on 2026-11-17 as a "placeholder" account | Hold; likely remove |
| Brett Magat | 213311 | brettmagat@yahoo.com | `-` | `-` | `-` | **not checked** | No screenshot yet | Hold |
| Eianne Tantiado | 229280 | tantiadoeianne@gmail.com | `-` | `-` | `-` | **not checked** | No screenshot yet | Hold |
| Shiela Mae Inoc | 230019 | shielamaeinoc0711@gmail.com | `-` | `-` | `-` | **not checked** | No screenshot yet | Hold |

## Other sender health flags

- **Sign-in:** every account is `heyreach_connected: true`, and `get_campaign_senders` reports `not_signed_in: []` on C1 and C5. No broken sign-ins.
- **Sales Navigator:** `sales_nav_connected: false` on all 14 accounts. Ralph John Taboada and Shiela Mae Inoc show `sales_nav_status: redeemed`, but neither is connected; the rest are `not_requested`. Not blocking for connection-request and DM sequences.
- **ReCo.Legal overlap:**
  - The 8 accounts that left the workspace and came back are another client's senders. 4 checked so far are fully branded for ReCo.Legal, and 2 have the twoHundred headline but a ReCo.Legal position.
  - Sending twoHundred copy from a ReCo.Legal profile looks inconsistent to prospects, and it may share daily limits with ReCo.Legal campaigns.
  - Confirm with John (SDR owner) whether these seats are meant to be shared.
- **Campaign state at audit time:** `get_campaign_senders` shows C1 (729831) and C5 (729838) as **PAUSED**, with `active_campaigns: 0` on every sender. The 2026-11-18 History entry had all five IN_PROGRESS. C6, C7 and C11 were not re-checked. This session did not pause anything.

## Recommended sender list

- **Keep now:** Chavali Praneeth (265480).
- **Keep after a fix:** Joanna Alipio (185097) and Milca Lavarias (243800). Change their current position to "Enterprise Account Executive at twoHundred" (select the twohundred-aps company page) and their location to Copenhagen.
- **Remove:** Delosjene Encarnado (182788), Marjorie Paulo (246363), Ralph John Taboada (213851), Kirky Palamos (241273), Christine Joy Ochosa (251033).
- **Decide after their profile cards are seen:** Kimberly Almazan (203828), Markim Eniola (264397), Erika Stefani (182761), Brett Magat (213311), Eianne Tantiado (229280), Shiela Mae Inoc (230019).
