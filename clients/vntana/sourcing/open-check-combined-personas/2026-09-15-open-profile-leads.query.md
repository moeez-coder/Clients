# 2026-09-15 — Open Profile export: ICP review + per-lead InMail copy

**Source:** HeyReach "Open Profile" view export supplied by the repo owner (135 leads — the
people the Open Check campaign `601752` confirmed as open-profile via the `VIEWED_PROFILE`
webhook `78850` → Clay). Not an API pull; the export was uploaded to this session and every
row is preserved here with its LinkedIn URL as the key.

**Purpose:** repo owner asked (1) how many of these are ICP fit and (2) the best message
to each to get a reply. The result feeds the Open Profile campaign `601753`
("US & Europe | Open Profile | General"), whose single INMAIL step is templated as
`{subject}` / `{inmail}` — the `inmail_subject` / `inmail_body` columns in this CSV are
exactly what those merge fields take.

## ICP basis

Scored against VNTANA's `tracking_clients` profile (`get_client` on
`5e0a22cf-6efb-432d-bc3c-6eb914440f13`, re-pulled this session): discrete manufacturer,
$100M+ ($500M+ preferred), 50+ configurable parts/variants, internal PLM/CAD, sells via
dealers/distributors or own storefront, multi-brand preferred. Target industries:
construction/ag/mining equipment, pumps & valves, heavy trucks, material handling,
industrial automation, hydraulics/pneumatics, power transmission, process equipment.
Hard disqualifiers: distributors, process manufacturers (chemicals/food/pharma/cement/
paint), agencies/consultants, outsourced-3D-only, wrong titles (VMO, analytics,
compliance, procurement). Buyer personas: VP Aftermarket/Service, Dir Service Ops, CDO,
Dir Digital Experience (Test 1); VP Digital/Digital Commerce, Dir eCommerce, CDO (Test 2).

## Tiers (in `icp_tier`)

| Tier | Count | Meaning |
|---|---|---|
| A | 31 | Strong fit: ICP company **and** a buying/influencing persona. Send first. |
| B | 48 | Fit, secondary: ICP company with a partial persona (brand/comms/PMO/regional GM), or a building-products OEM where the 3D case is valid but weaker than machinery, or likely sub-$100M. |
| C | 21 | Verify before sending: no company in the export, process-leaning product, wrong door at a fit company, or a borderline call flagged for the owner (e.g. Motorcar Parts of America). |
| X | 35 | Not a fit: distributors/retailers, agencies/consultants, software vendors, process manufacturers, dealers, wrong persona, or export data mismatches. |

`icp_test` marks which VNTANA market test the message leads with: `AM` = Test 1
Aftermarket parts catalog (18 leads — service/aftermarket/parts personas, or OEMs with a
dealer-parts business), `EC` = Test 2 B2B eCommerce 3D (61 leads).

## Copy approach (why the messages look the way they do)

Voice matched to VNTANA's two running sequences in `tracking_clients` (Aftermarket
`917d3d7a…`, B2B eCommerce `a45b07ac…`): observation about *their* catalog/channel →
one line on converting the CAD they already hold into interactive 3D with no engineering
tickets → proof (Doosan Bobcat / Astec / Kohler) only where it lands → a **question**
CTA rather than a meeting ask, because a question is the lowest-friction thing an
open-profile recipient can answer. Each InMail is 50–80 words, subject lines name the
company or brands specifically. Personas were split so Aftermarket/Service contacts get
the parts-identification pain and Marketing/Digital/Product contacts get the product-page
/ dealer-content pain. No message references a DNC company as a customer other than the
public proof points VNTANA itself uses (Bobcat, Astec, Kohler).

## Checks

- DNC: no lead's `company_domain` is on VNTANA's `dncList`.
- Dealers caught as X: RZK Agro (Deere dealer, domain `deere.com`).
- Export data mismatches flagged as X: row listing Bonfiglioli with a CBTS domain; a
  "Voll Entertainment" row mapped to Leica.

## Not done (needs the owner's go)

Nothing was pushed to `601753`. Loading the 79 A+B leads with `customUserFields`
`subject` / `inmail` is a single scripted step once the copy is approved.
