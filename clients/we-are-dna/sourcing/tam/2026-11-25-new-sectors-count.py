"""We Are DNA, 2026-11-25: size three candidate new sectors for Doc 1 C1-3 (Moe: "count new sectors first").
Count only: Blitz POST /v2/search/companies, max_results=1, total_results (indicative). UK HQ, by size band.
Labels verbatim from docs/blitz-api/company-search-industries.txt, legacy + current names.
Consulting labels are LinkedIn catch-alls (CLAUDE.md): counted for size only, never core without a keyword gate."""
import json, os, urllib.request
H = {"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"}
SECTORS = {
 "Tech": ["Software Development", "Computer Software", "IT Services and IT Consulting", "Information Technology and Services",
          "Technology; Information and Internet", "Internet"],
 "Education (private)": ["Education", "Education Management", "Education Administration Programs", "E-Learning Providers", "E-learning",
          "Primary and Secondary Education", "Higher Education", "Professional Training and Coaching"],
 "Consulting (catch-all)": ["Business Consulting and Services", "Management Consulting"]}
BANDS = {"51-200": ["51-200"], "201-500": ["201-500"], "501-1000": ["501-1000"], "1001+": ["1001-5000", "5001-10000", "10001+"]}
out = {}
for s, ind in SECTORS.items():
    for b, rng in BANDS.items():
        body = {"company": {"industry": {"include": ind}, "employee_range": rng, "hq": {"country_code": ["GB"]}}, "max_results": 1}
        d = json.load(urllib.request.urlopen(urllib.request.Request("https://api.blitz-api.ai/v2/search/companies", json.dumps(body).encode(), H), timeout=60))
        out[f"{s}|{b}"] = d.get("total_results"); print(s, b, d.get("total_results"), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "2026-11-25-new-sectors-count.json"), "w"), indent=1)
