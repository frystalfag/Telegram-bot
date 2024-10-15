import telebot
import sqlite3
from telebot import types
from dir import dir

bot = telebot.TeleBot('7870390365:AAH2U5ElAoactg7XN44zhfgJkykBtC1P1Cs')

@bot.message_handler(commands=['start'])

def start(message):
    connect = sqlite3.connect('DBTelegramBot.sql')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS User
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, XP INTEGER, Rate INTEGER, Date DATE, UDictionary) 
                 """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS Word
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, LWord TEXT, TWord Text, UserID INTEGER, foreign key(UserID) refernces User(id) ) 
                 """)

    bot.send_message(
        message.chat.id, f'Привіт, @{message.from_user.username}! 🎮 Ласкаво просимо до '
                         f'LingvoMate — місця, де гра стає навчанням! 🚀\n\nГотовий(-а) до пригод? 🌍')

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(f'Почнемо нашу мовну подорож разом! 🧠✨', url="https://example.com")
    markup.add(button)

    bot.send_message(message.chat.id, f'🌍 Мовна подорож: відкривай нові міста та країни, виконуючи завдання на переклад слів, фраз, та граматику.\n', reply_markup=markup)

bot.polling()
