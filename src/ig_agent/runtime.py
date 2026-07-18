"""Wire Instagram pipeline into the shared BotController."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from agent_sdk.control import BotController
from agent_sdk.models import ArtifactInfo, Direction, RunMode, RunRequest

from ig_agent.config import (
    AGENCY_CONTEXT_PATH,
    DATA_DIR,
    FILTERED_DIR,
    PROJECT_ROOT,
    RAW_DIR,
    REPORTS_DIR,
    get_settings,
)
from ig_agent.filter import filter_raw_file, load_agency_context
from ig_agent.ingest import capture_trends_with_delays
from ig_agent.multimodal import analyze_from_filtered_file
from ig_agent.safety import can_start_scroll_session, session_cooldown_seconds
from ig_agent.synthesize import synthesize_dashboard


def _direction_from_context(ctx: dict[str, Any]) -> Direction:
    return Direction(
        brand_name=ctx.get("brand_name", ""),
        business_type=ctx.get("business_type", ""),
        target_audience=list(ctx.get("target_audience", [])),
        content_pillars=list(ctx.get("content_pillars", [])),
        brand_voice=ctx.get("brand_voice", ""),
        competitor_hashtags=list(ctx.get("competitor_hashtags", [])),
        competitor_profiles=list(ctx.get("competitor_profiles", [])),
        goals=ctx.get("goals", ""),
        constraints=ctx.get(
            "constraints",
            "Observation only. Do not like, comment, follow, or post.",
        ),
    )


def load_direction() -> Direction:
    if not AGENCY_CONTEXT_PATH.exists():
        return Direction()
    return _direction_from_context(json.loads(AGENCY_CONTEXT_PATH.read_text(encoding="utf-8")))


def save_direction(direction: Direction) -> None:
    AGENCY_CONTEXT_PATH.write_text(
        json.dumps(direction.model_dump(), indent=2) + "\n",
        encoding="utf-8",
    )


def load_usage() -> dict[str, Any]:
    settings = get_settings()
    usage_path = DATA_DIR / "usage_log.json"
    if usage_path.exists():
        raw = json.loads(usage_path.read_text(encoding="utf-8"))
    else:
        raw = {"date": datetime.now().date().isoformat(), "scroll_sessions": 0}
    used = int(raw.get("scroll_sessions", 0))
    return {
        "date": raw.get("date", ""),
        "scroll_sessions": used,
        "max_scroll_sessions_per_day": settings.max_scroll_sessions_per_day,
        "sessions_remaining": max(0, settings.max_scroll_sessions_per_day - used),
        "last_session_at": raw.get("last_session_at"),
    }


def _mtime_iso(path: Path) -> str | None:
    if not path.exists():
        return None
    return datetime.fromtimestamp(path.stat().st_mtime).isoformat()


def load_artifacts() -> list[ArtifactInfo]:
    artifacts: list[ArtifactInfo] = []
    raw_files = sorted(RAW_DIR.glob("scraped_*.json"), key=lambda p: p.stat().st_mtime)
    if raw_files:
        p = raw_files[-1]
        artifacts.append(ArtifactInfo(kind="raw", path=str(p), modified_at=_mtime_iso(p)))
    filtered = sorted(FILTERED_DIR.glob("filtered_*.json"), key=lambda p: p.stat().st_mtime)
    if filtered:
        p = filtered[-1]
        artifacts.append(ArtifactInfo(kind="filtered", path=str(p), modified_at=_mtime_iso(p)))
    reports = sorted(REPORTS_DIR.glob("Daily_Social_Dashboard_*.md"), key=lambda p: p.stat().st_mtime)
    if reports:
        p = reports[-1]
        artifacts.append(ArtifactInfo(kind="report", path=str(p), modified_at=_mtime_iso(p)))
    return artifacts


async def run_pipeline(controller: BotController, request: RunRequest) -> None:
    settings = get_settings()
    direction = controller.get_direction()
    hashtags = direction.competitor_hashtags

    async def one_pass() -> None:
        await controller.checkpoint()
        controller.set_step("ingest", "Starting Instagram ingestion")

        if request.sample:
            sample_path = RAW_DIR / "sample_scraped.json"
            if not sample_path.exists():
                raise FileNotFoundError(f"Sample file missing: {sample_path}")
            raw_path = sample_path
            controller.set_step("ingest", f"Using sample data: {raw_path.name}")
        else:
            if not can_start_scroll_session(settings):
                raise RuntimeError(
                    f"Daily scroll session limit ({settings.max_scroll_sessions_per_day}) reached."
                )
            await controller.checkpoint()
            raw_path = await capture_trends_with_delays(settings, hashtags)
            controller.set_step("ingest", f"Ingested → {raw_path.name}")

        await controller.checkpoint()
        controller.set_step("filter", "Filtering for relevance")
        filtered_path = filter_raw_file(raw_path, offline=request.offline)
        controller.set_step("filter", f"Filtered → {filtered_path.name}")

        multimodal_notes = None
        if request.multimodal or settings.enable_multimodal:
            await controller.checkpoint()
            controller.set_step("multimodal", "Running multimodal analysis")
            multimodal_notes = analyze_from_filtered_file(filtered_path, settings)
            controller.set_step("multimodal", f"{len(multimodal_notes)} notes")

        await controller.checkpoint()
        controller.set_step("synthesize", "Synthesizing daily dashboard")
        report = synthesize_dashboard(
            multimodal_notes=multimodal_notes,
            offline=request.offline,
        )
        controller.set_step("synthesize", f"Dashboard → {report.name}")

    if request.mode == RunMode.ONCE:
        await one_pass()
        return

    # Daemon mode with cooperative pause/stop between sessions.
    session_timeout = settings.session_max_minutes * 60
    while not controller._stop.is_set():
        await controller.checkpoint()
        if not can_start_scroll_session(settings):
            controller.set_step("cooldown", "Daily session limit reached — sleeping 8h")
            for _ in range(8 * 3600):
                if controller._stop.is_set():
                    return
                await controller.checkpoint()
                await asyncio.sleep(1)
            continue

        try:
            await asyncio.wait_for(one_pass(), timeout=session_timeout)
        except asyncio.TimeoutError:
            controller.set_step("timeout", "Session exceeded time cap")
        except Exception as exc:
            controller.set_step("error", str(exc))
            controller.last_error = str(exc)

        wait = session_cooldown_seconds()
        controller.set_step("cooldown", f"Sleeping {wait // 3600}h until next session")
        for _ in range(wait):
            if controller._stop.is_set():
                return
            await controller.checkpoint()
            await asyncio.sleep(1)


def build_controller() -> BotController:
    get_settings()  # ensure dirs
    return BotController(
        bot_id="instagram",
        name="Instagram Trend Bot",
        network="instagram",
        root=PROJECT_ROOT,
        pipeline=run_pipeline,
        load_direction=load_direction,
        save_direction=save_direction,
        load_usage=load_usage,
        load_artifacts=load_artifacts,
    )
