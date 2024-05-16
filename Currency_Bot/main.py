import telebot
from config import TOKEN, vals
from extensions import Converter, APIException, Rubles

bot = telebot.TeleBot(TOKEN)


# Команды start, help. Идентичны и вызывают основное меню программы
@bot.message_handler(commands=["start", "help"])
def commands(message: telebot.types.Message):

    text = ("""Чтобы начать работу, напишите сообщение боту в следующем формате:\n
<конвертируемая валюта> <валюта, в которую конвертировать> <количество конвертируемой валюты>\n
к примеру: доллар рубль 10\n\n
Список доступных для конвертации валют: /values\n
Курс Рубля: /ruble""")
    bot.reply_to(message, text)


# команда values, вызывающая список доступных для конвертации валют
@bot.message_handler(commands=["values"])
def val(message: telebot.types.Message):

    text = "Доступные валюты:"
    for key in vals.keys():
        text = "\n- ".join((text, key))
    bot.reply_to(message, text)


# команда rubles, вызывающая курс рубля в соотношении с другими валютами
@bot.message_handler(commands=["ruble"])
def rub(message: telebot.types.Message):

    all_text = Rubles.rub()
    for text in all_text:
        bot.send_message(message.chat.id, text)


# основная часть бота с конвертацией
@bot.message_handler(content_types=["text", ])
def main(message: telebot.types.Message):

    try:
        values = list(map(str, message.text.lower().replace(",", ".").split(" ")))

        if len(values) != 3:
            raise APIException("Введите 3 параметра: <конвертируемая валюта> <в какую валюту конвертировать> "
                               "<количество конвертируемой валюты>")

        quote, base, amount = values
        json_r = Converter.get_price(quote, base, amount)  # загружаем данные в класс конвертации и выводим ответ

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать запрос\n{e}")
    else:
        # берем нужную строку из ответа класса и оформляем ответ пользователю
        text = f"Цена {amount} {quote} составляет: {json_r['conversion_result']} {base}"
        bot.send_message(message.chat.id, text)  # отправка ответа пользователю


bot.polling(non_stop=True)  # запуск бота в режиме nonstop
