# Pump Alarm Bot

A Python bot that fetches token trade volume data from [Dune Analytics](https://dune.com) and posts the top movers to Telegram. Results are stored locally for historical analysis and a small bar chart is generated for each run.

## Setup

1. **Python** – Install Python 3.10 or newer.
2. **Dependencies** – Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment variables** – Copy `.env.example` to `.env` and fill in your values or export them in your environment:
   - `DUNE_API_KEY` – your Dune API key
   - `TELEGRAM_BOT_TOKEN` – Telegram bot token
   - `TELEGRAM_CHAT_ID` – ID of the chat that should receive alerts

## Usage

Run the bot locally:

```bash
python main.py --hours 24 --min-volume 1000 --limit 10
```

A helper script `interactive_bot.py` provides Telegram commands (`/top`) to fetch the latest movers on demand.

## GitHub Actions

The repository includes a workflow that runs the bot every 15 minutes and a separate workflow that runs tests and linting on each push.
