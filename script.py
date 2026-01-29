import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# CONFIGURACIÓN DEL RADAR - MÁS DE 70 ACCIONES
SCT_IA_SEMI = ["NVDA", "AMD", "AVGO", "SMCI", "ARM", "ASML", "TSM", "INTC", "PLTR", "SOUN", "BBAI", "ATEYY", "RNECY"]
SCT_CRYPTO = ["BTC-USD", "ETH-USD", "SOL-USD", "COIN", "MSTR", "MARA", "RIOT", "IREN", "WULF", "CLSK", "HIVE"]
SCT_CRECIMIENTO = ["TSLA", "ASTS", "RKLB", "LUNR", "PLUG", "NIO", "XPEV", "LI", "RIVN", "LCID", "SOXL"]
SCT_EUROPA = ["SAP.DE", "IFX.DE", "DAI.DE", "BMW.DE", "AIR.DE", "AD.AS", "SAN.MC", "ITX.MC", "TEF.MC", "FER.MC"]
SCT_BIG_TECH = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NFLX", "ADBE", "PYPL", "HOOD", "UBER", "ABNB"]

# Unimos todas las listas en una sola
TODOS_LOS_TICKERS = SCT_IA_SEMI + SCT_CRYPTO + SCT_CRECIMIENTO + SCT_EUROPA + SCT_BIG_TECH

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def analizar(ticker):
    try:
        # Traemos datos de 5 días para tener contexto de volumen y precio
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if df.empty or len(df) < 2: return

        precio_actual = df['Close'].iloc[-1]
        variacion = ((precio_actual - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        vol_actual = df['Volume'].iloc[-1]
        vol_medio = df['Volume'].rolling(window=5).mean().iloc[-1]

        # REGLA DE ORO: Si sube más de un 4% y el volumen es alto, es señal de compra
        if variacion > 4.0 and vol_actual > vol_medio:
            mensaje = (
                f"🔥 *¡MOVIMIENTO DETECTADO!* ({ticker})\n"
                f"💰 *Precio:* {precio_actual:.2f}$\n"
                f"📈 *Variación:* +{variacion:.2f}%\n"
                f"📊 *Volumen:* Por encima de la media\n"
                f"🎯 _Acción detectada en el radar de Trade Republic._"
            )
            enviar_telegram(mensaje)
    except:
        pass

if __name__ == "__main__":
    enviar_telegram(f"🔎 *Escáner Global Activo:* Analizando {len(TODOS_LOS_TICKERS)} activos...")
    for t in TODOS_LOS_TICKERS:
        analizar(t)
