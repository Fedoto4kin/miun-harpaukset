import telebot
import os
import sys
import django
import time
import pathlib
import emoji
import logging
import json
from django.db.models import Count
from telebot import types

sys.path.append('../')
os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *


API_KEY = '1217434023:AAFyz8HYtVuVOCrZboD5Rqkrm-FBcFXnHRo'
bot = telebot.TeleBot(API_KEY)


def get_word(str):

    return Word.objects.filter(base_set__in=Base.objects.filter(
                         base_slug=Base.krl_slugify(Base, string=str)
                        )).last()


@bot.message_handler(commands=['test'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=4)
    button = telebot.types.InlineKeyboardButton(text='Click', callback_data='show_word')
    markup.add(button)
    bot.send_message(chat_id=message.chat.id, text='Text', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    data = json.loads(call.data)
    if 'word' in data:
        bot.send_message(call.message.chat.id, 'Terveh')


@bot.message_handler(commands=['start'])
def start_message(message):

    # markup = types.ReplyKeyboardMarkup()
    # items = []
    # for letter in KRL_ABC:
    #     print(letter)
    #     items.append(types.KeyboardButton(letter))
    #
    #
    # markup.row(*items[:5])
    # markup.row(*items[5:10])
    # markup.row(*items[10:15])
    # markup.row(*items[15:20])
    # markup.row(*items[20:25])
    # markup.row(*items[25:])
    bot.send_message(message.chat.id, 'Tulgua terveh. Mie olen Šana-bota\nKirjuttua šana, štobi löydiä šanan šanakniigašta')


@bot.message_handler(content_types=['text'])
def send_text(message):

    search = message.text
    queryset = Word.objects.filter(base_set__in=Base.objects.filter(
                base_slug_diacritic__startswith=Word.search_prepare(search)
                )
            ).annotate(total=Count('id'))

    count = len(queryset)

    if count:

        for q in queryset:
            q.definition_set_by_lang = {}
            for df in q.definition_set.all():
                if df.lang not in q.definition_set_by_lang:
                    q.definition_set_by_lang[df.lang] = [df.definition,]
                else:
                    q.definition_set_by_lang[df.lang].append(df.definition)

        word_set = sorted(queryset, key=lambda word: [Word.get_krl_abc().lower().index(c) for c in Base.krl_slugify(Base, word.word)])

        sana = 'šana'
        if count > 1:
            sana = 'šanua'
        msg = '_Löydy {} {}_\n\n'.format(count, sana)

        i = 0

        for t in word_set:
            msg += '*{}* -- {}\n\n'.format(str(t), ' '.join(t.definition_set_by_lang['ru']))
            i += 1

            if not i % 8 and count > 8:
                bot.send_message(message.chat.id, msg, parse_mode='Markdown')
                msg = ''
                count -= 8
                time.sleep(1)

        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'Ei nimidä löydyn')


if __name__ == '__main__':

    try:
        logging.info('Bot running..')
        bot.polling(none_stop=True, interval=2)
    except Exception as ex:
        logging.error('Error - {}'.format(str(ex)))

        logging.info('Restarting..')
        bot.stop_polling()
        time.sleep(15)

        logging.info('Running again!')
        bot.polling(none_stop=True, interval=2)

