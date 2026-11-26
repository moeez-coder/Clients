"""Split the 2026-11-26 size-expansion job descriptions into phrase batches for Claude sub-agents (Moe's JD-phrase prompt,
../recruitment-specific-open-roles/jd_phrase_prompt.md, with the same working constraints as earlier waves: PROMPT.md).
Each input is {"id", "title", "company", "job_description"}; the JD is cut to MAXC characters, starting at the requirements
section when one is found (that is where the phrase comes from), else from the top; no JD -> Blitz ai_summary.
Writes $RAW/$PHR/in_NN.json, ids.json (id -> company url), PROMPT.md.  Usage: RAW=/path PHR=phr-wide N=10 python3 make_phrase_batches.py"""
import json, os, re, shutil
RAW = os.environ["RAW"]; PHR = os.path.join(RAW, os.environ.get("PHR", "phr-wide")); N = int(os.environ.get("N", 10)); MAXC = 2200
os.makedirs(PHR, exist_ok=True)
REQ = re.compile(r"(requirements|qualifications|what you(?:'|’)ll need|what we(?:'|’)re looking for|you have|experience required|skills)", re.I)
comps = {c["company_linkedin_url"]: c for c in json.load(open(os.path.join(RAW, "wide-companies.json")))}
jd = [json.loads(l) for l in open(os.path.join(RAW, "wide-jd.jsonl"))]
items, ids = [], {}
for i, j in enumerate(sorted(jd, key=lambda j: j["company_linkedin_url"])):
    d = j["description"] or j["jd_summary"] or ""
    m = REQ.search(d, 300)
    d = d[max(0, m.start() - 200):][:MAXC] if m and len(d) > MAXC else d[:MAXC]
    items.append({"id": i, "title": j["open_role"], "company": comps[j["company_linkedin_url"]]["company_name"], "job_description": d})
    ids[i] = j["company_linkedin_url"]
json.dump(ids, open(os.path.join(PHR, "ids.json"), "w"))
k = -(-len(items) // N)
for b in range(N):
    json.dump(items[b * k:(b + 1) * k], open(os.path.join(PHR, f"in_{b:02d}.json"), "w"))
src = os.path.join(RAW, "..", "mpc-build", "phr4", "PROMPT.md")
shutil.copy(src, os.path.join(PHR, "PROMPT.md"))
print(len(items), "items in", N, "batches of", k)
