#!/usr/bin/env python3
"""Platform setup entrypoint.

Clone THIS repo, then run:

  python setup.py
  # or
  python setup.py --profile fleet
  python setup.py --profile instagram

It installs the packages you need (and can fetch missing siblings from GitHub).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from bootstrap_lib import main  # noqa: E402

if __name__ == "__main__":
    main()
