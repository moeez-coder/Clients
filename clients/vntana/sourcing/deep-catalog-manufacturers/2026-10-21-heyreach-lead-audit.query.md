# Query — 2026-10-21 parity audit of leads loaded into the two HeyReach test campaigns

Config `82d47d88-32b2-4dd8-8307-b12ac530aaf7`, campaign 6. **Expanding existing segment** (QA of what the owner loaded from Clay; no new sourcing). **Why:** owner asked to check data and messaging after loading leads.
**Source:** HeyReach `get_leads_from_list` (MCP VNTANA) on list `1049528` (Offer 1, campaign `673174`, 868 leads) and `1049529` (Offer 2, campaign `673175`, 864 leads), read in full on 2026-10-21 via 6 read-only subagents transcribing id, name, company, position and the `sku` custom field. Joined to `2026-10-21-sku-counts.csv` on company LinkedIn URL when present, else normalized company name. Script: `2026-10-21-scripts/audit_leads.py`.
**Output:** `2026-10-21-heyreach-lead-audit.csv`, one row per flagged lead (372 rows), `flags` explains why. Nothing was changed in HeyReach.
**Caveat:** the subagent transcription was spot-checked by row counts matching the API totals (868 and 864), not by re-reading every row. Title and A&D flags are keyword regex, so check before deleting (e.g. false hits on "Space" in a product name).
