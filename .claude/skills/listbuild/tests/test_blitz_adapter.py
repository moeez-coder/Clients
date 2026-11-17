from listbuild.providers.blitz import build_people_body, parse_person, SHARD_DIMS


def test_full_body_uses_all_icp_lists(icp):
    body = build_people_body(icp, {}, page_size=50)
    assert body["company"]["industry"]["include"] == icp["industries"]["blitz"]
    assert body["company"]["hq"]["country_code"] == ["US", "GB", "CA", "AU", "NZ"]
    assert body["company"]["revenue"] == {"min": 1000000}
    assert body["people"]["job_level"] == ["C-Team", "VP", "Director"]
    assert body["people"]["location"]["country_code"] == ["US", "GB", "CA", "AU", "NZ"]
    assert body["max_results"] == 50 and "cursor" not in body


def test_shard_filters_narrow_body_and_cursor_is_passed(icp):
    shard = {"country": "NZ", "job_level": "VP", "industry": "Marketing Services",
             "employee_range": "11-50", "founded_year": [2000, 2010]}
    body = build_people_body(icp, shard, page_size=25, cursor="abc")
    assert body["company"]["hq"]["country_code"] == ["NZ"]
    assert body["people"]["job_level"] == ["VP"]
    assert body["company"]["industry"]["include"] == ["Marketing Services"]
    assert body["company"]["employee_range"] == ["11-50"]
    assert body["company"]["founded_year"] == {"min": 2000, "max": 2010}
    assert body["cursor"] == "abc" and body["max_results"] == 25


def test_shard_dims_are_ordered_country_first(icp):
    names = [d[0] for d in SHARD_DIMS(icp)]
    assert names[:5] == ["country", "job_level", "industry", "person_country", "employee_range"]
    assert dict(SHARD_DIMS(icp))["country"] == ["US", "GB", "CA", "AU", "NZ"]


def test_parse_person_takes_current_experience(blitz_probe):
    row = parse_person(blitz_probe["results"][0], shard={"job_level": "C-Team", "country": "US"})
    assert row["linkedin_url"] == "https://www.linkedin.com/in/agustin-garcia-607ab03"
    assert row["company_domain"] == "garcorpinternational.com"
    assert row["company_name"] == "Garcorp International, Inc."
    assert row["job_title"] == "President/CEO"
    assert row["person_country"] == "US" and row["company_country"] == "US"
    assert row["seniority"] == "C-Team" and row["source"] == "blitz"
    assert row["company_linkedin_url"].startswith("https://www.linkedin.com/company/")


def test_parse_person_without_current_experience_still_returns_identity():
    row = parse_person({"first_name": "A", "last_name": "B", "full_name": "A B", "linkedin_url": "https://linkedin.com/in/ab",
                        "location": {"country_code": "GB"}, "experiences": []}, shard={})
    assert row["linkedin_url"] == "https://linkedin.com/in/ab" and row["company_domain"] is None
    assert row["person_country"] == "GB" and row["seniority"] is None


def test_company_body_targets_gated_industries_with_keywords(icp):
    from listbuild.providers.blitz import build_company_body, parse_company
    body = build_company_body(icp, {"country": "US", "employee_range": "11-50"}, page_size=50, cursor="c1",
                              industries=icp["fit"]["keyword_gated_industries"], keywords=icp["fit"]["keywords"])
    assert body["company"]["industry"]["include"] == icp["fit"]["keyword_gated_industries"]
    assert body["company"]["keywords"]["include"] == icp["fit"]["keywords"]
    assert body["company"]["hq"]["country_code"] == ["US"] and body["company"]["employee_range"] == ["11-50"]
    assert body["company"]["revenue"] == {"min": 1000000} and body["cursor"] == "c1" and "people" not in body
    body2 = build_company_body(icp, {"industry": "Marketing Services"}, page_size=50)
    assert body2["company"]["industry"]["include"] == ["Marketing Services"] and "keywords" not in body2["company"]
    c = parse_company({"linkedin_url": "https://www.linkedin.com/company/x", "name": "X Ltd", "industry": "Advertising Services",
                       "size": "11-50", "hq": {"country_code": "GB"}, "domain": "www.x.com", "website": None})
    assert c == {"domain": "x.com", "name": "X Ltd", "linkedin_url": "https://www.linkedin.com/company/x", "country": "GB",
                 "industry": "Advertising Services", "size": "11-50", "source": "blitz_companies"}
