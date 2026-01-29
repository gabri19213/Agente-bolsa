import yfinance as yf
import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# LISTA EXPANDIDA DE MICRO-CAPS Y ACCIONES VOLÁTILES (Aproximadamente 100)
MICRO_CAPS = [
    "IREN", "WULF", "CLSK", "CIFR", "BTBT", "ANY", "SDIG", "HIVE", "CAN", # Minería/Cripto
    "ASTS", "RKLB", "LUNR", "SIDU", "LLAP", "VLD", "QUBT", "RGTI",         # Space/Quantum
    "SOUN", "BBAI", "AISP", "GFAI", "VERI", "CXAI", "TRNR", "UPST",         # IA/Software
    "MULN", "LCID", "PSNY", "NKLA", "QS", "CHPT", "BLNK", "EVGO",         # EV/Energía
    "NVAX", "BNTX", "MRNA", "SRPT", "CRSP", "EDIT", "BEAM", "NTLA",         # BioTech
    "PLUG", "FCEL", "BE", "RUN", "SPWR", "ENPH", "SEDG", "FSLR",            # Solar/H2
    "HOOD", "SOFI", "AFRM", "NU", "MQ", "AVDX", "FLYW",                     # Fintech
    "DKNG", "PENN", "RUSHB", "GENI", "BETZ",                                # Betting
    "GME", "AMC", "KOSS", "BB", "TLRY", "CGC", "ACB", "SNDL",               # Meme/Cannabis
    "RIVN", "FSRN", "JOBY", "ACHR", "EVTL", "EH",                           # Movilidad/Drones
    "S", "SENT", "PANW", "FTNT", "CRWD", "OKTA", "ZS",                      # CyberSecurity
    "U", "RBLX", "MTTR", "TTD", "SNAP", "PINS"                              # Metaverso/Ads
]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def escanear_microcaps():
    print(f"🕵️ Escaneando {len(MICRO_CAPS)} Micro-Caps...")
    
    # Descargamos los datos en un solo bloque para no ser bloqueados
    data = yf.download(MICRO_CAPS, period="2d", interval="1h", progress=False)['Close']
    
    for ticker in MICRO_CAPS:
        try:
            precios = data[ticker].dropna()
            if len(precios) < 2: continue
            
            p_actual = precios.iloc[-1]
            p_previa = precios.iloc[-2]
            variacion = ((p_actual - p_previa) / p_previa) * 100
            
            # Filtro agresivo: Avísame si sube más del 3% en UNA HORA
            if variacion > 3.0:
                mensaje = (
                    f"🧨 *EXPLOSIÓN MICRO-CAP: {ticker}*\n\n"
                    f"📈 *Movimiento 1h:* +{variacion:.2f}%\n"
                    f"💰 *Precio:* {p_actual:.2f}$\n"
                    f"🚨 _Volatilidad extrema detectada._"
                )
                enviar_telegram(mensaje)
        except:
            continue

if __name__ == "__main__":
    escanear_microcaps()
