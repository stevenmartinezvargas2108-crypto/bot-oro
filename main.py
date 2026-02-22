import websocket
import json
import telebot

# Datos de tu captura verificados
USER_ID = "19974476"
PASSWORD = "Coste-2108"
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"
URL = "wss://ws.xtb.com/demo"

bot = telebot.TeleBot(TOKEN)

def enviar_telegram(m):
    try: bot.send_message(CHAT_ID, m)
    except: pass

def on_message(ws, message):
    data = json.loads(message)
    if data.get("status") and "streamSessionId" in data:
        enviar_telegram("💹 Bot de Trading Activo: Operando ORO y EURUSD.")
        # Aquí puedes añadir la lógica de compra automática que definimos
    print(f"Mensaje de XTB: {message}")

def on_open(ws):
    login = {"command": "login", "arguments": {"userId": USER_ID, "password": PASSWORD}}
    ws.send(json.dumps(login))

if _name_ == "_main_":
    try:
        ws = websocket.WebSocketApp(URL, on_open=on_open, on_message=on_message)
        ws.run_forever()
    except Exception as e:
        print(f"Error: {e}")
# Fin del programa seguro
