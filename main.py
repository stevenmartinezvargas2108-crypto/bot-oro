import websocket
import json
import telebot

# --- CONFIGURACIÓN DE CREDENCIALES ---
USER_ID = "19974476"
PASSWORD = "Coste-2108"
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"
URL = "wss://ws.xtb.com/demo"

bot = telebot.TeleBot(TOKEN)

# --- MEMORIA DEL BOT (Para la estrategia) ---
# Guardamos los últimos precios para calcular el cruce
historico_precios = {"GOLD": [], "EURUSD": []}
EMA_RAPIDA = 9
EMA_LENTA = 21

def enviar_telegram(mensaje):
    try:
        bot.send_message(CHAT_ID, mensaje)
    except Exception:
        pass

def calcular_ema(precios, periodo):
    if len(precios) < periodo: return None
    return sum(precios[-periodo:]) / periodo

def abrir_operacion(ws, symbol, cmd, volume):
    # Definimos SL y TP dinámicos básicos (puedes ajustarlos)
    sl = 0.0
    tp = 0.0
    
    trade_command = {
        "command": "tradeTransaction",
        "arguments": {
            "tradeTransInfo": {
                "cmd": cmd,
                "customComment": "Estrategia_Cruce_EMA",
                "expiration": 0, "offset": 0, "order": 0,
                "price": 0.0, "sl": sl, "tp": tp,
                "symbol": symbol, "type": 0, "volume": volume
            }
        }
    }
    ws.send(json.dumps(trade_command))
    enviar_telegram(f"⚡ Cruce de Medias detectado: {'COMPRA' if cmd==0 else 'VENTA'} en {symbol}")

def on_message(ws, message):
    data = json.loads(message)
    
    # 1. Confirmación de Login
    if data.get("status") is True and "streamSessionId" in data:
        enviar_telegram("💹 Bot Online: Estrategia EMA 9/21 activada.")
    
    # 2. Procesamiento de Precios (Lógica de la estrategia)
    # Suponiendo que el servidor envía ticks en 'returnData'
    if "returnData" in data:
        resp = data["returnData"]
        symbol = resp.get("symbol")
        precio = resp.get("last") # O el precio de cierre disponible

        if symbol in historico_precios and precio:
            historico_precios[symbol].append(precio)
            # Mantener solo lo necesario para ahorrar memoria
            if len(historico_precios[symbol]) > 30:
                historico_precios[symbol].pop(0)

            # Cálculo del cruce
            ema_9 = calcular_ema(historico_precios[symbol], EMA_RAPIDA)
            ema_21 = calcular_ema(historico_precios[symbol], EMA_LENTA)

            if ema_9 and ema_21:
                # Si EMA 9 cruza hacia ARRIBA la EMA 21 -> COMPRA (cmd: 0)
                if ema_9 > ema_21 and len(historico_precios[symbol]) > 21:
                    abrir_operacion(ws, symbol, 0, 0.01)
                
                # Si EMA 9 cruza hacia ABAJO la EMA 21 -> VENTA (cmd: 1)
                elif ema_9 < ema_21 and len(historico_precios[symbol]) > 21:
                    abrir_operacion(ws, symbol, 1, 0.01)

def on_open(ws):
    login = {
        "command": "login",
        "arguments": {"userId": USER_ID, "password": PASSWORD}
    }
    ws.send(json.dumps(login))

def on_error(ws, error):
    print(f"Error: {error}")

# --- EJECUCIÓN DIRECTA (SIN LINEA DE NAME) ---
ws_app = websocket.WebSocketApp(
    URL,
    on_open=on_open,
    on_message=on_message,
    on_error=on_error
)

print("Bot iniciado correctamente.")
ws_app.run_forever()

# Fin del script de trading.
