import websocket
import json
import telebot
from datetime import datetime
import pytz

# --- CONFIGURACIÓN DE CREDENCIALES ---
USER_ID = "19974476"
PASSWORD = "Coste-2108"
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"
URL_COMANDOS = "wss://ws.xtb.com/demo"

bot = telebot.TeleBot(TOKEN)

# --- CONFIGURACIÓN DE HORARIO (Temporizador) ---
# Definimos la zona horaria (ejemplo: Nueva York o Madrid)
ZONA_HORARIA = pytz.timezone('America/New_York')
HORA_INICIO = 8  # 8:00 AM
HORA_FIN = 17    # 5:00 PM

# --- MEMORIA DEL BOT (Estrategia EMA 9/21) ---
historico_precios = {"GOLD": [], "EURUSD": []}
EMA_RAPIDA = 9
EMA_LENTA = 21

def enviar_telegram(mensaje):
    try:
        bot.send_message(CHAT_ID, mensaje)
    except Exception:
        pass

def es_horario_operativo():
    """Verifica si la hora actual está dentro del rango permitido."""
    ahora = datetime.now(ZONA_HORARIA)
    # Solo opera de lunes (0) a viernes (4)
    if ahora.weekday() > 4:
        return False
    return HORA_INICIO <= ahora.hour < HORA_FIN

def calcular_ema(precios, periodo):
    if len(precios) < periodo: return None
    return sum(precios[-periodo:]) / periodo

def abrir_operacion(ws, symbol, cmd, volume):
    # Verificación del temporizador antes de disparar la orden
    if not es_horario_operativo():
        print(f"Señal detectada en {symbol}, pero fuera de horario operativo.")
        return

    trade_command = {
        "command": "tradeTransaction",
        "arguments": {
            "tradeTransInfo": {
                "cmd": cmd,
                "customComment": "Estrategia_EMA_Timer",
                "expiration": 0, "offset": 0, "order": 0,
                "price": 0.0, "sl": 0.0, "tp": 0.0,
                "symbol": symbol, "type": 0, "volume": volume
            }
        }
    }
    try:
        ws.send(json.dumps(trade_command))
        enviar_telegram(f"🚀 Ejecutada {symbol} en horario: {'COMPRA' if cmd==0 else 'VENTA'}")
    except Exception as e:
        print(f"Error al enviar orden: {e}")

def suscribir_a_precios(ws):
    for activo in ["GOLD", "EURUSD"]:
        msg = {
            "command": "getTickPrices",
            "arguments": {"level": 0, "symbols": [activo], "timestamp": 0}
        }
        ws.send(json.dumps(msg))
    enviar_telegram("📡 Temporizador Activo: Analizando flujo de precios...")

def on_message(ws, message):
    data = json.loads(message)
    
    if data.get("status") is True and "streamSessionId" in data:
        enviar_telegram("✅ Login exitoso. Temporizador configurado (NY Time).")
        suscribir_a_precios(ws)
    
    if "returnData" in data:
        ticks = data["returnData"].get("quotations", [])
        for tick in ticks:
            symbol = tick.get("symbol")
            precio = tick.get("ask")
            
            if symbol in historico_precios and precio:
                historico_precios[symbol].append(precio)
                if len(historico_precios[symbol]) > 30:
                    historico_precios[symbol].pop(0)

                ema9 = calcular_ema(historico_precios[symbol], EMA_RAPIDA)
                ema21 = calcular_ema(historico_precios[symbol], EMA_LENTA)

                if ema9 and ema21:
                    if ema9 > ema21 and len(historico_precios[symbol]) >= 22:
                         abrir_operacion(ws, symbol, 0, 0.01)
                    elif ema9 < ema21 and len(historico_precios[symbol]) >= 22:
                         abrir_operacion(ws, symbol, 1, 0.01)

def on_open(ws):
    login = {"command": "login", "arguments": {"userId": USER_ID, "password": PASSWORD}}
    ws.send(json.dumps(login))

def on_error(ws, error):
    print(f"Error: {error}")

# --- EJECUCIÓN DIRECTA (SIN LINEA NAME) ---
ws_app = websocket.WebSocketApp(
    URL_COMANDOS,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error
)

print("Bot con Temporizador iniciado...")
ws_app.run_forever()
