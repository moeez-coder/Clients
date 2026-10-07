# Query — 2026-10-07 companies snapshot, NARROWED stage (dealer-network manufacturers)

Follows `2026-10-07-companies-wide.csv` (97,469 companies, see its `.query.md`). Same segment and config: **`Dealer-network manufacturers reviewed for inconsistent product imagery across 10 dealer sites`, UUID `4d4f021e-e85b-4ce9-8ec6-96bdf98870a3`**; campaign "The Dealer Who Rebuilt Your Brand Badly" (`2a5ec07e-6fac-46e5-a6e4-8a0c6a3458d8`). Repo owner's instruction: "go as wide as possible and then narrow down." Output: `2026-10-07-companies-qualified.csv` (**1,667 companies**, one row each, tiered).

## Funnel

| Stage | Method | In → out |
|---|---|---|
| 0. Wide pool | Blitz + Prospeo + DiscoLike + EXA, deduped | → **97,469** |
| 1. Deterministic gates | Regex over name/industry/description/keywords. Keep if: matches one of six vertical patterns (construction/ag, trailers & truck bodies, material handling, power equipment, HVAC, flow/hydraulics) **or** has a dealer-network signal; has manufacturing language or a manufacturing industry; **not** dealer-/rental-/distributor-/reseller-shaped by name or text; industry not retail/wholesale/rental/services; ≥51 employees. | 97,469 → **31,940** |
| 2. Candidate cut | **A** = dealer-network signal (DiscoLike site phrase or profile text) + vertical/manufacturing industry (2,905). **B** = vertical match, no network signal yet, ≥200 employees, in US/CA/GB/IE/AU/NZ (2,802). | → **5,707** |
| 3. Classification | 14 Claude (Sonnet) subagents × ~408 records. Each record judged individually from name/domain/industry/country/size/signals/≤520 chars of description: `type` (oem / component_oem / contract_mfr / dealer_distributor / service_other / unclear), `vertical`, `network` (yes / likely / unknown / no_direct), `keep` Y/M/N. All 5,707 rows returned and alignment-checked against the input (index **and** a 12-char name echo): 0 misaligned. | 5,707 → **2,088 Y/M** (Y 1,016 · M 1,072 · N 3,619) |
| 4. Dealer-network evidence | **EXA `POST /search`** per company, `includeDomains:[<own domain>]`, query "<name> dealer network locator authorized dealers distributors", 5 results, highlights ("how many authorized dealers, distributors or dealer locations…"). 2,041 had a domain; **1,941 returned pages from their own site**; cost $13.59. | 2,041 → 1,941 with evidence |
| 5. Extraction | 10 Claude (Sonnet) subagents × ~195, each in its own scratch folder. Per company: `locator`, `network_type`, `count` + `count_text` **only if literally stated in the evidence**, `evidence_url`, `scale`. Alignment-checked (0 misaligned). **Every stated count is machine-verified: the quoted words must appear in the evidence text** — 190 of 193 "50+" claims passed; the other 3 are downgraded to `…count_unverified` and carry no count. | 1,941 rows |
| 6. Tiering + exclusions | See below. Dropped: 237 no network evidence either way, 120 evidence of direct-only sales, 35 not an OEM/component maker, 25 stated count <50, 3 on the client's DNC list, 1 not a target vertical. | → **1,667** |

## Tiers (`tier` column)

- **Q1_verified_50plus (188)**: the company's own site states ≥50 dealers/distributors/authorized locations (or "hundreds"/"thousands"); the count and exact quote are in `dealer_count_stated` / `dealer_count_quote`. **These are the only rows where the campaign's "50+ locations" qualifier is proven.**
- **Q2_network_evidenced_count_unstated (1,100) + …count_unverified (2)**: the site has a dealer/distributor/rep locator, "become a dealer" or dealer portal, but publishes no count. Plausible 50+, not proven.
- **Q3_network_claimed (221)**: the classifier judged a dealer/distributor network from the profile text, but the site pass didn't confirm a locator.
- **Q4 (156)**: `likely_unverified` (43), network is typical for the category only, or `no_site_evidence` (113), EXA returned nothing for the domain. Lowest confidence; use only if volume is needed.

## Findings the numbers hide

- **Only ~10% of companies publish a dealer count** (193 of 1,941), so "50+ locations" cannot be hard-verified for most of the list from public pages. If the client's bar is *proven* 50+, the list is Q1 (188). If it's "sells through a real dealer network", it's Q1+Q2 (1,290). The decision is the repo owner's; both are ready.
- Verticals (Q1+Q2): construction/ag 326 · trailers & trucks 255 · HVAC 227 · flow/hydraulics 203 · power 136 · material handling 100 · other industrial 43. 72% are in US/CA/GB/IE/AU/NZ.
- 660 of the 1,667 were already in the repo from earlier VNTANA pulls (`prev_sourced_in_repo`), so they're warm accounts for other campaigns; check for double-contacting.
- Several large global OEMs (Caterpillar, AGCO, Navistar/International, IC Bus…) are here and also sit in the separate "Largest Global OEMs / The Named Accounts" config (`38339bea-da1c-4b31-b232-6e5751ab4807`). Some OEMs have more than one LinkedIn page (e.g. Caterpillar and "Cat Construction"); not merged.

## Caveats

- Classification and extraction are model judgement over short text; the stated-count check is the only mechanical verification. Spot-check before outreach.
- Not applied: any revenue floor (revenue is present for a minority), and "used equipment excluded" (a property of the dealer sites, not the OEM list).
- Aerospace/defense-primary and passenger-car OEMs were excluded by the classifier (`not_target`); the 3 DNC and no existing-customer matches were dropped by domain.
- AI Ark was blocked (HTTP 402, subscription past due) for the whole run, so AI Ark's lookalike and keyword reach is **not** in this list; re-run once paid.

**Spend this stage:** EXA $13.59 (+$9.51 discovery in the wide stage) · Claude subagents for classification and extraction.
Scripts: `2026-10-07-scripts/`.

## DNC re-check (added 2026-10-07, after the repo owner uploaded the client's DNC file)

The uploaded `vntana-dnc-list.csv` (21 rows) is **identical** to `tracking_clients.get_client` `dncList`. The first build dropped only **exact primary-domain** matches (3 rows), so related entities on other domains slipped through. A name + domain-brand re-check found **3 companies** in this file: *Peterson, an Astec Brand* (`petersoncorp.com`), *Doosan Industrial Vehicle America* (`doosanlift.com`), *Bobcat Portable Power SA* (`doosansa.co.za`). **No lead in `2026-10-07-leads.csv` belongs to them (0 contacts affected).** Corrected file: **`2026-10-07-companies-qualified-2.csv`** (1,664 rows); the original stays as the audit trail. The wide file is unfiltered by design (95 DNC-named rows, mostly Bobcat/Doosan dealers, which the classifier rejected as dealers). Lesson recorded: match DNC by company/brand name and domain-brand, not by exact domain alone.
