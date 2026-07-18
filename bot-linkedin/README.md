# bot-linkedin

Stub LinkedIn observation bot. Implements the **agent-sdk** control API so it appears in the orchestrator fleet. Pipeline steps raise `NotImplementedError` until scraping is built.

## Setup

```powershell
pip install -e ../agent-sdk
pip install -e .
copy .env.example .env
python -m linkedin_bot.api
```

Listens on `http://127.0.0.1:7412`.
