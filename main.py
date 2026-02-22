import asyncio
from metaapi_cloud_sdk import MetaApi
import pandas as pd
import telebot
from datetime import datetime
import pytz

# --- CONFIGURACIÓN ---
TOKEN_MT = "TU_TOKEN_DE_METAAPI" # Necesitas generar uno en metaapi.cloud
ACCOUNT_ID = "5046933255" # Tu Login

TOKEN_TG = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
CHAT_ID = "1417066995"
bot = telebot.TeleBot(TOKEN_TG)

ZONA_HORARIA = pytz.timezone('America/New_York')
SIMBOLOS = ["GOLD", "EURUSD"]

async def ejecutar_bot():
    api = MetaApi(TOKEN_MT)
    try:
        account = await api.metatrader_account_api.get_account(ACCOUNT_ID)
        connection = account.get_streaming_connection()
        await connection.connect()
        await connection.wait_synchronized()
        
        bot.send_message(CHAT_ID, "✅ Bot en Linux conectado exitosamente via MetaApi")

        while True:
            ahora = datetime.now(ZONA_HORARIA)
            if ahora.weekday() <= 4 and 8 <= ahora.hour < 17:
                for s in SIMBOLOS:
                    # Lógica de EMA 9/21 aquí
                    pass
            await asyncio.sleep(60)
            
    except Exception as e:
        print(f"Error: {e}")

# Iniciar el proceso
asyncio.run(ejecutar_bot())
