import os, sys
import django 
import re

exit()
os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

from lexicon.models import *

for df in Definition.objects.all():
	r = re.split("\d\.", df.definition)

	if len(r) > 1:
		for _ in list(filter(None, r)):
			nd = Definition(definition=_.strip(), word=df.word, lang=df.lang)
			print(nd.word, nd.lang, nd.definition)
			nd.save()
		df.delete()
		print(df.word, df.lang, df.definition)
		print('-----------------')

