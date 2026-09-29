"""Launcher: run the pipeline from any folder. The folder you run it in is the workspace
(config/, .env, out/ live there); the code stays inside the skill folder.

    python "<skill folder>/scripts/listbuild.py" preview --icp config/x.yaml
"""
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR))
os.environ.setdefault("LISTBUILD_WORKSPACE", str(Path.cwd()))
os.environ.setdefault("PYTHONUTF8", "1")
os.environ["LISTBUILD_LAUNCHER"] = str(Path(__file__).resolve())

from listbuild.pipeline import main  # noqa: E402

if __name__ == "__main__":
    main()
