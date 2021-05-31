import telebot
from telebot import types

BOT_TOKEN = "1719204229:AAFTEDBCSZSJxYmuApcVkSgjCK4NZY5wNlc"
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


def process_activity_choice(message):
    markup = types.ReplyKeyboardMarkup()
    if message.text == 'Учить слова' or 'Продолжить':
        ru = types.KeyboardButton('Русский')
        eng = types.KeyboardButton('Английский')
        markup.add(ru, eng)
        msg = bot.send_message(message.chat.id,
                               "Выбери, с какого языка будем переводить",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, learn_words)
    elif message.text == 'Вывести статистику':
        msg = bot.send_message(message.chat.id,
                               "Здесь будет статистика", reply_markup=markup)


def learn_words(message):
    if message.text == "Русский" or 'Продолжить переводить с русского':
        markup = types.ReplyKeyboardMarkup()
        back = types.KeyboardButton('Вернуться')
        forward = types.KeyboardButton('Продолжить переводить с русского')
        markup.add(back, forward)
        msg = bot.send_message(message.chat.id,
                               "Выбран русский язык",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, welcome)
    elif message.text == "Английский" or 'Продолжить переводить с английского':
        markup = types.ReplyKeyboardMarkup()
        back = types.KeyboardButton('Вернуться')
        forward = types.KeyboardButton('Продолжить переводить с английского')
        markup.add(back, forward)
        msg = bot.send_message(message.chat.id,
                               "Выбран английский язык",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, welcome)


if __name__ == '__main__':
    bot.polling(none_stop=True)
