import os, sys
import django 


os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *

for word in Word.objects.all():
	base = word.base_set.get(num=0)
	try:
		base.word.speech = Speech.objects.get(text__iexact=base.base)
	except Exception:
		print(base.base)
	else:
		print(base.word.word)
		base.word.save()