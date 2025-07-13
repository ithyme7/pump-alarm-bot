# main.py - De Correcte Versie voor Week 2

import os
import requests 
from dotenv import load_dotenv
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import pandas as pd

# --- CONFIGURATIE ---
load_dotenv()
dune_api_key = os.getenv("DUNE_API_KEY")
QUERY_ID = 5467029 # Zorg dat dit JOUW eigen Query ID is

# -- Config voor Telegram --
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# --- FUNCTIES ---

def send_telegram_alert(message):
    """Verstuurt een bericht naar de geconfigureerde Telegram chat."""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("FOUT: TELEGRAM_BOT_TOKEN of TELEGRAM_CHAT_ID niet gevonden in .env bestand.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(">>> Telegram alert succesvol verzonden!")
        else:
            print(f">>> Fout bij verzenden Telegram alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f">>> Uitzondering bij verzenden Telegram alert: {e}")


def fetch_dune_data():
    """Haalt de resultaten van een specifieke Dune query op."""
    if not dune_api_key:
        print("Fout: DUNE_API_KEY niet gevonden.")
        return None
    print("Dune API aanroepen met Query ID:", QUERY_ID)
    query = QueryBase(name="Pump Alarm v6 Query", query_id=QUERY_ID)
    dune = DuneClient(dune_api_key)
    try:
        results_df = dune.run_query_dataframe(query)
        print("Data succesvol opgehaald!")
        return results_df
    except Exception as e:
        print(f"Er ging iets mis bij het ophalen van data: {e}")
        return None


def analyze_and_alert(df: pd.DataFrame):
    """Analyseert data en stuurt een alert als er iets interessants is."""
    if df is None or df.empty:
        print("Geen data om te analyseren.")
        return

    print("Data analyseren en alert voorbereiden...")
    
    alerts_message = "*🚨 Pump Alarm 2.0 - Top Movers (24u) 🚨*\n\n"
    
    for index, row in df.iterrows():
        symbol = row.get('token_symbol', 'Onbekend')
        if pd.isna(symbol): # Check of symbool 'NaN' is (Not a Number)
            symbol = 'Onbekend'
        volume = row.get('total_volume_usd', 0)
        
        # Formatteer de USD waarde netjes met komma's en zonder decimalen
        volume_formatted = f"${volume:,.0f}"
        
        alerts_message += f"• *${symbol}* - Volume: `{volume_formatted}`\n"

    # Stuur het complete bericht als één alert
    send_telegram_alert(alerts_message)


# --- HOOFDPROGRAMMA ---
if __name__ == "__main__":
    print("--- Pump-Alarm 2.0 - LOKALE TEST - Week 2 ---")
    
    # 1. Haal de data op
    crypto_data_frame = fetch_dune_data()
    
    # 2. Analyseer en stuur de alert
    analyze_and_alert(crypto_data_frame)

    print("\n--- Script succesvol afgerond. ---")