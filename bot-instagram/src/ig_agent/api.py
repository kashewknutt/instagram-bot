"""HTTP control API for the Instagram bot."""

from __future__ import annotations

import os

from agent_sdk.api import create_control_app

from ig_agent.runtime import build_controller

controller = build_controller()
app = create_control_app(controller, title="Instagram Bot Control API")


def serve() -> None:
    import uvicorn

    port = int(os.getenv("BOT_PORT", "7411"))
    uvicorn.run("ig_agent.api:app", host="127.0.0.1", port=port, reload=False)


if __name__ == "__main__":
    serve()
