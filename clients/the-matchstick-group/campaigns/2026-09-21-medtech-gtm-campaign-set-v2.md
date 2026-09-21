# Medtech GTM campaign set — v2 (7 campaigns)

**Client:** The Matchstick Group (`thematchstickgroup.com`, tracking_clients `45047afb-2d5a-4bfd-ac3d-caa290bdd568`)
**Received:** 2026-09-21, supplied verbatim by the repo owner in-session (no MCP/tool source — this is
client-strategy input, not sourced data).
**Status:** Campaign definitions only. Not yet created in `tracking_clients`, not yet built in HeyReach,
no sourcing configs exist for these segments yet (`list_sourcing_configs` returned 0 on 2026-09-21).
**Version note:** Labelled v2 by the author. Campaign 2 ("Before the Buyer Arrives") is explicitly new —
"Nothing in v1 addressed this buyer." No v1 document exists in this repo.

Each campaign below is one segment, and therefore one future `sourcing/<config-slug>/` folder per the
repo standard. Proposed config-slugs are given per campaign; they are proposals until the matching
sourcing config is created in `tracking_clients` and the slug confirmed.

---

## 1. NewCo Countdown — Sponsor Side

*Proposed config-slug:* `newco-countdown-sponsor-side`

**Segment** Private equity firms with a medtech portfolio. Screen for: a stated carve-out or corporate-divestiture strategy; a healthcare or industrials practice with medtech in it; deal sizes roughly $200M to $2B enterprise value; and either a current medtech separation in the portfolio or one recently announced.

**Persona** Operating Partner, Senior Operating Partner, Head of Portfolio Operations, Value Creation Director — healthcare practice. Not deal partners.

**Trigger** Close date five to twelve months out, regardless of how old the announcement is. Add the earlier signal: "intent to separate," "the board has authorized a separation," "strategic review." A separation announcement can precede a deal by twelve to eighteen months and it is public.

**Sources** 8-K filings, PE firm portfolio news pages, MedTech Dive, MassDevice, the Lawrence Evans weekly healthcare M&A digest.

**Angle** A separation gets a legal close date and a name. The commercial build starts after. The default is to announce the close with a name and nothing behind it, then spend the first two quarters of the new sales cycle working out the brand — while the sponsor's growth plan is already running against those quarters.

**Connection note**

> {first_name} — saw the {company} deal. We built the full commercial identity for a $1.5B medtech carve-out inside its separation window: seven sites in three countries, a dozen product brands down to two, naming through day-one launch in 93 business days. Would like to connect.

**Message 1**

> Saw the {company} separation, {first_name}.
>
> Most of these announce the close with a name and not much else, then spend the first two quarters of the new sales cycle working out the brand. Meanwhile the growth plan is already running against those quarters.
>
> We were brought into one about five months before close and did it inside the separation window instead — naming, brand architecture, complete with internal and external marketing assets and corporate signage in place on day-one across seven sites in three countries. 93 business days.
>
> Day one, the sales team had something to sell with.

**Message 2**

> Across your portfolio, when a business separates — how long before it is actually able to generate demand on its own?

**Message 3**

> Asking because we have seen that range from one quarter to four, and the difference is almost always whether anyone owned it before close. If it is useful, I can share what the 93-day version looked like — what had to happen before close, and what could wait.

**Notes**

- This list is small and the relationships are long. Do not run it for volume.
  *(Repo standard read: small TAM/SAM → more contacts per company, but low total volume. Record the
  actual per-company contact count in this segment's `.query.md` when it is first sourced.)*

---

## 2. Before the Buyer Arrives — Seller Side

*Proposed config-slug:* `before-the-buyer-arrives-seller-side`

New. Nothing in v1 addressed this buyer, and it is the channel with the longest runway and the least competition — every agency arrives after the newco exists.

**Segment** Medtech and diagnostics parents, $250M+ revenue, that have announced an intent to separate, a strategic review, or an active divestiture process. Also sponsors preparing to sell a portfolio company.

**Persona** Corporate Development lead, VP Corporate Communications, CEO, VP Sales & Marketing, VP Marketing. These people run the separation and they know about it twelve to eighteen months before the market does.

**Trigger** Specific language in an 8-K, investor day deck, or press release: "intent to separate," "the board has authorized," "strategic review," "exploring strategic alternatives," "divestiture process." Six to eighteen months ahead of expected close.

**Angle** The seller is measured on proceeds and on a clean separation. A business unit that goes to market with no standalone identity, no independent demand engine and no customer-facing story is harder to diligence and worth less. Separation work is funded as deal expense, not marketing budget — a larger pool, approved on a deal timeline, priced against the cost of missing a close date.

**Credential** TMG was reviewed and approved by all three parties on a $1.5B separation — the seller and both sponsors. Very few marketing firms can say they were brought inside a live transaction before announcement.

**Connection note**

> {first_name} — saw the {company} separation announcement. We ran the commercial build on a $1.5B medtech separation, approved by the seller and both sponsors, and delivered before close. Would like to connect.

**Message 1**

> Saw the {company} separation, {first_name}.
>
> Most of these go to market with a name and a close date, and the commercial build starts after the deal is done. Which means the business gets diligenced with no independent way to generate demand.
>
> We were brought in about five months before close on a $1.5B medtech separation and built it inside the window: brand architecture across seven sites in three countries, sales engine in place, day-one launch in 93 business days.
>
> Is the go-to-market side of the separation scoped yet, or is it sitting with the buyer?

**Message 2**

> Is the business being sold under its own brand, or does it carry the parent name today?

**Message 3**

> Asking because that is the difference between a naming and identity build and a transfer, and the two run on very different timelines against a close date. Happy to share how the last one was sequenced.

---

## 3. NewCo Countdown — NewCo Leadership

*Proposed config-slug:* `newco-countdown-newco-leadership`

**Segment** Newly separated medtech and diagnostics businesses, $250M+ in carved-out revenue, zero to twelve months past close.

**Persona** CEO, President, or the most senior commercial hire at the new entity.

**Trigger** Close completed, or the leadership appointment announced. At announcement this persona frequently does not exist yet, which is why this is a separate sequence from the sponsor campaign.

**Qualifying signal** If the newco is ninety or more days past close with no CMO or CCO listed on LinkedIn, nobody owns demand and the sponsor's growth plan is already slipping.

**Angle** On day one the business loses the parent's brand pull, channel relationships and installed-base access simultaneously, while the revenue plan still quietly assumes some of it carries over. It surfaces about two quarters in, as pipeline that is thinner than the model.

**Connection note**

> Congrats on the {company} close, {first_name}. We built the commercial side of a $1.5B medtech separation — brand through day-one launch, seven sites, three countries. Would like to connect.

**Message 1**

> Congrats on getting {company} across the line, {first_name}.
>
> We ran the commercial build on a separation like this one. The thing that rarely gets scoped: on day one you lose the parent's brand pull, their channel relationships and their installed-base access all at once, while the forecast still assumes some of it carries over.
>
> It usually surfaces about two quarters in, as pipeline that is thinner than the model.
>
> Is that showing up yet, or still early?

**Message 2**

> When you separated, did the customer data and the demand infrastructure come with the business, or did it stay with the parent?

**Message 3**

> Asking because that answer largely determines whether this is a rebuild or a repair. Happy to share what we found when we mapped it on the last one.

---

## 4. New Leader, Old Portfolio

*Proposed config-slug:* `new-leader-old-portfolio`

**Segment** Two company types only.
(a) Multi-business-unit device or diagnostics companies, $250M to $3B revenue, running three or more distinct product brands into overlapping hospital call points.
(b) PE-backed platforms mid-roll-up, $100M to $1B, that have absorbed two or more acquisitions without consolidating the brands.

**Exclusions** Single-product companies, pre-commercial companies, anything under roughly $100M, and anything currently in a separation — that belongs to campaigns 1 through 3.

**Persona** The most senior marketing or commercial person at the company, whatever the title happens to be. At a $2B company that is a CMO or CCO. At a $200M company, Marketing Director is the top job.

**Prioritize** External hires over internal promotions.

**Trigger** Role change announced thirty to seventy-five days ago.

**Angle** A new commercial leader has to publish a plan inside ninety days and does not yet know which inherited brands are worth keeping or how they ladder up.

**Connection note**

> {first_name} — congrats on the {company} move. Most new commercial leads in medtech inherit multiple product brands and have to publish a plan before they have worked out which ones matter – or how they ladder up with a story that makes sense. That is the part we help with. Would like to connect.

**Message 1**

> Congrats on the new seat, {first_name}.
>
> The hard part of a first ninety days in medtech usually is not building the story — it is deciding which of the brands you inherited are worth investing in, and which are just legacy that nobody has retired yet.
>
> We just did that on a carved-out medtech manufacturer: seven sites, three countries, about a dozen product brand names. Two had real equity with customers, so they stayed. The rest were retired and rolled under one master brand.
>
> The build was not the hard part. Working out what actually had equity, and what was just familiar internally — that was.

**Message 2**

> Out of curiosity — when you took the seat, was there a clear internal view on which product lines are actually strategic? Or is that still being argued?

**Message 3**

> Asking because that is where most first-ninety-days plans stall. If it is useful, I can walk you through the criteria we used to sort that portfolio into keep, merge and retire — including how we defended the retires internally. About twenty minutes.

---

## 5. Exit Ready

*Proposed config-slug:* `exit-ready`

**Segment** PE-backed medtech and diagnostics platforms, $100M to $1B, held three or more years, post-roll-up or in exit preparation.

**Persona** CEO, CCO, VP Marketing and Sales. The sponsor's operating partner as a secondary path — and if that path is available, take it first.

**Trigger** Hold period of three or more years; two or more add-on acquisitions not yet consolidated under one brand; a banker engaged or a sale process reported; or a senior finance hire with exit or IPO experience, which is a reliable tell.

**Angle** A buyer underwrites a story, not only an EBITDA number. A platform that reads as a collection of acquired companies with overlapping brands gets discounted against one that reads as a single business with a defensible position. The consolidation work has to happen well before the process starts, not during it.

**Connection note**

> {first_name} — {company} has grown through acquisition and still runs several brands. We consolidated a portfolio in that shape ahead of a transaction and prepped the company for an $800M exit. Would like to connect.

**Message 1**

> {first_name} — from the outside, {company} looks like it has grown through acquisition and still carries several of the original brands.
>
> That is normal and usually fine operationally. It gets expensive at exit, because a buyer underwrites one story, not four.
>
> We consolidated a portfolio in a similar spot — four companies, dozens of product names, all consolidated under one master brand prepping the organization ultimately for an $800M exit.
>
> Is the plan to bring those together before a process, or run them as they are?

**Message 2**

> Looking at the next eighteen months — is the priority growth, or getting the business into a shape a buyer can underwrite quickly?

**Message 3**

> Asking because those two need different sequencing, and the consolidation work is much cheaper before a process than during one. Happy to share the criteria we used to decide what to keep and what to retire.

---

## 6. The Import Without a Playbook

*Proposed config-slug:* `import-without-a-playbook`

**Segment** US subsidiaries and affiliates of non-US headquartered medtech and diagnostics parents, $100M to $500M in US revenue. Parent headquartered in Europe, Japan, Israel or Korea.

**Persona** The most senior US marketing or commercial person — Marketing Director, VP Marketing, Head of US Marketing, or the US General Manager.

**Trigger** FDA clearance or approval supporting a US launch in the last ninety days; an announced US expansion, new US facility, or first US commercial hires; or a new US marketing or commercial leader in the last thirty to seventy-five days.

**Angle** US subsidiaries run on assets translated from headquarters rather than built for how US hospitals, IDNs and GPOs actually buy. The US team usually knows this and has neither the budget line nor the mandate from the parent to fix it. The real obstacle is not conviction — it is headquarters approval.

**Connection note**

> {first_name} — noticed {company} runs the US business for a global parent. We rebuilt the US-facing brand and site for a subsidiary in that position, with no internal medtech marketing bench, in under four months. Would like to connect.

**Message 1**

> {first_name} — {company} runs the US arm of a global parent, which usually means US marketing runs on assets adapted from headquarters.
>
> That works until you are selling into US hospitals, IDNs and GPO contracts, where the buying process looks nothing like the home market.
>
> We rebuilt the US-facing brand and website for a company in exactly that position — no internal medtech marketing bench — in under four months.
>
> Is the US presence built for this market, or mostly adapted from what the parent already has?

**Message 2**

> Does headquarters own the global brand system, or do you have room to build for the US specifically?

**Message 3**

> Asking because that is the difference between a translation project and a build. Either way, happy to share how we handled the approval side with the parent company — that is usually the harder half.

---

## 7. Portfolio Without a Throughline

*Proposed config-slug:* `portfolio-without-a-throughline`

**Segment** Same as campaign 4(a) — multi-business-unit device and diagnostics companies, $250M to $3B, three or more product brands into overlapping call points.

**Persona** VP Product Marketing, VP Marketing, CMO.

**Angle** Multiple product families selling into the same hospital and physician call points compete with each other for internal budget and attention before they ever compete with an outside rival, because there is no shared value proposition tying them together.

**Connection note**

> {first_name} — noticed {company} runs several product lines into overlapping call points. We consolidated a portfolio in that shape: about a dozen product names down to two. Would like to connect.

**Message 1**

> {first_name} — {company} has several product families selling into a lot of the same hospital and physician call points.
>
> That usually means they are competing with each other for internal budget and attention before they compete with anyone outside the building and the dollars you're spending aren't going to realize the return you're hoping for.
>
> We unified a portfolio in exactly that shape – tripling engagements while cutting the cost of acquisition by 50%.
>
> Is there one shared value proposition across those lines today, or does each still tell its own story?

**Message 2**

> Is that a brand problem, a sales enablement problem, or both?

**Message 3**

> Asking because those get fixed with a different first step. Happy to compare notes on how we sequenced the last one.

---

## Open items for the next session

1. Campaigns 4(a) and 7 target the **same segment** with different personas and angles. Decide whether
   they share one sourcing config (one company universe, two people-search layers) or get two configs.
   Whichever is chosen, say so explicitly in the History entry.
2. None of these seven exist in `tracking_clients` yet — no sourcing configs, and campaign/sequence
   records not verified. Create them there before building anything in HeyReach, per CLAUDE.md
   "Campaign build standard per client" part 1.
3. Per-company contact counts are undecided for every segment except the note on campaign 1
   ("do not run it for volume"). Record the TAM/SAM read and resulting contact count in each
   segment's `.query.md` at first pull.
4. Message copy above uses `{first_name}` / `{company}`. HeyReach merge-variable syntax must be
   validated before launch — see the `heyreach-campaign-launch-prep` skill.
