from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("❓ Частые вопросы"),
        KeyboardButton("🛠 Проблема с сайтом / оплатой")
    )
    keyboard.add(
        KeyboardButton("📦 Вопрос по товару")
    )
    return keyboard