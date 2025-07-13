# Pump Alarm Bot

This project contains a small Python script that reads trade volume data from
[Dune Analytics](https://dune.com) and posts the results to a Telegram chat.
It can be executed manually or scheduled using GitHub Actions.

## Setup

1. **Python** – Install Python 3.10 or newer.
2. **Dependencies** – Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment variables** – Provide the following values either via a `.env`
   file or your environment:
   - `DUNE_API_KEY` – your Dune API key
   - `TELEGRAM_BOT_TOKEN` – Telegram bot token
   - `TELEGRAM_CHAT_ID` – ID of the chat that should receive alerts

## Usage

Run the main script locally after setting the environment variables:

```bash
python main.py
```

The repository also contains a GitHub Actions workflow in
`.github/workflows/main.yml` that runs `main.py` every 15 minutes when the
required secrets are configured in your GitHub repository.

The SQL query used to fetch the data can be found in `query.sql` for reference.
