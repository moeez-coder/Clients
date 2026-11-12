import pytest
from listbuild.providers.discolike import build_contact_params, parse_contact, revenue_qualifies


def test_params_are_repeatable_pairs_with_exclusion_and_employee_floor(icp):
    p = build_contact_params(icp, exclusion_id="abc", employee_floor=11)
    assert p.count(("filter_industry", "ADVERTISING_AND_MARKETING")) == 1
    assert [v for k, v in p if k == "filter_country"] == ["US", "GB", "CA", "AU", "NZ"]
    assert [v for k, v in p if k == "person_country"] == ["US", "GB", "CA", "AU", "NZ"]
    assert [v for k, v in p if k == "seniority"] == ["executive", "vp", "director"]
    assert ("has_linkedin", "true") in p and ("employee_range", "11,") in p and ("exclusion_query_id", "abc") in p


def test_params_without_optional_parts_and_with_extra_industries(icp):
    p = build_contact_params(icp, exclusion_id=None, employee_floor=None, include_optional_industries=True)
    assert ("filter_industry", "BUSINESS_PRODUCTS_AND_SERVICES") in p
    assert not any(k in ("exclusion_query_id", "employee_range") for k, _ in p)


def test_parse_contact_extracts_linkedin_from_social_urls_list():
    rec = {"persona_id": 5, "domain": "acme.com", "name": "Jane Doe", "title": "VP Marketing", "seniority": "vp",
           "social_urls": ["https://twitter.com/x", "https://www.linkedin.com/in/jane"], "country": "US",
           "industry": ["ADVERTISING_AND_MARKETING"], "revenue_range": "1-10M", "employees": "11-50"}
    row = parse_contact(rec)
    assert row["linkedin_url"] == "https://www.linkedin.com/in/jane"
    assert row["first_name"] == "Jane" and row["last_name"] == "Doe"
    assert row["company_domain"] == "acme.com" and row["seniority"] == "vp" and row["revenue_hint"] == "1-10M"
    assert row["person_country"] == "US" and row["source"] == "discolike" and row["persona_id"] == 5


def test_parse_contact_handles_dict_social_urls_and_missing_linkedin():
    rec = {"persona_id": 6, "domain": "b.com", "name": "Bob", "title": "CEO",
           "social_urls": [{"type": "linkedin", "url": "https://linkedin.com/in/bob"}]}
    assert parse_contact(rec)["linkedin_url"] == "https://linkedin.com/in/bob"
    assert parse_contact({"persona_id": 7, "domain": "c.com", "name": "C", "social_urls": None})["linkedin_url"] is None


@pytest.mark.parametrize("rng,expected", [
    ("1-10M", True), ("10-100M", True), ("100M-1B", True), (">1B", True), ("<1M", False),
    ("1000000,10000000", True), ("500000,900000", False), ("1000000+", True), (None, None), ("", None), ("unknown", None),
])
def test_revenue_qualifies_against_one_million_floor(rng, expected):
    assert revenue_qualifies(rng, 1_000_000) is expected
