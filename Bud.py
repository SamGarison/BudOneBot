import telebot
from telebot import types
import random

import os
bot = telebot.TeleBot(os.getenv("7721997031:AAHorBkDPu4thdaaN5iRHB_b0ipH_Q1LC9k"))

user_language = {}  # словарь, где храним язык для каждого пользователя

# Ответы в стиле магического шара
answers = {
    "ru": [
        "Бесспорно", "Скорее всего", "Возможно", "Спроси позже",
        "Не рассчитывай на это", "Нет", "Определённо да", "Очень сомневаюсь"
    ],
    "pt": [
        "Sem dúvida", "Provavelmente", "Talvez", "Pergunte mais tarde",
        "Não conte com isso", "Não", "Definitivamente sim", "Duvido muito"
    ]
}

# Обработка /start и выбор языка
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🇷🇺 Русский")
    btn2 = types.KeyboardButton("🇧🇷 Português")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выбери язык / Escolha o idioma:", reply_markup=markup)

# Обработка выбора языка
@bot.message_handler(func=lambda message: message.text in ["🇷🇺 Русский", "🇧🇷 Português"])
def set_language(message):
    lang = "ru" if "Русский" in message.text else "pt"
    user_language[message.chat.id] = lang
    greeting = "Задай мне вопрос, и я отвечу ✨" if lang == "ru" else "Faça-me uma pergunta e eu responderei ✨"
    bot.send_message(message.chat.id, greeting, reply_markup=types.ReplyKeyboardRemove())

# Ответ на любое сообщение после выбора языка
@bot.message_handler(func=lambda message: True)
def magic_ball_response(message):
    lang = user_language.get(message.chat.id)
    if not lang:
        start_message(message)
        return
    response = random.choice(answers[lang])
    bot.send_message(message.chat.id, response)

# Запуск бота
bot.polling()
