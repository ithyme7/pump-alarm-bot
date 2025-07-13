# main.py - VERBETERDE VERSIE VOOR GITHUB ACTIONS

import os
import requests 
from dotenv import load_dotenv
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import pandas as pd

# Laad .env bestand ALLEEN voor lokale ontwikkeling. In de cloud is dit niet nodig.
load_dotenv()

# --- CONFIGURATIE ---
# Haal variabelen direct uit de omgeving (dit werkt lokaal én in GitHub)
DUNE_API_KEY = os.getenv("DUNE_API_KEY")
QUERY_ID = 5467029 # Zorg dat dit JOUW Query ID is
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- FUNCTIES ---

def send_telegram_alert(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("FOUT: TELEGRAM_BOT_TOKEN of TELEGRAM_CHAT_ID niet gevonden.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = { "chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown" }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(">>> Telegram alert succesvol verzonden!")
        else:
            print(f">>> Fout bij verzenden Telegram alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f">>> Uitzondering bij verzenden Telegram alert: {e}")

def fetch_dune_data():
    if not DUNE_API_KEY:
        print("FOUT: DUNE_API_KEY niet gevonden.")
        return None
        
    print("Dune API aanroepen met Query ID:", QUERY_ID)
    query = QueryBase(name="Pump Alarm v6 Query", query_id=QUERY_ID)
    dune = DuneClient(DUNE_API_KEY)
    try:
        results_df = dune.run_query_dataframe(query)
        print("Data succesvol opgehaald!")
        return results_df
    except Exception as e:
        print(f"Er ging iets mis bij het ophalen van data: {e}")
        return None

def analyze_and_alert(df: pd.DataFrame):
    if df is None or df.empty:
        print("Geen data om te analyseren.")
        return

    print("Data analyseren en alert voorbereiden...")
    alerts_message = "*🚨 Pump Alarm 2.0 - Top Movers (24u) 🚨*\n\n"
    
    for index, row in df.iterrows():
        symbol = row.get('token_symbol', 'Onbekend')
        if pd.isna(symbol): symbol = 'Onbekend'
        volume = row.get('total_volume_usd', 0)
        volume_formatted = f"${volume:,.0f}"
        alerts_message += f"• *${symbol}* - Volume: `{volume_formatted}`\n"
        
    send_telegram_alert(alerts_message)

# --- HOOFDPROGRAMMA ---
if __name__ == "__main__":
    print("--- Pump-Alarm 2.0 - Cloud/Lokaal Run ---")
    
    # Controleer of alle sleutels aanwezig zijn
    if not all([DUNE_API_KEY, TELEGRAM_TOKEN, CHAT_ID]):
         print("Een of meer vereiste omgevingsvariabelen ontbreken! Script stopt.")
    else:
        crypto_data_frame = fetch_dune_data()
        analyze_and_alert(crypto_data_frame)
        
    print("\n--- Script succesvol afgerond. ---")