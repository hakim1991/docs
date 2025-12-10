# 🚀 Deployment

[← Testing](./infos-python-11-testing.md) | [Index](./infos-python-00-index.md)

## Variables d'environnement

### .env

```bash
# .env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=your-api-key
```

```python
# Charger variables
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

```bash
pip install python-dotenv
```

### .gitignore

```
# .gitignore
.env
*.pyc
__pycache__/
venv/
.venv/
*.db
*.sqlite3
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
```

## Streamlit Deployment

### Streamlit Cloud

1. **Préparer le projet**

```
myapp/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── README.md
```

```txt
# requirements.txt
streamlit==1.28.0
pandas==2.1.0
plotly==5.17.0
```

```toml
# .streamlit/config.toml
[theme]
primaryColor = "#F63366"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
```

2. **Déployer sur Streamlit Cloud**
   - Push sur GitHub
   - Aller sur https://share.streamlit.io
   - Connecter le repository
   - Sélectionner la branche et le fichier
   - Déployer !

3. **Secrets**

```toml
# .streamlit/secrets.toml (local, pas dans git)
api_key = "your-api-key"

[database]
host = "localhost"
port = 5432
```

```python
# Utiliser secrets
import streamlit as st

api_key = st.secrets["api_key"]
db_host = st.secrets["database"]["host"]
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

```bash
# Build
docker build -t myapp .

# Run
docker run -p 8501:8501 myapp
```

## Flask Deployment

### Production configuration

```python
# config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    # Force HTTPS
    PREFERRED_URL_SCHEME = "https"

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
```

```python
# app.py
from flask import Flask
from config import config
import os

def create_app():
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config[env])

    # Initialiser extensions
    from extensions import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)

    return app
```

### Gunicorn

```bash
pip install gunicorn
```

```python
# wsgi.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
```

```bash
# Lancer avec Gunicorn
gunicorn wsgi:app

# Avec workers
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

# Configuration
gunicorn -c gunicorn_config.py wsgi:app
```

```python
# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY . .

# Créer user non-root
RUN useradd -m myuser
USER myuser

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Nginx

```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/app/static;
        expires 30d;
    }
}
```

### Heroku

```
myapp/
├── app.py
├── wsgi.py
├── requirements.txt
├── Procfile
└── runtime.txt
```

```
# Procfile
web: gunicorn wsgi:app
```

```
# runtime.txt
python-3.11.5
```

```bash
# Déployer
heroku login
heroku create myapp
git push heroku main

# Variables d'environnement
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=postgresql://...

# Logs
heroku logs --tail

# Scale
heroku ps:scale web=2
```

## Django Deployment

### Production settings

```python
# settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

```python
# settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

```python
# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = [os.getenv("ALLOWED_HOST")]

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Database from environment
import dj_database_url
DATABASES["default"] = dj_database_url.config(
    default=os.getenv("DATABASE_URL"),
    conn_max_age=600
)
```

```python
# manage.py
import os
import sys

if __name__ == "__main__":
    env = os.getenv("DJANGO_ENV", "development")
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        f"myproject.settings.{env}"
    )

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
```

### Static files

```bash
# Installer WhiteNoise
pip install whitenoise

# Collecter static
python manage.py collectstatic --noinput
```

### Gunicorn

```bash
pip install gunicorn
```

```python
# wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings.production")

application = get_wsgi_application()
```

```bash
# Lancer
gunicorn myproject.wsgi:application -w 4 -b 0.0.0.0:8000
```

### Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code
COPY . .

# Collecter static
RUN python manage.py collectstatic --noinput

# User non-root
RUN useradd -m django
RUN chown -R django:django /app
USER django

EXPOSE 8000

CMD ["gunicorn", "myproject.wsgi:application", "-w", "4", "-b", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn myproject.wsgi:application -w 4 -b 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DJANGO_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Heroku

```
# Procfile
web: gunicorn myproject.wsgi:application
release: python manage.py migrate
```

```bash
# Déployer
heroku create myapp
heroku addons:create heroku-postgresql:hobby-dev

heroku config:set DJANGO_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOST=myapp.herokuapp.com

git push heroku main

# Migrations
heroku run python manage.py migrate

# Créer superuser
heroku run python manage.py createsuperuser

# Static files (avec WhiteNoise)
# Automatique avec collectstatic

# Logs
heroku logs --tail
```

## AWS (EC2)

### Setup serveur

```bash
# Connecter SSH
ssh -i key.pem ubuntu@ec2-ip-address

# Update système
sudo apt update && sudo apt upgrade -y

# Python et dépendances
sudo apt install python3-pip python3-venv nginx postgresql -y

# Créer user
sudo useradd -m -s /bin/bash myapp
sudo su - myapp

# Clone projet
git clone https://github.com/user/myapp.git
cd myapp

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install -r requirements.txt
pip install gunicorn

# Variables d'environnement
nano .env
```

### Systemd service

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=MyApp Gunicorn
After=network.target

[Service]
User=myapp
Group=www-data
WorkingDirectory=/home/myapp/myapp
Environment="PATH=/home/myapp/myapp/venv/bin"
ExecStart=/home/myapp/myapp/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/myapp/myapp/myapp.sock \
    wsgi:app

[Install]
WantedBy=multi-user.target
```

```bash
# Activer service
sudo systemctl start myapp
sudo systemctl enable myapp
sudo systemctl status myapp
```

### Nginx

```nginx
# /etc/nginx/sites-available/myapp
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://unix:/home/myapp/myapp/myapp.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/myapp/myapp/staticfiles;
        expires 30d;
    }

    location /media {
        alias /home/myapp/myapp/media;
        expires 30d;
    }
}
```

```bash
# Activer site
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL avec Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renouvellement
sudo certbot renew --dry-run
```

## CI/CD avec GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=myapp --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "myapp"
          heroku_email: "your-email@example.com"
```

## Monitoring et logs

### Sentry (error tracking)

```bash
pip install sentry-sdk
```

```python
# Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

# Django
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0
)
```

### Logging

```python
# logging_config.py
import logging
import logging.handlers

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))

    logger.addHandler(console)
    logger.addHandler(file_handler)
```

## Bonnes pratiques

```python
# ✅ Variables d'environnement
SECRET_KEY = os.getenv("SECRET_KEY")

# ❌ Hardcoded
SECRET_KEY = "my-secret-key-123"

# ✅ Debug off en production
DEBUG = os.getenv("DEBUG", "False") == "True"

# ✅ Requirements avec versions
# requirements.txt
Flask==3.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9

# ✅ Séparer config dev/prod
if os.getenv("ENV") == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# ✅ Health check endpoint
@app.route("/health")
def health():
    return {"status": "ok"}, 200

# ✅ Graceful shutdown
import signal
import sys

def signal_handler(sig, frame):
    logger.info("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

# ✅ Database connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True  # Check connection avant utilisation
)

# ✅ Static files avec CDN
STATIC_URL = "https://cdn.example.com/static/"

# ✅ Compression
# Flask
from flask_compress import Compress
Compress(app)

# Django (avec WhiteNoise)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ✅ Rate limiting
from flask_limiter import Limiter

limiter = Limiter(
    app,
    default_limits=["200 per day", "50 per hour"]
)

# ✅ Security headers
@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

## Checklist production

- [ ] Variables d'environnement configurées
- [ ] DEBUG = False
- [ ] SECRET_KEY fort et unique
- [ ] Base de données production (PostgreSQL/MySQL)
- [ ] ALLOWED_HOSTS configuré (Django)
- [ ] Static files collectés
- [ ] SSL/HTTPS activé
- [ ] Migrations appliquées
- [ ] Tests passent
- [ ] Monitoring configuré (Sentry)
- [ ] Logs configurés
- [ ] Backup base de données
- [ ] Health check endpoint
- [ ] Rate limiting activé
- [ ] Security headers configurés
- [ ] .env dans .gitignore
- [ ] Requirements.txt à jour
- [ ] Documentation déploiement

[← Testing](./infos-python-11-testing.md) | [Index](./infos-python-00-index.md)
