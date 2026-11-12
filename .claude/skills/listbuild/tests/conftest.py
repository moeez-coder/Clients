import json
from pathlib import Path

import pytest

PKG_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def icp():
    import yaml
    return yaml.safe_load((PKG_ROOT / "config" / "examples" / "marketing_companies_5geo_director_plus.yaml").read_text(encoding="utf-8"))


@pytest.fixture
def blitz_probe():
    return json.loads((PKG_ROOT / "tests" / "fixtures" / "blitz_all6_rev1m.json").read_text(encoding="utf-8"))
