# Kimi-Powered Local Instagram Trend Agent

Hybrid local agent for software agency social media trend analysis. Uses **browser-use** for Instagram data collection and **Kimi (Moonshot AI)** for filtering, multimodal analysis, and daily creative synthesis.

## Prerequisites

- Python 3.11+
- Google Chrome installed
- Kimi API key from [platform.kimi.ai](https://platform.kimi.ai)
- Logged-in Instagram session (browser profile persists login)

## Setup

```bash
cd instagram-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
playwright install chromium --with-deps

cp .env.example .env
# Edit .env and set MOONSHOT_API_KEY
```

## Commands

```bash
# Verify Kimi API works (requires MOONSHOT_API_KEY in .env)
python main.py smoke-test

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
