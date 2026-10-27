"""Select a HeyReach wave from the qualified snapshot and clean first names for the {FIRST_NAME} greeting.

Usage: python3 build_wave.py <qualified-leads.csv> <out.csv> <n> [exclude.csv ...] [--drop-odd-names]
Selection: QUALIFIED, within_company_cap=yes, Northeast first, then qualified_rank, then company name.
Drops rows whose name is clearly not a person (first name is a word of the company name, or the
first name contains a job title). Cleans the greeting name: a nickname in brackets wins ("Stoyan (Tony)" ->
"Tony"), trailing initials are stripped ("John B." -> "John"), ALL-CAPS is title-cased. The raw first
name is kept in first_name_raw. Leads already in any exclude CSV (e.g. earlier waves) are skipped.
"""
import csv, re, sys
NE = {'NY', 'NJ', 'CT', 'MA', 'PA', 'MD', 'DE', 'DC', 'RI', 'NH', 'VT', 'ME'}
TITLE_WORDS = {'cio', 'cto', 'ciso', 'vp', 'head', 'chief', 'director'}


def greeting(f):
    m = re.search(r"\(([^)]+)\)", f)
    f = (m.group(1) if m else re.sub(r"\(.*?\)", "", f)).strip()
    f = re.sub(r"(\s+([A-Z]\.)+)+$", "", f).strip()                # trailing initials ("B.", "G.A.")
    f = f.split()[0] if f.split() and f.split()[0].endswith(".") is False and len(f.split()) > 1 and all(len(p) <= 2 for p in f.split()[1:]) else f
    return f.title() if f.isupper() and len(f) > 2 else f


def odd_name(f):
    """HeyReach greets with the LinkedIn-resolved name, not what we send (wave 1), so a raw name that
    would render badly ("Stoyan (Tony)", "John B.", "CASEY", "Naresh H.") is dropped, not cleaned."""
    f = (f or "").strip()
    return (not f or "(" in f or re.search(r"\b[A-Z]\.", f) is not None or (f.isupper() and len(f) > 2)
            or re.search(r"[^A-Za-zÀ-ÿ' \-]", f) is not None or len(f) < 2)


def not_a_person(x):
    f = x['first_name'].lower()
    return f in x['company_name'].lower().split() or bool(TITLE_WORDS & set(re.findall(r"[a-z]+", f)))


src, out, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
seen = {r['linkedin_url'] for p in sys.argv[4:] if not p.startswith('--') for r in csv.DictReader(open(p))}
rows = [x for x in csv.DictReader(open(src)) if x['lead_verdict'] == 'QUALIFIED' and x['within_company_cap'] == 'yes'
        and x['first_name'] != '-' and x['linkedin_url'] not in seen]
rows.sort(key=lambda x: (x['person_state'] not in NE, int(x['qualified_rank']), x['company_name'].lower()))
dropped, wave = [], []
for x in rows:
    if len(wave) == n:
        break
    if not_a_person(x):
        dropped.append(x); continue
    if "--drop-odd-names" in sys.argv and odd_name(x['first_name']):
        dropped.append(dict(x, _why="odd name")); continue
    x = dict(x, first_name_raw=x['first_name'], first_name=greeting(x['first_name']))
    wave.append(x)
cols = ['linkedin_url', 'first_name', 'first_name_raw', 'last_name', 'job_title', 'persona_role', 'company_name',
        'company_domain', 'company_linkedin_url', 'person_city', 'person_state', 'person_country', 'qualified_rank']
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, cols, extrasaction='ignore'); w.writeheader(); w.writerows(wave)
print(f"{len(wave)} written, Northeast {sum(x['person_state'] in NE for x in wave)}, companies {len({x['company_linkedin_url'] for x in wave})}")
for x in dropped:
    print(f"dropped ({x.get('_why', 'not a person')}):", repr(x['first_name']), x['last_name'], '|', x['company_name'])
for x in wave:
    if x['first_name'] != x['first_name_raw']:
        print("greeting cleaned:", repr(x['first_name_raw']), '->', repr(x['first_name']))
