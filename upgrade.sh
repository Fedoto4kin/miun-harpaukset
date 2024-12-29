#!/bin/bash
    
echo "Checking repository status..."
if ! git diff-index --quiet HEAD --; then
  echo "Repository is not clean. Please commit or stash changes before deploying."
  exit 1
fi

echo "Pulling latest code from the repository..."
git pull --ff-only
if [ $? -ne 0 ]; then
  echo "Git pull failed! Please resolve any merge conflicts or update issues manually."
  exit 1
fi
echo "Code updated successfully."

echo "Building front-end..."
docker compose -f docker-compose-prod.yml run client npm run build
if [ $? -ne 0 ]; then
  echo "Front-end build failed!"
  exit 1
fi
echo "Front-end build completed successfully."

echo "Running backend migrations..."
docker compose -f docker-compose-prod.yml exec -it web python manage.py migrate
if [ $? -ne 0 ]; then
  echo "Backend migrations failed!"
  exit 1
fi
echo "Backend migrations completed successfully."

echo "Restarting containers..."
docker compose -f docker-compose-prod.yml restart
if [ $? -ne 0 ]; then
  echo "Restarting containers failed!"
  exit 1
fi
echo "Containers restarted successfully."

echo "Deployment tasks completed!"