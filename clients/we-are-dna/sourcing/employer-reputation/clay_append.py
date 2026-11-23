"""Append one Clay MCP search-contacts result to <date>-clay-calls/<campaign>-<batch>.json (Doc 1 C1-3 gap-fill).
Usage: python3 clay_append.py <campaign c1c2|c3> <batch_no> --file <saved tool-result path>
   or: python3 clay_append.py <campaign> <batch_no> --stdin   (paste {"taskId":..., "contacts":[...]} JSON on stdin)
Keeps only taskId and contacts (name, title, url, location, domain, companyIdentifier, profile_id, start date)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); camp, b = sys.argv[1], int(sys.argv[2])
d = json.load(open(sys.argv[4])) if sys.argv[3] == "--file" else json.load(sys.stdin)
K = ("name", "latest_experience_title", "url", "location_name", "domain", "companyIdentifier", "profile_id", "latest_experience_start_date")
rec = {"campaign": camp, "batch": b, "taskId": d.get("taskId"), "contacts": [{k: c.get(k) for k in K} for c in d.get("contacts", [])]}
os.makedirs(os.path.join(HERE, "2026-11-23-clay-calls"), exist_ok=True)
json.dump(rec, open(os.path.join(HERE, "2026-11-23-clay-calls", f"{camp}-{b:03d}.json"), "w"), indent=1)
print(camp, b, "contacts", len(rec["contacts"]))
