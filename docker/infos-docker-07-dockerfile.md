# 🐋 Dockerfile

[← Docker Compose](./infos-docker-06-compose.md) | [Index](./infos-docker-00-index.md) | [Registres et CI/CD →](./infos-docker-08-registres-cicd.md)

---

## Table des matières
- [Qu'est-ce qu'un Dockerfile ?](#quest-ce-quun-dockerfile)
- [Instructions de base](#instructions-de-base)
- [Multi-stage builds](#multi-stage-builds)
- [Best practices](#best-practices)
- [Optimisation](#optimisation)
- [Exemples complets](#exemples-complets)

---

## Qu'est-ce qu'un Dockerfile ?

### Définition

Un **Dockerfile** est un fichier texte contenant les **instructions** pour construire une image Docker.

```
Dockerfile → docker build → Image Docker → docker run → Conteneur
```

### Structure de base

```dockerfile
# Dockerfile
FROM ubuntu:22.04                    # Image de base

RUN apt-get update && \              # Exécuter des commandes
    apt-get install -y nginx

COPY index.html /var/www/html/       # Copier des fichiers

EXPOSE 80                            # Documenter les ports

CMD ["nginx", "-g", "daemon off;"]   # Commande par défaut
```

```bash
# Construire l'image
docker build -t mon-image:latest .

# Exécuter
docker run -d -p 80:80 mon-image:latest
```

---

## Instructions de base

### FROM - Image de base

```dockerfile
# Image officielle
FROM ubuntu:22.04

# Image spécifique
FROM node:18-alpine

# Multi-architecture
FROM --platform=linux/amd64 node:18

# Depuis une autre image buildée
FROM my-base-image:latest

# Image scratch (vide)
FROM scratch
# Pour binaires statiques (Go, Rust)
```

### WORKDIR - Répertoire de travail

```dockerfile
# Définir le workdir
WORKDIR /app

# Tout ce qui suit s'exécute dans /app
COPY . .
RUN npm install

# Créé automatiquement si n'existe pas
WORKDIR /app/src
```

### COPY vs ADD

```dockerfile
# COPY (recommandé) - Copie simple
COPY package.json /app/
COPY src/ /app/src/

# Avec wildcard
COPY *.json /app/

# Depuis un stage (multi-stage)
COPY --from=builder /app/dist /app/

# Avec permissions
COPY --chown=node:node package.json /app/

# ADD - Copie avec features supplémentaires
ADD https://example.com/file.tar.gz /app/  # Télécharge depuis URL
ADD archive.tar.gz /app/                    # Extrait automatiquement

# ❌ Utiliser ADD seulement pour extraction auto
# ✅ Utiliser COPY dans tous les autres cas
```

### RUN - Exécuter des commandes

```dockerfile
# Forme shell
RUN npm install

# Forme exec (recommandée)
RUN ["npm", "install"]

# Chaîner les commandes
RUN apt-get update && \
    apt-get install -y \
        curl \
        git \
        vim && \
    rm -rf /var/lib/apt/lists/*

# Installer des dépendances Node.js
RUN npm install --production

# Compiler du code
RUN go build -o app main.go
```

### CMD vs ENTRYPOINT

```dockerfile
# CMD - Commande par défaut (peut être overridée)
CMD ["node", "server.js"]
CMD node server.js         # Forme shell

# ENTRYPOINT - Point d'entrée fixe
ENTRYPOINT ["node"]
CMD ["server.js"]          # Arguments par défaut

# docker run image
# Exécute: node server.js

# docker run image app.js
# Exécute: node app.js

# Exemple: Script wrapper
ENTRYPOINT ["/entrypoint.sh"]
CMD ["start"]

# ENTRYPOINT seul
ENTRYPOINT ["nginx", "-g", "daemon off;"]
```

### ENV - Variables d'environnement

```dockerfile
# Définir une variable
ENV NODE_ENV production

# Plusieurs variables
ENV NODE_ENV=production \
    PORT=8080 \
    LOG_LEVEL=info

# Utiliser dans d'autres instructions
ENV APP_HOME /app
WORKDIR $APP_HOME

# Variables au build uniquement (ARG)
ARG VERSION=1.0.0
ENV APP_VERSION=$VERSION
```

### ARG - Arguments de build

```dockerfile
# Définir un argument
ARG NODE_VERSION=18

# Utiliser l'argument
FROM node:${NODE_VERSION}-alpine

# Avec default
ARG BUILD_DATE=unknown
ARG VERSION=latest

# Labels utilisant ARG
LABEL version="${VERSION}" \
      build_date="${BUILD_DATE}"
```

```bash
# Passer des arguments au build
docker build \
  --build-arg NODE_VERSION=20 \
  --build-arg VERSION=2.0.0 \
  -t mon-app:2.0.0 .
```

### EXPOSE - Documenter les ports

```dockerfile
# Port TCP (défaut)
EXPOSE 80

# Port UDP
EXPOSE 53/udp

# Plusieurs ports
EXPOSE 80 443 8080

# Variable
ARG PORT=8080
EXPOSE $PORT

# ⚠️ N'ouvre PAS le port, seulement documentation
# Utiliser -p lors du run
```

### USER - Utilisateur

```dockerfile
# Exécuter en tant qu'utilisateur non-root
USER node

# Créer un utilisateur
RUN useradd -m -u 1000 appuser
USER appuser

# Avec UID:GID
USER 1000:1000

# Revenir en root
USER root
```

### VOLUME - Points de montage

```dockerfile
# Déclarer un volume
VOLUME /data

# Plusieurs volumes
VOLUME ["/data", "/logs"]

# ⚠️ Crée un volume anonyme si pas monté explicitement
# Mieux: monter explicitement avec docker run -v
```

### LABEL - Métadonnées

```dockerfile
LABEL maintainer="dev@example.com"
LABEL version="1.0.0"
LABEL description="Mon application Docker"

# Plusieurs labels
LABEL org.opencontainers.image.authors="dev@example.com" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.vendor="MyCompany"
```

### HEALTHCHECK - Vérification de santé

```dockerfile
# Healthcheck simple
HEALTHCHECK CMD curl -f http://localhost/ || exit 1

# Avec options
HEALTHCHECK --interval=30s \
            --timeout=10s \
            --start-period=5s \
            --retries=3 \
  CMD curl -f http://localhost/health || exit 1

# Désactiver le healthcheck
HEALTHCHECK NONE
```

---

## Multi-stage builds

### Pourquoi multi-stage ?

```
Build stage:
- Outils de compilation
- Dépendances de développement
- Code source
→ Image volumineuse (1-2 Go)

Production stage:
- Seulement les binaires
- Dépendances de production
→ Image légère (50-100 Mo)
```

### Exemple Node.js

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copier package files
COPY package*.json ./

# Installer toutes les dépendances (dev + prod)
RUN npm ci

# Copier le code
COPY . .

# Build de l'application
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

WORKDIR /app

# Créer utilisateur non-root
RUN addgroup -g 1000 node && \
    adduser -u 1000 -G node -s /bin/sh -D node

# Copier seulement package files
COPY package*.json ./

# Installer seulement les dépendances de production
RUN npm ci --production

# Copier les fichiers buildés depuis le stage builder
COPY --from=builder /app/dist ./dist

# Changer ownership
RUN chown -R node:node /app

# Utiliser l'utilisateur non-root
USER node

# Exposer le port
EXPOSE 3000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD node healthcheck.js

# Commande de démarrage
CMD ["node", "dist/server.js"]
```

### Exemple Go

```dockerfile
# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copier go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copier le code source
COPY . .

# Build du binaire statique
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

# Stage 2: Production (scratch = image vide)
FROM scratch

# Copier les certificats SSL
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copier le binaire
COPY --from=builder /app/app /app

# Exposer le port
EXPOSE 8080

# Exécuter
ENTRYPOINT ["/app"]
```

### Exemple Python/FastAPI

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Installer les dépendances de build
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .

# Créer virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim

WORKDIR /app

# Copier le virtual environment depuis builder
COPY --from=builder /opt/venv /opt/venv

# Copier le code de l'application
COPY . .

# Activer le virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Exposer le port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build avec target

```bash
# Builder l'image finale (par défaut)
docker build -t mon-app:latest .

# Builder seulement le stage builder
docker build --target builder -t mon-app:builder .

# Utile pour debug ou tests
docker run -it mon-app:builder sh
```

---

## Best practices

### 1. Ordre des layers

```dockerfile
# ❌ MAUVAIS: Invalide le cache à chaque changement de code
FROM node:18-alpine
WORKDIR /app
COPY . .                    # Copie TOUT
RUN npm install             # Réinstalle à chaque changement !

# ✅ BON: Cache optimisé
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./       # Copie seulement les fichiers de dépendances
RUN npm install             # Réutilise le cache si package.json inchangé
COPY . .                    # Copie le code après
```

### 2. Minimiser les layers

```dockerfile
# ❌ MAUVAIS: Trop de layers
FROM ubuntu:22.04
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get clean

# ✅ BON: Un seul layer
FROM ubuntu:22.04
RUN apt-get update && \
    apt-get install -y \
        curl \
        git \
        vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Images de base légères

```dockerfile
# ❌ Grande image (1 Go+)
FROM node:18

# ✅ Image alpine (100-200 Mo)
FROM node:18-alpine

# ✅ Image slim (200-300 Mo)
FROM node:18-slim

# ✅ Distroless (50-100 Mo)
FROM gcr.io/distroless/nodejs18
```

### 4. .dockerignore

```
# .dockerignore
node_modules
npm-debug.log
.env
.git
.gitignore
README.md
.vscode
.idea
*.md
coverage
.DS_Store
dist
build
*.log
```

### 5. Utilisateur non-root

```dockerfile
# ✅ Créer et utiliser un utilisateur non-root
FROM node:18-alpine

WORKDIR /app

# Copier les fichiers
COPY package*.json ./
RUN npm ci --production

COPY . .

# Node image a déjà un user 'node'
RUN chown -R node:node /app
USER node

CMD ["node", "server.js"]
```

### 6. Secrets et sensibilité

```dockerfile
# ❌ MAUVAIS: Ne JAMAIS inclure de secrets
ENV API_KEY=sk-1234567890abcdef
ENV DATABASE_PASSWORD=secret123

# ✅ BON: Passer via variables d'environnement
# docker run -e API_KEY=$API_KEY

# ✅ BON: Utiliser Docker secrets (Swarm)
# ou des gestionnaires de secrets externes
```

### 7. Labels et métadonnées

```dockerfile
LABEL maintainer="dev@example.com" \
      version="1.0.0" \
      description="Application de production" \
      org.opencontainers.image.source="https://github.com/user/repo"
```

---

## Optimisation

### Cache de layers

```dockerfile
# Profiter du cache Docker

# 1. Instructions stables en premier
FROM node:18-alpine
WORKDIR /app

# 2. Dépendances (changent rarement)
COPY package*.json ./
RUN npm ci --production

# 3. Code applicatif (change souvent)
COPY . .

# Si seulement le code change, les layers 1-2 sont en cache !
```

### Réduire la taille

```bash
# 1. Images de base légères
FROM node:18-alpine    # au lieu de node:18

# 2. Multi-stage builds
# Séparer build et runtime

# 3. Nettoyer après installation
RUN apt-get update && \
    apt-get install -y package && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. npm/yarn
RUN npm ci --production         # Pas npm install
RUN npm cache clean --force     # Nettoyer le cache

# 5. Supprimer fichiers inutiles
RUN rm -rf /tmp/* /var/tmp/*
```

### Build args pour optimisation

```dockerfile
ARG BUILD_ENV=production

FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Installer selon l'environnement
RUN if [ "$BUILD_ENV" = "development" ]; then \
        npm install; \
    else \
        npm ci --production; \
    fi

COPY . .
```

```bash
# Build pour dev
docker build --build-arg BUILD_ENV=development -t app:dev .

# Build pour prod
docker build --build-arg BUILD_ENV=production -t app:prod .
```

---

## Exemples complets

### React Application

```dockerfile
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source et build
COPY . .
RUN npm run build

# Stage 2: Production avec Nginx
FROM nginx:alpine

# Copier le build depuis builder
COPY --from=builder /app/build /usr/share/nginx/html

# Copier config Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port
EXPOSE 80

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Nginx démarre automatiquement
```

### Next.js Application

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copier les fichiers nécessaires
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### FastAPI + PostgreSQL

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY . .

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Exposer le port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Script d'entrée
COPY --chown=appuser:appuser entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go Application

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /build

# Copier go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copier le source
COPY . .

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags="-w -s" -o app .

# Production stage
FROM scratch

# Copier certificats SSL
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copier le binaire
COPY --from=builder /build/app /app

# Copier les fichiers statiques si nécessaire
COPY --from=builder /build/static /static

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s \
  CMD ["/app", "healthcheck"]

ENTRYPOINT ["/app"]
```

---

## Commandes Docker build

```bash
# Build basique
docker build -t mon-image:latest .

# Build avec tag multiple
docker build -t mon-image:latest -t mon-image:1.0.0 .

# Build avec Dockerfile personnalisé
docker build -f Dockerfile.dev -t mon-image:dev .

# Build avec build args
docker build --build-arg VERSION=1.0.0 -t mon-image:1.0.0 .

# Build sans cache
docker build --no-cache -t mon-image:latest .

# Build avec target spécifique (multi-stage)
docker build --target builder -t mon-image:builder .

# Build avec progression simple
docker build --progress=plain -t mon-image:latest .

# Build pour une plateforme spécifique
docker build --platform linux/amd64 -t mon-image:latest .

# Build et push
docker build -t user/image:latest . && docker push user/image:latest

# Buildx (multi-plateforme)
docker buildx build --platform linux/amd64,linux/arm64 -t user/image:latest --push .
```

---

## Commandes de référence rapide

```bash
# Build
docker build -t nom:tag .                # Build image
docker build --no-cache .                # Sans cache
docker build --target stage .            # Multi-stage

# Analyse
docker history image                     # Voir les layers
docker inspect image                     # Détails de l'image

# Tags
docker tag source:tag target:tag         # Créer un tag

# Nettoyage
docker image prune                       # Supprimer images non utilisées
docker builder prune                     # Nettoyer le cache de build
```

---

[← Docker Compose](./infos-docker-06-compose.md) | [Index](./infos-docker-00-index.md) | [Registres et CI/CD →](./infos-docker-08-registres-cicd.md)
