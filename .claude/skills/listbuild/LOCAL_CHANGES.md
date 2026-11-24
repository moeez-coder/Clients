# Local changes vs the upstream listbuild skill

This folder is the listbuild skill supplied by the repo owner (added 2026-09-29), plus
the patches below. If a newer upstream version replaces this folder, re-apply any
patch here that upstream hasn't fixed, then re-run `python -m pytest -q tests`.

## 2026-09-30 — empty `.env` placeholders no longer erase environment keys

**Bug (verified 2026-09-29 in the Clients repo's cloud sessions):** `scripts/setup.py`
run without key arguments wrote `BLITZ_API_KEY=` / `CLAY_API_KEY=` / ... placeholders
into the workspace `.env`, and `config.load_keys()` loaded that file with
`override=True`. The empty values replaced keys the session already had in its
environment, so every provider failed with no obvious cause.

**Fix:**
- `listbuild/config.py` — `load_keys()` reads `.env` with `dotenv_values` instead of
  mutating `os.environ`; a **non-empty** `.env` value still wins (upstream behaviour
  kept), an **empty** one falls back to the environment variable.
- `scripts/setup.py` — `write_env()` no longer writes empty placeholders for keys it
  wasn't given; the "missing keys" message now also counts keys present in the
  environment.
- Tests: three new cases in `tests/test_workspace.py` (empty placeholders don't
  clobber, non-empty file still wins, setup writes no placeholders).
