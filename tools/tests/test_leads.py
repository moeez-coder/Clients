import csv
import importlib.util
import json
import sqlite3
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("leads", Path(__file__).resolve().parents[1] / "leads.py")
leads = importlib.util.module_from_spec(spec)
spec.loader.exec_module(leads)


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.setattr(leads, "REPO", tmp_path)
    return tmp_path


def test_normalize_maps_aliases_canonicalises_ids_and_puts_linkedin_first(tmp_path):
    src = tmp_path / "in.csv"
    write_csv(src, [{"Name": "Jane Doe", "Title": "VP Sales", "Company": "Acme", "Website": "https://www.acme.com/about",
                     "LinkedIn": "http://linkedin.com/in/Jane-Doe/", "score": "7"}])
    leads.main(["normalize", str(src), str(tmp_path / "out.csv"), "--source", "blitz"])
    out = tmp_path / "out.csv"
    header = out.read_text(encoding="utf-8").splitlines()[0].split(",")
    row = read_csv(out)[0]
    assert header[0] == "linkedin_url" and header[-1] == "score"          # rule 3b first; extra columns kept, not dropped
    assert row["linkedin_url"] == "https://www.linkedin.com/in/jane-doe"
    assert row["company_domain"] == "acme.com"
    assert (row["first_name"], row["last_name"]) == ("Jane", "Doe")
    assert row["title_check"] == "pass" and row["first_source"] == "blitz"
    assert row["industry"] == "-"                                          # rule 4: explicit dash, not blank


def test_in_file_dedupe_uses_both_keys_and_unions_sources():
    raw = [
        {"linkedin_url": "https://www.linkedin.com/in/jane-doe", "first_name": "Jane", "last_name": "Doe",
         "company_domain": "acme.com", "all_sources": "blitz"},
        {"linkedin_url": "linkedin.com/in/JANE-DOE/", "first_name": "Jane", "last_name": "Doe", "all_sources": "clay"},
        {"linkedin_url": "", "first_name": "Jane", "last_name": "Doe", "company_domain": "www.acme.com",
         "all_sources": "discolike", "job_title": "Director of Sales"},
        {"linkedin_url": "https://www.linkedin.com/in/bob", "first_name": "Bob", "last_name": "Lee", "all_sources": "blitz"},
    ]
    rows, _, stats = leads.normalize_rows(raw)
    assert stats["rows_out"] == 2 and stats["collapsed_duplicates"] == 2
    jane = rows[0]
    assert jane["all_sources"] == "blitz,clay,discolike"
    assert jane["job_title"] == "Director of Sales"                        # blank filled from the duplicate


def test_overlap_catches_slug_variants_and_name_domain_matches_but_not_itself(repo):
    base = repo / "clients" / "acme" / "sourcing"
    write_csv(base / "seg-a" / "2026-09-01-leads.csv",
              [{"linkedin_url": "https://www.linkedin.com/in/jane-doe", "first_name": "Jane", "last_name": "Doe", "company_domain": "x.com"}])
    write_csv(base / "seg-b" / "2026-09-02-leads.csv",
              [{"linkedin_url": "-", "first_name": "Bob", "last_name": "Lee", "company_domain": "y.com"}])
    new = base / "seg-c" / "2026-09-30-leads.csv"
    write_csv(new, [
        {"linkedin_url": "http://linkedin.com/in/Jane-Doe/", "first_name": "Jane", "last_name": "Doe", "company_domain": "x.com"},
        {"linkedin_url": "https://www.linkedin.com/in/bob-lee-new-slug", "first_name": "Bob", "last_name": "Lee", "company_domain": "https://y.com"},
        {"linkedin_url": "https://www.linkedin.com/in/new-person", "first_name": "New", "last_name": "Person", "company_domain": "z.com"},
    ])
    total, report = leads.overlap_report(new, "acme")
    assert total == 3
    assert dict(report) == {"sourcing/seg-a/2026-09-01-leads.csv": 1, "sourcing/seg-b/2026-09-02-leads.csv": 1}


def test_next_free_never_overwrites_a_dated_snapshot(tmp_path):
    p = tmp_path / "2026-09-30-leads.csv"
    assert leads.next_free(p) == p
    p.write_text("x")
    assert leads.next_free(p).name == "2026-09-30-leads-2.csv"
    (tmp_path / "2026-09-30-leads-2.csv").write_text("x")
    assert leads.next_free(p).name == "2026-09-30-leads-3.csv"


def test_from_listbuild_lands_all_three_exports_with_query_record_and_stays_append_only(repo):
    out = repo / "clients" / "acme" / "listbuild" / "out" / "acme_us"
    person = {"first_name": "Jane", "last_name": "Doe", "full_name": "Jane Doe", "job_title": "CEO", "company_domain": "x.com",
              "linkedin_url": "https://www.linkedin.com/in/jane", "first_source": "blitz", "all_sources": "blitz,clay"}
    write_csv(out / "acme_us_20260930_part01.csv", [person])
    write_csv(out / "acme_us_20260930_part02.csv", [{**person, "first_name": "Al", "linkedin_url": "https://www.linkedin.com/in/al"}])
    write_csv(out / "acme_us_20260930_consulting_candidates_part01.csv", [{**person, "linkedin_url": "https://www.linkedin.com/in/c"}])
    (out / "cost_report.md").write_text("# Cost report\n| blitz | 2 |", encoding="utf-8")
    con = sqlite3.connect(out / "ledger.sqlite")
    con.execute("CREATE TABLE kv(k TEXT PRIMARY KEY, v TEXT)")
    con.execute("INSERT INTO kv VALUES ('consolidate', ?)", (json.dumps({"total": 3, "title_fail_dropped": 0}),))
    con.commit(); con.close()

    args = ["from-listbuild", "--client", "acme", "--icp", "acme_us", "--config-slug", "general-us", "--date", "2026-09-30"]
    leads.main(args)
    dest = repo / "clients" / "acme" / "sourcing" / "general-us"
    main_rows = read_csv(dest / "2026-09-30-leads.csv")
    assert len(main_rows) == 2 and list(main_rows[0])[0] == "linkedin_url"
    assert len(read_csv(dest / "2026-09-30-leads-candidates.csv")) == 1
    assert not (dest / "2026-09-30-leads-unverified.csv").exists()          # no unverified export -> no empty file
    q = (dest / "2026-09-30-leads.query.md").read_text(encoding="utf-8")
    assert "clients/acme/listbuild/config/acme_us.yaml" in q and '"total": 3' in q and "| blitz | 2 |" in q

    leads.main(args)                                                        # second landing the same day
    assert (dest / "2026-09-30-leads-2.csv").exists()
    assert len(read_csv(dest / "2026-09-30-leads.csv")) == 2                # original untouched
