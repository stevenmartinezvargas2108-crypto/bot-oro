# -- coding: utf-8 --
import websocket, json, ssl, time, requests

# Datos de conexión
U, P = "19974476", "Coste-2108"
T = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
C, W = "1417066995", "wss://ws.xtb.com/demo"

while True:
    try:
        # Abrir conexión
        ws = websocket.create_connection(W, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps({"command": "login", "arguments": {"userId": U, "password": P}}))
        
        # Enviar aviso de encendido
        requests.post(f"https://api.telegram.org/bot{T}/sendMessage", json={"chat_id": C, "text": "🚀 BOT ORO ONLINE"})
        
        # Mantener conexión viva
        while True:
            ws.recv()
            
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
