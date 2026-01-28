import yfinance as yf
import pandas as pd
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# LISTA AMPLIADA (Top Movers, Semiconductores, Cripto-mineras y Tech)
TICKERS = [
    "ATEYY", "RNECY", "IREN", "WULF", "MARA", "RIOT", # Advantest, Renesas, Minería Crypto
    "ASTS", "PLTR", "SOUN", "BBAI", "RKLB",           # Space Tech e IA
    "NVDA", "AMD", "AVGO", "SMCI", "ARM",             # Semiconductores Top
    "TSLA", "COIN", "MSTR", "HOOD", "U",              # Volatilidad alta
    "BTC-USD", "ETH-USD", "SOL-USD"                   # Cripto (24/7)
]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def analizar_accion(ticker):
    try:
        # Descargamos datos de los últimos 2 días para comparar
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if len(df) < 2: return

        precio_hoy = df['Close'].iloc[-1]
        precio_ayer = df['Close'].iloc[-2]
        cambio_porcentaje = ((precio_hoy - precio_ayer) / precio_ayer) * 100
        
        vol_actual = df['Volume'].iloc[-1]
        vol_medio = df['Volume'].rolling(window=20).mean().iloc[-1]

        # ESTRATEGIA: Si sube más de un 4% CON volumen alto
        if cambio_porcentaje > 4.0 and vol_actual > (vol_medio * 1.2):
            mensaje = (
                f"🔥 *MOVIMIENTO DETECTADO: {ticker}*\n\n"
                f"💰 *Precio:* {precio_hoy:.2f}$\n"
                f"📈 *Subida:* +{cambio_porcentaje:.2f}%\n"
                f"📊 *Volumen:* Muy superior a la media\n"
                f"🚀 _Esta acción está rompiendo con fuerza hoy._"
            )
            enviar_telegram(mensaje)
    except Exception as e:
        print(f"Error analizando {ticker}: {e}")

def ejecutar():
    print(f"Escaneando {len(TICKERS)} acciones seleccionadas...")
    for t in TICKERS:
        analizar_accion(t)
    print("Escaneo finalizado.")

if __name__ == "__main__":
    ejecutar()
    
