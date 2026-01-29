import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Lista optimizada (he quitado las que dan error como PEPE para limpiar el log)
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

def escanear():
    print(f"🕵️ Iniciando radar sobre {len(MICRO_CAPS)} activos...")
    try:
        # Descarga masiva (mucho más rápido)
        data = yf.download(MICRO_CAPS, period="2d", interval="1h", progress=False)['Close']
        alertas_enviadas = 0

        for ticker in MICRO_CAPS:
            if ticker not in data: continue
            precios = data[ticker].dropna()
            if len(precios) < 2: continue
            
            p_actual = precios.iloc[-1]
            p_previa = precios.iloc[-2]
            variacion = ((p_actual - p_previa) / p_previa) * 100
            
            # Bajamos el filtro al 1.5% para que sea más fácil que te avise ahora
            if variacion > 1.5:
                enviar_telegram(f"🧨 *MICRO-CAP:* {ticker}\n📈 *Subida 1h:* +{variacion:.2f}%\n💰 *Precio:* {p_actual:.2f}$")
                alertas_enviadas += 1

        # MENSAJE DE CONTROL (Para que sepas que ha terminado)
        if alertas_enviadas == 0:
            print("Escaneo finalizado sin alertas.")
            # Descomenta la línea de abajo si quieres que te avise aunque no encuentre nada:
            # enviar_telegram("✅ Escaneo completado. Mercado tranquilo.")
        else:
            print(f"Escaneo finalizado. {alertas_enviadas} alertas enviadas.")

    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    escanear()
    
