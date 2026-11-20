"""DNC / client matcher for the Doc 2 sizing. Normalised-name prefix match against context/2026-11-12-dnc-accounts.csv
(199 rows) + known HLD clients + aliases. A company matches when the DNC key's tokens are the first tokens of its
normalised name (so 'gilead' matches 'Gilead Sciences' but 'ani pharmaceuticals' never matches 'Animal ...').
Matches marked review=True are close calls kept as flags, not auto-removed."""
import csv, re, os
HERE = os.path.dirname(os.path.abspath(__file__))
SUFFIX = {"inc", "llc", "corp", "corporation", "co", "ltd", "limited", "lp", "plc", "the", "sa", "sarl", "us", "usa", "fka", "aka"}
def norm(s):
    s = re.split(r",? a division of |,? powered by |,? an? \w+ company\b", (s or "").lower())[0]
    s = re.sub(r"\(d\)", "d", s)   # SOLVE(D) -> solved, not solve
    s = re.sub(r"\(.*?\)", " ", s).replace("&", " and ").replace("+", " and ")
    return [t for t in re.sub(r"[^a-z0-9 ]", " ", s).split() if t not in SUFFIX]
def load_keys():
    names = [r[0] for r in csv.reader(open(os.path.join(HERE, "../../context/2026-11-12-dnc-accounts.csv"))) if r and r[0] != "account_name"]
    keys = [(n, norm(n), "dnc") for n in names]
    clients = ["AstraZeneca", "Alexion", "AbbVie", "Allergan", "Gilead", "Kite Pharma", "Takeda", "Incyte", "Bausch Health",
               "Bausch and Lomb", "Salix Pharmaceuticals", "Octapharma", "Publicis Health Media", "EVERSANA", "Relevate Health"]
    keys += [(n, norm(n), "client") for n in clients]
    aliases = {"GSW": "Syneos Health (GSW is its agency)", "Syneos": "Syneos Health", "CMI": "CMI Media Group",
               "Health Monitor Network": "Health Monitor", "MJH": "MJH Life Sciences", "Vaniam": "Vaniam Group",
               "Hibbert": "The Hibbert Group", "Cadent Aperture": "Cadent", "WebMD": "WebMD", "Medscape": "WebMD",
               "Veeva": "Veeva Systems", "Doximity": "Doximity", "ZS": "ZS Associates", "InStep": "InStep Health",
               "Evolution Health": "Evolution Health Group", "Fingerpaint": "Fingerpaint", "Underscore": "Underscore"}
    keys += [(src, norm(a), "alias") for a, src in aliases.items()]
    return [k for k in keys if k[1]]
KEYS = load_keys()
REVIEW = {"publicis health", "deerfield", "cadent medical", "prompt"}
# confirmed false positives: single-word DNC names that collide with unrelated companies
FALSE_POS = {"verve therapeutics"}   # same parent / similar name to a DNC row, not the same company
def match(name):
    t = norm(name)
    if " ".join(t) in FALSE_POS: return None
    j0 = " ".join(t)
    for r in ("cadent medical", "prompt"):
        if j0.startswith(r): return {"dnc_source": r, "kind": "review", "review": True}
    for src, k, kind in KEYS:
        # first word must match exactly; later words may be abbreviated in the DNC row (Pharma -> Pharmaceuticals), 4+ chars
        if len(t) >= len(k) and t[0] == k[0] and all(a == b or (len(b) >= 4 and a.startswith(b)) for a, b in zip(t[1:len(k)], k[1:])):
            return {"dnc_source": src, "kind": kind, "review": False}
    j = " ".join(t)
    for r in REVIEW:
        if j.startswith(r): return {"dnc_source": r, "kind": "review", "review": True}
    return None
