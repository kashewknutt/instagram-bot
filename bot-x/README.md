# bot-x

Stub X (Twitter) observation bot. Implements the **agent-sdk** control API for orchestrator fleet discovery. Pipeline is not implemented yet.

## Setup

```powershell
pip install -e ../agent-sdk
pip install -e .
copy .env.example .env
python -m x_bot.api
```

Listens on `http://127.0.0.1:7413`.
