import telebot
from telebot import types

BOT_TOKEN = "1719204229:AAFTEDBCSZSJxYmuApcVkSgjCK4NZY5wNlc"
BOT_URL = "https://learn-english-with-me-bot.herokuapp.com/"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id,
                           "Привет, {}! Давай изучать английский! С чего начнем?".format(message.from_user.first_name),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, choose_activity)


def choose_activity(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        words = types.KeyboardButton('Учить слова')
        statistics = types.KeyboardButton('Вывести статистику')
        markup.add(words, statistics)

        msg = bot.send_message(message.chat.id, "Выбери активность", reply_markup=markup)
        bot.register_next_step_handler(msg, process_activity_choice)
    except Exception as e:
        bot.reply_to(message, "Выбери одну из предложенных активностей")


def process_activity_choice(message):
    bot.reply_to(message, "Здесь мы выбираем активность")


if __name__ == '__main__':
    bot.polling(none_stop=True)
