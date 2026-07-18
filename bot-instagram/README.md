# bot-instagram

Observation-only Instagram trend bot. Implements the **agent-sdk** control API.

## Clone & setup

**Preferred:** clone the platform repo and run root setup:

```powershell
git clone https://github.com/kashewknutt/instagram-bot.git
cd instagram-bot
.\setup.ps1 -Profile instagram   # or fleet
```

**Open in Cursor:** `instagram-bot` (repo root) or this folder for CLI-only work.

### If you only cloned this package

```powershell
cd D:\GitHub\bot-instagram
python bootstrap.py
# auto-fetches ../agent-sdk
```

## Run

```powershell
# CLI
python main.py --offline run-once --sample
python main.py serve --port 7411

# or via Fleet Control
cd ..\orchestrator
python -m orchestrator_app.main
# http://127.0.0.1:7400
```

Set `MOONSHOT_API_KEY` in `.env` for live runs. First live ingest: log into Instagram in the opened browser (session saved under `data/browser-profile`).
