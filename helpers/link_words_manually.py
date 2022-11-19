import os, sys
import django 

os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *


def get_word(str):

    return  Word.objects.filter(base_set__in=Base.objects.filter(
                         base_slug=Base.krl_slugify(Base, string=str)
                        )).last()

while True:
    
    word1 = get_word(input('Enter word: '))
    if word1:
        print(word1)
        word2 = get_word(input("Enter word to link with '{}' ".format(word1.word)))
        word1.alias.add(word2)
        word1.save()
    else:
        print('Not Found')
