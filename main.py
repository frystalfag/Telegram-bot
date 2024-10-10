import telebot

bot = telebot.TeleBot('7870390365:AAH2U5ElAoactg7XN44zhfgJkykBtC1P1Cs')

@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.chat.id, 'Hello, Я LingvoMate')

bot.polling()
