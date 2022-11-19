import os, sys
import glob
import django 
from django.core.files import File

os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *

Speech.objects.all().delete()

for d in glob.glob("./words/annotated/*.mp3"):

    word = os.path.splitext(os.path.basename(d))[0]
    f = File(open(d, 'rb'))

    speech = Speech(text=word)
    speech.mp3 = f
    speech.save()
