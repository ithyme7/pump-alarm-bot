import os 
import telebot 

BOT_TOKEN = os.environ.get('8073616851:AAFqfGN9G1glAs9Bm5VzBeq7kVrVlT2yhi8') 

bot = telebot.TeleBot(8073616851:AAFqfGN9G1glAs9Bm5VzBeq7kVrVlT2yhi8)”

@bot.message_handler(commands=['start', 'hello']) 
def send_welcome(message): bot.reply_to(message, "Hi there. What’s happening?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message): bot.reply_to(message, message.text)