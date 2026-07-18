#!/usr/bin/env python3
"""Bootstrap agent-sdk when cloned alone (install into a local venv)."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
SCRIPTS = PARENT / "scripts"
if (SCRIPTS / "bootstrap_lib.py").exists():
    sys.path.insert(0, str(SCRIPTS))
else:
    sys.path.insert(0, str(HERE / "scripts"))

from bootstrap_lib import bootstrap  # noqa: E402


if __name__ == "__main__":
    bootstrap(packages=["agent-sdk"], workspace=PARENT, interactive=False)
