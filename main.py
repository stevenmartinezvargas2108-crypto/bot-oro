import ssl
import json
import websocket
import time
import requests

# Credenciales cortas para evitar errores
U = "19974476"
P = "Coste-2108"
T = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
C = "1417066995"
W = "wss://ws.xtb.com/demo"

def enviar(m):
    try:
        url = f"https://api.telegram.org/bot{T}/sendMessage"
        requests.post(url, json={"chat_id": C, "text": m}, timeout=10)
    except:
        pass

def iniciar():
    while True:
        try:
            ws = websocket.WebSocketApp(W,
                on_open=lambda ws: ws.send(json.dumps({"command":"login","arguments":{"userId":U,"password":P}})),
                on_message=lambda ws, m: enviar("🚀 Bot Online en Railway"))
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except:
            pass
        time.sleep(10)

iniciar()
