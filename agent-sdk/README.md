# agent-sdk

Shared runtime and HTTP control contract for social observation bots.

## Clone & setup

Usually installed automatically when you run the platform `setup.ps1` / `setup.py`.

```powershell
git clone https://github.com/kashewknutt/instagram-bot.git
cd instagram-bot
.\setup.ps1 -Profile fleet
```

**Open:** the platform repo root in Cursor (not this folder alone), unless you are editing the SDK.

Standalone:

```powershell
cd D:\GitHub\agent-sdk
python bootstrap.py
```

## Control API (every bot)

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness |
| GET | `/status` | Lifecycle, step, usage, artifacts |
| POST | `/run` | `{ "mode": "once" \| "daemon" }` |
| POST | `/pause` `/resume` `/stop` | Lifecycle |
| GET/PUT | `/direction` | Goals, hashtags, pillars |
