import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Lista masiva optimizada para Trade Republic (Tech, Europa, USA, Cripto y Penny Stocks)
TICKERS = [
    "NVDA", "AAPL", "TSLA", "AMD", "MSFT", "GOOGL", "AMZN", "META", "NFLX", "PLTR", # Big Tech
    "ASML", "SAP.DE", "IFX.DE", "AIR.DE", "ATEYY", "RNECY", "SAN.MC", "ITX.MC",     # Europa y Japón
    "IREN", "ASTS", "RKLB", "LUNR", "SOUN", "BBAI", "MARA", "RIOT", "CLSK",        # Agresivas/Crecimiento
    "BTC-USD", "ETH-USD", "SOL-USD", "DOGE-USD", "PEPE-USD",                       # Cripto
    "TQQQ", "SOXL", "COIN", "MSTR", "HOOD", "PYPL", "U", "NET", "SNOW"             # Volatilidad
]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def analizar(ticker):
    try:
        # Traemos datos en intervalos de 15 min para captar el movimiento actual
        stock = yf.Ticker(ticker)
        df = stock.history(period="1d", interval="15m")
        if df.empty or len(df) < 2: return

        nombre_empresa = stock.info.get('longName', ticker)
        precio_actual = df['Close'].iloc[-1]
        precio_apertura = df['Open'].iloc[0]
        variacion = ((precio_actual - precio_apertura) / precio_apertura) * 100

        # FILTRO: Si sube más de un 3% desde que abrió hoy
        if variacion > 3.0:
            mensaje = (
                f"🚨 *ALERTA DE COMPRA EN TRADE REPUBLIC*\n\n"
                f"🏢 *Empresa:* {nombre_empresa}\n"
                f"🔑 *Ticker:* `{ticker}`\n"
                f"💰 *Precio Actual:* {precio_actual:.2f}$\n"
                f"📈 *Subida Hoy:* +{variacion:.2f}%\n\n"
                f"📱 _Búscala ahora por su nombre o ticker en la app._"
            )
            enviar_telegram(mensaje)
    except:
        pass

if __name__ == "__main__":
    # Escaneo silencioso: Solo avisa si encuentra algo, para no molestarte cada hora
    for t in TICKERS:
        analizar(t)
