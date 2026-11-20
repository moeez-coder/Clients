<!--
Internal discussion draft for Moe. NOT in tracking_clients, NOT sent to the client, NOT a config.
Written 2026-11-16 for Moe's question: "For Health Link, what could be an MQL (marketing
qualified lead) campaign? Something that will increase the reply ratio."
Nothing here gets built (campaign doc edit, config, lead pull, client message) until Moe
picks an idea and says go.

Sources used for every claim:
- ICP form (context/icp-form.md, submitted 2026-11-04): segments, personas, pain points,
  stats (3.8M+ emails, 98% MD/DO/NP/PA coverage, 20M+ annual deployments, 95% retention,
  NPS 79), the client's own sample LinkedIn message and long email.
- Client description (context/client-description.md): Profile / Enrich / Engage / Pulse,
  1.2M+ MDs and DOs, 600K+ NPs and PAs, 3.4M+ validated emails, 95%+ coverage.
- healthlinkdimensions.com claims as read on 2026-11-13 (see
  campaign-docs/2026-11-13-doc-1-offers-section.md header): Assertio 24.9% vs 18.58% open rate.
- Client comments on doc 1 (tracking_clients doc 1f2e4277-1a09-445e-8684-75cc542ab003,
  comments 1, 2, 3, 4, 6, 12), read 2026-11-16.
-->

# HealthLink Dimensions: MQL campaign ideas (for discussion)

## What we are solving for

The client's feedback on doc 1, in their words:

- Comment 1, on the free data review: "We have done this in the past. Not sure how successful it's been."
- Comment 2: "It feels like we are selling a lot in the message, and asking for something from the client."
- Comments 4, 6 and 12: lead with client-ready HCP audience strategy for agencies, not "you have a bad file".

**An MQL campaign answers comment 2 directly.** Message 1 asks for one word or one choice, not a meeting and not the prospect's data. The meeting ask moves to the nurture step, after they have replied.

**Pushback worth keeping.** The client said the data review's results were unclear ("not sure how successful"), not that it failed. Their concern is the friction: the prospect has to hand over a file. None of the ideas below asks the prospect for data, so we drop that friction without throwing out the whole "show them the gap" idea. Their own sample LinkedIn message is already an MQL-style question ("How is your team thinking about audience reach across channels right now"). Idea 1 builds on it.

**MQL definition used throughout:** a reply that says yes to an asset, answers the question, or names a specialty or therapy area. Out-of-office, "not interested" and "remove me" do not count. HeyReach tag: `MQL`.

---

## Idea 1: The one-question reach poll (no asset, can launch first)

- **Segments:** all five. Variant wording per segment through `{segment_label}`.
- **Hook:** a single multiple-choice question about how their HCP audience holds up across channels. This is lifted from the client's own sample message and long email ("the same prescriber shows up one way in the CRM, another in the email file, and another in the media plan").
- **What HLD needs to produce:** nothing to launch. After about 50 answers, a short write-up of the results ("what we heard from X commercial teams") to send back to everyone who answered. We can draft it; HLD approves.
- **Why it lifts replies:** A/B/C takes about five seconds to answer. There is no pitch and no ask for data, and the promise of seeing peers' answers is a reason to reply.
- **Connection request:**
  > Hi {first_name}, I talk with a lot of {segment_label} teams about how their HCP audiences hold up across channels. Would be good to connect.
- **Message 1:**
  > Thanks for connecting, {first_name}. Quick one, no pitch. When your team plans an HCP campaign, which is closest?
  > A) one HCP list feeds CRM, email and media
  > B) each channel works from its own list
  > C) honestly not sure
  > I'm collecting answers from {segment_label} teams and will share what comes back with everyone who replies.
- **MQL:** any A, B or C answer.
- **Handoff to discovery:**
  - B or C: "That's the most common answer so far. HLD runs every channel off one verified HCP view. Worth 20 minutes to see how other teams set that up?"
  - A: send the results write-up when it is ready, then ask how they keep that list current month to month.
- **HLD must approve:** sending the results write-up under their name.

## Idea 2: Your specialty, counted (pharma, biotech, med device)

- **Segments:** specialty pharma and commercial biotech (1), pre-launch biotech (2), med device (3).
- **Hook:** one number the prospect cannot easily get: the current count of verified U.S. prescribers in their specialty, including NPs and PAs, and how it splits by state. It needs nothing from them, unlike the data review.
- **What HLD needs to produce:** counts from Profile for about 15 to 20 specialties that map to our target accounts. Examples: neurology and psychiatry (Neurocrine, Axsome, Supernus), hepatology (Madrigal), pulmonology (Insmed), endocrinology (Corcept), ophthalmology (Glaukos), interventional cardiology and neurology (Penumbra), electrophysiology (iRhythm). One small template, refreshed monthly.
- **Why it lifts replies:** the answer is "yes". The number is specific to their brand's world, and it shows the monthly verification claim working instead of stating it.
- **Connection request:**
  > Hi {first_name}, saw {company} is focused on {therapy_area}. We track the U.S. {specialty} audience closely. Would be good to connect.
- **Message 1:**
  > Thanks for connecting, {first_name}. We keep a monthly-verified count of U.S. {specialty} prescribers, NPs and PAs included. Want me to send you the current number and how it splits by state? A "yes" is all I need.
  - **Med device variant:** "{specialty} surgeons and specialists" instead of "prescribers". This also answers comment 3. Device lists should include Marketing Ops, CRM and Sales Ops titles, not only HCP-marketing roles, since the count is useful to all of them.
- **MQL:** "yes", or the prospect names a different specialty.
- **Handoff to discovery:** send the count, then: "How close is that to the number in your CRM today?" A gap answer leads to Enrich, and the meeting ask comes in that reply.
- **HLD must approve:** sharing specialty counts externally, the specialty list, and turnaround (same day matches their "same-day response" claim).
- **Note:** this sits close to the "snapshot of your HCP audience" freebie already in doc 1's potential offers. It is the lightest version of it: one number, no file exchange.

## Idea 3: First-launch HCP data checklist (pre-launch and newly launched biotech)

- **Segments:** pre-launch biotech (2). Triggers: FDA approval, PDUFA date, funding (doc 1 campaigns 6 and 7).
- **Hook:** a one-page checklist of what the HCP data foundation needs before launch day. The ICP form says these teams are "building their HCP data foundation from scratch".
- **What HLD needs to produce:** the one-pager. We can draft it from HLD's own pain points (stale records, cross-channel reach, measurement) and the four pillars. HLD edits and brands it.
- **Why it lifts replies:** first-time commercial leaders are short on templates. A checklist is useful whether or not they buy, and the reply is "send it".
- **Connection request:**
  > Hi {first_name}, congrats on {launch_event}. Would be good to connect with someone building the commercial side of a launch.
- **Message 1:**
  > Thanks for connecting, {first_name}. First launches usually mean building the HCP data side from scratch. We put together a one-page checklist of what that foundation needs before launch day: specialty targeting, NPI-level records, channel reach and how you will measure it. Want a copy?
- **MQL:** a request for the checklist.
- **Handoff to discovery:** two days after sending it: "Which of those is still open for your team?" Any named gap gets a 20-minute call with HLD's launch team.
- **HLD must approve:** the checklist content and its branding.

## Idea 4: A client-ready HCP audience idea, on request (agencies)

- **Segments:** HCP agencies (5). Signals: open roles, account wins, new leaders (doc 1 campaigns 5 and 10, plus the separate new-leader sequence promised on comment 12).
- **Hook:** this is the client's own positioning made concrete. Their agency copy offers to "share a few approaches", which is still a soft meeting ask. Here the prospect names a therapy area, and HLD sends back a one-page HCP audience idea for it (who to reach, how many, which channels) that the agency can take to its client.
- **What HLD needs to produce:** a one-page template plus a fast turnaround per request. This is the costliest idea per MQL, so keep it to qualified agencies only.
- **Why it lifts replies:** the reply is two words ("oncology", "dermatology"), and what they get back helps them win or keep a client. That is exactly the "client-ready" framing the client asked for.
- **Connection request:** the client's approved copy, unchanged:
  > Hi {first_name}, noticed {company} is hiring for {open_role}. We work with healthcare agencies on HCP audience strategy and activation. Thought it would be good to connect.
- **Message 1:**
  > Thanks for connecting, {first_name}. Which therapy area is your team planning or pitching in next? Tell me and we'll put together a one-page HCP audience idea for it, covering who to reach, how many and on which channels, that your team can take to the client. No call needed.
- **New-leader variant** (comment 12, no account-win assumption): open with "congrats on the new role" and ask "what's the first client plan on your desk?"
- **MQL:** names a therapy area or client brief.
- **Handoff to discovery:** deliver the one-pager, then: "Want to walk your planner through how we would activate it?" That call is the discovery call.
- **HLD must approve:** the template, turnaround time, and who on their side builds each one-pager.

## Idea 5: HCP email engagement benchmarks (brand teams and agencies)

- **Segments:** large pharma brand and omnichannel teams (4), specialty pharma (1), agencies (5).
- **Hook:** benchmarks drawn from HLD's 20M+ HCP email deployments a year, plus the website's Assertio result: a 24.9% open rate against an 18.58% pharma average.
- **What HLD needs to produce:** a short benchmark sheet of open and click ranges by specialty, in aggregate, from their deployment data.
- **Why it lifts replies:** brand managers get judged on engagement, and a benchmark tells them whether their last send was good. The reply is "send it", and it ties straight into Pulse (measurement), one of the client's three pain points.
- **Connection request:**
  > Hi {first_name}, I work with pharma brand teams on HCP email engagement. Would be good to connect.
- **Message 1:**
  > Thanks for connecting, {first_name}. HealthLink sends 20M+ HCP emails a year, so we see where engagement really lands by specialty. One campaign for Assertio hit a 24.9% open rate against an 18.58% pharma average. Want the benchmarks for {specialty} so you can see how your recent sends compare?
- **MQL:** a request for the benchmarks.
- **Handoff to discovery:** "How did your last {specialty} send compare?" Below benchmark leads to a call on Engage and Pulse.
- **HLD must approve:** naming Assertio and its result in outreach (Assertio is a client), and publishing aggregate benchmarks.

---

## Recommendation for the discussion

1. **Launch Idea 1 first, across all five segments.** It needs no asset, so it can go live as soon as doc 1 is approved, and it gives us a reply-rate baseline against doc 1's copy.
2. **Pair it with one asset idea per audience:**
   - Idea 4 for agencies, since it is the client's own positioning turned into an offer.
   - Idea 2 for pharma, biotech and device, since it is the cheapest asset for HLD to produce.
3. **Hold Ideas 3 and 5** until HLD confirms they can produce the checklist and the benchmarks.

## Flags for HLD before anything ships

- **Stat conflict.** The ICP form says 3.8M+ emails and 98% coverage; the website says 3.4M+ and 95%+. None of the copy above uses either figure, but HLD should confirm which one is current before any copy does.
- **Approvals.** Every asset, the Assertio name and the turnaround times need HLD sign-off.
- **Booking link and reply owner** are still empty in tracking_clients. The handoff steps depend on both.
- **DNC and client exclusion lists** are still empty (0 entries).
