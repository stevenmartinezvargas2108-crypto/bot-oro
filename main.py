import websocket, json, ssl, time, requests

U = "19974476"
P = "Coste-2108"
T = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
C = "1417066995"
W = "wss://ws.xtb.com/demo"

while True:
    try:
        ws = websocket.create_connection(W, sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.send(json.dumps({"command": "login", "arguments": {"userId": U, "password": P}}))
        requests.post(f"https://api.telegram.org/bot{T}/sendMessage", json={"chat_id": C, "text": "🚀 BOT ACTIVO"})
        while True:
            ws.recv()
    except:
        time.sleep(10)

