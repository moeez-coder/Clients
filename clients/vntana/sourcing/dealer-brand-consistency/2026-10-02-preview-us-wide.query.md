# Campaign 10 — wider-USA preview (2026-10-02)
Segment: expanding existing segment `dealer-brand-consistency` (client VNTANA 5e0a22cf-6efb-432d-bc3c-6eb914440f13, config 4d4f021e-e85b-4ce9-8ec6-96bdf98870a3). PREVIEW sizing only, not final sourcing.

## What was done
1. Universe: `icp-universe-na-weu/2026-09-29-companies.csv`, universe_status=IN, US HQ, minus the 938 companies already qualified in `2026-09-28-companies.csv` -> 18,328 companies in 3 strata: A_vertical 3,791 (keyword tag in a campaign-10 vertical), B_othertag 3,971 (other keyword tags), C_notag 10,566 (no tag).
2. Qualification sample (Haiku web-research agents, spec `2026-09-28-qualification-spec.md`, 15 per batch): 180 companies = A 75, B 60, C 45 -> `2026-10-02-preview-us-wide-sample.csv`. One agent (us4) exhausted its WebSearch budget; its answers are lower confidence.
3. Personas: Blitz `POST /v2/search/employee-finder` on 7,727 A+B companies (3,782 + 3,945 resolved), levels C-Team/VP/Director/Manager, functions Advertising & Marketing / Sales & BD / General Business & Mgmt / Operations, person countries US, GB, EU27, <=4 pages x 50. 136,743 rows / 128,684 unique people (2,732 companies returned 0). Classified with `classify_people.py` rules (T1 channel/dealer/co-op owners, T2 marcom leaders, T3 marketing-leader fallback) -> 3,032 persona rows (T1 565, T2 319, T3 2,148) -> `2026-10-02-preview-us-wide-personas.csv`. Stratum C was not pulled for people.
4. Projection: per-stratum sample rates x stratum population.

## Sample rates (dealer/mixed OEM = role OEM and channel independent_dealers or mixed)
| stratum | n | dealer/mixed | with >=50 locations stated |
|---|---|---|---|
| A_vertical | 75 | 27 (36%) | 4 (5%) |
| B_othertag | 60 | 18 (30%) | 2 (3%) |
| C_notag | 45 | 8 (18%) | 1 (2%) |

## Projection (wide US only, excludes the 938 already-qualified and UK/EU)
- Dealer/mixed OEM companies: ~4,430 (A ~1,360, B ~1,190, C ~1,880). Wide interval: n is small; treat as +/-30%.
- With a stated/verified >=50 locations: ~570. Most agents could not verify a count, so this is a floor, not a central estimate.
- People at dealer/mixed companies (A+B pulled, C extrapolated from B yields): core T1+T2 ~290 (A 154 + B 136) in A+B, ~510 incl. C; T1-T3 ~1,000 in A+B, ~1,700 incl. C.
- People at >=50-stated companies: core ~38, T1-T3 ~130 (A+B).

## Limits
Persona classifier is title-regex: T1 has false positives, T3 is noisy; core T1+T2 is the safer figure. Persona rows are not filtered to qualified companies (rates applied statistically). Agent evidence is web-search based and unaudited. Raw 136k-row Blitz pull is not committed (classified personas only).
