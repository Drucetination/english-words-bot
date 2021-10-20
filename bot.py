import telebot
from telebot import types

BOT_TOKEN = "1700397980:AAG_jUlxPxHhLgqxB6bS24bPtcxGx7WFWbk"
BOT_URL = "https://learn-english-with-me-bot.herokuapp.com/"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    words = types.KeyboardButton('Учить слова')
    statistics = types.KeyboardButton('Вывести статистику')
    markup.add(words, statistics)
    msg = bot.send_message(message.chat.id,
                           "Привет, {}! Давай изучать английский! С чего начнем?".format(message.from_user.first_name),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, process_activity_choice)


def learn(message):
    markup = types.ReplyKeyboardMarkup()
    ru = types.KeyboardButton('Русский')
    eng = types.KeyboardButton('Английский')
    markup.add(ru, eng)
    msg = bot.send_message(message.chat.id,
                           "Выбери, с какого языка будем переводить",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, learn_words)


def statistics(message):
    msg = bot.send_message(message.chat.id,
                           "Здесь будет статистика")
    bot.register_next_step_handler(msg, welcome)


def process_activity_choice(message):
    if message.text == ('Учить слова' or 'Продолжить'):
        learn(message)
    elif message.text == 'Вывести статистику':
        statistics(message)


def english_to_russian(message):
    markup = types.ReplyKeyboardMarkup()
    back = types.KeyboardButton('Вернуться')
    forward = types.KeyboardButton('Продолжить переводить с английского')
    markup.add(back, forward)
    msg = bot.send_message(message.chat.id,
                           "Выбран английский язык",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, welcome)


def russian_to_english(message):
    markup = types.ReplyKeyboardMarkup()
    back = types.KeyboardButton('Вернуться')
    forward = types.KeyboardButton('Продолжить переводить с русского')
    markup.add(back, forward)
    msg = bot.send_message(message.chat.id,
                           "Выбран русский язык",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, welcome)


def learn_words(message):
    if message.text == ("Английский" or 'Продолжить переводить с английского'):
        english_to_russian(message)
    elif message.text == "Русский" or 'Продолжить переводить с русского':
        russian_to_english(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
