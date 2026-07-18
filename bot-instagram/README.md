# bot-instagram

Observation-only Instagram trend bot. Ingests Explore/hashtag signals with browser-use, filters and synthesizes with Kimi (Moonshot AI).

Implements the shared **agent-sdk** control API so the orchestrator (or any HTTP client) can start / pause / stop / steer it.

## Prerequisites

- Python 3.11+
- Sibling `agent-sdk` package (`../agent-sdk`)
- Kimi API key from [platform.kimi.ai](https://platform.kimi.ai)

## Setup

```powershell
# from D:\GitHub (or this monorepo root)
cd agent-sdk
python -m venv ..\bot-instagram\.venv
..\bot-instagram\.venv\Scripts\Activate.ps1
pip install -e .
cd ..\bot-instagram
pip install -e .
playwright install chromium
copy .env.example .env
# set MOONSHOT_API_KEY in .env
```

## CLI

```powershell
python main.py smoke-test
python main.py --offline run-once --sample
python main.py ingest
python main.py run-once
python main.py daemon
```

## Control API

```powershell
python -m ig_agent.api
# listens on http://127.0.0.1:7411
```

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/status` | State, step, usage, artifacts |
| POST | `/run` | `{ "mode": "once" \| "daemon", "sample": true }` |
| POST | `/pause` `/resume` `/stop` | Lifecycle |
| GET/PUT | `/direction` | Hashtags, pillars, goals |

Direction is stored in `agency_context.json`.

## Instagram login

```powershell
python main.py ingest
```

Log in once in the opened Chromium window. Session persists under `data/browser-profile`.
