# orchestrator

Local control plane and **Fleet Control** dashboard for plug-and-play social observation bots.

## What it does

- Reads `orchestrator.yaml` for bot paths/ports
- Proxies start / pause / resume / stop / direction / logs
- Can boot each bot’s control API as a subprocess
- Serves the control UI at `http://127.0.0.1:7400`

## Setup

```powershell
cd orchestrator
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .

# optional Vite build (public/ fallback works without this)
cd frontend
npm install
npm run build
cd ..
```

Also install sibling packages the bots need:

```powershell
pip install -e ..\agent-sdk
pip install -e ..\bot-instagram
pip install -e ..\bot-linkedin
pip install -e ..\bot-x
```

## Run

```powershell
python -m orchestrator_app.main
# open http://127.0.0.1:7400
```

In the UI:

1. Select a bot
2. **Boot API** (starts that bot’s uvicorn process)
3. **Run once** / **Daemon** / **Pause** / **Stop**
4. Edit **Direction** (hashtags, pillars, goals) and save

## Config

```yaml
# orchestrator.yaml
bots:
  - id: instagram
    path: ../bot-instagram
    port: 7411
    enabled: true
```

Add another bot: clone/copy a bot package, add an entry, refresh the UI.
