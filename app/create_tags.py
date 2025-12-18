import os

import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "krl.settings")
django.setup()

from lessons.models import Tag

tags_data = [
    {
        "code": "grammar",
        "name": "Grammatikka",
        "hint_russian": "Грамматика",
        "hint_finnish": "Kielioppi",
    },
    {
        "code": "tell",
        "name": "Šanele!",
        "hint_russian": "Расскажи",
        "hint_finnish": "Kerro",
    },
    {
        "code": "vocabulary",
        "name": "Uuvet šanat",
        "hint_russian": "Новая лексика",
        "hint_finnish": "Uusi sanasto",
    },
    {
        "code": "dialogue",
        "name": "Dialoga",
        "hint_russian": "Диалог",
        "hint_finnish": "Vuoropuhelu",
    },
    {
        "code": "remember",
        "name": "Muissuta!",
        "hint_russian": "Запомни",
        "hint_finnish": "Muista",
    },
    {
        "code": "proverbs",
        "name": "Šanapolvet",
        "hint_russian": "Пословицы",
        "hint_finnish": "Sanonnat",
    },
    {
        "code": "task",
        "name": "Annanda / Kyžymykšet",
        "hint_russian": "Задание / Вопросы",
        "hint_finnish": "Tehtävä / Kysymykset",
    },
    {"code": "game", "name": "Kiza", "hint_russian": "Игра", "hint_finnish": "Peli"},
    {
        "code": "read",
        "name": "Luve da kiännä!",
        "hint_russian": "Прочитай и переведи",
        "hint_finnish": "Lue ja käännä",
    },
    {"code": "sing", "name": "Laula!", "hint_russian": "Спой", "hint_finnish": "Laula"},
    {
        "code": "write",
        "name": "Kirjuta! / Täyvennä!",
        "hint_russian": "Напиши / Заполни",
        "hint_finnish": "Kirjoita / Täydennä",
    },
    {
        "code": "smile",
        "name": "Muhaha!",
        "hint_russian": "Улыбнись",
        "hint_finnish": "Hymyile",
    },
    {
        "code": "listen",
        "name": "Kuundele da tačkuta! / Kuundele oigie varianta!",
        "hint_russian": "Послушай и повтори / Послушай правильный вариант",
        "hint_finnish": "Kuuntele ja toista / Kuuntele oikea vaihtoehto",
    },
    {"code": "test", "name": "Testa", "hint_russian": "Тест", "hint_finnish": "Testi"},
    {"code": "key", "name": "Avuan", "hint_russian": "Ключ", "hint_finnish": "Avain"},
]


# Создание уроков
def create_tags():
    for data in tags_data:
        Tag.objects.create(**data)


if __name__ == "__main__":
    create_tags()
