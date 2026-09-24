# Query — Consolidated target universe (2026-09-24)

**Purpose:** Single deduped CSV of all potential target companies across both Sensor Bio ICPs, per user follow-up request ("one consolidated CSV of all potential target companies").

**Source:** Merge of the two per-segment pulls made the same day:
- `sourcing/sensor-bio-clinical-health-systems-custom/2026-09-24-companies.csv` (1,000 rows)
- `sourcing/campaign-1-enterprise-platforms-casual-connections/2026-09-24-companies.csv` (1,000 rows)

Deduped by `company_linkedin_tag`. 55 companies appeared in both segment pulls (health systems large enough to also match the Enterprise & Platforms digital-health keyword filter) — these are kept once, with `icp_segments` listing both segment names (`|`-separated). Result: **1,945 unique companies**.

**Not yet applied:** the ICP qualifier/scoring step for either segment — this is still the raw pre-qualification universe, now just deduped and merged into one file rather than the qualification step itself.

**Caveat:** both source pulls are 1,000-company samples of their respective Blitz-reported TAMs (17,014 for Clinical & Health Systems, 4,305 for Enterprise & Platforms — see each segment's own `.query.md`), not the full enumeration. This consolidated file inherits that same limit.
