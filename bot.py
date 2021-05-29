import telebot
from telebot import types

BOT_TOKEN = "1719204229:AAFTEDBCSZSJxYmuApcVkSgjCK4NZY5wNlc"
BOT_URL = "https://learn-english-with-me-bot.herokuapp.com/"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(["Учить слова", "Вывести статистику"])
    words = types.InlineKeyboardButton('Учить слова', callback_data='1')
    statistics = types.InlineKeyboardButton('Вывести статистику', callback_data='2')
    markup.add(words, statistics)
    msg = bot.send_message(message.chat.id,
                           "Привет, {}! Давай изучать английский! С чего начнем?".format(message.from_user.first_name),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, process_activity_choice)


def process_activity_choice(message):
    if message.text == '1':
        bot.reply_to(message, "Здесь мы выбираем активность 1")
    else:
        bot.reply_to(message, "Здесь мы выбираем активность 2")


if __name__ == '__main__':
    bot.polling(none_stop=True)
