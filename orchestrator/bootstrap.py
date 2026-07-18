#!/usr/bin/env python3
"""Bootstrap when this package is cloned alone.

Fetches agent-sdk + selected bots as siblings, then installs them.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent

# Prefer platform scripts if present (monorepo); else vendor path
SCRIPTS = PARENT / "scripts"
if (SCRIPTS / "bootstrap_lib.py").exists():
    sys.path.insert(0, str(SCRIPTS))
else:
    sys.path.insert(0, str(HERE / "scripts"))

from bootstrap_lib import bootstrap  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap orchestrator dependencies")
    parser.add_argument(
        "--with",
        dest="bots",
        nargs="*",
        default=["instagram"],
        help="Bots to include (instagram linkedin x). Default: instagram",
    )
    parser.add_argument("--all-bots", action="store_true", help="Include instagram + linkedin + x")
    parser.add_argument("--no-install", action="store_true")
    args = parser.parse_args()

    bots = ["instagram", "linkedin", "x"] if args.all_bots else list(args.bots or ["instagram"])
    packages = ["agent-sdk", "orchestrator"] + [f"bot-{b}" for b in bots]
    bootstrap(
        packages=packages,
        workspace=PARENT if (PARENT / "platform.manifest.yaml").exists() else PARENT,
        install=not args.no_install,
        interactive=False,
    )


if __name__ == "__main__":
    main()
