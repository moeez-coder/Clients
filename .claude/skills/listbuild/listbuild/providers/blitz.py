"""Blitz adapter: POST /v2/search/people with cursor paging, sharded under the 50k cap.

Search results carry the person, their full experience list (with company domain and company
LinkedIn URL) but no company firmographics, so company country and seniority are taken from
the shard filters that produced the row.
"""
from ..http import Http

EMPLOYEE_RANGES = ["1-10", "11-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10001+"]
FOUNDED_RANGES = [[1800, 1990], [1991, 2000], [2001, 2005], [2006, 2010], [2011, 2013], [2014, 2016], [2017, 2019], [2020, 2030]]


def SHARD_DIMS(icp):
    """Single-valued dimensions, coarse to fine. Order matters: cheap, high-cardinality-of-skew first."""
    return [
        ("country", list(icp["company_hq_countries"])),
        ("job_level", list(icp["seniority_map"]["blitz"])),
        ("industry", list(icp["industries"]["blitz"])),
        ("person_country", list(icp["person_countries"])),
        ("employee_range", list(EMPLOYEE_RANGES)),
        ("founded_year", [list(r) for r in FOUNDED_RANGES]),
    ]


def build_people_body(icp, shard, page_size, cursor=None):
    shard = shard or {}
    company = {
        "industry": {"include": [shard["industry"]] if "industry" in shard else list(icp["industries"]["blitz"])},
        "hq": {"country_code": [shard["country"]] if "country" in shard else list(icp["company_hq_countries"])},
    }
    if icp.get("revenue_min_usd"):
        company["revenue"] = {"min": int(icp["revenue_min_usd"])}
    if "employee_range" in shard:
        company["employee_range"] = [shard["employee_range"]]
    if "founded_year" in shard:
        lo, hi = shard["founded_year"]
        company["founded_year"] = {"min": int(lo), "max": int(hi)}
    people = {
        "job_level": [shard["job_level"]] if "job_level" in shard else list(icp["seniority_map"]["blitz"]),
        "location": {"country_code": [shard["person_country"]] if "person_country" in shard else list(icp["person_countries"])},
    }
    body = {"company": company, "people": people, "max_results": int(page_size)}
    if cursor:
        body["cursor"] = cursor
    return body


def COMPANY_SHARD_DIMS(icp, industries):
    return [
        ("country", list(icp["company_hq_countries"])),
        ("industry", list(industries)),
        ("employee_range", list(EMPLOYEE_RANGES)),
        ("founded_year", [list(r) for r in FOUNDED_RANGES]),
    ]


def build_company_body(icp, shard, page_size, cursor=None, industries=None, keywords=None):
    """POST /v2/search/companies body: same company filters as the people search, optional keyword gate."""
    shard = shard or {}
    inds = [shard["industry"]] if "industry" in shard else list(industries or icp["industries"]["blitz"])
    company = {
        "industry": {"include": inds},
        "hq": {"country_code": [shard["country"]] if "country" in shard else list(icp["company_hq_countries"])},
    }
    if icp.get("revenue_min_usd"):
        company["revenue"] = {"min": int(icp["revenue_min_usd"])}
    if "employee_range" in shard:
        company["employee_range"] = [shard["employee_range"]]
    if "founded_year" in shard:
        lo, hi = shard["founded_year"]
        company["founded_year"] = {"min": int(lo), "max": int(hi)}
    if keywords:
        company["keywords"] = {"include": list(keywords)}
    body = {"company": company, "max_results": int(page_size)}
    if cursor:
        body["cursor"] = cursor
    return body


def parse_company(result):
    from ..identity import normalize_domain
    return {
        "domain": normalize_domain(result.get("domain") or result.get("website")),
        "name": result.get("name"),
        "linkedin_url": result.get("linkedin_url"),
        "country": (result.get("hq") or {}).get("country_code"),
        "industry": result.get("industry"),
        "size": result.get("size"),
        "source": "blitz_companies",
    }


def _current_experience(experiences):
    exps = experiences or []
    current = [e for e in exps if e.get("job_is_current")]
    if current:
        return current[0]
    return exps[0] if exps else {}


def parse_person(result, shard):
    shard = shard or {}
    exp = _current_experience(result.get("experiences"))
    loc = result.get("location") or {}
    return {
        "linkedin_url": result.get("linkedin_url"),
        "first_name": result.get("first_name"),
        "last_name": result.get("last_name"),
        "full_name": result.get("full_name"),
        "job_title": exp.get("job_title"),
        "seniority": shard.get("job_level"),
        "company_name": exp.get("company_name"),
        "company_domain": exp.get("company_domain"),
        "company_linkedin_url": exp.get("company_linkedin_url"),
        "industry": shard.get("industry"),
        "revenue_hint": None,
        "person_country": loc.get("country_code"),
        "company_country": shard.get("country"),
        "source": "blitz",
        "cost_usd": 0.0,
    }


class BlitzClient:
    def __init__(self, api_key, base_url="https://api.blitz-api.ai", rps=40):
        self.http = Http(base_url, {"x-api-key": api_key, "Content-Type": "application/json"}, rps=rps, retry_timeouts=True)
        self.records_used = 0

    def key_info(self):
        return self.http.request("GET", "/v2/account/key-info")

    def search_people(self, body):
        data = self.http.request("POST", "/v2/search/people", json=body)
        fu = data.get("fair_usage") or {}
        self.records_used += int(fu.get("records_used") or 0)
        return data

    def count(self, icp, shard):
        """total_results for a shard. Costs 1 record (max_results=1)."""
        data = self.search_people(build_people_body(icp, shard, page_size=1))
        return int(data.get("total_results") or 0)

    def search_companies(self, body):
        data = self.http.request("POST", "/v2/search/companies", json=body)
        fu = data.get("fair_usage") or {}
        self.records_used += int(fu.get("records_used") or 0)
        return data

    def count_companies(self, icp, shard, industries=None, keywords=None):
        data = self.search_companies(build_company_body(icp, shard, page_size=1, industries=industries, keywords=keywords))
        return int(data.get("total_results") or 0)
