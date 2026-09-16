# VNTANA ICP TRIAGE spec — t2 (2026-09-16, text-only, no web)

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

## VERDICT RULES (triage — fit only, no revenue tier)

**Never return NO because revenue is low. Low revenue is NEAR.**
**Never return NO because they sell direct-to-customer.** Own storefront is in scope.
**Never return NO because some buyers are hobbyists, makers, prosumers or small shops.**
The test is whether they manufacture a deep catalogue of physical products, not who buys
it. Desktop 3D printers, laser cutters/engravers, benchtop machines and commercial
cleaning or floor equipment are all IN scope. "Consumer retail" as an exclusion means a
*retailer* or a lifestyle/household-goods brand — not a machine maker with prosumer
customers.
**When you cannot verify catalogue depth or revenue, return NEAR, never NO.**
`NO` requires positive evidence of a failed core test or an excluded category. Absence of
evidence is NEAR with `confidence: low`.

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


## METHOD — TEXT ONLY, NO WEB RESEARCH
You are given each company's name, LinkedIn industry, employee count and its own
LinkedIn "about" text. **Do not search the web. Do not open any URL.** Judge only from
the text provided plus what you already know about the company.

This is a TRIAGE pass. Its job is to remove companies that are clearly outside the ICP
and to flag the rest for a deeper check. Being wrong in the direction of keeping a
company is cheap; wrongly discarding a real prospect is expensive.

- `FIT`    — the text shows a manufacturer of a catalogue of physical industrial products
- `UNSURE` — the text is thin, generic, or you cannot tell. **This is the safe default.**
- `NO`     — the text positively shows an excluded category (software/SaaS, IT services,
             consultancy, staffing, distributor/reseller/dealer with no manufacturing
             parent, service bureau, job shop, education, association, media, retailer)

Do NOT use `NO` for a company you simply have not heard of, or whose catalogue depth or
revenue you cannot confirm. That is `UNSURE`.
Do not assign a revenue tier in this pass.

### Three traps — each of these has already caused a wrong NO. Read them.
1. **"Semiconductor" is not a blanket exclusion.** Only semiconductor *capital equipment*
   (the machines that fabricate chips) is out. A company that **makes chips, power
   components, sensors or electronic parts and sells them as a catalogue is IN SCOPE** —
   that is a component manufacturer. Never return NO on "semiconductor" alone.
2. **A joint venture or national arm whose name contains a manufacturer's name is not a
   distributor.** Names like "<Japanese maker> <US city>, Inc." or "<Maker A>-<Maker B>,
   Inc." are almost always the manufacturer's own sales/JV entity. Return `FIT`, or
   `UNSURE` if genuinely unclear — not `NO`. Reserve `NO` for a clearly independent
   multi-brand reseller with no manufacturing parent of its own.
3. **Service bureaus and contract manufacturers are `UNSURE`, not `NO`.** A firm offering
   machining/3D-printing as a service may still sell a configurable parts catalogue.
   Flag it for the deeper check rather than discarding it here.

## OUTPUT — strict JSON array, one object per input id, nothing else
[{"id":1,"company":"...","verdict":"FIT|UNSURE|NO","confidence":"high|medium|low",
  "reason":"<= 18 words, concrete"}]
