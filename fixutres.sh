#!/bin/bash

# Asking user if they want to create fixtures and upload to repository
read -p "Do you want to create fixtures and upload to repository y/n? " choice
case "$choice" in 
  y|yes|Y|YES ) 
    echo "Creating fixtures..."
    docker compose exec -it web python manage.py dumpdata lexicon --indent 4 > app/lexicon/fixtures/lexicon.json
    docker compose exec -it web python manage.py dumpdata lessons --indent 4 > app/lessons/fixtures/lessons.json
    echo "Fixtures created successfully."

    echo "Adding fixtures to git..."
    git add app/lexicon/fixtures/lexicon.json app/lessons/fixtures/lessons.json
    git commit -m "[Auto] Update fixtures and commit on $(date '+%Y-%m-%d')"
    git push
    echo "Fixtures committed and pushed successfully."
    ;;
  * ) 
    echo "Skipping fixtures creation."
    ;;
esac

echo "Deployment tasks completed!"
