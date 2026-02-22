import ssl
import json
import websocket
import time
import requests

# --- CONFIGURACIÓN ---
USER_ID = "19974476"
PASSWORD = "Coste-2108" 
TOKEN_TELEGRAM = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
ID_CHAT_TELEGRAM = "1417066995"
URL = "wss://ws.xtb.com/demo"

def enviar_telegram(mensaje):
    try:
        url_tel = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
        requests.post(url_tel, json={"chat_id": ID_CHAT_TELEGRAM, "text": mensaje}, timeout=10)
    except:
        print("Error Telegram")

def on_message(ws, message):
    data = json.loads(message)
    print("Respuesta:", message)
    if data.get("status") == True and "streamSessionId" in data:
        print("✅ CONECTADO")
        enviar_telegram("🚀 ¡Bot Online! Conexión exitosa desde la nube.")

def iniciar():
    while True:
        try:
            ws = websocket.WebSocketApp(URL,
                on_open=lambda ws: ws.send(json.dumps({
                    "command": "login", 
                    "arguments": {"userId": USER_ID, "password": PASSWORD}
                })),
                on_message=on_message)
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except:
            pass
        time.sleep(10)

# Lanzamos el bot directamente sin la línea de "name"
iniciar()
