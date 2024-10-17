import telebot
import sqlite3
from telebot import types
from dir import words
import random

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

@bot.message_handler(commands=['play'])
def start_game(message):
    english_word, ukrainian_translation = random.choice(list(words.items()))
    bot.send_message(message.chat.id, f"Переклади це слово: *{english_word}* з англійської на українську!", parse_mode='Markdown')
    bot.register_next_step_handler(message, check_translation, english_word, ukrainian_translation)


def check_translation(message, english_word, ukrainian_translation):
    user_answer = message.text.strip().lower()

    if user_answer == ukrainian_translation:
        bot.send_message(message.chat.id, "✅ Правильно! Ти молодець!")
        add_xp(message.from_user.username, 10)
    else:
        bot.send_message(message.chat.id, f"❌ Неправильно. Правильна відповідь: *{ukrainian_translation}*.", parse_mode='Markdown')

def add_xp(username, xp):
    connect = db_conn()
    cursor = connect.cursor()

    cursor.execute('SELECT * FROM User WHERE Name=?', (username,))
    user = cursor.fetchone()

    if user:
        new_xp = user[2] + xp
        cursor.execute('UPDATE User SET XP=? WHERE Name=?', (new_xp, username))
        connect.commit()

    connect.close()

# @bot.message_handler(commands=['Add'])
bot.polling()
