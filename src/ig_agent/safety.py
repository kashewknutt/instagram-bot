"""Humanized delays and daily rate limits for Instagram safety."""

from __future__ import annotations

import asyncio
import json
import random
from datetime import date, datetime
from pathlib import Path

from ig_agent.config import DATA_DIR, Settings, get_settings

USAGE_LOG = DATA_DIR / "usage_log.json"


def human_delay(min_seconds: float, max_seconds: float) -> float:
    """Return a randomized delay within bounds."""
    return random.uniform(min_seconds, max_seconds)


async def async_sleep(min_seconds: float, max_seconds: float) -> None:
    delay = human_delay(min_seconds, max_seconds)
    await asyncio.sleep(delay)


def _load_usage() -> dict:
    if USAGE_LOG.exists():
        return json.loads(USAGE_LOG.read_text(encoding="utf-8"))
    return {"date": str(date.today()), "scroll_sessions": 0}


def _save_usage(data: dict) -> None:
    USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    USAGE_LOG.write_text(json.dumps(data, indent=2), encoding="utf-8")


def can_start_scroll_session(settings: Settings | None = None) -> bool:
    """Check if another scroll session is allowed today."""
    cfg = settings or get_settings()
    usage = _load_usage()
    today = str(date.today())
    if usage.get("date") != today:
        usage = {"date": today, "scroll_sessions": 0}
        _save_usage(usage)
    return usage["scroll_sessions"] < cfg.max_scroll_sessions_per_day


def record_scroll_session() -> None:
    usage = _load_usage()
    today = str(date.today())
    if usage.get("date") != today:
        usage = {"date": today, "scroll_sessions": 0}
    usage["scroll_sessions"] += 1
    usage["last_session_at"] = datetime.now().isoformat()
    _save_usage(usage)


def scroll_delay() -> float:
    """Delay between scroll actions (simulated human scrolling)."""
    return human_delay(2.0, 5.0)


def profile_query_delay() -> float:
    """Delay between profile/hashtag queries."""
    return human_delay(60.0, 120.0)


def session_cooldown_seconds() -> int:
    """Idle time between sessions (3–6 hours)."""
    return random.randint(3 * 3600, 6 * 3600)
