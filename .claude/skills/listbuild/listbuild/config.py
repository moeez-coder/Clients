"""Paths and settings.

PKG_ROOT   = the folder that contains the `listbuild` package (the skill folder when installed as a skill).
WORKSPACE  = the teammate's project folder: config/<icp>.yaml, .env, out/<icp>/ all live here.
             Set with LISTBUILD_WORKSPACE, else the current working directory.
"""
import os
from pathlib import Path

import yaml
from dotenv import dotenv_values

PKG_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(os.environ.get("LISTBUILD_WORKSPACE") or Path.cwd()).resolve()


def workspace_out():
    return WORKSPACE / "out"


def resolve(path):
    p = Path(path)
    return p if p.is_absolute() else WORKSPACE / p


def load_icp(path=None):
    p = resolve(path) if path else WORKSPACE / "config" / "icp.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8"))


def load_providers(path=None):
    candidates = [resolve(path)] if path else [WORKSPACE / "config" / "providers.yaml", PKG_ROOT / "config" / "providers.yaml"]
    for p in candidates:
        if p.exists():
            return yaml.safe_load(p.read_text(encoding="utf-8"))
    raise FileNotFoundError("providers.yaml not found in workspace or package")


_KEY_VARS = {"blitz": "BLITZ_API_KEY", "clay": "CLAY_API_KEY", "discolike": "DISCOLIKE_API_KEY", "coldiq": "COLDIQ_API_KEY"}


def load_keys():
    """A non-empty value in the workspace .env wins; an empty placeholder falls back to the environment."""
    env = WORKSPACE / ".env"
    file_vals = dotenv_values(env) if env.exists() else {}
    return {name: (file_vals.get(var) or os.getenv(var, "")) for name, var in _KEY_VARS.items()}
