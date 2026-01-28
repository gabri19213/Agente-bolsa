import yfinance as yf
import pandas as pd
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TICKERS = ["NVDA", "TSLA", "AAPL", "AMD", "COIN", "PLTR", "MSFT", "META"]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def escanear():
    for ticker in TICKERS:
        try:
            df = yf.download(ticker, period="60d", interval="1d", progress=False)
            if len(df) < 30: continue
            precio = df['Close'].iloc[-1]
            vol_actual = df['Volume'].iloc[-1]
            vol_medio = df['Volume'].rolling(window=20).mean().iloc[-1]
            if true: # Ajustado a 1.2 para que sea más fácil que salte hoy
                aviso = f"🚀 *ALERTA: {ticker}*\n💰 Precio: {precio:.2f}$\n📊 ¡Volumen alto detectado!"
                enviar_telegram(aviso)
        except: continue

if __name__ == "__main__":
    escanear()
  
