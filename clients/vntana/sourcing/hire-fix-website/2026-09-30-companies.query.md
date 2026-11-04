# Campaign 7 "The Hire Who Has to Fix the Website" — PREVIEW sourcing (2026-09-30)

**Client:** VNTANA (`5e0a22cf-6efb-432d-bc3c-6eb914440f13`) · **Campaign:** `tracking_clients` session `9ae9e746-06e6-4fb8-987f-47627806220a`
(HeyReach `628482`) · **Sourcing config:** "Industrial manufacturers advertising eCommerce, digital or digitization roles (last 60d)"
`bde2c03e-9c76-4770-85bf-a3526f0dd5d3` (draft, 0 companies in `tracking_clients` — **nothing was written back there**).
**New segment**, config-slug `hire-fix-website`. **Preview only — no leads pushed to HeyReach or Clay.**

Repo owner's instruction: *"cast as wide of a net as possible. So any job posting signal that we can find and barebones qualified
company. I want the persona from that company. Do a preview of this. Give me a count of the companies and the final prospects."*

## Result
| | Count |
|---|---|
| Hiring companies returned by all sources (worldwide, any industry) | 18,605 (`-hiring-companies-raw.csv`) |
| After geography + headcount + manufacturer + DNC | 814 (`-companies.csv`, all rows) |
| **Qualified (company check F/U and a genuine matching posting)** | **393** |
| …with a dated posting in the last 60 days | 380 |
| …with ≥1 persona contact found | 308 |
| **Persona prospects, all** | **3,034** — digital/eCommerce leaders 919 · CDOs 32 · marketing leaders 2,083 |
| Prospects capped at top 5 per company | 1,177 (`in_top5`) |
| Prospects capped at top 3 per company | 796 (`in_top3`) |

## Job-posting signal (wide net)
Title keyword groups (a posting matches if its title contains any, whole-word): **ecommerce** eCommerce, e-commerce, ecommerce,
E-Business, Webshop, Online Shop, Digital Commerce, Marketplace · **digital_exp** Digital Experience, Customer Experience Digital,
Web Experience, UX · **digital_lead** Head of/Director of/VP Digital, Chief Digital, Digital Director, Digital Transformation,
Digitalization/Digitalisation/Digitalisierung, Digital Strategy, Digital Product · **web_content** Website, Web Manager, Web Content,
Webmaster, Product Content, Content Manager, Digital Content · **pim_dam** PIM, Product Information, Product Data, Master Data Product,
DAM, Digital Asset, Catalog/Catalogue · **digital_marketing** Digital Marketing, Online Marketing, Marketing Technology, MarTech,
Performance Marketing, SEO. Excluded: intern/internship/Praktikum/Werkstudent/apprentice/trainee/stage/student titles.

Sources:
1. **Blitz `POST /v2/company/tam-by-jobs`** — `job.title.include` = each group, `job.date_posted.last_days: 60`,
   `company.is_agency: false`; run (a) per group × each of 36 manufacturing LinkedIn industries (232 calls, 2,071 rows) and
   (b) per group × job-location country for the 18 target countries with **no** industry filter (540 calls, 24,326 rows).
2. **Prospeo `POST /search-company`** (`X-KEY`) — `company_job_posting_hiring_for` (same keywords, `match_type: contains`) +
   `company_industry` (23 Prospeo industry names); 649 companies, 26 credits. Prospeo gives currently-open titles, **no dates**.
3. **Blitz `POST /v2/jobs/company`** per qualifying company (same titles, 60 days) → 1,940 dated postings (`-postings.csv`),
   used for `open_role` / date / URL.
Not used: ColdIQ/TheirStack (balance 1.72 credits, a search costs ≥5); EXA (reserved for replatform/agency/PLM boosters).
Blitz quirk: on `/v2/jobs/search` the company `industry`/`size`/`hq` filters return HTTP 500 — only `employee_count` and
`is_agency` work — so geography/size/industry are applied client-side.

## Barebones company qualification
HQ in US, CA or the 16 Western European countries · LinkedIn size band ≥ 201 · either IN in
`sourcing/icp-universe-na-weu/2026-09-29-companies.csv` or carrying a manufacturing LinkedIn industry and not hit by the exclusion
keywords · not on the campaign's 21-domain DNC list (removed: Bobcat) · **then a Haiku company check** (6 batches, text-only, spec
`sourcing/icp-universe-na-weu/2026-09-29-triage-spec-t3.md` plus "consumer/household/personal-care/tobacco/food/chemicals/pharma/
medical and equipment dealers are NO") because the universe's loose keyword rule had let in bioMérieux, Colgate-Palmolive, Reynolds
American, Essity and Caterpillar dealers. F 456 / U 115 / N 243; 5 "aftermarket/contract-manufacturer" NOs moved to U (wide net).
Finally 178 companies were dropped because none of their postings genuinely matched once titles were matched on whole words
(e.g. "UX" inside "commerciaux", "DAM" inside "Beaver Dam") or all matches were internships.
**No revenue filter was applied** (the brief's $100M+) — `prospeo_revenue_band` is filled only where Prospeo supplied it.

## Persona
Blitz `POST /v2/search/employee-finder` per company: `job_level` C-Team/VP/Director, `job_function` Advertising & Marketing,
Information Technology, Sales & Business Development, General Business & Management; up to 6 pages × 50 (1,822 calls, 65,291
unique people → `-senior-staff-raw.csv`). Current title taken from the current experience at that company. Persona tiers:
**1 digital/eCommerce leader** (VP/Head/Director/Chief/Lead + digital, eCommerce, e-business, online, web, omnichannel, CX,
digitalisation) · **2 CDO** · **3 marketing leader** (CMO, VP/Head/Director of Marketing — the brief's "VP Marketing where digital
reports into marketing"). Excluded titles: assistants, analytics/data, compliance, procurement/purchasing, VMO, HR/talent,
finance, legal, security/infrastructure, board/advisor/consultant. People located outside the 18 countries dropped.
Ranking inside a company: tier, then VP/C-level before Director. **TAM/SAM read:** ~400 companies is a small universe, so per the
inverse rule more contacts per company are justified — top 5 recommended (1,177), all 3,034 kept in the file.

## Known limitations
- "digital_lead"/"Digitalisierung" also catches factory-digitalisation roles (e.g. "Engineer Smart Factory / Digitalisierung
  Produktion") — real digital hiring, weaker fit to the website angle. `signal_group` lets you cut them.
- Tier 3 (marketing leaders) is 69% of prospects; at large groups it includes regional/brand marketing directors far from the web team.
- 85 qualified companies have no persona found by Blitz at Director+ in those functions — a Prospeo person search could fill them.
- Message 1 must use `open_role_clean`, not the lead's own `{{ title }}`; German/French titles are left in their original language.
- Phase 2 (contact whoever takes the job, 30 days in) is not built yet; `role_start_date` is captured on every lead for it.
