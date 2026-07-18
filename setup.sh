#!/usr/bin/env bash
# macOS / Linux bootstrap
# Usage:
#   ./setup.sh                 # interactive
#   ./setup.sh --profile fleet
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pip install --user pyyaml >/dev/null 2>&1 || true
if [[ $# -eq 0 ]]; then
  exec python3 setup.py -i
else
  exec python3 setup.py "$@"
fi
