import os, sys
import django 
from bs4 import BeautifulSoup

os.environ["DJANGO_SETTINGS_MODULE"] = 'krl.settings'
django.setup()

with open("harp1.html") as file:  
    data = file.read() 

soup = BeautifulSoup(data, 'html.parser')
words = soup.find_all('p')
result = []


for w in words:
    if w.find('b'):
        for t in w.find_all('b'):
            t = t.get_text().strip().replace('|', '')
            if t not in result and t != '':
                result.append(t)
            #    print(t)
     
print(','.join(result))