# VNTANA ICP verification spec — v2 (2026-09-16)

VNTANA converts a manufacturer's existing 3D/CAD assets into interactive 3D for eCommerce
product pages, dealer spare-parts catalogues, sales enablement and simulation. Buyers are
industrial manufacturers with deep product catalogues.

## THE CORE TEST
The company **manufactures physical industrial products and sells a catalogue of roughly
200+ SKUs**, with configurable options or variants, sold to businesses through dealers,
distributors, reps, or its own storefront.

**Catalogue breadth is the test — NOT whether the product itself is a big machine.**
A company that makes 4,000 SKUs of collets qualifies exactly as much as one that makes
CNC machining centres.

## IN SCOPE — all of these count as industrial products
- Machines & equipment — CNC machines, presses, robots, compressors, packaging lines
- **Components & sub-assemblies** — hydraulics, pneumatics, actuators, bearings, valves,
  seals, gears, drives, tool changers, grippers, vacuum handling, cable management
- **Tooling & workholding** — chucks, collets, mandrels, fixtures, cutting tools, inserts
- **Abrasives & consumables** — grinding wheels, saw blades, brushes, industrial ceramics
- **Metrology & inspection instruments** — CMMs, 3D scanners, microscopes, optical
  measurement, balancing and vibration-test machines
- **Shop support** — industrial computers, lighting, filtration, air handling, framing
- Marine / RV / powersports **component** makers that supply dealer parts networks
- Robotics OEMs (including for simulation / physical-AI use cases)
- Forgings, castings and machined components sold as a catalogue

## VERDICT RULES
- `YES`  — passes the core test AND estimated annual revenue **$100M or more**
- `NEAR` — passes the core test BUT revenue **under $100M**
- `NO`   — **only** when the company fails the core test or is an excluded category

**Never return NO because revenue is low. Low revenue is NEAR.**
**Never return NO because they sell direct-to-customer.** Own storefront is in scope.

## SUBSIDIARY RULE — this is a hard rule, apply it every time
An entity named "X America", "X USA", "X North America", "X Inc." or similar that is the
national arm of a manufacturer **is itself a manufacturer — never a distributor.**
Judge revenue on the **GLOBAL PARENT GROUP**, not the local entity's headcount or filings.
- "Chiron America" → Chiron Group, German machine-tool builder → manufacturer, judge on the group
- "Botek America" → botek Praezisionsbohrtechnik, German tooling maker → manufacturer
Only call something a distributor when it sells **other companies'** brands and has no
manufacturing parent of its own.

## EXCLUDED — return NO
Fashion/apparel/footwear · consumer retail & retailers · gaming · building products &
architectural specification · **medical devices meaning patient-care equipment** · rail &
transit · semiconductor capital equipment · contract/office furniture · aerospace &
defence · energy as a sector · independent distributors, dealers, resellers, rental/hire ·
contractors & construction firms · agencies, consultancies, staffing · pure software /
SaaS / IT services · 3D-printing or machining **service bureaus** (sell a service, not a
catalogue) · education, non-profits, trade associations · **process manufacturers, meaning
chemicals, food, pharma, cement and paint made in continuous batches**.

### Two exclusions that are commonly misapplied — read carefully
1. **Metrology and inspection instruments are IN SCOPE.** The medical exclusion covers
   patient-care devices only. Electron microscopes, CMMs and balancing machines are IN.
2. **Abrasives, ceramics, forgings and castings are DISCRETE manufacturing and are IN.**
   They are not "process manufacturing". Process means chemicals/food/pharma/cement/paint.

## WORKED EXAMPLES (these are the correct answers)
| Company | Verdict | Why |
|---|---|---|
| SMC Corporation of America | YES | Pneumatic components — vast catalogue, parent ~$5B |
| CERATIZIT USA | YES | Cutting tools and inserts = tooling catalogue, $1.3B |
| Bruker Alicona | YES | Optical metrology instruments are IN scope, parent $3.4B |
| Chiron America, Inc. | YES | National arm of a German machine-tool builder, not a distributor |
| Indo-MIM Inc. | YES | Metal-injection castings sold as a catalogue = discrete manufacturing |
| Sunnen Products Company | YES | Honing machines plus abrasive tooling consumables, $100M+ |
| 80/20 LLC | YES | Aluminium framing catalogue — shop support is in scope |
| DATRON USA | NEAR | Real CNC machine manufacturer, revenue only $60-80M |
| GMN USA | NEAR | Spindles and bearings catalogue, under $100M |
| Kosmek USA Ltd. | NEAR | Hydraulic clamping components, parent under $100M-ish |
| A CNC machining job shop | NO | Sells a service, not a product catalogue |
| An independent machine-tool dealer | NO | Resells other brands, no manufacturing parent |


## METHOD
Use WebSearch and WebFetch. Open the company's own site. Judge on what they actually make
and how deep the catalogue is. For revenue use published figures where available,
otherwise a reasoned estimate of the global parent — set `confidence` to `low` when
estimating.

## OUTPUT — strict JSON array, one object per input id, nothing else
[{"id":1,"company":"...","verdict":"YES|NEAR|NO","confidence":"high|medium|low",
  "reason":"<= 25 words, concrete","evidence":"<url you actually opened>"}]
