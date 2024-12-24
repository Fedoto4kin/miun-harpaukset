

`docker exec -it mhkk_django pip install django-cors-headers`

Deploy(1st):

1. Migrate  
 docker exec -it mhkk_django python manage.py migrate
2. Upload fixtures  
python manage.py loaddata lexicon/fixtures/pos.json
python manage.py loaddata lexicon/fixtures/lexicon.json
