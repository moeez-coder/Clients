"""Extract Doc 1 v4 Campaigns 1-3 copy verbatim (campaign-docs/2026-11-20-doc-1-v4.md) into tracking_clients
set_campaign_sequence steps. Variables: {first_name} -> {{module.standard.first_name}}, {company} ->
{{module.standard.company_name}}, {sector_peers} -> {{module.custom.sector_peers}}, {theme} -> {{module.custom.theme}}.
Delays: the doc gives none for Campaigns 1-3, so Campaign 6's cadence is used: message 1 on accept, +3, +3 days.
Writes campaign-docs/2026-11-23-doc1-c1-3-sequences.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); DOC = os.path.join(HERE, "..", "2026-11-20-doc-1-v4.md")
t = open(DOC).read()
VARS = {"{first_name}": "{{module.standard.first_name}}", "{company}": "{{module.standard.company_name}}",
        "{sector_peers}": "{{module.custom.sector_peers}}", "{theme}": "{{module.custom.theme}}"}
out = {}
for n in (1, 2, 3):
    sec = t.split(f"## Campaign {n}:")[1].split("\n## ")[0].split("### Messaging")[1].split("\n### ")[0]
    parts = re.split(r"\n\*\*(Connection request|Message 1|Message 2|Message 3)\*\*\n", sec)
    blocks = dict(zip(parts[1::2], [p.strip() for p in parts[2::2]]))
    steps = []
    for i, (k, typ, delay) in enumerate([("Connection request", "connection_request", 0), ("Message 1", "dm", 0), ("Message 2", "dm", 3), ("Message 3", "dm", 3)], 1):
        raw = blocks[k]; c = raw
        for a, b in VARS.items(): c = c.replace(a, b)
        steps.append({"step_number": i, "channel": "linkedin", "type": typ, "thread_id": "t1", "subject": None, "copy": c, "delay_days": delay, "doc_text": raw})
    out[f"c{n}"] = steps
json.dump(out, open(os.path.join(HERE, "..", "2026-11-23-doc1-c1-3-sequences.json"), "w"), indent=1, ensure_ascii=False)
for k, s in out.items():
    print(k, [len(x["doc_text"]) for x in s], "dashes:", any("—" in x["copy"] or "–" in x["copy"] for x in s))
