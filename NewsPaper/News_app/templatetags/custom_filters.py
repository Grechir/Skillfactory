from django import template

register = template.Library()

censor_words = {
    "животные",
    "будущее"     # рандомные слова из текста и заголовка только ради демонстрации
}


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise TypeError("Ожидался строковой тип данных")

    censor_words_lower = {word.lower() for word in censor_words}
    censor_words_title = {word.title() for word in censor_words}

    all_censor_words = censor_words_lower.union(censor_words_title)

    for word in all_censor_words:
        text = text.replace(word, word[0] + "*" * (len(word) - 1))
    return text
