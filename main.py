import telebot

# Tu Token verificado
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
bot = telebot.TeleBot(TOKEN)

# Tu ID de chat verificado
CHAT_ID = "1243761899"

print("🤖 Intentando conectar el robot a Telegram...")

try:
    # Mensaje de prueba al encender
    bot.send_message(CHAT_ID, "🚀 ¡Éxito! Tu robot ya está funcionando en Railway.")
    print("✅ Mensaje enviado correctamente.")
except Exception as e:
    print(f"❌ Error al enviar mensaje: {e}")

# Mantiene al bot activo
bot.polling()
