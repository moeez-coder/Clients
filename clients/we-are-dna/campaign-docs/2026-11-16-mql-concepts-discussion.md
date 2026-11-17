<!-- Internal discussion note, We Are DNA (tracking_clients f5ff426b-c514-4a64-91b0-0e141a6a0669). Written 2026-11-16 at Moe's request: "what could an MQL campaign look like for We Are DNA? The goal is to raise the reply ratio." Discussion only: nothing here exists in tracking_clients, HeyReach or GTM Sheets, nothing was sent to the client, and no paid sourcing was run. Grounded in context/icp-form.md, campaign-docs/2026-11-12-doc-1.md (doc fed8e905-ea1c-4a91-ade7-0da0f7f732a6), John Tarrant's 2026-11-12 feedback (sourcing/tam/2026-11-13-signal-read.query.md) and sourcing/tam/2026-11-13-gpg-signal-companies.csv. Sector benchmarks below were computed locally from that CSV on 2026-11-16 (£0). -->

# We Are DNA: MQL campaign concepts (discussion draft, 2026-11-16)

## The problem this solves

Every doc 1 campaign and campaign 6 asks for something on the first touch: a free AI visibility audit, which means a call or at least a handover of time. For C-suite buyers who "get bombarded by recruitment agencies and despise them" (John, 2026-11-12), that is a bigger ask than it looks. An MQL campaign asks only for a reply ("yes, send it"), gives something first, and converts to a sales-qualified lead on the second step.

**Definitions used below**
- **MQL (hand-raise):** a reply that accepts the asset or answers the question.
- **SQL:** the MQL then books a discovery call through DNA's booking link, or confirms an EVP, employer brand or careers site project in the next 12 months.

## Constraints carried over from the record

- No open roles, vacancies or candidate language (John, 2026-11-12).
- Buyers: CEO/MD, CPO/People Director/HRD, COO/CFO. Not TA managers.
- UK English, no em dashes. Connection notes under 200 characters.
- HeyReach caveat from campaign 6: `gtm_sheet_create_heyreach_campaign` can't set a note fallback, so a note with `{first_name}`/`{company}` has to be fixed in the HeyReach UI.
- DNC: 143 companies now in tracking_clients (`context/dnc-list.csv`). It includes Pets at Home, Medivet, Dunbia, Aesop and OVO. 10 match the GPG list by exact name.
- John has not yet said whether campaigns may quote a company's own pay gap figure (doc 1 "Before launch").
- One campaign per company per month. Campaign 6 companies are off limits to any MQL test.

## Sector benchmarks already in the repo (GPG 2025, 3,796 employers)

| Sector | Employers | Median of median gaps | 75th percentile | Women in top pay quartile (median) |
|---|---|---|---|---|
| Health, care, vet | 1,107 | 0.8% | 7.0% | 72.4% |
| Retail, hospitality | 1,035 | 1.1% | 5.4% | 46.8% |
| Manufacturing, engineering | 1,144 | 6.0% | 13.0% | 20.0% |
| Law, accounting | 66 | 18.4% | 26.6% | 53.0% |
| Financial services | 537 | 19.6% | 28.7% | 31.1% |

## Concept A: "Where you sit" pay gap benchmark (recommended first test)

- **Hook / asset:** a one-page benchmark that puts the company next to every UK employer in its sector that reported in 2025. It covers median gap, rank and women in the top pay quartile. The page is generated from the CSV by a script, so it's free and can go out within the hour.
- **List:** `2026-11-13-gpg-signal-companies.csv`, manufacturing and financial services first (1,681 employers), minus DNC and campaign 6.
  - Campaigns 3 and 5 only use companies at 15% or more, so the MQL test can take the **other 1,106** with zero overlap.
  - Everyone wants to know their rank, not only the outliers.
- **Persona:** People Director/CPO/HRD (they sign the GPG report), then CEO/MD. 2 per company.
- **Connection note:** Hi {first_name}, I've been comparing the 2025 gender pay gap reports across UK financial services firms. Would be good to connect.
- **Message 1:**
  > Thanks for connecting, {first_name}.
  >
  > We lined up all 537 UK financial services employers that reported in 2025. The sector median gap is 19.6%, and women hold 31% of top quartile roles.
  >
  > I've put {company} on the same page so you can see where you sit. It's one page. Want me to send it over?
- **Why it lifts replies:**
  - Real numbers in the first message.
  - A rank people are curious about.
  - A one-word answer is enough.
  - It's on HR's desk every April.
  - It doesn't quote the company's own figure until they ask, so it sidesteps John's open question.
- **Reply to SQL:**
  - Send the page.
  - Follow up: "Most of the gap usually comes from who applies and who stays in senior roles, not pay. Would 20 minutes on how {company} comes across to the people you're not reaching yet help before the April 2027 report?"
  - The AI visibility audit becomes the second step, not the first.

## Concept B: One line from the AI

- **Hook / asset:** we ask ChatGPT what it is like to work at {company}, quote one real line in message 1, and offer the full answer plus a comparison with one competitor for talent. This is doc 1's offer, but the first piece is given before anything is asked.
- **List:** retail/hospitality and health/care employers from the GPG list (recognisable consumer-facing brands get the richest AI answers), minus DNC and campaign 6.
- **Persona:** CPO/People Director, then CEO.
- **Connection note:** Hi {first_name}, I've been looking at what AI tools tell job seekers about UK employers. {company} came up. Happy to share what I found.
- **Message 1:**
  > Thanks for connecting, {first_name}.
  >
  > I asked ChatGPT what it's like to work at {company}. One line stood out: "{ai_line}"
  >
  > Candidates are asking it the same question before they apply. I've got the full answer and how it compares with {competitor}. Want me to send it over?
- **Why it lifts replies:** it's specific to them and new, and people can't resist reading what's said about them.
- **Reply to SQL:**
  - Send the snapshot.
  - Ask: "Does that match the story you'd want told?"
  - A "no" is the discovery call.
- **Risks:**
  - AI answers can be wrong or unflattering. Every line needs a human check.
  - Frame it as "what it says", never as fact.
  - It costs a small LLM spend per company.

## Concept C: "Worth sending over?" sector case study

- **Hook / asset:** a two-minute case study matched to the sector:
  - DHU Healthcare, £2m in 20 months (health)
  - Glendola, unwanted turnover cut by over half (hospitality)
  - MAN Truck & Bus UK, £1m a year (manufacturing)
  - Superdry, boohoo and Pets at Home, £500k to £600k a year (retail)
- **List:** any sector pool. This is the lowest-effort concept.
- **Persona:** CEO/MD, because the figures are money.
- **Connection note:** Hi {first_name}, we work with hospitality groups on keeping their people. Thought it was worth connecting.
- **Message 1:**
  > Thanks for connecting, {first_name}.
  >
  > Glendola, a national hospitality group, cut unwanted staff turnover by more than half with us. We wrote up what they changed, most of it in the first 90 days after someone joins.
  >
  > It's a two-minute read. Worth sending over?
- **Why it lifts replies:** it gives peer proof with a number and asks for nothing but a yes.
- **Reply to SQL:** send it, then ask: "Would a version of that for {company} be useful?"
- **Dependency:** DNA has to supply or approve the write-ups. The ICP form says they have "brilliant best practice case studies we are happy to share". Pets at Home is on the DNC list, so it can be cited but not contacted.

## Concept D: Three-question peer pulse

- **Hook / asset:** "We're asking 50 {sector} leaders three questions about attraction and retention for 2027, and sharing the results with everyone who answers."
- **The questions:**
  1. Your biggest people cost for 2027.
  2. Is turnover up or down.
  3. Has your employer story kept up with the business.
- **List:** any sector pool. Best in law and accounting (66 GPG employers, a tight peer group) and the Top 100 list.
- **Persona:** CEO/Managing Partner, then People Director.
- **Connection note:** Hi {first_name}, I'm gathering views from UK law firm leaders on keeping people in 2027. Would be good to connect.
- **Message 1:**
  > Thanks for connecting, {first_name}.
  >
  > We're asking leaders at the Top 100 firms three quick questions about attraction and retention for 2027, and sharing the results with everyone who answers.
  >
  > Can I send them over? You can answer right here.
- **Why it lifts replies:** people like to be asked their view, the answers come back in the chat, and those answers qualify the lead.
- **Reply to SQL:**
  - Send the results, with a line on where their answers sit.
  - Ask: "worth 20 minutes?"
  - DNA also gets a content asset.
- **Risk:** DNA has to actually publish the results. It's the slowest to fulfil.

## Concept E: Reputation snippet (parked)

- **Hook:** the company's Indeed or Glassdoor rating against the sector, and the most common theme in reviews.
- **Why parked:**
  - It needs scraping (Apify through GTM Sheets, which is paid and not yet costed).
  - Review-site terms need checking.
  - A negative number sent cold to a CEO reads as an attack. That is the tone John objected to.
- **Better use:** as a section inside concept B's asset, not as a cold hook.

## Recommendation

**Test concept A first.**
- The data is already in the repo and cost £0.
- The asset can be generated by a script, so a hand-raise is fulfilled within the hour, with no DNA team time.
- It uses the 1,106 GPG employers that no doc 1 campaign touches.
- It doesn't depend on John's pay gap figure decision.

Concept B is the second test. It is the upgrade of doc 1's own offer.

## How to measure it against campaign 6 and doc 1

- **Baseline:** none of the comparison campaigns are live yet. Campaign 6 waits for Moe's approval, and doc 1 is in `client_review`.
- **Best design:** a controlled split, rather than a comparison across time.
  - Take one GPG pool (financial services plus manufacturing below 15%) and randomise companies into two arms.
  - **Arm 1:** doc 1 style, with the audit ask in message 1.
  - **Arm 2:** concept A.
  - Use the same senders split evenly, the same week and the same personas.
  - Campaign 6 runs alongside as a reference, not a control, because its signal and pool differ.
- **Metrics** (HeyReach plus tracking_clients reply tags):
  1. Acceptance rate.
  2. Reply rate on accepted connections (the headline).
  3. Positive reply rate.
  4. Hand-raise rate.
  5. SQL rate within 30 days of the first reply.
  6. **Meetings per 100 connection requests.** This is the guard against an MQL that only inflates replies.
- **Sample:**
  - About 250 accepted connections per arm detects a reply rate moving from about 10% to 18% (80% power).
  - At about 35 to 40% acceptance, that is roughly 650 to 700 requests per arm.
  - Campaign 6's 439 leads will be directional only.
- **Decision rule:** concept A wins if its reply rate is at least 1.5 times arm 1's and meetings per 100 requests are no lower after 30 days.

## Cost before anything is run (needs Moe's go-ahead)

- **GPG data and benchmark pages:** £0.
- **Leads:**
  - About 350 companies at 2 contacts is about 700 leads.
  - Campaign 6 used 629 Blitz records for 491 leads, so this would be about 700 to 900 Blitz records.
  - The repo doesn't record a per-record price.
- **Concept B:** add an LLM call per company (a few dollars for 350) plus human review time.
- **Concept E:** Apify cost not quoted.

## Open decisions for Moe

1. Which concept to test first (A recommended).
2. Who fulfils the asset, in DNA's name: Algo, by script, or DNA's team?
3. Run the controlled split now, alongside campaign 6, or wait until John approves doc 1 so arm 1 can use doc 1 copy?
4. This is a new campaign, not in doc 1, so it should go to John as a doc addition before launch. Nothing has been sent.
