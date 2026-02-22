import asyncio
from metaapi_cloud_sdk import MetaApi
import telebot

# --- CONFIGURACIÓN DE CREDENCIALES ---
TOKEN_TELEGRAM = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"

# ID de la cuenta en MetaApi (sacado de tu captura)
ACCOUNT_ID = "ae97b580-a231-403d-8051-7096e5797825" 

# Tu Token de MetaApi (el código largo que ya configuraste)
TOKEN_META = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiJmMTI3ZTdlZjUzZGJmZmJmODkxYzJkYzViMTc0MjYwNSIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiZjEyN2U3ZWY1M2RiZmZiZjg5MWMyZGM1YjE3NDI2MDUiLCJpYXQiOjE3NzE3ODE5MDUsImV4cCI6MTc3OTU1NzkwNX0.If_n4d3AYl0aNLcQ7X4k2k8o00KPHusKpZpADaWflJeN9yYWNmE5zODh8AYIz7GziZ1f6PPuL5sguiSKPryRmpvppAZ6vEcgkzEcj7ZNasAwSX-NaLpQv4Yo3tI3Q8N4UMFRGuPXtNkxvEJtViorIjZsvz-8Rx3BzsmaOwUtvp1xR2l9D5BJKqUpG_tcgwFzgTYCQBRlt7AZ8iap_gxULi4zEVSegVFNLKSw6RmhlH6faOT5oakE_Pd-LR7azAkpIVkCc-0NKbmRX0mdUyWtbO2UYNJIC1oZucxHD6xP56A0af69id2wgokCfcMS7ODjMF9kiZKw2bXwMg1tIbYDh_sN-pUzD-s5DK1QvLtaMi1CFFaalSm0AXzb0d4waY4e2UEZcEM98EZn8UrY1I-gIr0Aife2aPG80dqyUz5zN8pfXRloaELTGMHOgAMOyJePSMLzm4et_ERUtNxaM6bLTrqVtsCLcdY3y1gsoyyBP6Xm_mpqEKOqXYCEeYEMgPHhP5NUny25xjEz6rC6Wc3W4bE7sDBM4e8_tmhzz3f_iWoZs6Vhh9zBjxYwLjQX-3hJp-oa-S8FmbsHZFlNjwVgnrDqYnU1-fWsIQmnF2mpfWUleTFM2AsQm0jKdv6ElPQzSa5XBky8UwJGgsXJzftdxvsavHS2mKjEFfA1FTLLGG8"

bot = telebot.TeleBot(TOKEN_TELEGRAM)

async def main():
    api = MetaApi(TOKEN_META)
    try:
        # Buscamos la cuenta específica de Exness
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        
        # IMPORTANTE: Forzamos el despliegue si está en 'Undeployed'
        if account.state != 'DEPLOYED':
            print("🚀 Iniciando servidor de MetaApi para Exness...")
            await account.deploy()
        
        print("⏳ Esperando conexión con Exness-MT5Trial11...")
        await account.wait_connected()
        
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        bot.send_message(CHAT_ID, "✅ BOT CONECTADO A EXNESS\nCuenta Demo: 198183358\nServidor: MT5Trial11")

        while True:
            # En Exness Standard, los pares suelen llevar 'm' (ej: XAUUSDm)
            for s in ["XAUUSD", "EURUSD"]:
                try:
                    tick = await connection.terminal_state.wait_tick(s, timeoutInMilliseconds=5000)
                    precio = tick['ask']
                    
                    # Estrategia Oro (XAUUSD) vs Forex
                    dist = 2.0 if "XAU" in s else 0.0010
                    sl = precio - dist
                    tp = precio + (dist * 2)

                    # Envío de orden automática de 0.01 lotes
                    await connection.create_market_buy_order(s, 0.01, sl, tp)
                    bot.send_message(CHAT_ID, f"🎯 Compra en {s}\nPrecio: {precio}\nSL: {sl:.2f} | TP: {tp:.2f}")
                    
                except Exception as e:
                    print(f"Buscando tick en {s}...")

            await asyncio.sleep(60) # Pausa para Railway

    except Exception as e:
        error_txt = f"❌ Error: {str(e)[:100]}"
        print(error_txt)
        bot.send_message(CHAT_ID, error_txt)

# Ejecución sin bloque 'name' para evitar problemas en Railway
asyncio.run(main())
