from django import template


register = template.Library()

BANNED_WORDS = [
    "вредина",
    "гадина",
    "дурак",
    "политика",
    "бурных",
    "Оскар",
    "охране",
    "Сдохни",
]


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise ValueError("мы только тексты цензурируем в нашей редакции")

    for bad_word in BANNED_WORDS:
        if bad_word in text:
            censored = bad_word[0] + ("*" * (len(bad_word) - 1))
            text = text.replace(bad_word, censored)

        if bad_word.capitalize() in text:
            censored = bad_word[0].capitalize() + ("*" * (len(bad_word) - 1))
            text = text.replace(bad_word, censored)

    return text


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
