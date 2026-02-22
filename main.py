import websocket, json, ssl, time, requests

# 1. Configuración
U = "19974476"
P = "Coste-2108"
T = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
C = "1417066995"
W = "wss://ws.xtb.com/demo"

print("Iniciando Bot...")

# 2. Bucle de conexión
while True:
    try:
        ws = websocket.create_connection(W, sslopt={"cert_reqs": ssl.CERT_NONE})
        login = {"command": "login", "arguments": {"userId": U, "password": P}}
        ws.send(json.dumps(login))
        
        # Si llega aquí, enviar mensaje a Telegram
        requests.post(f"https://api.telegram.org/bot{T}/sendMessage", json={"chat_id": C, "text": "🚀 Bot Oro Online"})
        
        while True:
            result = ws.recv()
            print(result)
            
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
