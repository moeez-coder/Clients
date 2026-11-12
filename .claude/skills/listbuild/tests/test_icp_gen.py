from listbuild.icp_gen import build_icp, map_industries


def test_map_industries_expands_legacy_labels_and_discolike_buckets():
    m = map_industries(["Marketing Services", "Advertising Services"])
    assert m["clay"] == ["Marketing Services", "Advertising Services"]
    assert m["blitz"] == ["Marketing Services", "Advertising Services", "Marketing and Advertising"]
    assert m["discolike"] == ["ADVERTISING_AND_MARKETING"]
    assert m["catch_all"] == [] and m["unmapped"] == []


def test_catch_all_labels_are_split_out_as_candidates_not_core():
    m = map_industries(["Marketing Services", "Business Consulting and Services", "Strategic Management Services"])
    assert m["clay"] == ["Marketing Services", "Business Consulting and Services", "Strategic Management Services"]
    assert m["catch_all"] == ["Business Consulting and Services", "Strategic Management Services", "Management Consulting"]
    assert "Business Consulting and Services" not in m["core_blitz"]
    assert m["discolike"] == ["ADVERTISING_AND_MARKETING"]


def test_unknown_label_is_kept_for_clay_and_blitz_but_flagged():
    m = map_industries(["Staffing and Recruiting", "Underwater Basket Weaving"])
    assert m["discolike"] == ["HUMAN_RESOURCES"]
    assert "Underwater Basket Weaving" in m["blitz"] and m["unmapped"] == ["Underwater Basket Weaving"]


def test_build_icp_produces_a_complete_config(icp):
    cfg = build_icp(name="staffing_us_gb", industries=["Staffing and Recruiting"], countries=["US", "GB"],
                    revenue_min_usd=5_000_000, seniority="director_plus")
    assert cfg["name"] == "staffing_us_gb"
    assert cfg["company_hq_countries"] == ["US", "GB"] and cfg["person_countries"] == ["US", "GB"]
    assert cfg["clay_country_names"] == {"US": "United States", "GB": "United Kingdom"}
    assert cfg["clay_revenue_buckets"][0] == "5M-10M" and "1M-5M" not in cfg["clay_revenue_buckets"]
    assert cfg["seniority_map"] == icp["seniority_map"]
    assert cfg["industries"]["blitz"] == ["Staffing and Recruiting"]
    assert cfg["industries"]["discolike"] == ["HUMAN_RESOURCES"]
    assert cfg["fit"]["core_industries"] == ["Staffing and Recruiting", "HUMAN_RESOURCES"]
    assert cfg["fit"]["keyword_gated_industries"] == [] and cfg["fit"]["keywords"] == []


def test_build_icp_rejects_unknown_country_or_seniority():
    import pytest
    with pytest.raises(ValueError):
        build_icp(name="x", industries=["Marketing Services"], countries=["XX"], revenue_min_usd=0)
    with pytest.raises(ValueError):
        build_icp(name="x", industries=["Marketing Services"], countries=["US"], revenue_min_usd=0, seniority="everyone")
