# 🎼 Docker Compose

[← Réseaux](./infos-docker-05-reseaux.md) | [Index](./infos-docker-00-index.md) | [Dockerfile →](./infos-docker-07-dockerfile.md)

---

## Table des matières
- [Qu'est-ce que Docker Compose ?](#quest-ce-que-docker-compose)
- [Installation](#installation)
- [Fichier docker-compose.yml](#fichier-docker-composeyml)
- [Commandes Compose](#commandes-compose)
- [Services](#services)
- [Volumes et réseaux](#volumes-et-reseaux)
- [Variables d'environnement](#variables-denvironnement)
- [Dépendances et healthchecks](#dependances-et-healthchecks)
- [Exemples complets](#exemples-complets)

---

## Qu'est-ce que Docker Compose ?

### Définition

**Docker Compose** est un outil pour **définir et exécuter des applications Docker multi-conteneurs**.

```
Sans Compose:
docker network create app-net
docker volume create db-data
docker run -d --name db --network app-net -v db-data:/var/lib/postgresql/data postgres
docker run -d --name api --network app-net -p 8080:8080 -e DATABASE_URL=... api-image
docker run -d --name web --network app-net -p 80:80 web-image

Avec Compose:
docker-compose up
✅ Tout démarre en une commande !
```

### Avantages

```
✅ Configuration as Code (docker-compose.yml)
✅ Gestion simplifiée des applications multi-conteneurs
✅ Environnements reproductibles
✅ Commandes simples (up, down, ps, logs)
✅ Idéal pour développement et tests
✅ Facilite les déploiements
```

---

## Installation

### Linux

```bash
# Méthode 1: Via Docker Desktop (inclut Compose v2)
# Installer Docker Desktop

# Méthode 2: Plugin Docker Compose (recommandé)
# Compose v2 est intégré comme plugin docker compose

# Vérifier l'installation
docker compose version
# Docker Compose version v2.xx.x

# Méthode 3: Standalone binary (ancienne version)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### Windows / macOS

```bash
# Docker Desktop inclut Docker Compose automatiquement

# Vérifier
docker compose version
# ou
docker-compose --version
```

### Note: v1 vs v2

```bash
# Compose v1 (ancienne syntaxe)
docker-compose up

# Compose v2 (nouvelle syntaxe - recommandée)
docker compose up

# Ce guide utilise la syntaxe v2
```

---

## Fichier docker-compose.yml

### Structure de base

```yaml
version: '3.8'  # Version du format Compose

services:       # Définition des conteneurs
  web:
    image: nginx:alpine
    ports:
      - "80:80"

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret

volumes:        # Volumes persistants
  db-data:

networks:       # Réseaux personnalisés
  app-network:
```

### Exemple minimal

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

```bash
# Démarrer
docker compose up

# Accéder à http://localhost:8080
```

---

## Commandes Compose

### Commandes principales

```bash
# Démarrer les services
docker compose up
# Démarre tous les services définis

# En arrière-plan (detached)
docker compose up -d

# Rebuild + start
docker compose up --build

# Arrêter les services
docker compose down
# Arrête et supprime les conteneurs

# Arrêter sans supprimer
docker compose stop

# Redémarrer
docker compose restart

# Voir les services en cours
docker compose ps

# Logs
docker compose logs
docker compose logs -f          # Suivre en temps réel
docker compose logs web         # Logs d'un service spécifique

# Exécuter une commande
docker compose exec web sh
docker compose exec db psql -U postgres

# Construire les images
docker compose build

# Pull les images
docker compose pull

# Voir la configuration
docker compose config
```

### Gestion avancée

```bash
# Démarrer un service spécifique
docker compose up web

# Scaler un service
docker compose up --scale web=3

# Supprimer tout (conteneurs, réseaux, volumes)
docker compose down -v

# Supprimer seulement les conteneurs et réseaux
docker compose down

# Pause / unpause
docker compose pause
docker compose unpause

# Voir les processus
docker compose top

# Événements en temps réel
docker compose events

# Valider le fichier compose
docker compose config --quiet
```

---

## Services

### Définir un service

```yaml
version: '3.8'

services:
  web:
    image: nginx:alpine               # Image à utiliser
    container_name: mon-nginx         # Nom du conteneur
    ports:
      - "8080:80"                     # Port mapping
    volumes:
      - ./html:/usr/share/nginx/html  # Bind mount
      - nginx-logs:/var/log/nginx     # Volume nommé
    environment:
      - ENV_VAR=value                 # Variables d'env
    restart: unless-stopped           # Politique redémarrage
    networks:
      - frontend                      # Réseaux
    depends_on:
      - api                           # Dépendances

volumes:
  nginx-logs:

networks:
  frontend:
```

### Build custom image

```yaml
services:
  api:
    build:
      context: ./api              # Dossier avec Dockerfile
      dockerfile: Dockerfile      # Nom du Dockerfile
      args:
        - NODE_ENV=production     # Build args
    image: my-api:latest          # Tag de l'image
    ports:
      - "8080:8080"
```

### Build avancé

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
      target: production          # Multi-stage build
      args:
        VERSION: "1.0.0"
      cache_from:
        - my-app:latest
    image: my-app:1.0.0
```

---

## Volumes et réseaux

### Volumes dans Compose

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      # Volume nommé
      - postgres-data:/var/lib/postgresql/data

      # Bind mount
      - ./init-scripts:/docker-entrypoint-initdb.d:ro

      # Volume anonyme
      - /var/lib/postgresql/backups

  web:
    image: nginx
    volumes:
      # Bind mount relatif
      - ./html:/usr/share/nginx/html

      # Bind mount absolu
      - /host/logs:/var/log/nginx

      # Volume from another service
      - data-volume:/data

# Définition des volumes
volumes:
  postgres-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /path/on/host

  data-volume:
    external: true  # Volume existant
```

### Réseaux dans Compose

```yaml
version: '3.8'

services:
  web:
    image: nginx
    networks:
      - frontend

  api:
    image: my-api
    networks:
      - frontend
      - backend

  db:
    image: postgres
    networks:
      - backend

# Définition des réseaux
networks:
  frontend:
    driver: bridge

  backend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

  # Réseau existant
  external-net:
    external: true
    name: existing-network
```

---

## Variables d'environnement

### Fichier .env

```bash
# .env
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=mydb
API_PORT=8080
NODE_ENV=production
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      # Utiliser les variables du .env
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}

  api:
    image: my-api
    ports:
      - "${API_PORT}:8080"
    environment:
      NODE_ENV: ${NODE_ENV}
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```

```bash
# Démarrer avec le .env
docker compose up
# Les variables sont automatiquement chargées
```

### env_file

```yaml
services:
  web:
    image: my-app
    env_file:
      - .env.common      # Variables communes
      - .env.production  # Variables d'env spécifiques
```

### Variables complexes

```yaml
services:
  app:
    image: my-app
    environment:
      # String simple
      - ENV=production

      # Liste
      - ALLOWED_HOSTS=host1,host2,host3

      # JSON
      - CONFIG={"debug": false, "port": 8080}

      # Depuis .env
      - DATABASE_URL=${DATABASE_URL}

      # Avec default
      - LOG_LEVEL=${LOG_LEVEL:-info}
```

---

## Dépendances et healthchecks

### Depends_on

```yaml
version: '3.8'

services:
  web:
    image: nginx
    depends_on:
      - api

  api:
    image: my-api
    depends_on:
      - db
      - redis

  db:
    image: postgres:15

  redis:
    image: redis:7

# Ordre de démarrage:
# 1. db, redis
# 2. api
# 3. web
```

### Healthchecks

```yaml
services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s

  api:
    image: my-api
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  web:
    image: nginx
    depends_on:
      api:
        condition: service_healthy
```

---

## Exemples complets

### Exemple 1: Stack NGINX + PostgreSQL

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: postgres-db
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    ports:
      - "5432:5432"
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d myapp"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    image: nginx:alpine
    container_name: nginx-web
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./html:/usr/share/nginx/html:ro
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - nginx-logs:/var/log/nginx
    networks:
      - frontend
    restart: unless-stopped
    depends_on:
      - db

volumes:
  postgres-data:
  nginx-logs:

networks:
  frontend:
  backend:
```

```bash
# Démarrer
docker compose up -d

# Logs
docker compose logs -f

# Arrêter
docker compose down
```

### Exemple 2: Stack complète (Web + API + DB + Cache)

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Frontend
  web:
    image: nginx:alpine
    container_name: frontend
    ports:
      - "80:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html:ro
      - ./frontend/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - frontend-net
    depends_on:
      - api
    restart: unless-stopped

  # Backend API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: backend-api
    ports:
      - "8080:8080"
    environment:
      NODE_ENV: production
      DATABASE_URL: postgresql://postgres:secret@db:5432/myapp
      REDIS_URL: redis://redis:6379
      PORT: 8080
    volumes:
      - ./backend/uploads:/app/uploads
      - api-logs:/app/logs
    networks:
      - frontend-net
      - backend-net
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Database
  db:
    image: postgres:15-alpine
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d:ro
    networks:
      - backend-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Cache Redis
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - backend-net
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Admin tools (optional)
  adminer:
    image: adminer:latest
    container_name: adminer
    ports:
      - "8081:8080"
    environment:
      ADMINER_DEFAULT_SERVER: db
    networks:
      - backend-net
    depends_on:
      - db
    restart: unless-stopped

volumes:
  postgres-data:
  redis-data:
  api-logs:

networks:
  frontend-net:
  backend-net:
```

```bash
# .env
NODE_ENV=production
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
API_PORT=8080
```

### Exemple 3: Stack de développement

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  web:
    build:
      context: ./frontend
      target: development
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev
    ports:
      - "3000:3000"
    environment:
      - CHOKIDAR_USEPOLLING=true  # Hot reload
    networks:
      - dev-net

  api:
    build:
      context: ./backend
      target: development
    volumes:
      - ./backend:/app
      - /app/node_modules
    command: npm run dev
    ports:
      - "8080:8080"
      - "9229:9229"  # Debug port
    environment:
      NODE_ENV: development
      DATABASE_URL: postgresql://dev:dev@db:5432/devdb
      REDIS_URL: redis://redis:6379
    networks:
      - dev-net
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: devdb
    volumes:
      - dev-postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - dev-net

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - dev-net

volumes:
  dev-postgres-data:

networks:
  dev-net:
```

```bash
# Développement
docker compose -f docker-compose.dev.yml up

# Production
docker compose -f docker-compose.yml up -d
```

---

## Profiles

```yaml
version: '3.8'

services:
  web:
    image: nginx
    # Toujours démarré

  db:
    image: postgres
    # Toujours démarré

  debug-tools:
    image: busybox
    profiles:
      - debug
    # Démarré seulement avec --profile debug

  test-runner:
    image: test-image
    profiles:
      - test
    # Démarré seulement avec --profile test
```

```bash
# Démarrage normal
docker compose up
# Démarre: web, db

# Avec profile debug
docker compose --profile debug up
# Démarre: web, db, debug-tools

# Avec profile test
docker compose --profile test up
# Démarre: web, db, test-runner
```

---

## Extensions et réutilisation

### Extension avec x-

```yaml
version: '3.8'

# Template réutilisable
x-common-config: &common
  restart: unless-stopped
  logging:
    driver: json-file
    options:
      max-size: "10m"
      max-file: "3"

services:
  web:
    <<: *common  # Utilise le template
    image: nginx

  api:
    <<: *common  # Utilise le template
    image: my-api

  db:
    <<: *common  # Utilise le template
    image: postgres
```

### Override files

```yaml
# docker-compose.yml (base)
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "80:80"

# docker-compose.override.yml (auto-chargé)
version: '3.8'
services:
  web:
    environment:
      - DEBUG=true
    volumes:
      - ./logs:/var/log/nginx

# docker-compose.prod.yml (spécifique)
version: '3.8'
services:
  web:
    restart: always
    environment:
      - DEBUG=false
```

```bash
# Utilise automatiquement base + override
docker compose up

# Utiliser un fichier spécifique
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## Best practices

```yaml
# ✅ BON: Structure claire et commentée
version: '3.8'

services:
  # Frontend web server
  web:
    image: nginx:alpine
    container_name: web-server
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html:ro
    networks:
      - frontend
    restart: unless-stopped
    depends_on:
      api:
        condition: service_healthy

  # Backend API
  api:
    build: ./api
    environment:
      DATABASE_URL: ${DATABASE_URL}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
    networks:
      - frontend
      - backend

# ✅ Variables dans .env
# ✅ Healthchecks pour dépendances
# ✅ Réseaux pour isolation
# ✅ Volumes nommés pour persistance
# ✅ Restart policies
# ✅ Container names explicites
# ✅ Read-only mounts quand possible
```

---

## Commandes de référence rapide

```bash
# Démarrage
docker compose up                        # Démarrer
docker compose up -d                     # Detached
docker compose up --build                # Rebuild + start

# Arrêt
docker compose down                      # Stop + remove
docker compose down -v                   # + remove volumes
docker compose stop                      # Stop (garde conteneurs)

# Gestion
docker compose ps                        # Statut services
docker compose logs -f                   # Logs temps réel
docker compose exec service bash         # Shell interactif
docker compose restart                   # Redémarrer

# Build
docker compose build                     # Builder images
docker compose build --no-cache          # Sans cache

# Validation
docker compose config                    # Voir config
docker compose config --quiet            # Valider syntaxe
```

---

[← Réseaux](./infos-docker-05-reseaux.md) | [Index](./infos-docker-00-index.md) | [Dockerfile →](./infos-docker-07-dockerfile.md)
