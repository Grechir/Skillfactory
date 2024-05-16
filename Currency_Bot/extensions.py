import requests
import json
from config import vals, API


class APIException(Exception):  # исключение, возникающее при ошибке конвертации
    pass


class Converter:
    """Предварительные проверки значений

            и непосредственная конвертация"""
    @staticmethod
    def get_price(quote, base, amount):

        # 1
        if quote == base:
            raise APIException(f"Нельзя конвертировать одинаковые валюты, {base}")

        # 2
        try:
            quote_t = vals[quote]
        except KeyError:
            raise APIException(f"Не удалось конвертировать валюту {quote}")

        # 3
        try:
            base_t = vals[base]
        except KeyError:
            raise APIException(f"Не удалось конвертировать валюту {base}")

        # 4.1, 4.2
        try:
            amount_t = float(amount)
            if float(amount_t) <= 0:
                raise APIException(f"Не удалось конвертировать {amount_t} валюты {quote_t}")
        except ValueError:
            raise APIException(f"Ошибка конвертации: используйте цифровое значение")

        # конвертация и получение ответа в формате json
        r = requests.get(f"https://v6.exchangerate-api.com/v6/{API}/pair/{quote_t}/{base_t}/{amount_t}").content
        json_r = json.loads(r)

        return json_r


class Rubles:
    @staticmethod
    def rub():
        """ Обработчик команды:

                    /ruble"""

        all_text = []
        amount, base = 1, "рубль"
        for key in vals.keys():
            if key != "рубль":
                html = requests.get(f"https://v6.exchangerate-api.com/v6/{API}/pair/{vals[key]}/{vals[base]}/{amount}")
                response = html.content
                json_r = json.loads(response)
                text = f"Стоимость {amount} {key} составляет: {json_r['conversion_result']} рублей\n"
                all_text.append(text)

        return all_text
