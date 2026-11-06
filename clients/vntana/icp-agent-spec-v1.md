# VNTANA ICP verification spec (2026-09-16)

Decide whether a company is a fit for VNTANA, a platform that converts a manufacturer's
existing 3D/CAD assets into interactive 3D for eCommerce product pages, dealer spare-parts
catalogues, sales enablement, and simulation. Buyers are industrial manufacturers.

## The core test — this matters more than the industry label
The company must **manufacture industrial equipment or components assembled from many
smaller parts**: roughly **50+ configurable parts or variants** and a catalogue of
**200+ SKUs**. Products should be complex, configurable, and hard or expensive to
photograph at scale. They must sell through dealers, distributors, or their own
storefront. They must own 3D/CAD assets (any format — native CAD is NOT required).

## Verdict rules
- `YES`  = passes the core test AND estimated annual revenue is **$100M or more**
- `NEAR` = passes the core test BUT estimated revenue is **under $100M**
- `NO`   = fails the core test, or falls in an excluded category below

For a company that is a national subsidiary of a larger group (e.g. "X America Inc."),
judge revenue on the **global parent**, and say so in the reason.

## Excluded — always NO
Fashion/apparel/footwear · consumer retail · retailers · gaming · building products &
architectural specification · medical devices · rail & transit · semiconductor capital
equipment · contract/office furniture · aerospace & defence · energy as a sector (a
multi-part industrial machine sold into energy is fine) · distributors, dealers,
resellers, rental/hire · contractors & construction firms · agencies, consultancies,
staffing · pure software/SaaS/IT services · 3D-printing or machining **service bureaus**
(they sell a service, not a product catalogue) · education, non-profits, trade
associations · process manufacturers (chemicals, food, pharma, cement, paint).

## Method
Use web search and fetch the company's own site. Judge on what they actually manufacture.
Base revenue on published figures where available, otherwise a reasoned estimate — and
mark confidence `low` when you are estimating.

## Output — strict JSON array, one object per input id, nothing else
[{"id":1,"company":"...","verdict":"YES|NEAR|NO","confidence":"high|medium|low",
  "reason":"<= 25 words, concrete","evidence":"<url you actually opened>"}]
