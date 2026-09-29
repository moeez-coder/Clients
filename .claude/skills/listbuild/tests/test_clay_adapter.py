from listbuild.providers.clay import build_people_query, build_companies_query, parse_person, parse_company


def test_people_query_has_one_experiences_block_with_all_filters(icp):
    q = build_people_query(icp, {})
    assert q.count("experiences.any(") == 1
    assert 'location_country in ("United States", "United Kingdom", "Canada", "Australia", "New Zealand")' in q
    assert 'company.industry in ("Marketing Services", "Advertising Services", "Business Consulting and Services", "Strategic Management Services")' in q
    assert 'company.annual_revenue in ("1M-5M",' in q
    assert 'company.locations.any(is_headquarters = true and country_name in ("United States",' in q
    assert 'seniority in ("C-suite", "VP", "Director", "Head", "Founder", "Owner", "Partner", "Board Member")' in q
    assert "is_current = true" in q and q.startswith("select from people")


def test_people_query_shard_narrows_country_industry_seniority_revenue(icp):
    q = build_people_query(icp, {"location_country": "US", "industry": "Marketing Services", "seniority": "VP", "annual_revenue": "1M-5M"})
    assert 'location_country in ("United States")' in q
    assert 'company.industry in ("Marketing Services")' in q
    assert 'seniority in ("VP")' in q
    assert 'company.annual_revenue in ("1M-5M")' in q


def test_companies_query_uses_top_level_fields(icp):
    q = build_companies_query(icp, {"country": "GB"})
    assert q.startswith("select from companies")
    assert 'industry in ("Marketing Services",' in q
    assert 'annual_revenue in ("1M-5M",' in q
    assert 'locations.any(is_headquarters = true and country_name in ("United Kingdom"))' in q
    assert "experiences.any" not in q


def test_parse_person_maps_matched_experience_and_shard_country(icp):
    raw = {"clay_profile_id": 1, "name": "Jane Doe", "first_name": "Jane", "last_name": "Doe",
           "linkedin_url": "https://www.linkedin.com/in/jane", "location": {"name": "Austin, Texas, United States"},
           "matched_experiences": [{"company": "Acme Inc", "title": "VP Marketing", "start_date": "2020-01-01", "end_date": None}]}
    row = parse_person(raw, shard={"location_country": "US", "seniority": "VP"}, icp=icp)
    assert row["company_name"] == "Acme Inc" and row["job_title"] == "VP Marketing"
    assert row["person_country"] == "US" and row["seniority"] == "VP" and row["source"] == "clay"
    assert row["company_domain"] is None


def test_parse_person_infers_country_from_location_name_when_no_shard(icp):
    raw = {"name": "J D", "first_name": "J", "last_name": "D", "linkedin_url": "https://linkedin.com/in/jd",
           "location": {"name": "London, England, United Kingdom"}, "matched_experiences": []}
    row = parse_person(raw, shard={}, icp=icp)
    assert row["person_country"] == "GB" and row["company_name"] is None


def test_parse_company_normalises_domain_and_country(icp):
    raw = {"clay_company_id": 9, "name": "Acme Inc", "domain": "www.acme.com", "country": "United States",
           "industry": "Marketing Services", "linkedin_url": "https://www.linkedin.com/company/acme", "annual_revenue": "1M-5M"}
    c = parse_company(raw, icp=icp)
    assert c == {"domain": "acme.com", "name": "Acme Inc", "linkedin_url": "https://www.linkedin.com/company/acme",
                 "country": "US", "industry": "Marketing Services", "source": "clay"}
