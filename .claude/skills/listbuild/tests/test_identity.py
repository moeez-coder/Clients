from listbuild.identity import (
    normalize_linkedin_url, normalize_domain, normalize_company_name, contact_key,
)


def test_linkedin_url_strips_protocol_www_query_and_trailing_slash():
    assert normalize_linkedin_url("https://www.linkedin.com/in/Jane-Doe-123/?utm=x") == "linkedin.com/in/jane-doe-123"


def test_linkedin_country_subdomain_collapses_to_bare_domain():
    assert normalize_linkedin_url("http://uk.linkedin.com/in/jane") == "linkedin.com/in/jane"


def test_linkedin_url_rejects_non_profile_urls():
    assert normalize_linkedin_url("https://www.linkedin.com/company/acme") is None
    assert normalize_linkedin_url("") is None
    assert normalize_linkedin_url(None) is None


def test_domain_normalisation_strips_scheme_www_path_and_port():
    assert normalize_domain("https://www.Acme-Agency.com:443/about") == "acme-agency.com"
    assert normalize_domain(None) is None
    assert normalize_domain("   ") is None


def test_company_name_drops_legal_suffixes_and_punctuation():
    assert normalize_company_name("Acme Marketing, Inc.") == "acme marketing"
    assert normalize_company_name("The Brand Group Ltd") == "brand group"
    assert normalize_company_name("Blue Sky Consulting Pty Ltd") == "blue sky consulting"


def test_contact_key_prefers_linkedin_then_falls_back_to_name_domain_hash():
    assert contact_key("https://linkedin.com/in/jane/", "Jane", "Doe", "acme.com") == "li:linkedin.com/in/jane"
    k = contact_key(None, "Jane", "Doe", "www.acme.com")
    assert k.startswith("alt:") and len(k) == 4 + 40
    assert k == contact_key(None, "jane ", "DOE", "acme.com")
    assert contact_key(None, None, "Doe", "acme.com") is None
