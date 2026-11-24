# GRN Piedmont: non-API list sources review (2026-11-24)

**What this is:** a check of whether free, non-API lists (association directories, trade-show
exhibitor lists, state economic-development pages) can feed GRN Piedmont's two ICP slices better
than database APIs. Prompted by the VNTANA finding (`clients/vntana/icp-universe-map.md`) that one
IMTS exhibitor list held 3x the client-confirmed ICP fits our taxonomy queries found.

**How:** free web access only (curl of public pages, public JSON behind public directory pages,
web search). No paid APIs, no logins, no credits spent. All fetches on 2026-11-24, roughly one
request per second.

**ICP slices tested against:**
- **MFG:** US manufacturers HQ'd in NC or SC, 201 to 1,000 employees.
- **FLS:** US fire and life safety companies (sprinkler/suppression contractors, alarm/detection
  integrators, ITM providers; F&LS equipment manufacturers flagged separately), HQ in an Eastern or
  Central time-zone state, 201 to 1,000 employees.

## Headline

1. **NFSA's contractor directory is fully public and fully extractable in one request.** The page
   `member.nfsa.org/Directories/Contractor-Directory` ships the whole directory inline in its HTML
   (no login): 1,500 company/branch rows with business type, street address, city, state and
   website. 1,044 are contractors (597 union, 447 open shop) and 456 are suppliers/manufacturers.
   In Eastern/Central states: 793 contractor rows that roll up to **468 distinct companies**, 58 of
   them with more than one listed location. This is the best F&LS discovery list found.
2. **IMTS 2026's Map Your Show directory has a working public JSON search with a state filter.**
   One call per state returns every exhibitor listed in that state: **52 NC + 17 SC = 69**. Names
   and descriptions only; the exhibitor detail pages (city, website) sit behind a bot check that
   returns HTTP 202 with no body.
3. **FABTECH 2025's printed show directory is a free PDF.** 1,652 unique booths parsed. No
   addresses, but 1,116 carry a phone number, and the area code gives a rough state: **36 NC/SC**.
4. **Both trade shows are a poor fit for GRN's MFG slice as discovery lists.** Their NC/SC
   exhibitors are mostly *equipment and tooling vendors selling to manufacturers*, often US sales
   arms of German, Italian or Japanese parents (Chiron America, Okuma America, Schunk, Zimmer, Weima).
   Many are well under 201 US employees. Contrast with VNTANA, whose ICP *was* the equipment makers.
   For GRN, a show exhibitor list is only useful where the show's exhibitors are the ICP itself.
5. **State economic-development announcements are a clean, free, regularly updated signal.** In the
   last 90 days (2026-08-26 to 2026-11-24): 22 SC company announcements and 17 NC company-level
   entries (11 company press releases plus 7 companies named in one Rural Infrastructure Authority
   grant release). Every SC release links the company website and LinkedIn page; NC releases name
   the company, county, jobs and investment but link no company site.

## Sources checked

Verdict key: **usable now** (free, extracted here) / **needs scraping tool** (public but needs
form automation, a headless browser, or a bot-check bypass) / **login-walled** / **not useful**
(public but wrong content for GRN's ICP) / **blocked** (site refused our requests).

### Fire and life safety (FLS slice)

| Source | URL fetched (2026-11-24) | Public, no login? | Approx size | Fields given | How to get at scale | Cost | Verdict |
|---|---|---|---|---|---|---|---|
| NFSA Contractor Directory | https://member.nfsa.org/Directories/Contractor-Directory (same payload at `/Directories/Buyers-Guide`) | Yes. Whole directory is inline in a 7.9 MB HTML page. | 1,500 company rows: 1,044 contractors, 456 suppliers/mfrs. ET/CT: 468 distinct contractor companies, 329 supplier rows. Also ~300 individual contact rows with emails (not extracted). | Company name, business type (Union Contractor / Open Shop Contractor / Supplier and Manufacturer), member flag, street address, city, state, ZIP, website (349 of 793 ET/CT contractor rows). No headcount. | One GET, parse `div.account-row` blocks (script in this review: parse by class `row-comapny-name`, `row-bus-type`, `span.row-city`, `row-state`, `row-address-composite`, `website-contact`). | Free | **Usable now.** Sample: `2026-11-24-nonapi-nfsa-contractors-sample.csv` (150 rows). |
| AFSA (American Fire Sprinkler Association) contractor directory | https://www.firesprinkler.org/find-a-contractor and https://firesprinkler.org/ | Unknown | Unknown | Unknown | Cloudflare challenge on every request (HTTP 403 "Attention Required") | Free if reachable | **Blocked.** Needs a real browser session. Worth one manual look: AFSA is the open-shop counterpart to NFSA and should add contractors NFSA lacks. |
| NFPA Conference & Expo 2026 exhibitor list (June 22 to 24, 2026, Las Vegas) | https://www.nfpa.org/events/nfpa-conference-and-expo (404), `.../exhibitors` (404); probed `nfpa2026.mapyourshow.com`, `nfpa26.mapyourshow.com` (no such show id) | Not found | About 420 exhibitors per trade press | Unknown | Official list URL not located; resellers (exhibitorsdata.com, jufair.com) sell copies | Free (official) / paid (resellers) | **Not found.** Retry when NFPA posts the 2027 floor plan; mostly manufacturers and testing labs, so it would feed the F&LS-manufacturer flag more than contractors. |
| AFAA (Automatic Fire Alarm Association) member list | https://www.afaa.org/ (200), `/member-directory`, `/find-a-member`, `/members` (all 404) | No public roster found | Unknown | - | Membership runs through state affiliates; no roster published | - | **Not useful** as a list today. |
| NICET certified-firm data | https://www.nicet.org/ (200) | NICET certifies individuals, not firms; its public verification is per person | - | - | - | - | **Not useful** for company discovery. |
| FSSA (Fire Suppression Systems Association) | https://www.fssa.net/members (404) | Not found | - | - | - | - | **Not found.** |
| State fire-sprinkler associations (NC, SC, GA, TX) | Web search only; NFSA chapter pages (`member.nfsa.org/Communities/Our-Chapters`) | No standalone state rosters found | - | - | NFSA's directory already covers its chapter members by state | - | **Not useful** separately; NFSA directory covers it. |
| Texas State Fire Marshal (TDI) licensed company lookup | https://appscenter.tdi.texas.gov/reports/p/sfmo | Yes, public search form | Every sprinkler and alarm firm licensed in TX | Company, license type and number, branch offices, **employee (licensee) list per company** | Form-driven search; no bulk export found. Needs form automation. | Free | **Needs scraping tool.** Strong lead: licensee count per company is a free size proxy. Other states' fire-marshal licensing rolls (e.g. Arkansas publishes a sprinkler-company PDF at labor.arkansas.gov) are the same idea and worth a per-state pass. |

### Manufacturing (MFG slice)

| Source | URL fetched (2026-11-24) | Public, no login? | Approx size | Fields given | How to get at scale | Cost | Verdict |
|---|---|---|---|---|---|---|---|
| IMTS 2026 exhibitor directory (Sept 14 to 19, 2026, Chicago) | https://directory.imts.com/8_0/explore/exhibitor-gallery.cfm, JSON at `https://directory.imts.com/8_0/ajax/remote-proxy.cfm?action=search&searchtype=exhibitorgallery&searchsize=200&start=0&state=NC` (needs the gallery page's session cookie, `X-Requested-With`, `Referer`) | Yes | 1,757 exhibitors total; **52 NC, 17 SC** | Name, exhibitor id, description, booth, tags. State only via the filter. No city, website or size in the list response. | One JSON call per state. Detail pages return HTTP 202 with an empty body (bot check), so websites need a browser or a later domain lookup. | Free | **Usable now** for names. Sample: `2026-11-24-nonapi-imts2026-ncsc-sample.csv` (69 rows, 4 flagged as non-companies). Weak ICP fit: mostly machine-tool and tooling vendors. |
| FABTECH 2025 official on-site guide and directory (PDF) | https://cdn.fabtechexpo.com/assets/downloads/25ft-directory-web-final-compressed.pdf | Yes (146-page PDF, 7.8 MB) | 1,652 unique booths; 1,116 with phone | Name, booth, phone, website, product categories. No address. | `pdftotext`, then parse "name / Booth / ph: ... \| domain" blocks. State inferred from phone area code (NC: 252 336 704 743 828 910 919 980 984; SC: 803 839 843 854 864). | Free | **Usable now**, low yield: **36 NC/SC.** Sample: `2026-11-24-nonapi-fabtech2025-ncsc-sample.csv`. Area code is a proxy, not an address. |
| FABTECH 2026 online exhibitor directory (Oct 21 to 23, 2026, Las Vegas) | https://www.fabtechexpo.com/exhibitors; probed `fabtech2026.mapyourshow.com` | Cloudflare challenge (403 "Just a moment") | ~1,300 to 1,450 per resellers | - | Needs a browser | Free | **Blocked.** The 2025 PDF above covers the same exhibitor base. |
| PACK EXPO International / PACK EXPO East | https://www.packexpointernational.com/ (403), https://www.packexpoeast.com/ (200), `/exhibitors` (404); probed `packexpo2026.mapyourshow.com`, `packexpoeast2026.mapyourshow.com` (no such show id) | Home page only | - | - | Exhibitor search not located on a reachable URL | Free | **Blocked / not found.** Same caveat as FABTECH: exhibitors are packaging-machinery vendors, not NC/SC packaged-goods manufacturers. |
| NC Commerce "Largest Employers" (QCEW, by county and quarter) | https://d4.nccommerce.com/QCEWLargestEmployers.aspx | Yes | Top employers per county, all 100 NC counties, per quarter | Legal name, industry, **employment size class**, county | ASP.NET/Telerik postback form with a county tree; needs form automation (one postback per county) | Free | **Needs scraping tool.** The most ICP-relevant free MFG source found: it is the only free list here that gives NC employment bands. Worth building. |
| NC Commerce "N.C. Manufacturing Employers Only" (statewide top 300) | https://commerce.nc.gov/nc-manufacturing-employers-only/open (PDF) | Yes | 300 rows | Legal name, industry, employment range | Direct PDF | Free | **Not useful as-is:** Q1 2019 data, and the top 300 are mostly 1,000+ employers (above GRN's band). |
| SC Manufacturers Alliance (SCMA) member directory | https://www.scma.org/, https://scma.org/ | Connection failed (no response) | - | - | - | - | **Blocked / unreachable** from this environment. |
| NC Manufacturers Alliance / NC Chamber | https://www.ncmfg.org/, https://ncmanufacturers.org/ | Connection failed (no response) | - | - | - | - | **Blocked / unreachable.** Retry from a normal browser. |
| SC Commerce SourceSC supplier database | https://sourcesc.sccommerce.com/ | Connection failed (no response) | Self-listed SC suppliers | Per web search: product, geography | Search tool, no bulk export found | Free | **Needs scraping tool** (unverified, not reached). |
| NAM (National Association of Manufacturers) | https://www.nam.org/ (200) | No member directory published | - | - | - | - | **Not useful.** |
| ThomasNet NC/SC supplier search | https://www.thomasnet.com/, https://www.thomasnet.com/suppliers/usa/north-carolina | 403 on every request | Large | Name, city, type, rough size band | Bot-protected | Free to browse | **Blocked.** |
| SC State Library county company lists | Web search only (dc.statelibrary.sc.gov) | Yes | Short per-county PDFs | Name, location, product | Per-county PDF | Free | **Not useful:** 2016 to 2018 data. |

### Signal source: state economic-development announcements

| Source | URL fetched (2026-11-24) | Update cadence | Last 90 days (2026-08-26 to 2026-11-24) | Fields given | Verdict |
|---|---|---|---|---|---|
| NC Commerce press releases | https://www.commerce.nc.gov/news/press-releases (pages 0 to 6, 10 per page) | Several a week; company announcements about 1 to 2 a week | 11 company-specific releases + 1 Rural Infrastructure Authority grant release naming 7 companies = 17 company entries in the CSV. Plus non-company items skipped (Navy FRCE facility, WTA move to Charlotte, workforce and housing grants). | Company name, county and town, jobs, investment, wage, grant. **No company website links.** The company's own headcount is never given. | **Usable now.** HTML list is parseable; each release is plain text. |
| SC Commerce newsroom, "New and expanding business" | https://www.sccommerce.com/newsroom/new-expanding-business (pages 0 to 3, 12 per page) and each release under `https://www.sccommerce.com/newsroom/<slug>` | About 1 to 3 a week | **22** company announcements | Company name, county, street address of the site, jobs, investment, company description, **company website and LinkedIn link in every release**. Company headcount occasionally (e.g. Laudisi: ~170 employees). | **Usable now.** Cleanest of all sources reviewed. |

CSV: `2026-11-24-signal-expansions-sample.csv` (39 rows: 17 NC, 22 SC). `hq_state` is filled only
where the release states it or the company is well known (e.g. Westinghouse PA, Okonite NJ);
otherwise `-`, including foreign parents. `domain` comes only from links in the release, so every
NC row is `-` except SteelFab (domain taken from its SC release). One cited domain looks malformed
in the source (VITREUS: `vitreus.com.de`); verify before use. Amounts like Caterpillar's
"billion-dollar" (statement, no figure) and Westinghouse's "approximately $1 billion" are entered
as 1000000000.

What the signal is good for: these are companies hiring dozens to hundreds of people at a new or
expanded site in NC/SC right now, which is a direct retained-search trigger (plant manager, ops
leadership, EHS, quality). Several are inside GRN's MFG ICP or adjacent to it (US Conec, Utili-Serve,
Corvid Technologies, SteelFab, Laudisi, Re:Build, Okonite), and one is F&LS (Stöbich Fire
Protection Systems, a German fire-curtain manufacturer expanding in Dorchester County SC).
Note that many SC announcements are foreign parents opening a first US site, so the NC/SC
"HQ" test often fails even when the facility is local.

## Sample files written

| File | Rows | What it is |
|---|---|---|
| `2026-11-24-nonapi-nfsa-contractors-sample.csv` | 150 | NFSA contractor companies in ET/CT states, one row per company (branches rolled up), sorted by number of listed locations (a rough size proxy), then NC/SC, then GA/VA/TN, then FL/AL. 82 have a website. 5 are NC/SC. `hq_city`/`hq_state` are the listed location of the head row and may be a branch. The two largest rows (JCI Fire Protection, Siemens) are national divisions far above 1,000 employees. |
| `2026-11-24-nonapi-imts2026-ncsc-sample.csv` | 69 | IMTS 2026 exhibitors filed under NC (52) or SC (17). 4 flagged non-companies (EDPNC pavilion, SKY nonprofit, Phillips student summit, GD&T Basics). No domains (detail pages bot-blocked). |
| `2026-11-24-nonapi-fabtech2025-ncsc-sample.csv` | 36 | FABTECH 2025 exhibitors whose phone area code is NC or SC. About a dozen also appear in the IMTS sample; the two together give roughly 93 distinct NC/SC names. |
| `2026-11-24-signal-expansions-sample.csv` | 39 | NC and SC Commerce new-facility / expansion announcements, 2026-08-26 to 2026-11-24. |

All `company_linkedin_url` values are `-`: none of the list sources gives one (SC releases do link
LinkedIn, but that column is not in the signal CSV schema). No LinkedIn URL was guessed.

## Verdicts in plain terms

- **FLS: yes, non-API lists are worth it.** NFSA alone gives 468 named ET/CT sprinkler contractor
  companies with addresses for free, which is directly comparable to whatever Blitz/Clay return for
  "fire protection" in those states. Next step: run the 468 through Blitz/Clay for LinkedIn URL and
  headcount, then measure how many land in 201 to 1,000 and how many the API pull already had (the
  VNTANA test). Add AFSA (needs a browser) and state fire-marshal licensing rolls (TX first; the
  licensee count per firm is a free size signal).
- **MFG: trade-show exhibitor lists are not the answer for GRN.** They list vendors to
  manufacturers, not NC/SC manufacturers. The better free MFG source is the state's own data:
  NC Commerce's QCEW Largest Employers tool (name + employment band by county) and SC's SourceSC,
  both of which need form automation. The state expansion announcements are the best free
  *signal*, and are small enough to read by hand every week.
- **Nothing here gives headcount except NC QCEW (bands) and the occasional SC release.** Every list
  still needs an enrichment pass for size; treat these as discovery lists and the APIs as the
  qualification layer, as the VNTANA review concluded.

## Not done / open

- No overlap check against GRN's existing API pulls (out of scope for this pass; files are ready
  for `tools/leads.py`-style company matching on domain).
- NC QCEW Largest Employers, TX SFMO lookup, AFSA, FABTECH 2026, PACK EXPO, SCMA, NCMA, ThomasNet
  and SourceSC were not extracted (blocked or form-driven), see table.
- NFSA directory individual contact rows (names, emails) were seen but deliberately not extracted.
