# Kimi-Powered Local Instagram Trend Agent

Hybrid local agent for software agency social media trend analysis. Uses **browser-use** for Instagram data collection and **Kimi (Moonshot AI)** for filtering, multimodal analysis, and daily creative synthesis.

## Prerequisites

- Python 3.11+
- Google Chrome installed
- Kimi API key from [platform.kimi.ai](https://platform.kimi.ai)
- Logged-in Instagram session (saved under `data/browser-profile`)

## Setup

### Windows (PowerShell)

```powershell
cd instagram-bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
playwright install chromium

copy .env.example .env
# Edit .env and set MOONSHOT_API_KEY
# CHROME_PATH defaults to C:\Program Files\Google\Chrome\Application\chrome.exe
```

### macOS / Linux

```bash
cd instagram-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
playwright install chromium --with-deps

cp .env.example .env
# Edit .env and set MOONSHOT_API_KEY
```

## Instagram login

Ingest uses bundled Chromium with a persistent profile at `data/browser-profile`.

```powershell
python main.py ingest
```

On first run, log into Instagram in the opened browser window (including 2FA). Close nothing until the agent finishes or you are logged in — the session is saved and reused on later runs.

# Test full pipeline offline (no API key needed)
python main.py --offline run-once --sample

# Filter sample data only
python main.py --offline filter-sample

# Live Instagram scrape → filter → dashboard
python main.py run-once

# Individual steps
python main.py ingest
python main.py filter
python main.py synthesize

# Continuous background scheduler
python main.py daemon

# Multimodal analysis on top Reels (requires ENABLE_MULTIMODAL=true + API key)
python main.py analyze-media
```

## Configuration

Edit `agency_context.json` for your brand, audience, and content pillars.

Key env vars in `.env`:

| Variable | Default | Purpose |
|---|---|---|
| `MOONSHOT_API_KEY` | — | Kimi API key |
| `BROWSER_USER_DATA_DIR` | `./data/browser-profile` | Persistent Instagram login profile |
| `KIMI_FILTER_MODEL` | `kimi-k2.6` | Relevance filtering |
| `KIMI_SYNTH_MODEL` | `kimi-k3` | Daily dashboard synthesis |
| `ENABLE_MULTIMODAL` | `false` | Video/image analysis (costs more) |
| `MAX_SCROLL_SESSIONS_PER_DAY` | `4` | Safety rate limit |

## Output

- Raw scrapes: `data/raw/scraped_*.json`
- Filtered trends: `data/filtered/filtered_*.json`
- Daily dashboard: `reports/Daily_Social_Dashboard_YYYY-MM-DD.md`

## Safety

This agent is **observation-only** — it does not like, comment, follow, or post. Daily session limits and humanized delays are enforced in `src/ig_agent/safety.py`.

## Architecture

```
Scheduler → Ingest (browser-use) → Filter (kimi-k2.6) → Synthesize (kimi-k3) → Markdown Dashboard
                                              ↓
                                    Multimodal (optional, kimi-k3)
```
