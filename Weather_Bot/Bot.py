import asyncio
import logging
from config import tg_bot_token, open_weather_token

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart

import requests
import datetime
# from pprint import pprint

bot = Bot(token=tg_bot_token)
dp = Dispatcher()


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def handle_start(message: types.message):
    await message.reply("Здравствуйте, напишите название города, в котором Вы хотите узнать погоду")


@dp.message()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Мелкий дождь \U00002600",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Не могу распознать погоду"
        weather = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(f" ***{datetime.datetime.now().strftime("%d-%m-%Y %H-%M")}***\n\n"
                            f"Погода в городе {city}: {wd}\n\n"
                            f"Температура: {weather} C° , Ощущается как: {feels_like} С°\n\n"
                            f"Скорость ветра: {wind} м/c\n\n"
                            f"Влажность: {humidity} %\n\n"
                            f"Атмосферное давление: {pressure} мм рт. ст.\n\n\n"
                            f"Восход: {sunrise_timestamp} по Мск\n"
                            f"Закат: {sunset_timestamp} по Мск\n")

        if -70 < feels_like <= -15:
            await message.reply("Мороз, наденьте пуховик и теплые штаны.")
        elif -15 < feels_like <= 0:
            await message.reply("Очень холодно, одевайтесь потеплее.")
        elif 0 < feels_like <= 10:
            await message.reply("Холодно, наденьте куртку.")
        elif 10 < feels_like <= 17:
            await message.reply("Прохладно, наденьте ветровку.")
        elif 17 < feels_like <= 26:
            await message.reply("Тепло, подойдет футболка с коротким рукавом.")
        elif 26 < feels_like < 55:
            await message.reply("Жара! Пейте больше воды, старайтесь пребывать в тени.")
        else:
            await message.reply("Экстремальный температурный диапазон")

        await message.reply("Хорошего Вам дня!")

    except TypeError:
        await message.reply("Проверьте название города")


if __name__ == "__main__":
    asyncio.run(main())
