<!-- Internal draft for Moe, We Are DNA (tracking_clients f5ff426b-c514-4a64-91b0-0e141a6a0669). Written 2026-11-17 by session_013MzxQfnKsdVbThAsX3zi7V from Moe's brief of the same day (Glassdoor bad-review outreach). NOT in any campaign doc, NOT in tracking_clients or HeyReach, nothing sent. Grounded in context/icp-form.md (offers, case studies), John's 2026-11-12 tone feedback, and campaign-docs/2026-11-16-mql-concepts-discussion.md (Concept E risks). UK English, no em dashes. -->

# Glassdoor bad-review campaign: messaging draft v1 (for Moe)

## Rules this copy follows

- Talks about **themes and ratings only**: "reviews keep mentioning communication from leadership", "the rating has dipped this year". **Never quotes a review, never names or hints at a reviewer** (no job titles, locations or dates of single reviews).
- **Never shames.** No "bad", "poor", "negative", "low score". Frames it as what candidates and staff see, and as common in the sector.
- **Reply-first** (from the MQL note): message 1 gives something and asks for a one-word yes. Concept E's risk was "a negative number sent cold to a CEO reads as an attack", so the rating itself is never the headline, the theme is.
- Leads with DNA's EVP / engagement angle, uses the client's own case studies by sector.

## Offer each message leads with

**Offer 1, Employer reputation snapshot (free, one page):** what staff are saying about {company} by theme, how the score has moved over 12 months, and how that compares with sector peers, plus "what AI tools tell job seekers" (folds in DNA's own AI visibility audit). Built by script from the scraped data, so Algo can fulfil it the same day.

Offers 2 and 3 (for a doc's `## Offers for your feedback`, if this goes to John): **EVP / employer brand audit** and **careers site audit with a 90-day uplift**, both from the ICP form's own offer list. Offer 4: **competitor comparison** against two named employers for talent.

## Variables (filled per company from the scored data, reviewed by hand)

- `{first_name}`, `{company}`
- `{sector_peers}`: e.g. "UK care providers", "national retailers", "mid-sized law firms"
- `{theme}`: the most common complaint theme in the last 12 months, in neutral words. Allowed values (mapped from the theme scoring): "communication from leadership", "career progression", "how new starters are brought in", "workload and work-life balance", "recognition", "pay and benefits" (only used if nothing else qualifies; DNA doesn't fix pay)
- `{trend_line}`: only one of
  - "and the overall score has slipped over the last year" (decline flag)
  - "and it's a theme that comes up more often than at most {sector_peers}" (low-rating flag, no decline)
- `{proof}`: sector case study from the ICP form (Glendola for hospitality, DHU for health and care, MAN Truck & Bus UK for manufacturing, Superdry/boohoo for retail; law/finance: the MAN £1m figure framed generically). **Pets at Home, boohoo, Glendola, DHU, MAN and Medivet are all on the DNC list:** fine to cite (with DNA's permission), never to contact.

## Sequence (connection request, then 3 messages at +0 / +3 / +4 days)

**Connection note** (≤200 characters, no variables so HeyReach needs no fallback; the C6 issue):
> Hi, I've been looking at what staff and candidates are saying about employers across your sector this year. Some useful patterns. Would be good to connect.

**Message 1** (on acceptance; offer 1, reply-first):
> Thanks for connecting, {first_name}.
>
> I've been reading through what people say about working at {sector_peers} on Glassdoor. At {company}, the comments keep coming back to {theme}, {trend_line}.
>
> Candidates read the same pages before they apply. I've put it on one page, by theme and next to your peers. Want me to send it over?

**Message 2** (+3 days; proof, EVP angle):
> {proof}
>
> Most of it came from getting the story right inside the business first, so what people say on their way in matches what they find once they're there.
>
> Happy to send the one-pager either way. No pitch attached.

Example `{proof}` (hospitality): "Glendola, a national hospitality group, had a similar pattern in what their teams were saying. After we reworked their employer story with them, unwanted staff turnover fell by more than half."

**Message 3** (+4 days; soft close, offer 1 again plus AI angle):
> Last one from me, {first_name}. If {theme} is already on the list for 2027, the snapshot also shows what AI tools tell job seekers about {company}, which is where a lot of candidates now start.
>
> Shall I send it?

## Reply handling (to SQL)

- "Yes" → send the one-pager (themes, trend, peer comparison, AI answer). Follow up: "Does that match what you're hearing internally?" A "no, it's worse" or "we know" is the discovery call: offer 20 minutes with John via the booking link.
- "Who are you / is this a sales pitch" → one line on DNA (Bristol, EVP and employer brand, since 2010) and re-offer the one-pager.
- "How did you get this" → "It's all public on Glassdoor; we just group it by theme." Never send review text or reviewer details, even if asked.

## Open points for Moe

1. Is "Glassdoor" named in message 1, or kept as "what people say online"? Naming it is more concrete; not naming it is softer. Draft names it.
2. Confirm the theme list (DNA can genuinely move communication, onboarding, career story, recognition; pay is excluded on purpose).
3. Who fulfils the one-pager in DNA's name: Algo by script (recommended), or DNA's team?
4. John hasn't approved review-based outreach. Concept E was parked partly on tone. Doc route vs your own approval is the open gate.
