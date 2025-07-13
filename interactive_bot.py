"""Simple interactive Telegram bot using python-telegram-bot."""
import asyncio
import os

import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from main import fetch_dune_data, format_message

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Pump Alarm Bot ready. Use /top to get the latest movers.")


async def top(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    df = await fetch_dune_data(24, 1000, 10, None)
    if df.empty:
        await update.message.reply_text("No data available.")
    else:
        await update.message.reply_text(format_message(df, 24), parse_mode="Markdown")


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not set")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("top", top))
    app.run_polling()


if __name__ == "__main__":
    main()
