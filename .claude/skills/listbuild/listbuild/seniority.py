"""Title-level guard for 'director and above'.

Provider seniority enums leak a few percent of sub-director titles. This classifier looks at
the raw title and returns 'pass', 'fail' or 'unknown' (no title to judge). Unknown rows are
kept; failing rows are dropped from the export.
"""
import re
import unicodedata

_STRONG = re.compile(
    r"\b(directors?|directeur|directrice|diretor|diretora|vp|svp|evp|avp|vice[- ]?president|head|chief|c[a-z]{1,2}o|"
    r"president|owner|founder|co[- ]?founder|proprietor|board member|chair|chairman|chairwoman|chairperson|"
    r"general manager|managing member|entrepreneur|fondateur|fondatrice|proprietaire)\b"
)
# Weak positives pass only when no individual-contributor / manager word is present.
_WEAK = re.compile(r"\b(partner|principal|md)\b")
_IC_WORDS = re.compile(
    r"\b(manager|coordinator|specialist|associate|analyst|executive|representative|consultant|engineer|"
    r"assistant|intern|trainee|student|apprentice)\b"
)
_HARD_FAIL = re.compile(r"\b(assistant|intern|trainee|student|apprentice)\b|advisory board|board advisor|advisor to the board")
_TOKEN = re.compile(r"[a-z0-9]+|[&,/|-]")
_PARTNER_QUALIFIERS = {"&", ",", "/", "|", "-", "and", "senior", "managing", "general", "equity", "founding", "salaried", "associate", "junior", "name"}
_PARTNER_COMPOUNDS = {"manager", "management", "marketing", "success", "relations", "program", "programs", "development", "sales",
                      "specialist", "coordinator", "enablement", "operations", "support", "engineer", "executive"}
_DOTTED_ABBREV = re.compile(r"\b(?:[a-z]\.\s?){2,}")  # v.p. / s.v.p. / c.e.o.


def _fold(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).lower()


def _standalone_partner(tokens):
    """'Partner' is a role of its own at the start / after a separator or qualifier and not part of a compound noun."""
    for i, tok in enumerate(tokens):
        if tok != "partner":
            continue
        prev = tokens[i - 1] if i > 0 else "&"
        nxt = tokens[i + 1] if i + 1 < len(tokens) else None
        if prev in _PARTNER_QUALIFIERS and nxt not in _PARTNER_COMPOUNDS:
            return True
    return False


def classify_title(title):
    if not title or not isinstance(title, str) or not title.strip():
        return "unknown"
    t = _fold(title)
    t = _DOTTED_ABBREV.sub(lambda m: m.group(0).replace(".", "").replace(" ", "") + " ", t)
    t = re.sub(r"\bproduct owner\b", "productowner", t)  # an IC role, not an owner
    if _HARD_FAIL.search(t):
        return "fail"
    if _STRONG.search(t):
        return "pass"
    if _standalone_partner(_TOKEN.findall(t)):
        return "pass"
    if _WEAK.search(t) and not _IC_WORDS.search(t):
        return "pass"
    return "fail"
