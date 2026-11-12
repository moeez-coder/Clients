"""DiscoLike adapter: free counts, exclusion lists, and the flat GET /contacts endpoint.

Never use POST /contacts/discover for bulk pulls: it adds per-company firmographic charges and a
query fee on top of the per-contact price. GET /contacts bills only contacts_billed x rate.
"""
import re

from ..http import Http

_UNIT = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}


def build_contact_params(icp, exclusion_id=None, employee_floor=None, include_optional_industries=False, extra=None):
    """Repeatable query params as a list of (key, value) pairs."""
    p = []
    inds = list(icp["industries"]["discolike"])
    if include_optional_industries:
        inds += list(icp["industries"].get("discolike_optional") or [])
    p += [("filter_industry", i) for i in inds]
    p += [("seniority", s) for s in icp["seniority_map"]["discolike"]]
    p += [("filter_country", c) for c in icp["company_hq_countries"]]
    p += [("person_country", c) for c in icp["person_countries"]]
    p.append(("has_linkedin", "true"))
    if employee_floor:
        p.append(("employee_range", f"{int(employee_floor)},"))
    if exclusion_id:
        p.append(("exclusion_query_id", exclusion_id))
    if extra:
        p += list(extra)
    return p


def _linkedin_from_social(social_urls):
    for s in social_urls or []:
        url = s.get("url") if isinstance(s, dict) else s
        if url and "linkedin.com/in/" in url.lower():
            return url
    return None


def parse_contact(rec):
    name = (rec.get("name") or "").strip()
    first, last = (name.split(" ", 1) + [None])[:2] if name else (None, None)
    inds = rec.get("industry")
    return {
        "linkedin_url": _linkedin_from_social(rec.get("social_urls")),
        "first_name": first,
        "last_name": last,
        "full_name": name or None,
        "job_title": rec.get("title"),
        "seniority": rec.get("seniority"),
        "company_name": rec.get("company_name") or rec.get("company") or None,
        "company_domain": rec.get("domain"),
        "company_linkedin_url": None,
        "industry": ",".join(inds) if isinstance(inds, list) else inds,
        "revenue_hint": rec.get("revenue_range"),
        "person_country": rec.get("country"),
        "company_country": None,
        "source": "discolike",
        "cost_usd": 0.0,
        "persona_id": rec.get("persona_id"),
        "employees": rec.get("employees"),
    }


def _num(token):
    token = token.strip().upper().replace("$", "").replace(",", "")
    m = re.fullmatch(r"(\d+(?:\.\d+)?)([KMBT])?", token)
    if not m:
        return None
    return float(m.group(1)) * _UNIT.get(m.group(2) or "", 1)


def revenue_qualifies(rng, min_usd):
    """True if the whole range is >= min_usd, False if the whole range is below it, None if unknown/straddling."""
    if not rng or not isinstance(rng, str) or not rng.strip():
        return None
    s = rng.strip().upper().replace(" ", "")
    if s.startswith("<"):
        hi = _num(s[1:])
        return None if hi is None else (False if hi <= min_usd else None)
    if s.startswith(">") or s.endswith("+"):
        lo = _num(s.strip(">+"))
        return None if lo is None else (True if lo >= min_usd else None)
    for sep in (",", "-"):
        if sep in s:
            a, b = s.split(sep, 1)
            hi = _num(b)
            lo = _num(a)
            if lo is not None and hi is not None and a[-1].isdigit() and b and b[-1] in _UNIT:
                lo = lo * _UNIT[b[-1]]  # "1-10M": the unit belongs to both bounds
            if lo is None or hi is None:
                return None
            if lo >= min_usd:
                return True
            if hi <= min_usd:
                return False
            return None
    v = _num(s)
    return None if v is None else v >= min_usd


class DiscoLikeClient:
    def __init__(self, api_key, base_url="https://api.discolike.com/v1", rps=0.4):
        # unbilled contact operations are capped at 30 requests/minute on every plan
        self.http = Http(base_url, {"x-discolike-key": api_key}, rps=rps, retry_timeouts=False, max_retries=4)

    def usage(self):
        return self.http.request("GET", "/usage")

    def count(self, params):
        return int(self.http.request("GET", "/contacts/count", params=params).get("count") or 0)

    def create_exclusion_list(self, name, domains=None, persona_ids=None, tags=None):
        body = {"query_name": name}
        if domains:
            body["domains"] = sorted(set(domains))
        if persona_ids:
            body["persona_ids"] = sorted(set(int(p) for p in persona_ids))
        if tags:
            body["tags"] = tags
        return self.http.request("POST", "/queries/exclusion-list", json=body)

    def saved_queries(self):
        return self.http.request("GET", "/queries/saved")

    def contacts(self, params, max_records, offset=0):
        p = list(params) + [("max_records", str(int(max_records))), ("offset", str(int(offset)))]
        data = self.http.request("GET", "/contacts", params=p)
        if isinstance(data, dict):
            for k in ("contacts", "results", "data"):
                if isinstance(data.get(k), list):
                    return data[k], data
            return [], data
        return data, {}

    @staticmethod
    def billing_since(usage, since_iso):
        """Sum billing_events after a timestamp: (cost_usd, contacts_billed, companies_billed)."""
        cost = contacts = companies = 0
        for ev in usage.get("billing_events") or []:
            if ev.get("created_at", "") > since_iso:
                cost += float(ev.get("cost_usd") or 0)
                contacts += int(ev.get("contacts_billed") or 0)
                companies += int(ev.get("companies_billed") or 0)
        return round(cost, 4), contacts, companies
