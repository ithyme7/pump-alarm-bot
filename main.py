"""Pump Alarm Bot with logging, history and graph support."""
import argparse
import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from dune_client.client import DuneClient
from dune_client.query import QueryBase, QueryParameter
import requests

load_dotenv()

DUNE_API_KEY = os.getenv("DUNE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
QUERY_ID = 5467029

HISTORY_FILE = Path("data/history.csv")
CHART_FILE = Path("charts/latest.png")


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler("bot.log")],
    )


def send_telegram_alert(message: str, image_path: Path | None = None) -> None:
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logging.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return

    if image_path and image_path.exists():
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        with image_path.open("rb") as photo:
            data = {"chat_id": CHAT_ID, "caption": message, "parse_mode": "Markdown"}
            files = {"photo": photo}
            requests.post(url, data=data, files=files, timeout=10)
    else:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=10)


async def fetch_dune_data(hours: int, min_volume: int, limit: int, token: str | None) -> pd.DataFrame:
    if not DUNE_API_KEY:
        logging.error("DUNE_API_KEY not set")
        return pd.DataFrame()

    params = [
        QueryParameter.number_type("hours", hours),
        QueryParameter.number_type("min_volume", min_volume),
        QueryParameter.number_type("limit", limit),
    ]
    if token:
        params.append(QueryParameter.text_type("token", token))

    query = QueryBase(name="Pump Alarm Query", query_id=QUERY_ID, params=params)
    dune = DuneClient(DUNE_API_KEY)
    return await asyncio.to_thread(dune.run_query_dataframe, query)


def save_history(df: pd.DataFrame, path: Path = HISTORY_FILE) -> None:
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, index=False)


def create_chart(df: pd.DataFrame, path: Path = CHART_FILE) -> Path:
    path.parent.mkdir(exist_ok=True)
    plt.figure(figsize=(8, 4))
    plt.bar(df["token_symbol"], df["total_volume_usd"])
    plt.title("Top token volume")
    plt.xlabel("Token")
    plt.ylabel("Volume USD")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path


def format_message(df: pd.DataFrame, hours: int) -> str:
    lines = [f"*🚨 Pump Alarm - Top Movers ({hours}h) 🚨*\n"]
    for _, row in df.iterrows():
        symbol = row.get("token_symbol", "?")
        volume = row.get("total_volume_usd", 0)
        lines.append(f"• *${symbol}* - `{volume:,.0f}`")
    return "\n".join(lines)


async def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(description="Pump Alarm Bot")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--min-volume", type=int, default=1000)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--token", type=str, default=None)
    args = parser.parse_args()

    df = await fetch_dune_data(args.hours, args.min_volume, args.limit, args.token)
    if df.empty:
        logging.info("No data returned from Dune")
        return

    save_history(df)
    chart = create_chart(df)
    message = format_message(df, args.hours)
    send_telegram_alert(message, chart)


if __name__ == "__main__":
    asyncio.run(main())
