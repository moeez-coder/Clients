from listbuild.seeds import load_seed_keys, detect_columns


def test_detect_columns_finds_linkedin_name_and_domain_headers():
    hdr = ["Company Name", "First Name", "Last Name", "LinkedIn Profile", "Company Domain", "Conn Req"]
    assert detect_columns(hdr) == {"linkedin": "LinkedIn Profile", "first": "First Name", "last": "Last Name", "domain": "Company Domain"}


def test_load_seed_keys_returns_linkedin_and_name_domain_keys(tmp_path):
    p = tmp_path / "prior.csv"
    p.write_text("First Name,Last Name,Company Domain,LinkedIn Profile\n"
                 "Jane,Doe,acme.com,https://www.linkedin.com/in/jane-doe-1/\n"
                 "Bob,Ray,,\n", encoding="utf-8")
    li, alt = load_seed_keys([p])
    assert li == {"linkedin.com/in/jane-doe-1"}
    assert len(alt) == 1
