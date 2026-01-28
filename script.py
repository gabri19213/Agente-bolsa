import requests
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def test():
    print(f"Intentando enviar mensaje a ID: {CHAT_ID}")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "¡HOLA! Si lees esto, tu bot está configurado al 100% 🚀"}
    r = requests.post(url, data=payload)
    print(f"Resultado: {r.status_code}")
    print(f"Respuesta completa: {r.text}")

if __name__ == "__main__":
    test()
    
