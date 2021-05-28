import telebot
import requests
import os
from telebot import types

BOT_TOKEN = os.environ['TELEGRAM_TOKEN']
BOT_URL = "https://learn-english-with-me-bot.herokuapp.com/"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id,
                           "Привет, {}, давай изучать английский! С чего начнем?".format(message.from_user.first_name),
                           reply_markup=markup)
    # bot.register_next_step_handler(msg, process_num1_step)


if __name__ == '__main__':
    bot.polling(none_stop=True)
