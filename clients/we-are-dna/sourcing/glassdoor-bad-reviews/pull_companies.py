"""Glassdoor bad-review campaign (We Are DNA), 2026-11-17: pull the ICP company pool from Blitz.
Blitz POST /v2/search/companies, UK HQ (hq.country_code GB), 201+ employees, doc 1's five sectors
(industry labels copied from ../tam/tam_counts.py SEGMENTS, legacy + current names). One query per
sector x size band (keeps each slice far under the 50k cap); paged with max_results=25 until cursor is null.
Raw responses -> <date>-companies-blitz-raw.jsonl. Usage: python3 pull_companies.py 2026-11-17"""
import ast, json, os, sys, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(HERE, "..", "tam", "tam_counts.py")).read()
_node = next(n for n in ast.parse(_src).body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "SEGMENTS")
SEGMENTS = eval(compile(ast.Expression(_node.value), "tam_counts.py", "eval"), {"dict": dict})
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
BANDS_ALL = {"51-200": ["51-200"], "201-500": ["201-500"], "501-1000": ["501-1000"], "1001-5000": ["1001-5000"], "5001+": ["5001-10000", "10001+"]}
BANDS = {"201-500": ["201-500"], "501-1000": ["501-1000"], "1001-5000": ["1001-5000"], "5001+": ["5001-10000", "10001+"]}

def post(body):
    for i in range(5):
        try:
            r = urllib.request.urlopen(urllib.request.Request("https://api.blitz-api.ai/v2/search/companies",
                                       json.dumps(body).encode(), H), timeout=90)
            return json.load(r)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            print("retry", i, e, file=sys.stderr); time.sleep(2 * (i + 1))
    raise SystemExit("blitz failed")

date = sys.argv[1]
# optional 2nd arg: comma-separated band names to pull (default: all in BANDS); 3rd arg: output suffix
if len(sys.argv) > 2:
    BANDS = {b: BANDS_ALL[b] for b in sys.argv[2].split(",")}
suffix = sys.argv[3] if len(sys.argv) > 3 else ""
out_path = os.path.join(HERE, f"{date}{suffix}-companies-blitz-raw.jsonl")
assert not os.path.exists(out_path) and not os.path.exists(out_path + ".gz"), "append-only: pick a new suffix"
out = open(out_path, "w")
used = 0
for seg, s in SEGMENTS.items():
    for band, rng in BANDS.items():
        cursor, n, pages = None, 0, 0
        while True:
            body = {"company": {"industry": {"include": s["industries"]}, "employee_range": rng,
                                "hq": {"country_code": ["GB"]}}, "max_results": 25, "cursor": cursor}
            d = post(body)
            used += d.get("fair_usage", {}).get("records_used", 0)
            for r in d.get("results", []):
                out.write(json.dumps({"segment": seg, "band": band, "record": r}) + "\n"); n += 1
            cursor = d.get("cursor"); pages += 1
            if not cursor or not d.get("results"):
                break
        print(seg, band, n, "rows", pages, "pages", flush=True)
print("records_used", used)
