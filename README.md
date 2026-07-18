# bot-instagram (plugin)

Instagram observation bot — a **plugin** for [social-agent-platform](https://github.com/kashewknutt/social-agent-platform).

Do **not** treat this repo as the product. Clone the platform, then let setup pull this plugin.

## Recommended setup

```powershell
cd D:\GitHub
git clone https://github.com/kashewknutt/social-agent-platform.git
cd social-agent-platform
.\setup.ps1 -Profile instagram   # or fleet
```

**Open in Cursor:** `D:\GitHub\social-agent-platform`  
(or the multi-root workspace file `social-agents.code-workspace`)

This plugin is cloned into `social-agent-platform/plugins/bot-instagram`.

## Develop this plugin alone

```powershell
git clone https://github.com/kashewknutt/instagram-bot.git bot-instagram
cd bot-instagram
python bootstrap.py
# ensures the platform (and agent-sdk) exist as siblings / parent
```

## CLI

```powershell
pip install -e ../agent-sdk   # or from platform .venv
pip install -e .
copy .env.example .env        # set MOONSHOT_API_KEY
python main.py --offline run-once --sample
python main.py serve --port 7411
```
