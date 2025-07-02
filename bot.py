import telebot
import psycopg2
from datetime import datetime

TOKEN = '7686596054:AAH6X95tGY942s7Jlk_Z0jBUDNvImFxlv88'
bot = telebot.TeleBot(TOKEN)

conn = psycopg2.connect(
    dbname="database",
    user="postgres",
    password="963600zx",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

@bot.message_handler(commands=['start'])
def handle_start(message):
    tg_id = message.from_user.id

    cur.execute("SELECT * FROM telegram_users WHERE login = %s", (tg_id,))
    user = cur.fetchone()

    if user:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы.")
    else:
        cur.execute(
            "INSERT INTO telegram_users (login, date, isbuy) VALUES (%s, %s, %s)",
            (tg_id, datetime.now(), False)
        )
        conn.commit()
        bot.send_message(message.chat.id, "Регистрация завершена. Спасибо!")

@bot.message_handler(commands=['buy'])
def handle_buy(message):
    tg_id = message.from_user.id
    cur.execute("UPDATE telegram_users SET isbuy = %s WHERE login = %s", (True, tg_id))
    conn.commit()
    bot.send_message(message.chat.id, "Подписка активирована!")
bot.polling(none_stop=True)
