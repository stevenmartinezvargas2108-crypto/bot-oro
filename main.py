import telebot

# Tu Token verificado
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
bot = telebot.TeleBot(TOKEN)

# Tu ID de chat verificado
CHAT_ID = "1243761899"

print("🤖 El bot está intentando arrancar...")

try:
    # Esto envía un mensaje automático al encenderse
    bot.send_message(CHAT_ID, "🚀 ¡Victoria! Tu robot de Railway ya despertó y está activo.")
    print("✅ Mensaje enviado a Telegram correctamente.")
except Exception as e:
    print(f"❌ Error al enviar mensaje: {e}")

# Mantiene al bot escuchando mensajes
bot.polling()
