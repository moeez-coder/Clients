from listbuild.icp_fit import classify_company_fit
from listbuild.ledger import Ledger


def test_core_industry_is_fit(icp):
    assert classify_company_fit(icp, "Advertising Services", None) == ("fit", "core industry")
    assert classify_company_fit(icp, "ADVERTISING_AND_MARKETING,SAAS", None) == ("fit", "core industry")


def test_gated_industry_needs_keyword_flag(icp):
    assert classify_company_fit(icp, "Business Consulting and Services", True) == ("candidate", "consulting with marketing keywords")
    assert classify_company_fit(icp, "Business Consulting and Services", False) == ("unfit", "consulting without marketing keywords")
    assert classify_company_fit(icp, "Strategic Management Services", None) == ("unknown", "consulting, keywords not checked")


def test_unknown_or_foreign_industry(icp):
    assert classify_company_fit(icp, None, None) == ("unknown", "industry unknown")
    assert classify_company_fit(icp, "Oil and Gas", None) == ("unfit", "industry outside ICP")


def _row(**kw):
    base = dict(linkedin_url="https://linkedin.com/in/x", first_name="A", last_name="B", full_name="A B", job_title="Director",
                seniority="Director", company_name="X", company_domain="x.com", company_linkedin_url="https://www.linkedin.com/company/x",
                industry=None, revenue_hint=None, person_country="US", company_country="US", source="blitz", cost_usd=0.0)
    base.update(kw)
    return base


def test_apply_fit_uses_company_table_then_contact_industry(tmp_path, icp):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/a", company_domain="agency.com"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/b", company_domain="energy.com"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/c", company_domain="brandco.com"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/d", company_domain=None, company_linkedin_url=None, industry="Marketing Services", source="clay"))
    lg.upsert_contact(_row(linkedin_url="https://linkedin.com/in/e", company_domain=None, company_linkedin_url=None, industry="Business Consulting and Services", source="clay"))
    lg.upsert_company({"domain": "agency.com", "name": "Agency", "industry": "Advertising Services", "source": "blitz"})
    lg.upsert_company({"domain": "energy.com", "name": "Energy", "industry": "Business Consulting and Services", "source": "blitz"})
    lg.upsert_company({"domain": "brandco.com", "name": "BrandCo", "industry": "Business Consulting and Services", "source": "blitz"})
    lg.set_keyword_fit(["brandco.com"], checked_domains=["brandco.com", "energy.com"])
    counts = lg.apply_fit(icp)
    assert counts == {"fit": 2, "candidate": 1, "unfit": 1, "unknown": 1}
    assert lg.get_contact("li:linkedin.com/in/b")["icp_fit"] == "unfit"
    assert lg.get_contact("li:linkedin.com/in/c")["icp_fit"] == "candidate"
    assert lg.get_contact("li:linkedin.com/in/d")["icp_fit"] == "fit"
    assert lg.get_contact("li:linkedin.com/in/e")["icp_fit"] == "unknown"
    # the authoritative company-table industry is written back onto the contact
    assert lg.get_contact("li:linkedin.com/in/a")["industry"] == "Advertising Services"
