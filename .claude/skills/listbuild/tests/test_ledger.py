from listbuild.ledger import Ledger


def row(**kw):
    base = dict(linkedin_url="https://www.linkedin.com/in/jane/", first_name="Jane", last_name="Doe",
                full_name="Jane Doe", job_title="Director of Marketing", seniority="Director",
                company_name="Acme Inc", company_domain="acme.com", company_linkedin_url=None,
                industry="Marketing Services", revenue_hint=None, person_country="US", company_country="US",
                source="blitz", cost_usd=0.0)
    base.update(kw)
    return base


def test_duplicate_linkedin_merges_sources_into_one_row(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    assert lg.upsert_contact(row()) == "inserted"
    assert lg.upsert_contact(row(linkedin_url="linkedin.com/in/JANE", source="clay")) == "merged"
    assert lg.count_contacts() == 1
    c = lg.get_contact("li:linkedin.com/in/jane")
    assert c["first_source"] == "blitz" and c["all_sources"] == "blitz,clay"


def test_excluded_seed_blocks_insert_and_is_reported(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.add_excluded([{"linkedin_url": "https://linkedin.com/in/jane", "company_domain": "acme.com", "origin": "prior.csv"}])
    assert lg.upsert_contact(row()) == "excluded"
    assert lg.count_contacts() == 0


def test_known_domains_come_from_contacts_and_excluded_only(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(row())
    lg.add_excluded([{"linkedin_url": "https://linkedin.com/in/bob", "company_domain": "old.com", "origin": "prior.csv"}])
    lg.upsert_company({"domain": "lonely.com", "name": "Lonely", "country": "US", "source": "blitz"})
    assert lg.known_domains() == {"acme.com", "old.com"}
    assert lg.company_only_domains() == {"lonely.com"}


def test_shard_state_roundtrip_and_spend_log(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.save_shard("blitz", {"country": "NZ"}, expected_total=4930)
    lg.update_shard("blitz", {"country": "NZ"}, fetched=50, cursor="abc", status="running")
    s = lg.get_shard("blitz", {"country": "NZ"})
    assert s["fetched"] == 50 and s["cursor"] == "abc" and s["status"] == "running"
    assert [x["filters"] for x in lg.pending_shards("blitz")] == [{"country": "NZ"}]
    lg.record_spend("discolike", "contacts", units=20, cost_usd=0.07, note="sample")
    assert lg.total_spend("discolike") == 0.07


def test_two_people_with_same_name_and_company_but_different_linkedin_stay_separate(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    assert lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/john-smith-1")) == "inserted"
    assert lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/john-smith-2")) == "inserted"
    assert lg.count_contacts() == 2


def test_row_without_linkedin_merges_into_existing_by_name_and_domain(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(row())
    assert lg.upsert_contact(row(linkedin_url=None, source="clay")) == "merged"
    assert lg.count_contacts() == 1


def test_purge_excluded_removes_contacts_seeded_after_insert(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(row())
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/bob", first_name="Bob", last_name="Ray"))
    lg.upsert_contact(row(linkedin_url=None, first_name="Ann", last_name="Lee", company_domain="ann.com"))
    lg.add_excluded([{"linkedin_url": "https://www.linkedin.com/in/jane/", "company_domain": "acme.com", "origin": "later.csv"},
                     {"linkedin_url": None, "first_name": "Ann", "last_name": "Lee", "company_domain": "ann.com", "origin": "later.csv"}])
    assert lg.purge_excluded() == 2
    assert lg.count_contacts() == 1 and lg.get_contact("li:linkedin.com/in/bob") is not None


def test_purge_excluded_also_matches_name_and_domain_when_linkedin_slugs_differ(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/janedoe"))
    lg.add_excluded([{"linkedin_url": "https://linkedin.com/in/jane-doe-75a040139", "first_name": "Jane", "last_name": "Doe",
                      "company_domain": "acme.com", "origin": "prior.csv"}])
    assert lg.purge_excluded() == 1
    assert lg.count_contacts() == 0


def test_dedupe_similar_slugs_collapses_same_person_but_keeps_distinct_people(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/rafael-bolivar-1731ba38", first_name="Rafael", last_name="Bolivar", source="blitz"))
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/rafaelbolivar", first_name="Rafael", last_name="Bolivar", source="clay"))
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/chapman-eric", first_name="Eric", last_name="Chapman", source="blitz"))
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/ericechapman", first_name="Eric", last_name="Chapman", source="clay"))
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/jsmith-cx", first_name="John", last_name="Smith", source="blitz"))
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/johnsmith", first_name="John", last_name="Smith", source="clay"))
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/john-smith-headofgrowth", first_name="John", last_name="Smith", source="clay"))
    removed = lg.dedupe_similar_slugs()
    # name-derived slugs (name letters + short suffix) collapse; a slug with a substantive custom part stays distinct
    assert removed == 3 and lg.count_contacts() == 4
    kept = lg.get_contact("li:linkedin.com/in/rafael-bolivar-1731ba38")
    assert kept is not None and kept["all_sources"] == "blitz,clay"
    assert lg.get_contact("li:linkedin.com/in/john-smith-headofgrowth") is not None


def test_refresh_alt_keys_after_domain_backfill_lets_purge_match(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/janedoe", company_domain=None, source="clay"))
    lg.conn.execute("UPDATE contacts SET company_domain = 'acme.com'")
    lg.conn.commit()
    lg.add_excluded([{"linkedin_url": "https://linkedin.com/in/jane-doe-75a040139", "first_name": "Jane", "last_name": "Doe",
                      "company_domain": "acme.com", "origin": "prior.csv"}])
    assert lg.purge_excluded() == 0          # stale key: no match yet
    assert lg.refresh_alt_keys() == 1
    assert lg.purge_excluded() == 1


def test_excluded_keeps_every_name_variant_for_the_same_linkedin_url(tmp_path):
    lg = Ledger(tmp_path / "l.sqlite")
    lg.add_excluded([{"linkedin_url": "https://linkedin.com/in/jaime-frantz-9ab9a88", "first_name": "Jaime", "last_name": "Frantz", "company_domain": "x.com"},
                     {"linkedin_url": "https://linkedin.com/in/jaime-frantz-9ab9a88", "first_name": "Jaime", "last_name": "Cramer", "company_domain": "x.com"}])
    lg.upsert_contact(row(linkedin_url="https://linkedin.com/in/jaime-cramer-9ab9a88", first_name="Jaime", last_name="Cramer", company_domain="x.com"))
    assert lg.purge_excluded() == 1
