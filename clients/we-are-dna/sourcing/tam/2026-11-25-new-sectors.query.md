# New-sector count for Doc 1 C3 (2026-11-25, count only, nothing pulled)

- **Client:** We Are DNA `f5ff426b-c514-4a64-91b0-0e141a6a0669`. Why: Moe chose "Count new sectors first" for getting C3 to +800. Session session_013MzxQfbTXPU4XS6uuyCtrr.
- **Tool:** Blitz API `POST /v2/search/companies`, `max_results: 1`, `total_results` (indicative only, CLAUDE.md). UK HQ. Script `2026-11-25-new-sectors-count.py`, output `2026-11-25-new-sectors-count.json`. Labels verbatim from `docs/blitz-api/company-search-industries.txt` (legacy + current).

| Sector (labels) | 51-200 | 201-500 | 501-1000 | 1001+ |
|---|---|---|---|---|
| Tech (Software Development, Computer Software, IT Services and IT Consulting, Information Technology and Services, Technology; Information and Internet, Internet) | 6,468 | 1,452 | 440 | 698 |
| Education (Education, Education Management, Education Administration Programs, E-Learning Providers, E-learning, Primary and Secondary Education, Higher Education, Professional Training and Coaching) | 7,568 | 2,274 | 1,013 | 1,363 |
| Consulting (Business Consulting and Services, Management Consulting) | 1,597 | 342 | 105 | 176 |

**Rough C3 yield** (201+ only), using the 2026-11-17 lookup's pass rate at the 3.8/3.6 bar (201-500 13.7%, 501-1000 21.0%, 1001+ 28.8%) and snapshot 3's C3 leads per company: Tech ≈ 230, Education ≈ 440 before removing public bodies (schools, universities, colleges are a large share and doc 1 excludes the public sector by default), Consulting ≈ 60 and a catch-all label (keyword gate required). Glassdoor lookup ≈ $0.10 per 1,000 companies (2026-11-17: $2.80 for 29,489), so all three at 201+ ≈ $1; with 51-200 ≈ $2.60.
**Caveat:** these are outside doc 1's five sectors; adding them changes doc 1's scope and needs new `sector_peers` wording.
