# Query — 2026-11-04 leads expansion and HeyReach load (Render Stuck offer test)

**Segment:** expanding existing segment (`2026-10-30-leads.csv`). Config **`7166f187-d30d-4d52-86be-79ba8f4f3dbf`** (Industrial OEMs paying an outside render agency). **Why:** repo owner asked to "source more leads for this campaign but push them randomly into both" and "add as many as you can".
**Sourcing:** no new Blitz pull. The same raw Blitz people results (`POST /v2/search/people`, approved Slack titles, NA + Europe) were re-ranked with **minimum title score 65 (was 75) and up to 12 contacts per account (was 4)**, giving 807 contacts at 108 accounts. Removed 23 at accounts whose `render_copy_ready` is `review` (no recent named product, so "congratulations on {product}" cannot render) and 12 already in earlier VNTANA leads files. **772 loaded.**
**Load:** HeyReach `add_leads_to_list_v2` via 8 batches (<=100), custom fields `product`, `category`, `demo_link`. **Random split** (seeded shuffle, seed 20261104): 386 to Offer 1 list `1082187` (campaign `693232`), 386 to Offer 2 list `1082188` (campaign `693233`), each person in exactly one list. All 8 batches: added, 0 failed. List counts verified 386 / 386. Colleagues at the same account can land in different offers (82 of 98 accounts are split). The campaigns remain DRAFT and unstarted.
**Output:** `2026-11-04-leads-loaded.csv` (772 rows, `linkedin_url` first, `assigned_list` shows the list).

## Caveats found in a spot-check of 6 loaded leads
- HeyReach enriches the profile on import and **overwrites** position and company URL with live LinkedIn data, so some titles differ from Blitz's cached title (e.g. a loaded lead now reads "Senior Advisor, Brand Campaigns"). Titles/exclusions need re-checking on the loaded data.
- Some researched `category` values read oddly (e.g. "filter deck outlet" for MANN+HUMMEL "Nanoclass RTM Series"); the category goes straight into "a {category} built from CAD".
- Lower-score titles (65: product manager, operations manager, business development) are included at the owner's request for volume.
