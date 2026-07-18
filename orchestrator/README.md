# orchestrator

Local **Fleet Control** dashboard for social observation bots.

## Clone & setup

**Preferred:** clone the platform and pick a profile that includes the dashboard:

```powershell
git clone https://github.com/kashewknutt/instagram-bot.git
cd instagram-bot
.\setup.ps1 -Profile fleet
```

**Open in Cursor:** the platform repo root (`instagram-bot`), then run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m orchestrator_app.main
# http://127.0.0.1:7400
```

### If you only cloned this package

```powershell
cd D:\GitHub\orchestrator
python bootstrap.py --all-bots
# fetches ../agent-sdk and bot-* siblings as needed
```

Or Instagram only:

```powershell
python bootstrap.py --with instagram
```

## UI actions

1. Select a bot  
2. **Boot API**  
3. **Run once** / **Daemon** / **Pause** / **Stop**  
4. Edit **Direction** (hashtags, pillars, goals) and save  
