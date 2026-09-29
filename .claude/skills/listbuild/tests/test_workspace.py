import os
from pathlib import Path

import pytest


@pytest.fixture
def ws(tmp_path, monkeypatch):
    monkeypatch.setenv("LISTBUILD_WORKSPACE", str(tmp_path))
    import importlib
    from listbuild import config
    importlib.reload(config)
    return tmp_path, config


def test_workspace_comes_from_env_and_outputs_live_there(ws):
    tmp, config = ws
    assert config.WORKSPACE == tmp
    assert config.workspace_out() == tmp / "out"
    assert config.PKG_ROOT != tmp and (config.PKG_ROOT / "listbuild").is_dir()


def test_providers_fall_back_to_the_packaged_default_when_workspace_has_none(ws):
    tmp, config = ws
    prov = config.load_providers()
    assert prov["blitz"]["page_size"] == 50
    (tmp / "config").mkdir()
    (tmp / "config" / "providers.yaml").write_text("blitz:\n  page_size: 7\n", encoding="utf-8")
    assert config.load_providers()["blitz"]["page_size"] == 7


def test_icp_path_resolves_relative_to_workspace_and_keys_come_from_workspace_env(ws):
    tmp, config = ws
    (tmp / "config").mkdir()
    (tmp / "config" / "x.yaml").write_text("name: x\n", encoding="utf-8")
    assert config.load_icp("config/x.yaml")["name"] == "x"
    (tmp / ".env").write_text("BLITZ_API_KEY=abc\n", encoding="utf-8")
    os.environ.pop("BLITZ_API_KEY", None)
    assert config.load_keys()["blitz"] == "abc"
