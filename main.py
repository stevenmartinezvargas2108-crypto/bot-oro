import telebot
import requests

# Tu Token que verificamos que está perfecto
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
bot = telebot.TeleBot(TOKEN)

# Tu ID de chat de Telegram
CHAT_ID = "1243761899"

print("🚀 Intentando despertar al robot...")

def enviar_mensaje(mensaje):
    try:
        bot.send_message(CHAT_ID, mensaje)
        print(f"✅ Mensaje enviado: {mensaje}")
    except Exception as e:
        print(f"❌ Error al enviar a Telegram: {e}")

def iniciar_bot():
    print("🤖 El bot ahora está activo y escuchando...")
    enviar_mensaje("🚀 ¡Hola! Tu robot de XTB ya está despierto y funcionando.")

if _name_ == "_main_":
    iniciar_bot()
