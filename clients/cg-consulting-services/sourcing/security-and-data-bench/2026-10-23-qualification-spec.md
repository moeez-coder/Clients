# Qualification spec: Security and Data Bench (C&G Consulting Services)

Each Haiku agent gets this spec plus a batch file. Each batch row is **one company and its candidate leads**, at most 3, from the Blitz pull. The agent judges every company and every person **individually**. It has no web access; it uses the row data plus its own knowledge of the company. It writes one JSON line per company.

Sources:
- tracking_clients ICP config `885e8da7-6318-4ede-b434-68cf84512790`
- segment `2bef2c27-…`
- persona `e399896d-…`
- sourcing config `09be87f3-0db4-4e2d-842d-b70af7d29d7c`
- campaign `c8855ae2-…`
- `context/client-brief.md` and `context/icp-form.md`

## Who the client is

C&G Consulting Services is a New Jersey staffing firm. It fills **technology** roles (software engineering, IT security, data science and data engineering, IT project management) and life-sciences roles. It works on contract, direct hire, temp-to-perm and project teams. The campaign pitch: AI, data and security roles are the hardest technical seats to fill; C&G is privately held with fair pricing and a 100% onshore team.

## Company: QUALIFIED when ALL hold

1. **It is an operating company that employs its own in-house technology team**, meaning engineering, IT, security or data people on staff, in one of these sectors:
   - **software / SaaS / internet / security software / data and analytics software**
   - **fintech, banking, capital markets, investment management**
   - **insurance carriers**
   - **education companies and education publishers** (edtech, e-learning, curriculum and textbook publishers)
   - **retail and e-commerce**
2. **US-based**: headquartered in the US, or with its main US operation here.
3. **Plausibly $20M+ revenue and roughly 200 to 5,000 employees.** The Blitz pull already filtered on this, so reject only on clear contrary knowledge, e.g. it is plainly a 20-person shop or a 50,000-employee global giant.

## Company: NOT QUALIFIED if ANY hold

- **Staffing, recruiting, RPO, executive search or talent marketplace.** These are competitors.
- **IT services, IT consulting, outsourcing, offshore development or MSP firms** whose business is supplying technologists to others. They are competitors for the same talent and budget.
- **Government agency, public school district, university or college, nonprofit or association.** The qualifier says "companies"; an education *company* or *publisher* is fine.
- **Insurance agencies and brokerages** with no meaningful in-house tech team, or a company in an obviously different sector that Blitz mis-tagged (e.g. a construction firm labelled software).
- **Clearly outside the size band**, or defunct, acquired and absorbed, or a holding shell.
- Any company on the client's DNC list, if one is provided in the batch (none loaded yet).

## Person: QUALIFIED when ALL hold

1. **Their current title is one of the persona roles at this company:** CIO, CTO, CISO, VP or SVP or EVP of Engineering, VP of Data, Head of Data, Head of IT. Spelled-out forms count. A combined title counts when one of these roles is real, e.g. "SVP & CIO" or "CTO and Co-founder".
2. **They are a hiring decision maker for technology roles at this company.** They own the team, not a customer-facing role that borrows the title.
3. **Based in the US.**

## Person: NOT QUALIFIED if ANY hold

- A field, partner, channel, solutions or sales CTO; a "CTO in residence"; a fractional, virtual, interim-for-hire or advisory CISO/CIO/CTO; an advisor, board member, consultant or former holder.
- A deputy, assistant or associate version of the role, or a director-level title.
- The title belongs to a different company than the one in the row (a stale experience).
- **The company itself is NOT QUALIFIED.** Every person at that company is then NOT QUALIFIED, reason "company not qualified".

## Output (one JSON object per line, one line per input company, in input order)

```json
{"company_linkedin_url": "...", "company_verdict": "QUALIFIED|NOT_QUALIFIED", "company_reason": "<=20 words",
 "leads": [{"linkedin_url": "...", "lead_verdict": "QUALIFIED|NOT_QUALIFIED", "lead_reason": "<=15 words"}]}
```

- Every input company and every input lead must appear exactly once, keyed by the URLs exactly as given.
- When unsure about a company, decide from the sector rules above and say "uncertain" in the reason. Don't invent facts.
