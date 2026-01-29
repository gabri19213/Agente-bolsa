import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Lista de Micro-Caps y activos volátiles
MICRO_CAPS = [
    "IREN", "WULF", "CLSK", "CIFR", "BTBT", "HIVE", "CAN",
    "ASTS", "RKLB", "LUNR", "SIDU", "QUBT", "RGTI",
    "SOUN", "BBAI", "AISP", "GFAI", "UPST",
    "MULN", "LCID", "NKLA", "QS", "CHPT",
    "PLUG", "FCEL", "BE", "RUN", "ENPH",
    "HOOD", "SOFI", "AFRM", "NU",
    "GME", "AMC", "TLRY", "CGC",
    "BTC-USD", "ETH-USD", "SOL-USD"
]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def obtener_nombre_detallado(ticker):
    try:
        t = yf.Ticker(ticker)
        # Intentamos sacar el nombre largo, si falla, devolvemos el ticker
        return t.info.get('longName', ticker)
    except:
        return ticker

def escanear():
    print(f"🕵️ Iniciando radar sobre {len(MICRO_CAPS)} activos...")
    try:
        # Descarga masiva para mayor velocidad
        data = yf.download(MICRO_CAPS, period="2d", interval="1h", progress=False)['Close']
        alertas_enviadas = 0

        for ticker in MICRO_CAPS:
            if ticker not in data: continue
            precios = data[ticker].dropna()
            if len(precios) < 2: continue
            
            p_actual = precios.iloc[-1]
            p_previa = precios.iloc[-2]
            variacion = ((p_actual - p_previa) / p_previa) * 100
            
            # Filtro: 1.5% de subida en la última hora
            if variacion > 1.5:
                nombre_real = obtener_nombre_detallado(ticker)
                
                mensaje = (
                    f"🧨 *ALERTA MICRO-CAP (1H)*\n\n"
                    f"🏢 *Empresa:* {nombre_real}\n"
                    f"🆔 *Ticker:* `{ticker}`\n"
                    f"📈 *Subida 1h:* +{variacion:.2f}%\n"
                    f"💰 *Precio:* {p_actual:.2f}$\n\n"
                    f"🚀 _Movimiento agresivo detectado. ¡Ojo!_"
                )
                enviar_telegram(mensaje)
                alertas_enviadas += 1

        print(f"Escaneo finalizado. {alertas_enviadas} alertas enviadas.")

    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    escanear()
