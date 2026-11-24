# Company-type classifier rules (GRN Piedmont data-source review, 2026-11-24)

Judge ONLY the company type from name, domain, industry and description (and your general knowledge of
the company if you know it). Geography and headcount are checked separately by a script; ignore them.

## MFG files (in-mfg-*.csv): is this a manufacturer?
- `yes`: makes physical products in its own plants (discrete, process, food, textiles, chemicals,
  plastics, metal, furniture, equipment, packaging, components...). A manufacturer that also
  distributes or services still counts.
- `no`: distributor / wholesaler / dealer, repair or field-service shop, engineering or design firm,
  construction or installation contractor, software / IT, staffing, consulting, logistics, retail,
  hospital, school, government, nonprofit, holding/investment company, R&D lab with no production.
- `unclear`: not enough information to tell.

## FLS files (in-fls-*.csv): is this a fire & life safety company?
- `core`: fire sprinkler / suppression contractor, fire alarm / detection integrator, fire & life
  safety inspection-testing-maintenance (ITM) provider, or a fire & security integrator where fire is
  a main service line.
- `adjacent`: makes or distributes fire protection / life safety equipment (sprinkler heads, alarm
  panels, fire pumps, extinguishers), or a security/alarm company where fire is a minor line.
- `no`: MEP engineering/design firm, general / mechanical / electrical contractor where fire is one of
  many trades, software, nonprofit / association, university, government, insurance, consulting, anything else.
- `unclear`: not enough information to tell.

## Output
For each input file `classify/in-<x>.csv` write `classify/out-<x>.csv` with header `key,verdict,reason`,
one row per input row, same `key` value copied exactly, `reason` <= 12 words, no commas inside reason
unless the field is quoted (use Python csv module to write it). Every input row must appear once.
