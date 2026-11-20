"""Glassdoor bad-review campaign (We Are DNA), 2026-11-17: company pool size by sector x size band.
Count only: Blitz POST /v2/search/companies, max_results=1, reads total_results (indicative, see CLAUDE.md).
Industries are doc 1's five sectors, copied from ../tam/tam_counts.py. Output: gd_counts.json."""
import json, os, sys, urllib.request
import ast
# tam_counts.py has no __main__ guard (importing it re-runs its calls), so read SEGMENTS out of it statically.
_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tam", "tam_counts.py")).read()
_node = next(n for n in ast.parse(_src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SEGMENTS")
SEGMENTS = eval(compile(ast.Expression(_node.value), "tam_counts.py", "eval"), {"dict": dict})
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
BANDS = {"201-500": ["201-500"], "501-1000": ["501-1000"], "1001+": ["1001-5000", "5001-10000", "10001+"]}
out = {}
for seg, s in SEGMENTS.items():
    for band, rng in BANDS.items():
        body = {"company": {"industry": {"include": s["industries"]}, "employee_range": rng,
                            "hq": {"country_code": ["GB"]}}, "max_results": 1}
        r = urllib.request.urlopen(urllib.request.Request("https://api.blitz-api.ai/v2/search/companies",
                                   json.dumps(body).encode(), H), timeout=60)
        d = json.load(r)
        out[f"{seg}|{band}"] = {"total_results": d.get("total_results"), "body": body}
        print(seg, band, d.get("total_results"))
json.dump(out, open(os.path.join(os.path.dirname(__file__), "gd_counts.json"), "w"), indent=1)
