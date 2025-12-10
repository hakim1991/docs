# 🎯 Cas Pratiques

[← Différences Linux/Windows](./infos-docker-12-differences-linux-windows.md) | [Index](./infos-docker-00-index.md)

---

## Table des matières
- [Stack Odoo + PostgreSQL](#stack-odoo-postgresql)
- [Stack Next.js + FastAPI](#stack-nextjs-fastapi)
- [Stack complète avec MinIO](#stack-complete-avec-minio)
- [Environnement de développement](#environnement-de-developpement)
- [Stack de monitoring](#stack-de-monitoring)

---

## Stack Odoo + PostgreSQL

### Architecture

```
┌─────────────┐
│   Nginx     │  Reverse Proxy
│   :80/443   │
└──────┬──────┘
       │
┌──────▼──────┐
│   Odoo      │  ERP
│   :8069     │
└──────┬──────┘
       │
┌──────▼──────┐
│ PostgreSQL  │  Base de données
│   :5432     │
└─────────────┘
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: odoo-postgres
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=${DB_PASSWORD:-odoo}
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - odoo-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U odoo"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Odoo ERP
  odoo:
    image: odoo:17.0
    container_name: odoo-app
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=${DB_PASSWORD:-odoo}
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./config:/etc/odoo
      - ./addons:/mnt/extra-addons
    networks:
      - odoo-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8069/web/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

  # Nginx Reverse Proxy (optionnel)
  nginx:
    image: nginx:alpine
    container_name: odoo-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx-logs:/var/log/nginx
    depends_on:
      - odoo
    networks:
      - odoo-network
    restart: unless-stopped

volumes:
  postgres-data:
    driver: local
  odoo-web-data:
    driver: local
  nginx-logs:
    driver: local

networks:
  odoo-network:
    driver: bridge
```

### Configuration Odoo

```ini
# config/odoo.conf
[options]
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo
admin_passwd = ${ADMIN_PASSWORD}
db_host = db
db_port = 5432
db_user = odoo
db_password = ${DB_PASSWORD}
dbfilter = ^%d$
list_db = False
proxy_mode = True
workers = 4
max_cron_threads = 2
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648
limit_request = 8192
limit_time_cpu = 600
limit_time_real = 1200
log_level = info
```

### Configuration Nginx

```nginx
# nginx/nginx.conf
upstream odoo {
    server odoo:8069;
}

upstream odoochat {
    server odoo:8072;
}

server {
    listen 80;
    server_name odoo.example.com;

    # Redirect to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name odoo.example.com;

    # SSL Configuration
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_session_timeout 30m;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Logs
    access_log /var/log/nginx/odoo-access.log;
    error_log /var/log/nginx/odoo-error.log;

    # Proxy settings
    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;

    # Increase proxy buffer
    proxy_buffering off;
    proxy_redirect off;

    # Odoo
    location / {
        proxy_pass http://odoo;
    }

    # Odoo longpolling
    location /longpolling {
        proxy_pass http://odoochat;
    }

    # Cache static files
    location ~* /web/static/ {
        proxy_cache_valid 200 90m;
        proxy_buffering on;
        expires 864000;
        proxy_pass http://odoo;
    }

    # File size limit
    client_max_body_size 100M;
}
```

### Démarrage et gestion

```bash
# Démarrer la stack
docker compose up -d

# Voir les logs
docker compose logs -f odoo

# Accéder à Odoo
# http://localhost:8069 ou https://odoo.example.com

# Backup de la base de données
docker exec odoo-postgres pg_dump -U odoo postgres | gzip > odoo-backup-$(date +%Y%m%d).sql.gz

# Restaurer
gunzip -c odoo-backup.sql.gz | docker exec -i odoo-postgres psql -U odoo postgres

# Mise à jour Odoo
docker compose pull odoo
docker compose up -d --force-recreate odoo
```

---

## Stack Next.js + FastAPI

### Architecture

```
┌──────────────┐
│   Next.js    │  Frontend (SSR)
│   :3000      │
└──────┬───────┘
       │
┌──────▼───────┐
│   FastAPI    │  Backend API
│   :8000      │
└──────┬───────┘
       │
┌──────▼───────┬───────────────┬──────────────┐
│ PostgreSQL   │    Redis      │   MinIO      │
│  :5432       │    :6379      │   :9000      │
│  Database    │    Cache      │   Storage    │
└──────────────┴───────────────┴──────────────┘
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: app-postgres
    environment:
      POSTGRES_DB: ${DB_NAME:-appdb}
      POSTGRES_USER: ${DB_USER:-admin}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d:ro
    networks:
      - backend-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-admin}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: app-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD:-redissecret}
    volumes:
      - redis-data:/data
    networks:
      - backend-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # MinIO Object Storage
  minio:
    image: minio/minio:latest
    container_name: app-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD:-minioadmin}
    volumes:
      - minio-data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - backend-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3

  # FastAPI Backend
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: app-api
    environment:
      # Database
      DATABASE_URL: postgresql://${DB_USER:-admin}:${DB_PASSWORD:-secret}@postgres:5432/${DB_NAME:-appdb}

      # Redis
      REDIS_URL: redis://:${REDIS_PASSWORD:-redissecret}@redis:6379/0

      # MinIO
      MINIO_ENDPOINT: minio:9000
      MINIO_ACCESS_KEY: ${MINIO_USER:-minioadmin}
      MINIO_SECRET_KEY: ${MINIO_PASSWORD:-minioadmin}
      MINIO_BUCKET: ${MINIO_BUCKET:-uploads}

      # App config
      SECRET_KEY: ${SECRET_KEY:-supersecretkey}
      ENVIRONMENT: ${ENVIRONMENT:-production}
      ALLOWED_ORIGINS: http://localhost:3000,https://yourdomain.com
    volumes:
      - ./backend/app:/app
      - api-uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      minio:
        condition: service_started
    networks:
      - frontend-net
      - backend-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Next.js Frontend
  web:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-http://localhost:8000}
    container_name: app-web
    environment:
      NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-http://localhost:8000}
      NODE_ENV: production
    ports:
      - "3000:3000"
    depends_on:
      api:
        condition: service_healthy
    networks:
      - frontend-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: app-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx-logs:/var/log/nginx
    depends_on:
      - web
      - api
    networks:
      - frontend-net
    restart: unless-stopped

volumes:
  postgres-data:
  redis-data:
  minio-data:
  api-uploads:
  nginx-logs:

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
```

### Backend Dockerfile (FastAPI)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile (Next.js)

```dockerfile
# frontend/Dockerfile

# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### FastAPI main.py (exemple)

```python
# backend/app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import redis
from minio import Minio

app = FastAPI(title="My API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Database connection
from .database import get_db

@app.get("/api/data")
async def get_data(db: Session = Depends(get_db)):
    # Your logic here
    return {"data": "example"}

# Redis cache example
redis_client = redis.Redis(
    host='redis',
    port=6379,
    password='redissecret',
    decode_responses=True
)

@app.get("/api/cache/{key}")
async def get_cache(key: str):
    value = redis_client.get(key)
    return {"key": key, "value": value}

# MinIO upload example
minio_client = Minio(
    "minio:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

@app.post("/api/upload")
async def upload_file(file: UploadFile):
    # Upload to MinIO
    minio_client.put_object(
        "uploads",
        file.filename,
        file.file,
        length=-1,
        part_size=10*1024*1024
    )
    return {"filename": file.filename}
```

### .env

```bash
# .env
# Database
DB_NAME=appdb
DB_USER=admin
DB_PASSWORD=supersecret

# Redis
REDIS_PASSWORD=redissecret

# MinIO
MINIO_USER=minioadmin
MINIO_PASSWORD=minioadmin123
MINIO_BUCKET=uploads

# API
SECRET_KEY=your-secret-key-here
ENVIRONMENT=production

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Commandes utiles

```bash
# Démarrer tout
docker compose up -d

# Logs
docker compose logs -f api web

# Rebuild après changements
docker compose up -d --build

# Shell dans le backend
docker exec -it app-api bash

# Console MinIO
# http://localhost:9001
# User: minioadmin / Pass: minioadmin

# Migrations database
docker exec app-api alembic upgrade head

# Tests
docker exec app-api pytest

# Backup
docker exec app-postgres pg_dump -U admin appdb | gzip > backup-$(date +%Y%m%d).sql.gz
```

---

## Stack complète avec MinIO

### docker-compose.yml production-ready

```yaml
version: '3.8'

services:
  # Load Balancer / Reverse Proxy
  traefik:
    image: traefik:v2.10
    container_name: traefik
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - traefik-certificates:/letsencrypt
    networks:
      - proxy-net
    restart: unless-stopped

  # ... (autres services comme avant)

  # Monitoring: Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - monitoring-net
    restart: unless-stopped

  # Monitoring: Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
    volumes:
      - grafana-data:/var/lib/grafana
    ports:
      - "3001:3000"
    depends_on:
      - prometheus
    networks:
      - monitoring-net
    restart: unless-stopped

volumes:
  traefik-certificates:
  prometheus-data:
  grafana-data:

networks:
  proxy-net:
  monitoring-net:
```

---

## Environnement de développement

### docker-compose.dev.yml

```yaml
version: '3.8'

services:
  # PostgreSQL avec pgAdmin
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: devdb
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres-dev-data:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres

  # Redis avec RedisInsight
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  redis-insight:
    image: redislabs/redisinsight:latest
    ports:
      - "8001:8001"

  # MailHog (SMTP test)
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP
      - "8025:8025"  # Web UI

  # API en mode dev
  api-dev:
    build:
      context: ./backend
      target: development
    volumes:
      - ./backend:/app
      - /app/node_modules
    command: uvicorn app.main:app --reload --host 0.0.0.0
    ports:
      - "8000:8000"
      - "5678:5678"  # Debugger
    environment:
      DATABASE_URL: postgresql://dev:dev@postgres:5432/devdb
      REDIS_URL: redis://redis:6379
      DEBUG: "true"

  # Frontend en mode dev
  web-dev:
    build:
      context: ./frontend
      target: development
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    command: npm run dev
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
      CHOKIDAR_USEPOLLING: "true"  # Hot reload

volumes:
  postgres-dev-data:
```

```bash
# Démarrer en mode dev
docker compose -f docker-compose.dev.yml up

# Accès aux outils:
# - Frontend: http://localhost:3000
# - API: http://localhost:8000/docs
# - pgAdmin: http://localhost:5050
# - Redis Insight: http://localhost:8001
# - MailHog: http://localhost:8025
```

---

## Stack de monitoring

### docker-compose.monitoring.yml

```yaml
version: '3.8'

services:
  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    ports:
      - "9090:9090"

  # Grafana
  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./grafana/datasources:/etc/grafana/provisioning/datasources:ro
    ports:
      - "3000:3000"

  # Node Exporter (métriques système)
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"

  # cAdvisor (métriques conteneurs)
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8080:8080"

  # Loki (logs)
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml

  # Promtail (collecteur de logs)
  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log:ro
      - ./promtail-config.yml:/etc/promtail/config.yml:ro
    command: -config.file=/etc/promtail/config.yml

volumes:
  prometheus-data:
  grafana-data:
```

---

## Scripts d'automatisation

### deploy.sh

```bash
#!/bin/bash
# deploy.sh - Script de déploiement

set -e

ENV=${1:-production}

echo "🚀 Déploiement en $ENV..."

# 1. Pull des dernières images
echo "📦 Pull des images..."
docker compose -f docker-compose.yml -f docker-compose.$ENV.yml pull

# 2. Backup avant déploiement
echo "💾 Backup de la base de données..."
./scripts/backup.sh

# 3. Déploiement
echo "🔄 Déploiement..."
docker compose -f docker-compose.yml -f docker-compose.$ENV.yml up -d

# 4. Vérification santé
echo "🏥 Vérification santé..."
sleep 10
docker compose ps

# 5. Tests
echo "🧪 Tests de smoke..."
curl -f http://localhost/health || exit 1

echo "✅ Déploiement réussi!"
```

### Commandes de référence

```bash
# Démarrage
docker compose up -d

# Logs
docker compose logs -f

# Rebuild
docker compose up -d --build

# Scale
docker compose up -d --scale api=3

# Arrêt
docker compose down

# Backup
./scripts/backup.sh

# Restauration
./scripts/restore.sh backup-20240101.tar.gz

# Monitoring
docker stats
```

---

[← Différences Linux/Windows](./infos-docker-12-differences-linux-windows.md) | [Index](./infos-docker-00-index.md)
