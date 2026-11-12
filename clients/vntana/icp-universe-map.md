# VNTANA — ICP universe map (2026-09-15)

> ## ⚠️ MAJOR CORRECTION — read this before §3/§5
>
> §3 and §5 sized these segments from Blitz and AI Ark and concluded the universe was
> "genuinely niche" (~120 CNC companies, 414 across all seven at $100M+). **Ground truth
> from the client says that undercounts badly.**
>
> The repo owner supplied VNTANA's own ICP verdicts on IMTS 2026 exhibitors: **250 marked
> "ICP Yes" and 113 "Near-ICP"** — 363 fits from **one trade show**, against an API-derived
> estimate of ~120 for the whole CNC/machine-tools segment. Every one of the 250 "Yes"
> companies is $100M+ revenue; 104 are $500M+. The client draws their ICP line at ~$100M,
> which does validate the revenue bar — but not the size of the pool.
>
> **Our sourcing had only 100 of those 250 (40%). We missed 142 client-confirmed fits**,
> including FANUC, KUKA, Sandvik, Iscar, ZEISS, Keyence, Thermo Fisher, Nikon Metrology,
> Stratasys, JTEKT, NSK, SICK, Weidmüller, Amada, Mitsubishi EDM, Okamoto and Tsugami.
>
> **Why we missed them** (diagnosed in Supabase against the enriched exhibitor list):
> 1. **The 201+ employee floor is wrong for this market.** 27 of 41 missed US companies
>    have <201 employees on LinkedIn because they are *US subsidiaries of large foreign
>    parents* (Chiron America, Tsugami America, Star CNC, Hwacheon America…). The parent
>    clears $100M+ easily; the US LinkedIn page does not clear 201 headcount. Filter on
>    **revenue**, not headcount, or drop the floor to ~50 for subsidiary-heavy segments.
> 2. **The 10-country geography is wrong for machine tools.** Missed companies sit in CH,
>    ES, AT, JP, CN, IL, IN, IE — none of which were in our `US CA GB DE AU FR IT SE NL MX`
>    set. Switzerland, Austria, Spain, Japan, Korea and Taiwan are core machine-tool
>    countries and were excluded by construction.
>
> **Methodological conclusion: for niche industrial segments, trade-show exhibitor lists
> and association member lists beat API taxonomy queries.** One exhibitor list produced 3×
> the fits our best API query could find. Treat Blitz/AI Ark as *enrichment and
> qualification* layers over an acquired list, not as the discovery layer. §3/§5 numbers
> should be read as a floor on each segment, not a ceiling.
>
> Working data now lives in Supabase (`vntana-universe`, project `xjhkjkjdidixdhqysdth`),
> table `public.companies` with `universe` and `addressable` views — 12,789 rows across
> four sources. See §10.

Reference doc, not a sourcing snapshot. Written to answer: *what industry taxonomy are we
using, and how big is the universe for Physical AI / plumbing-HVAC small parts / CNC /
off-highway, plus Bobcat- and Astec-lookalikes.* All counts are live Blitz
`POST /v2/search/companies` probes taken 2026-09-15. **Read the "Health warning" section
before planning volume off these numbers.**

## 1. The instruments Blitz actually gives us

The company filter supports more than we've been using. Confirmed live this session:

| Filter | Status | Use it for |
|---|---|---|
| `industry.include` | used since day 1 | Blunt bucketing only — see §2 |
| `naics_code.include` | **never used — works** | Precise segmentation. This is the right tool for all four segments asked about |
| `keywords.include` / `.exclude` | never used | Concepts neither taxonomy expresses; `[brackets]` = exact match |
| `revenue.min` / `.max` | **never used — works** | The ICP's actual `$100M+ / $500M+ preferred` bar, instead of proxying via headcount |
| `employee_range` | used | `1-10, 11-50, 51-200, 201-500, 501-1000, 1001-5000, 5001-10000, 10001+` |
| `employee_count.min/max`, `type`, `founded_year`, funding fields | never used | Available per the find-people schema (same `company` object) |

Two immediate consequences: we have been approximating a **revenue** ICP with a
**headcount** filter for three months when the real filter exists, and we have been
segmenting with the one field that cannot express any of VNTANA's segments.

## 2. The taxonomy we've been using, and why it can't segment

Blitz normalizes industry to the **LinkedIn/Clay industry taxonomy** (the ~457-value set),
with one formatting quirk: **commas become semicolons** — `Agriculture; Construction;
Mining Machinery Manufacturing`, `Metal Valve; Ball; and Roller Manufacturing`,
`Electric Power Transmission; Control; and Distribution`. Values are case-sensitive; a
wrong string silently returns 0.

Of ~120 manufacturing-relevant values, five hold essentially everything and the precise
ones are nearly empty. Solo counts, 201+ employees, our 10 target countries:

| Value | Count | |
|---|---|---|
| Motor Vehicle Manufacturing | 597 | the generic buckets… |
| Manufacturing | 550 | |
| Appliances; Electrical; and Electronics Manufacturing | 410 | |
| Machinery Manufacturing | 360 | |
| Industrial Machinery Manufacturing | 284 | |
| Wholesale Building Materials | 275 | *(distributor bucket — ICP disqualifier)* |
| **Agriculture; Construction; Mining Machinery Manufacturing** | **23** | …and the precise ones |
| HVAC and Refrigeration Equipment Manufacturing | 15 | |
| Robotics Engineering / Robot Manufacturing | 7 / 1 | |
| Metalworking Machinery Manufacturing | 4 | |
| Metal Valve; Ball; and Roller Manufacturing | 1 | |
| Cutlery and Handtool Manufacturing | 1 | |

The single most on-ICP value in the entire taxonomy — construction/ag/mining machinery —
holds 23 companies. Caterpillar- and Komatsu-class firms are tagged generic `Machinery
Manufacturing`. **There is no taxonomy value at all** for: heavy-duty trucks, material
handling, hydraulics & pneumatics, industrial tools, process equipment, machine tools, or
off-highway — all of which the ICP names explicitly. Every prior pull hand-translated
those into broad proxies, which is where the contamination we scrub each round comes from.

## 3. Segment map — NAICS (the recommended instrument)

Live counts, 201+ employees, 10 countries (US CA GB DE AU FR IT SE NL MX). `union` is
de-duplicated across the codes in that row; revenue columns apply the ICP's own bars.

| Segment | NAICS codes | union | $100M+ | $500M+ |
|---|---|---|---|---|
| **Physical AI / robotics / sensing** | 333998, 334511, 334519, 335999 | 417 | 194 | 152 |
| **Plumbing / HVAC small parts** (Kohler-, Taco-like) | 333415, 332913, 332911, 332912, 332919, 333414, 326191 | 155 | 82 | 63 |
| **CNC / machine tools** | 333517, 333515, 333514, 333519 | 120 | 54 | 42 |
| **Off-highway / construction equip** (Bobcat-like) | 333120, 333131, 333111, 333112, 333924 | 95 | 50 | 34 |
| **Aggregate / road building** (Astec-like) | 333120, 333131, 333922, 332420 | 72 | 38 | 26 |
| **Hydraulics / pneumatics** *(named in ICP, never sourced)* | 333995, 333996, 333912, 333914 | 62 | 35 | 29 |
| **Power transmission / engines** | 333612, 333613, 333618 | 37 | 19 | 14 |
| **All seven, de-duplicated** | | **849** | **414** | **315** |

Code reference: 333120 Construction Machinery · 333131 Mining Machinery · 333111 Farm
Machinery · 333924 Industrial Truck/Stacker (material handling) · 333922 Conveyor ·
333517 Machine Tool · 333515 Cutting Tool & Accessory · 333519 Rolling Mill/Other
Metalworking · 333415 AC/Heating/Commercial Refrigeration · 332911 Industrial Valve ·
332913 Plumbing Fixture Fitting & Trim · 332912 Fluid Power Valve & Hose Fitting ·
332919 Other Metal Valve & Pipe Fitting · 333414 Heating Equipment · 326191 Plastics
Plumbing Fixture · 333998 All Other General Purpose Machinery (where most robotics sits) ·
334511 Search/Detection/Navigation/Guidance (lidar) · 334519 Other Measuring & Controlling
Device · 335999 Other Electrical Equipment · 333995/333996 Fluid Power Cylinder/Pump ·
333912 Air & Gas Compressor · 333914 Measuring/Dispensing Pump.

## 4. Current coverage — these segments are effectively unmapped

Against the 10,586 companies already in this repo, matching segment terms **in the company
name only** (the company CSVs carry no description field, so this is a floor, not true
coverage):

| Segment | Companies in repo whose *name* matches |
|---|---|
| Plumbing / HVAC | 82 |
| Physical AI (robot/autonomous/lidar/sim) | 56 |
| CNC / machine tools | 15 |
| Aggregate / road building | 7 |
| Off-highway / compact equipment | 6 |

The existing pool is generic-machinery shaped. None of the four segments has been
deliberately sourced.

## 5. Second-source validation — the universe really is this small

Blitz alone would not be trustworthy here (see §6), so every segment was re-sized against
**AI Ark**, an independent provider with a completely different method: Blitz counts by
NAICS code, AI Ark counts by keyword match against the company description. They agree on
order of magnitude for every segment.

| Segment | AI Ark, any rev | Blitz, any rev | **AI Ark $100M+** | **Blitz $100M+** |
|---|---|---|---|---|
| Physical AI / robotics / sensing | 744 | 417 | 116 | 194 |
| Plumbing / HVAC small parts | 844 | 155 | 86 | 82 |
| Aggregate / road building | 385 | 72 | 45 | 38 |
| Hydraulics / pneumatics | 253 | 62 | 30 | 35 |
| Off-highway / construction equip | 122 | 95 | 12 | 50 |
| CNC / machine tools | 119 | 120 | 9 | 54 |

**Conclusion: these are genuinely niche segments.** At the ICP's own $100M+ revenue bar,
each is on the order of **tens to low hundreds of companies**, and Blitz's de-duplicated
union across all seven is **414** ($500M+: **315**). Two independent vendors, two
methodologies, same answer. This is not a sourcing failure — it is the actual shape of the
market VNTANA sells into.

That reframes the 8,200-company `aftermarket-oems` pool: it is a broad-industry dragnet,
not 8,200 ICP-fit accounts. It is consistent with what we already scrub out of it each
round (464 automotive leads dropped last round, 1,630 building-materials distributors
sitting in it). And it explains why the "at least 5,000 prospects" push topped out at 660
quality leads — the addressable universe at that quality bar is a few hundred companies per
segment, not thousands.

## 6. Instrument health warnings

**Blitz `total_results` is internally coherent but disagrees with its own history.** The
`aftermarket-oems` recorded filter was paginated earlier *the same day* to 10,000 raw
records → 8,200 companies now in this repo. Re-running it now returns `total_results` =
1,793 and genuinely exhausts (`cursor: null`) at 1,793. Per-country: US 169 / DE 71 / IT 30
against repo holdings of US 1,100 / DE 615 / IT 212 from that same filter. The repo rows
are internally consistent with the filter (all 201+, all in-geo), so it is not a historical
filter error. `total_results` slices additively (per-country and per-band sum *exactly* to
the combined figure) so it is not a random cap, and slicing finer does **not** recover
volume. `fair_usage.records_remaining` is 14.17M, so it is not quota exhaustion. Most
likely an index rebuild or a change in what this account can reach — **re-probe before
committing to a plan**, and note that AI Ark's independent numbers (§5) are in Blitz's
current range, not its historical one.

Also: Blitz `max_results` documented max is **25**; prior VNTANA pulls passed 50.

**AI Ark blocks the default Python user-agent.** `Python-urllib` gets `403 error code 1010`
(Cloudflare) on every call. Sending `User-Agent: curl/8.5.0` fixes it. Base URL is
`https://api.ai-ark.com/api/developer-portal`, auth header `X-TOKEN`, endpoint
`POST /v1/companies`. Credits at time of writing: 14,769.

**AI Ark lookalikes: seed with the LinkedIn company URL, not the domain.** Seeding
`astecindustries.com` returned Mexican government agencies, schools and a fried-chicken
chain — the domain did not resolve. Seeding
`https://www.linkedin.com/company/astecindustries` returned a coherent list immediately.

**EXA is a web-page similarity engine, not a company-entity engine.** `findSimilar` on
these seeds returns Wikipedia, Bloomberg, Owler and LeadIQ profile pages about the seed
rather than peer companies. Use EXA Websets for entity work, or not at all for this.

## 7. Lookalikes — Bobcat and Astec

Seed file: `sourcing/2026-09-15-lookalike-seeds.csv` (200 rows, DNC removed, each row
classified). Sources: AI Ark `lookalikeDomains` (LinkedIn-URL seeds) plus Clay's
`Company Competitors` enrichment.

Clay competitors (shallow — 3 each, useful only as seeds): **Bobcat → Caterpillar, John
Deere, Kubota**; **Astec → Caterpillar, Komatsu, Metso Outotec**.

**Bobcat-like (compact construction equipment)** — 100 returned, 74 classified as
manufacturers. Strong hits: JCB, Wacker Neuson, BOMAG, YANMAR, Kubota, Komatsu, Manitou,
Carraro, Takeuchi, Mecalac (Fayat), Multiquip, Putzmeister, McLanahan, Toro, AGCO, Altec,
Linamar. This list is directly usable.

**Astec-like (aggregate / road building)** — 100 returned, 48 classified as manufacturers,
but **the classification needs a human pass**: lookalike-by-similarity returns companies in
the same *industry*, not the same *business model*. Most results (Holcim, Heidelberg, Knife
River, CalPortland, Cemex, Colas, Eurovia, Peab, Heijmans, Aggregate Industries) are
aggregate producers and road contractors — i.e. **Astec's customers, not Astec's peers**,
and contractors/producers are ICP disqualifiers. The genuine peers in the list are Marini /
FAYAT Group, Metso, McLanahan, Rulmeca and Mellott. A keyword-based query on
`asphalt plant / aggregate processing / crushing and screening` returned only 12 companies
total, which corroborates §5 — this is a very small segment.

Dealer contamination persists in both lists (Holt of California, Thompson Tractor, Finning,
Milton CAT, Wagner Equipment, Blanchard, Hugg & Hall). The `classification` column flags
what it can; treat `manufacturer - REVIEW` as a candidate, not a verdict.

## 8. Tool inventory — six sourcing APIs are live in this environment

CLAUDE.md and the root README are **out of date** on three of these (flagged, not edited —
both are governed system files):

| Key | Status | Best used for |
|---|---|---|
| `BLITZ_API_KEY` | live, used | NAICS + revenue + keyword company search; see §6 health warning |
| `AIARK_API_KEY` | live, first used today | **Lookalike search** (LinkedIn-URL seeds), description-keyword search, revenue/employee ranges, `productAndServices`, tech filters |
| `CLAY_API_KEY` + `mcp__Clay__*` | live | Single-company enrichment, `Company Competitors`, own-CRM queries. Not a bulk sizing tool |
| `PROSPEO_API_KEY` | **live now** — CLAUDE.md and root README both say "not confirmed live" | Not yet exercised; both docs ask to be updated once confirmed |
| `EXA_API_KEY` | **live** — CLAUDE.md says EXA is "not wired into these sessions" | Web-page similarity; Websets for entity work. Poor fit for company lookalikes |
| `COLDIQ_API_KEY` | **live, undocumented anywhere in this repo** | Unknown — not yet exercised |
| `DISCOLIKE_API_KEY` | **live** — CLAUDE.md says DiscoLike is "not wired into these sessions" | Original source of the two 99-company DiscoLike configs; not yet exercised this session |

## 9. Open questions for the repo owner

1. **Physical AI is two different motions, and only one is in the current ICP.** (a) Robot
   and autonomous-machine OEMs are ordinary VNTANA targets — discrete manufacturers with
   CAD, dealer channels, configurable products. (b) The Omniverse/simulation play — physical
   AI companies needing CAD converted into simulation-ready and synthetic-training assets —
   is a genuinely different pitch that VNTANA's own materials support (Omniverse is named
   as an activation channel) but the ICP form does not describe. Which one are we sourcing?
2. **The plumbing/HVAC segment already has two proof logos on the DNC list** — Kohler and
   Taco Comfort Solutions (hydronic pumps and valves). That is the strongest named-customer
   evidence for any segment here, and it is the one segment where small, visually-similar
   parts make mis-ordering worst. Confirm we can reference them.
3. **`Wholesale Building Materials` (275 live / 1,630 already in repo) is a distributor
   bucket and distributors are a hard ICP disqualifier** — yet it is written into the
   `VNTANA Aftermarket OEMs` config's own `market` string in `tracking_clients`, alongside
   `Retail Building Materials and Garden Equipment`. Fixing that is an edit to the source of
   truth and needs your sign-off.
4. **Switch the size bar from headcount to `revenue.min`?** The ICP says $100M+ / $500M+
   preferred; the filter exists and we have never used it.

## 10. Supabase working database

Project **`vntana-universe`** (`xjhkjkjdidixdhqysdth`, us-east-1, free tier, $0/mo) in org
`moeez-coder's Org`. Created 2026-09-15 as the working layer for universe refinement —
the repo stays the audit trail, Supabase is where the set gets sliced and enriched.

**`public.companies`** — 12,789 rows, one row per (company, source) observation:

| source | rows | what it is |
|---|---|---|
| `repo_sourcing` | 10,388 | every company CSV in `clients/vntana/sourcing/**` |
| `imts_exhibitor` | 1,738 | IMTS 2026 exhibitor list, enriched via Blitz (87% LinkedIn match, 85% employee count) |
| `client_icp_verdict` | 363 | **VNTANA's own ICP verdicts** — 250 Yes / 113 Near-ICP, with revenue band, products and their `3D Model` demo-asset call |
| `aiark_lookalike` | 300 | Bobcat/Astec lookalike peers from AI Ark |

Refinement columns added in-database: `is_dnc` (VNTANA's `dncList`), `exclusion_reason`
(dealer / rental / distributor / services / education-nonprofit / software-services /
contractor — 421 rows flagged), `size_band`.

Views: **`universe`** (11,949 — deduped on domain→linkedin→name, best source wins, client
verdict ranked first) and **`addressable`** (10,692 — DNC-clean, no exclusion reason,
201+ employees *or* unknown).

RLS is enabled with no policies, and both views are `security_invoker` — nothing is
readable through the anon/publishable key. Access is via the MCP server's privileged
connection. Verified clean on the security advisor apart from the informational
"RLS enabled, no policy" notice, which is the intended state for a private working table.

**Caveat on `addressable`:** it still applies the 201+ headcount floor that the correction
at the top of this document shows is wrong for subsidiary-heavy segments. Re-cut it on
revenue once revenue coverage is filled in.

## 11. Client's own segmentation (from their IMTS verdicts)

Worth mirroring in how we build campaigns — this is VNTANA telling us how they see the
market, including which 3D demo asset each group needs:

| Client's group | Companies | `3D Model` they'd build |
|---|---|---|
| Machine Tools & Fabrication Machinery | 168 | CNC Machine |
| Automation, Robotics & Material Handling | 58 | Robotic Arm |
| Cutting Tools, Tooling & Workholding | 57 | "Small like Caplugs" |
| Shop Support, Components & Consumables | 45 | mixed |
| Metrology & Inspection | 35 | mixed |

Note the middle row: **"Small like Caplugs"** is exactly the small-mechanical-parts
catalogue motion — the client already thinks in that shape, which supports the
plumbing/HVAC-parts segment thesis alongside Kohler and Taco Comfort as reference logos.
