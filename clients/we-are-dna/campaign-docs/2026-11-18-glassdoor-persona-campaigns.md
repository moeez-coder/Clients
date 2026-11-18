<!-- Internal draft for Moe, We Are DNA (tracking_clients f5ff426b-c514-4a64-91b0-0e141a6a0669). Written 2026-11-18 (session_013MzxQfS4USBg3GQoTHx9Ai) on Moe's ask: three campaigns on the same Glassdoor company list, one per persona, each with the connection request + 3-message sequence in the format sent to John in doc 1 (fed8e905-ea1c-4a91-ade7-0da0f7f732a6). Offers from the outcome-led-offer-generation skill run of 2026-11-18 (algoacquisition-brain PR #36). NOT in doc 1, NOT in tracking_clients or HeyReach, nothing sent. Every guarantee needs John's sign-off. UK English, no em dashes. -->

# Glassdoor campaigns by persona (draft for Moe)

All three campaigns use the **same company list** and the **same signal**. Only the persona, the offer and the messages change.

## Shared ICP and signal

- **Market:** DNA's five sectors:
  - health, care and vet
  - retail and hospitality
  - manufacturing and engineering
  - law and accounting
  - financial services
- **Segment:** private-sector UK employers with 51 to 5,000 staff.
- **Signal:** the company's public employer review profile is below the bar on at least 30 reviews:
  - overall rating under 3.5, or
  - culture and values under 3.3, or
  - senior leadership under 3.3

  Ratings are slow-moving, so the list stays valid for months. We re-check before each wave.

### Signal and data (applies to all three)

**Repo record:** `sourcing/glassdoor-bad-reviews/`. Tool: Apify `kaix/glassdoor-company-scraper`, run 2026-11-17, $2.80. Query record: `2026-11-17-glassdoor-profiles.query.md`.

**Funnel:**

| Stage | Companies |
|---|---|
| ICP companies looked up on Glassdoor | 29,489 |
| Pass the bar | 1,796 |
| **Pass the bar, high-confidence match (the list)** | **1,384** |
| Pass the bar, low-confidence match | 412, held back (372 have a non-UK HQ, so they're likely the wrong company) |

**The list by sector:**

| Sector | Companies |
|---|---|
| Retail and hospitality | 560 |
| Financial services | 329 |
| Manufacturing and engineering | 191 |
| Health, care and vet | 173 |
| Law and accounting | 131 |

**The list by size:**

| Staff | Companies |
|---|---|
| 51 to 200 | 389 |
| 201 to 500 | 375 |
| 501 to 1,000 | 250 |
| 1,001 to 5,000 | 370 |

**What the list looks like:**
- median overall rating 3.2
- median senior leadership rating 2.8
- median "would recommend to a friend" 48%
- **Weakest area:** senior leadership at 634 companies, then pay and benefits at 282, career progression at 240, work-life balance at 111, culture and values at 96.

**Before it goes in a doc:**
- Dedupe the 131 passing rows that share a Glassdoor employer (e.g. "Christie's" matched to Christies Care).
- Measure reachable contacts per persona per company (Blitz + Clay). This hasn't been run yet; leads are waiting on your go-ahead.

**Client-facing wording for "Signal and data":** "Public employer review ratings, at least 30 reviews, checked in November 2026: about 1,400 UK employers in your five sectors where staff rate the company, its culture or its leadership noticeably below average."

### Rules for all three sequences

- The rating is never the headline. We name a **theme**, never a score in the first line.
- We never quote a review or hint at who wrote one.
- We never say "bad", "poor" or "negative".
- **Free first step in every campaign:** the reputation snapshot. It covers what staff, candidates and AI tools say about the company, by theme, next to sector peers, delivered within 10 days. It extends DNA's own free AI visibility snapshot (doc 1, Offer 1, plus Offer 7, competitor comparison).
- **Variables:**
  - `{first_name}`, `{company}`
  - `{sector_peers}`, e.g. "UK care providers", "national retailers", "mid-sized law firms"
  - `{theme}` comes from the company's weakest sub-rating:

    | Weakest sub-rating | `{theme}` |
    |---|---|
    | Senior leadership | "communication from leadership" |
    | Career opportunities | "career progression" |
    | Work-life balance | "workload and work-life balance" |
    | Culture and values | "culture and values" |
    | Diversity and inclusion | "inclusion" |

    Pay and benefits is skipped, because DNA doesn't fix pay. We use the next-weakest area instead.
- **Sending:**
  - A company gets **one person per campaign**, so up to 3 people in total. Each person hears a different offer.
  - The three campaigns start in the same week, so nobody at the company hears from us twice.
  - Each lead list holds 1 contact per company (fewer per company because the list is large, so 1,384 companies, not depth).
  - A company already in doc 1 campaigns 1 to 8 that month is skipped.

---

## Campaign A: Glassdoor, the Cost of Turnover, CEOs and Managing Directors

### ICP
The shared list, all 1,384 companies.

### Persona
CEO or Managing Director, and at larger groups the COO or CFO. John's guidance is that DNA sells to the C-suite. This persona owns the profit and loss, not the people metrics, so the offer is about money.

### Signal and data
As above.

### Lead list
- **Volume:** 1 contact per company (CEO or MD first; COO or CFO if there's no CEO profile).
- **Filtered out:** DNA's current clients and DNC list, and companies in doc 1 campaigns 1 to 8 that month.

### Offer led
Pays for itself within 24 months, or DNA refunds the difference.
- **Proof:** DHU Healthcare, over £2m added to the bottom line in 20 months; MAN Truck & Bus UK, £1m a year.
- **First step:** the free snapshot, then a 30-minute business case session.
- **Needs John's sign-off.**

### Messaging

**Connection request**

Hi {first_name}, I've been looking at what staff say about employers across {sector_peers} this year. A few patterns worth sharing. Would be good to connect.

**Message 1**

Thanks for connecting, {first_name}.

When the people inside a business rate {theme} below their peers, it rarely stays an HR problem. It turns up in turnover, agency bills and how long roles sit empty.

We help leadership teams fix the story at the root. For DHU Healthcare that added over £2m to the bottom line in 20 months, and we're happy to stand behind a programme that pays for itself within two years.

Would a one-page snapshot of how {company} comes across to staff and candidates, next to your peers, be useful?

**Message 2**

Hey {first_name}, following up so this doesn't get buried.

Is the cost of staff leaving something the board is looking at this year?

**Message 3**

No worries if the timing's off, {first_name}.

If the snapshot would be useful, we'll send it over and you can read it whenever suits. If not, no hard feelings and we'll leave it there.

---

## Campaign B: Glassdoor, Unwanted Turnover, People Leaders

### ICP
The shared list, all 1,384 companies.

### Persona
Chief People Officer, People Director, HR Director, Head of People and Culture. John's top two pains for this person are attrition and "shaping and sharing their story".

### Signal and data
As above.

### Lead list
- **Volume:** 1 contact per company, the most senior people leader.
- **Filtered out:** as in Campaign A.

### Offer led
A quarter off unwanted staff turnover within 18 months, or DNA keeps working at no cost until it gets there.
- **Proof:** MAN Truck & Bus UK, attrition from 20% to under 10% within a year; Glendola, unwanted turnover cut by over 50%.
- **First step:** the free snapshot.
- **Needs John's sign-off.**

### Messaging

**Connection request**

Hi {first_name}, I've been reading what staff and candidates say about {sector_peers} this year. Some useful patterns for people teams. Would be good to connect.

**Message 1**

Thanks for connecting, {first_name}.

At {company}, what people say online keeps coming back to {theme}. Candidates read the same pages before they apply, so expectations get set before day one.

We help close the gap between what people are promised and what they find. At MAN Truck & Bus UK attrition went from 20% to under 10% within a year, and we'd put a quarter off your unwanted turnover in writing.

Would a one-page snapshot, by theme and next to your peers, be useful?

**Message 2**

Is retention something the people team is focused on this year?

**Message 3**

Asking because candidates now read review sites and ask AI tools about a place to work before they apply, and both shape who joins and who stays.

No pressure either way. Happy to send the snapshot if it helps.

---

## Campaign C: Glassdoor, Agency Spend, Talent Acquisition Leaders

### ICP
The shared list at **201+ staff only (995 companies)**. Companies with 51 to 200 staff rarely have a talent lead, so we reach them through Campaign B.

### Persona
Head or Director of Talent Acquisition, Head of Resourcing, Head of Recruitment. John's top pain for this person is cost per hire.

### Signal and data
As above.

### Lead list
- **Volume:** 1 contact per company.
- **Filtered out:** as in Campaign A.

### Offer led
Half off recruitment agency spend within 18 months, or DNA keeps working at no cost until it gets there.
- **Proof:** MAN Truck & Bus UK, agency spend from over £600k to under £30k within a year.
- **For 1,001 to 5,000 staff:** the £250k-a-year version is backed by Superdry (over £500k a year) and boohoo and Pets at Home (over £600k a year).
- **First step:** the free snapshot, then a free review of their last 12 months of agency fees.
- **Needs John's sign-off.**

### Messaging

**Connection request**

Hi {first_name}, I've been looking at what candidates read about {sector_peers} before they apply. Some useful patterns for talent teams. Would be good to connect.

**Message 1**

Thanks for connecting, {first_name}.

Before someone applies to {company}, they read what staff say online, and right now that keeps coming back to {theme}. When the story puts good people off, roles go to agencies.

MAN Truck & Bus UK were spending over £600k a year on agencies. Within a year it was under £30k, because the right people started applying direct. We'd put half off your agency spend in writing.

Would a one-page snapshot of what candidates see about {company}, next to your peers, be useful?

**Message 2**

Is agency spend something you're being asked to bring down this year?

**Message 3**

Asking because it's usually the quickest number to move once candidates like what they read. No pressure either way.

---

## Open points for Moe

1. **Approval route:** add these as campaigns in doc 1 (tracked suggestions via `review_campaign_doc`, since doc 1 is with John), or your own approval?
2. **Naming the source:** these messages say "what staff say online", not "Glassdoor", the same as doc 1 campaign 8. Name Glassdoor instead?
3. **Overlap with doc 1:** do these replace doc 1 campaign 8 (Reputation and Retention), which uses the same signal?
4. **Snapshot:** who builds it in DNA's name, Algo by script or DNA's team, and does DNA accept the Glassdoor themes in it?
5. **Guarantees:** all of them (24-month payback, a quarter off turnover, half off agency spend) need John's sign-off before launch.
