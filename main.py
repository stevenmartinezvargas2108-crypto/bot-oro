import MetaTrader5 as mt5
import pandas as pd
import telebot
from datetime import datetime
import pytz
import time

# --- CREDENCIALES ACTUALIZADAS ---
CUENTA_MT5 = 5046933255
PASSWORD_MT5 = "VmV*Fn2j"
SERVIDOR_MT5 = "MetaQuotes-Demo"

TOKEN_TELEGRAM = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"
bot = telebot.TeleBot(TOKEN_TELEGRAM)

# Parámetros Estrategia
SIMBOLOS = ["GOLD", "EURUSD"]
EMA_RAPIDA, EMA_LENTA = 9, 21
LOTE = 0.01

# Temporizador NY
ZONA_HORARIA = pytz.timezone('America/New_York')
HORA_INICIO, HORA_FIN = 8, 17

def enviar_telegram(m):
    try: bot.send_message(CHAT_ID, m)
    except: pass

def es_horario():
    ahora = datetime.now(ZONA_HORARIA)
    return ahora.weekday() <= 4 and HORA_INICIO <= ahora.hour < HORA_FIN

def abrir_op(symbol, tipo):
    tick = mt5.symbol_info_tick(symbol)
    precio = tick.ask if tipo == mt5.ORDER_TYPE_BUY else tick.bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": LOTE,
        "type": tipo,
        "price": precio,
        "magic": 202602,
        "comment": "Bot_EMA_Final",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    res = mt5.order_send(request)
    if res.retcode == mt5.TRADE_RETCODE_DONE:
        enviar_telegram(f"🚀 MT5 {symbol}: {'BUY' if tipo==0 else 'SELL'}")

# --- INICIO ---
print("Conectando a MT5...")
if not mt5.initialize(login=CUENTA_MT5, server=SERVIDOR_MT5, password=PASSWORD_MT5):
    print("Error:", mt5.last_error())
    quit()

enviar_telegram("✅ Bot MT5 Conectado. Monitoreando Oro y EURUSD.")

while True:
    if es_horario():
        for s in SIMBOLOS:
            velas = mt5.copy_rates_from_pos(s, mt5.TIMEFRAME_M1, 0, 30)
            if velas is not None and len(velas) >= EMA_LENTA:
                df = pd.DataFrame(velas)
                df['ema9'] = df['close'].ewm(span=EMA_RAPIDA).mean()
                df['ema21'] = df['close'].ewm(span=EMA_LENTA).mean()
                
                # Detectar cruce
                if df['ema9'].iloc[-1] > df['ema21'].iloc[-1] and df['ema9'].iloc[-2] <= df['ema21'].iloc[-2]:
                    abrir_op(s, mt5.ORDER_TYPE_BUY)
                elif df['ema9'].iloc[-1] < df['ema21'].iloc[-1] and df['ema9'].iloc[-2] >= df['ema21'].iloc[-2]:
                    abrir_op(s, mt5.ORDER_TYPE_SELL)
    time.sleep(60)
