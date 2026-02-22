import asyncio
from metaapi_cloud_sdk import MetaApi
import telebot

# --- CONFIGURACIÓN ---
TOKEN_TELEGRAM = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"
# El token JWT que me pasaste de MetaApi
TOKEN_META = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJmMTI3ZTdlZjUzZGJmZmJmODkxYzJkYzViMTc0MjYwNSIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiw6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdl_ERUtNxaM6bLTrqVtsCLcdY3y1gsoyyBP6Xm_mpqEKOqXYCEeYEMgPHhP5NUny25xjEz6rC6Wc3W4bE7sDBM4e8_tmhzz3f_iWoZs6Vhh9zBjxYwLjQX-3hJp-oa-S8FmbsHZFlNjwVgnrDqYnU1-fWsIQmnF2mpfWUleTFM2AsQm0jKdv6ElPQzSa5XBky8UwJGgsXJzftdxvsavHS2mKjEFfA1FTLLGG8"

bot = telebot.TeleBot(TOKEN_TELEGRAM)

async def ejecutar_estrategia():
    api = MetaApi(TOKEN_META)
    try:
        # 1. Conexión a la cuenta
        accounts = await api.metatrader_account_api.get_accounts()
        if not accounts:
            print("No se encontraron cuentas en MetaApi. Regístrala en su web primero.")
            return
        
        account = accounts[0]
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        bot.send_message(CHAT_ID, f"✅ Robot MT5 Online\nCuenta: {account.name}\nAnalizando ORO y EURUSD...")

        # 2. Lógica de Riesgo y Operación
        # Símbolos: "GOLD" (o "XAUUSD") y "EURUSD"
        for symbol in ["GOLD", "EURUSD"]:
            # Obtener precio actual
            price_info = await connection.terminal_state.wait_tick(symbol)
            price = price_info['ask']
            
            # Gestión de Riesgo: Stop Loss y Take Profit
            distancia = 2.0 if "GOLD" in symbol else 0.0010
            sl = price - distancia
            tp = price + (distancia * 2)

            # 3. Ejecutar Compra Automática (Market Order)
            result = await connection.create_market_buy_order(symbol, 0.01, sl, tp)
            bot.send_message(CHAT_ID, f"🚀 Compra ejecutada en {symbol}\nPrecio: {price}\nSL: {sl} | TP: {tp}")

    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(CHAT_ID, f"❌ Error en MT5: {str(e)[:100]}")

if _name_ == "_main_":
    asyncio.run(ejecutar_estrategia())
# FIN DEL ARCHIVO - SIN LINEAS EXTRAS
