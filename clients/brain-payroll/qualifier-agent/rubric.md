# Brain Payroll — company qualification rubric (v1, 2026-09-17)

This is the decision rule a qualifier sub-agent applies to ONE company. It is derived
from the client brief in `tracking_clients` (`get_client` → `clientBrief`) for
Brain Payroll UK Limited (`0a09f3c7-9a9b-4f57-bbec-e2fbf0dc6780`).

## What Brain Payroll sells, and therefore who can buy

Brain Payroll is a UK cloud **payroll software vendor**. Its buyers are organisations that
**run payroll on behalf of other organisations** and would therefore license payroll
software to do it at scale. The single question that decides every verdict is:

> **Does this company process payroll for clients who are not itself?**

A company that merely *has* a payroll (every employer does) is not a buyer. A company that
*sells* payroll software is a competitor, not a buyer.

## Verdict values

| Verdict | Meaning |
|---|---|
| `QUALIFIED` | Confirmed: runs payroll for external clients. Evidence URL required. |
| `LIKELY` | An accountancy practice of 11+ staff with no payroll page found, but nothing contradicting it. Payroll is a near-universal practice service line. |
| `DISQUALIFIED` | Fails a hard rule below. `reason` required. |

## Hard disqualifiers — any one of these ends it

1. **Competitor.** Sells payroll, HR or HCM *software*, or is a global payroll outsourcer
   selling a platform (Sage, IRIS, BrightPay, Moorepay, Zellis, CloudPay, Mercans, Vialto,
   ADP, Dayforce, SD Worx, Employment Hero, PayFit …). Being a *reseller or partner* of one
   (e.g. "Xero Gold Partner", "Sage certified") is **not** disqualifying — that is a
   customer profile, not a rival.
2. **End employer only.** Runs payroll solely for its own staff — a retailer, NHS trust,
   council, school, manufacturer, housing association.
3. **Geography.** HQ outside the United Kingdom or Republic of Ireland.
4. **Size.** Fewer than 11 employees.
5. **Professional body / institute.** CIPP, ICAEW, ACCA, AAT, CIMA, ICAS and similar.
6. **Recruiter only.** Recruits accountants or payroll staff *into other businesses* but
   does not itself run payroll. Note the exception below.
7. **DNC.** Appears on the client's do-not-contact list.
8. **Defunct / acquired.** Ceased trading, or absorbed into a parent that is already in the
   list — say which parent.

## Segment assignment (for QUALIFIED and LIKELY)

- `payroll-bureau` — core business is processing payroll for client organisations.
- `accountancy-practice-payroll` — accountancy or bookkeeping practice offering payroll as
  a service line to its clients.
- `umbrella-contractor-payroll` — umbrella company, CIS or contractor payroll provider
  paying agency workers or subcontractors under PAYE.
- `recruitment-umbrella-contractor-payroll` — a recruitment or staffing agency that runs
  its **own** in-house umbrella/contractor payroll. This is the exception to hard rule 6:
  a recruiter that pays its own contractors through its own payroll operation **qualifies**.

## Buying signals to capture when visible (`signals` field)

From the client brief, in priority order: new senior appointment in payroll services;
change of ownership, merger or acquisition of a practice or bureau; investment round;
advertising payroll vacancies; new client-win announcements; public interest in payroll AI
or automation; complaints about their current payroll software provider; exhibiting at
accountancy or payroll events.

## Evidence standard

`evidence_url` must be a page on the company's **own domain** that shows payroll offered as
a service to clients — a "Payroll services" or "Outsourced payroll" page, a bureau page, or
an umbrella/CIS page. A LinkedIn About blurb is acceptable only when no website page exists,
and must then be marked `evidence_quality: weak`. Never invent a URL: if none was found,
return an empty string and let the verdict be `LIKELY` or `DISQUALIFIED`.

## Output — one JSON object per company, nothing else

```json
{
  "company_linkedin_tag": "<as given>",
  "name": "<as given>",
  "verdict": "QUALIFIED | LIKELY | DISQUALIFIED",
  "payroll_service_confirmed": true,
  "segment": "payroll-bureau",
  "evidence_url": "https://example.co.uk/services/payroll",
  "evidence_quote": "<= 200 chars, quoted verbatim from the page",
  "evidence_quality": "strong | weak | none",
  "reason": "<required when DISQUALIFIED, else empty>",
  "signals": ["hiring payroll staff"],
  "notes": "<= 200 chars, anything a human should know"
}
```

Rules: return one object per input company and no prose around them. Do not guess a verdict
to fill the shard — `LIKELY` with `evidence_quality: none` is the correct, honest answer for
a practice whose website could not be reached.
