
### Help
`docker compose exec -it web python manage.py makemigrations`
`docker compose exec -it web python manage.py migrate`

### Deploy(1st):

Create `mhkk` user and clone code into `miun-harpaukset` directory

Set up certbot (?)

*Backend*
1. Migrate  
 `docker exec -it mhkk_django python manage.py migrate`
2. Upload fixtures  
`docker exec -it mhkk_django python manage.py loaddata lexicon/fixtures/whole_lexicon.json`
3. Init admin
`docker exec -it mhkk_django python manage.py createsuperuser`

*Frontend*
1. `docker compose -f docker-compose-prod.yml run client npm install`
2. `docker compose -f docker-compose-prod.yml run client npm run build`

### Deploy(changes)

1. `cd /home/mhkk/miun-harpaukset`
2. `git pull`
3. `bash ./upgrade.sh`