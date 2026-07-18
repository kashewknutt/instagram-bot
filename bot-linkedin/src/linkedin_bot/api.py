"""HTTP control API for the LinkedIn stub bot."""

from __future__ import annotations

import os

from agent_sdk.api import create_control_app

from linkedin_bot.runtime import build_controller

controller = build_controller()
app = create_control_app(controller, title="LinkedIn Bot Control API")


def serve() -> None:
    import uvicorn

    port = int(os.getenv("BOT_PORT", "7412"))
    uvicorn.run("linkedin_bot.api:app", host="127.0.0.1", port=port, reload=False)


if __name__ == "__main__":
    serve()
