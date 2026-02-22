import ssl, json, websocket, time, requests

USER_ID = "19974476"
PASSWORD = "Coste-2108" 
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"
URL = "wss://ws.xtb.com/demo"

def enviar(m):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": m})
    except: pass

def on_message(ws, msg):
    data = json.loads(msg)
    if data.get("status") == True:
        enviar("🚀 ¡Bot Online en Railway! Vigilando el Oro.")

def iniciar():
    while True:
        try:
            ws = websocket.WebSocketApp(URL,
                on_open=lambda ws: ws.send(json.dumps({"command": "login", "arguments": {"userId": USER_ID, "password": PASSWORD}})),
                on_message=on_message)
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        except: pass
        time.sleep(10)

iniciar()
