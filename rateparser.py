import telebot
import requests

TOKEN = '7480238695:AAHCiCIGYmeVLkutkAmPldUReX3ASwfECiY'  
bot = telebot.TeleBot(TOKEN)


white_list = [1828281181]  

def bool_login(chat_id):
    return chat_id in white_list

def get_wb_product_info(nm_ids):
    url = "https://card.wb.ru/cards/detail"
    params = {
        "appType": 1,
        "curr": "kzt",
        "dest": 269,
        "spp": 30,
        "hide_dtype": "10;13;14",
        "ab_testing": "false",
        "lang": "ru",
        "nm": ";".join(map(str, nm_ids))
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return None

    try:
        return response.json()["data"]["products"]
    except KeyError:
        return None

@bot.message_handler(commands=['start'])
def welcome(message):
    if bool_login(message.chat.id):
        bot.send_message(message.chat.id, "Добро пожаловать! Отправь артикул товара WB.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа. Купите подписку.")

@bot.message_handler(content_types=['text'])
def analyze_product(message):
    print(f"Получено сообщение: {message.text} от {message.chat.id}")

    if not bool_login(message.chat.id):
        bot.send_message(message.chat.id, "У вас нет доступа к боту.")
        return

    raw_text = message.text.strip()
    nm_ids = [x for x in raw_text.replace(',', ';').split(';') if x.isdigit()]

    if not nm_ids:
        bot.send_message(message.chat.id, "Введите корректные артикулы.")
        return

    products = get_wb_product_info(nm_ids)
    if not products:
        bot.send_message(message.chat.id, "Не удалось получить данные по артикулу(ам).")
        return

    for product in products:
        name = product.get("name")
        article = product.get("id")
        seller_id = product.get("supplierId")
        rating = product.get("supplierRating")
        reviews = product.get("supplierReviewsCount")

        msg = f"Товар: {name}\n"
        msg += f"Артикул: {article}\n"
        msg += f"Продавец ID: {seller_id}\n"
        msg += f"Рейтинг: {rating}\n"
        msg += f"Отзывы: {reviews}\n"

    if rating is not None and reviews is not None:
        if rating >= 4.5 and reviews >= 500:
            bot.send_message(message.chat.id, "Отличный товар! Высокий рейтинг и много отзывов.")
    else:
        bot.send_message(message.chat.id, "Обычный товар. Стоит проверить подробнее.")
    else:
        bot.send_message(message.chat.id, "Не удалось получить рейтинг или количество отзывов.")

    bot.send_message(message.chat.id, msg, parse_mode="Markdown")

bot.polling(none_stop=True)
