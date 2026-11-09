# Campaign 10 universe — "The Dealer Who Rebuilt Your Brand Badly" — 2026-09-28

**New segment** (new config-slug `dealer-brand-consistency`). Campaign definition supplied by
the repo owner in-session: manufacturers selling through independent dealer, distributor or
rep networks of **50+ locations** in construction & ag equipment, trailers, material
handling, power equipment, HVAC, trucks & bodies, plus flow control & hydraulics. Contacts:
Director of Channel/Dealer Marketing, Dealer Development Manager, Director of Marketing
Communications, Co-op Marketing Manager; in flow/hydraulics the distributor-marketing or
rep-program owner.

**Not yet in `tracking_clients`.** No VNTANA campaign carries this name. A blank campaign
(`cd455ffa-92d0-4a7a-ab29-25e3d54b7bf0`, step 1, created 2026-09-28 16:04 UTC) may be it —
unconfirmed.

## Result
| Tier | Count | Meaning |
|---|---|---|
| **A_verified_50plus** | **98** | OEM, in-vertical, dealer/mixed channel, evidence cites a published count ≥50 |
| **B_dealer_channel_size_unpublished** | **~408** | OEM, in-vertical, dealer channel confirmed (locator and/or channel staff), **no published count** |
| C_verified_under_50 | 54 | published count below 50 |
| out_* | ~378 | not an OEM, off-vertical, sells direct, or no evidence |

**The headline finding: the campaign's 50+ gate cannot be verified from the public web for
most accounts.** Dealer-network size is simply not published by most manufacturers. Two
agent passes proved this from opposite directions — see "What went wrong" below.

## Pipeline — every tool used
1. **Base:** the 3,472 FIT+UNSURE US companies from `../2026-09-16-us-icp-triage.csv`.
2. **Blitz** `/v2/search/people` — dealer-channel persona scan on all 3,472. Working shape:
   `{"company":{"linkedin_url":[u]},"people":{"job_title":{"include":[...]}},"max_results":25}`.
   Top-level title keys and `people.title`/`job_titles`/`keywords` are **silently ignored**
   (identical to a fake key). Titles come back in `headline`, not `job_title`.
   → 468 companies with dealer-channel staff; 2,009 people.
   Signal is **sufficient, not necessary**: correctly flags Kubota (18), Toro (22), Trane (50),
   Hyster-Yale (45); misses Vermeer, CNH, Reading Truck, Fisher Snow Plows.
3. **AI Ark** — independent gap check. `keyword.any` on DESCRIPTION works; combining two
   keyword blocks with `keyword.all` returns 400 "request not readable"; must send
   `Accept: */*`. 234 US dealer-channel companies, **189 not in our universe** — genuine
   misses incl. Great Dane, Utility Trailer, Big Tex, Takeuchi, Titan, Kenworth. Trailers is
   the most under-covered vertical. 76 in-vertical gap companies added to the candidate set.
4. **EXA** `/search` with `includeDomains=[domain]` — dealer-locator check on 1,712
   candidates. 716 locators found. Catches exactly the persona scan's misses (Reading Truck,
   Fisher Plows, Great Dane, Big Tex, Takeuchi). Vermeer missed by **both** signals.
5. **Miss-rate sample:** 40 random companies with neither signal, fully researched —
   5/40 (12.5%) still clear 50 (Romac 75, Fulton 65, ADD-USA 120, Broderson 68, Mogas 50).
   ~100 expected in that 774-company pool; wide interval at n=40. **Not yet pursued.**
6. **Web qualification:** 938 candidates, 47 Haiku agents × 20, ~4.7k tokens/account.
   Prompt: `2026-09-28-qualification-spec.md`. Keyed on batch **position**, never on an
   agent-echoed id (lesson from the 2026-09-16 run).
7. **Clay** `search-companies` works and returns `annual_revenue` at ~1k tokens/record (vs
   ~8k for `find-and-enrich-company`) — revenue for a shortlist is now affordable. Not used
   here: this campaign's gate is network size, not revenue. DSL field `country` does not
   exist as a filter.
8. **DiscoLike** — first use in this repo. Auth header `x-discolike-key`; endpoints
   `/v1/usage`, `/v1/discover`, `/v1/bizdata`. **Blocked: account over its monthly cap**
   ($202.19 spent vs $99 max, 57,768 records MTD). Not caused by this session.

## What went wrong, and how the numbers were made honest
- **Inflation.** First-pass agents padded counts toward the 50 threshold: Sanden's evidence
  said "8 North American distributors" → reported 100; OMAX "38 distributors" → 120; LMC Ag
  site shows 18 dealers → reported 175. A stone supplier with a 404 locator came out at 50.
- **Unresearched batches.** Batch 40 stated it classified 17/20 "using company names … and
  standard industry models". Batches 26, 40, 41 were rejected and re-run under hard
  anti-inflation rules (kept as `r0NN.rejected.json` in the scratch record).
- **Deflation.** The strict re-runs swung the other way: "count not published" was written
  as **0** (Franklin Electric, which plainly has a large network, came back 0).
- **Resolution:** tiers are assigned from the *evidence text*, not the agent's number. A
  row is Tier A only if its evidence cites a published figure ≥50 and does not say the
  count is unpublished. **26 rows** claimed 50+ while their own evidence stated fewer and
  were demoted automatically. Everything with a confirmed channel but no published figure
  is Tier B — "size unknown", never "0".
- **Is dealer-channel headcount a usable size proxy for Tier B?** Weakly. Among verified
  rows the base rate of ≥50 is ~65%; 5+ channel staff → 82% (n=17); 0 staff → 68%. Useful
  for prioritising, not for qualifying individually.

## Tier B — how to qualify it
The campaign's own first step — reviewing ten dealer sites side by side — **is** the size
test. An account whose locator cannot produce ten independent dealer websites fails the
angle regardless of network size. Qualify Tier B at build time from the locator, not now.
If Tier B behaves like the verified set, ~60% of it (~250) clears 50, but individually
unidentified.

## TAM/SAM → contacts per company (repo standard: small segment = go deeper)
Target = A+B, by vertical: flow/hydraulics 126 → **2** · construction/ag 94 → **2** ·
power equipment 73 → **3** · material handling 72 → **3** · HVAC 58 → **3** ·
trucks & bodies 52 → **3** · trailers 23 → **5** · RV 8 → **5**.
The persona is narrow (the dealer-marketing owner), so real depth is usually capped by how
many such people exist.

## Leads — `2026-09-28-leads.csv`
209 people at 117 target companies, keyed on `linkedin_url` (first column). From the 2,009
scanned: dropped 1,173 at non-target companies, 284 not the persona, 65 excluded roles
(dealer finance, dealer *learning*/training), 111 outside North America, 2 student co-op /
IT-channel false positives, 122 over the per-company depth. 102 `primary`, 107 `secondary`.
**Coverage gap: only 23% of target companies have a contact.** The scan capped at 25 people
per company, used dealer-specific title words only (excluding "Marketing Communications",
which is in the brief but is not a dealer-channel signal), and never ran on the 76 AI Ark
gap companies. Next step: a targeted people pull at the ~390 uncovered target companies
with the brief's full title list.

## Scope calls flagged to the repo owner (included, tagged, not yet ruled on)
- **HVAC** is in this brief but conflicts with the earlier "no building products" rule.
- **Trucks** (e.g. Isuzu Commercial Truck, Kenworth) conflicts with the earlier "not the
  vehicle OEM" rule — the brief names "trucks and bodies".
- **RV** OEMs (Forest River, Jayco, Heartland, Grand Design) were labelled `trailers` by
  agents; re-tagged `rv`. Earlier rule allowed RV *components* only.
