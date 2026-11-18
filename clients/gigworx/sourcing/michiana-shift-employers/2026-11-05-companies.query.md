# 2026-11-05 market sizing pull: Michiana shift employers

**Client:** GigWorx (`94da4a2f-8f90-4bc0-87e6-22ff98fafd6a`)
**Config:** GigWorx - Michiana shift employers (Clay people search) (`184a0f39-d738-4f8f-a908-3c97d71dd4cf`)
**Segment:** first pull for this config, so this opens a **new segment**. Nothing was pushed to Clay, HeyReach or `tracking_clients`.
**Why:** to size the market for the client analysis (`clients/gigworx/client-analysis.md`). The brief's estimate of 300–800 companies was an unvalidated guess.
**Pulled:** 2026-11-05, by the GigWorx per-client session on branch `claude/stoic-hawking-utkftq`.

## File 1: `2026-11-05-companies.csv` (4,378 companies)

Tool: **Blitz API `POST /v2/search/companies`**, paged with a cursor until `cursor: null`.

```json
{"company": {
  "hq": {"country_code": ["US"], "state": {"include": ["Indiana"]},
         "city": {"include": ["South Bend","Mishawaka","Granger","Osceola","North Liberty","Walkerton",
                              "Lakeville","New Carlisle","Notre Dame",
                              "Elkhart","Goshen","Nappanee","Middlebury","Bristol","Wakarusa","Millersburg","Dunlap"]}},
  "employee_range": ["11-50","51-200","201-500","501-1000","1001-5000","5001-10000","10001+"]},
 "max_results": 50}
```

The first 9 cities are in St. Joseph County and the other 8 are in Elkhart County. The pull returned 4,379 rows, which dedupe to 4,378 on `company_linkedin_url`.

The same filter was also run once per size band (with `max_results: 1`) to get counts only. The `1-10` band holds **9,183** companies. They were counted but not pulled, because the ICP config starts at 11 employees.

| Band | 1-10 | 11-50 | 51-200 | 201-500 | 501-1000 | 1001-5000 | 5001-10000 | 10001+ |
|---|---|---|---|---|---|---|---|---|
| Companies | 9,183 | 3,411 | 657 | 174 | 53 | 59 | 11 | 14 |

`icp_bucket` was set in this session from the Blitz LinkedIn `industry`:

- **manufacturing:** any `*Manufacturing` industry, plus Automotive, Mining, Consumer Goods, Food Production and Printing Services
- **warehousing-logistics:** `Wholesale*`, Truck Transportation, Transportation/Logistics/Supply Chain, Freight
- **retail:** `Retail*`
- **construction:** Construction and the trade/civil variants
- **hospitality-events-facilities:** Hospitality, Restaurants, F&B Services, Events, Entertainment, Recreational Facilities, Spectator Sports, Facilities Services
- **staffing-competitor:** Staffing and Recruiting
- **unknown-industry:** no industry in Blitz
- **out-of-icp:** everything else (health care, education, finance, nonprofits, software and so on)

**Known limits. Read these before reusing this file.**

1. **The search matches on headquarters, not site location.** Plants and warehouses run by companies headquartered outside the two counties are missing. The hiring-signal file below shows this gap is large.
2. **Industry tags are noisy.** At least 8 Gurley Leep car dealerships are tagged as manufacturing, Martin's Super Market is tagged as personal-care manufacturing, and Tire Rack (a distribution centre) is tagged as motor-vehicle manufacturing. The buckets are good enough for sizing, but rows need checking before outreach.
3. **City matching is by keyword.** Every row's `hq_state` is Indiana, but "Bristol" or "Granger" could in principle match a small entity's mailing address that isn't really in Michiana.

## File 2: `2026-11-05-hiring-signal-companies.csv` (140 companies)

Tool: **Blitz API `POST /v2/company/tam-by-jobs`**, paged until `cursor: null`.

```json
{"job": {"title": {"include": ["production","assembler","assembly","warehouse","general labor","laborer",
                               "material handler","forklift","machine operator","picker","packer","fabricator",
                               "welder","line worker","manufacturing associate","shipping","loader","sanitation",
                               "stocker","order selector"]},
         "location": {"city": {"include": ["South Bend","Mishawaka","Elkhart","Goshen","Nappanee"]},
                      "country_code": {"include": ["US"]}},
         "date_posted": {"last_days": 60}},
 "max_results": 50}
```

`job.location` accepts only `city` and `country_code`, not `state`. A first run that used all 17 cities returned towns with the same name in other states (Middlebury VT, Bristol CT and PA, Lakeville MN). The final run uses only the 5 main city names, which are distinctive. Elkhart, Goshen and South Bend do exist in other states, so a few false positives may remain.

The pull found **140 companies with 462 matching postings in the last 60 days**. **Only 32 of the 140 have their headquarters in Indiana.** Lippert (69 postings), SpartanNash, Lowe's, Vestis, Valmont, Smurfit Westrock and JBS all hire hourly staff locally from headquarters elsewhere. This is why file 1 under-counts, and why the lead list has to be built on **where the person works** (Clay people search by person location), not on company headquarters.

Coverage warning: hourly roles are mostly posted on Indeed and walk-in boards, so Blitz's job data catches only part of the real hiring. Treat this file as a sample of active hirers to prioritise, not as the full set.
