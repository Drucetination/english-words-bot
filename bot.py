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
    if message.text == 'Учить слова':
        markup = types.ReplyKeyboardMarkup()
        ru = types.KeyboardButton('Русский')
        eng = types.KeyboardButton('Английский')
        msg = bot.send_message(message.chat.id,
                               "Выбери, с какого языка будем переводить",
                               reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id,
                               "Здесь будет статистика")


if __name__ == '__main__':
    bot.polling(none_stop=True)
