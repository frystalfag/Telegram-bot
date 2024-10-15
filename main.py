import telebot
import sqlite3
from telebot import types
from dir import Dir

bot = telebot.TeleBot('7870390365:AAH2U5ElAoactg7XN44zhfgJkykBtC1P1Cs')

def db_conn():
    return sqlite3.connect('DBTelegramBot.sql')

def create_tables():
    connect = db_conn()
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS User
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, XP INTEGER, Rate INTEGER, Date DATE) 
                     """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS Word
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, LWord TEXT, TWord Text, UserID INTEGER, foreign key(UserID) references User(id) ) 
                     """)

    connect.commit()
    connect.close()

create_tables()

@bot.message_handler(commands=['start'])

def start(message):
    connect = db_conn()
    cursor = connect.cursor()

    cursor.execute('Select * from User where Name=?',(message.from_user.username,))

    if not cursor.fetchone():
        cursor.execute("Insert into User (Name, Xp, Rate, Date) values (?, 0, 0, Date('now'))", (message.from_user.username,))
        connect.commit()

    connect.close()

    bot.send_message(
        message.chat.id, f'Привіт, @{message.from_user.username}! 🎮 Ласкаво просимо до '
                         f'LingvoMate — місця, де гра стає навчанням! 🚀\n\nГотовий(-а) до пригод? 🌍')

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(f'Почнемо нашу мовну подорож разом! 🧠✨', url="https://example.com")
    markup.add(button)

    bot.send_message(message.chat.id, f'🌍 Мовна подорож: відкривай нові міста та країни, виконуючи завдання на переклад слів, фраз, та граматику.\n', reply_markup=markup)

# @bot.message_handler(commands=['Add'])
bot.polling()
