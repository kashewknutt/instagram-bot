# agent-sdk

Shared runtime and HTTP control contract for plug-and-play social observation bots.

## Install

```bash
pip install -e ../agent-sdk
# or from a sibling clone:
pip install -e ./agent-sdk
```

## Bot contract

Every bot exposes the same FastAPI control surface via `create_control_app(controller)`:

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness |
| GET | `/status` | Lifecycle, step, usage, artifacts |
| POST | `/run` | `{ "mode": "once" \| "daemon" }` |
| POST | `/pause` | Pause a running job |
| POST | `/resume` | Resume from pause |
| POST | `/stop` | Cooperative stop |
| GET | `/logs?tail=200` | Recent log / event lines |
| GET | `/direction` | Current goals / hashtags / pillars |
| PUT | `/direction` | Update direction |

Lifecycle states: `idle | running | paused | error | stopped`.

## Package layout

- `agent_sdk.models` — status / direction / event schemas
- `agent_sdk.control` — `BotController` pause/stop/status runtime
- `agent_sdk.events` — JSONL run event stream
- `agent_sdk.api` — FastAPI router factory
- `agent_sdk.safety` — session caps and humanized delays
- `agent_sdk.llm` — Moonshot/Kimi client (fixed temperature=1)

## bot.yaml

```yaml
id: instagram
name: Instagram Trend Bot
network: instagram
version: 0.1.0
entry: ig_agent.api:app
default_port: 7411
```
