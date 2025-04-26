import telebot
from telebot import types
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Тонировка")
    markup.add(btn1)
    bot.send_message(message.chat.id, "Привет! Что вас интересует?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Тонировка")
def tonirovka_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        "Тонировка в круг",
        "Тонировка задней полусферы",
        "Тонировка передней полусферы",
        "Тонировка боковых стёкол",
        "Тонировка двух передних стёкол",
        "Тонировка двух задних стёкол",
        "Тонировка одного стекла",
        "Тонировка форточки",
        "Тонировка лобового стекла",
        "Тонировка заднего стекла",
        "Тонировка козырька 14 см ГОСТ"
    ]
    for btn in buttons:
        markup.add(types.KeyboardButton(btn))
    bot.send_message(message.chat.id, "Выберите категорию тонировки:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [
    "Тонировка в круг", "Тонировка задней полусферы", "Тонировка передней полусферы",
    "Тонировка боковых стёкол", "Тонировка двух передних стёкол",
    "Тонировка двух задних стёкол", "Тонировка одного стекла",
    "Тонировка форточки", "Тонировка лобового стекла",
    "Тонировка заднего стекла", "Тонировка козырька 14 см ГОСТ"
])
def select_light(message):
    user_data[message.chat.id] = {"type": message.text}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    light_options = ["5%", "15%", "20%", "35%", "50%", "70%", "80% отормалка"]
    for option in light_options:
        markup.add(types.KeyboardButton(option))
    bot.send_message(message.chat.id, "Выберите светопропускание:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["5%", "15%", "20%", "35%", "50%", "70%", "80% отормалка"])
def ask_name(message):
    user_data[message.chat.id]["light"] = message.text
    bot.send_message(message.chat.id, "Укажите марку и год автомобиля:")

    bot.register_next_step_handler(message, ask_phone)

def ask_phone(message):
    user_data[message.chat.id]["car"] = message.text
    bot.send_message(message.chat.id, "Введите ваш номер телефона:")

    bot.register_next_step_handler(message, finish)

def finish(message):
    user_data[message.chat.id]["phone"] = message.text
    info = user_data[message.chat.id]
    text = f"""Новая заявка:
Тип тонировки: {info['type']}
Светопропускание: {info['light']}
Автомобиль: {info['car']}
Телефон: {info['phone']}"""
    bot.send_message(message.chat.id, "Спасибо! Мы свяжемся с вами!")
    # Замените YOUR_ADMIN_CHAT_ID на ваш ID, чтобы получать уведомления
    bot.send_message(YOUR_ADMIN_CHAT_ID, text)

bot.infinity_polling()
