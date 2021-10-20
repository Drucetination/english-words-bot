import telebot
from telebot import types
import redis
from urllib.parse import urlparse
from random import shuffle

BOT_TOKEN = "1700397980:AAG_jUlxPxHhLgqxB6bS24bPtcxGx7WFWbk"
BOT_URL = "https://learn-english-with-me-bot.herokuapp.com/"

url = urlparse(
    "redis://:pf202c59bbb3e296e1e073559d07e643a73a9232d08f76f0b6fa99abcf8604c91@ec2-46-137-24-228.eu-west-1.compute.amazonaws.com:24520")
r = redis.Redis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True,
                ssl_cert_reqs=None)
exercise = []

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


def learn_words(message):
    if message.text == 'Русский':
        process_r2e(message)
    else:
        process_e2r(message)


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
    bot.register_next_step_handler(msg, process_e2r)


def back_to_start(message):
    bot.register_next_step_handler(message, welcome)


def next_e2r_exercise(message):
    english_word = r.randomkey().decode('utf8', errors='ignore')
    russian_word = r.get(english_word).decode('utf8', errors='ignore')
    exercise.extend([english_word, russian_word])
    msg = bot.send_message(message.chat.id,
                           "Переведи на русский {}".format(english_word))
    bot.register_next_step_handler(msg, e2r_exercise)


def process_e2r(message):
    if message.text == "Вернуться":
        back_to_start(message)
    else:
        next_e2r_exercise(message)


def e2r_exercise(message):
    rw = types.KeyboardButton(exercise[1])
    fake_english_word_1 = r.randomkey().decode('utf8', errors='ignore')
    frw_1 = types.KeyboardButton(r.get(fake_english_word_1).decode('utf8', errors='ignore'))
    fake_english_word_2 = r.randomkey().decode('utf8', errors='ignore')
    frw_2 = types.KeyboardButton(r.get(fake_english_word_2).decode('utf8', errors='ignore'))
    markup = types.ReplyKeyboardMarkup()
    for word in shuffle([rw, frw_1, frw_2]):
        markup.add(word)
    msg = bot.send_message(message.chat.id,
                           "Проверка ответа...",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, check_answer_e2r)


def correct_e2r(message):
    msg = bot.send_message(message.chat.id,
                           "Ура, правильно!")
    bot.register_next_step_handler(msg, english_to_russian)


def wrong_e2r(message):
    msg = bot.send_message(message.chat.id,
                           "Неверно!")
    bot.register_next_step_handler(msg, english_to_russian)


def check_answer_e2r(message):
    if message.text == exercise[1]:
        correct_e2r(message)
    else:
        wrong_e2r(message)


def russian_to_english(message):
    markup = types.ReplyKeyboardMarkup()
    back = types.KeyboardButton('Вернуться')
    forward = types.KeyboardButton('Продолжить переводить с русского')
    markup.add(back, forward)
    msg = bot.send_message(message.chat.id,
                           "Выбран русский язык",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, process_r2e)


def next_r2e_exercise(message):
    english_word = r.randomkey().decode('utf8', errors='ignore')
    russian_word = r.get(english_word).decode('utf8', errors='ignore')
    exercise.extend([english_word, russian_word])
    msg = bot.send_message(message.chat.id,
                           "Переведи на английский: {}".format(russian_word))
    bot.register_next_step_handler(message, r2e_exercise)


def process_r2e(message):
    if message.text == "Вернуться":
        back_to_start(message)
    else:
        next_r2e_exercise(message)


def r2e_exercise(message):
    ew = types.KeyboardButton(exercise[0])
    few_1 = types.KeyboardButton(r.randomkey().decode('utf8', errors='ignore'))
    few_2 = types.KeyboardButton(r.randomkey().decode('utf8', errors='ignore'))
    markup = types.ReplyKeyboardMarkup()
    for word in shuffle([ew, few_1, few_2]):
        markup.add(word)
    msg = bot.send_message(message.chat.id,
                           "Проверка ответа...",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, check_answer_r2e)


def correct_r2e(message):
    msg = bot.send_message(message.chat.id,
                           "Ура, правильно!")
    bot.register_next_step_handler(msg, russian_to_english)


def wrong_r2e(message):
    msg = bot.send_message(message.chat.id,
                           "Неверно!")
    bot.register_next_step_handler(msg, russian_to_english)


def check_answer_r2e(message):
    if message.text == exercise[0]:
        correct_r2e(message)
    else:
        wrong_r2e(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
