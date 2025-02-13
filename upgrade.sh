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

echo "Installing front-end dependencies..."
docker compose -f docker-compose-prod.yml run client npm install
if [ $? -ne 0 ]; then
  echo "Front-end dependency installation failed!"
  exit 1
fi
echo "Front-end dependencies installed successfully."

echo "Building front-end..."
docker compose -f docker-compose-prod.yml run client npm run build
if [ $? -ne 0 ]; then
  echo "Front-end build failed!"
  exit 1
fi
echo "Front-end build completed successfully."

echo "Installing Python dependencies..."
docker compose -f docker-compose-prod.yml exec -it web pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo "Python dependency installation failed!"
  exit 1
fi
echo "Python dependencies installed successfully."

echo "Running backend migrations..."
docker compose -f docker-compose-prod.yml exec -it web python manage.py migrate
if [ $? -ne 0 ]; then
  echo "Backend migrations failed!"
  exit 1
fi
echo "Backend migrations completed successfully."

echo "Collecting static files..."
docker compose -f docker-compose-prod.yml exec -it web python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
  echo "Collecting static files failed!"
  exit 1
fi
echo "Static files collected successfully."

echo "Stopping containers and removing orphans..."
docker compose -f docker-compose-prod.yml down --remove-orphans
if [ $? -ne 0 ]; then
  echo "Stopping containers failed!"
  exit 1
fi
echo "Containers stopped and orphans removed successfully."

echo "Starting containers..."
docker compose -f docker-compose-prod.yml up -d
if [ $? -ne 0 ]; then
  echo "Starting containers failed!"
  exit 1
fi
echo "Containers started successfully."

echo "Deployment tasks completed!"