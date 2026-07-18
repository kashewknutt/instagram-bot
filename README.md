# social-agent-platform

**This is the repo to clone.** Fleet Control + shared SDK. Network bots (Instagram, LinkedIn, X, …) are **plugins**.

```text
social-agent-platform/          ← you are here (clone this)
├── agent-sdk/                  core
├── orchestrator/               Fleet Control UI
├── bot-linkedin/ bot-x/        optional built-in stubs
├── plugins/
│   └── bot-instagram/          ← cloned from kashewknutt/instagram-bot
├── setup.ps1 / setup.py
└── platform.manifest.yaml
```

## Quick start (Windows)

```powershell
cd D:\GitHub
git clone https://github.com/kashewknutt/social-agent-platform.git
cd social-agent-platform
.\setup.ps1 -Profile fleet
```

Profiles:

| Profile | What you get |
|---------|----------------|
| `core` | SDK + dashboard only |
| `instagram` | + Instagram plugin |
| `fleet` | + Instagram + LinkedIn/X stubs |

**Open in Cursor:** this folder, or double-click `social-agents.code-workspace`.

```powershell
.\.venv\Scripts\Activate.ps1
# set MOONSHOT_API_KEY in plugins\bot-instagram\.env
python -m orchestrator_app.main
# http://127.0.0.1:7400
```

## Instagram is a plugin

Setup clones [kashewknutt/instagram-bot](https://github.com/kashewknutt/instagram-bot) into `plugins/bot-instagram`.  
You do **not** need to clone Instagram first.

To add another bot later: publish it as its own repo, add an entry under `packages:` in `platform.manifest.yaml` with `kind: plugin`, and reference it from a profile.

## Multi-root workspace

`social-agents.code-workspace` opens the platform and any checked-out plugins together for development.
