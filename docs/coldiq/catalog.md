# ColdIQ API gateway - full catalog

Generated 2026-09-30 from the live OpenAPI spec `GET https://api.coldiq.com/openapi.json` (ColdIQ API v0.1.0, OpenAPI 3.0.0): **705 paths / 820 operations / 45 declared tags**. Interactive docs: https://api.coldiq.com/docs. Provider list cross-checked against https://coldiq.com/marketplace/apis (45 entries, identical to the 45 tags the spec declares; operations also use 6 undeclared admin tags - Account, Public, Dashboard, Chats, Connections, Mailboxes - for 51 in use).

**Source key:** everything below (endpoints, params, costs, vendor doc URLs) is read from the spec unless marked *(inferred)*. Categories and the relevance notes are my own classification.

## Essentials

- Base URL `https://api.coldiq.com`, header `Authorization: Bearer $COLDIQ_API_KEY`. **Send a User-Agent**: default `Python-urllib` is blocked at Cloudflare with a bare 403 (spec note).
- Rate limit (per billing account, shared by all keys): 120 req/min, 3000 req/h; a batched verb call (`inputs[]`, <=50 rows) counts as 1. 429 carries `Retry-After`.
- **Free balance check:** `GET /v1/me/credits` -> `balance`, `usedThisMonth`, `usd_per_credit`, `credit_rate_plan`, `billing_scope`. Checked 2026-09-30: **balance 1.72 credits, 23,703 used this month**, usd_per_credit = **0.0142857 ($1 = 70 credits)**. Balance is effectively empty; any paid call will 402.
- `/dashboard/*` routes (credits, quota, usage, API keys, team, connections) need a dashboard session JWT - the API key gets `401 Malformed session token`. `/public/billing/*` needs no auth (price lists).
- Credit packs (from `GET /public/billing/products`): PAYG $100 = 6,000 cr ... $2,000 = 135,000 cr; subscriptions Starter $99/mo = 7,000 cr, Pro $199/mo = 15,000, Scale $499/mo = 40,000.
- Cost shapes (`x-credits-cost`): `per_call` = flat per request even if nothing returns; `per_result`; `per_page` (N rows per charge); `per_call_variable`; `query_plus_record`. Actual charge returned in `X-ColdIQ-Credits-Charged` header.
- **Correction to prior assumption:** `POST /v1/apollo/people/search` is **not free** - spec prices it at **9.91 credits per call** (flat, ~$0.14), results obfuscated. Earlier "free preview" test calls were most likely billed.
- Many per-provider endpoints say "Managed alternative: POST /v1/<verb>" - the GTM verb runs that provider in a waterfall with charge-on-success billing.

## Summary by category

| Category | Providers | Operations |
|---|---|---|
| Managed GTM verbs (ColdIQ waterfall over many providers) | GTM Verbs | 24 |
| People & company search / B2B databases | AI Ark, Prospeo, Apollo, Lima Data, DiscoLike, LinkUp API, Sumble, Wiza, Openmart | 130 |
| LinkedIn scraping & engagement extraction | HarvestAPI, LeadsFactory, Jungler | 36 |
| Email / phone finding & verification | FullEnrich, Findymail, Icypeas, LeadMagic, BounceBan | 82 |
| Signals, intent, technographics & job postings | PredictLeads, Signalbase, TheirStack, BuiltWith, LinkedIn Jobs API, Career Site Jobs | 45 |
| Ad intelligence | Adyntel, LinkedIn Ad Library, Meta Ads Library, Google Ads, Twitter Ads Scraper | 16 |
| Web search, crawling & SEO | Exa, Jina, Serper, DataForSEO | 64 |
| Social / web / local scraping | Twitter, Reddit, Google Maps, Influencers Club | 13 |
| Outreach, sequencing & messaging (BYOK) | Instantly, Lemlist, Unipile | 245 |
| CRM (BYOK) | Attio | 22 |
| ColdIQ-native products | Visitor ID, ColdIQ Mailbox, Mailboxes | 80 |
| Account, billing & workspace admin | Account, Public, Dashboard, Team, Slack, Connections, Chats | 63 |

## Top picks for LinkedIn-first sourcing

| Rank | Tool | Endpoint(s) | Cost (credits; x $0.0143) | Why |
|---|---|---|---|---|
| 1 | GTM verb Find People | `POST /v1/people/search` | charge-on-success; routed provider rate; `max_credits` cap | One normalized schema (100+ filters incl. company_linkedin_urls, titles, seniorities, headcount, industries, max_per_company); routable providers: AI Ark, LeadMagic, Findymail, Prospeo, LinkUp, Apollo, FullEnrich, Lima Data (the default auto waterfall order is not stated in the spec); 50 rows/request |
| 2 | GTM verb Search Companies | `POST /v1/companies/search` | charge-on-success | Firmographic / tech / funding / hiring / lookalike (`similar_to_domains` -> DiscoLike) account lists; `linkedin_search_url` input |
| 3 | LeadsFactory | `POST /v1/leadsfactory/contact-finder/searches`, `POST /v1/leadsfactory/sn-scraper/jobs` (+ GET status, free) | 0.35/contact, 0.35/profile | Titles across a company list, and Sales Navigator search-URL scraping on ColdIQ's shared SN seat - cheapest LinkedIn URL per row |
| 4 | HarvestAPI | `GET /v1/harvestapi/linkedin/lead-search`, `/account-search`, `/profile-search`, `/company-search`, `/profile`, `/company` | 16.8/25 SN leads; 0.67/10 profiles; 0.67/50 companies; 0.67-1.07/profile | Live LinkedIn + Sales Navigator search without an account |
| 5 | AI Ark | `POST /v1/ai-ark/people`, `POST /v1/ai-ark/companies` | 1.03/returned person; 0.21/returned company | Large DB, LinkedIn URLs, cheap per row |
| 6 | Lima Data (database) | `POST /v1/limadata/database/search-people`, `/search-employees`, `/search-companies`; `POST /v1/limadata/find/company-linkedin` | 0.35/result; 3.5/call | Very cheap per row; company LinkedIn finder |
| 7 | Prospeo | `POST /v1/prospeo/search-person`, `/search-company`, `/enrich-person` | 3.5/call | 30+ filters, enrich by LinkedIn URL |
| 8 | Icypeas | `POST /v1/icypeas/find-people`, `/find-companies`, `/url-search/profile(s)`, `/url-search/company(ies)` | 1.05/result or call | Cheap people/company search and name->LinkedIn URL resolution |
| 9 | Jungler / Lima Data posts | `POST /v1/jungler/workbooks`; `POST /v1/limadata/posts/reactions` | 35/task; 7/reaction | LinkedIn post engagers as intent lists |
| 10 | Sumble / LinkUp | `POST /v1/sumble/people/find`; `POST /v1/linkupapi/data/search/profiles` | 2.1/result; 6.3/10 results | Role-at-org and LinkedIn profile search alternatives |

Signals worth pairing (why-now): PredictLeads (`/v1/predictleads/discover/job_openings`, `/discover/financing_events`), Signalbase (`/v1/signalbase/*-signals`), TheirStack, LinkedIn Jobs API, Career Site Jobs, or the verb `POST /v1/signals/find`.

## GTM verbs - routing slugs *(read from each verb's `provider` field description)*

- `POST /v1/email/find` - Find Email - providers: "findymail", "prospeo", "leadmagic", "limadata-work-email", "apollo-people-match", "wiza"
- `POST /v1/email/verify` - Verify Email - providers: "bounceban", "leadmagic", "findymail", "instantly", "linkupapi-validate"
- `POST /v1/phone/find` - Find Phone - providers: "prospeo", "ai-ark", "leadmagic", "limadata"
- `POST /v1/person/enrich` - Enrich Person - providers: "harvestapi", "limadata-person", "prospeo-enrich-person", "leadmagic-profile-search", "findymail-business-profile", "linkupapi-profile-enrich", "ai-ark-reverse-lookup", "apollo-people-match", "leadmagic-b2b-profile"
- `POST /v1/company/enrich` - Enrich Company - providers: "limadata", "apollo", "prospeo", "openmart", "findymail", "icypeas", "discolike", "fullenrich-company", "leadmagic-company", "wiza", "builtwith", "linkupapi-by-url"
- `POST /v1/people/search` - Find People - providers: "ai-ark-people", "leadmagic", "findymail-search-employees", "prospeo-search-person", "linkupapi-search-profiles", "apollo", "fullenrich-people-search", "limadata-prospect-employees", "limadata-prospect-employees-batch"
- `POST /v1/companies/search` - Search Companies - providers: "fullenrich", "theirstack", "signalbase", "limadata", "predictleads", "sumble", "linkupapi-search", "linkupapi-fundraising", "linkupapi-hiring", "prospeo-search-company", "ai-ark-companies", "apollo", "limadata-prospect-filter", "limadata-prospect-url", "discolike"
- `POST /v1/signals/find` - Find Signals - providers: "signalbase-funding", "signalbase-acquisition", "theirstack-hiring", "signalbase-hiring", "signalbase-job-change", "theirstack-intent-discovery", "theirstack-buying-intents", "predictleads-financing", "predictleads-news", "predictleads-startup-posts"
- `POST /v1/ads/search` - Search Ads - providers: "adyntel_google", "adyntel_linkedin", "adyntel_meta", "google_ads", "linkedin_ad_library", "meta_ads", "twitter_ads"
- `POST /v1/web/search` - Web Search - providers: "serper", "limadata", "exa", "jina"
- `POST /v1/web/fetch` - Fetch Page Content - providers: "exa-contents"
- `POST /v1/jobs/search` - Search Jobs - providers: "career_site_jobs", "linkedin_jobs_api", "theirstack-jobs"
- `POST /v1/places/search` - Search Places - providers: "openmart", "google_maps"
- `POST /v1/places/reviews` - Get Place Reviews - providers: "google_maps_reviews"
- `POST /v1/influencers/find` - Find Influencers - providers: "influencers_similar", "influencers_discovery"
- `POST /v1/reddit/search` - Search Reddit - providers: "reddit"
- `POST /v1/seo/search` - Search SEO - providers: "kw_search_volume", "kw_trends", "serp_google", "serp_bing", "serp_youtube", "bl_summary", "bl_backlinks", "bl_referring", "domain_tech", "domain_whois", "labs_rank_overview", "labs_ranked_kw", "labs_competitors", "labs_kw_ideas", "page_lighthouse", "page_content"
- `POST /v1/email/verify/bulk/submit` - Bulk Verify Emails
- `POST /v1/email/find/bulk/submit` - Bulk Find Emails
- `POST /v1/person/enrich/bulk/submit` - Bulk Enrich People
- `POST /v1/company/enrich/bulk/submit` - Bulk Enrich Companies
- `POST /v1/phone/find/bulk/submit` - Bulk Find Phones
- `POST /v1/jobs/{job_id}/results` - Get Bulk Job Results
- `POST /v1/jobs/{job_id}/cancel` - Cancel Bulk Job

## Managed GTM verbs (ColdIQ waterfall over many providers)

### GTM Verbs

- **What:** Provider-agnostic GTM verbs — one call (find an email, enrich a company) routed across the best provider via a managed waterfall. Pin a vendor or supply an ordered chain with `provider`; charged only on a usable result.
- **Docs:** vendor https://coldiq.com | ColdIQ https://coldiq.com/marketplace/apis/gtm-verbs | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** HIGH. /v1/people/search and /v1/companies/search are provider-agnostic waterfalls (AI Ark, Prospeo, Apollo, LinkUp, Lima Data, DiscoLike, etc.) with charge-on-success billing, max_credits caps and 50-row batching; /v1/person/enrich resolves a person to a LinkedIn profile. Best default entry point.
- **Endpoints (24):**

  - `POST /v1/email/find` - Find Email - params: `input.id`, `input.first_name`, `input.last_name`, `input.full_name`, `input.domain`, `input.company_name`, `input.linkedin_url`, `inputs`, `provider`, `max_credits` (+2)
  - `POST /v1/email/verify` - Verify Email - params: `input.email`, `inputs`, `provider`, `max_credits`, `soft_miss`
  - `POST /v1/phone/find` - Find Phone - params: `input.id`, `input.first_name`, `input.last_name`, `input.full_name`, `input.domain`, `input.company_name`, `input.linkedin_url`, `inputs`, `provider`, `max_credits` (+1)
  - `POST /v1/person/enrich` - Enrich Person - params: `input.email`, `input.linkedin_url`, `input.first_name`, `input.last_name`, `input.full_name`, `input.company_name`, `input.domain`, `input.phone`, `inputs`, `provider` (+2)
  - `POST /v1/company/enrich` - Enrich Company - params: `input.domain`, `input.name`, `input.company_name`, `input.linkedin_url`, `inputs`, `provider`, `max_credits`, `soft_miss`
  - `POST /v1/people/search` - Find People - params: `input.job_titles`, `input.title_mode`, `input.title_scope`, `input.exclude_job_titles`, `input.seniorities`, `input.exclude_seniorities`, `input.departments`, `input.skills`, `input.keywords`, `input.keyword_mode` (+95)
  - `POST /v1/companies/search` - Search Companies - params: `input.keywords`, `input.keyword_match`, `input.keyword_mode`, `input.keyword_sources`, `input.exclude_keywords`, `input.products_services`, `input.exclude_products_services`, `input.products_services_mode`, `input.industries`, `input.industries_mode` (+60)
  - `POST /v1/signals/find` - Find Signals - params: `input.signal_type`, `input.companies`, `input.domains`, `input.since`, `input.industries`, `input.countries`, `input.round_type`, `input.topics`, `input.limit`, `inputs` (+3)
  - `POST /v1/ads/search` - Search Ads - params: `input.query`, `input.domains`, `input.advertiser_ids`, `input.search_urls`, `input.country`, `input.max_results`, `input.ad_type`, `input.start_date`, `input.end_date`, `input.platform` (+4)
  - `POST /v1/web/search` - Web Search - params: `input.query`, `input.num_results`, `input.country`, `input.search_type`, `inputs`, `provider`, `max_credits`, `soft_miss`
  - `POST /v1/web/fetch` - Fetch Page Content - params: `input.urls`, `input.include_text`, `input.include_summary`, `inputs`, `provider`, `max_credits`, `soft_miss`
  - `POST /v1/jobs/search` - Search Jobs - params: `input.title_keywords`, `input.exclude_title_keywords`, `input.locations`, `input.exclude_locations`, `input.description_keywords`, `input.exclude_description_keywords`, `input.companies`, `input.exclude_companies`, `input.remote`, `input.exclude_agencies` (+26)
  - `POST /v1/places/search` - Search Places - params: `input.query`, `input.country`, `input.city`, `input.limit`, `input.state`, `input.zip_code`, `input.lat`, `input.long`, `input.geo_radius`, `input.tags` (+21)
  - `POST /v1/places/reviews` - Get Place Reviews - params: `input.place_urls`, `input.max_reviews`, `input.sort`, `input.language`, `inputs`, `provider`, `max_credits`, `soft_miss`
  - `POST /v1/influencers/find` - Find Influencers - params: `input.platform`, `input.limit`, `input.page`, `input.sort_by`, `input.sort_order`, `input.ai_search`, `input.location`, `input.gender`, `input.type`, `input.handle` (+4)
  - `POST /v1/reddit/search` - Search Reddit - params: `input.start_urls`, `input.query`, `input.search_type`, `input.search_community_name`, `input.sort`, `input.time`, `input.limit`, `input.max_comments`, `input.include_comments`, `input.post_date_limit` (+5)
  - `POST /v1/seo/search` - Search SEO - params: `input.category`, `input.target`, `input.keyword`, `input.keywords`, `input.location`, `input.language`, `input.limit`, `input.date_from`, `input.date_to`, `input.time_range` (+12)
  - `POST /v1/email/verify/bulk/submit` - Bulk Verify Emails - params: `emails`, `use_providers`, `webhook_url`
  - `POST /v1/email/find/bulk/submit` - Bulk Find Emails - params: `people`, `resolve_current_employer`, `max_credits`, `webhook_url`
  - `POST /v1/person/enrich/bulk/submit` - Bulk Enrich People - params: `inputs`, `max_credits`, `webhook_url`
  - `POST /v1/company/enrich/bulk/submit` - Bulk Enrich Companies - params: `inputs`, `max_credits`, `webhook_url`
  - `POST /v1/phone/find/bulk/submit` - Bulk Find Phones - params: `inputs`, `max_credits`, `webhook_url`
  - `POST /v1/jobs/{job_id}/results` - Get Bulk Job Results - params: `job_id`, `cursor`, `limit`
  - `POST /v1/jobs/{job_id}/cancel` - Cancel Bulk Job - params: `job_id`

## People & company search / B2B databases

### AI Ark

- **What:** B2B people & company intelligence — search 500M+ people and 70M+ companies, find emails, look up mobile phones, and export enriched profiles with verified contact data
- **Docs:** vendor https://docs.ai-ark.com/ | ColdIQ https://coldiq.com/marketplace/apis/ai-ark | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x6; 2.06 cr/found email (per_result) x2; 0 cr/call (per_call), 25 rows/call x2; 0 cr/call (per_call), 10 rows/call x2 ...
- **Relevance (LinkedIn-first sourcing):** HIGH. Cheapest large people/company DB here (people 1.03 cr/returned person, companies 0.21 cr/returned company); returns LinkedIn URLs. Same vendor the repo already calls directly.
- **Endpoints (19):**

  - `POST /v1/ai-ark/companies` - Company Search API - **0.21 cr/returned company (per_result)** - params: `lookalikeDomains`, `account`, `lists`, `page`, `size`
  - `POST /v1/ai-ark/lists` - Save List - **0 cr/call (per_call)** - params: `id`, `type`, `values`, `mode`
  - `POST /v1/ai-ark/people` - People Search API - **1.03 cr/returned person (per_result)** - params: `account`, `contact`, `lists`, `page`, `size`, `max_per_account`
  - `POST /v1/ai-ark/people/reverse-lookup` - Reverse People Lookup API - **1.03 cr/request (per_call)** - params: `search`
  - `POST /v1/ai-ark/people/mobile-phone-finder` - Mobile Phone Finder API - **10.29 cr/found phone number (per_result)** - params: `linkedin`, `domain`, `name`
  - `POST /v1/ai-ark/people/export/single` - Export Single Person with Email - **2.06 cr/found email (per_result)** - params: `id`, `url`
  - `POST /v1/ai-ark/people/preview` - People Preview - **2.06 cr/page (per_result)** - params: `account`, `contact`, `lists`, `page`, `size`
  - `POST /v1/ai-ark/people/analysis` - Personality Analysis API - **8.23 cr/request (per_call)** - params: `url`, `id`
  - `GET /v1/ai-ark/credits` - Fetch Your Credit - **0 cr/call (per_call)**
  - `GET /v1/ai-ark/people/export/submissions` - Export People Submissions - **0 cr/call (per_call), 25 rows/call** - params: `state`, `fullyRefunded`, `page`, `size`
  - `GET /v1/ai-ark/people/export/{trackId}/statistics` - Export People Statistics - **0 cr/call (per_call)** - params: `trackId`
  - `PATCH /v1/ai-ark/people/export/{trackId}/notify` - Resend Export People Webhook - **0 cr/call (per_call)** - params: `trackId`
  - `GET /v1/ai-ark/people/email-finder/submissions` - Email Finder Submissions - **0 cr/call (per_call), 25 rows/call** - params: `state`, `fullyRefunded`, `page`, `size`
  - `GET /v1/ai-ark/people/email-finder/{trackId}/statistics` - Email Finder Statistics - **0 cr/call (per_call)** - params: `trackId`
  - `PATCH /v1/ai-ark/people/email-finder/{trackId}/notify` - Resend Email Finder Webhook - **0 cr/call (per_call)** - params: `trackId`
  - `POST /v1/ai-ark/people/export` - Export People with Email - **profile=1.03, verified_email=1.03 cr/exported profile + verified email (per_result)** - params: `account`, `contact`, `page`, `size`, `webhook`
  - `POST /v1/ai-ark/people/email-finder` - Find Emails by Track ID - **2.06 cr/found email (per_result)** - params: `trackId`, `webhook`
  - `GET /v1/ai-ark/people/export/{trackId}` - Get Export People Results - **0 cr/call (per_call), 10 rows/call** - params: `trackId`, `page`, `size`
  - `GET /v1/ai-ark/people/email-finder/{trackId}` - Get Email Finder Results - **0 cr/call (per_call), 10 rows/call** - params: `trackId`, `page`, `size`

### Prospeo

- **What:** Person and company enrichment and search — enrich by LinkedIn URL, email, or name; search with 30+ filters
- **Docs:** vendor https://prospeo.io/api-docs | ColdIQ https://coldiq.com/marketplace/apis/prospeo | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 3.5 cr/call (per_call) x3; standard=3.5, mobile=35 cr/call (per_call_variable) x1; standard=3.5, mobile=35 cr/record (per_result) x1; 3.5 cr/record (per_result) x1
- **Relevance (LinkedIn-first sourcing):** HIGH. Person/company search with 30+ filters at 3.5 cr/call; enrich by LinkedIn URL. Same vendor already used directly by the repo.
- **Endpoints (6):**

  - `POST /v1/prospeo/enrich-person` - Enrich Person - **standard=3.5, mobile=35 cr/call (per_call_variable)** - params: `data`, `only_verified_email`, `enrich_mobile`, `only_verified_mobile`
  - `POST /v1/prospeo/bulk-enrich-person` - Bulk Enrich Person - **standard=3.5, mobile=35 cr/record (per_result)** - params: `data`, `only_verified_email`, `enrich_mobile`, `only_verified_mobile`
  - `POST /v1/prospeo/search-person` - Search Person - **3.5 cr/call (per_call)** - params: `filters`, `page`
  - `POST /v1/prospeo/enrich-company` - Enrich Company - **3.5 cr/call (per_call)** - params: `data`
  - `POST /v1/prospeo/bulk-enrich-company` - Bulk Enrich Company - **3.5 cr/record (per_result)** - params: `data`
  - `POST /v1/prospeo/search-company` - Search Company - **3.5 cr/call (per_call)** - params: `filters`, `page`

### Apollo

- **What:** B2B contact & company database with CRM features
- **Docs:** vendor https://docs.apollo.io/reference | ColdIQ https://coldiq.com/marketplace/apis/apollo | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 9.91 cr/call (per_call) x5; 9.91 cr/person (per_result) x1; 9.91 cr/org (per_result) x1
- **Relevance (LinkedIn-first sourcing):** MEDIUM. People/org search at 9.91 cr per CALL (flat, not per row) - results are obfuscated (last names hidden) unless revealed; LinkedIn URLs available on match/enrich. Pricier per useful row than AI Ark/Prospeo.
- **Endpoints (7):**

  - `POST /v1/apollo/people/match` - People Enrichment - **9.91 cr/call (per_call)** - params: `first_name`, `last_name`, `name`, `email`, `hashed_email`, `organization_name`, `domain`, `id`, `linkedin_url`, `reveal_personal_emails` (+2)
  - `POST /v1/apollo/people/bulk-match` - Bulk People Enrichment - **9.91 cr/person (per_result)** - params: `details`, `reveal_personal_emails`, `reveal_phone_number`, `webhook_url`
  - `POST /v1/apollo/organizations/enrich` - Organization Enrichment - **9.91 cr/call (per_call)** - params: `domain`
  - `POST /v1/apollo/organizations/bulk-enrich` - Bulk Organization Enrichment - **9.91 cr/org (per_result)** - params: `domains`
  - `POST /v1/apollo/people/search` - People API Search - **9.91 cr/call (per_call)** - params: `q_keywords`, `person_titles`, `person_not_titles`, `include_similar_titles`, `person_seniorities`, `q_organization_domains`, `organization_ids`, `organization_num_employees_ranges`, `person_locations`, `organization_locations` (+11)
  - `POST /v1/apollo/organizations/search` - Organization Search - **9.91 cr/call (per_call)** - params: `q_keywords`, `q_organization_name`, `organization_ids`, `organization_num_employees_ranges`, `organization_locations`, `organization_not_locations`, `q_organization_keyword_tags`, `organization_not_keyword_tags`, `revenue_range`, `currently_using_any_of_technology_uids` (+10)
  - `POST /v1/apollo/organizations/info` - Get Complete Organization Info - **9.91 cr/call (per_call)** - params: `organization_id`

### Lima Data

- **What:** Company and people data intelligence platform
- **Docs:** vendor https://limadata.com | ColdIQ https://coldiq.com/marketplace/apis/lima-data | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 3.5 cr/call (per_call) x9; 0 cr/call (per_call) x8; 7 cr/call (per_call) x6; 87.5 cr/call (per_call) x5 ...
- **Relevance (LinkedIn-first sourcing):** MEDIUM-HIGH. Database search-people/search-companies/search-employees at 0.35 cr/result is very cheap; the "prospect" (LinkedIn/Sales-Nav-style) endpoints are expensive (87.5 cr/call). Has company-linkedin finder (3.5 cr).
- **Endpoints (52):**

  - `POST /v1/limadata/enrich/person` - Enrich Person
  - `POST /v1/limadata/enrich/company` - Enrich Company
  - `POST /v1/limadata/person` - Person
  - `POST /v1/limadata/company` - Company
  - `POST /v1/limadata/company/insights` - Company Insights
  - `POST /v1/limadata/database/autocomplete` - Database Autocomplete
  - `POST /v1/limadata/database/search-companies` - Database Search Companies
  - `POST /v1/limadata/database/search-people` - Database Search People
  - `POST /v1/limadata/database/search-employees` - Database Search Employees
  - `POST /v1/limadata/company/workplace-benefits` - Workplace Benefits
  - `POST /v1/limadata/company/workplace-ratings` - Workplace Ratings
  - `POST /v1/limadata/find/hashed-email` - Hashed Email
  - `POST /v1/limadata/find/personal-email` - Personal Email
  - `POST /v1/limadata/find/email-verification` - Email Verification
  - `POST /v1/limadata/find/work-email` - Work Email
  - `POST /v1/limadata/find/work-email-linkedin` - Work Email from LinkedIn
  - `POST /v1/limadata/find/company-linkedin` - Company LinkedIn
  - `POST /v1/limadata/find/phone` - Phone Number
  - `POST /v1/limadata/find/identity-resolution` - Identity Resolution
  - `POST /v1/limadata/find/reverse-email-lookup` - Reverse Email Lookup
  - `POST /v1/limadata/find/glassdoor-company` - Company Glassdoor ID
  - `POST /v1/limadata/jobs` - Company Jobs
  - `POST /v1/limadata/jobs/details` - Job Details
  - `POST /v1/limadata/posts` - Posts
  - `POST /v1/limadata/posts/comments` - Post Comments
  - `POST /v1/limadata/posts/reactions` - Post Reactions
  - `POST /v1/limadata/search/people` - Search People
  - `POST /v1/limadata/search/companies` - Search Companies
  - `POST /v1/limadata/search/jobs` - Search Jobs
  - `POST /v1/limadata/search/posts` - Search Posts
  - `POST /v1/limadata/search/web` - Web Search
  - `POST /v1/limadata/research/ai-search` - AI Search
  - `POST /v1/limadata/research/extract` - Extract
  - `POST /v1/limadata/references/autocomplete` - Autocomplete
  - `POST /v1/limadata/prospect/people/search-url` - Prospect People by URL
  - `POST /v1/limadata/prospect/people/filter` - Prospect People
  - `POST /v1/limadata/prospect/employees` - Prospect Employees
  - `POST /v1/limadata/prospect/employees/batch` - Prospect Employees (batch)
  - `POST /v1/limadata/prospect/companies/filter` - Prospect Companies
  - `POST /v1/limadata/prospect/companies/search-url` - Prospect Companies by URL
  - `POST /v1/limadata/batch/people` - Batch People Profiles
  - `POST /v1/limadata/batch/companies` - Batch Company Profiles
  - `POST /v1/limadata/batch/prospect-people` - Batch Prospect People
  - `POST /v1/limadata/batch/prospect-companies` - Batch Prospect Companies
  - `POST /v1/limadata/batch/post-engagements` - Batch Post Engagements
  - `POST /v1/limadata/batch/list` - Batch Operations List
  - `POST /v1/limadata/batch/results` - Batch Operation Results
  - `POST /v1/limadata/watch` - Create a Watch
  - `POST /v1/limadata/watch/list` - List Watches
  - `POST /v1/limadata/watch/get` - Get Watch by ID
  - `POST /v1/limadata/watch/update` - Update Watch
  - `POST /v1/limadata/watch/mock-payload` - Mock Webhook Payload
  - *(parameters omitted here for this large provider; see catalog.json)*

### DiscoLike

- **What:** Company discovery & B2B contacts — lookalike domain search, natural-language ICP matching, firmographics, and contact enrichment across 70M+ companies
- **Docs:** vendor https://docs.discolike.com/ | ColdIQ https://coldiq.com/marketplace/apis/discolike | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 42 cr/call (per_call) x4; query=37.8, record=0.74 cr/query + record (query_plus_record) x3; 38.5 cr/call (per_call) x2
- **Relevance (LinkedIn-first sourcing):** MEDIUM. Lookalike-domain company discovery (TAM from seed domains) - company-level; 37.8 cr/query + 0.74 cr/record. Same vendor used by listbuild directly (currently overdrawn there - via ColdIQ it bills ColdIQ credits instead).
- **Endpoints (9):**

  - `GET /v1/discolike/discover` - Discover similar businesses - **query=37.8, record=0.74 cr/query + record (query_plus_record)** - params: `domain`, `negate_domain`, `icp_text`, `negate_icp_text`, `exclude_domain`, `country`, `negate_country`, `state`, `negate_state`, `category` (+19)
  - `GET /v1/discolike/count` - Count matching businesses - **38.5 cr/call (per_call)** - params: `country`, `negate_country`, `state`, `negate_state`, `category`, `negate_category`, `employee_range`, `revenue_range`, `business_model`, `negate_business_model` (+9)
  - `GET /v1/discolike/bizdata` - Get business firmographic data - **42 cr/call (per_call)** - params: `domain`
  - `GET /v1/discolike/score` - Get digital footprint score breakdown - **42 cr/call (per_call)** - params: `domain`
  - `GET /v1/discolike/growth` - Get company growth metrics - **42 cr/call (per_call)** - params: `domain`
  - `POST /v1/discolike/contacts/discover` - Discover contacts grouped by domain - **query=37.8, record=0.74 cr/query + record (query_plus_record)** - params: `icp_prompt`, `icp_text`, `domain`, `title`, `negate_title`, `seniority`, `department`, `person_country`, `filter_industry`, `filter_country` (+11)
  - `GET /v1/discolike/contacts/count` - Count Contacts - **38.5 cr/call (per_call)** - params: `icp_text`, `domain`, `title`, `negate_title`, `seniority`, `department`, `person_country`, `has_email`, `has_phone`, `has_linkedin`
  - `GET /v1/discolike/contacts/lookup` - Lookup Contact - **42 cr/call (per_call)** - params: `persona_id`, `linkedin`
  - `GET /v1/discolike/contacts/match` - Contact Match - **query=37.8, record=0.74 cr/query + record (query_plus_record)** - params: `name`, `company_name`, `domain`, `person_country`, `limit`

### LinkUp API

- **What:** B2B data intelligence — person & company enrichment, email finder & validation, reverse email lookup, and intent signals (funded companies, hiring companies)
- **Docs:** vendor https://docs.linkupapi.com/api-reference/introduction | ColdIQ https://coldiq.com/marketplace/apis/linkup-api | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 6.3 cr/call (per_call) x6; 6.3 cr/10 results (per_page), 10 rows/call x4
- **Relevance (LinkedIn-first sourcing):** MEDIUM. LinkedIn-profile/company search at 6.3 cr per 10 results, plus funded/hiring-company lists.
- **Endpoints (10):**

  - `POST /v1/linkupapi/data/profil/enrich` - Profile Enrichment - **6.3 cr/call (per_call)** - params: `first_name`, `last_name`, `company_name`
  - `POST /v1/linkupapi/data/search/profiles` - Search Profiles - **6.3 cr/10 results (per_page), 10 rows/call** - params: `keyword`, `job_title`, `industry`, `school`, `location`, `current_company`, `total_results`
  - `POST /v1/linkupapi/data/company/info` - Company Info - **6.3 cr/call (per_call)** - params: `company_url`
  - `POST /v1/linkupapi/data/company/info-by-domain` - Company Info By Domain - **6.3 cr/call (per_call)** - params: `domain`
  - `POST /v1/linkupapi/data/search/companies` - Company Search - **6.3 cr/10 results (per_page), 10 rows/call** - params: `keyword`, `industry`, `location`, `employee_range`, `founding_company`, `total_results`
  - `POST /v1/linkupapi/data/mail/finder` - Email Finder - **6.3 cr/call (per_call)** - params: `linkedin_url`, `first_name`, `last_name`, `company_domain`, `company_name`
  - `POST /v1/linkupapi/data/mail/reverse` - Email Reverse - **6.3 cr/call (per_call)** - params: `email`
  - `POST /v1/linkupapi/data/mail/validate` - Email Validation - **6.3 cr/call (per_call)** - params: `email`
  - `POST /v1/linkupapi/data/fundraising-companies` - Fundraising Companies - **6.3 cr/10 results (per_page), 10 rows/call** - params: `keyword`, `funding_stage`, `min_funding_amount`, `max_funding_amount`, `industry`, `location`, `date_range`, `investor_name`, `employee_range`, `enrich` (+1)
  - `POST /v1/linkupapi/data/hiring-companies` - Hiring Companies - **6.3 cr/10 results (per_page), 10 rows/call** - params: `job_title`, `industry`, `location`, `employee_range`, `min_active_jobs`, `total_results`

### Sumble

- **What:** B2B intelligence platform — find and enrich organizations, match company lists, find people by role, enrich contact details, and search job postings by technology
- **Docs:** vendor https://docs.sumble.com/api | ColdIQ https://coldiq.com/marketplace/apis/sumble | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 10.5 cr/result (per_result) x1; 10.5 cr/technology (per_result) x1; 2.1 cr/match (per_result) x1; 2.1 cr/result (per_result) x1 ...
- **Relevance (LinkedIn-first sourcing):** MEDIUM. Find people by role at orgs (2.1 cr/result), org find/match by technology; good for tech-stack-defined segments.
- **Endpoints (6):**

  - `POST /v1/sumble/organizations/find` - Find Organizations - **10.5 cr/result (per_result)** - params: `filters`, `include_entity_details`, `limit`, `offset`, `order_by_column`, `order_by_direction`
  - `POST /v1/sumble/organizations/enrich` - Enrich Organization - **10.5 cr/technology (per_result)** - params: `organization`, `filters`
  - `POST /v1/sumble/organizations/match` - Match Organizations - **2.1 cr/match (per_result)** - params: `organizations`
  - `POST /v1/sumble/people/find` - Find People - **2.1 cr/result (per_result)** - params: `organization`, `filters`, `limit`, `offset`
  - `POST /v1/sumble/people/enrich` - Enrich Person - **21 cr/call (per_call)** - params: `person_id`
  - `POST /v1/sumble/jobs/find` - Find Jobs - **base=4.2, with_description=6.3 cr/job (per_result)** - params: `organization`, `filters`, `include_descriptions`, `limit`, `offset`

### Wiza

- **What:** LinkedIn prospecting & email finder — export leads with verified contact data
- **Docs:** vendor https://wiza.co/api-docs | ColdIQ https://coldiq.com/marketplace/apis/wiza | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** none=17.5, partial=35, phone=122.5, full=122.5 cr/contact (per_result) x4; 0 cr/call (per_call) x4; 17.5 cr/profile (per_result) x1; 35 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW-MEDIUM. LinkedIn prospect search at 17.5 cr/profile - expensive for LinkedIn-URL-only needs; value is in email/phone reveals.
- **Endpoints (10):**

  - `POST /v1/wiza/individual-reveals` - Start Individual Reveal - **none=17.5, partial=35, phone=122.5, full=122.5 cr/contact (per_result)** - params: `individual_reveal`, `enrichment_level`, `email_options`, `callback_url`
  - `GET /v1/wiza/individual-reveals/{id}` - Get Individual Reveal - **0 cr/call (per_call)** - params: `id`
  - `POST /v1/wiza/lists` - Create List - **none=17.5, partial=35, phone=122.5, full=122.5 cr/contact (per_result)** - params: `list`
  - `GET /v1/wiza/lists/{id}` - Get List - **0 cr/call (per_call)** - params: `id`
  - `GET /v1/wiza/lists/{id}/contacts` - Get List Contacts - **0 cr/call (per_call)** - params: `id`, `segment`
  - `POST /v1/wiza/prospects/search` - Prospect Search - **17.5 cr/profile (per_result)** - params: `filters`, `size`
  - `POST /v1/wiza/prospects/create-prospect-list` - Create Prospect List - **none=17.5, partial=35, phone=122.5, full=122.5 cr/contact (per_result)** - params: `list`, `filters`, `enrichment_level`, `email_options`, `skip_duplicates`, `callback_url`
  - `POST /v1/wiza/prospects/continue-search` - Continue Prospect Search - **none=17.5, partial=35, phone=122.5, full=122.5 cr/contact (per_result)** - params: `id`, `max_profiles`, `enrichment_level`, `callback_url`
  - `POST /v1/wiza/company-enrichments` - Company Enrichment - **35 cr/call (per_call)** - params: `company_name`, `company_domain`, `company_linkedin_id`, `company_linkedin_slug`
  - `GET /v1/wiza/meta/credits` - Get Credits - **0 cr/call (per_call)**

### Openmart

- **What:** Retail & local business search, enrichment, and people intelligence
- **Docs:** vendor https://api.openmart.ai/docs | ColdIQ https://coldiq.com/marketplace/apis/openmart | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x4; 3.13 cr/result (per_result) x3; per_phone=31.29, per_email=3.13, per_name=3.13 cr/task (per_call_variable) x1; 6.26 cr/task (per_call) x1 ...
- **Relevance (LinkedIn-first sourcing):** LOW. Local/retail/SMB business search - only for local-business ICPs.
- **Endpoints (11):**

  - `POST /v1/openmart/search` - Search - **3.13 cr/result (per_result)** - params: `query`, `tags`, `location`, `min_locations`, `max_locations`, `has_contact_info`, `min_total_reviews`, `max_total_reviews`, `ownership_type`, `min_price_tier` (+16)
  - `POST /v1/openmart/search/only_ids` - Search Ids - **0 cr/call (per_call)** - params: `query`, `tags`, `location`, `min_locations`, `max_locations`, `has_contact_info`, `min_total_reviews`, `max_total_reviews`, `ownership_type`, `min_price_tier` (+16)
  - `POST /v1/openmart/business_records/list/{id_type}` - List By Ids - **3.13 cr/result (per_result)** - params: `id_type`
  - `POST /v1/openmart/enrich_company` - Enrich Company - **3.13 cr/result (per_result)** - params: `website`, `social_media_link`, `limit`, `estimate_total`, `location`
  - `POST /v1/openmart/task/batch/find_people` - Submit Batch (Find People) - **per_phone=31.29, per_email=3.13, per_name=3.13 cr/task (per_call_variable)**
  - `POST /v1/openmart/task/batch/find_tech` - Submit Batch (Find Tech) - **6.26 cr/task (per_call)**
  - `POST /v1/openmart/task/batch/lookup_people` - Submit Batch (Lookup People) - **per_phone=31.29, per_email=3.13, per_name=3.13 cr/person (per_result)**
  - `POST /v1/openmart/task/batch/lookup_business_email` - Submit Batch (Lookup Business Email) - **3.13 cr/task (per_call)**
  - `GET /v1/openmart/task/{task_id}` - Get Task - **0 cr/call (per_call)** - params: `task_id`
  - `GET /v1/openmart/task/batch/{batch_id}/status` - Check Batch - **0 cr/call (per_call)** - params: `batch_id`
  - `GET /v1/openmart/task/batch/{batch_id}/task_ids` - Get Task Ids - **0 cr/call (per_call)** - params: `batch_id`, `status`

## LinkedIn scraping & engagement extraction

### HarvestAPI

- **What:** Real-time LinkedIn scraping without a LinkedIn account — profiles (with optional verified email), companies, Sales Navigator lead and account search, posts, comments, reactions, jobs, groups, and the LinkedIn Ad Library
- **Docs:** vendor https://docs.harvestapi.io/guides/quickstart | ColdIQ https://coldiq.com/marketplace/apis/harvestapi | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.67 cr/100 results (per_page), 100 rows/call x6; 0.67 cr/50 results (per_page), 50 rows/call x4; 0.67 cr/10 results (per_page), 10 rows/call x2; 16.8 cr/25 results (per_page), 25 rows/call x2 ...
- **Relevance (LinkedIn-first sourcing):** HIGH. Real-time LinkedIn without a LinkedIn account: profile search (0.67 cr/10 results), Sales Navigator lead search and account search (16.8 cr/25 results), company search (0.67 cr/50), post engagers. Directly yields LinkedIn URLs; fills the "Sales Nav not wired in" gap.
- **Endpoints (24):**

  - `GET /v1/harvestapi/linkedin/profile` - Get Profile - **full=1.07, main=0.67, email=3.36 cr/call (per_call_variable)** - params: `url`, `publicIdentifier`, `profileId`, `main`, `findEmail`, `skipSmtp`, `includeAboutProfile`
  - `GET /v1/harvestapi/linkedin/profile-search` - Search LinkedIn profiles - **0.67 cr/10 results (per_page), 10 rows/call** - params: `search`, `currentCompany`, `pastCompany`, `school`, `firstName`, `lastName`, `title`, `location`, `geoId`, `industryId` (+4)
  - `GET /v1/harvestapi/linkedin/service-search` - Search Profile Services - **0.67 cr/10 results (per_page), 10 rows/call** - params: `search`, `location`, `geoId`, `page`
  - `GET /v1/harvestapi/linkedin/profile-posts` - Profile Posts - **0.67 cr/50 results (per_page), 50 rows/call** - params: `profile`, `profileId`, `profilePublicIdentifier`, `postedLimit`, `scrapePostedLimit`, `page`, `paginationToken`
  - `GET /v1/harvestapi/linkedin/profile-comments` - Profile comments - **0.67 cr/100 results (per_page), 100 rows/call** - params: `profile`, `profileId`, `postedLimit`, `page`, `paginationToken`
  - `GET /v1/harvestapi/linkedin/profile-reactions` - Profile reactions - **0.67 cr/100 results (per_page), 100 rows/call** - params: `profile`, `profileId`, `page`, `paginationToken`
  - `GET /v1/harvestapi/linkedin/lead-search` - Search Leads - **16.8 cr/25 results (per_page), 25 rows/call** - params: `search`, `currentCompanies`, `pastCompanies`, `locations`, `geoIds`, `schools`, `currentJobTitles`, `pastJobTitles`, `firstNames`, `lastNames` (+24)
  - `GET /v1/harvestapi/linkedin/account-search` - Search Sales Navigator Accounts - **16.8 cr/25 results (per_page), 25 rows/call** - params: `search`, `headquarterLocations`, `headquarterGeoIds`, `industryIds`, `companyHeadcount`, `companyHeadcountGrowth`, `annualRevenue`, `numOfFollowers`, `departmentHeadcount`, `departmentHeadcountGrowth` (+12)
  - `GET /v1/harvestapi/linkedin/company` - Get Company - **0.67 cr/call (per_call)** - params: `url`, `universalName`, `search`
  - `GET /v1/harvestapi/linkedin/company-search` - Search Companies - **0.67 cr/50 results (per_page), 50 rows/call** - params: `search`, `location`, `geoId`, `companySize`, `industryId`, `page`
  - `GET /v1/harvestapi/linkedin/company-posts` - Company Posts - **0.67 cr/50 results (per_page), 50 rows/call** - params: `company`, `companyId`, `companyUniversalName`, `postedLimit`, `scrapePostedLimit`, `page`, `paginationToken`
  - `GET /v1/harvestapi/linkedin/post-search` - Search Posts - **0.67 cr/50 results (per_page), 50 rows/call** - params: `search`, `profile`, `profileId`, `company`, `companyId`, `authorsCompany`, `authorsIndustryId`, `mentioningMember`, `mentioningCompany`, `contentType` (+7)
  - `GET /v1/harvestapi/linkedin/post` - Get post - **0.67 cr/call (per_call)** - params: `url`
  - `GET /v1/harvestapi/linkedin/post-comments` - Post comments - **0.67 cr/100 results (per_page), 100 rows/call** - params: `post`, `sortBy`, `page`, `paginationToken`
  - `GET /v1/harvestapi/linkedin/post-reactions` - Post reactions - **0.67 cr/100 results (per_page), 100 rows/call** - params: `post`, `sortBy`, `page`
  - `GET /v1/harvestapi/linkedin/post-comment-replies` - Comment replies - **0.67 cr/100 results (per_page), 100 rows/call** - params: `url`, `paginationToken`
  - `GET /v1/harvestapi/linkedin/comment-reactions` - Comment reactions - **0.67 cr/100 results (per_page), 100 rows/call** - params: `url`, `page`
  - `GET /v1/harvestapi/linkedin/ad-search` - Search Ad Library - **0.27 cr/24 results (per_page), 24 rows/call** - params: `searchUrl`, `keyword`, `accountOwner`, `countries`, `dateOption`, `startdate`, `enddate`, `paginationToken`
  - `GET /v1/harvestapi/linkedin/ad` - Get Ad Details - **0.27 cr/call (per_call)** - params: `adId`, `url`
  - `GET /v1/harvestapi/linkedin/job` - Get Job - **0.17 cr/call (per_call)** - params: `jobId`, `url`
  - `GET /v1/harvestapi/linkedin/job-search` - Search Jobs - **0.17 cr/25 results (per_page), 25 rows/call** - params: `search`, `companyId`, `location`, `geoId`, `sortBy`, `workplaceType`, `employmentType`, `salary`, `postedLimit`, `experienceLevel` (+5)
  - `GET /v1/harvestapi/linkedin/group` - Get Group - **0.34 cr/call (per_call)** - params: `url`, `groupId`
  - `GET /v1/harvestapi/linkedin/group-search` - Search Groups - **0.34 cr/10 results (per_page), 10 rows/call** - params: `search`, `page`
  - `GET /v1/harvestapi/linkedin/geo-id-search` - Search GeoID - **0.17 cr/call (per_call)** - params: `search`

### LeadsFactory

- **What:** LinkedIn prospecting platform — find contacts matching job titles across company lists (Contact Finder) and scrape Sales Navigator searches using the shared infrastructure account (SN Scraper)
- **Docs:** vendor https://apiv2.leadsfactory.io/docs | ColdIQ https://coldiq.com/marketplace/apis/leadsfactory | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x2; 0.35 cr/contact (per_result) x1; 0.35 cr/profile (per_result) x1
- **Relevance (LinkedIn-first sourcing):** HIGH. Contact Finder (titles across a company list, 0.35 cr/contact) and Sales Navigator search scraper (0.35 cr/profile) on ColdIQ's shared SN account - cheapest LinkedIn-URL-per-row option in the catalog.
- **Endpoints (4):**

  - `POST /v1/leadsfactory/contact-finder/searches` - Find People — Create Search - **0.35 cr/contact (per_result)** - params: `name`, `company_linkedin_urls`, `company_domains`, `search`, `webhook_url`, `custom_metadata`, `send_webhook_on_no_results`
  - `GET /v1/leadsfactory/contact-finder/searches/{id}` - Find People — Get Search Status - **0 cr/call (per_call)** - params: `id`, `include_contacts`, `contacts_limit`, `contacts_after`
  - `POST /v1/leadsfactory/sn-scraper/jobs` - Sales Navigator Scraper — Start Job - **0.35 cr/profile (per_result)** - params: `sales_nav_url`, `search_name`, `max_profiles`, `webhook_url`
  - `GET /v1/leadsfactory/sn-scraper/jobs/{job_id}` - Sales Navigator Scraper — Get Job Status - **0 cr/call (per_call)** - params: `job_id`

### Jungler

- **What:** LinkedIn post engagement extraction — collect commenters and reactors from any LinkedIn post, then retrieve contacts, comments, and reaction data
- **Docs:** vendor https://jungler.io | ColdIQ https://coldiq.com/marketplace/apis/jungler | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x3; 0 cr/call (per_call), 500 rows/call x3; 35 cr/task (per_call) x1; 3.5 cr/page (per_result) x1
- **Relevance (LinkedIn-first sourcing):** MEDIUM. Pull commenters/reactors from a LinkedIn post (35 cr/task, results free) - intent-based LinkedIn lists.
- **Endpoints (8):**

  - `POST /v1/jungler/workbooks` - Create Collection Task - **35 cr/task (per_call)** - params: `post_url`, `data_types`
  - `GET /v1/jungler/tasks/{task_id}/status` - Get Task Status - **0 cr/call (per_call)** - params: `task_id`
  - `GET /v1/jungler/workbooks/{workbook_id}/contacts` - Get Contacts - **0 cr/call (per_call), 500 rows/call** - params: `workbook_id`, `fields`, `activity_filter`, `page`, `page_size`
  - `GET /v1/jungler/workbooks/{workbook_id}/comments` - Get Comments - **0 cr/call (per_call), 500 rows/call** - params: `workbook_id`, `include_replies`, `page`, `page_size`
  - `GET /v1/jungler/workbooks/{workbook_id}/reactions` - Get Reactions - **0 cr/call (per_call), 500 rows/call** - params: `workbook_id`, `page`, `page_size`
  - `GET /v1/jungler/searches` - List Searches - **0 cr/call (per_call)**
  - `GET /v1/jungler/searches/{search_id}` - Get Search - **0 cr/call (per_call)** - params: `search_id`
  - `GET /v1/jungler/posts` - List Posts - **3.5 cr/page (per_result)** - params: `search_ids`, `page`, `page_size`, `match`, `post_type`, `sentiment`, `language`, `from_date`, `to_date`, `country` (+5)

## Email / phone finding & verification

### FullEnrich

- **What:** Email & phone number enrichment via LinkedIn URLs
- **Docs:** vendor https://docs.fullenrich.com/ | ColdIQ https://coldiq.com/marketplace/apis/fullenrich | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 11.63 cr/call (per_call) x2; 11.63 cr/result (per_result) x2; contact.emails=14, contact.phones=119, contact.personal_emails=35 cr/contact (per_result) x1; 11.63 cr/contact (per_result) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Email/phone waterfall from LinkedIn URL; people/company search at 11.63 cr/result (pricey).
- **Endpoints (6):**

  - `POST /v1/fullenrich/contact/enrich/bulk` - Enrich Contacts In Bulk - **contact.emails=14, contact.phones=119, contact.personal_emails=35 cr/contact (per_result)** - params: `name`, `webhook_url`, `webhook_events`, `data`
  - `GET /v1/fullenrich/contact/enrich/bulk/{enrichmentId}` - Get Bulk Enrich Results - **11.63 cr/call (per_call)** - params: `enrichmentId`
  - `POST /v1/fullenrich/contact/reverse/email/bulk` - Reverse Contact Lookup In Bulk - **11.63 cr/contact (per_result)** - params: `name`, `webhook_url`, `webhook_events`, `data`
  - `GET /v1/fullenrich/contact/reverse/email/bulk/{enrichmentId}` - Get Bulk Reverse Email Results - **11.63 cr/call (per_call)** - params: `enrichmentId`
  - `POST /v1/fullenrich/people/search` - Search people - **11.63 cr/result (per_result)** - params: `offset`, `limit`, `search_after`, `current_company_names`, `current_company_domains`, `current_company_linkedin_urls`, `current_company_specialties`, `current_company_industries`, `current_company_types`, `current_company_headquarters` (+17)
  - `POST /v1/fullenrich/company/search` - Search company - **11.63 cr/result (per_result)** - params: `offset`, `limit`, `search_after`, `names`, `domains`, `linkedin_urls`, `keywords`, `specialties`, `industries`, `types` (+4)

### Findymail

- **What:** Professional email finder & verifier
- **Docs:** vendor https://app.findymail.com/docs/ | ColdIQ https://coldiq.com/marketplace/apis/findymail | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 3.57 cr/call (per_call) x27; 3.57 cr/result (per_result) x3; default=3.57, with_profile=7.13 cr/call (per_call_variable) x1; 0.36 cr/result (per_result) x1 ...
- **Relevance (LinkedIn-first sourcing):** LOW. Email finder/verifier; employee search (3.57 cr/result) and cheap lookalike companies (0.36 cr/result) are the sourcing-relevant parts. Note even list/admin calls cost 3.57 cr.
- **Endpoints (33):**

  - `POST /v1/findymail/verify` - Verify an email for potential bounce - **3.57 cr/call (per_call)** - params: `email`
  - `POST /v1/findymail/search/name` - Find from name - **3.57 cr/call (per_call)** - params: `name`, `domain`, `webhook_url`
  - `POST /v1/findymail/search/domain` - Find from domain - **3.57 cr/call (per_call)** - params: `domain`, `roles`, `webhook_url`
  - `POST /v1/findymail/search/business-profile` - Find from business profile - **3.57 cr/call (per_call)** - params: `linkedin_url`, `webhook_url`
  - `POST /v1/findymail/search/reverse-email` - Reverse email lookup - **default=3.57, with_profile=7.13 cr/call (per_call_variable)** - params: `email`, `with_profile`
  - `POST /v1/findymail/search/company` - Get company information - **3.57 cr/call (per_call)** - params: `domain`, `linkedin_url`, `name`
  - `POST /v1/findymail/search/employees` - Find employees - **3.57 cr/result (per_result)** - params: `website`, `job_titles`, `count`
  - `POST /v1/findymail/search/phone` - Find phone - **3.57 cr/call (per_call)** - params: `linkedin_url`
  - `GET /v1/findymail/lists` - Get the list of contact lists - **3.57 cr/call (per_call)**
  - `POST /v1/findymail/lists` - Create a new list - **3.57 cr/call (per_call)** - params: `name`
  - `PUT /v1/findymail/lists/{id}` - Update a contact list - **3.57 cr/call (per_call)** - params: `id`, `name`, `isShared`
  - `DELETE /v1/findymail/lists/{id}` - Delete a given list - **3.57 cr/call (per_call)** - params: `id`
  - `GET /v1/findymail/contacts/{id}` - Get contacts saved - **3.57 cr/call (per_call)** - params: `id`
  - `POST /v1/findymail/intellimatch/search` - Search leads - **3.57 cr/call (per_call)** - params: `query`, `limit`, `config`
  - `GET /v1/findymail/intellimatch/status` - Get export status - **3.57 cr/call (per_call)** - params: `hash`
  - `GET /v1/findymail/intellimatch/data` - Get results - **3.57 cr/result (per_result)** - params: `hash`, `page`, `per_page`
  - `GET /v1/findymail/intellimatch/exclusion-lists` - Get all exclusion lists - **3.57 cr/call (per_call)**
  - `POST /v1/findymail/intellimatch/exclusion-lists` - Create a new exclusion list - **3.57 cr/call (per_call)** - params: `name`, `is_shared`
  - `GET /v1/findymail/intellimatch/exclusion-lists/{id}` - Get exclusion list details - **3.57 cr/call (per_call)** - params: `id`
  - `PUT /v1/findymail/intellimatch/exclusion-lists/{id}` - Update an exclusion list - **3.57 cr/call (per_call)** - params: `id`, `name`, `is_shared`
  - `DELETE /v1/findymail/intellimatch/exclusion-lists/{id}` - Delete an exclusion list - **3.57 cr/call (per_call)** - params: `id`
  - `GET /v1/findymail/intellimatch/domains` - Get excluded domains - **3.57 cr/call (per_call)**
  - `POST /v1/findymail/intellimatch/domains` - Add excluded domains - **3.57 cr/call (per_call)** - params: `domains`, `list_id`
  - `DELETE /v1/findymail/intellimatch/domains` - Remove excluded domains - **3.57 cr/call (per_call)** - params: `ids`
  - `GET /v1/findymail/signals` - List signals - **3.57 cr/call (per_call)** - params: `page`, `per_page`, `signal_type`, `monitor_id`, `date_from`, `date_to`
  - `GET /v1/findymail/signals/monitors` - List monitors - **3.57 cr/call (per_call)**
  - `POST /v1/findymail/signals/monitors` - Create a monitor - **3.57 cr/call (per_call)** - params: `name`, `signal_type`, `keywords`, `webhook_url`, `post_url`, `engagement_types`, `enrichment_level`, `lead_list_id`, `icp_filters`
  - `PATCH /v1/findymail/signals/monitors/{id}` - Update a monitor - **3.57 cr/call (per_call)** - params: `id`, `name`, `keywords`, `webhook_url`, `post_url`, `engagement_types`, `enrichment_level`, `lead_list_id`, `icp_filters`
  - `DELETE /v1/findymail/signals/monitors/{id}` - Delete a monitor - **3.57 cr/call (per_call)** - params: `id`
  - `POST /v1/findymail/lookalike/search` - Search for lookalike companies - **0.36 cr/result (per_result)** - params: `seed`, `limit`
  - `GET /v1/findymail/technologies/search` - Search available technologies - **0 cr/call (per_call)** - params: `q`
  - `POST /v1/findymail/technologies` - Look up technologies by domain - **3.57 cr/result (per_result)** - params: `domain`, `technologies`
  - `GET /v1/findymail/signals/{id}` - Get a signal - **3.57 cr/call (per_call)** - params: `id`

### Icypeas

- **What:** Email search, verification & domain scanning
- **Docs:** vendor https://api-doc.icypeas.com/ | ColdIQ https://coldiq.com/marketplace/apis/icypeas | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 1.05 cr/call (per_call) x18; 1.05 cr/result (per_result) x2
- **Relevance (LinkedIn-first sourcing):** MEDIUM. Beyond email: find-people / find-companies (1.05 cr/result) and URL-search (find a LinkedIn profile/company page from name+company, 1.05 cr) - cheap LinkedIn URL resolution.
- **Endpoints (20):**

  - `POST /v1/icypeas/email-search` - Single Search: Email Discovery - **1.05 cr/call (per_call)** - params: `firstname`, `lastname`, `domainOrCompany`, `custom`
  - `POST /v1/icypeas/domain-scan` - Single Search: Domain Scan - **1.05 cr/call (per_call)** - params: `domainOrCompany`, `custom`
  - `POST /v1/icypeas/email-verification` - Single Search: Email Verification - **1.05 cr/call (per_call)** - params: `email`, `custom`
  - `POST /v1/icypeas/bulk-search` - Bulk search - **1.05 cr/call (per_call)** - params: `name`, `task`, `data`, `custom`
  - `POST /v1/icypeas/scrape/profile` - Single profile scraping - **1.05 cr/call (per_call)** - params: `url`
  - `POST /v1/icypeas/scrape/profiles` - Bulk profiles scraping - **1.05 cr/call (per_call)** - params: `data`
  - `POST /v1/icypeas/scrape/company` - Single company scraping - **1.05 cr/call (per_call)** - params: `url`
  - `POST /v1/icypeas/scrape/companies` - Bulk companies scraping - **1.05 cr/call (per_call)** - params: `data`
  - `POST /v1/icypeas/url-search/profile` - Search for profile page one at a time - **1.05 cr/call (per_call)** - params: `firstname`, `lastname`, `companyOrDomain`, `jobTitle`
  - `POST /v1/icypeas/url-search/profiles` - Search for profile pages in bulk - **1.05 cr/call (per_call)** - params: `data`
  - `POST /v1/icypeas/url-search/company` - Search for company page one at a time - **1.05 cr/call (per_call)** - params: `companyOrDomain`
  - `POST /v1/icypeas/url-search/companies` - Search for company pages in bulk - **1.05 cr/call (per_call)** - params: `data`
  - `POST /v1/icypeas/find-people/count` - Count the number of people matching your query - **1.05 cr/call (per_call)** - params: `query`
  - `POST /v1/icypeas/find-people` - Find people - **1.05 cr/result (per_result)** - params: `query`, `pagination`
  - `POST /v1/icypeas/find-companies/count` - Count the number of companies matching your query - **1.05 cr/call (per_call)** - params: `query`
  - `POST /v1/icypeas/find-companies` - Find companies - **1.05 cr/result (per_result)** - params: `query`, `pagination`
  - `POST /v1/icypeas/reverse-email-lookup` - Single search : Find the profile URL behind a single email address - **1.05 cr/call (per_call)** - params: `email`
  - `POST /v1/icypeas/reverse-email-lookups` - Bulk search : Find the profile URLs behind many email addresses - **1.05 cr/call (per_call)** - params: `data`
  - `POST /v1/icypeas/search-results` - Retrieve your results - **1.05 cr/call (per_call)** - params: `mode`, `id`, `file`, `limit`, `next`, `sort`, `type`
  - `POST /v1/icypeas/search-files` - Fetch information and stats about your bulk searches - **1.05 cr/call (per_call)** - params: `file`, `status`

### LeadMagic

- **What:** B2B enrichment — work/personal email finder and validation, mobile finder, profile and company intel, competitor ads
- **Docs:** vendor https://leadmagic.io/docs/v1/making-api-calls | ColdIQ https://coldiq.com/marketplace/apis/leadmagic | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 4.16 cr/call (per_call) x4; 8.32 cr/call (per_call) x3; 20.79 cr/call (per_call) x3; 4.16 cr/ad (per_result) x3 ...
- **Relevance (LinkedIn-first sourcing):** LOW-MEDIUM. Mostly email/mobile; employee-finder (0.21 cr/employee) and role-finder are sourcing-relevant.
- **Endpoints (18):**

  - `POST /v1/leadmagic/people/email-finder` - Email Finder - **4.16 cr/call (per_call)** - params: `first_name`, `last_name`, `full_name`, `domain`, `company_name`
  - `POST /v1/leadmagic/people/email-validation` - Email Validation - **1.04 cr/call (per_call)** - params: `email`
  - `POST /v1/leadmagic/people/personal-email-finder` - Personal Email Finder - **8.32 cr/call (per_call)** - params: `profile_url`
  - `POST /v1/leadmagic/people/b2b-profile-email` - B2B Person Profile to Email - **20.79 cr/call (per_call)** - params: `profile_url`
  - `POST /v1/leadmagic/people/profile-search` - B2B Person Profile - **4.16 cr/call (per_call)** - params: `profile_url`
  - `POST /v1/leadmagic/people/b2b-profile` - Email Address to B2B Person Profile - **41.58 cr/call (per_call)** - params: `work_email`, `personal_email`
  - `POST /v1/leadmagic/people/mobile-finder` - Mobile Finder - **20.79 cr/call (per_call)** - params: `profile_url`, `work_email`, `personal_email`
  - `POST /v1/leadmagic/people/job-change-detector` - Job Change Detector - **12.47 cr/call (per_call)** - params: `profile_url`, `company_name`, `company_domain`
  - `POST /v1/leadmagic/people/role-finder` - Role Finder - **8.32 cr/call (per_call)** - params: `job_title`, `company_name`, `company_domain`
  - `POST /v1/leadmagic/people/employee-finder` - Employee Finder - **0.21 cr/employee (per_result)** - params: `company_domain`, `company_name`, `limit`
  - `POST /v1/leadmagic/companies/company-search` - Company Search - **4.16 cr/call (per_call)** - params: `profile_url`, `company_domain`, `company_name`
  - `POST /v1/leadmagic/companies/company-funding` - Company Funding - **16.63 cr/call (per_call)** - params: `company_name`, `company_domain`
  - `POST /v1/leadmagic/companies/competitors-search` - Competitors Search - **20.79 cr/call (per_call)** - params: `company_domain`, `company_url`, `company_name`
  - `POST /v1/leadmagic/companies/technographics` - Company Technographics - **4.16 cr/call (per_call)** - params: `company_domain`
  - `POST /v1/leadmagic/ads/google-ads-search` - Google Ads Search - **4.16 cr/ad (per_result)** - params: `company_domain`, `company_name`
  - `POST /v1/leadmagic/ads/meta-ads-search` - Meta Ads Search - **4.16 cr/ad (per_result)** - params: `company_domain`, `company_name`
  - `POST /v1/leadmagic/ads/b2b-ads-search` - B2B Search Ads - **4.16 cr/ad (per_result)** - params: `company_domain`, `company_name`
  - `POST /v1/leadmagic/ads/b2b-ads-details` - B2B Ad Details - **8.32 cr/call (per_call)** - params: `ad_url`

### BounceBan

- **What:** Verify catch-all and risky emails without sending — verdicts for addresses other tools mark unknown
- **Docs:** vendor https://bounceban.com/public/doc/api.html | ColdIQ https://coldiq.com/marketplace/apis/bounceban | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x3; 0.71 cr/verification (per_result) x1; 0.71 cr/email (per_result) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Email verification (catch-all) only.
- **Endpoints (5):**

  - `POST /v1/bounceban/verify/single` - Waterfall single verification - **0.71 cr/verification (per_result)** - params: `email`, `mode`, `disable_catchall_verify`
  - `POST /v1/bounceban/verify/bulk` - Create bulk task from a list of emails - **0.71 cr/email (per_result)** - params: `emails`, `name`, `mode`, `greylisting_bypass`, `disable_catchall_verify`
  - `GET /v1/bounceban/verify/bulk/status` - Get bulk task status - **0 cr/call (per_call)** - params: `id`
  - `POST /v1/bounceban/verify/bulk/emails` - Get results for specific emails - **0 cr/call (per_call)** - params: `id`, `emails`
  - `GET /v1/bounceban/verify/bulk/dump` - Dump all results as JSON (paginated) - **0 cr/call (per_call)** - params: `id`, `state`, `cursor`, `page_size`, `retrieve_all`

## Signals, intent, technographics & job postings

### PredictLeads

- **What:** Company growth signals & buying intent data
- **Docs:** vendor https://docs.predictleads.com/ | ColdIQ https://coldiq.com/marketplace/apis/predictleads | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 2.51 cr/call (per_call) x16; 2.51 cr/result (per_result) x9; 7.53 cr/result (per_result) x1
- **Relevance (LinkedIn-first sourcing):** MEDIUM (signals). Job openings, financing, news, tech detections, similar companies - "why now" triggers and lookalikes; 2.51 cr per call/result.
- **Endpoints (26):**

  - `GET /v1/predictleads/companies/{idOrDomain}` - Retrieve Company - **2.51 cr/call (per_call)** - params: `idOrDomain`
  - `GET /v1/predictleads/discover/companies` - Retrieve Companies - **2.51 cr/result (per_result)** - params: `location`, `sizes`, `naics_codes`, `industry`, `revenue_range_low`, `revenue_range_high`, `page`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/similar_companies` - Retrieve company's Similar Companies - **2.51 cr/result (per_result)** - params: `companyIdOrDomain`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/job_openings` - Retrieve company's Job Openings - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `active_only`, `not_closed`, `first_seen_at_from`, `first_seen_at_until`, `last_seen_at_from`, `last_seen_at_until`, `with_description_only`, `with_location_only`, `categories` (+2)
  - `GET /v1/predictleads/job_openings/{id}` - Retrieve a single Job Opening by ID - **2.51 cr/call (per_call)** - params: `id`
  - `GET /v1/predictleads/discover/job_openings` - Retrieve a list of Job Openings - **2.51 cr/result (per_result)** - params: `onet_codes`, `location`, `active_only`, `found_at_from`, `seniority`, `page`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/technology_detections` - Retrieve Technologies used by specific Company - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `first_seen_at_from`, `first_seen_at_until`, `last_seen_at_from`, `last_seen_at_until`, `page`, `limit`
  - `GET /v1/predictleads/discover/technologies/{technologyIdOrFuzzyName}/technology_detections` - Retrieve Companies using specific Technology ID or fuzzy name - **2.51 cr/result (per_result)** - params: `technologyIdOrFuzzyName`, `first_seen_at_from`, `first_seen_at_until`, `last_seen_at_from`, `last_seen_at_until`, `page`, `limit`
  - `GET /v1/predictleads/extended_technology_detections/{id}` - Retrieve a single Extended Technology Detection by ID - **2.51 cr/call (per_call)** - params: `id`
  - `GET /v1/predictleads/technologies` - Retrieve all tracked Technologies - **7.53 cr/result (per_result)** - params: `fuzzy_name`, `order_by`, `page`, `limit`
  - `GET /v1/predictleads/technologies/{idOrFuzzyName}` - Retrieve a single Technology by ID or fuzzy name - **2.51 cr/call (per_call)** - params: `idOrFuzzyName`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/news_events` - Retrieve company's News Events - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `found_at_from`, `found_at_until`, `categories`, `page`, `limit`
  - `GET /v1/predictleads/news_events/{id}` - Retrieve a single News Event by ID - **2.51 cr/call (per_call)** - params: `id`
  - `GET /v1/predictleads/discover/news_events` - Retrieve News Events - **2.51 cr/result (per_result)** - params: `categories`, `company_location`, `company_sizes`, `page`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/financing_events` - Retrieve company's Financing Events - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `first_seen_at_from`, `first_seen_at_until`, `page`, `limit`
  - `GET /v1/predictleads/discover/financing_events` - Retrieve Financing Events - **2.51 cr/result (per_result)** - params: `financing_types_normalized`, `company_location`, `page`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/sec_filings` - Retrieve company's SEC Filings - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `form_types`, `filed_at_from`, `filed_at_until`, `page`, `limit`
  - `GET /v1/predictleads/sec_filings/{id}` - Retrieve a single SEC Filing by ID - **2.51 cr/call (per_call)** - params: `id`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/connections` - Retrieve company's Connections - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `first_seen_at_from`, `first_seen_at_until`, `categories`, `page`, `limit`
  - `GET /v1/predictleads/discover/portfolio_companies/connections` - Retrieve Portfolio Companies - **2.51 cr/result (per_result)** - params: `first_seen_at_from`, `first_seen_at_until`, `last_seen_at_from`, `last_seen_at_until`, `page`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/website_evolution` - Retrieve company's Website Evolution - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `first_seen_at_from`, `first_seen_at_until`, `page`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/github_repositories` - Retrieve company's Github Repositories - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `first_seen_at_from`, `first_seen_at_until`, `page`, `limit`
  - `GET /v1/predictleads/companies/{companyIdOrDomain}/products` - Retrieve company's Products - **2.51 cr/call (per_call)** - params: `companyIdOrDomain`, `categories`, `subcategories`, `page`, `limit`
  - `GET /v1/predictleads/products/{id}` - Retrieve a single Product by ID - **2.51 cr/call (per_call)** - params: `id`
  - `GET /v1/predictleads/discover/products` - Retrieve a list of Products - **2.51 cr/result (per_result)** - params: `categories`, `subcategories`, `page`, `limit`
  - `GET /v1/predictleads/discover/startup_platform_posts` - Retrieve latest posts - **2.51 cr/result (per_result)** - params: `published_at_from`, `published_at_until`, `post_types`, `page`, `limit`

### Signalbase

- **What:** Real-time funding, acquisition, job change, and hiring signals plus investor and company data — track market movements, discover opportunities, and enrich your pipeline with verified signal intelligence
- **Docs:** vendor https://docs.trysignalbase.com | ColdIQ https://coldiq.com/marketplace/apis/signalbase | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 3.5 cr/call (per_call) x6
- **Relevance (LinkedIn-first sourcing):** MEDIUM (signals). Funding, acquisition, job-change, hiring signals at 3.5 cr/call.
- **Endpoints (6):**

  - `GET /v1/signalbase/funding-signals` - Get Funding Signals - **3.5 cr/call (per_call)** - params: `page`, `limit`, `dateFrom`, `dateTo`, `date_preset`, `countries`, `categories`, `industry`, `subcategories`, `round` (+15)
  - `GET /v1/signalbase/acquisition-signals` - Get Acquisition Signals - **3.5 cr/call (per_call)** - params: `page`, `limit`, `dateFrom`, `dateTo`, `date_preset`, `countries`, `categories`, `industry`, `subcategories`, `search` (+13)
  - `GET /v1/signalbase/job-change-signals` - Get Job Change Signals - **3.5 cr/call (per_call)** - params: `page`, `limit`, `dateFrom`, `dateTo`, `date_preset`, `search`, `countries`, `city`, `person_name`, `company_name` (+11)
  - `GET /v1/signalbase/hiring-signals` - Get Hiring Signals - **3.5 cr/call (per_call)** - params: `page`, `limit`, `dateFrom`, `dateTo`, `date_preset`, `search`, `countries`, `states`, `city`, `categories` (+9)
  - `GET /v1/signalbase/investors` - Get Investors - **3.5 cr/call (per_call)** - params: `page`, `limit`, `dateFrom`, `dateTo`, `date_preset`, `search`, `countries`, `type`, `categories`, `headquarters` (+5)
  - `GET /v1/signalbase/companies` - Get Companies - **3.5 cr/call (per_call)** - params: `page`, `limit`, `search`, `countries`, `industry`, `employee_count_min`, `employee_count_max`, `founded_year_min`, `founded_year_max`, `sort_by` (+2)

### TheirStack

- **What:** Job postings and company technographics — search jobs by tech stack, find companies by technology usage and buying intent signals
- **Docs:** vendor https://theirstack.com/en/docs/api-reference | ColdIQ https://coldiq.com/marketplace/apis/theirstack | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 12.6 cr/call (per_call) x2; 4.2 cr/job (per_result) x1; 12.6 cr/company (per_result) x1
- **Relevance (LinkedIn-first sourcing):** MEDIUM (signals). Jobs by tech stack, companies by technology usage, buying intents (12.6 cr/company).
- **Endpoints (4):**

  - `POST /v1/theirstack/jobs/search` - Search jobs - **4.2 cr/job (per_result)** - params: `page`, `limit`, `offset`, `order_by`, `job_title_or`, `job_title_pattern_or`, `job_title_pattern_and`, `job_country_code_or`, `posted_at_max_age_days`, `posted_at_gte` (+15)
  - `POST /v1/theirstack/companies/search` - Search companies - **12.6 cr/company (per_result)** - params: `page`, `limit`, `offset`, `order_by`, `expand_technology_slugs`, `company_name_or`, `company_domain_or`, `company_linkedin_url_or`, `company_technology_slug_or`, `company_technology_slug_and` (+12)
  - `POST /v1/theirstack/companies/technologies` - Get company technologies - **12.6 cr/call (per_call)** - params: `company_domain`, `company_name`, `company_linkedin_url`, `company_name_or`, `order_by`, `technology_slug_or`, `technology_category_slug_or`, `keyword_slug_or`, `keyword_category_slug_or`, `confidence_or` (+1)
  - `POST /v1/theirstack/companies/buying_intents` - Get company buying intents - **12.6 cr/call (per_call)** - params: `company_domain`, `company_name`, `company_linkedin_url`, `company_name_or`, `order_by`, `technology_slug_or`, `technology_category_slug_or`, `keyword_slug_or`, `keyword_category_slug_or`, `confidence_or` (+1)

### BuiltWith

- **What:** Technology profiling — detect the full tech stack of any domain including frameworks, analytics, CRMs, ad networks, and CDNs
- **Docs:** vendor https://api.builtwith.com/ | ColdIQ https://coldiq.com/marketplace/apis/builtwith | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 3.13 cr/call (per_call) x3
- **Relevance (LinkedIn-first sourcing):** LOW-MEDIUM. Tech-stack profiling of a domain / list of sites using a tech (3.13 cr/call).
- **Endpoints (3):**

  - `POST /v1/builtwith/domain` - Domain API - **3.13 cr/call (per_call)** - params: `domain`
  - `POST /v1/builtwith/lists` - Lists API - **3.13 cr/call (per_call)** - params: `technology`, `other_technologies`, `include_meta`, `countries`, `offset`, `since`, `all`, `spend`, `revenue`, `sku` (+13)
  - `POST /v1/builtwith/relationships` - Relationships API - **3.13 cr/call (per_call)** - params: `domain`, `domains`, `offset`, `include_ip`

### LinkedIn Jobs API

- **What:** Real-time LinkedIn job search with advanced filters — title, location, description, company size, industry, seniority, employment type, and AI enrichments (work arrangement, salary, experience level, visa sponsorship)
- **Docs:** vendor https://www.linkedin.com/jobs | ColdIQ https://coldiq.com/marketplace/apis/linkedin-jobs-api | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call), 20 rows/call x1; 0.74 cr/job (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** MEDIUM (signals). LinkedIn job search (0.74 cr/job) - hiring-intent company lists.
- **Endpoints (3):**

  - `GET /v1/linkedin-jobs-api/search` - List Advanced LinkedIn Job Search jobs - **0 cr/call (per_call), 20 rows/call** - params: `limit`, `offset`
  - `POST /v1/linkedin-jobs-api/search` - Advanced LinkedIn Job Search - **0.74 cr/job (per_result)** - params: `timeRange`, `limit`, `includeAi`, `removeAgency`, `titleSearch`, `titleExclusionSearch`, `locationSearch`, `locationExclusionSeach`, `descriptionSearch`, `descriptionExclusionSearch` (+28)
  - `GET /v1/linkedin-jobs-api/search/{jobId}` - Get Advanced LinkedIn Job Search result - **0 cr/call (per_call)** - params: `jobId`

### Career Site Jobs

- **What:** Real-time job postings scraped directly from 175k+ company career sites across 54 ATS platforms (Workday, Greenhouse, Ashby, Lever, and more) — with AI enrichments and LinkedIn company data
- **Docs:** vendor https://fantastic.jobs | ColdIQ https://coldiq.com/marketplace/apis/career-site-jobs | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call), 20 rows/call x1; 1.26 cr/job (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** MEDIUM (signals). ATS/career-site job postings (1.26 cr/job) with LinkedIn company data.
- **Endpoints (3):**

  - `GET /v1/career-site-jobs/search` - List Career Site Job Listing API jobs - **0 cr/call (per_call), 20 rows/call** - params: `limit`, `offset`
  - `POST /v1/career-site-jobs/search` - Career Site Job Listing API - **1.26 cr/job (per_result)** - params: `limit`, `timeRange`, `titleSearch`, `titleExclusionSearch`, `locationSearch`, `locationExclusionSearch`, `descriptionSearch`, `descriptionExclusionSearch`, `organizationSearch`, `organizationExclusionSearch` (+23)
  - `GET /v1/career-site-jobs/search/{jobId}` - Get Career Site Job Listing API result - **0 cr/call (per_call)** - params: `jobId`

## Ad intelligence

### Adyntel

- **What:** Ad intelligence across Meta, Google, LinkedIn & TikTok ad libraries — by domain or keyword
- **Docs:** vendor https://docs.adyntel.com/ | ColdIQ https://coldiq.com/marketplace/apis/adyntel | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 1.85 cr/call (per_call) x8
- **Relevance (LinkedIn-first sourcing):** LOW. Ad intelligence by domain/keyword (1.85 cr/call).
- **Endpoints (8):**

  - `POST /v1/adyntel/facebook` - Facebook & Instagram Ads - **1.85 cr/call (per_call)** - params: `company_domain`, `facebook_url`, `country_code`, `media_type`, `active_status`, `check_ugc`, `continuation_token`
  - `POST /v1/adyntel/google` - Google Ads - **1.85 cr/call (per_call)** - params: `company_domain`, `media_type`, `continuation_token`
  - `POST /v1/adyntel/linkedin` - LinkedIn Ads - **1.85 cr/call (per_call)** - params: `company_domain`, `linkedin_page_id`, `date_filter`, `continuation_token`
  - `POST /v1/adyntel/linkedin-keyword-search` - LinkedIn Keyword Search - **1.85 cr/call (per_call)** - params: `keyword`, `country`, `dateOption`, `startDate`, `endDate`, `continuation_token`
  - `POST /v1/adyntel/meta-ad-search` - Meta Ad Search - **1.85 cr/call (per_call)** - params: `keyword`, `country_code`, `continuation_token`
  - `POST /v1/adyntel/tiktok-search` - TikTok Ad Search - **1.85 cr/call (per_call)** - params: `keyword`, `country_code`
  - `POST /v1/adyntel/tiktok-ad-details` - TikTok Ad Details - **1.85 cr/call (per_call)** - params: `id`
  - `POST /v1/adyntel/domain-keywords` - Paid vs Organic Keywords - **1.85 cr/call (per_call)** - params: `company_domain`, `language`, `limit`

### LinkedIn Ad Library

- **What:** Search and extract ads from the LinkedIn Ad Library — ad copy, media, CTAs, impressions, and advertiser details
- **Docs:** vendor https://www.linkedin.com/ad-library | ColdIQ https://coldiq.com/marketplace/apis/linkedin-ad-library | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.21 cr/ad (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Who advertises on LinkedIn (0.21 cr/ad) - possible intent signal.
- **Endpoints (2):**

  - `POST /v1/linkedin-ad-library/search` - LinkedIn Ad Library Scraper - **0.21 cr/ad (per_result)** - params: `searchUrls`, `maxResults`
  - `GET /v1/linkedin-ad-library/search/{jobId}` - Get LinkedIn Ad Library job result - **0 cr/call (per_call)** - params: `jobId`

### Meta Ads Library

- **What:** Search and scrape ads from the Facebook Ads Library — creatives, targeting, spend, and activity data
- **Docs:** vendor https://www.facebook.com/ads/library | ColdIQ https://coldiq.com/marketplace/apis/meta-ads-library | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.16 cr/ad (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Facebook/Instagram ads scraping.
- **Endpoints (2):**

  - `POST /v1/meta-ads/search` - Search ads - **0.16 cr/ad (per_result)** - params: `search`, `country`, `adType`, `urls`, `maxItems`
  - `GET /v1/meta-ads/search/{jobId}` - Get Meta Ads search job result - **0 cr/call (per_call)** - params: `jobId`

### Google Ads

- **What:** Scrape Google Ads from the Ads Transparency Center — search by advertiser name, domain, or ID to get ad creatives, formats, dates, and preview URLs
- **Docs:** vendor https://adstransparency.google.com | ColdIQ https://coldiq.com/marketplace/apis/google-ads | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.21 cr/ad (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Google Ads Transparency scraping.
- **Endpoints (2):**

  - `POST /v1/google-ads/search` - Google Ads Scraper - **0.21 cr/ad (per_result)** - params: `searchTerms`, `domains`, `advertiserIds`, `region`, `maxAds`
  - `GET /v1/google-ads/search/{jobId}` - Get Google Ads job result - **0 cr/call (per_call)** - params: `jobId`

### Twitter Ads Scraper

- **What:** Scrape Twitter/X Ad Transparency Center — extract ad text, images, impressions, engagement metrics, and targeting details
- **Docs:** vendor https://ads.x.com/transparency | ColdIQ https://coldiq.com/marketplace/apis/twitter-ads-scraper | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.31 cr/result (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW. X ad transparency scraping.
- **Endpoints (2):**

  - `POST /v1/twitter-ads-scraper/search` - Search Ads - **0.31 cr/result (per_result)** - params: `searchTerms`, `maxItems`, `country`, `startDate`, `endDate`
  - `GET /v1/twitter-ads-scraper/search/{jobId}` - Get Twitter Ads search job result - **0 cr/call (per_call)** - params: `jobId`

## Web search, crawling & SEO

### Exa

- **What:** AI-powered semantic web search & crawling
- **Docs:** vendor https://docs.exa.ai/ | ColdIQ https://coldiq.com/marketplace/apis/exa | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x5; 1.05 cr/call (per_call) x1; 1.05 cr/content page (per_result) x1; 10.5 cr/call (per_call) x1 ...
- **Relevance (LinkedIn-first sourcing):** LOW-MEDIUM. Semantic web search/crawl for research and signals (repo already has a direct Exa key).
- **Endpoints (9):**

  - `POST /v1/exa/search` - Search - **1.05 cr/call (per_call)** - params: `query`, `type`, `category`, `numResults`, `additionalQueries`, `includeDomains`, `excludeDomains`, `startPublishedDate`, `endPublishedDate`, `userLocation` (+5)
  - `POST /v1/exa/contents` - Get Contents - **1.05 cr/content page (per_result)** - params: `text`, `highlights`, `summary`, `livecrawlTimeout`, `maxAgeHours`, `subpages`, `subpageTarget`, `extras`, `ids`, `urls`
  - `POST /v1/exa/answer` - Answer - **10.5 cr/call (per_call)** - params: `query`, `stream`, `text`, `outputSchema`
  - `POST /v1/exa/agent/runs` - Create a run - **21 cr/run (per_call)** - params: `input.data`, `input.exclusion`, `query`, `systemPrompt`, `outputSchema`, `effort`, `previousRunId`, `metadata`
  - `GET /v1/exa/agent/runs` - List runs - **0 cr/call (per_call)** - params: `limit`, `cursor`
  - `GET /v1/exa/agent/runs/{id}` - Get a run - **0 cr/call (per_call)** - params: `id`
  - `DELETE /v1/exa/agent/runs/{id}` - Delete a run - **0 cr/call (per_call)** - params: `id`
  - `POST /v1/exa/agent/runs/{id}/cancel` - Cancel a run - **0 cr/call (per_call)** - params: `id`
  - `GET /v1/exa/agent/runs/{id}/events` - List run events - **0 cr/call (per_call)** - params: `id`, `limit`, `cursor`

### Jina

- **What:** Usage-based web reading, search, reranking, zero-shot classification, grounding, segmentation, and deep research — no Jina account required
- **Docs:** vendor https://docs.jina.ai/ | ColdIQ https://coldiq.com/marketplace/apis/jina | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** token=1.05e-05 cr/token used (per_result) x6; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Web reader/search/rerank/classify, token-billed - research utility.
- **Endpoints (7):**

  - `POST /v1/jina/reader` - Read URL - **token=1.05e-05 cr/token used (per_result)** - params: `url`, `targetSelector`, `removeSelector`, `waitForSelector`, `withGeneratedAlt`, `withImagesSummary`, `withLinksSummary`, `timeout`, `noCache`, `tokenBudget`
  - `POST /v1/jina/search` - Search - **token=1.05e-05 cr/token used (per_result)** - params: `q`, `count`, `page`, `type`, `gl`, `hl`
  - `POST /v1/jina/rerank` - Rerank documents - **token=1.05e-05 cr/token used (per_result)** - params: `model`, `query`, `documents`, `top_n`, `return_documents`
  - `POST /v1/jina/classify` - Classify text - **token=1.05e-05 cr/token used (per_result)** - params: `model`, `labels`
  - `POST /v1/jina/grounding` - Ground a statement - **token=1.05e-05 cr/token used (per_result)** - params: `statement`, `references`
  - `POST /v1/jina/segment` - Tokenize and segment text - **0 cr/call (per_call)** - params: `content`, `tokenizer`, `return_tokens`, `return_chunks`, `max_chunk_length`, `head`, `tail`
  - `POST /v1/jina/deepsearch` - DeepSearch - **token=1.05e-05 cr/token used (per_result)** - params: `messages`, `reasoning_effort`, `budget_tokens`, `max_attempts`, `boost_hostnames`, `bad_hostnames`, `only_hostnames`, `max_returned_urls`, `search_provider`, `stream`

### Serper

- **What:** Real-time Google Search API — web, news, images, videos, places, shopping, scholar, patents, and autocomplete results in structured JSON
- **Docs:** vendor https://serper.dev/playground | ColdIQ https://coldiq.com/marketplace/apis/serper | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.063 cr/call (per_call) x9
- **Relevance (LinkedIn-first sourcing):** LOW-MEDIUM. Very cheap Google SERP (0.063 cr/call) - useful for "site:linkedin.com/in" style URL resolution and research.
- **Endpoints (9):**

  - `POST /v1/serper/search` - Google Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/news` - Google News Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/images` - Google Images Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/videos` - Google Videos Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/places` - Google Places Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/shopping` - Google Shopping Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/scholar` - Google Scholar Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/patents` - Google Patents Search - **0.063 cr/call (per_call)** - params: `q`, `num`, `page`, `gl`, `hl`, `location`, `tbs`, `autocorrect`
  - `POST /v1/serper/autocomplete` - Google Autocomplete - **0.063 cr/call (per_call)** - params: `q`, `gl`, `hl`

### DataForSEO

- **What:** SEO data platform — SERP results, keyword research, backlink analysis, domain analytics, traffic estimation, and on-page audits
- **Docs:** vendor https://docs.dataforseo.com/v3/ | ColdIQ https://coldiq.com/marketplace/apis/dataforseo | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 2.31 cr/result (per_result) x12; 0.13 cr/call (per_call) x5; 0.13 cr/result (per_result) x4; 0 cr/call (per_call) x4 ...
- **Relevance (LinkedIn-first sourcing):** LOW. SEO/SERP/backlink data.
- **Endpoints (39):**

  - `POST /v1/dataforseo/serp/youtube/locations` - YouTube Locations - **0.13 cr/call (per_call)** - params: `country_iso_code`, `location_type`, `location_name`
  - `POST /v1/dataforseo/serp/youtube/organic` - YouTube Organic Search - **0.13 cr/result (per_result)** - params: `keyword`, `location_name`, `language_code`, `device`, `os`, `block_depth`
  - `POST /v1/dataforseo/serp/youtube/video-info` - YouTube Video Info - **0.13 cr/call (per_call)** - params: `video_id`, `location_name`, `language_code`, `device`, `os`
  - `POST /v1/dataforseo/serp/youtube/video-comments` - YouTube Video Comments - **0.13 cr/result (per_result)** - params: `video_id`, `location_name`, `language_code`, `device`, `os`, `depth`
  - `POST /v1/dataforseo/serp/youtube/video-subtitles` - YouTube Video Subtitles - **0.13 cr/call (per_call)** - params: `video_id`, `location_name`, `language_code`, `subtitles_language`, `subtitles_translate_language`, `device`, `os`
  - `POST /v1/dataforseo/serp/{search_engine}/locations` - SERP Locations - **0.13 cr/call (per_call)** - params: `search_engine`, `country_iso_code`, `location_type`, `location_name`
  - `POST /v1/dataforseo/serp/{search_engine}/organic` - Organic SERP - **0.13 cr/result (per_result)** - params: `search_engine`, `keyword`, `language_code`, `location_name`, `depth`, `device`, `max_crawl_pages`, `people_also_ask_click_depth`
  - `POST /v1/dataforseo/keywords/google-ads/locations` - Google Ads Locations - **0.11 cr/call (per_call)** - params: `country_iso_code`, `location_type`, `location_name`
  - `POST /v1/dataforseo/keywords/google-ads/search-volume` - Google Ads Search Volume - **0.11 cr/keyword (per_result)** - params: `keywords`, `location_name`, `language_code`
  - `GET /v1/dataforseo/keywords/google-trends/categories` - Google Trends Categories - **0 cr/call (per_call)**
  - `POST /v1/dataforseo/keywords/google-trends/explore` - Google Trends Explore - **0.11 cr/call (per_call)** - params: `keywords`, `location_name`, `language_code`, `type`, `date_from`, `date_to`, `time_range`, `item_types`, `category_code`
  - `POST /v1/dataforseo/labs/ranked-keywords` - Ranked Keywords - **2.31 cr/result (per_result)** - params: `target`, `location_name`, `language_code`, `limit`, `offset`, `filters`, `order_by`, `include_subdomains`, `include_clickstream_data`, `item_types`
  - `POST /v1/dataforseo/labs/competitors-domain` - Competitors Domain - **2.31 cr/result (per_result)** - params: `target`, `location_name`, `language_code`, `ignore_synonyms`, `limit`, `offset`, `filters`, `order_by`, `exclude_top_domains`, `include_clickstream_data` (+1)
  - `POST /v1/dataforseo/labs/domain-rank-overview` - Domain Rank Overview - **2.31 cr/call (per_call)** - params: `target`, `location_name`, `language_code`, `ignore_synonyms`
  - `POST /v1/dataforseo/labs/keyword-ideas` - Keyword Ideas - **2.31 cr/result (per_result)** - params: `keywords`, `location_name`, `language_code`, `limit`, `offset`, `filters`, `order_by`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/related-keywords` - Related Keywords - **2.31 cr/result (per_result)** - params: `keyword`, `depth`, `location_name`, `language_code`, `limit`, `offset`, `filters`, `order_by`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/keyword-suggestions` - Keyword Suggestions - **2.31 cr/result (per_result)** - params: `keyword`, `location_name`, `language_code`, `limit`, `offset`, `filters`, `order_by`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/historical-serp` - Historical SERP - **2.31 cr/call (per_call)** - params: `keyword`, `location_name`, `language_code`
  - `POST /v1/dataforseo/labs/serp-competitors` - SERP Competitors - **2.31 cr/result (per_result)** - params: `keywords`, `location_name`, `language_code`, `limit`, `offset`, `filters`, `order_by`, `include_subdomains`, `item_types`
  - `POST /v1/dataforseo/labs/bulk-keyword-difficulty` - Bulk Keyword Difficulty - **2.31 cr/keyword (per_result)** - params: `keywords`, `location_name`, `language_code`
  - `POST /v1/dataforseo/labs/subdomains` - Subdomains - **2.31 cr/result (per_result)** - params: `target`, `location_name`, `language_code`, `ignore_synonyms`, `limit`, `offset`, `filters`, `order_by`, `item_types`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/keyword-overview` - Keyword Overview - **2.31 cr/keyword (per_result)** - params: `keywords`, `location_name`, `language_code`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/top-searches` - Top Searches - **2.31 cr/result (per_result)** - params: `location_name`, `language_code`, `limit`, `offset`, `filters`, `order_by`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/search-intent` - Search Intent - **2.31 cr/keyword (per_result)** - params: `keywords`, `language_code`
  - `POST /v1/dataforseo/labs/keywords-for-site` - Keywords for Site - **2.31 cr/result (per_result)** - params: `target`, `location_name`, `language_code`, `limit`, `offset`, `filters`, `order_by`, `include_subdomains`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/domain-intersection` - Domain Intersection - **2.31 cr/result (per_result)** - params: `target1`, `target2`, `location_name`, `language_code`, `ignore_synonyms`, `limit`, `offset`, `filters`, `order_by`, `intersections` (+2)
  - `POST /v1/dataforseo/labs/historical-rank-overview` - Historical Rank Overview - **2.31 cr/call (per_call)** - params: `target`, `location_name`, `language_code`, `ignore_synonyms`, `include_clickstream_data`
  - `POST /v1/dataforseo/labs/page-intersection` - Page Intersection - **2.31 cr/result (per_result)** - params: `pages`, `exclude_pages`, `intersection_mode`, `location_name`, `language_code`, `ignore_synonyms`, `limit`, `offset`, `filters`, `order_by` (+2)
  - `POST /v1/dataforseo/labs/bulk-traffic-estimation` - Bulk Traffic Estimation - **2.31 cr/target (per_result)** - params: `targets`, `location_name`, `language_code`, `ignore_synonyms`, `item_types`
  - `GET /v1/dataforseo/labs/available-filters` - Available Filters - **0 cr/call (per_call)**
  - `POST /v1/dataforseo/labs/historical-keyword-data` - Historical Keyword Data - **2.31 cr/keyword (per_result)** - params: `keywords`, `location_name`, `language_code`
  - `POST /v1/dataforseo/labs/relevant-pages` - Relevant Pages - **2.31 cr/result (per_result)** - params: `target`, `location_name`, `language_code`, `ignore_synonyms`, `limit`, `offset`, `filters`, `order_by`, `exclude_top_domains`, `item_types` (+1)
  - `POST /v1/dataforseo/domain-analytics/whois` - WHOIS Overview - **0.13 cr/result (per_result)** - params: `limit`, `offset`, `filters`, `order_by`, `is_claimed`
  - `GET /v1/dataforseo/domain-analytics/whois/available-filters` - WHOIS Available Filters - **0 cr/call (per_call)**
  - `POST /v1/dataforseo/domain-analytics/technologies` - Domain Technologies - **0.13 cr/call (per_call)** - params: `target`
  - `GET /v1/dataforseo/domain-analytics/technologies/available-filters` - Technologies Available Filters - **0 cr/call (per_call)**
  - `POST /v1/dataforseo/on-page/content-parsing` - Content Parsing - **0.26 cr/call (per_call)** - params: `url`, `enable_javascript`, `custom_user_agent`, `accept_language`
  - `POST /v1/dataforseo/on-page/instant-pages` - Instant Pages - **0.26 cr/call (per_call)** - params: `url`, `enable_javascript`, `custom_js`, `custom_user_agent`, `accept_language`
  - `POST /v1/dataforseo/on-page/lighthouse` - Lighthouse - **0.26 cr/call (per_call)** - params: `url`, `enable_javascript`, `custom_user_agent`, `accept_language`, `full_data`

## Social / web / local scraping

### Twitter

- **What:** Twitter (X) scraping — search, profile, list, and URL-based tweet extraction
- **Docs:** vendor https://x.com | ColdIQ https://coldiq.com/marketplace/apis/twitter | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.084 cr/tweet (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Tweet scraping.
- **Endpoints (2):**

  - `POST /v1/twitter/tweet-scraper/scrape` - Scrape tweets by keyword, handle, URL, or conversation ID. - **0.084 cr/tweet (per_result)** - params: `startUrls`, `searchTerms`, `twitterHandles`, `conversationIds`, `maxItems`, `sort`, `tweetLanguage`, `onlyVerifiedUsers`, `onlyTwitterBlue`, `onlyImage` (+15)
  - `GET /v1/twitter/tweet-scraper/scrape/{jobId}` - Get tweet scraper job result - **0 cr/call (per_call)** - params: `jobId`

### Reddit

- **What:** Scrape Reddit posts and comments by subreddit, post URL, or search query
- **Docs:** vendor https://reddit.com | ColdIQ https://coldiq.com/marketplace/apis/reddit | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0.16 cr/item (per_result) x1; 0 cr/call (per_call) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Reddit scraping.
- **Endpoints (2):**

  - `POST /v1/reddit/scrape` - Reddit Scraper - **0.16 cr/item (per_result)** - params: `startUrls`, `searchQueries`, `searchType`, `searchCommunityName`, `sort`, `time`, `maxItems`, `maxComments`, `includeComments`, `postDateLimit` (+1)
  - `GET /v1/reddit/scrape/{jobId}` - Get Reddit scrape job result - **0 cr/call (per_call)** - params: `jobId`

### Google Maps

- **What:** Scrape reviews and place data from Google Maps
- **Docs:** vendor https://maps.google.com | ColdIQ https://coldiq.com/marketplace/apis/google-maps | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x2; 0.084 cr/review (per_result) x1; 0.084 cr/place (per_result) x1
- **Relevance (LinkedIn-first sourcing):** LOW. Places/reviews scraping - local-business ICPs only.
- **Endpoints (4):**

  - `POST /v1/google-maps/reviews` - Scrape Google Maps reviews - **0.084 cr/review (per_result)** - params: `startUrls`, `maxReviews`, `reviewsSort`, `language`, `personalDataOptions`
  - `GET /v1/google-maps/reviews/{jobId}` - Get Google Maps reviews job result - **0 cr/call (per_call)** - params: `jobId`
  - `POST /v1/google-maps/scraper` - Google Maps Scraper - **0.084 cr/place (per_result)** - params: `searchStringsArray`, `startUrls`, `maxCrawledPlacesPerSearch`, `countryCode`, `city`, `language`, `includeOpeningHours`, `additionalInfo`
  - `GET /v1/google-maps/scraper/{jobId}` - Get Google Maps Scraper job result - **0 cr/call (per_call)** - params: `jobId`

### Influencers Club

- **What:** Creator intelligence platform — enrich influencer profiles by email or handle, discover creators with AI-powered filters, and find lookalikes across Instagram, TikTok, YouTube, Twitch, Twitter, and OnlyFans
- **Docs:** vendor https://docs.influencers.club/ | ColdIQ https://coldiq.com/marketplace/apis/influencers-club | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 125.58 cr/call (per_call) x3; 125.58 cr/result (per_result) x2
- **Relevance (LinkedIn-first sourcing):** NONE. Creator/influencer data (125.58 cr/call) - not B2B.
- **Endpoints (5):**

  - `POST /v1/influencers-club/creators/enrich/email` - Enrich by Email - **125.58 cr/call (per_call)** - params: `email`
  - `POST /v1/influencers-club/creators/enrich/handle/full` - Enrich by Handle - Full - **125.58 cr/call (per_call)** - params: `handle`, `platform`, `include_lookalikes`, `email_required`
  - `POST /v1/influencers-club/creators/enrich/handle/raw` - Enrich by Handle - Raw - **125.58 cr/call (per_call)** - params: `handle`, `platform`, `email_required`
  - `POST /v1/influencers-club/discovery` - Discovery - **125.58 cr/result (per_result)** - params: `platform`, `paging`, `sort`, `filters`
  - `POST /v1/influencers-club/discovery/creators/similar` - Find Lookalikes - **125.58 cr/result (per_result)** - params: `handle`, `platform`, `paging`, `filters`

## Outreach, sequencing & messaging (BYOK)

### Instantly

- **What:** Cold email outreach automation — campaigns, leads, email accounts, and deliverability
- **Docs:** vendor https://developer.instantly.ai | ColdIQ https://coldiq.com/marketplace/apis/instantly | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x147
- **BYOK:** needs your own account key (per-request key param or a dashboard connection); routes cost 0 ColdIQ credits.
- **Relevance (LinkedIn-first sourcing):** NONE for sourcing. Cold-email platform control (BYOK, free in credits).
- **Endpoints (147):**

  - `POST /v1/instantly/accounts` - Create Account
  - `GET /v1/instantly/accounts` - List Accounts
  - `POST /v1/instantly/accounts/warmup/enable` - Enable Warmup
  - `POST /v1/instantly/accounts/warmup/disable` - Disable Warmup
  - `GET /v1/instantly/accounts/ctd/status` - Get Custom Tracking Domain Status
  - `POST /v1/instantly/accounts/move` - Move Account
  - `POST /v1/instantly/accounts/warmup-analytics` - Get Warmup Analytics
  - `GET /v1/instantly/accounts/analytics/daily` - Get Daily Account Analytics
  - `POST /v1/instantly/accounts/test/vitals` - Test Account Vitals
  - `GET /v1/instantly/accounts/{email}` - Get Account
  - `PATCH /v1/instantly/accounts/{email}` - Patch Account
  - `DELETE /v1/instantly/accounts/{email}` - Delete Account
  - `POST /v1/instantly/accounts/{email}/pause` - Pause Account
  - `POST /v1/instantly/accounts/{email}/resume` - Resume Account
  - `POST /v1/instantly/accounts/{email}/mark-fixed` - Mark Account Fixed
  - `GET /v1/instantly/account-campaign-mappings/{email}` - Get Account Campaign Mappings
  - `POST /v1/instantly/campaigns` - Create Campaign
  - `GET /v1/instantly/campaigns` - List Campaigns
  - `GET /v1/instantly/campaigns/count-launched` - Get Launched Campaign Count
  - `GET /v1/instantly/campaigns/search-by-contact` - Search Campaigns by Contact
  - `GET /v1/instantly/campaigns/analytics` - Get Campaign Analytics
  - `GET /v1/instantly/campaigns/analytics/overview` - Get Campaign Analytics Overview
  - `GET /v1/instantly/campaigns/analytics/daily` - Get Campaign Analytics Daily
  - `GET /v1/instantly/campaigns/analytics/steps` - Get Campaign Analytics Steps
  - `GET /v1/instantly/campaigns/{id}` - Get Campaign
  - `PATCH /v1/instantly/campaigns/{id}` - Patch Campaign
  - `DELETE /v1/instantly/campaigns/{id}` - Delete Campaign
  - `POST /v1/instantly/campaigns/{id}/activate` - Activate Campaign
  - `POST /v1/instantly/campaigns/{id}/pause` - Pause Campaign
  - `POST /v1/instantly/campaigns/{id}/share` - Share Campaign
  - `POST /v1/instantly/campaigns/{id}/export` - Export Campaign
  - `POST /v1/instantly/campaigns/{id}/duplicate` - Duplicate Campaign
  - `POST /v1/instantly/campaigns/{id}/variables` - Add Campaign Variables
  - `GET /v1/instantly/campaigns/{id}/sending-status` - Get Campaign Sending Status
  - `POST /v1/instantly/subsequences` - Create Subsequence
  - `GET /v1/instantly/subsequences` - List Subsequences
  - `GET /v1/instantly/subsequences/{id}` - Get Subsequence
  - `PATCH /v1/instantly/subsequences/{id}` - Patch Subsequence
  - `DELETE /v1/instantly/subsequences/{id}` - Delete Subsequence
  - `POST /v1/instantly/subsequences/{id}/duplicate` - Duplicate Subsequence
  - `POST /v1/instantly/subsequences/{id}/pause` - Pause Subsequence
  - `POST /v1/instantly/subsequences/{id}/resume` - Resume Subsequence
  - `GET /v1/instantly/subsequences/{id}/sending-status` - Get Subsequence Sending Status
  - `POST /v1/instantly/leads` - Create Lead
  - `DELETE /v1/instantly/leads` - Bulk Delete Leads
  - `POST /v1/instantly/leads/list` - List Leads
  - `POST /v1/instantly/leads/merge` - Merge Leads
  - `POST /v1/instantly/leads/add` - Bulk Add Leads
  - `POST /v1/instantly/leads/move` - Move Leads
  - `POST /v1/instantly/leads/bulk-assign` - Bulk Assign Leads
  - `POST /v1/instantly/leads/update-interest-status` - Update Lead Interest Status
  - `POST /v1/instantly/leads/subsequence/move` - Move Lead to Subsequence
  - `POST /v1/instantly/leads/subsequence/remove` - Remove Lead from Subsequence
  - `GET /v1/instantly/leads/{id}` - Get Lead
  - `PATCH /v1/instantly/leads/{id}` - Patch Lead
  - `DELETE /v1/instantly/leads/{id}` - Delete Lead
  - `POST /v1/instantly/lead-labels` - Create Lead Label
  - `GET /v1/instantly/lead-labels` - List Lead Labels
  - `POST /v1/instantly/lead-labels/ai-reply-label` - Test AI Reply Label Prediction
  - `GET /v1/instantly/lead-labels/{id}` - Get Lead Label
  - `PATCH /v1/instantly/lead-labels/{id}` - Patch Lead Label
  - `DELETE /v1/instantly/lead-labels/{id}` - Delete Lead Label
  - `POST /v1/instantly/lead-lists` - Create Lead List
  - `GET /v1/instantly/lead-lists` - List Lead Lists
  - `GET /v1/instantly/lead-lists/{id}` - Get Lead List
  - `PATCH /v1/instantly/lead-lists/{id}` - Patch Lead List
  - `DELETE /v1/instantly/lead-lists/{id}` - Delete Lead List
  - `GET /v1/instantly/lead-lists/{id}/verification-stats` - Get Lead List Verification Stats
  - `GET /v1/instantly/emails/unread/count` - Get Unread Email Count
  - `POST /v1/instantly/emails/test` - Send Test Email
  - `POST /v1/instantly/emails/reply` - Reply to Email
  - `POST /v1/instantly/emails/forward` - Forward Email
  - `POST /v1/instantly/emails/threads/{thread_id}/mark-as-read` - Mark Thread as Read
  - `GET /v1/instantly/emails` - List Emails
  - `GET /v1/instantly/emails/{id}` - Get Email
  - `PATCH /v1/instantly/emails/{id}` - Update Email
  - `DELETE /v1/instantly/emails/{id}` - Delete Email
  - `POST /v1/instantly/email-verification` - Create Email Verification
  - `GET /v1/instantly/email-verification/{email}` - Get Email Verification Status
  - `POST /v1/instantly/block-lists-entries` - Create Block List Entry
  - `GET /v1/instantly/block-lists-entries` - List Block List Entries
  - `DELETE /v1/instantly/block-lists-entries` - Delete All Block List Entries
  - `POST /v1/instantly/block-lists-entries/bulk-create` - Bulk Create Block List Entries
  - `POST /v1/instantly/block-lists-entries/bulk-delete` - Bulk Delete Block List Entries
  - `GET /v1/instantly/block-lists-entries/download` - Download Block List
  - `GET /v1/instantly/block-lists-entries/{id}` - Get Block List Entry
  - `PATCH /v1/instantly/block-lists-entries/{id}` - Patch Block List Entry
  - `DELETE /v1/instantly/block-lists-entries/{id}` - Delete Block List Entry
  - `POST /v1/instantly/custom-tags` - Create Custom Tag
  - `GET /v1/instantly/custom-tags` - List Custom Tags
  - `POST /v1/instantly/custom-tags/toggle-resource` - Toggle Tag Resource
  - `GET /v1/instantly/custom-tags/{id}` - Get Custom Tag
  - `PATCH /v1/instantly/custom-tags/{id}` - Patch Custom Tag
  - `DELETE /v1/instantly/custom-tags/{id}` - Delete Custom Tag
  - `GET /v1/instantly/custom-tag-mappings` - List Custom Tag Mappings
  - `POST /v1/instantly/webhooks` - Create Webhook
  - `GET /v1/instantly/webhooks` - List Webhooks
  - `GET /v1/instantly/webhooks/event-types` - List Webhook Event Types
  - `GET /v1/instantly/webhooks/{id}` - Get Webhook
  - `PATCH /v1/instantly/webhooks/{id}` - Patch Webhook
  - `DELETE /v1/instantly/webhooks/{id}` - Delete Webhook
  - `POST /v1/instantly/webhooks/{id}/test` - Test Webhook
  - `POST /v1/instantly/webhooks/{id}/resume` - Resume Webhook
  - `GET /v1/instantly/webhook-events` - List Webhook Events
  - `GET /v1/instantly/webhook-events/summary` - Get Webhook Event Summary
  - `GET /v1/instantly/webhook-events/summary-by-date` - Get Webhook Event Summary by Date
  - `GET /v1/instantly/webhook-events/{id}` - Get Webhook Event
  - `GET /v1/instantly/background-jobs` - List Background Jobs
  - `GET /v1/instantly/background-jobs/{id}` - Get Background Job
  - `GET /v1/instantly/audit-logs` - List Audit Logs
  - `POST /v1/instantly/inbox-placement-tests` - Create Inbox Placement Test
  - `GET /v1/instantly/inbox-placement-tests` - List Inbox Placement Tests
  - `GET /v1/instantly/inbox-placement-tests/email-service-provider-options` - Get Email Service Provider Options
  - `GET /v1/instantly/inbox-placement-tests/{id}` - Get Inbox Placement Test
  - `PATCH /v1/instantly/inbox-placement-tests/{id}` - Patch Inbox Placement Test
  - `DELETE /v1/instantly/inbox-placement-tests/{id}` - Delete Inbox Placement Test
  - `GET /v1/instantly/inbox-placement-analytics` - List Inbox Placement Analytics
  - `POST /v1/instantly/inbox-placement-analytics/stats-by-test-id` - Get Inbox Placement Stats by Test ID
  - `POST /v1/instantly/inbox-placement-analytics/deliverability-insights` - Get Inbox Placement Deliverability Insights
  - `POST /v1/instantly/inbox-placement-analytics/stats-by-date` - Get Inbox Placement Stats by Date
  - `GET /v1/instantly/inbox-placement-analytics/{id}` - Get Inbox Placement Analytics
  - `GET /v1/instantly/inbox-placement-reports` - List Inbox Placement Reports
  - `GET /v1/instantly/inbox-placement-reports/{id}` - Get Inbox Placement Report
  - `POST /v1/instantly/supersearch-enrichment` - Create SuperSearch Enrichment
  - `POST /v1/instantly/supersearch-enrichment/enrich-leads-from-supersearch` - Enrich Leads from SuperSearch
  - `POST /v1/instantly/supersearch-enrichment/run` - Run SuperSearch Enrichment
  - `POST /v1/instantly/supersearch-enrichment/count-leads-from-supersearch` - Count Leads from SuperSearch
  - `POST /v1/instantly/supersearch-enrichment/preview-leads-from-supersearch` - Preview Leads from SuperSearch
  - `POST /v1/instantly/supersearch-enrichment/ai` - Create AI Enrichment
  - `GET /v1/instantly/supersearch-enrichment/{resource_id}` - Get SuperSearch Enrichment Status
  - `GET /v1/instantly/supersearch-enrichment/ai/{resource_id}/in-progress` - Get AI Enrichment In-Progress Status
  - `GET /v1/instantly/supersearch-enrichment/history/{resource_id}` - Get SuperSearch Enrichment History
  - `PATCH /v1/instantly/supersearch-enrichment/{resource_id}/settings` - Update SuperSearch Enrichment Settings
  - `POST /v1/instantly/oauth/google/init` - Initialize Google OAuth
  - `POST /v1/instantly/oauth/microsoft/init` - Initialize Microsoft OAuth
  - `GET /v1/instantly/oauth/session/status/{sessionId}` - Get OAuth Session Status
  - `POST /v1/instantly/api-keys` - Create API Key
  - `GET /v1/instantly/api-keys` - List API Keys
  - `DELETE /v1/instantly/api-keys/{id}` - Delete API Key
  - `POST /v1/instantly/dfy-email-account-orders` - Place DFY Email Account Order
  - `GET /v1/instantly/dfy-email-account-orders` - List DFY Email Account Orders
  - `POST /v1/instantly/dfy-email-account-orders/domains/check` - Check Domain Availability
  - `POST /v1/instantly/dfy-email-account-orders/domains/similar` - Generate Similar Available Domains
  - `POST /v1/instantly/dfy-email-account-orders/domains/pre-warmed-up-list` - Get Pre-Warmed Up Domains
  - `GET /v1/instantly/dfy-email-account-orders/accounts` - List DFY Email Accounts
  - `POST /v1/instantly/dfy-email-account-orders/accounts/cancel` - Cancel DFY Email Accounts
  - `PATCH /v1/instantly/workspace` - Patch Workspace
  - *(parameters omitted here for this large provider; see catalog.json)*

### Lemlist

- **What:** Cold email & multichannel outreach platform — campaigns, leads, and personalization
- **Docs:** vendor https://developer.lemlist.com/ | ColdIQ https://coldiq.com/marketplace/apis/lemlist | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x38
- **BYOK:** needs your own account key (per-request key param or a dashboard connection); routes cost 0 ColdIQ credits.
- **Relevance (LinkedIn-first sourcing):** NONE for sourcing. Outreach platform control (BYOK, free).
- **Endpoints (38):**

  - `GET /v1/lemlist/campaigns` - List Campaigns - **0 cr/call (per_call)** - params: `limit`
  - `POST /v1/lemlist/campaigns` - Create Campaign - **0 cr/call (per_call)** - params: `name`, `type`, `scheduleIds`, `senderIds`, `labels`
  - `GET /v1/lemlist/campaigns/{campaignId}` - Get Campaign - **0 cr/call (per_call)** - params: `campaignId`
  - `PATCH /v1/lemlist/campaigns/{campaignId}` - Update Campaign - **0 cr/call (per_call)** - params: `campaignId`, `name`, `scheduleIds`, `senderIds`, `labels`
  - `POST /v1/lemlist/campaigns/{campaignId}/duplicate` - Duplicate Campaign - **0 cr/call (per_call)** - params: `campaignId`
  - `POST /v1/lemlist/campaigns/{campaignId}/start` - Start Campaign - **0 cr/call (per_call)** - params: `campaignId`
  - `POST /v1/lemlist/campaigns/{campaignId}/pause` - Pause Campaign - **0 cr/call (per_call)** - params: `campaignId`
  - `GET /v1/lemlist/campaigns/{campaignId}/stats` - Get Campaign Stats - **0 cr/call (per_call)** - params: `campaignId`, `startDate`, `endDate`, `timezone`
  - `POST /v1/lemlist/campaigns/{campaignId}/export` - Export Campaign Stats - **0 cr/call (per_call)** - params: `campaignId`
  - `GET /v1/lemlist/campaigns/{campaignId}/export-status` - Get Campaign Export Status - **0 cr/call (per_call)** - params: `campaignId`
  - `POST /v1/lemlist/campaigns/{campaignId}/leads` - Create Lead in Campaign - **0 cr/call (per_call)** - params: `campaignId`, `email`, `firstName`, `lastName`, `companyName`, `jobTitle`, `linkedinUrl`, `picture`, `phone`, `companyDomain` (+3)
  - `GET /v1/lemlist/campaigns/{campaignId}/leads` - List Campaign Leads - **0 cr/call (per_call)** - params: `campaignId`, `limit`, `offset`, `status`
  - `GET /v1/lemlist/leads/{leadId}` - Get Lead - **0 cr/call (per_call)** - params: `leadId`
  - `DELETE /v1/lemlist/leads/{leadId}` - Delete Lead - **0 cr/call (per_call)** - params: `leadId`
  - `PATCH /v1/lemlist/campaigns/{campaignId}/leads/{leadId}` - Update Lead in Campaign - **0 cr/call (per_call)** - params: `campaignId`, `leadId`, `email`, `firstName`, `lastName`, `companyName`, `jobTitle`, `linkedinUrl`, `picture`, `phone` (+4)
  - `POST /v1/lemlist/leads/{leadId}/variables` - Add Lead Variable - **0 cr/call (per_call)** - params: `leadId`, `name`, `value`
  - `PATCH /v1/lemlist/leads/{leadId}/variables` - Update Lead Variable - **0 cr/call (per_call)** - params: `leadId`, `name`, `value`
  - `DELETE /v1/lemlist/leads/{leadId}/variables` - Delete Lead Variable - **0 cr/call (per_call)** - params: `leadId`, `name`
  - `POST /v1/lemlist/leads/{leadId}/interested` - Mark Lead as Interested - **0 cr/call (per_call)** - params: `leadId`
  - `POST /v1/lemlist/leads/{leadId}/not-interested` - Mark Lead as Not Interested - **0 cr/call (per_call)** - params: `leadId`
  - `POST /v1/lemlist/leads/{leadId}/pause` - Pause Lead - **0 cr/call (per_call)** - params: `leadId`
  - `POST /v1/lemlist/leads/{leadId}/resume` - Resume Lead - **0 cr/call (per_call)** - params: `leadId`
  - `GET /v1/lemlist/contacts` - Get Contacts - **0 cr/call (per_call)** - params: `idsOrEmails`
  - `GET /v1/lemlist/contacts/{contactId}` - Get Contact - **0 cr/call (per_call)** - params: `contactId`
  - `GET /v1/lemlist/database/filters` - Get Database Filters - **0 cr/call (per_call)**
  - `POST /v1/lemlist/enrich` - Enrich Entity - **0 cr/call (per_call)** - params: `email`, `linkedinUrl`, `firstName`, `lastName`, `companyName`, `companyDomain`, `findEmail`, `findPhone`, `linkedinEnrichment`, `verifyEmail`
  - `POST /v1/lemlist/enrich/bulk` - Bulk Enrich Entities - **0 cr/call (per_call)** - params: `leads`
  - `POST /v1/lemlist/leads/{leadId}/enrich` - Enrich Lead - **0 cr/call (per_call)** - params: `leadId`
  - `GET /v1/lemlist/enrich/{enrichId}` - Get Enrichment Results - **0 cr/call (per_call)** - params: `enrichId`
  - `GET /v1/lemlist/unsubscribes` - List Unsubscribes - **0 cr/call (per_call)** - params: `limit`, `offset`
  - `POST /v1/lemlist/unsubscribes` - Add Unsubscribe - **0 cr/call (per_call)** - params: `email`
  - `GET /v1/lemlist/unsubscribes/{email}` - Get Unsubscribe Status - **0 cr/call (per_call)** - params: `email`
  - `DELETE /v1/lemlist/unsubscribes/{email}` - Remove Unsubscribe - **0 cr/call (per_call)** - params: `email`
  - `POST /v1/lemlist/unsubscribes/export` - Export Unsubscribes - **0 cr/call (per_call)**
  - `GET /v1/lemlist/activities` - List Activities - **0 cr/call (per_call)** - params: `campaignId`, `type`, `limit`, `offset`
  - `GET /v1/lemlist/team` - Get Team - **0 cr/call (per_call)**
  - `GET /v1/lemlist/team/credits` - Get Team Credits - **0 cr/call (per_call)**
  - `GET /v1/lemlist/team/senders` - List Team Senders - **0 cr/call (per_call)**

### Unipile

- **What:** Unified messaging & email API — manage LinkedIn, WhatsApp, Gmail, Outlook and more from a single integration: send messages, manage chats, sync emails, handle invitations, and post on social
- **Docs:** vendor https://developer.unipile.com/reference | ColdIQ https://coldiq.com/marketplace/apis/unipile | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x60
- **BYOK:** needs your own account key (per-request key param or a dashboard connection); routes cost 0 ColdIQ credits.
- **Relevance (LinkedIn-first sourcing):** LOW. LinkedIn/WhatsApp/email messaging API (BYOK, free in credits) - outreach side, not sourcing.
- **Endpoints (60):**

  - `GET /v1/unipile/accounts` - List All Accounts
  - `POST /v1/unipile/accounts` - Connect Account
  - `POST /v1/unipile/accounts/hosted` - Connect Account via Hosted Auth
  - `GET /v1/unipile/accounts/{id}` - Retrieve Account
  - `DELETE /v1/unipile/accounts/{id}` - Delete Account
  - `PATCH /v1/unipile/accounts/{id}` - Update Account
  - `POST /v1/unipile/accounts/{id}/reconnect` - Reconnect Account
  - `GET /v1/unipile/accounts/{id}/resync` - Resync Account
  - `POST /v1/unipile/accounts/{id}/checkpoint/solve` - Solve Checkpoint
  - `POST /v1/unipile/accounts/{id}/checkpoint/resend` - Resend Checkpoint
  - `POST /v1/unipile/accounts/{id}/restart` - Restart Account
  - `GET /v1/unipile/chats` - List All Chats
  - `POST /v1/unipile/chats` - Start New Chat
  - `GET /v1/unipile/chats/{id}` - Retrieve Chat
  - `PATCH /v1/unipile/chats/{id}` - Update Chat
  - `DELETE /v1/unipile/chats/{id}` - Delete Chat
  - `GET /v1/unipile/chats/{chatId}/messages` - List Chat Messages
  - `POST /v1/unipile/chats/{chatId}/messages` - Send Message
  - `GET /v1/unipile/chats/{id}/attendees` - List Chat Attendees
  - `GET /v1/unipile/chats/{id}/sync` - Sync Chat
  - `GET /v1/unipile/messages` - List All Messages
  - `GET /v1/unipile/messages/{messageId}` - Retrieve Message
  - `PATCH /v1/unipile/messages/{messageId}` - Edit Message
  - `DELETE /v1/unipile/messages/{messageId}` - Delete Message
  - `POST /v1/unipile/messages/{messageId}/forward` - Forward Message
  - `POST /v1/unipile/messages/{messageId}/reactions` - Add Message Reaction
  - `GET /v1/unipile/users/attendees` - List Attendees
  - `GET /v1/unipile/users/me` - Get Own Profile
  - `GET /v1/unipile/users/invite/sent` - List Sent Invitations
  - `GET /v1/unipile/users/invite/received` - List Received Invitations
  - `POST /v1/unipile/users/invite/{inviteId}` - Handle Received Invitation
  - `DELETE /v1/unipile/users/invite/{inviteId}` - Cancel Sent Invitation
  - `GET /v1/unipile/emails` - List Emails
  - `POST /v1/unipile/emails` - Send Email
  - `GET /v1/unipile/emails/contacts` - List Email Contacts
  - `GET /v1/unipile/emails/{mailId}` - Retrieve Email
  - `PUT /v1/unipile/emails/{mailId}` - Update Email
  - `DELETE /v1/unipile/emails/{mailId}` - Delete Email
  - `GET /v1/unipile/folders` - List Email Folders
  - `GET /v1/unipile/folders/{folderId}` - Retrieve Email Folder
  - `POST /v1/unipile/drafts` - Create Email Draft
  - `GET /v1/unipile/linkedin/search/parameters` - Get LinkedIn Search Parameters
  - `POST /v1/unipile/linkedin/search` - Execute LinkedIn Search
  - `GET /v1/unipile/linkedin/jobs` - List LinkedIn Job Postings
  - `POST /v1/unipile/linkedin/jobs` - Create LinkedIn Job Posting
  - `GET /v1/unipile/linkedin/jobs/{jobId}` - Retrieve LinkedIn Job Posting
  - `PATCH /v1/unipile/linkedin/jobs/{jobId}` - Update LinkedIn Job Posting
  - `POST /v1/unipile/linkedin/jobs/{jobId}/publish` - Publish LinkedIn Job Posting
  - `POST /v1/unipile/linkedin/jobs/{jobId}/close` - Close LinkedIn Job Posting
  - `GET /v1/unipile/linkedin/jobs/{jobId}/applicants` - List Job Applicants
  - `GET /v1/unipile/webhooks` - List Webhooks
  - `POST /v1/unipile/webhooks` - Create Webhook
  - `DELETE /v1/unipile/webhooks/{webhookId}` - Delete Webhook
  - `GET /v1/unipile/calendars` - List Calendars
  - `GET /v1/unipile/calendars/{calendarId}` - Retrieve Calendar
  - `GET /v1/unipile/calendars/{calendarId}/events` - List Calendar Events
  - `POST /v1/unipile/calendars/{calendarId}/events` - Create Calendar Event
  - `GET /v1/unipile/calendars/{calendarId}/events/{eventId}` - Retrieve Calendar Event
  - `PATCH /v1/unipile/calendars/{calendarId}/events/{eventId}` - Update Calendar Event
  - `DELETE /v1/unipile/calendars/{calendarId}/events/{eventId}` - Delete Calendar Event
  - *(parameters omitted here for this large provider; see catalog.json)*

## CRM (BYOK)

### Attio

- **What:** CRM platform — manage people, companies, notes, tasks, and search across records
- **Docs:** vendor https://developers.attio.com/reference | ColdIQ https://coldiq.com/marketplace/apis/attio | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x22
- **BYOK:** needs your own account key (per-request key param or a dashboard connection); routes cost 0 ColdIQ credits.
- **Relevance (LinkedIn-first sourcing):** NONE for sourcing. CRM (BYOK, free).
- **Endpoints (22):**

  - `POST /v1/attio/people/query` - List person records - **0 cr/call (per_call)** - params: `filter`, `sorts`, `limit`, `offset`
  - `POST /v1/attio/people` - Create a person record - **0 cr/call (per_call)** - params: `data`
  - `PUT /v1/attio/people` - Assert a person record - **0 cr/call (per_call)** - params: `matching_attribute`, `data`
  - `GET /v1/attio/people/{record_id}` - Get a person record - **0 cr/call (per_call)** - params: `record_id`
  - `PATCH /v1/attio/people/{record_id}` - Update a person record - **0 cr/call (per_call)** - params: `record_id`, `data`
  - `DELETE /v1/attio/people/{record_id}` - Delete a person record - **0 cr/call (per_call)** - params: `record_id`
  - `POST /v1/attio/companies/query` - List company records - **0 cr/call (per_call)** - params: `filter`, `sorts`, `limit`, `offset`
  - `POST /v1/attio/companies` - Create a company record - **0 cr/call (per_call)** - params: `data`
  - `PUT /v1/attio/companies` - Assert a company record - **0 cr/call (per_call)** - params: `matching_attribute`, `data`
  - `GET /v1/attio/companies/{record_id}` - Get a company record - **0 cr/call (per_call)** - params: `record_id`
  - `PATCH /v1/attio/companies/{record_id}` - Update a company record - **0 cr/call (per_call)** - params: `record_id`, `data`
  - `DELETE /v1/attio/companies/{record_id}` - Delete a company record - **0 cr/call (per_call)** - params: `record_id`
  - `POST /v1/attio/notes` - Create a note - **0 cr/call (per_call)** - params: `data`
  - `GET /v1/attio/notes` - List notes - **0 cr/call (per_call)** - params: `parent_object`, `parent_record_id`, `limit`, `offset`
  - `GET /v1/attio/notes/{note_id}` - Get a note - **0 cr/call (per_call)** - params: `note_id`
  - `DELETE /v1/attio/notes/{note_id}` - Delete a note - **0 cr/call (per_call)** - params: `note_id`
  - `POST /v1/attio/tasks` - Create a task - **0 cr/call (per_call)** - params: `data`
  - `GET /v1/attio/tasks` - List all tasks - **0 cr/call (per_call)** - params: `limit`, `offset`, `sort`, `linked_object`, `linked_record_id`, `assignee`, `is_completed`
  - `GET /v1/attio/tasks/{task_id}` - Get a task - **0 cr/call (per_call)** - params: `task_id`
  - `PATCH /v1/attio/tasks/{task_id}` - Update a task - **0 cr/call (per_call)** - params: `task_id`, `data`
  - `DELETE /v1/attio/tasks/{task_id}` - Delete a task - **0 cr/call (per_call)** - params: `task_id`
  - `POST /v1/attio/records/search` - Search records - **0 cr/call (per_call)** - params: `query`, `objects`, `request_as`, `limit`

## ColdIQ-native products

### Visitor ID

- **What:** ColdIQ Visitor ID — turn anonymous website traffic into identified people and companies. Install a tracking pixel on any site you own (one per client, for agencies) and get verified emails, titles, LinkedIn profiles, firmographics, page-visit activity, lead scores, and real-time webhooks. Credits are charged per identified person or company, never for setup or reads
- **Docs:** vendor https://coldiq.com/marketplace | ColdIQ https://coldiq.com/marketplace/apis/visitor-id | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x20
- **Relevance (LinkedIn-first sourcing):** LOW-MEDIUM. Website visitor de-anonymization incl. LinkedIn profiles; needs a pixel on a client site.
- **Endpoints (20):**

  - `GET /v1/visitor-id/websites` - List Websites - **0 cr/call (per_call)**
  - `POST /v1/visitor-id/websites` - Add Website - **0 cr/call (per_call)** - params: `domain`, `name`
  - `GET /v1/visitor-id/websites/{website_id}` - Get Website - **0 cr/call (per_call)** - params: `website_id`
  - `PATCH /v1/visitor-id/websites/{website_id}` - Update Website - **0 cr/call (per_call)** - params: `website_id`, `name`, `domain`, `monthly_limit_credits`
  - `DELETE /v1/visitor-id/websites/{website_id}` - Remove Website - **0 cr/call (per_call)** - params: `website_id`
  - `POST /v1/visitor-id/websites/{website_id}/resume` - Resume Identification - **0 cr/call (per_call)** - params: `website_id`
  - `GET /v1/visitor-id/websites/{website_id}/usage` - Get Usage - **0 cr/call (per_call)** - params: `website_id`
  - `GET /v1/visitor-id/websites/{website_id}/contacts` - List Identified People - **0 cr/call (per_call)** - params: `website_id`, `limit`, `cursor`, `filters`, `filter_set_id`, `email`, `account_id`
  - `GET /v1/visitor-id/websites/{website_id}/contacts/{contact_id}` - Get Identified Person - **0 cr/call (per_call)** - params: `website_id`, `contact_id`
  - `GET /v1/visitor-id/websites/{website_id}/accounts` - List Identified Companies - **0 cr/call (per_call)** - params: `website_id`, `limit`, `cursor`, `filters`, `filter_set_id`, `domain`
  - `GET /v1/visitor-id/websites/{website_id}/accounts/{account_id}` - Get Identified Company - **0 cr/call (per_call)** - params: `website_id`, `account_id`
  - `GET /v1/visitor-id/websites/{website_id}/activity` - Get Visit Activity - **0 cr/call (per_call)** - params: `website_id`, `account_id`, `contact_id`, `limit`, `cursor`
  - `GET /v1/visitor-id/websites/{website_id}/scores` - Get Lead Score - **0 cr/call (per_call)** - params: `website_id`, `account_id`, `contact_id`, `include_history`, `limit`, `cursor`
  - `GET /v1/visitor-id/websites/{website_id}/scores/recent` - List Recent Lead Scores - **0 cr/call (per_call)** - params: `website_id`, `limit`, `cursor`
  - `PUT /v1/visitor-id/websites/{website_id}/webhook` - Set Event Webhook - **0 cr/call (per_call)** - params: `website_id`, `url`, `events`
  - `GET /v1/visitor-id/websites/{website_id}/webhook` - Get Event Webhook - **0 cr/call (per_call)** - params: `website_id`
  - `DELETE /v1/visitor-id/websites/{website_id}/webhook` - Remove Event Webhook - **0 cr/call (per_call)** - params: `website_id`
  - `PUT /v1/visitor-id/websites/{website_id}/slack-alerts` - Set Slack Alerts - **0 cr/call (per_call)** - params: `website_id`, `slack_team_id`, `channel_id`
  - `GET /v1/visitor-id/websites/{website_id}/slack-alerts` - Get Slack Alerts - **0 cr/call (per_call)** - params: `website_id`
  - `DELETE /v1/visitor-id/websites/{website_id}/slack-alerts` - Remove Slack Alerts - **0 cr/call (per_call)** - params: `website_id`

### ColdIQ Mailbox

- **What:** ColdIQ Mailbox — managed cold-email sending infrastructure with your API key: price and buy sending domains and Google or Microsoft inboxes, read their status, reveal credentials and connect inboxes to your sending tool (Instantly, Smartlead, Lemlist and more). Purchases return a hosted payment link plus the dashboard order page; provisioning starts once payment is confirmed. Mailboxes are billed as subscriptions, never in credits — every route here costs 0 credits. Credentials responses are live secrets: keep them out of chat transcripts and shared channels
- **Docs:** vendor https://coldiq.com/marketplace | ColdIQ https://coldiq.com/marketplace/apis/coldiq-mailbox | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** 0 cr/call (per_call) x24
- **Relevance (LinkedIn-first sourcing):** NONE for sourcing. Buy domains/inboxes (subscription-billed, 0 credits).
- **Endpoints (24):**

  - `GET /v1/mailboxes/catalog` - Get Mailbox Catalog - **0 cr/call (per_call)**
  - `GET /v1/mailboxes/domains/availability` - Check Domain Availability - **0 cr/call (per_call)** - params: `domain`
  - `POST /v1/mailboxes/domains/availability` - Check Domain Availability In Bulk - **0 cr/call (per_call)** - params: `domains`
  - `POST /v1/mailboxes/quotes` - Price A Mailbox Order - **0 cr/call (per_call)**
  - `POST /v1/mailboxes/purchases` - Buy Mailboxes - **0 cr/call (per_call)** - params: `Idempotency-Key`, `quoteId`, `idempotencyKey`
  - `GET /v1/mailboxes/purchases` - List Mailbox Purchases - **0 cr/call (per_call)**
  - `POST /v1/mailboxes/carts` - Buy Google And Microsoft Mailboxes Together - **0 cr/call (per_call)** - params: `Idempotency-Key`, `quoteIds`, `idempotencyKey`
  - `GET /v1/mailboxes/purchases/{purchaseId}` - Get Mailbox Purchase - **0 cr/call (per_call)** - params: `purchaseId`
  - `GET /v1/mailboxes/domains` - List Sending Domains - **0 cr/call (per_call)** - params: `status`, `provider_type`
  - `GET /v1/mailboxes/integrations` - List Sending Tools - **0 cr/call (per_call)**
  - `GET /v1/mailboxes/integrations/{sequencer}/connections` - List Sending Tool Connections - **0 cr/call (per_call)** - params: `sequencer`
  - `POST /v1/mailboxes/integrations/{sequencer}/connections` - Save Sending Tool Connection - **0 cr/call (per_call)** - params: `sequencer`, `name`, `setupToken`
  - `POST /v1/mailboxes/integrations/{sequencer}/connections/validate` - Validate Sending Tool Credentials - **0 cr/call (per_call)** - params: `sequencer`, `name`, `credentials`
  - `DELETE /v1/mailboxes/integrations/{sequencer}/connections/{connectionId}` - Remove Sending Tool Connection - **0 cr/call (per_call)** - params: `sequencer`, `connectionId`
  - `POST /v1/mailboxes/integrations/{sequencer}` - Connect Mailboxes To A Sending Tool - **0 cr/call (per_call)** - params: `sequencer`, `mailboxIds`, `connectionId`
  - `GET /v1/mailboxes/subscriptions` - List Mailbox Subscriptions - **0 cr/call (per_call)**
  - `GET /v1/mailboxes/orders` - List Mailbox Orders - **0 cr/call (per_call)** - params: `status`
  - `GET /v1/mailboxes/orders/{id}` - Get Order Status - **0 cr/call (per_call)** - params: `id`
  - `GET /v1/mailboxes/orders/{id}/nameservers` - Get Microsoft Order Nameservers - **0 cr/call (per_call)** - params: `id`
  - `POST /v1/mailboxes/exports` - Export Mailboxes To A Sending Tool - **0 cr/call (per_call)** - params: `mailbox_ids`, `sequencer`, `username`, `password`, `app_workspace_name`, `client_id`, `url`
  - `GET /v1/mailboxes` - List Mailboxes - **0 cr/call (per_call)** - params: `domain_id`, `status`
  - `GET /v1/mailboxes/{id}` - Get Mailbox - **0 cr/call (per_call)** - params: `id`
  - `GET /v1/mailboxes/{id}/credentials` - Reveal Mailbox Credentials - **0 cr/call (per_call)** - params: `id`, `totp`
  - `DELETE /v1/mailboxes/{id}/integrations` - Disconnect Mailbox From Its Sending Tool - **0 cr/call (per_call)** - params: `id`

### Mailboxes

- **What:** Dashboard (session-auth) mailbox purchase/management routes mirroring ColdIQ Mailbox.
- **Docs:** vendor - | ColdIQ - | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** NONE. Dashboard-session versions of the mailbox routes (not usable with the API key).
- **Endpoints (36):**

  - `GET /dashboard/mailboxes/catalog` - Mailbox catalog — prices, limits and purchase availability
  - `GET /dashboard/mailboxes/domains/availability` - Check domain availability - params: `domain`
  - `POST /dashboard/mailboxes/domains/availability` - Check domain availability in bulk - params: `domains`
  - `POST /dashboard/mailboxes/domains` - Buy sending domains - params: `domains`
  - `GET /dashboard/mailboxes/domains` - List your sending domains - params: `status`, `provider_type`
  - `DELETE /dashboard/mailboxes/domains/{id}` - Delete a domain and its mailboxes - params: `id`, `confirm`
  - `DELETE /dashboard/mailboxes/domains/{id}/mailboxes` - Release every inbox on a domain, keeping the domain - params: `id`, `confirm`
  - `POST /dashboard/mailboxes` - Create mailboxes on a domain - params: `domain_id`, `mailboxes`
  - `GET /dashboard/mailboxes` - List your mailboxes - params: `domain_id`, `status`
  - `POST /dashboard/mailboxes/quotes` - Price a mailbox order
  - `POST /dashboard/mailboxes/purchases` - Create a mailbox purchase from a quote - params: `quoteId`, `idempotencyKey`
  - `GET /dashboard/mailboxes/purchases` - List your mailbox purchases
  - `POST /dashboard/mailboxes/carts` - Create a combined mailbox order from several quotes - params: `quoteIds`, `idempotencyKey`
  - `GET /dashboard/mailboxes/purchases/{purchaseId}` - Get one mailbox purchase - params: `purchaseId`
  - `GET /dashboard/mailboxes/integrations` - List supported sending tools
  - `GET /dashboard/mailboxes/integrations/{sequencer}/connections` - List sending-tool connections - params: `sequencer`
  - `POST /dashboard/mailboxes/integrations/{sequencer}/connections` - Save a sending-tool connection - params: `sequencer`, `name`, `setupToken`
  - `POST /dashboard/mailboxes/integrations/{sequencer}/connections/validate` - Validate sending-tool credentials - params: `sequencer`, `name`, `credentials`
  - `DELETE /dashboard/mailboxes/integrations/{sequencer}/connections/{connectionId}` - Remove a sending-tool connection - params: `sequencer`, `connectionId`
  - `POST /dashboard/mailboxes/integrations/{sequencer}` - Add inboxes to a sending tool - params: `sequencer`, `mailboxIds`, `connectionId`
  - `GET /dashboard/mailboxes/credentials.csv` - Download inbox credentials as CSV - params: `mailboxIds`
  - `GET /dashboard/mailboxes/subscriptions` - List your mailbox subscriptions
  - `GET /dashboard/mailboxes/orders` - List your mailbox orders - params: `status`
  - `GET /dashboard/mailboxes/{id}` - Get a mailbox - params: `id`
  - `DELETE /dashboard/mailboxes/{id}` - Delete a mailbox - params: `id`
  - `DELETE /dashboard/mailboxes/{id}/integrations` - Remove an inbox from its sending tool - params: `id`
  - `GET /dashboard/mailboxes/{id}/credentials` - Reveal mailbox credentials - params: `id`, `totp`
  - `POST /dashboard/mailboxes/orders/microsoft` - Order Microsoft mailboxes - params: `domain`, `is_purchase`, `mailbox_mode`, `full_name`, `mailboxes`, `inbox_provider_id`, `sequencer_connection`
  - `GET /dashboard/mailboxes/orders/{id}` - Get order status - params: `id`
  - `DELETE /dashboard/mailboxes/orders/{id}` - Delete a Microsoft order - params: `id`, `confirm`
  - `GET /dashboard/mailboxes/orders/{id}/nameservers` - Get Microsoft order nameservers - params: `id`
  - `POST /dashboard/mailboxes/domains/{id}/inboxes/stop-renewal` - Stop inbox billing at period end - params: `id`
  - `POST /dashboard/mailboxes/domains/{id}/inboxes/resume` - Resume inbox billing - params: `id`
  - `POST /dashboard/mailboxes/orders/{id}/stop-renewal` - Stop Microsoft order billing at period end - params: `id`
  - `POST /dashboard/mailboxes/orders/{id}/resume` - Resume Microsoft order billing - params: `id`
  - `POST /dashboard/mailboxes/exports` - Export mailboxes to a sequencer - params: `mailbox_ids`, `sequencer`, `username`, `password`, `app_workspace_name`, `client_id`, `url`

## Account, billing & workspace admin

### Account

- **What:** API-key account endpoints: credit balance and feedback.
- **Docs:** vendor - | ColdIQ - | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** USEFUL. GET /v1/me/credits is the free balance + usd_per_credit check.
- **Endpoints (2):**

  - `GET /v1/me/credits` - Get credit balance
  - `POST /v1/feedback` - Send feedback - params: `message`, `endpoint`, `severity`, `metadata`

### Public

- **What:** Unauthenticated public billing/product listings.
- **Docs:** vendor - | ColdIQ - | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** Info only. Public price lists (no auth).
- **Endpoints (3):**

  - `GET /public/billing/products` - List credit packages (public)
  - `GET /public/billing/lite-products` - List Find Anything plans (public)
  - `POST /public/billing/campaign-checkout` - Create campaign checkout session - params: `priceId`, `utmSource`

### Dashboard

- **What:** Web dashboard routes: billing, API keys, usage, credits, quota, Visitor ID websites.
- **Docs:** vendor - | ColdIQ - | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** Admin. Requires a dashboard session JWT - API key returns 401 "Malformed session token".
- **Endpoints (40):**

  - `GET /dashboard/billing/products` - List credit packages
  - `POST /dashboard/billing/checkout` - Create checkout session - params: `priceId`, `successUrl`, `cancelUrl`
  - `POST /dashboard/billing/top-up/preview` - Preview credit top-up - params: `priceId`
  - `POST /dashboard/billing/top-up/payment-intent` - Create credit top-up PaymentIntent - params: `priceId`, `amount`, `credits`, `idempotencyKey`
  - `POST /dashboard/billing/plan-change/preview` - Preview subscription plan change - params: `priceId`
  - `POST /dashboard/billing/plan-change/confirm` - Confirm subscription plan change - params: `priceId`, `prorationDate`, `amountDue`, `idempotencyKey`
  - `POST /dashboard/billing/redeem` - Redeem an offer code - params: `code`, `successUrl`, `cancelUrl`
  - `POST /dashboard/billing/portal` - Create billing portal session - params: `returnUrl`, `flow`
  - `GET /dashboard/billing/subscriptions` - List active subscriptions - params: `refresh`
  - `POST /dashboard/billing/pause` - Pause subscription - params: `resumesAt`
  - `POST /dashboard/billing/resume` - Resume subscription
  - `GET /dashboard/billing/invoices` - List billing invoices - params: `limit`, `startingAfter`
  - `GET /dashboard/quota` - Get remaining lookups
  - `POST /dashboard/signup-context` - Capture signup network context
  - `GET /dashboard/visitor-id/websites` - List websites
  - `POST /dashboard/visitor-id/websites` - Add a website - params: `domain`, `name`
  - `GET /dashboard/visitor-id/websites/{website_id}` - Get a website - params: `website_id`
  - `PATCH /dashboard/visitor-id/websites/{website_id}` - Update a website - params: `website_id`, `name`, `domain`, `monthly_limit_credits`
  - `DELETE /dashboard/visitor-id/websites/{website_id}` - Remove a website - params: `website_id`
  - `POST /dashboard/visitor-id/websites/{website_id}/resume` - Resume identification - params: `website_id`
  - `GET /dashboard/visitor-id/websites/{website_id}/usage` - Get usage - params: `website_id`
  - `GET /dashboard/visitor-id/websites/{website_id}/contacts` - List identified people - params: `website_id`, `limit`, `cursor`, `filters`, `filter_set_id`, `email`, `account_id`
  - `GET /dashboard/visitor-id/websites/{website_id}/contacts/{contact_id}` - Get an identified person - params: `website_id`, `contact_id`
  - `GET /dashboard/visitor-id/websites/{website_id}/accounts` - List identified companies - params: `website_id`, `limit`, `cursor`, `filters`, `filter_set_id`, `domain`
  - `GET /dashboard/visitor-id/websites/{website_id}/accounts/{account_id}` - Get an identified company - params: `website_id`, `account_id`
  - `GET /dashboard/visitor-id/websites/{website_id}/activity` - Get visit activity - params: `website_id`, `account_id`, `contact_id`, `limit`, `cursor`
  - `GET /dashboard/visitor-id/websites/{website_id}/scores` - Get lead score - params: `website_id`, `account_id`, `contact_id`, `include_history`, `limit`, `cursor`
  - `GET /dashboard/visitor-id/websites/{website_id}/scores/recent` - List recent lead scores - params: `website_id`, `limit`, `cursor`
  - `PUT /dashboard/visitor-id/websites/{website_id}/webhook` - Set the event webhook - params: `website_id`, `url`, `events`
  - `GET /dashboard/visitor-id/websites/{website_id}/webhook` - Get the event webhook - params: `website_id`
  - `DELETE /dashboard/visitor-id/websites/{website_id}/webhook` - Remove the event webhook - params: `website_id`
  - `GET /dashboard/me` - Get user profile
  - `GET /dashboard/api-keys` - List API keys
  - `POST /dashboard/api-keys` - Create API key - params: `name`
  - `DELETE /dashboard/api-keys/{id}` - Revoke API key - params: `id`
  - `GET /dashboard/credits` - Get credit balance
  - `GET /dashboard/usage` - Get usage history - params: `page`, `limit`, `provider`, `from`, `to`
  - `GET /dashboard/usage/export.csv` - Export usage history as CSV - params: `provider`, `from`, `to`
  - `GET /dashboard/usage/summary` - Get usage summary - params: `from`, `to`
  - `GET /dashboard/usage/summary/windows` - Get usage summary for the 7, 30 and 90 day windows

### Team

- **What:** Invite teammates into your workspace. Members get full access to the API on your subscription — their usage bills your credits, and only you manage billing.
- **Docs:** vendor - | ColdIQ https://coldiq.com/marketplace/apis/team | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** Admin (dashboard session).
- **Endpoints (6):**

  - `GET /dashboard/team` - Get your team and its members
  - `POST /dashboard/team/invitations` - Invite a member to your team - params: `email`, `role`
  - `DELETE /dashboard/team/invitations/{invitationId}` - Revoke a pending invitation - params: `invitationId`
  - `DELETE /dashboard/team/members/{userId}` - Remove a member from your team - params: `userId`
  - `PATCH /dashboard/team/members/{userId}` - Change a member's role - params: `userId`, `role`
  - `GET /dashboard/team/usage` - Get this month's team usage per member

### Slack

- **What:** Connect your Slack workspace to your ColdIQ team, so the agent answers any member in Slack and the team owner pays for it.
- **Docs:** vendor - | ColdIQ https://coldiq.com/marketplace/apis/slack | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** Admin (dashboard session).
- **Endpoints (2):**

  - `GET /dashboard/slack/connection` - Get the Slack workspace connected to your team
  - `DELETE /dashboard/slack/connection` - Disconnect your team from Slack - params: `slackTeamId`

### Connections

- **What:** Store/validate your own (BYOK) provider API keys.
- **Docs:** vendor - | ColdIQ - | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** Admin: where BYOK provider keys are stored (dashboard session).
- **Endpoints (6):**

  - `GET /dashboard/connections/providers` - List connectable BYOK providers
  - `GET /dashboard/connections` - List your connected tools
  - `PUT /dashboard/connections/{provider}` - Connect or update a tool - params: `provider`, `login`, `password`, `email`, `workspace_id`, `api_token`, `fallback_to_coldiq`
  - `PATCH /dashboard/connections/{provider}` - Update connection settings - params: `provider`, `fallback_to_coldiq`
  - `DELETE /dashboard/connections/{provider}` - Disconnect a tool - params: `provider`
  - `POST /dashboard/connections/{provider}/validate` - Re-validate a stored connection - params: `provider`

### Chats

- **What:** Saved ColdIQ agent chats.
- **Docs:** vendor - | ColdIQ - | reference https://api.coldiq.com/docs
- **Cost (spec x-credits-cost):** not stated (no x-credits-cost)
- **Relevance (LinkedIn-first sourcing):** Admin (dashboard session).
- **Endpoints (4):**

  - `GET /dashboard/chats` - List saved chats - params: `page`, `limit`, `status`
  - `GET /dashboard/chats/{publicId}` - Get a saved chat - params: `publicId`
  - `PATCH /dashboard/chats/{publicId}` - Rename or archive a saved chat - params: `publicId`, `title`, `status`
  - `DELETE /dashboard/chats/{publicId}` - Delete a saved chat - params: `publicId`

## Not in the gateway

coldiq.com/apis/<name>-api pages (e.g. hunter-api, rocketreach-api, saleshandy-api, valid8-api, servicenow-api, apify-api) are a generic **API directory** on ColdIQ's marketing site linking to each vendor's own docs - they are *not* routed through api.coldiq.com (verified on hunter/rocketreach/saleshandy pages; none has a `/v1/<vendor>` path in the spec). Hunter, RocketReach, Saleshandy, Smartlead, Clay, Blitz are not gateway providers (Smartlead appears only as a mailbox-export target).

## Caveats

- Costs are the spec's published `x-credits-cost`; descriptions say "call get_endpoint_details for the live rate" (an agent/MCP tool, not an HTTP route in the spec), so live rates may differ.
- No provider data endpoint was called during this research. Only free calls made: `/openapi.json`, `/docs`, `/health`, `GET /v1/me/credits`, `GET /public/billing/products`, `GET /public/billing/lite-products`, and three `/dashboard/*` reads (401).
- Async providers (Twitter, Reddit, Google Maps, ad libraries, job APIs) submit a job then poll a free `GET .../{jobId}`; that they are Apify actors underneath is *(inferred)* from the pattern only.