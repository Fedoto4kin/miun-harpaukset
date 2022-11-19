import os, sys
import django 
from bs4 import BeautifulSoup
from collections import defaultdict

os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *

with open("harp1.html") as file:  
    data = file.read() 

soup = BeautifulSoup(data, 'html.parser')
words = soup.find_all('p')
result = []


for w in words:
    if w.find('b'):
        for t in w.find_all('b'):
            t = t.get_text().strip().split(',')
        #    t.pop(0)
            if (len(t) > 1):
                print(t)
                ws = []
                groups = defaultdict(list)
                for w in t:
                    ws += Word.objects.filter(base_set__in=Base.objects.filter(
                        base_slug=Base.krl_slugify(Base, string=w)))
                for w in ws:
                    groups[w.pos.id].append(w)
                result.append(groups)

# for _ in result:
#     for _i in _:
#         print(_[_i])
#         _[_i][0].alias.add(_[_i][1])
#         _[_i][0].save()