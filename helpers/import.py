import os, sys
import django 
from bs4 import BeautifulSoup

os.environ["DJANGO_SETTINGS_MODULE"] = 'project.settings'
django.setup()

from lexicon.models import *

with open("MAuuzi.html") as file:  
    data = file.read() 

soup = BeautifulSoup(data, 'html.parser')
words = soup.find_all('p')
for w in words:

    lemma = w.find('b').get_text().strip()
    pos =  w.find('i').get_text().strip()
    dif = w.find('mark').get_text().split('–')
    W = None

    try:
        P = Pos.objects.get(abbr=pos.split(" ", 1)[0])
    except Pos.DoesNotExist:
        P = Pos.objects.get(id=12)
    
    W = Word(word=lemma, orig=str(w), pos=P)
    W.save()
    d_ru = Definition.objects.create(lang='ru', definition=dif[0].strip(), word=W)
    d_fi = Definition.objects.create(lang='fi', definition=dif[1].strip(), word=W)
    W.definition.add(*[d_ru, d_fi])
    base_0 = Base.objects.create(num=0, base=lemma.replace('|',''), word=W)
    W.base.add(base_0)
    print(lemma + ' added')