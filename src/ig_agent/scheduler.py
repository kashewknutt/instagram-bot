"""Continuous background scheduler for Instagram trend ingestion."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from ig_agent.config import get_settings
from ig_agent.filter import filter_latest_raw, load_agency_context
from ig_agent.ingest import capture_trends_with_delays
from ig_agent.multimodal import analyze_from_filtered_file
from ig_agent.safety import can_start_scroll_session, session_cooldown_seconds
from ig_agent.synthesize import synthesize_dashboard

logger = logging.getLogger("ig_agent.scheduler")


async def _run_session_with_timeout(coro, timeout_seconds: int):
    """Run ingestion with a hard session time cap."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout_seconds)
    except asyncio.TimeoutError:
        logger.warning("Session exceeded %d minute cap — stopping.", timeout_seconds // 60)
        raise


async def run_daemon() -> None:
    """Run continuous ingestion loop with safe delays and daily limits."""
    settings = get_settings()
    ctx = load_agency_context()
    hashtags = ctx.get("competitor_hashtags", [])
    session_timeout = settings.session_max_minutes * 60

    logger.info(
        "Daemon started — max %d sessions/day, %d min/session cap",
        settings.max_scroll_sessions_per_day,
        settings.session_max_minutes,
    )

    while True:
        try:
            if not can_start_scroll_session(settings):
                logger.info("Daily session limit reached. Sleeping 8 hours.")
                await asyncio.sleep(8 * 3600)
                continue

            logger.info("[%s] Starting ingestion pass...", datetime.now().isoformat())

            raw_path = await _run_session_with_timeout(
                capture_trends_with_delays(settings, hashtags),
                session_timeout,
            )
            logger.info("Raw data saved to %s", raw_path)

            filtered_path = filter_latest_raw(settings)
            if filtered_path:
                logger.info("Filtered data saved to %s", filtered_path)

                multimodal_notes = None
                if settings.enable_multimodal:
                    multimodal_notes = analyze_from_filtered_file(filtered_path, settings)
                    logger.info("Multimodal analysis: %d notes", len(multimodal_notes))

                report = synthesize_dashboard(settings, multimodal_notes)
                logger.info("Dashboard written to %s", report)

        except asyncio.TimeoutError:
            logger.warning("Session timed out — will retry after cooldown.")
        except Exception as exc:
            logger.exception("Session error: %s", exc)

        wait = session_cooldown_seconds()
        logger.info("Sleeping %d hours until next session...", wait // 3600)
        await asyncio.sleep(wait)
