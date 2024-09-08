import requests
import datetime
# from pprint import pprint
from config import open_weather_token
from colorama import init
from colorama import Back, Fore, Style
init()

# Тут мы создаем базовую функцию, в которую прописываем 2 значения (город, токен) и работаем с данными с сайта и ответом


def get_weather(city, open_weather_token):

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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
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

        print(f" ***{datetime.datetime.now().strftime("%d-%m-%Y %H-%M")}***\n"
              f"Погода в городе {city}: {wd}\n"
              f"Температура: {weather} C° , Ощущается как: {feels_like} С°\n"
              f"Скорость ветра: {wind} м/c\n"
              f"Влажность: {humidity} %\n"
              f"Атмосферное давление: {pressure} мм рт. ст.\n\n\n"
              f"Восход: {sunrise_timestamp} по Мск\n"
              f"Закат: {sunset_timestamp} по Мск\n")

        if -70 < feels_like <= -15:
            print("Мороз, наденьте пуховик и теплые штаны.")
        elif -15 < feels_like <= 0:
            print("Очень холодно, одевайтесь потеплее.")
        elif 0 < feels_like <= 10:
            print("Холодно, наденьте куртку.")
        elif 10 < feels_like <= 17:
            print("Прохладно, наденьте ветровку.")
        elif 17 < feels_like <= 22:
            print("Тепло, подойдет футболка с коротким рукавом.")
        elif 22 < feels_like < 55:
            print("Жара! Пейте больше воды, старайтесь пребывать в тени.")
        else:
            print(Back.RED), print(Fore.BLACK), print(Style.NORMAL)
            print("Экстремальный температурный диапазон")

        print("Хорошего Вам дня!")

    except Exception as ex:
        print(ex)
        print(Back.RED), print(Fore.BLACK), print(Style.NORMAL)
        print("Проверьте название города")

# теперь создаем главную функцию, которая обрабатывает запрос пользователя и вызывает функцию get_weather


def main():
    city = input("Введите название города: ")
    get_weather(city, open_weather_token)


if __name__ == "__main__":
    main()
