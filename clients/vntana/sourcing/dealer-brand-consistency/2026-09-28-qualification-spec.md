# Campaign 10 qualification — "The Dealer Who Rebuilt Your Brand Badly"

VNTANA turns a manufacturer's CAD/3D into a deep, configurable image and 3D feed. This
campaign targets manufacturers whose **independent dealers rebuild the brand badly** on
their own websites because the OEM only sends them a PDF and six images.

For EACH company answer five questions. Use WebSearch/WebFetch. Open the company's own
site — look for "Find a Dealer", "Dealer Locator", "Where to Buy", "Find a Distributor",
"Find a Rep".

## Q1 `role` — what is this company?
- `OEM` — designs and manufactures its own branded equipment/products
- `DEALER` — sells or rents OTHER companies' brands (e.g. "Warren CAT", "Peterson Cat",
  "Doggett John Deere", any "___ Equipment" dealership, any "___ Auto Group")
- `FINANCE` — captive finance / leasing / acceptance corp (e.g. "Hyundai Capital")
- `OTHER` — retailer, service company, security, software, feed/farm co-op, anything else
A national sales arm of a foreign manufacturer (e.g. "Kubota Tractor Corporation",
"Takeuchi US") counts as `OEM`.

## Q2 `vertical` — pick the ONE best fit
`construction_ag` · `trailers` · `material_handling` · `power_equipment` · `hvac` ·
`trucks_bodies` · `flow_hydraulics` · `none`
- trucks_bodies = truck OEMs, truck bodies, service bodies, upfit, snowplows, liftgates,
  fire apparatus, refuse bodies
- flow_hydraulics = pumps, valves, fluid power, hydraulics sold via distributors or reps
- power_equipment = engines, generators, compressors, outdoor power, welders, light towers
  (an ENGINE maker is power_equipment, not flow_hydraulics)
- none = an OEM outside all seven

## Q3 `channel` — how do customers buy it?
- `independent_dealers` — through independently owned dealers/distributors/reps
- `direct` — sells direct or through company-owned stores only
- `mixed` — both
- `unknown`

## Q4 `dealer_locations` — estimated number of dealer/distributor/rep LOCATIONS in North America
Give an integer estimate. Use the locator, the "about" page ("our network of 400+
dealers"), press releases, or annual reports. If the company states a number, use it.
If you cannot find one, estimate from evidence and set `confidence: low`. Use 0 only if
there is no dealer channel at all.

## Q4b `dealer_companies` — number of distinct independent DEALER BUSINESSES in North America
Not the same as locations. Caterpillar has ~48 North American dealer companies (Warren CAT,
Holt CAT...) operating hundreds of branches. Each dealer business runs its own website,
which is what this campaign reviews. If a source gives only one of the two numbers, fill
that one and estimate the other; lower `confidence` accordingly. Use 0 if no dealer channel.

## HARD RULES FOR THE NUMBERS — read before answering Q4/Q4b
- **Never report a number larger than your own evidence supports.** If your evidence says
  "8 distributors", dealer_companies is 8 — not 100. If it says "more than 50 dealers",
  report 50-something, not 100.
- **Never estimate from "industry norms", "standard models" or the company name.** You
  must actually open the company's site or a source about it.
- If you researched and genuinely found no number, set `confidence: "low"` and give your
  best evidence-based figure — and say in `evidence` that no number was published.
- 50 is the campaign threshold. Do not round up to reach it.
- Every `evidence` string must name where the number came from (the page or source).

## Q5 `locator_url` — the URL of their dealer/distributor locator page, or "-"

## OUTPUT — strict JSON array, one object per input id, nothing else
[{"id":1,"role":"OEM","vertical":"trailers","channel":"independent_dealers",
  "dealer_locations":350,"dealer_companies":120,"locator_url":"https://...","confidence":"high|medium|low",
  "evidence":"<= 20 words, where the number came from"}]

**Do not copy or return any company id other than the `id` given in the input.**
