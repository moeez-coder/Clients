import pytest
from listbuild.seniority import classify_title


@pytest.mark.parametrize("title", [
    "Director of Marketing", "Account Director", "Managing Director", "VP Sales", "SVP, Growth",
    "Vice President of Operations", "Head of Strategy", "Chief Executive Officer", "CEO & Founder",
    "CMO", "Co-Founder", "Owner", "Partner", "Managing Partner", "Principal", "President",
    "Executive Director", "Director, Account Management", "Directrice générale", "Président",
])
def test_director_plus_titles_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", [
    "Marketing Manager", "Account Executive", "Senior Consultant", "Account Coordinator",
    "Assistant to the Director", "Executive Assistant to CEO", "Assistant Director of Sales",
    "Marketing Specialist", "Analyst", "Intern",
])
def test_sub_director_titles_fail(title):
    assert classify_title(title) == "fail"


def test_missing_title_is_unknown_not_dropped():
    assert classify_title(None) == "unknown"
    assert classify_title("   ") == "unknown"


@pytest.mark.parametrize("title", ["Chair", "Board Chair", "Vice Chair", "Executive Chair", "Partner & Senior Consultant",
                                   "Diretor administrativo", "Directeur général", "Associate Director"])
def test_additional_director_plus_variants_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", ["Product Owner", "Business Success Partner - Business Consultant", "Partner Manager",
                                   "Mr. Moritz", "Committee Member"])
def test_additional_sub_director_variants_fail(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", ["Member Board of Directors", "V.P. Manufacturing", "Managing Member", "Entrepreneur",
                                   "Executive Search Consultant - Partner", "Sr. Director of Planning"])
def test_board_and_abbreviated_variants_pass(title):
    assert classify_title(title) == "pass"


@pytest.mark.parametrize("title", ["Advisory Board", "Member, Strategic Advisory Board", "Executive Business Partner", "Managing Editor"])
def test_advisory_and_compound_variants_fail(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", ["Advisory Board Member", "Member of the Advisory Board", "Board Advisor", "Advisor to the Board"])
def test_advisory_board_roles_fail(title):
    assert classify_title(title) == "fail"


@pytest.mark.parametrize("title", ["Director, Advisory Services", "Partner - Deal Advisory", "Board Member"])
def test_advisory_practice_leaders_still_pass(title):
    assert classify_title(title) == "pass"
