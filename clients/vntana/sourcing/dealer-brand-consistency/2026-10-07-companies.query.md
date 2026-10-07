# Campaign 10 sourcing run — 2026-10-07
Client VNTANA `5e0a22cf-6efb-432d-bc3c-6eb914440f13`; sourcing config `4d4f021e-e85b-4ce9-8ec6-96bdf98870a3` (campaign `2a5ec07e-6fac-46e5-a6e4-8a0c6a3458d8`). **Expanding existing segment** `dealer-brand-consistency` (adds US-wide + UK/EU to the 2026-09-28 US set). Contacts limited to US, UK and EU27 persons.

## Cut applied (repo owner had not picked a cut; this is the "independent-dealer or mixed channel" cut they asked about on 2026-10-02)
A company qualifies when role = OEM and channel = independent_dealers or mixed.
- `A_verified_50plus`: qualifies and 50+ dealer locations found (2026-09-28 rows keep their original verified tier; new rows need confidence high/medium).
- `B_dealer_channel_size_unconfirmed`: qualifies but the count is unpublished or only a low-confidence estimate (includes new rows whose >=50 estimate was low confidence — 91 downgraded from A).
- `C_verified_under_50`: qualifies on channel but a count under 50 was found. Kept in the companies file, NOT in leads.
- `out`: not an OEM selling through dealers.
Leads cover tiers A and B only. Tighten to strict = A only.

## Steps
1. Candidates: every company with at least one T1/T2 persona from the Blitz employee-finder pulls (2026-10-02 UK/EU+US and US-wide) that was not already qualified: 850 (508 US, 342 UK/EU). Companies with no core contact were not researched.
2. Qualification: 57 batches x 15 Haiku web-research agents (WebSearch/WebFetch), spec `C10_SPEC_Q.md` derived from `2026-09-28-qualification-spec.md` (count in USA+UK+Europe combined; no inflating numbers). Many agents hit search limits; 457 of the 1,105 newly researched rows (850 + 255 sample) are confidence=low — treat B as unverified.
3. Merged with the 938 rows of `2026-09-28-companies.csv` (936 keyed; 2 had duplicate LinkedIn URLs) and the 255 sample rows from the 2026-10-02 previews -> 2,041 companies.
4. Contacts: Blitz `/v2/search/employee-finder` personas (2026-10-02 pulls), the 2026-09-28 leads, and a Prospeo `POST /search-person` gap-fill (filters `company.websites.include=[domain]`, 15 title keywords, `X-KEY`, ~1 req/s; 279 calls, 147 companies returned people, only rows whose company domain matched the target kept -> 34 contacts at 21 companies).
5. Depth rule: 989 qualified companies = a mid-sized TAM, so up to 3 contacts per company: T1 (channel/dealer/co-op/rep owners) first, then T2 (marketing communications), T3 (marketing leaders) only if fewer than 2 T1/T2 exist.

## Result
- 2,041 companies: A 239, B 750, C 126, out 926.
- 1,385 leads at 727 of the 989 A+B companies (T1 541, T2 462, T3 382). **262 qualified companies (A 48-ish, B rest) have no contact yet.**
- Not run: AI Ark/EXA/ColdIQ gap-fill for those 262, deeper (non-core-title) people pulls, email enrichment.

## Known issues
- Legacy 2026-09-28 leads carried a bad `company_domain` for some rows (e.g. `ow.ly` for PSG); copied as-is.
- T1 title regex still has false positives; confirm before sending.
- Candidate set excludes qualified-looking companies that had no T1/T2 contact in the pulls, so the A/B universe is lower than the projection (~6,500) — those need a contact-first pull to find.
