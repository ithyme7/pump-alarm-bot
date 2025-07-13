# Pump Alarm Bot

This repository contains a small script that fetches trading data from Dune and sends alerts to Telegram.

## Required environment variables

The application expects the following variables to be available at runtime:

- `DUNE_API_KEY` – API key for Dune Analytics
- `TELEGRAM_BOT_TOKEN` – token for your Telegram bot
- `TELEGRAM_CHAT_ID` – ID of the Telegram chat that should receive the alerts

### Local usage

Create a `.env` file in the project root containing the variables above, e.g.:

```env
DUNE_API_KEY=your-dune-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id
```

The project uses [python-dotenv](https://github.com/theskumar/python-dotenv) so these values will be loaded automatically when running the script locally.

### GitHub Actions

When running in GitHub Actions, define the same variables as repository secrets. They will be passed to the workflow defined in `.github/workflows/main.yml`.

