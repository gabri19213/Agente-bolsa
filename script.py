import yfinance as yf
import pandas as pd
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# LISTA AGRESIVA: Semiconductores, IA, Minería Cripto, Space Tech y "Top Movers"
TICKERS = [
    # --- Las que tú mencionaste ---
    "ATEYY", "RNECY", "IREN", "ASTS", 
    # --- IA y Datos ---
    "NVDA", "PLTR", "SOUN", "BBAI", "SMCI", "AMD", "ARM", "AI",
    # --- Minería Cripto y Blockchain (Muy volátiles) ---
    "MARA", "RIOT", "WULF", "CLSK", "COIN", "MSTR",
    # --- Space & Futuro ---
    "RKLB", "LUNR", "SPCE", "IONQ",
    # --- Agresivas USA ---
    "TSLA", "UPST", "AFRM", "HOOD", "PYPL", "U", "NET", "SNOW",
    # --- Penny Stocks / High Volatility ---
    "SOXL", "TQQQ", "BITO", 
    # --- Criptomonedas (24/7) ---
    "BTC-USD", "ETH-USD", "SOL-USD", "PEPE-USD", "DOGE-USD"
]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def analizar(ticker):
    try:
        df = yf.download(ticker, period="60d", interval="1d", progress=False)
        if len(df) < 30: return

        # Cálculos básicos
        precio_hoy = df['Close'].iloc[-1]
        precio_ayer = df['Close'].iloc[-2]
        cambio_diario = ((precio_hoy - precio_ayer) / precio_ayer) * 100
        
        # Volumen
        vol_actual = df['Volume'].iloc[-1]
        vol_medio = df['Volume'].rolling(window=20).mean().iloc[-1]

        # RSI (Para detectar caídas excesivas o sobrecompra)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]

        # --- ESTRATEGIA 1: COHETE (SUBIDA FUERTE) ---
        if cambio_diario > 5.0 and vol_actual > (vol_medio * 1.3):
            mensaje = (
                f"🚀 *¡COHETE DETECTADO!* \n"
                f"💎 *Activo:* {ticker}\n"
                f"📈 *Subida:* +{cambio_diario:.2f}%\n"
                f"📊 *Volumen:* EXPLOSIVO (x1.3+)\n"
                f"🔥 *RSI:* {rsi:.1f}\n"
                f"💰 *Precio:* {precio_hoy:.2f}$"
            )
            enviar_telegram(mensaje)

        # --- ESTRATEGIA 2: OPORTUNIDAD (CAÍDA Y REBOTE) ---
        elif rsi < 30:
            mensaje = (
                f"📉 *OPORTUNIDAD (Sobrevendido)*\n"
                f"💎 *Activo:* {ticker}\n"
                f"🛡️ *RSI:* {rsi:.1f} (Punto de rebote)\n"
                f"💰 *Precio:* {precio_hoy:.2f}$\n"
                f"⚠️ _Está muy barata. Vigila el giro al alza._"
            )
            enviar_telegram(mensaje)

    except Exception as e:
        print(f"Error con {ticker}: {e}")

def ejecutar():
    print(f"Escaneando radar de {len(TICKERS)} activos...")
    for t in TICKERS:
        analizar(t)
    print("Fin del escaneo.")

if __name__ == "__main__":
    ejecutar()
    
