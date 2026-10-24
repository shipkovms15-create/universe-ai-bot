import sqlite3
import random
import string
import telebot
from telebot import types, apihelper

# Подключаем твой TGWS Proxy по адресу из скриншота (порт 1443)
apihelper.proxy = {
    'http': 'socks5://127.0.0.1:1443',
    'https': 'socks5://127.0.0.1:1443'
}

# === НАСТРОЙКИ БОТА ===
TOKEN = "8819038212:AAGkO3hJVNMON-j4ynZ31Khr8LhGjXrykr8"
ADMIN_ID = 8540585927
CREATOR_USERNAME = "@molodoypacanzatazit"

bot = telebot.TeleBot(TOKEN)

# Автоматически создаем базу данных SQLite для хранения ключей
def init_db():
    conn = sqlite3.connect("universe_system.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS keys (
        key_code TEXT PRIMARY KEY, 
        status TEXT DEFAULT "FREE"
    )''')
    conn.commit()
    conn.close()

# Генерация серийного номера подписки
def generate_serial():
    chars = string.ascii_uppercase + string.digits
    return "UNIVERSE-" + "".join(random.choice(chars) for _ in range(4)) + "-" + "".join(random.choice(chars) for _ in range(4))

@bot.message_handler(commands=['start'])
def start_cmd(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🌌 О софте Universe AI"), types.KeyboardButton("💰 Купить подписку"))
    
    if message.from_user.id == ADMIN_ID:
        markup.add(types.KeyboardButton("🔑 Сгенерировать ключ"))
        
    bot.send_message(message.chat.id, "👋 Привет! Добро пожаловать в Мультивселенную Universe AI.\nВыберите действие на панели внизу:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🌌 О софте Universe AI":
        info = "🪐 Universe AI — футуристичная ИТ-студия и голосовой ассистент!\n\n" \
               "🔹 Скрытый запуск приложений и сайтов намертво без окон CMD.\n" \
               "🔹 Локальные ИИ-уши (Vosk) — работают полностью без интернета.\n" \
               "🔹 Смена нейро-голосов (Джарвис, Альтрон, ЭДИС, Пятница).\n\n" \
               "⚡ Стоимость лицензии: 500 рублей!"
        bot.send_message(message.chat.id, info, parse_mode="Markdown")
        
    elif message.text == "💰 Купить подписку":
        msg = f"💳 Для покупки лицензии и мгновенной активации напишите создателю напрямую:\n\n👉 {CREATOR_USERNAME}\n\nПосле оплаты вы получите уникальный ключ для входа!"
        bot.send_message(message.chat.id, msg)

    elif message.text == "🔑 Сгенерировать ключ" and message.from_user.id == ADMIN_ID:
        new_key = generate_serial()
        conn = sqlite3.connect("universe_system.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO keys (key_code) VALUES (?)", (new_key,))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ Новый лицензионный ключ успешно создан и добавлен в базу данных SQLite:\n\n`{new_key}`", parse_mode="Markdown")
        except sqlite3.IntegrityError:
            bot.send_message(message.chat.id, "⚠️ Ошибка: такой ключ уже существует, попробуйте еще раз.")
        finally:
            conn.close()

if __name__ == "__main__":
    init_db()
    print("[Система]: Бот Universe AI запущен через TGWS Proxy (порт 1443)...")
    bot.infinity_polling(none_stop=True)
