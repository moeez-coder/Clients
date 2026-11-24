# ClinicalTrials.gov Phase 3 sponsors (2026-11-19)

- **What:** industry-sponsored Phase 3 trials with at least one US site and a primary completion date from 2025-11-01 to 2027-06-30. These are companies close to a launch (Doc 2 Campaigns 1 to 5) and early warning of specialty moves (Campaign 6).
- **Client:** Health Link Dimensions, tracking_clients `8f80aeaa-1ca1-4b9a-9f27-756c2a5be696`. **Config:** none (`-`).
- **Why:** Moe asked whether the ClinicalTrials.gov scraping done for MeetLife / MX Life Sciences was relevant to HLD, then asked for the sponsor list in GTM Sheets (2026-11-19).
- **Source:** ClinicalTrials.gov API v2, `GET https://clinicaltrials.gov/api/v2/studies`, free, no key. Script: `ctgov_phase3.py`.
  - `filter.advanced = AREA[Phase]PHASE3 AND AREA[LeadSponsorClass]INDUSTRY AND AREA[LocationCountry]"United States" AND AREA[PrimaryCompletionDate]RANGE[2025-11-01,2027-06-30]`
  - Fields: NCTId, BriefTitle, LeadSponsorName, Phase, OverallStatus, PrimaryCompletionDate, CompletionDate, Condition, InterventionType, InterventionName, LastUpdatePostDate.
- **Result:** 898 trials (API `totalCount` 898), 384 distinct lead sponsors, 365 with a drug or biologic intervention.
  - `2026-11-19-ctgov-phase3-trials.csv`: one row per trial.
  - `2026-11-19-ctgov-phase3-sponsors-companies.csv`: one row per sponsor (trial count, next and last primary completion, sample conditions and interventions, NCT IDs).
- **DNC / clients:** flagged, not removed, in `dnc_or_client` (matcher `dnc.py`). 14 sponsors flagged: AstraZeneca, AbbVie, Incyte, Takeda, Gilead, Alexion, Ionis, Octapharma, Apellis, Bausch Health, Bracco, Harrow, IDEAYA, Revolution Medicines.
- **GTM Sheets:** workbook "ClinicalTrials.gov Phase 3 sponsors (2026-11-19)" (`4fbb1975-fb05-4e26-8b2f-919e8c6707b8`) in the client folder, table "Phase 3 sponsors" (`0fe38b7c-6f24-4f6d-b390-5bd6de86934b`, webhook table, 384 rows posted from the sponsors CSV, with one field column per CSV column).
- **Caveats:**
  - Lead sponsor names are as registered (for example "Hoffmann-La Roche", "Merck Sharp & Dohme LLC"). They need mapping to LinkedIn company pages before people searches.
  - Some sponsors are non-US companies with US sites, and a few are consumer, device or animal-health companies (for example Colgate Palmolive). Filter on `drug_or_biologic = yes` and check US commercial presence before outreach.
  - Primary completion dates are the sponsor's estimate and slip often.
- **Cost:** free.
