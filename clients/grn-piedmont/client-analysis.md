# GRN Piedmont: client analysis

**Written:** 2026-11-05. **Client:** GRN Piedmont (tracking_clients `3abc2243-889c-4177-a75a-3ac680766d20`).

**Sources, all pulled 2026-11-05 from `tracking_clients` `get_client`:**
- `icpForm`: the onboarding Typeform, submitted 2026-11-03, verbatim in [`onboarding-form.md`](onboarding-form.md).
- `clientBrief`: verbatim in [`client-brief.md`](client-brief.md).
- `clientDescription`: website research.
- `callerBriefing` / `callerFaqs`: for warm callers.
- `infrastructure`.

**Not available yet:**
- `callTranscript` is empty, and `get_client_meetings` shows no onboarding call booked or recorded.
- `get_client_experience` is blocked by the MCP firewall, so the Slack channel was not read.

This is analysis, not client-confirmed fact. Anything marked **[confirm]** needs to go to Harvey before it drives a campaign.

---

## 1. One-paragraph read

GRN Piedmont is a small executive-search office in Myrtle Beach, SC. It is the Piedmont franchise of the Global Recruiters Network, founded in 2013. It places senior leaders and specialists (executive management, operations, engineering, purchasing, supply chain) on a direct-hire basis, and it is a GSA contract holder. Its real differentiator is method, not network size:
- It defines what the hire must achieve in year one before searching (performance-based hiring and SMART-goal position profiles).
- It sources passive candidates who are already succeeding elsewhere.
- It presents very few candidates: over 90% of presented candidates get an interview, and 8 or 9 roles in 2026 were filled from a single presented candidate.

They want C-suite, Owner and VP buyers at 201–1,000-employee manufacturers and fire & life safety companies in the EST/CST US. They pay $13k a month against a stated $40k average deal and a 4-week sales cycle. The hook they own is *"Of the people your organization hired over the past year, how many would you enthusiastically rehire?"* The door-opener is a **Complimentary Hiring Process Effectiveness Review**.

## 2. What the onboarding form actually says (and what it implies)

| Form field | Answer | What it means for us |
|---|---|---|
| Verticals | Manufacturing + "Other" | "Other" is never specified. The dream-persona answer fills it in: **Fire Protection**. Government shows up in the website research and the brief but **not** on the form, so it is not a requested segment. |
| Company size | 201–500, 501–1,000 | Mid-market. Below about 200 there's rarely budget for a $40k search. Above 1,000 there's usually in-house talent acquisition (TA), which removes the "no internal recruiting" pain. |
| Geography | North America; "EST and CST time zones in USA" | US only, Eastern and Central time zones. This covers about 36 states, including the Southeast and Midwest manufacturing belts. The form doesn't specify the split states (TN, KY, IN, MI, FL, ND, SD, NE, KS, TX); see §6. |
| Min revenue | $500K–$1M | **Non-binding in practice.** A 201-employee manufacturer is typically $30M+ in revenue, so the employee band does all the filtering. Don't add a revenue filter that could wrongly drop companies with missing revenue data. |
| Titles | CEO, COO, CFO, CHRO, President, Owner (+ VP, Founder by seniority) | Right buyers for exec search. CFO is weaker: it signs off but rarely starts a search, except when the search is for a finance leader. |
| Avoid | Manager, Director | Clear, but it **clashes with CHRO** at this size; see §5.2. |
| Dream personas | "Fire Protection, Human Resources, Mid-Sized Manufacturing" | Three personas, not three industries. "Human Resources" most likely means **the HR leader as buyer** (CHRO / VP HR), not HR-services companies. **[confirm]** |
| Buying signals | Systems integration; leadership vacancies; prolonged vacancies; expansion/new facilities; no internal recruiting; rapid growth/transformation | Good list, and most of it is sourceable (§4.3). "Systems integration" is unusual: it presumably means an ERP/MES/OT project that creates new leadership or specialist roles. **[confirm]** |
| Objective | Discovery call, Demo, Event invite, Other | Only the **discovery call** fits exec search. "Demo" doesn't apply, and no event exists. Treat the Hiring Process Review as the meeting. |
| Deal value / cycle | $40,000 / 4 weeks | See unit economics, §3. |
| Pain points | Can't find qualified candidates; ineffective hiring processes; (+ position profiles, structured interviews) | Only the first two are prospect pains. The last two are GRN's *solutions*. That's useful for proof, not for the opener. |
| Differentiators | Performance-based hiring; industry depth; passive talent; single-candidate presentations; rigorous qualification | The single-candidate stat is the most concrete and least generic. Lead proof with it. |
| Proof | >90% presentation-to-interview; 8 single-candidate hires in 2026; 85% repeat for 15 yrs; Fire & Life Safety client: 380 searched, 10 presented, 8 placed; GSA | The fire & life safety case study is the strongest asset for that segment, and nearly unusable outside it. |
| Tone | Consultative + Friendly/Casual | Their own samples read consultative and fairly formal, not casual. Write warm and plain, not chatty. |
| Offer | Complimentary Hiring Process Effectiveness Review | A good low-commitment offer for leaders with **no open role**, which widens the market beyond "has a vacancy now". |
| CTA | "Would you like to learn how our performance-based hiring approach can help improve your hiring results?" | Too soft and too long for LinkedIn. Keep the spirit and shorten it (§7). |
| DNC | `Do_Not_Contact_List.xlsx` uploaded | **Not loaded**: `dncList` in tracking_clients is `[]` and `dncCount` is 0. This blocks launch. |
| Assets | `GRN_LOGO_2026.docx` | A logo inside a .docx. We need real image files (PNG/SVG), plus headshots and a banner, for VA SDR profiles. |

## 3. Unit economics

- **Retainer:** $13,000/month = $156k/year.
- **Average deal:** $40k, so **about 4 placements a year just to cover the retainer**, and about 8 for a 2× return. This assumes "$40k" is the fee per placement, not per engagement **[confirm]**.
- **Back-of-envelope funnel** (assumptions, not data):
  - 15–25% of held discovery calls turning into a signed search = **16–27 held meetings per year to break even**, about 2 a month.
  - 30–50 held meetings a year to clearly win, about **3–4 a month**.
- **The 4-week cycle is fast** for exec search, so meetings should become revenue inside a quarter. If nothing has closed by month 3, the issue is more likely meeting quality than volume.
- **Implication:** this is a **quality-over-volume** account. One fit meeting with a 300-person manufacturer that has an open plant-manager role is worth more than ten "curious" meetings. Optimize sourcing for signals, not breadth.

## 4. Segments (= candidate sourcing configs)

The repo standard is segment = sourcing config, with outreach depth inverse to TAM/SAM. None of these exist in tracking_clients yet. This is the proposed order.

### 4.1 Fire & life safety: **open first**

- **Who:** fire sprinkler/suppression contractors, fire alarm and detection integrators, life-safety inspection/testing/maintenance (ITM) firms, and fire & security service companies. 201–1,000 employees, EST/CST.
- **Why first:**
  - It is the only segment with a **segment-specific case study** (380 → 10 → 8).
  - The brief calls it the high-priority niche.
  - Market noise is low compared with manufacturing.
  - The sector has been consolidating through PE-backed roll-ups. That creates exactly the signals they listed: acquisitions, integration ("systems integration" may mean exactly this), new branches, and leadership gaps at acquired companies. **[verify with data]**
- **Size read:** **narrow.** Mid-sized fire & life safety companies in this geography likely number in the low hundreds, not thousands. The brief's 500–2,000 estimate is probably high once the 201+ employee floor is applied. **To be measured, not assumed.**
- **Depth:** small TAM means **more contacts per company**: about **3–4** (Owner/President/CEO + COO/VP Ops + CHRO/VP HR, plus CFO only if needed to reach 3). Cover every qualifying company.
- **Watch-outs:**
  - PE-owned platforms often hire through the sponsor's talent partner. Target the **operating company**, not the holdco.
  - Many of the larger players are above 1,000 employees and out of band.

### 4.2 Mid-sized manufacturing: **open second, signal-led**

- **Who:** discrete and process manufacturers, 201–1,000 employees, EST/CST, with GRN's desks in mind (operations, engineering, purchasing, supply chain leadership).
- **Size read:** **wide.** Several thousand companies (the brief estimates 8–15k). Too broad to blast. Cut it with signals into sub-segments, each its own config or campaign:
  1. **New plant / expansion announced** in the last 6–12 months. Highest intent: new site leadership gets hired.
  2. **Open leadership or specialist role posted 60+ days.** The "prolonged vacancy" pain is exactly what GRN solves.
  3. **No internal TA:** no recruiter/TA titles on LinkedIn at a 201–500-employee company.
  4. **ERP/MES/OT implementation, or recent acquisition/ownership change.** This is the "systems integration / transformation" signal.
- **Depth:** large TAM means **fewer contacts per company**: about **1–2** (Owner/President/CEO, plus COO/VP Ops where the open role is operational).

### 4.3 HR-leader persona (cross-cutting angle, not a separate company list)

- "Human Resources" is best run as a **persona track** across 4.1 and 4.2: CHRO / VP HR / Head of People. The message is the **Hiring Process Effectiveness Review** rather than "we fill roles".
- This is the one buyer who feels "ineffective hiring process" personally, and who can say yes to a review without an open role.
- **Constraint:** see §5.2 on Director-level HR.

### 4.4 Government / public sector: **parked**

- GSA approval and the government-search pitch are real (website, brief). But the client **did not select it on the form**, and it has a different buyer, sales cycle and procurement path.
- Don't open it unless Harvey asks. **[confirm]**

## 5. Gaps, contradictions and risks

### 5.1 Contradictions between sources

- **Address:** the form gives *2020 Santa Maria St, Myrtle Beach SC 29579*; the website research gives *3721 Wesley Drive, Suite 135*. One is outdated. **[confirm]**. It matters for SDR profile location and email signatures.
- **"Eight" vs "nine" single-candidate hires in 2026:** the form's stats field says 8, and their own long-form email says 9. Use **8** until confirmed. Never put both in front of a prospect.
- **Speed positioning:** the website says GRN "drastically reduce[s] time to hire" and presents "in record time". The brief says *don't lead with speed*. The form's differentiators are all quality. **Follow the form:** quality and precision first, speed only as a supporting point.
- **Retained vs contingent:** the caller briefing calls them "retained executive search", but the brief only infers "direct-hire". This affects how the "what does it cost / what if it doesn't work" objections are answered. **[confirm]**
- **Contact name:** the brief refers to the primary contact as "Heden", which is the email handle. Their name is **Harvey Eden**, per the tracking_clients profile. The caller FAQs already use "Harvey".

### 5.2 Title exclusion vs. company size

- "Avoid Director" is sensible for operations, but at 201–500 employees the senior HR person is often titled **HR Director** or **Director of Human Resources**, not CHRO.
- A strict Director exclusion will remove most HR buyers in the lower half of the band.
- **Proposal:** exclude Director titles **except** the top HR title at companies with no VP/CHRO-level HR person. **[confirm with Harvey]**

### 5.3 Blockers before any launch

1. **DNC not loaded:** the xlsx is on the form, but tracking_clients has 0 entries. Load it via `update_client_dnc` before any list goes to HeyReach.
2. **No LinkedIn seats yet:**
   - Infra was submitted 2026-11-05 for **5 client LinkedIn seats + 5 VA seats**, but `list_client_accounts` returns 0.
   - The HeyReach workspace `172413` is connected but has no senders.
3. **No email channel:** `emailProvider` is empty, there's no Smartlead/Instantly, and no sending domains have been discussed. LinkedIn-only to start.
4. **Brand assets:** we have a logo in a .docx only. We need PNG/SVG, a banner and headshots for VA profiles. The SDR defaults (headline, about, location) are all empty.
5. **No onboarding call on record.** Book it via `get_client_meeting_links`. The open questions in §8 are its agenda.

### 5.4 Strategic risks

- **Franchise overlap:** other GRN offices may already work these companies or verticals. Outreach into a sister office's client would be awkward. **[confirm territory rules]**
- **"Recruiter fatigue":** owners of mid-sized manufacturers get a steady stream of recruiter outreach. The "enthusiastically rehire" question and the free review are the way around it, so don't open with "we fill roles".
- **Narrow niche burn:** the fire & life safety TAM is small, so sequencing mistakes there are expensive. Test copy on manufacturing sub-segments before spending the whole fire & life safety list.

## 6. ICP definition (proposed, for the first ICP config)

- **Geography:** US states in the Eastern and Central time zones. **[confirm]** whether split states (TN, KY, IN, MI, FL panhandle, TX El Paso, ND/SD/NE/KS west) are in. Simplest is to include whole states.
- **Size:** 201–1,000 employees. No revenue filter (see §2).
- **Industries:** fire & life safety (4.1); manufacturing (4.2). Exclude staffing/recruiting firms, HR-tech vendors and government (for now).
- **Include titles:** Owner, Founder, President, CEO, COO, CFO, CHRO, Chief People Officer, VP Operations, VP Manufacturing, VP Human Resources, VP People, General Manager (single-site companies only) **[confirm GM]**.
- **Exclude titles:** Manager, Director (except top HR per §5.2), Coordinator, Specialist, Recruiter, Talent Acquisition, Assistant, Intern.
- **Exclude companies:** client DNC list, existing GRN Piedmont clients **[need list]**, other GRN offices' clients **[need rule]**.

## 7. Messaging analysis

**What to keep:**
- **The hook:** "Of the people your organization hired over the past year, how many would you enthusiastically rehire?" It's distinctive, it's theirs, and it is a question a CEO actually thinks about.
- **The proof:** single-candidate hires; >90% presentation-to-interview; for fire & life safety, the 380 → 10 → 8 case study.
- **The offer:** the Complimentary Hiring Process Effectiveness Review.
- **Voice rules:** never "staffing"; no speed-first claims; no jargon ("talent acquisition solutions", "end-to-end"); "we" for the firm, "I" for the ask.

**What to change:**
- **Length:** their short LinkedIn sample is ~480 characters, well over the 300-character connection-note limit. It also packs hook, belief statement and positioning into one message. Split it: hook in the connection request (or no note), proof in message 1, offer in message 2.
- **CTA:** the form's CTA is a long yes/no question about "learning about our approach". Better: a specific, low-commitment ask tied to the review, e.g. "Worth a 20-minute look at how you're hiring leaders today?"
- **Segment-specific proof:** in manufacturing, lead with single-candidate hires. In fire & life safety, lead with the 380 → 10 → 8 case study and "we already know your industry".
- **Signal-specific openers** (e.g. new plant, a long-open role) beat the generic hook when the signal is real. Keep the hook for no-signal lists and HR-persona messages.

## 8. Open questions for Harvey (onboarding-call agenda)

1. Is the $40k figure per placement, and what is the fee model: retained, contingent, or mixed?
2. Which address is current, and is the 2026 single-candidate count 8 or 9?
3. Does "Human Resources" mean HR leaders as buyers, or a target industry?
4. Is Director-level HR acceptable at companies under ~500 employees with no VP/CHRO-level HR?
5. Are existing GRN Piedmont clients excluded, and can we get the list? Are there GRN network territory or client conflicts to avoid?
6. Is government/public-sector outreach wanted at all?
7. Whose LinkedIn accounts will send (Harvey, Chris Missler)? Do they have Sales Navigator? Are they comfortable with VA-operated profiles under the GRN brand and with anonymous referral-style campaigns?
8. Do they want to approve copy before launch? How should replies and warm leads be handed off, and to whom?
9. Do they have an existing CRM/ATS database for a re-engagement campaign?
10. What does "systems integration" mean as a signal for them?
11. What is the target launch date?

## 9. Recommended next steps (in order)

1. **Load the DNC** file into tracking_clients (`update_client_dnc`). It needs the xlsx from the Typeform upload, which is not in this repo.
2. **Book the onboarding call** and use §8 as the agenda.
3. **Size the fire & life safety segment with real data** (Blitz / AI Ark, eyeballing results per repo guidance). Record the count and per-company depth in its `.query.md`.
4. Create the first **ICP config and sourcing config** (fire & life safety) in tracking_clients, then mirror it here.
5. When senders exist, run the **HeyReach Vertical Launch** build (4 campaigns + 2 webhooks) for fire & life safety, then manufacturing sub-segments.
6. Draft copy following §7, then put it to Harvey for approval. Approval is required: `autoApprove` is false.
