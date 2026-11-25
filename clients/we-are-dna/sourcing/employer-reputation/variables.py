"""Clean {first_name} and {company} for Doc 1 Campaigns 1-3 copy (We Are DNA). Shared by preview and full pull.
first_name: drop honorifics (Dr, Mr, Mrs, Ms, Prof, Sir, Dame), brackets and emoji, keep the first word.
company: drop brackets and legal suffixes (Ltd, Limited, plc, LLP, Group Ltd stays 'Group'), title-case names in ALL CAPS
longer than 4 letters (ALBERT BARTLETT -> Albert Bartlett; ICG stays ICG)."""
import re
HON = re.compile(r"^(dr|mr|mrs|ms|miss|prof|professor|sir|dame)\.?\s+", re.I)
def first_name(fn, full=""):
    s = re.sub(r"\(.*?\)", "", fn or "").strip()
    s = HON.sub("", s) if s else s
    if not s or s.lower() in ("dr", "mr", "mrs", "ms", "prof", "sir", "dame"):
        s = HON.sub("", re.sub(r"\(.*?\)", "", full or "")).strip()
    s = re.sub(r"[^\w'\-À-ÿ ]", "", s).strip()
    w = s.split()[0] if s.split() else "-"
    return w[:1].upper() + w[1:] if w.islower() or w.isupper() else w
SUFFIX = re.compile(r"[\s,]+(ltd\.?|limited|plc|llp|llc|inc\.?|uk ltd|\(uk\))$", re.I)
def company(name):
    s = re.sub(r"\s*\(.*?\)", "", name or "").strip()
    for _ in range(2): s = SUFFIX.sub("", s).strip()
    s = s.replace(" Stores", "") if s.endswith(" Stores") else s
    if s.isupper() and len(s.replace(" ", "")) > 4: s = " ".join(w.capitalize() for w in s.split())
    return s or name
