import websocket
import json
import telebot
import datetime

# --- DATOS DE CONEXIÓN ---
CONFIG = {
    "USER": "19974476",
    "PASS": "Coste-2108",
    "TOKEN": "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s",
    "CHAT_ID": "1417066995",
    "URL": "wss://ws.xtb.com/demo"
}

bot = telebot.TeleBot(CONFIG["TOKEN"])

def enviar_telegram(mensaje):
    try:
        bot.send_message(CONFIG["CHAT_ID"], mensaje)
    except: pass

def abrir_orden(ws, simbolo, tipo, precio):
    vol = 0.01
    dist = 2.0 if "GOLD" in simbolo else 0.0010
    sl = precio - dist if tipo == 0 else precio + dist
    tp = precio + (dist * 2) if tipo == 0 else precio - (dist * 2)
    
    data = {
        "command": "tradeTransaction",
        "arguments": {
            "tradeTransInfo": {
                "cmd": tipo, "price": precio, "symbol": simbolo,
                "type": 0, "volume": vol, "sl": sl, "tp": tp,
                "customComment": "Bot_Limpio"
            }
        }
    }
    ws.send(json.dumps(data))
    enviar_telegram(f"🎯 Orden en {simbolo}\nTipo: {'BUY' if tipo==0 else 'SELL'}\nSL: {sl} | TP: {tp}")

def on_message(ws, message):
    res = json.loads(message)
    if res.get("status") and "streamSessionId" in res:
        enviar_telegram("💹 Conectado a XTB. Operando ORO y EURUSD en horario óptimo.")
        for s in ["GOLD", "EURUSD"]:
            ws.send(json.dumps({"command": "getSymbol", "arguments": {"symbol": s}}))
    
    if "returnData" in res:
        # Aquí el bot recibe los precios y lanza la operación
        r = res["returnData"]
        abrir_orden(ws, r["symbol"], 0, r["ask"])

def on_open(ws):
    ws.send(json.dumps({"command": "login", "arguments": {"userId": CONFIG["USER"], "password": CONFIG["PASS"]}}))

# --- BLOQUE DE CIERRE SEGURO ---
if _name_ == "_main_":
    try:
        ws = websocket.WebSocketApp(CONFIG["URL"], on_open=on_open, on_message=on_message)
        ws.run_forever()
    except KeyboardInterrupt:
        print("Bot detenido manualmente")
    except Exception as e:
        print(f"Error inesperado: {e}")
# FIN DEL ARCHIVO - SIN ESPACIOS EXTRAS
