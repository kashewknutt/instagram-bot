"""Configuration loaded from environment variables."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
FILTERED_DIR = DATA_DIR / "filtered"
MEDIA_DIR = DATA_DIR / "media"
REPORTS_DIR = PROJECT_ROOT / "reports"
AGENCY_CONTEXT_PATH = PROJECT_ROOT / "agency_context.json"

_DEFAULT_CHROME_PATHS = {
    "win32": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "darwin": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "linux": "/usr/bin/google-chrome",
}


def _default_chrome_path() -> str:
    return _DEFAULT_CHROME_PATHS.get(sys.platform, _DEFAULT_CHROME_PATHS["linux"])


def _expand_path(value: str) -> Path:
    return Path(os.path.expanduser(value)).resolve()


@dataclass
class Settings:
    moonshot_api_key: str = field(default_factory=lambda: os.getenv("MOONSHOT_API_KEY", ""))
    kimi_base_url: str = field(
        default_factory=lambda: os.getenv("KIMI_BASE_URL", "https://api.moonshot.ai/v1")
    )
    kimi_filter_model: str = field(
        default_factory=lambda: os.getenv("KIMI_FILTER_MODEL", "kimi-k2.6")
    )
    kimi_synth_model: str = field(
        default_factory=lambda: os.getenv("KIMI_SYNTH_MODEL", "kimi-k3")
    )
    kimi_browser_model: str = field(
        default_factory=lambda: os.getenv("KIMI_BROWSER_MODEL", "kimi-k2.6")
    )
    chrome_path: str = field(
        default_factory=lambda: os.getenv("CHROME_PATH", _default_chrome_path())
    )
    browser_user_data_dir: Path = field(
        default_factory=lambda: _expand_path(
            # Avoid "chrome" in the path — browser-use treats those as system
            # Chrome profiles and copies them to a disposable temp directory.
            os.getenv("BROWSER_USER_DATA_DIR", "./data/browser-profile")
        )
    )
    max_posts_per_session: int = field(
        default_factory=lambda: int(os.getenv("MAX_POSTS_PER_SESSION", "5"))
    )
    max_scroll_sessions_per_day: int = field(
        default_factory=lambda: int(os.getenv("MAX_SCROLL_SESSIONS_PER_DAY", "4"))
    )
    session_max_minutes: int = field(
        default_factory=lambda: int(os.getenv("SESSION_MAX_MINUTES", "12"))
    )
    multimodal_top_n: int = field(
        default_factory=lambda: int(os.getenv("MULTIMODAL_TOP_N", "3"))
    )
    enable_multimodal: bool = field(
        default_factory=lambda: os.getenv("ENABLE_MULTIMODAL", "false").lower() == "true"
    )
    relevance_threshold: int = 60

    def ensure_dirs(self) -> None:
        for path in (RAW_DIR, FILTERED_DIR, MEDIA_DIR, REPORTS_DIR):
            path.mkdir(parents=True, exist_ok=True)
        self.browser_user_data_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_dirs()
    return settings
