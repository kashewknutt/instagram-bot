#!/usr/bin/env bash
# Run once when your GitHub token can create repos:
#   ./scripts/create-github-repo.sh
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=social-agent-platform
OWNER="${GITHUB_OWNER:-kashewknutt}"
if gh repo view "$OWNER/$NAME" >/dev/null 2>&1; then
  echo "Repo already exists: https://github.com/$OWNER/$NAME"
else
  gh repo create "$OWNER/$NAME" --public --source=. --remote=origin --description "Plug-and-play social observation agent platform. Bots are plugins."
fi
git push -u origin main
echo "Open: https://github.com/$OWNER/$NAME"
