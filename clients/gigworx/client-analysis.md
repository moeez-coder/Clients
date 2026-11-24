# GigWorx: client analysis

**Client:** GigWorx (`94da4a2f-8f90-4bc0-87e6-22ff98fafd6a`). Contact: Mathew Welsch, owner. Package: Solo.
**Written:** 2026-11-05 by the GigWorx per-client session.
**Sources:**
- Typeform onboarding form, submitted 2026-10-29 (`get_client.icpForm`)
- The generated client brief, client description, caller briefing and caller FAQs (`get_client`)
- The ICP config, sourcing config, campaign and campaign-plan doc in `tracking_clients`
- A market-sizing pull made in this session (Blitz API). The files are in `sourcing/michiana-shift-employers/` and the method is in `2026-11-05-companies.query.md`.

Every claim below is labelled with its source:
- **[form]**: Matt's own words on the onboarding form
- **[brief]**: the generated brief or client description (website research)
- **[data]**: this session's Blitz pull
- **[view]**: my analysis or inference, to be checked

---

## 1. Summary

GigWorx sells **on-demand, W-2 shift labour through an app** to employers who staff hourly roles. The campaign is hyper-local: St. Joseph and Elkhart County, Indiana (Michiana). It runs from **one LinkedIn seat with no Sales Navigator**. The offer is low-friction: **we comp your first shift**.

What the form and the data show together:

1. **The market is about 1,050 companies, not 300–800 [data].** Manufacturing, warehousing and retail companies headquartered in the two counties with 11+ employees come to 1,052. Of those, 329 have 51+ employees. Construction and hospitality, both GigWorx verticals, add about 550 more. This is still a small, finite market, so every lead counts.
2. **Searching by headquarters misses the biggest local employers [data].** Of the 140 companies posting hourly jobs in Michiana in the last 60 days, **108 have their headquarters out of state**: SpartanNash, Lowe's, Vestis, Valmont, JBS, Smurfit Westrock and others. The lead list has to be built on **where the person works**, not where the company is based. The config is already set up as a Clay *people* search, which handles this, but it must filter on person location.
3. **Staffing is crowded locally [data].** There are 14 staffing firms headquartered in the area (Peoplelink, Express Employment's Elkhart franchise, Alliance Staffing, Jobsquad, Agile Staffing, TalentSource and others). National firms (Kelly, PrideNow, Employbridge) also post jobs there. The messaging has to say why GigWorx is *not another agency*. The current copy does this well.
4. **GigWorx has almost no local proof yet [view].** Every named client and stat (Marriott, West Paw's 8,000 shifts, 95% fill rate) comes from the Montana and Utah markets [brief]. A Michiana buyer will ask "who here uses you?" The comped first shift is the right answer to that. We should also ask Matt for any South Bend or Elkhart clients we can name.
5. **One seat sets the pace [view].** One seat at roughly 100–150 connection requests a week (an estimate, not measured) takes about **3–5 months** to reach around 2,000 contacts once. That is fine for a market this size, but it means the order of the list matters. Contact active hirers and the 51–500 employee band first.

---

## 2. The business

| | |
|---|---|
| What they do | App-based, on-demand staffing. A business posts a shift in a web portal, vetted W-2 workers claim it in a mobile app, and GigWorx runs payroll, insurance and compliance [form, brief] |
| One-liner (Matt's words) | "GigWorx connects businesses with skilled, fully-vetted workers in real time. Flexible jobs and on-demand staffing at your fingertips." [form] |
| Founded | 2018 in Montana, after Matt worked in healthcare staffing [brief] |
| Markets | Bozeman/Helena MT, Salt Lake City UT, South Bend–Elkhart IN. Franchising is being explored [brief] |
| Verticals | Manufacturing, warehousing, retail, construction, hospitality, admin, special events [brief] |
| Roles filled | Hourly, shift-based roles: production, warehouse, general labour, event and hospitality staff, retail associates [brief] |
| Commercial model | No subscription, no minimums, no contract. Billed only for hours worked: pay rate plus a markup agreed with the client [form] |
| Temp-to-hire | Flat **$1,500 conversion fee** with no minimum hours. Matt: "we set it low as to not be a barrier" [form] |
| Bad fit handling | Client blocks the worker in the app and GigWorx handles the conversation [form] |
| Claimed proof | 95% shift fill rate. 8,000+ shifts for West Paw over 5 years. Clients include Marriott, ServiceMaster Restore, Albertsons, Arco Murray and SpringHill Suites [brief] |
| Deal value / cycle | **$5,000** average deal value, **10-week** sales cycle [form] |

**How they make money [view].** Revenue is the markup on worker hours, so a client is worth its recurring shift volume, not a one-off fee. $5,000 per deal is about what a small client spends in a few months. A plant that uses GigWorx for its weekly swings is worth much more. That makes 51–1,000 employee sites with regular demand swings the most valuable targets, even though the form ticked every size.

**How they position themselves [form, brief].** Three things set them apart:
- Workers are **W-2 employees, not 1099 gig contractors**, so there is no misclassification risk for the client.
- **Technology**: post shifts in minutes, see who has clocked in, keep a favourites list.
- **Local ownership**: a local team, not a national agency.

The value proposition Matt wrote on the form: "Quality workers and technology to manage a contingent workforce without the hassle."

---

## 3. What the onboarding form says, answer by answer

| Form question | Matt's answer | What it means for the campaign |
|---|---|---|
| Sales Navigator? | No | The lead list can't come from a Sales Nav scrape. Use Clay or Blitz people search filtered on person location. The config is already a Clay people search. |
| Extra LinkedIn profiles | 0 | One sending seat (Matt), which caps volume. Whether VA seats are acceptable wasn't asked (see §9). |
| Industries | Retail, Manufacturing, Other | "Other" is undefined. The config reads it as warehousing. Construction and hospitality, both GigWorx verticals, are left out for now. |
| Company size | Every band, from self-employed to 10,000+ | The config starts at 11 employees. Self-employed and 2–10 are dropped. That's sensible for staffing but **wasn't confirmed with Matt**. |
| Geography | St. Joseph County, Elkhart County | Hyper-local, so location is filtered at person level. |
| Min. revenue | "Other" (not stated) | No revenue floor. Don't add one: revenue data for local private firms is mostly missing. |
| Seniority | All seven boxes | Broad. Owners decide at small firms; ops or HR decide at large ones. |
| Titles | President, Operations Manager, Production Manager, HR Business Partner, HR Manager, Production Supervisor | The config adds Owner, General Manager, Plant Manager and Warehouse Manager. These are good additions and fit the decision makers. |
| Titles to avoid | (blank) | No exclusions given. |
| Buying signals | "Hiring, Seasonal businesses, Large manufacturing, businesses with short lead time" | Active hourly hiring can be measured (see §5). The others are judgement calls. |
| Goal | Book a call / meeting | |
| Pain points | "Turnover, demand changes, hiring and recruiting" | Three angles for messaging (see §7). |
| Offer | "I will comp their first shift with GigWorx" | A strong, low-risk trial offer. It doubles as proof in a market where GigWorx has no local references. |
| Long-form email | "a powerful tool for businesses in the Michiana area… pay only for staff that work… local ownership… compare notes?" | Sets the tone: plain, local, owner to owner. "Compare notes" is his call to action. |
| Pricing | "Say it depends and book a call" | Never quote rates. Safe to say: no subscription, no minimums, billed for hours worked. |
| Top 3 FAQs | Subscription fee? Hire a worker? Bad worker? | Ready-made objection handling, already in the caller FAQs and Message 2. |
| Never say | "Not that I can think of" | No hard limits. The campaign notes add one: keep the $1,500 fee out of cold outreach. |
| Anything else | "Happy to jump on a call when you're ready before launch" | **He expects a call before launch.** Book it before anything goes live. |
| Referrals | (blank) | — |
| Booking link | HubSpot (`meetings.hubspot.com/mathew-welsch`) | He uses HubSpot, so a suppression list of existing customers could be exported from it. |
| Hours | EDT 08:30–18:00 | South Bend and Elkhart are on Eastern time, the same as the prospects. |

---

## 4. ICP as configured in `tracking_clients`

- **ICP:** Michiana shift employers (`e91ece83-…`). Market: Manufacturing, Warehousing & Logistics, Retail.
- **Geography:** Saint Joseph County, IN and Elkhart County, IN.
- **Sizes:** 11-50 through 10000+.
- **Persona:** President, Owner, General Manager, Plant Manager, Operations Manager, Production Manager, Production Supervisor, Warehouse Manager, HR Manager, HR Business Partner. All seniority levels from entry-level manager to CXO.
- **Qualifier:** a physical site in the two counties; staffs hourly shift roles (including RV and RV-supplier plants); excludes staffing agencies and the self-employed.
- **Lead list:** `184a0f39-…`, Custom module, **draft, 0 companies, 0 leads**, no Clay table yet.
- **Campaign:** "GigWorx - Michiana ops & HR - first shift comped". LinkedIn, client identity, in **creation** (step 18), not approved, no HeyReach campaign.

---

## 5. Market sizing [data]

Blitz `/v2/search/companies` returns **4,378 companies with 11+ employees headquartered in the 17 Michiana towns**, plus **9,183 with 1–10 employees** (counted, not pulled). By ICP bucket:

| Bucket | 11-50 | 51-200 | 201-500 | 501-1000 | 1001-5000 | 5001+ | **Total** | **51+** |
|---|---|---|---|---|---|---|---|---|
| Manufacturing | 382 | 165 | 43 | 17 | 16 | 5 | **628** | **246** |
| Warehousing & logistics | 129 | 45 | 10 | 7 | 4 | 1 | **196** | **67** |
| Retail | 212 | 11 | 2 | 0 | 3 | 0 | **228** | **16** |
| **Core ICP (configured)** | 723 | 221 | 55 | 24 | 23 | 6 | **1,052** | **329** |
| Construction | 154 | 28 | 4 | 1 | 2 | 2 | 191 | 37 |
| Hospitality, events & facilities | 298 | 45 | 9 | 1 | 3 | 1 | 357 | 59 |
| Unknown industry | 617 | 81 | 10 | 1 | 2 | 2 | 713 | 96 |
| Staffing (competitors) | 5 | 5 | 2 | 0 | 2 | 0 | 14 | 9 |
| Out of ICP (health, education, finance, etc.) | 1,614 | 276 | 94 | 26 | 27 | 14 | 2,051 | 437 |

**How to read the table:**
- **The core ICP is about 1,050 companies, 330 of them with 51+ staff.** The brief's estimate of 300–800 matches the 51+ number, not the full ICP.
- **This undercounts.** Plants run by out-of-area companies aren't here because the search is by headquarters. About 15% of the 713 unknown-industry companies are probably also in the ICP [view]. The real core is probably **1,200–1,500 sites** [view].
- **Retail is mostly small shops.** Only 16 retailers headquartered locally have 51+ staff. Big-box stores (Lowe's, Meijer, Menards, ALDI) are run from elsewhere, and their store managers rarely choose staffing vendors [view]. Retail should be the third priority.
- **Manufacturing is the core, and RV is its centre.** The largest local manufacturers are Lippert, Forest River, Thor, Jayco, Heartland, Grand Design, Newmar, Dexter, Utilimaster, Steel Warehouse, AM General and Conn Selmer. Below them sit hundreds of RV-supplier shops: plastics (Elkhart Plastics, Thunderbird Molding, Alpha Systems), composites, aluminium (Postle), furniture and trailers.
- **The industry tags are noisy.** Car dealerships (the Gurley Leep group) are tagged as manufacturing, and a supermarket chain is tagged as personal-care manufacturing. The list needs a company check before people are pulled.

**Active hourly hiring (the form's main buying signal).** Blitz `/v2/company/tam-by-jobs` found **140 companies with 462 hourly or production postings in South Bend, Mishawaka, Elkhart, Goshen and Nappanee in the last 60 days.**
- **By bucket:** 55 manufacturing, 27 warehousing and logistics, 6 retail, 6 construction.
- **Top posters:** Lippert (69 postings), SpartanNash (19), Lowe's (16), Vestis (15), Valmont (10), TD SYNNEX (8), Smurfit Westrock (7), UPS (7), Hubbell (7), DSV (7), JBS (6), MORryde (5) and Conn Selmer (5).
- **Only 32 of the 140 are headquartered in Indiana.** This is the strongest reason to source by person location.
- **Coverage is partial.** Hourly jobs live on Indeed and walk-in boards. Use this list as a **Tier 1 priority tag**, not as the universe.

---

## 6. Competitive landscape

**Local agencies headquartered in the area [data]:**
- Peoplelink Group / Peoplelink Staffing Solutions (South Bend, 201–500)
- Express Employment Professionals, North Central & North Eastern Indiana (Elkhart, 1,001–5,000)
- Alliance Staffing Work Solutions (Granger, 1,001–5,000)
- Jobsquad Indiana (Elkhart)
- Agile Staffing & Professional Services (South Bend)
- TalentSource (Mishawaka)
- Specialized Staffing Solutions (South Bend)
- Zing Recruiting (South Bend)

**National agencies posting local hourly jobs [data]:** Kelly, PrideNow, Employbridge, CyberCoders, STS Technical Services.

**Gig-style platforms [view, not verified this session]:** national on-demand apps such as Instawork, Veryable (aimed at manufacturing), Wonolo and Qwick may be active in the South Bend area. Check with Matt which ones he loses to.

**Where GigWorx wins against them [form, brief]:**
- Against **agencies**: no contract or minimums, pay only for hours worked, self-service in the app, a cheap and easy temp-to-hire fee, and the client never has to fire a bad worker personally.
- Against **1099 gig apps**: W-2 employees, with insurance and compliance handled.
- Against **both**: local ownership.

**Risk [view]:** the big RV makers and the national employers probably already have master agreements with Express, Peoplelink or Alliance. At those firms, GigWorx is a **backup for overflow**, not a replacement. The message should be "for the swings your agency doesn't cover", not "switch from your agency". The caller FAQ already says this well ("Most of our clients use it for the swings").

---

## 7. Pain points and angles

| Pain point (form) | What it looks like on the floor | Angle | Proof / offer |
|---|---|---|---|
| **Turnover** | Production and warehouse roles churn constantly, with no-shows and call-offs every shift | "Short on the floor because of call-offs? Post the shift, a vetted worker claims it." | 95% fill rate [brief]; first shift comped |
| **Demand changes** | Order spikes, RV model-year ramps, seasonal peaks, a contract won at short notice | "Cover the swing without hiring full-time you'll have to let go." | No minimums, no contract |
| **Hiring and recruiting** | Ops managers and HR spend hours sourcing and screening hourly staff | "Try someone on a shift, then hire them if they're good." | Temp-to-hire with no minimum hours (fee only on request) |
| Agency frustration [brief] | Slow fills, hit-or-miss quality, locked into contracts | "Not another agency." | Self-service app, pay per hour worked |

**Timing [view, background knowledge, not verified]:**
- RV production follows the model year. Plants ramp ahead of spring dealer stocking and around the late-summer model-year changeover. Elkhart's RV Open House is in late September.
- Warehouses and retail peak in November and December, which is now.
- An RV-focused message about seasonal ramps fits best in Q1. A message about holiday peaks and call-offs fits warehouses and retail right now.

---

## 8. Messaging review (current sequence in `tracking_clients`)

The sequence is 4 steps: a connection request, then messages after +1, +4 and +7 days. It is in the campaign plan doc and the campaign's `linkedInSequence`.

**What works:**
- It sounds like Matt: plain words, short sentences, local ("I run GigWorx here in Michiana").
- Message 1 opens with a question about how they cover shortfalls today ("Agency, overtime, or just running short?"). It's specific to the reader's floor and easy to answer.
- Matt's three FAQs are used as objection handling in Message 2.
- The offer appears in Messages 1 and 3. Replying "shift" in Message 3 is an easy way in.
- It follows the pricing rule (no number) and the campaign rule (no $1,500 figure).

**Gaps and suggestions [view]:**
1. **No local proof.** Once Matt confirms names, add one line like "we already staff [local company]". Until then, the comped shift does that job. Don't use Montana client names as if they were local.
2. **One message for every persona.** A Production Supervisor feels call-offs, while an HR Manager feels time spent recruiting. Consider an HR version of Message 1 ("try a worker on a shift before you hire them") and keep the current one for operations.
3. **One message for every vertical.** Plants, warehouses and retail have different swings. "Plants, warehouses and stores" in the connection request covers all three, but Message 1 says "short on the floor", which reads as manufacturing. Fine for now; split it if retail volume grows.
4. **The connection request is 177 characters with a 4-letter first name** (measured), well under HeyReach's 300-character limit.
5. **Matt's call to action, "compare notes", isn't used.** Consider it in Message 2 instead of "walk you through it".
6. **The booking link is in Message 2 only.** Fine for LinkedIn, but the reply AI should also send it whenever a reply sounds interested.

---

## 9. Gaps to close with Matt (pre-launch call, which he asked for)

**Blocking: needed before launch**
1. **Suppression list.** Existing Michiana clients, and any past or lost deals, from HubSpot. The DNC list is currently empty (`dncCount: 0`).
2. **Local proof.** Any South Bend or Elkhart clients we can name or describe?
3. **Approval of the copy and the ICP scope** (11+ employees; manufacturing, warehousing and retail).
4. **Reply handling.** Should all replies be forwarded, or only interested ones? Who handles "send me info"?

**Important: shapes scale**
5. **Industries under "Other".** Can we add construction (191 companies) and hospitality/events (357) as a second campaign? Both are GigWorx verticals.
6. **Company size.** Does he really want 2–10 employee firms (thousands of them, with low shift volume)? The config currently excludes them.
7. **VA seats or referral campaigns** on Algo accounts, to add volume beyond one seat. Not discussed on the form.
8. **Capacity.** How many shifts and workers can GigWorx fill each week in Michiana today? Ten new plant clients would need workers the same week.

**Useful but not blocking**
9. Matt's LinkedIn connection count and profile state, to see whether the profile needs work before sending.
10. Who he loses to most (a named agency or a gig app).
11. Any industries or companies to avoid (unions, etc.).

---

## 10. Recommendations

1. **Source by person location, not company headquarters.** Run the Clay people search (or Blitz Find People) with person location set to St. Joseph and Elkhart County. Use the config's titles and industries. Then check each company against the industry buckets in `2026-11-05-companies.csv`, and remove staffing firms and dealerships.
2. **Contacts per company, inverse to market size (CLAUDE.md rule).** The market is small and finite, so go deeper per company:
   - **51+ employees: 3–4 contacts.** Plant or ops manager, production supervisor, HR manager, and GM or president.
   - **11–50 employees: 1–2 contacts.** Owner or president, plus the ops manager.
   - That totals roughly **330×3.5 + 720×1.5 ≈ 2,200 contacts** for the configured core.
3. **Order the list by priority.**
   - **Tier 1:** the 140 active hirers (in the hiring-signal file), plus 51–1,000 employee manufacturers and warehouses.
   - **Tier 2:** other 51+ employee companies in the ICP.
   - **Tier 3:** 11–50 employee companies and retail.
   - One seat goes through a tier in weeks, so the order is what decides who hears from us before year end.
4. **Book Matt's pre-launch call now,** using the §9 list as the agenda. Get the suppression list and any local proof before the first send.
5. **Plan a second segment** (construction plus hospitality and events) once he confirms "Other". It is about 550 more companies, with the same offer and different pain points (project surges, event days).
6. **Treat the RV majors as overflow targets.** Lippert, Forest River, Thor, Jayco and Grand Design probably have agency contracts already. Pitch them on covering the swings at plant level, not on switching.

---

## Files

- `sourcing/michiana-shift-employers/2026-11-05-companies.csv`: 4,378 companies (Blitz), with an `icp_bucket` tag
- `sourcing/michiana-shift-employers/2026-11-05-hiring-signal-companies.csv`: 140 hourly-hiring companies (Blitz TAM by jobs)
- `sourcing/michiana-shift-employers/2026-11-05-companies.query.md`: exact queries, bucket rules and limitations
