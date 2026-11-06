# 2026-10-05 harvested unique companies (17,039)

- **What:** the pre-qualification union cited in the 2026-09-17 funnel ("27,333 raw records -> 17,039 unique companies").
- **Method:** no new API calls. Re-ran the first-pass dedupe of `merge.py` over saved raw files: Blitz `pool.json` (company search + jobs-enriched, 8,915 + EXA-enriched 486 = 9,401 records) plus AI Ark `ark_raw.jsonl` filtered to GB/IE HQ (17,932 records) = 27,333 raw. Key: canonical LinkedIn company URL, else domain, else name.
- **Result:** 17,039 unique rows — matches the funnel exactly.
- **Not included:** Prospeo and DiscoLike/ColdIQ records (added later; the full 29,096 pool is in the 2026-09-17 files), and the second-pass shared-domain collapse.
- **Caveats:** unqualified (includes non-payroll firms, competitors, non-ICP sizes: 12,279 are 1-10 staff); description is the source's `about` text; AI Ark rows carry no `specialties`.
- **TAM/SAM / contact depth:** none pulled.
