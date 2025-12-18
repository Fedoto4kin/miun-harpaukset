## TO-DO



### Dev Help
```bash
docker compose exec -it web python manage.py makemigrations
```
```bash
docker compose exec -it web python manage.py migrate
```

Create lesson blocks(modules)
E.g. Lesson 1 create 5 modules
`docker compose exec -it web python manage.py create_modules 1 5`

Clear lesson speeches files (deattached)
`docker compose exec -it web python manage.py clear_lesson_speeches`



### Deploy(1st):

Create `mhkk` user and clone code into `miun-harpaukset` directory

Set up certbot (?)


**Set up environment**
`cp .env.example .env`

```
echo "USER_ID=$(id -u)" >> .env
echo "GROUP_ID=$(id -g)" >> .env
```

```
docker compose -f docker-compose-prod.yml build 
```

*Backend*
1. Migrate  
 `docker exec -it mhkk_django python manage.py migrate`
2. Upload fixtures  
`docker exec -it mhkk_django python manage.py loaddata lexicon/fixtures/whole_lexicon.json`
`docker exec -it mhkk_django python manage.py loaddata lexicon/fixtures/lessons.json`
3. Init admin
`docker exec -it mhkk_django python manage.py createsuperuser`

*Frontend*
1. `docker compose -f docker-compose-prod.yml run client npm install`
2. `docker compose -f docker-compose-prod.yml run client npm run build`

### Deploy(changes)

1. `cd /home/mhkk/miun-harpaukset`
2. `git pull`
3. `bash ./upgrade.sh`
4. [optional] Upload fixtures, if you need


### Data upload

1. Create dump fixture
    * Lessons:
`docker compose exec -it web python manage.py dumpdata lessons --indent 4 > app/lessons/fixtures/lessons.json`
    * Lexicon
`docker compose exec -it web python manage.py dumpdata lexixon --indent 4 > app/lexicon/fixtures/lexicon.json`    
2. Upload to server
3. Clear lessons_* tables
4. Run on server
    * Lessons:
`docker exec -it mhkk_django python manage.py loaddata lessons/fixtures/lessons.json`
    * Lexicon
`docker compose exec -it web python manage.py loaddata lexicon/fixtures/lexicon.json`    