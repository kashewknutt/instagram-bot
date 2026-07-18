"""Stub pipeline + controller for X."""

from __future__ import annotations

import json
from pathlib import Path

from agent_sdk.control import BotController
from agent_sdk.models import ArtifactInfo, Direction, RunRequest

ROOT = Path(__file__).resolve().parents[2]
DIRECTION_PATH = ROOT / "direction.json"


def load_direction() -> Direction:
    if not DIRECTION_PATH.exists():
        return Direction(brand_name="X stub")
    return Direction(**json.loads(DIRECTION_PATH.read_text(encoding="utf-8")))


def save_direction(direction: Direction) -> None:
    DIRECTION_PATH.write_text(json.dumps(direction.model_dump(), indent=2) + "\n", encoding="utf-8")


def load_usage() -> dict:
    return {
        "date": "",
        "scroll_sessions": 0,
        "max_scroll_sessions_per_day": 0,
        "sessions_remaining": 0,
        "last_session_at": None,
    }


def load_artifacts() -> list[ArtifactInfo]:
    return []


async def run_pipeline(controller: BotController, request: RunRequest) -> None:
    await controller.checkpoint()
    controller.set_step("stub", "X pipeline not implemented")
    raise NotImplementedError(
        "bot-x is a stub. Implement X observation ingest before running."
    )


def build_controller() -> BotController:
    (ROOT / "data" / "runs").mkdir(parents=True, exist_ok=True)
    return BotController(
        bot_id="x",
        name="X Trend Bot",
        network="x",
        root=ROOT,
        pipeline=run_pipeline,
        load_direction=load_direction,
        save_direction=save_direction,
        load_usage=load_usage,
        load_artifacts=load_artifacts,
    )
