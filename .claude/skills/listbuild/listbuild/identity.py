"""Canonical identity helpers shared by every provider adapter.

Primary key for a contact is the normalised LinkedIn URL. When a provider gives no
LinkedIn URL the fallback key is sha1(first|last|domain). Both are stored on every row so
that a later provider matching on either one is recognised as a duplicate.
"""
import hashlib
import re
from urllib.parse import urlsplit

_LEGAL_SUFFIXES = {
    "inc", "incorporated", "llc", "ltd", "limited", "plc", "corp", "corporation", "pty", "pte",
    "gmbh", "bv", "nv", "sa", "ag", "llp", "lp", "pllc", "pc", "sarl", "srl", "pvt",
}
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def _host_and_path(url: str):
    u = url.strip()
    if not u:
        return None, None
    if "://" not in u:
        u = "https://" + u
    parts = urlsplit(u.lower())
    host = parts.netloc.rsplit("@", 1)[-1].split(":")[0]
    return host, parts.path


def normalize_linkedin_url(url):
    """Return 'linkedin.com/in/<slug>' or None if this is not a personal profile URL."""
    if not url or not isinstance(url, str):
        return None
    host, path = _host_and_path(url)
    if not host or not (host == "linkedin.com" or host.endswith(".linkedin.com")):
        return None
    path = path.rstrip("/")
    if not path.startswith("/in/") or len(path) <= len("/in/"):
        return None
    return "linkedin.com" + path


def normalize_domain(value):
    """Lower-case registrable host: no scheme, no www., no port, no path."""
    if not value or not isinstance(value, str):
        return None
    host, _ = _host_and_path(value)
    if not host:
        return None
    if host.startswith("www."):
        host = host[4:]
    return host or None


def normalize_company_name(name):
    """Lower-case, punctuation-free name with a leading 'the' and trailing legal suffixes removed."""
    if not name or not isinstance(name, str):
        return ""
    tokens = [t for t in _NON_ALNUM.split(name.lower()) if t]
    if tokens and tokens[0] == "the":
        tokens = tokens[1:]
    while tokens and tokens[-1] in _LEGAL_SUFFIXES:
        tokens.pop()
    return " ".join(tokens)


def alt_key(first_name, last_name, domain):
    """sha1 over normalised first|last|domain, or None when any part is missing."""
    d = normalize_domain(domain)
    if not first_name or not last_name or not d:
        return None
    raw = f"{first_name.strip().lower()}|{last_name.strip().lower()}|{d}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def contact_key(linkedin_url, first_name, last_name, domain):
    """'li:<normalised url>' when a profile URL exists, else 'alt:<sha1>', else None."""
    li = normalize_linkedin_url(linkedin_url)
    if li:
        return "li:" + li
    ak = alt_key(first_name, last_name, domain)
    return "alt:" + ak if ak else None
