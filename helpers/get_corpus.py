import mysql.connector
import os, sys, re
import django 
from collections import OrderedDict

os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *

mydb = mysql.connector.connect(
  host="rc1c-pgaz6h6wqx0h7l6n.mdb.yandexcloud.net",
  user="karvep",
  passwd="Petr0z4v0dsK",
  database="karvep"
)

mycursor = mydb.cursor()
sql = 'select t.text from texts t LEFT JOIN dialect_text dt ON dt.text_id=t.id WHERE dt.dialect_id IN (26, 27, 47)';
mycursor.execute(sql)

corpus = ''
lexicon  = ''
_c = ''

for b in Base.objects.all():
    lexicon += b.base + ' '


for _ in mycursor.fetchall():
    _c += _[0].lower().replace('ü', 'y').replace('\n',' ').replace('\t','').replace('\r','')

for _w in filter(None, _c.split(' ')):
    if 'w' in _w:
        if re.search('[aou]', _w):
            _w = _w.replace('w', 'u')
        else:
            _w = _w.replace('w', 'y') 
    corpus += ' ' + _w

res_c = {}
res_l = {}
total_l = 0
total_c = 0

for _l in KRL_ABC.lower():
    res_c[_l] = corpus.count(_l)
    res_l[_l] = lexicon.count(_l)
    total_c += corpus.count(_l)
    total_l += lexicon.count(_l)

r_c = 1
data_c = []

r_l = 1
data_l = []

for _i in sorted(res_c.items(), key=lambda t: t[1], reverse=True):
    data_c.append((r_c, _i[0], "{0:.2f}%".format(_i[1]/total_c*100) ))
    r_c += 1

for _i in sorted(res_l.items(), key=lambda t: t[1], reverse=True):
    data_l.append((r_l, _i[0], "{0:.2f}%".format(_i[1]/total_l*100) ))
    r_l += 1


col_width = 6

for row in data_l:
    print("".join(str(word).ljust(col_width) for word in row))