"""One-time workspace setup for a teammate. Run from the project folder that should hold configs and outputs:

    python "<skill folder>/scripts/setup.py" --blitz KEY --clay KEY --discolike KEY

Installs requirements, writes .env (merging with an existing one), copies default provider settings and example
configs, runs the test suite, and checks each API key read-only. Idempotent.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR))


def write_env(ws, keys):
    env = ws / ".env"
    current = {}
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                current[k.strip()] = v.strip()
    for k, v in keys.items():
        if v:
            current[k] = v
    env.write_text("".join(f"{k}={v}\n" for k, v in current.items()), encoding="utf-8")
    return current


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=".")
    ap.add_argument("--blitz"); ap.add_argument("--clay"); ap.add_argument("--discolike"); ap.add_argument("--coldiq")
    ap.add_argument("--skip-install", action="store_true"); ap.add_argument("--skip-tests", action="store_true")
    a = ap.parse_args()
    ws = Path(a.workspace).resolve()
    ws.mkdir(parents=True, exist_ok=True)
    print(f"skill folder : {SKILL_DIR}\nworkspace    : {ws}")

    if not a.skip_install:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(SKILL_DIR / "requirements.txt")], check=True)
        print("dependencies : installed")

    keys = write_env(ws, {"BLITZ_API_KEY": a.blitz, "CLAY_API_KEY": a.clay, "DISCOLIKE_API_KEY": a.discolike, "COLDIQ_API_KEY": a.coldiq})
    missing = [k for k in ("BLITZ_API_KEY", "CLAY_API_KEY", "DISCOLIKE_API_KEY") if not (keys.get(k) or os.getenv(k))]
    print(f".env         : {ws / '.env'}" + (f"  (missing: {', '.join(missing)})" if missing else ""))

    (ws / "config" / "examples").mkdir(parents=True, exist_ok=True)
    if not (ws / "config" / "providers.yaml").exists():
        shutil.copy(SKILL_DIR / "config" / "providers.yaml", ws / "config" / "providers.yaml")
    for ex in (SKILL_DIR / "config" / "examples").glob("*.yaml"):
        shutil.copy(ex, ws / "config" / "examples" / ex.name)
    gi = ws / ".gitignore"
    wanted = [".env", "out/", "__pycache__/"]
    have = gi.read_text(encoding="utf-8").splitlines() if gi.exists() else []
    gi.write_text("\n".join(have + [w for w in wanted if w not in have]) + "\n", encoding="utf-8")
    print("config       : config/providers.yaml + config/examples/ ready; out/ and .env git-ignored")

    env = {**os.environ, "LISTBUILD_WORKSPACE": str(ws), "PYTHONUTF8": "1"}
    if not a.skip_tests:
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", str(SKILL_DIR / "tests")], env=env, capture_output=True, text=True)
        print("tests        :", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:])

    os.environ["LISTBUILD_WORKSPACE"] = str(ws)
    from listbuild.config import load_keys, load_providers
    from listbuild.providers.blitz import BlitzClient
    from listbuild.providers.clay import ClayClient
    from listbuild.providers.discolike import DiscoLikeClient
    k, prov = load_keys(), load_providers()
    if k["blitz"]:
        try:
            ki = BlitzClient(k["blitz"], prov["blitz"]["base_url"]).key_info()
            print(f"Blitz        : ok, plan {[p.get('name') for p in ki.get('active_plans', [])]}, {ki.get('records_remaining'):,} records left")
        except Exception as e:  # noqa: BLE001
            print(f"Blitz        : FAILED ({str(e)[:120]})")
    if k["clay"]:
        try:
            me = ClayClient(k["clay"], prov["clay"]["base_url"]).me()
            print(f"Clay         : ok, workspace {me.get('workspace', {}).get('name')} (quota shows in preview)")
        except Exception as e:  # noqa: BLE001
            print(f"Clay         : FAILED ({str(e)[:120]})")
    if k["discolike"]:
        try:
            u = DiscoLikeClient(k["discolike"], prov["discolike"]["base_url"]).usage()
            left = (u.get("total_available_spend") or 0) - (u.get("month_to_date_spend") or 0)
            state = f"WARNING overdrawn by ${-left:,.0f}; paid pulls need a top-up (run with --discolike-cap-usd 0)" if left < 0 else f"${left:,.0f} left to spend"
            print(f"DiscoLike    : ok, month-to-date ${u.get('month_to_date_spend')} of ${u.get('total_available_spend')} available -> {state}")
        except Exception as e:  # noqa: BLE001
            print(f"DiscoLike    : FAILED ({str(e)[:120]})")
    print(f'\nnext: python "{SKILL_DIR / "scripts" / "listbuild.py"}" new-icp --name <slug> --industries "<label>" --countries US --revenue-min 1000000')


if __name__ == "__main__":
    main()
