## 📖 **Extended README**

### TO-DO
*Add your development tasks here*

---

## 🚀 **Development Commands**

### Dev Help
```bash
# Migrations
docker compose exec -it web python manage.py makemigrations
docker compose exec -it web python manage.py migrate

# Create lesson modules
docker compose exec -it web python manage.py create_modules 1 5

# Clear not-used audio files
docker compose exec -it web python manage.py clear_lesson_speeches
```

---

## 🌐 **Production Deployment (First Time)**

### 1. Server Preparation
```bash
# Create user and clone code
sudo adduser mhkk
sudo -u mhkk -i
cd ~
git clone <your-repo> miun-harpaukset
cd miun-harpaukset
```

### 2. Environment Setup
```bash
# Copy environment variables
cp .env.example .env

# Set user/group IDs
echo "USER_ID=$(id -u)" >> .env
echo "GROUP_ID=$(id -g)" >> .env

# Build containers
docker compose -f docker-compose-prod.yml build
```

### 3. SSL Setup (Certbot)
*Run certbot to obtain SSL certificates*
@todo 
### 4. Backend Initialization
```bash
# Database migrations
docker exec -it mhkk_django python manage.py migrate

# Load fixtures
docker exec -it mhkk_django python manage.py loaddata lexicon/fixtures/whole_lexicon.json
docker exec -it mhkk_django python manage.py loaddata lexicon/fixtures/lessons.json

# Create administrator
docker exec -it mhkk_django python manage.py createsuperuser
```

### 5. Frontend Build
```bash
docker compose -f docker-compose-prod.yml run client npm install
docker compose -f docker-compose-prod.yml run client npm run build
```

---

## 🔄 **Version Update (Deployment)**

```bash
cd /home/mhkk/miun-harpaukset
git pull
bash ./upgrade.sh

# Optional: Update fixtures if needed
```

---

## 📊 **Data Management**

### 1. Create Data Dumps
```bash
# Lessons
docker compose exec -it web python manage.py dumpdata lessons --indent 4 > app/lessons/fixtures/lessons.json

# Lexicon
docker compose exec -it web python manage.py dumpdata lexicon --indent 4 > app/lexicon/fixtures/lexicon.json

# Grammar
docker compose exec -it web python manage.py dumpdata grammar --indent 4 > app/grammar/fixtures/grammar.json
```

### 2. Upload to Server
*Upload created JSON files to the server*

### 3. Data Loading
```bash
# Clear tables (if needed)
# Load data
docker exec -it mhkk_django python manage.py loaddata lessons/fixtures/lessons.json
docker exec -it mhkk_django python manage.py loaddata lexicon/fixtures/lexicon.json
docker exec -it mhkk_django python manage.py loaddata lexicon/fixtures/grammar.json
```

---

## 🧹 **System Maintenance & Cleanup**

### ⚙️ **Automatic Cleanup (Recommended)**

The system is configured for automatic cleanup to maintain disk space.

#### Root Cron Setup:
```bash
sudo crontab -e

# Add these lines:
# Docker cleanup (Sunday 3:00)
0 3 * * 0 /usr/bin/docker image prune -f && /usr/bin/docker volume prune -f

# APT cache cleanup (Sunday 4:00)
0 4 * * 0 /usr/bin/apt clean && /usr/bin/apt autoclean

# System journal cleanup (Sunday 5:00)
0 5 * * 0 /usr/bin/journalctl --vacuum-time=7d
```

#### User Cron (for certbot renewal):
```bash
# As mhkk user, edit crontab:
crontab -e

# Add to reload nginx after certbot renewal:
0 3 * * * docker exec mhkk_nginx nginx -s reload
```

### 🔧 **Manual Cleanup Commands**

#### Docker Space Management:
```bash
# Check disk usage
docker system df

# Remove unused images
docker image prune -a -f

# Remove build cache
docker builder prune -f

# Remove stopped containers
docker container prune -f

# Remove unused networks
docker network prune -f
```

#### System Space Management:
```bash
# Check disk usage
df -h

# Clear APT cache
sudo apt clean
sudo apt autoclean

# Remove old kernels
sudo apt autoremove --purge

# Clean system logs
sudo journalctl --vacuum-time=7d
```

#### Application-Specific Cleanup:
```bash
# Clear Django static files cache
docker exec mhkk_django -it python manage.py collectstatic --clear

# Clear Django cache
docker exec mhkk_django -it python manage.py clearcache
```

### 📊 **Monitoring Disk Space**

```bash
# Quick disk check
df -h

# Docker disk usage
docker system df -v

# Large files in /var
sudo du -h --max-depth=1 /var | sort -hr
```

### 🛡️ **Safety Notes**

1. **Docker volumes**: `docker volume prune` only removes **unused named volumes**. Your PostgreSQL data in `./db` bind mount is safe.
2. **Build cache**: Clearing build cache may slow down subsequent builds but saves significant space.
3. **Logs**: Keeping 7 days of logs is usually sufficient for debugging while saving space.
4. **Images**: Only unused images are removed. Running containers are not affected.

### 📝 **Cleanup Script**

For convenience, create `/usr/local/bin/cleanup-system.sh`:
```bash
#!/bin/bash
echo "=== System Cleanup $(date) ==="
echo "1. Docker cleanup..."
docker system prune -f
echo "2. APT cleanup..."
apt clean && apt autoclean
echo "3. Log cleanup..."
journalctl --vacuum-time=7d
echo "Cleanup completed"
```

Make executable: `sudo chmod +x /usr/local/bin/cleanup-system.sh`

---

## **Support**

For issues with the deployment or maintenance, check:
- Docker logs: `docker-compose -f docker-compose-prod.yml logs`
- Nginx logs: `docker logs mhkk_nginx`
- Django logs: `docker logs mhkk_django`
- System logs: `journalctl -u docker`
