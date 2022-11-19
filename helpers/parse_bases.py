import os, sys
import django 
from bs4 import BeautifulSoup

sys.path.append('../')

os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *

def filter_mod(mod):
    return mod.replace('-', '').replace(' ', '')

def parse_name(W, base, mod, pos):

    bases = []

    if 'pl.' in pos:
        m_4_5 = mod[0].replace('/', ':').split(':')
        base_4 = base + filter_mod(m_4_5[0])
        if len(m_4_5) > 1:
            base_5 = base + filter_mod(m_4_5[1])
        else:
            base_5 = base_4
        bases.append((4, base_4))
        bases.append((5, base_5))
    elif 'sing.' in pos:
        m_1_2 = mod[0].replace('/', ':').split(':')
        base_1 = base + filter_mod(m_1_2[0])
        if len(m_1_2) > 1:
            base_2 = base + filter_mod(m_1_2[1])
        else:
            base_2 = base_1
        base_3 = base + filter_mod(mod[1])
        bases.append((1, base_1))
        bases.append((2, base_2))
        bases.append((3, base_3))
    else:
        m_1_2 = mod[0].replace('/', ':').split(':')
        base_1 = base + filter_mod(m_1_2[0])
        if len(m_1_2) > 1:
            base_2 = base + filter_mod(m_1_2[1])
        else:
            base_2 = base_1
        base_3 = base + filter_mod(mod[1])
        m_4_5 = mod[2].replace('/', ':').split(':')
        base_4 = base + filter_mod(m_4_5[0])
        if len(m_4_5) > 1:
            base_5 = base + filter_mod(m_4_5[1])
        else:
            base_5 = base_4
        bases.append((1, base_1))
        bases.append((2, base_2))
        bases.append((3, base_3))
        bases.append((4, base_4))
        bases.append((5, base_5))

    for i, j in bases:
        Base.objects.create(num=i, base=j, word=W)



def parse_verb(W, base, mod, pos):

    bases = []

    if 'def.' in pos:
        bases.append((2, base + filter_mod(mod[0])))
        bases.append((4, base + filter_mod(mod[1])))
        bases.append((5, base + filter_mod(mod[2])))
        if len(mod) > 3:
            bases.append((6, base + filter_mod(mod[3])))
        if len(mod) > 4:
            bases.append((7,  base + filter_mod(mod[3])))

    else:
        m_1_2 = mod[0].replace('/', ':').split(':')
        base_1 = base + filter_mod(m_1_2[0])
        if len(m_1_2) > 1:
            base_2 = base + filter_mod(m_1_2[1])
        else:
            base_2 = base_1

        m_3_4 = mod[1].replace('/', ':').split(':')
        base_3 = base + filter_mod(m_3_4[0])
        if len(m_3_4) > 1:
            base_4 = base + filter_mod(m_3_4[1])
        else:
            base_4 = base_3

        base_5 = base + filter_mod(mod[2])
        base_6 = base + filter_mod(mod[3])
        base_7 = base + filter_mod(mod[4])

        bases.append((1, base_1))
        bases.append((2, base_2))
        bases.append((3, base_3))
        bases.append((4, base_4))
        bases.append((5, base_5))
        bases.append((6, base_6))
        bases.append((7, base_7))

    for i, j in bases:
        b = Base.objects.create(num=i, base=j, word=W)


if __name__ == "__main__":

    Base.objects.all().exclude(num=0).delete()

    for W in Word.objects.all():
        soup = BeautifulSoup(W.orig, "html.parser")
        if soup.code:
            pos = soup.i.text
            base = W.word.split('|')[0]
            mod = soup.code.text.split(',')
            if W.pos.abbr != 'pron.':
                if 'v.' in pos:
                    parse_verb(W, base, mod, pos)
                else:
                    parse_name(W, base, mod, pos)
