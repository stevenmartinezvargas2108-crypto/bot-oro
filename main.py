import websocket
import json
import telebot
from datetime import datetime
import pytz
import time

# --- CREDENCIALES ---
USER_ID = "19974476"
PASSWORD = "Coste-2108"
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"

# Intentaremos con la URL de producción (pero con tus datos demo) 
# que suele ser más estable en servidores de nube.
URL_COMANDOS = "wss://ws.xtb.com/demo" 

bot = telebot.TeleBot(TOKEN)

# --- CONFIGURACIÓN ---
ZONA_HORARIA = pytz.timezone('America/New_York')
HORA_INICIO, HORA_FIN = 8, 17
historico_precios = {"GOLD": [], "EURUSD": []}
EMA_RAPIDA, EMA_LENTA = 9, 21

def enviar_telegram(m):
    try: bot.send_message(CHAT_ID, m)
    except: pass

def es_horario():
    ahora = datetime.now(ZONA_HORARIA)
    return ahora.weekday() <= 4 and HORA_INICIO <= ahora.hour < HORA_FIN

def abrir_op(ws, sym, cmd, vol):
    if not es_horario(): return
    payload = {
        "command": "tradeTransaction",
        "arguments": {
            "tradeTransInfo": {
                "cmd": cmd, "symbol": sym, "type": 0, "volume": vol,
                "price": 0.0, "sl": 0.0, "tp": 0.0, "customComment": "Bot_Fase_Demo"
            }
        }
    }
    ws.send(json.dumps(payload))
    enviar_telegram(f"🚀 {sym}: {'BUY' if cmd==0 else 'SELL'}")

def on_message(ws, message):
    data = json.loads(message)
    if data.get("status") and "streamSessionId" in data:
        enviar_telegram("✅ BOT CONECTADO. Esperando señales...")
        # Suscripción inmediata tras login
        for s in ["GOLD", "EURUSD"]:
            ws.send(json.dumps({"command": "getTickPrices", "arguments": {"level": 0, "symbols": [s]}}))

    if "returnData" in data and "quotations" in data["returnData"]:
        for t in data["returnData"]["quotations"]:
            s, p = t.get("symbol"), t.get("ask")
            if s in historico_precios and p:
                historico_precios[s].append(p)
                if len(historico_precios[s]) > 30: historico_precios[s].pop(0)
                
                if len(historico_precios[s]) >= EMA_LENTA:
                    e9 = sum(historico_precios[s][-EMA_RAPIDA:]) / EMA_RAPIDA
                    e21 = sum(historico_precios[s][-EMA_LENTA:]) / EMA_LENTA
                    if e9 > e21: abrir_op(ws, s, 0, 0.01)
                    elif e9 < e21: abrir_op(ws, s, 1, 0.01)

def on_open(ws):
    # Pequeña pausa para asegurar que el socket esté listo
    time.sleep(1)
    ws.send(json.dumps({"command": "login", "arguments": {"userId": USER_ID, "password": PASSWORD}}))

def on_error(ws, err):
    print(f"Error detectado: {err}")

# --- EJECUCIÓN DIRECTA (Cumpliendo tus reglas de 2026-02-21) ---
ws_app = websocket.WebSocketApp(
    URL_COMANDOS,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error
)

print("Iniciando Bot...")
ws_app.run_forever()
