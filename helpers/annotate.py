import os, sys
import glob

from slugify import slugify

with open("_parsed_list.txt") as file:  
    data = file.read() 

krl_abc = ''
letter = ''
n = 1
for word in data.split(','):
    if letter != word[0].upper():
        letter = word[0].upper()
        n = 1
        krl_abc += letter

    print(n, word)
    n += 1
