import yfinance as yf
import pandas as pd
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# LISTA ADAPTADA A TRADE REPUBLIC (Mercados que abren por la mañana en Europa)
TICKERS = [
    "ATE.DE", "RN7.DE", "IREN", "ASTS",          # Advantest y Renesas en Alemania (Euros)
    "SAP.DE", "ASML.AS", "IFX.DE", "AIR.DE",     # Gigantes europeos (Tech y Aero)
    "SAN.MC", "ITX.MC", "TEF.MC",                # Ibex 35 (España)
    "BTC-USD", "ETH-USD", "SOL-USD",             # Cripto (Siempre activas)
    "NVDA", "TSLA", "AAPL", "AMD"                # USA (Para la tarde)
]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def analizar(ticker):
    try:
        # Usamos un periodo corto para ver el movimiento de HOY
        df = yf.download(ticker, period="2d", interval="15m", progress=False)
        if df.empty or len(df) < 5: return

        precio_actual = df['Close'].iloc[-1]
        precio_apertura = df['Open'].iloc[0]
        cambio_desde_apertura = ((precio_actual - precio_apertura) / precio_apertura) * 100
        
        # Filtro: Subida de más del 3% desde que abrió el mercado hoy
        if cambio_desde_apertura > 3.0:
            mensaje = (
                f"☀️ *AVISO MAÑANERO: {ticker}*\n\n"
                f"💰 *Precio:* {precio_actual:.2f}\n"
                f"📈 *Subida hoy:* +{cambio_desde_apertura:.2f}%\n"
                f"🚀 Está destacando en la apertura."
            )
            enviar_telegram(mensaje)
    except Exception as e:
        print(f"Error con {ticker}: {e}")

if __name__ == "__main__":
    # Esto te llegará siempre para confirmar que el bot funciona
    enviar_telegram("🔎 *Radar activado:* Buscando oportunidades en Trade Republic...")
    for t in TICKERS:
        analizar(t)
