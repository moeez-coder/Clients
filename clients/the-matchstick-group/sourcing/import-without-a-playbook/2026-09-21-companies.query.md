# Query — The Import Without a Playbook, 2026-09-21

**Campaign 6** — segment: US subsidiaries of non-US medtech/diagnostics parents (Europe, Japan,
Israel, Korea), $100M-$500M in US revenue.

**Tool:** ColdIQ Marketplace API, `POST /v1/companies/search`, `provider: "fullenrich"`.

**Filter used:**
```json
{"industries": ["Medical Equipment Manufacturing"], "countries": ["DE","JP","IL","KR","CH","FR","SE","NL"], "min_employees": 500, "limit": 100}
```

**Important caveat — this sources PARENTS, not US subsidiaries:** the `countries` filter matches
company HQ location, so this pull returns non-US-headquartered medtech companies of plausible scale.
It does **not** identify which of these actually maintain a US subsidiary/affiliate with its own
marketing organization (the actual persona target), nor does it verify the $100M-$500M **US-specific**
revenue band, nor the FDA-clearance/US-expansion trigger. This list is the parent-company candidate
pool the US-subsidiary research has to start from, not the qualified segment itself. Countries list
extended beyond the brief's four (added CH/FR/SE/NL) to widen the candidate pool given time/credit
constraints — flagged as a deviation from the literal brief, worth confirming with the client.

**Result:** 27 unique new companies added; 74 total in the CSV after merging an earlier pull.

**Cost:** ~896 credits (~$12.80).
