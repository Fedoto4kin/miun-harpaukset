import os, sys
import django 
from slugify import slugify


os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *

# for word in Word.objects.all():
#     word.word = word.word.replace('о', 'o')
#     word.save()

for d in Definition.objects.all():
    print(d.definition)
    d.save()