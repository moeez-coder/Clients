# We Are DNA: Casual Connections plan, v0 for Moe (2026-11-18)

**Status:** internal draft for Moe. Nothing has been built, pushed or started. This is not a client campaign doc and has no tracking_clients doc id.
**Asked for by:** Moe, 2026-11-18. It is part 3 of CLAUDE.md's campaign build standard.
**Skill:** `anthropic-skills:casual-connections-campaign` is **not in this session's skills listing**. So this plan follows CLAUDE.md's standards plus Moe's brief.
**Session:** session_013MzxQfxb1tFTNdnVAHYrw5.

## 1. Who sends: the blocker

| Person | Role | Source | In HeyReach 172307? |
|---|---|---|---|
| John Tarrant | **Founder** (2010), now Founder & Chair (since 21 Jul 2026); still the client contact | wearedna.co.uk team page; Worldcom press release, 21 Jul 2026 | **No** |
| Eoin Rodgers | Managing Director, joined Jul 2026 (not a founder); about 500 connections, 2,789 followers | wearedna.co.uk; linkedin.com/in/eoinrodgers | **No** |
| Chris Bennett, Fiona Stewart | Partners (Creative; Client Strategy & Digital) | team page | **No** |

- **What the workspace holds:** all 10 HeyReach sender accounts are VA/SDR seats: Ian Vilarde, Gyrichy Padua, Alden Damlu-an, Mikle Patalinghug, Zarrah Sotillo, Samantha Siervo, Kelly Cruz, Kent Lor Daguimol, Arpit Singh and Marichu Lomonsod.
- **How it was checked:** tracking_clients `list_client_accounts` (10 rows, all `va::`, `clientAccountSyncRows` empty) and `get_campaign_senders` on Campaign 6. Those return every account in workspace 172307; `available` and `not_signed_in` are both empty.
- **Consequence:** **no founder account is connected, so Casual Connections can't send yet.** John's LinkedIn has to be added to HeyReach workspace 172307 first, plus Eoin's if Moe wants a second sender.
- **To check once connected:** whether John's account has Premium. Free LinkedIn accounts cap personalised connection notes at a few a month, and limit note length.

## 2. Volume vs capacity

- **LinkedIn's weekly invitation limit:** about 100 a week for most accounts, and up to about 200 for older, well-accepted accounts. HeyReach's safe default for a new sender is 15 to 20 a day, ramping up.
- **At 7 days a week** (the repo rule): about 15 a day per founder, so about 100 a week.

| Senders | Invites per week | 4-week wave | Whole 29,489-company TAM at 1 contact each |
|---|---|---|---|
| John only | about 100 | about 400 | about 5.5 years |
| John + Eoin | about 200 | about 800 | about 2.8 years |

**Proposed wave 1: Bristol-HQ companies in the TAM.**
- **Pool:** 312 companies, all sizes, all five sectors.
- **Why Bristol:** DNA is a Bristol agency and John founded it there, so "local peer" is the genuine reason a founder connects. That keeps it casual, not salesy.
- **Expected size:** the preview yielded about 0.95 usable C-suite contacts per company. With 2 per company at 201+ staff, wave 1 is about **300 to 350 contacts**, roughly 3 to 4 weeks for John alone.
- **Wave 2:** the rest of the South West, about 1,040 companies.
- **Wave 3+:** the national list, largest companies first, and only once wave 1's acceptance and reply rates are known.

## 3. Preview list (25 asked, 19 usable from 20 companies)

The full file is `sourcing/casual-connections/2026-11-18-preview-leads.csv`; removed rows stay in it with their reasons. The query is in `2026-11-18-preview.query.md`.

| Name | Title | Company | Sector, size |
|---|---|---|---|
| David Haynes | Chief Executive Officer | ARAG Legal Services UK | Financial services, 501-1,000 |
| Kate Banks | Chief People Officer | ARAG Legal Services UK | Financial services, 501-1,000 |
| Jodie Sinclair | Senior Partner | Bevan Brittan LLP | Law, 501-1,000 |
| Roger Bull | Managing Partner | Burges Salmon LLP | Law, 501-1,000 |
| Ross Fairley | Senior Partner | Burges Salmon LLP | Law, 501-1,000 |
| Simon Day | Partner and MD, Commercial Property | Clarke Willmott | Law, 501-1,000 |
| Michael Sansom | Managing Director UK Registry | Computershare UK | Financial services, 1,001-5,000 |
| Stuart Irving | President & CEO (group) | Computershare UK | Financial services, 1,001-5,000 |
| Jeremy Fennell | Chief Executive Officer | Harding+ | Retail, 1,001-5,000 |
| Chris Matthews | Chief Executive Officer (possibly stale) | Harding+ | Retail, 1,001-5,000 |
| Damian Arnold | Chief Executive Officer | Somerset Bridge Group | Financial services, 501-1,000 |
| Teresa Dadey | Chief People Officer | Somerset Bridge Group | Financial services, 501-1,000 |
| Mark Screeton | Chief Executive Officer | SunLife UK | Financial services, 51-200 |
| Victoria Heath | Chief Marketing Officer | SunLife UK | Financial services, 51-200 |
| John Wood | Managing Partner | TLT LLP | Law, 1,001-5,000 |
| Ajith Jayawickrema | Founder Director | Turtle Bay Restaurants | Hospitality, 1,001-5,000 |
| Daniel Hawes Baker | Chief Financial Officer | Turtle Bay Restaurants | Hospitality, 1,001-5,000 |
| Stuart Simpson | Chief Executive Officer | Vertical Aerospace | Manufacturing, 201-500 |
| Stephen Fitzpatrick | Founder | Vertical Aerospace | Manufacturing, 201-500 |

**What the preview taught us** (proposed improvements to the skill when it exists):
- Blitz title matching is fuzzy:
  - "Senior Partner" also matched "Senior People Partner".
  - "Owner" also matched "Product Owner" and law-firm fee earners.
  - The fix is strict excludes plus a regex check after the pull.
- The pool's "private sector" flag lets charities and CICs through (Hft, Sirona, Brandon Trust).
- Clay found CPOs and CFOs that Blitz missed, so the Clay + Blitz pair matters here.
- A big local firm can be a subsidiary of a global group (Computershare), so drop the group-level C-suite.

## 4. Draft copy (UK English, no em dashes, no pitch, no recruitment language)

**Connection note, from John** (153 characters with the variable; 152 with an 11-letter first name):
> Hi {first_name}, I founded DNA here in Bristol back in 2010 and I like to know the people running good businesses locally. Would be good to connect. John

**Connection note, from Eoin, if he sends too** (152 characters with the variable):
> Hi {first_name}, I joined DNA in Bristol as MD this summer and I'm keen to get to know more people leading businesses in the area. Good to connect. Eoin

**Alternative: no note.** A plain request from a founder often gets more accepts from C-suite, and it sidesteps the note cap on free accounts. Worth A/B testing in wave 1.

**Message 1, 1 day after they accept, no pitch:**
> Thanks for connecting, {first_name}. Always good to know more people at the helm of businesses round here. Hope things are going well at {company} heading into the new year.

**Message 2, about 14 days later, optional and soft:**
> {first_name}, we've been pulling together what we've seen keep good people in UK businesses this year, from work with the likes of Superdry and MAN Truck & Bus. Happy to send it over if it's useful, no strings attached.
- Leads with a light "sample deliverable" offer.
- **Moe decides** whether casual connections get any follow-up beyond message 1.
- If the report doesn't exist, cut this message or swap in something DNA really has.

**Rules applied:**
- No "talent", "hiring", "roles" or "candidates".
- No pitch before the person has accepted and replied.
- Signed as a person, never as "the team".

## 5. Proposed build (nothing done until Moe says go)

- **Sourcing:** wave 1 pulled with the Blitz + Clay pair and the same filters as the preview, then normalised, overlap-checked and DNC-checked. It lands as `sourcing/casual-connections/<date>-leads.csv`.
- **HeyReach:** one campaign per founder sender, `UK | Casual Connections | Bristol | {Sender} | Moe v1`, with its own list. Sequence: connection request, then message 1 after +1 day, then (optional) message 2 after +14 days. Withdraw unaccepted requests after 25 days.
- **Schedule:** `update_campaign_schedule` with all 7 days on. Proposed window 08:00 to 18:00 Europe/London, Moe to confirm.
- **GTM Sheets:** one workbook in DNA's folder `9a6928d3-…` with tables 1 Companies (Bristol slice, leads per company), 2 Leads (Status, Push to HeyReach with auto-run off and `run_if` Status = "launch set").
- **tracking_clients:** campaign created and linked, if Moe wants it tracked there.

## 6. Questions for Moe

1. **Sender accounts:** John only, or John and Eoin? Neither is in HeyReach 172307 yet. Who gets them connected (John Paul, infrastructure)?
2. **Wave 1 slice:** Bristol HQ first (312 companies, about 300 to 350 contacts), or a different cut (South West, a sector, or the largest companies nationally)?
3. **Approval route:** does this need John's approval through a campaign doc, or does it run on Moe's approval? It runs from John's own profile, so at the very least John has to agree to the copy.
4. **Follow-ups:** message 1 only, or message 1 plus the soft message 2?
5. **Charities and CICs:** exclude them (as in the preview), or keep them?
6. **Schedule:** 08:00 to 18:00 Europe/London, 7 days a week, OK?
