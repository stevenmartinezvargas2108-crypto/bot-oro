import telebot

# Tu Token verificado
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
bot = telebot.TeleBot(TOKEN)

# Tu ID de chat verificado
CHAT_ID = "1243761899"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ ¡Bot conectado correctamente!")

print("🤖 El bot está intentando arrancar...")

try:
    bot.send_message(CHAT_ID, "🚀 ¡Hola! Tu robot de Railway ya despertó y está activo.")
    print("✅ Mensaje de prueba enviado a Telegram.")
except Exception as e:
    print(f"❌ Error al enviar mensaje: {e}")

bot.polling()
