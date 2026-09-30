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


def test_empty_env_file_values_do_not_clobber_keys_already_in_the_environment(ws, monkeypatch):
    # setup.py run without key args writes empty placeholders; they must not erase keys the shell already has
    tmp, config = ws
    for name in ("BLITZ_API_KEY", "CLAY_API_KEY", "DISCOLIKE_API_KEY", "COLDIQ_API_KEY"):
        monkeypatch.setenv(name, f"real-{name}")
    (tmp / ".env").write_text("BLITZ_API_KEY=\nCLAY_API_KEY=\nDISCOLIKE_API_KEY=\nCOLDIQ_API_KEY=\n", encoding="utf-8")
    keys = config.load_keys()
    assert keys == {"blitz": "real-BLITZ_API_KEY", "clay": "real-CLAY_API_KEY",
                    "discolike": "real-DISCOLIKE_API_KEY", "coldiq": "real-COLDIQ_API_KEY"}


def test_a_non_empty_env_file_value_still_wins_over_the_environment(ws, monkeypatch):
    tmp, config = ws
    monkeypatch.setenv("BLITZ_API_KEY", "from-shell")
    (tmp / ".env").write_text("BLITZ_API_KEY=from-file\n", encoding="utf-8")
    assert config.load_keys()["blitz"] == "from-file"


def test_setup_write_env_does_not_add_empty_placeholders_for_keys_it_was_not_given(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("lb_setup", Path(__file__).resolve().parents[1] / "scripts" / "setup.py")
    setup = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(setup)
    setup.write_env(tmp_path, {"BLITZ_API_KEY": "k1", "CLAY_API_KEY": None, "DISCOLIKE_API_KEY": None, "COLDIQ_API_KEY": None})
    text = (tmp_path / ".env").read_text(encoding="utf-8")
    assert "BLITZ_API_KEY=k1" in text
    assert "CLAY_API_KEY=" not in text and "DISCOLIKE_API_KEY=" not in text
