"""Clay public API adapter: query-mode search, 500 rows per run, stateful iterator.

People rows return the company NAME only (no domain); domains are joined locally against the
companies table. Company rows do return domain.
"""
from ..http import Http, HttpError


def _lit(values):
    return ", ".join('"' + str(v).replace('"', '\\"') + '"' for v in values)


def _country_names(icp, codes):
    return [icp["clay_country_names"][c] for c in codes]


def CLAY_PEOPLE_DIMS(icp):
    return [
        ("location_country", list(icp["person_countries"])),
        ("industry", list(icp["industries"]["clay"])),
        ("seniority", list(icp["seniority_map"]["clay"])),
        ("annual_revenue", list(icp["clay_revenue_buckets"])),
    ]


def CLAY_COMPANY_DIMS(icp):
    return [
        ("country", list(icp["company_hq_countries"])),
        ("industry", list(icp["industries"]["clay"])),
        ("annual_revenue", list(icp["clay_revenue_buckets"])),
    ]


def build_people_query(icp, shard):
    shard = shard or {}
    person_countries = [shard["location_country"]] if "location_country" in shard else list(icp["person_countries"])
    industries = [shard["industry"]] if "industry" in shard else list(icp["industries"]["clay"])
    seniorities = [shard["seniority"]] if "seniority" in shard else list(icp["seniority_map"]["clay"])
    revenues = [shard["annual_revenue"]] if "annual_revenue" in shard else list(icp["clay_revenue_buckets"])
    hq = _country_names(icp, icp["company_hq_countries"])
    return (
        "select from people\n"
        f"where location_country in ({_lit(_country_names(icp, person_countries))})\n"
        "  and experiences.any(is_current = true"
        f" and seniority in ({_lit(seniorities)})"
        f" and company.industry in ({_lit(industries)})"
        f" and company.annual_revenue in ({_lit(revenues)})"
        f" and company.locations.any(is_headquarters = true and country_name in ({_lit(hq)})))"
    )


def build_companies_query(icp, shard):
    shard = shard or {}
    countries = [shard["country"]] if "country" in shard else list(icp["company_hq_countries"])
    industries = [shard["industry"]] if "industry" in shard else list(icp["industries"]["clay"])
    revenues = [shard["annual_revenue"]] if "annual_revenue" in shard else list(icp["clay_revenue_buckets"])
    return (
        "select from companies\n"
        f"where industry in ({_lit(industries)})\n"
        f"  and annual_revenue in ({_lit(revenues)})\n"
        f"  and locations.any(is_headquarters = true and country_name in ({_lit(_country_names(icp, countries))}))"
    )


_UK_PARTS = {"england", "scotland", "wales", "northern ireland"}


def _infer_country(icp, location_name):
    if not location_name:
        return None
    parts = [p.strip() for p in location_name.split(",") if p.strip()]
    if not parts:
        return None
    tail = parts[-1]
    for code, name in icp["clay_country_names"].items():
        if tail.lower() == name.lower():
            return code
    if tail.lower() in _UK_PARTS:
        return "GB"
    return None


def parse_person(raw, shard, icp):
    shard = shard or {}
    exps = raw.get("matched_experiences") or []
    exp = exps[0] if exps else {}
    loc = raw.get("location") or {}
    first, last = raw.get("first_name"), raw.get("last_name")
    if not (first or last) and raw.get("name"):
        bits = raw["name"].split(" ", 1)
        first, last = bits[0], (bits[1] if len(bits) > 1 else None)
    return {
        "linkedin_url": raw.get("linkedin_url"),
        "first_name": first,
        "last_name": last,
        "full_name": raw.get("name") or " ".join(x for x in (first, last) if x),
        "job_title": exp.get("title"),
        "seniority": shard.get("seniority"),
        "company_name": exp.get("company"),
        "company_domain": None,
        "company_linkedin_url": None,
        "industry": shard.get("industry"),
        "revenue_hint": shard.get("annual_revenue"),
        "person_country": shard.get("location_country") or _infer_country(icp, loc.get("name")),
        "company_country": None,
        "source": "clay",
        "cost_usd": 0.0,
        "clay_profile_id": raw.get("clay_profile_id"),
    }


def parse_company(raw, icp):
    from ..identity import normalize_domain
    country = raw.get("country")
    code = None
    for c, name in icp["clay_country_names"].items():
        if country and country.lower() == name.lower():
            code = c
    return {
        "domain": normalize_domain(raw.get("domain")),
        "name": raw.get("name"),
        "linkedin_url": raw.get("linkedin_url"),
        "country": code or country,
        "industry": raw.get("industry"),
        "source": "clay",
    }


class QuotaExceeded(Exception):
    pass


class ClayClient:
    def __init__(self, api_key, base_url="https://api.clay.com/public/v0", rps=None):
        self.http = Http(base_url, {"clay-api-key": api_key, "Content-Type": "application/json"}, rps=rps,
                         retry_timeouts=False, max_retries=6)
        self.last_quota = None

    def me(self):
        return self.http.request("GET", "/me")

    def create_search(self, query):
        data = self.http.request("POST", "/search/query-mode", json={"query": query})
        return data["search_id"], data.get("source_type")

    def run(self, search_id, limit=500):
        try:
            data = self.http.request("POST", f"/search/query-mode/{search_id}/run", json={"limit": int(limit)})
        except HttpError as e:
            if e.status == 402:
                raise QuotaExceeded(str(e))
            raise
        if data.get("period_quota"):
            self.last_quota = data["period_quota"]
        return data
