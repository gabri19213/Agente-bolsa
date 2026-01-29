import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Grupos de acciones por sectores (Estas están casi todas en Trade Republic)
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

def obtener_nombre_completo(ticker):
    try:
        # Buscamos el nombre largo de la empresa
        info = yf.Ticker(ticker).info
        return info.get('longName', ticker)
    except:
        return ticker

def escanear_mercado_total():
    # Creamos un mapa para saber a qué sector pertenece cada ticker
    ticker_to_sector = {ticker: sector for sector, tickers in SECTORES.items() for ticker in tickers}
    todas = list(ticker_to_sector.keys())
    
    print(f"Escaneando {len(todas)} acciones globales...")
    
    # Descargamos datos (Close)
    data = yf.download(todas, period="2d", interval="1h", progress=False)['Close']
    
    for ticker in todas:
        try:
            precios = data[ticker].dropna()
            if len(precios) < 2: continue
            
            precio_actual = precios.iloc[-1]
            precio_hace_una_hora = precios.iloc[-2]
            cambio = ((precio_actual - precio_hace_una_hora) / precio_hace_una_hora) * 100
            
            # Filtro: Subida mayor al 2% en una hora
            if cambio > 2.0:
                nombre_real = obtener_nombre_completo(ticker)
                sector_real = ticker_to_sector.get(ticker, "General")
                
                mensaje = (
                    f"⚠️ *DETECCIÓN INTRADÍA (1H)*\n\n"
                    f"🏢 *Empresa:* {nombre_real}\n"
                    f"🆔 *Ticker:* `{ticker}` (Búscalo así en Trade Republic)\n"
                    f"📁 *Sector:* {sector_real}\n"
                    f"🚀 *Subida 1h:* +{cambio:.2f}%\n"
                    f"💰 *Precio:* {precio_actual:.2f}$\n\n"
                    f"⚡ _Volumen fuerte detectado. Revisa la tendencia._"
                )
                enviar_telegram(mensaje)
                print(f"Alerta enviada para {ticker}")
        except Exception as e:
            print(f"Error con {ticker}: {e}")
            continue

if __name__ == "__main__":
    escanear_mercado_total()
    
