# Review: levers to reach ~800 leads per MPC campaign (2026-11-25)

**Asked:** Moe, 2026-11-25: "what variables do we have to change to increase the lead count to around 800 per campaign", then "do 1-3 and 5 and give me a review".

**Baseline:** 394 launch-set leads across the 5 campaigns, about 80 per campaign. Most of the live campaign's persona has already been contacted (`2026-11-24-mpc-segments.query.md`).

**How it was measured** (script `lever_counts.py`, output `2026-11-25-levers.json`, **204 Blitz records**):
- Blitz `POST /v2/jobs/search` count calls, using the same 71 titles, manufacturing labels and gates as the 11-24 pull, and changing one variable at a time.
- `total_results` is indicative. The base variant counts 4,666 postings, against 1,256 companies in the real 11-24 pull, so roughly 0.27 companies per posting.
- Plus a Director waterfall on 80 seeded-random hiring companies (`2026-11-25-levers-director-sample.csv`).
- **Lead estimates** use the 11-24 reach rate at never-pulled companies: 57% have a persona contact, at 2.4 each, so about **1.4 C-level/VP leads per new company**. They are estimates, not pulls.

| Lever | What changes | Measured | Est. new hiring companies | Est. new leads (all 5 campaigns) | Needs GRN to agree? |
|---|---|---|---|---|---|
| **1. Directors** | Add Director-level titles (Managers stay out) | 56 of 80 companies (70%) have at least one Director; **2.25 Directors per company** (180 people, all real Director titles) | 0 (same companies) | **~2,800** across the 1,256 companies already in the segments. None of them can be in 734516/756466, which only took C-level/VP | **Yes**: GRN excluded Directors |
| **2a. Size 1,001-5,000** | Add the next size band | 5,263 postings (113% of base) | ~800-1,000 (bigger firms post more roles each, so fewer companies per posting) | ~1,200-1,500 C-level/VP, about double with Directors | **Yes**: outside the 201-1,000 ICP |
| **2b. Size 51-200** | Add the smaller band | 2,680 postings (57% of base) | ~900-1,100 | ~1,300-1,500 (often Owner/President-led) | **Yes**: outside the ICP |
| **3. Mountain/Pacific/AK/HI** | Drop the time-zone limit | 1,362 postings (29% of base) | ~350-400 | ~500 C-level/VP, ~1,300 with Directors | **Yes**: ICP form says Eastern and Central |
| **5a. Window 180 days** | 120 to 180 days | 5,575 postings (+19%) | ~250 | ~350, but 85% of 60+ day postings are already closed | No |
| **5b. Window 365 days** | 120 to 365 days | 5,603 postings (+20%; Blitz keeps about 6 months) | same as 180d | same as 180d | No |
| **5c. More contacts per company** | Raise the cap | 11-24 pull: Blitz returned everyone at ~2.1 per company | 0 | ~0 | No |

## Review

- **Directors (lever 1) is the only lever that reaches about 800 per campaign on its own terms.** It roughly multiplies the pool by 8 without touching which companies are targeted. The Director is also often the actual hiring manager for the open role, which is what MPC copy speaks to.
  - Estimated split by segment (companies x 2.25 + today's leads): Executive ~620, Ops & Plant ~850, Eng & Quality ~700, Supply Chain ~475, EHS & Maintenance ~570.
  - Before launch it needs the usual noise check on titles; the 80-company sample was clean.
- **Size and geography (levers 2 and 3) add new companies, but outside GRN's stated ICP.** 1,001-5,000 is the closest fit to GRN's market: still mid-market manufacturing, and they hire the same roles. 51-200 is mostly owner-led shops with fewer specialist roles.
- **The window (lever 5) barely moves anything.** Blitz holds about 6 months, and older postings are mostly closed. Contacts per company is already maxed under the current persona.

## Paths to ~800 per campaign (4,000 total)

| Path | Est. total leads | Per campaign | GRN sign-off |
|---|---|---|---|
| Directors only | ~3,200 | ~640 | Directors |
| **Directors + 1,001-5,000** | ~5,500-6,500 | **~1,100-1,300** | Directors + size |
| Directors + Mountain/Pacific | ~4,500 | ~900 | Directors + geography |
| No ICP change (window + cap) | ~750 | ~150 | none |

**Recommendation:** ask GRN to approve Directors first; it gets close to 800 alone. Then add 1,001-5,000 if they are comfortable with it. Each would be pulled with the same pipeline (`../mpc-build/`), deduped against 734516/756466 and the five MPC lists, and pushed into the existing five campaigns as new waves.
