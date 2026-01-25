from database.db import init_db
init_db()
import json
import telebot
from config import TOKEN
from keyboards.main_keyboard import main_menu
from database.db import add_request

bot = telebot.TeleBot(TOKEN)

user_states = {}
def load_faq():
    with open("data/faq.json", "r", encoding="utf-8") as f:
        return json.load(f)

faq_data = load_faq()
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


@bot.message_handler(func=lambda message: message.text == "❓ Частые вопросы")
def show_faq(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    for question in faq_data.keys():
        keyboard.add(KeyboardButton(question))
    
    keyboard.add(KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите интересующий вас вопрос:",
        reply_markup=keyboard
    )
from keyboards.main_keyboard import main_menu


@bot.message_handler(func=lambda message: message.text == "🛠 Проблема с сайтом / оплатой")
def site_problem(message):
    user_states[message.chat.id] = "programmers"
    bot.send_message(
        message.chat.id,
        "Опишите, пожалуйста, проблему с сайтом или оплатой 🛠"
    )

@bot.message_handler(func=lambda message: message.text == "📦 Вопрос по товару")
def product_question(message):
    user_states[message.chat.id] = "sales"
    bot.send_message(
        message.chat.id,
        "Опишите, пожалуйста, ваш вопрос по товару 📦"
    )

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_request(message):
    category = user_states.get(message.chat.id)

    add_request(
        user_id=message.from_user.id,
        username=message.from_user.username,
        category=category,
        message=message.text
    )

    bot.send_message(
        message.chat.id,
        "✅ Спасибо! Ваше обращение принято.\n"
        "Наш специалист свяжется с вами при необходимости."
    )

    del user_states[message.chat.id]

@bot.message_handler(func=lambda message: message.text == "⬅️ Назад")
def back_to_menu(message):
    bot.send_message(
        message.chat.id,
        "Вы вернулись в главное меню",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: message.text in faq_data)
def answer_faq(message):
    bot.send_message(
        message.chat.id,
        faq_data[message.text]
    )

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()