"""Prior-contact CSVs (any export with a LinkedIn column) -> exclusion keys."""
import csv
from pathlib import Path

from .identity import alt_key, normalize_linkedin_url

csv.field_size_limit(10**8)


def _pick(header, *cands):
    hl = [h.lower().strip() for h in header]
    for cand in cands:
        for i, h in enumerate(hl):
            if cand in h:
                return header[i]
    return None


def detect_columns(header):
    return {
        "linkedin": _pick(header, "linkedin url", "linkedin_url", "linkedin", "profile url", "profile_url"),
        "first": _pick(header, "first name", "first_name", "firstname"),
        "last": _pick(header, "last name", "last_name", "lastname"),
        "domain": _pick(header, "company domain", "company_domain", "domain", "website", "company website"),
    }


def iter_seed_rows(paths):
    """Yield dicts with linkedin_url / first_name / last_name / company_domain / origin for every row."""
    for path in paths:
        p = Path(path)
        with p.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            cols = detect_columns(reader.fieldnames or [])
            for row in reader:
                yield {
                    "linkedin_url": row.get(cols["linkedin"]) if cols["linkedin"] else None,
                    "first_name": row.get(cols["first"]) if cols["first"] else None,
                    "last_name": row.get(cols["last"]) if cols["last"] else None,
                    "company_domain": row.get(cols["domain"]) if cols["domain"] else None,
                    "origin": p.name,
                }


def load_seed_keys(paths):
    """(set of normalised LinkedIn URLs, set of first+last+domain keys) across all files."""
    li, alt = set(), set()
    for r in iter_seed_rows(paths):
        u = normalize_linkedin_url(r["linkedin_url"])
        if u:
            li.add(u)
        a = alt_key(r["first_name"], r["last_name"], r["company_domain"])
        if a:
            alt.add(a)
    return li, alt


def is_seeded(row, li, alt):
    u = normalize_linkedin_url(row.get("linkedin_url"))
    if u and u in li:
        return True
    a = alt_key(row.get("first_name"), row.get("last_name"), row.get("company_domain"))
    return bool(a and a in alt)
