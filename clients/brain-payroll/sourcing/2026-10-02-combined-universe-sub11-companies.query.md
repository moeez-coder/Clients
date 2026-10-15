# 2026-10-02 sub-11 companies — query record

- **Client / config scope:** Brain Payroll UK Limited (`0a09f3c7-9a9b-4f57-bbec-e2fbf0dc6780`);
  all four sourcing configs (`a47f2b39-0aaf-48d4-a1e0-45909b305979`,
  `cb081b3d-9e0c-44ce-aa5e-364cc4d8a249`, `b790b5bd-eb5b-4e68-a807-5c674138dd1a`,
  `7806e67e-a2e9-4fff-91a3-5982cbde52b5`).
- **Segment status:** *expanding existing segments* — no new segment opened. This file is the
  complement of `2026-09-17-combined-universe-companies.csv`: the same four segments, minus the
  11+ headcount floor.
- **Requested by:** repo owner, in-session ("Remove the headcount filter and give me the list
  of those companies"), 2026-10-02.
- **Produced by:** no new API calls. The 29,096-company deduped pool from the 2026-09-17 harvest
  (six tools — see the 2026-09-17 query file) was re-run through the *identical* rule-based
  qualifier with exactly one change: the `size<11` rejection rule removed. Every other rule
  (GB/IE geography, foreign-ccTLD, DNC by domain and name, competitor identity, payroll-provider
  evidence, professional body, end-employer industry, recruiter, wealth manager) is unchanged.
- **Result:** 6,606 companies pass without the headcount rule = the 2,492 already delivered
  + **4,114 new**, all with 1–10 employees. Reconciles exactly: zero previously-qualified
  companies dropped, and 4,114 equals the count of rows in
  `2026-09-17-combined-universe-rejected.csv` whose *only* reason is `size<11`.
  This file holds the 4,114 only.
- **Breakdown:** accountancy-practice-payroll 3,765 / payroll-bureau 164 /
  umbrella-contractor-payroll 138 / recruitment-umbrella-contractor-payroll 47.
  GB 3,796 / IE 318. `icp_confidence`: high 618 / medium 3,496. `tier` = `micro-1-10`.
- **TAM/SAM read for contact depth:** removing the floor adds 4,114 to a segment already
  rated large-SAM (accountancy), so the existing inverse rule holds — 2 contacts per
  accountancy practice, 4 per bureau/umbrella — if these are ever taken to prospecting.
  No prospects have been pulled for them.

## Caveats

1. **Rule-based only.** These companies have *not* been through the Tier-1 website-evidence
   pass or the Tier-2 LLM adjudication that produced the QUALIFIED / LIKELY / DISQUALIFIED
   verdicts on the 2,492. Expect the same ~29% DISQUALIFIED rate or worse (micro firms are
   less likely to run a real payroll bureau). `icp_confidence: medium` rows are inferred
   from "accountant" identity, not verified payroll service.
2. **Employee counts are LinkedIn-derived** (`employees_on_linkedin`, mostly 1–5), so these
   are largely sole practitioners and micro practices.
3. **Not sent to Clay.** Nothing from this file has been pushed to either Clay webhook.
4. 90 rows have no LinkedIn URL and 775 have no domain on record (written as `-`); the
   rest of the key is `linkedin_url`, falling back to `domain`.
