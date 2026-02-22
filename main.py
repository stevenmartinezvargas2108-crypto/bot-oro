import telebot

# Tu Token que está perfecto
TOKEN = "8081063984:AAGAt736SEOvD5WPQlCieD6TguIOd_MRv6s"
bot = telebot.TeleBot(TOKEN)

print("🤖 Bot iniciado. Esperando mensaje en Telegram...")

# Este comando te dirá tu ID real cuando le escribas algo al bot
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"✅ Tu ID real es: {message.chat.id}")
    bot.reply_to(message, f"¡Hola! Recibí tu mensaje. Tu ID es: {message.chat.id}")

bot.polling()
