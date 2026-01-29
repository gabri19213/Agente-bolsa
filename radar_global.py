import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Grupos de acciones por sectores (puedes añadir 100 más si quieres)
SECTORES = {
    "TECNOLOGÍA": ["AAPL", "MSFT", "GOOGL", "META", "AVGO", "ORCL", "ADBE", "ASML", "CSCO"],
    "SEMICONDUCTORES": ["NVDA", "AMD", "INTC", "MU", "TSM", "KLAC", "LRCX", "TXN"],
    "ENERGÍA/MINERÍA": ["XOM", "CVX", "SHEL", "BP", "RIO", "VALE", "FCX", "CCJ"],
    "BANCA/FINANZAS": ["JPM", "BAC", "GS", "MS", "V", "MA", "PYPL"],
    "CRECIMIENTO/AGRESIVAS": ["SNOW", "SHOP", "NET", "PATH", "DDOG", "ZS", "OKTA", "CRWD"]
}

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def escanear_mercado_total():
    # Unimos todos los sectores en una sola lista gigante
    todas = [ticker for sublista in SECTORES.values() for ticker in sublista]
    
    print(f"Escaneando {len(todas)} acciones globales...")
    
    # Descargamos datos de todas a la vez (más rápido)
    data = yf.download(todas, period="2d", interval="1h", progress=False)['Close']
    
    for ticker in todas:
        try:
            precios = data[ticker].dropna()
            if len(precios) < 2: continue
            
            precio_actual = precios.iloc[-1]
            precio_hace_una_hora = precios.iloc[-2]
            cambio = ((precio_actual - precio_hace_una_hora) / precio_hace_una_hora) * 100
            
            # Si sube más de un 2% EN SOLO UNA HORA, hay fuego ahí
            if cambio > 2.0:
                mensaje = (
                    f"⚠️ *DETECCIÓN INTRADÍA (1H)*\n"
                    f"💎 *Activo:* {ticker}\n"
                    f"🚀 *Subida en 1h:* +{cambio:.2f}%\n"
                    f"💰 *Precio:* {precio_actual:.2f}$\n"
                    f"⚡ _Entrando volumen fuerte ahora mismo._"
                )
                enviar_telegram(mensaje)
        except: continue

if __name__ == "__main__":
    escanear_mercado_total()
