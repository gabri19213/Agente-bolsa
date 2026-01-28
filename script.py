import yfinance as yf
import pandas as pd
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Tu lista de vigilancia (puedes añadir más)
TICKERS = ["NVDA", "TSLA", "AAPL", "AMD", "COIN", "PLTR", "MSFT", "META", "AMZN", "GOOGL"]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def analizar_accion(ticker):
    # Descargamos datos históricos
    df = yf.download(ticker, period="100d", interval="1d", progress=False)
    if len(df) < 50: return
    
    # 1. Indicador de Tendencia: Media Móvil de 50 días
    sma_50 = df['Close'].rolling(window=50).mean().iloc[-1]
    precio_actual = df['Close'].iloc[-1]
    
    # 2. Indicador de Fuerza: RSI (14 periodos)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    # 3. Volumen: Comparar hoy con la media de los últimos 20 días
    vol_actual = df['Volume'].iloc[-1]
    vol_medio = df['Volume'].rolling(window=20).mean().iloc[-1]
    
    # --- ESTRATEGIA DE COMPRA ---
    # Queremos: Precio sobre la media + RSI no muy alto + Volumen fuerte
    if precio_actual > sma_50 and rsi < 70 and vol_actual > (vol_medio * 1.3):
        
        # Gestión de Riesgo (ATR simplificado para Stop Loss)
        stop_loss = precio_actual * 0.95 # 5% de pérdida máxima
        objetivo = precio_actual * 1.15 # Buscamos un 15% de beneficio
        
        mensaje = (
            f"🎯 *OPORTUNIDAD DE COMPRA: {ticker}*\n\n"
            f"💰 *Precio:* {precio_actual:.2f}$\n"
            f"📈 *Tendencia:* Alcista (Sobre SMA50)\n"
            f"💪 *Fuerza RSI:* {rsi:.1f} (Ideal)\n"
            f"📊 *Volumen:* +30% sobre la media\n\n"
            f"🛡️ *Stop Loss Sugerido:* {stop_loss:.2f}$\n"
            f"🚀 *Objetivo:* {objetivo:.2f}$\n"
            f"⚠️ _Recuerda gestionar tu riesgo._"
        )
        enviar_telegram(mensaje)

def ejecutar():
    print("Iniciando análisis de mercado...")
    for t in TICKERS:
        analizar_accion(t)
    print("Análisis finalizado.")

if __name__ == "__main__":
    ejecutar()
    
