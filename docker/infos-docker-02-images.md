# 🖼️ Images Docker

[← Introduction](./infos-docker-01-introduction-installation.md) | [Index](./infos-docker-00-index.md) | [Conteneurs →](./infos-docker-03-conteneurs.md)

---

## Table des matières
- [Qu'est-ce qu'une image Docker ?](#quest-ce-quune-image-docker)
- [Gestion des images](#gestion-des-images)
- [Construire des images](#construire-des-images)
- [Registres d'images](#registres-dimages)
- [Optimisation des images](#optimisation-des-images)

---

## Qu'est-ce qu'une image Docker ?

### Définition
Une **image Docker** est un **template immuable** (qui ne change pas) qui contient tout ce dont une application a besoin pour s'exécuter:
- Le code de l'application
- Le runtime (Node.js, Python, Java, etc.)
- Les librairies et dépendances
- Les variables d'environnement
- Les fichiers de configuration

### Architecture en couches (layers)

Les images Docker sont construites en **couches superposées**. Chaque instruction dans un Dockerfile créé une nouvelle couche.

```
┌─────────────────────────────┐
│   Application (app.js)      │ ← Couche 5
├─────────────────────────────┤
│   node_modules              │ ← Couche 4
├─────────────────────────────┤
│   npm install               │ ← Couche 3
├─────────────────────────────┤
│   Node.js 18                │ ← Couche 2
├─────────────────────────────┤
│   Ubuntu base               │ ← Couche 1
└─────────────────────────────┘
```

**Avantages:**
- **Réutilisation**: Les couches communes sont partagées entre images
- **Cache**: Lors du rebuild, seules les couches modifiées sont reconstruites
- **Économie d'espace**: Plusieurs images peuvent partager les mêmes couches de base

---

## Gestion des images

### Lister les images

```bash
# Lister toutes les images locales
docker images
# Affiche: REPOSITORY, TAG, IMAGE ID, CREATED, SIZE

# Ou syntaxe alternative
docker image ls

# Afficher avec plus de détails
docker images --all --no-trunc
# --all: inclut les images intermédiaires
# --no-trunc: affiche les IDs complets

# Afficher seulement les IDs
docker images -q

# Filtrer les images
docker images --filter "dangling=true"
# Images "dangling" = sans tag (orphelines)

docker images --filter "reference=nginx:*"
# Toutes les versions de nginx

docker images --filter "before=nginx:latest"
# Images créées avant nginx:latest

docker images --filter "since=ubuntu:22.04"
# Images créées après ubuntu:22.04

# Format personnalisé
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### Télécharger une image (Pull)

```bash
# Télécharger depuis Docker Hub (par défaut)
docker pull nginx
# Télécharge la version "latest" (dernière)

# Télécharger une version spécifique
docker pull nginx:1.25.3
# Format: IMAGE:TAG
# ⚠️ Toujours spécifier la version en production !

# Télécharger depuis un autre registre
docker pull registry.gitlab.com/mon-projet/mon-app:latest
docker pull ghcr.io/username/mon-app:v1.0
docker pull myregistry.azurecr.io/mon-app:latest

# Télécharger toutes les versions (tags) d'une image
docker pull --all-tags ubuntu
# ⚠️ Peut télécharger plusieurs Go de données !

# Télécharger pour une plateforme spécifique
docker pull --platform linux/amd64 nginx
docker pull --platform linux/arm64 nginx
# Utile pour Mac M1/M2 ou serveurs ARM

# Voir la progression du téléchargement
docker pull postgres:15
# Affiche chaque couche téléchargée:
# f1ca037084ed: Downloading [=====>    ] 10.5MB/45.5MB
```

### Rechercher des images

```bash
# Rechercher sur Docker Hub
docker search nginx
# Affiche: NAME, DESCRIPTION, STARS, OFFICIAL, AUTOMATED

# Limiter les résultats
docker search --limit 5 nginx

# Filtrer par étoiles
docker search --filter stars=100 nginx

# Filtrer par images officielles
docker search --filter is-official=true nginx

# Format personnalisé
docker search --format "table {{.Name}}\t{{.Stars}}\t{{.IsOfficial}}" nginx
```

### Inspecter une image

```bash
# Voir tous les détails d'une image
docker image inspect nginx:latest
# Retourne un JSON avec:
# - Layers (couches)
# - Taille
# - Date de création
# - Architecture
# - OS
# - Commandes
# - Variables d'environnement
# - Ports exposés
# - Volumes

# Extraire une information spécifique avec --format
docker image inspect nginx:latest --format='{{.Size}}'
# Affiche la taille en bytes

docker image inspect nginx:latest --format='{{.Architecture}}'
# Affiche: amd64, arm64, etc.

docker image inspect nginx:latest --format='{{.Os}}'
# Affiche: linux, windows

docker image inspect nginx:latest --format='{{.Config.Cmd}}'
# Affiche la commande de démarrage par défaut

docker image inspect nginx:latest --format='{{.Config.ExposedPorts}}'
# Affiche les ports exposés

docker image inspect nginx:latest --format='{{.Config.Env}}'
# Affiche les variables d'environnement

# Voir l'historique des layers
docker history nginx:latest
# Affiche chaque couche avec:
# - IMAGE: ID de la couche
# - CREATED: Date de création
# - CREATED BY: Commande utilisée
# - SIZE: Taille de la couche

# Format lisible
docker history --no-trunc nginx:latest
# Affiche les commandes complètes
```

### Tagger une image

```bash
# Un tag est comme un "alias" pour une image
# Il ne duplique pas l'image, juste créé un nouveau pointeur

# Créer un tag "latest" pour une version
docker tag mon-app:1.0 mon-app:latest

# Tagger pour un registre privé
docker tag mon-app:1.0 registry.gitlab.com/username/mon-app:1.0
docker tag mon-app:1.0 registry.gitlab.com/username/mon-app:latest

# Convention de nommage
# Format: [REGISTRE/][NAMESPACE/]IMAGE:TAG
# Exemples:
docker tag mon-app:1.0 docker.io/username/mon-app:1.0  # Docker Hub
docker tag mon-app:1.0 registry.gitlab.com/group/project/mon-app:1.0  # GitLab
docker tag mon-app:1.0 ghcr.io/username/mon-app:1.0  # GitHub
docker tag mon-app:1.0 myregistry.azurecr.io/mon-app:1.0  # Azure

# Stratégie de tags recommandée
docker tag mon-app:1.0.5 mon-app:1.0.5  # Version exacte
docker tag mon-app:1.0.5 mon-app:1.0    # Version mineure
docker tag mon-app:1.0.5 mon-app:1      # Version majeure
docker tag mon-app:1.0.5 mon-app:latest # Dernière version
```

### Supprimer des images

```bash
# Supprimer une image par nom et tag
docker rmi nginx:latest
# ou
docker image rm nginx:latest

# Supprimer une image par ID
docker rmi abc123def456

# Supprimer plusieurs images
docker rmi nginx:latest postgres:15 redis:7

# Forcer la suppression (même si l'image est utilisée)
docker rmi -f nginx:latest
# ⚠️ À éviter ! Mieux vaut arrêter/supprimer les conteneurs d'abord

# Supprimer toutes les images "dangling" (sans tag)
docker image prune
# Demande confirmation
# Supprime les images comme: <none>:<none>

# Supprimer sans confirmation
docker image prune -f

# Supprimer TOUTES les images non utilisées (même avec tag)
docker image prune -a
# ⚠️ ATTENTION: Supprime toutes les images non liées à un conteneur

# Supprimer les images de plus de 7 jours
docker image prune -a --filter "until=168h"
# 168h = 7 jours

# Supprimer toutes les images locales
docker rmi $(docker images -q)
# ⚠️ Très destructif ! À utiliser avec prudence

# Supprimer toutes les images d'un repository
docker rmi $(docker images nginx -q)
```

---

## Construire des images

### Avec docker build

```bash
# Construire depuis un Dockerfile dans le répertoire courant
docker build -t mon-app:1.0 .
# -t : tag (nom:version) de l'image
# .  : contexte de build (répertoire contenant le Dockerfile)

# Construire avec un Dockerfile spécifique
docker build -f Dockerfile.dev -t mon-app:dev .
# -f : spécifier le fichier Dockerfile

# Construire sans utiliser le cache
docker build --no-cache -t mon-app:1.0 .
# Utile quand on veut forcer le téléchargement de nouvelles dépendances

# Construire avec des arguments (ARG)
docker build --build-arg NODE_VERSION=18 -t mon-app:1.0 .
# Les ARG définis dans le Dockerfile peuvent être passés ainsi

# Exemple de Dockerfile avec ARG
# FROM node:${NODE_VERSION}
# ARG NODE_VERSION=16
# docker build --build-arg NODE_VERSION=18 -t mon-app .

# Construire pour plusieurs plateformes (multi-platform)
docker buildx build --platform linux/amd64,linux/arm64 -t mon-app:1.0 .
# Utile pour Mac M1/M2 ou serveurs ARM

# Construire et pousser directement
docker buildx build --platform linux/amd64,linux/arm64 \
  -t registry.gitlab.com/user/mon-app:1.0 \
  --push .

# Voir les layers créées pendant le build
docker build --progress=plain -t mon-app:1.0 .
# Affiche chaque étape en détail

# Construire avec un tag spécifique pour un stage
docker build --target production -t mon-app:prod .
# Utile avec multi-stage builds
```

### Multi-stage builds

Les **multi-stage builds** permettent de créer des images optimisées en séparant la phase de build de la phase de production.

```dockerfile
# Stage 1: Builder (avec tous les outils de build)
FROM node:18 AS builder
WORKDIR /app

# Installer les dépendances
COPY package*.json ./
RUN npm ci

# Copier le code source
COPY . .

# Build de l'application
RUN npm run build

# Stage 2: Production (image finale légère)
FROM node:18-slim
WORKDIR /app

# Copier uniquement les fichiers nécessaires depuis le stage builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .

# Variables d'environnement
ENV NODE_ENV=production

# Commande de démarrage
CMD ["node", "dist/index.js"]
```

**Avantages:**
- ✅ Image finale beaucoup plus légère (pas d'outils de build)
- ✅ Meilleure sécurité (moins de surface d'attaque)
- ✅ Temps de build plus rapide avec le cache

```bash
# Construire l'image multi-stage
docker build -t mon-app:prod .
# Seul le stage final (production) est dans l'image finale

# Construire jusqu'à un stage spécifique
docker build --target builder -t mon-app:builder .
# Utile pour le debug ou les tests
```

---

## Registres d'images

### Se connecter à un registre

```bash
# Docker Hub (par défaut)
docker login
# Demande username et password

# GitLab Container Registry
docker login registry.gitlab.com
docker login registry.gitlab.com -u username -p ACCESS_TOKEN

# GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u username --password-stdin

# Azure Container Registry
docker login myregistry.azurecr.io -u username -p password

# AWS ECR (nécessite AWS CLI)
aws ecr get-login-password --region region | \
    docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com

# Se déconnecter
docker logout
docker logout registry.gitlab.com
```

### Pousser une image (Push)

```bash
# Tagger l'image pour le registre
docker tag mon-app:1.0 registry.gitlab.com/username/mon-app:1.0

# Pousser l'image
docker push registry.gitlab.com/username/mon-app:1.0

# Pousser plusieurs tags
docker push registry.gitlab.com/username/mon-app:1.0
docker push registry.gitlab.com/username/mon-app:latest

# Pousser tous les tags d'une image
docker push --all-tags registry.gitlab.com/username/mon-app
```

---

## Optimisation des images

### Principes de base

```dockerfile
# ❌ MAUVAIS: Image lourde, beaucoup de layers
FROM ubuntu:latest
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y curl
RUN apt install -y git
RUN pip3 install flask
RUN pip3 install requests
COPY . /app

# ✅ BON: Image optimisée
FROM python:3.11-slim
# Utiliser une image de base légère

# Combiner les RUN en une seule couche
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask requests

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "app.py"]
```

### Techniques d'optimisation

#### 1. Utiliser des images de base légères

```dockerfile
# Images Alpine (très légères)
FROM node:18-alpine     # ~180 MB vs node:18 ~900 MB
FROM python:3.11-alpine # ~50 MB vs python:3.11 ~900 MB
FROM nginx:alpine       # ~40 MB vs nginx:latest ~140 MB

# Images slim (compromis taille/fonctionnalités)
FROM node:18-slim       # ~250 MB
FROM python:3.11-slim   # ~125 MB

# Image scratch (vide, pour binaires statiques)
FROM scratch
COPY mybinary /
CMD ["/mybinary"]
```

#### 2. Ordre des instructions (cache)

```dockerfile
# ❌ MAUVAIS: Le cache est invalidé à chaque changement de code
FROM node:18
WORKDIR /app
COPY . .
RUN npm install

# ✅ BON: Les dépendances sont cachées si package.json ne change pas
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
```

#### 3. Nettoyer dans le même RUN

```dockerfile
# ❌ MAUVAIS: Les fichiers temporaires restent dans la couche
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*

# ✅ BON: Tout est dans la même couche
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

#### 4. Utiliser .dockerignore

```bash
# .dockerignore (comme .gitignore)
# Exclut les fichiers inutiles du contexte de build

node_modules
npm-debug.log
.git
.env
.env.local
README.md
*.md
tests/
*.test.js
coverage/
.vscode/
.idea/
.DS_Store
Thumbs.db
```

#### 5. Multi-stage builds

Déjà expliqué ci-dessus - c'est la meilleure technique pour réduire la taille !

### Exemples de comparaison

```bash
# Taille des images selon l'optimisation

# Non optimisé
mon-app:v1  1.2 GB

# Avec Alpine + nettoyage
mon-app:v2  350 MB

# Avec multi-stage build
mon-app:v3  180 MB

# Vérifier la taille
docker images mon-app
```

---

## Sauvegarder et charger des images

### Export/Import d'images

```bash
# Sauvegarder une image dans un fichier tar
docker save -o mon-app.tar mon-app:1.0
# Créé un fichier mon-app.tar

# Sauvegarder plusieurs images
docker save -o mes-images.tar mon-app:1.0 postgres:15 redis:7

# Avec compression (gzip)
docker save mon-app:1.0 | gzip > mon-app.tar.gz

# Charger une image depuis un fichier tar
docker load -i mon-app.tar
# Restaure l'image avec son tag d'origine

# Charger depuis un fichier compressé
gunzip < mon-app.tar.gz | docker load

# Ou en une commande
docker load < mon-app.tar.gz
```

### Cas d'usage

```bash
# Transférer des images sans registre
# Machine A:
docker save mon-app:1.0 | gzip > mon-app.tar.gz
# Copier mon-app.tar.gz vers Machine B
# Machine B:
gunzip < mon-app.tar.gz | docker load

# Backup d'images importantes
docker save $(docker images -q) | gzip > all-images-backup.tar.gz

# Restaurer toutes les images
gunzip < all-images-backup.tar.gz | docker load
```

---

## Commandes de référence rapide

```bash
# Gestion de base
docker images                      # Lister les images
docker pull IMAGE:TAG              # Télécharger
docker build -t NAME:TAG .         # Construire
docker tag SOURCE TARGET           # Tagger
docker push IMAGE:TAG              # Pousser vers registre
docker rmi IMAGE                   # Supprimer

# Inspection
docker image inspect IMAGE         # Détails complets
docker history IMAGE               # Historique des couches

# Nettoyage
docker image prune                 # Supprimer images dangling
docker image prune -a              # Supprimer images non utilisées
docker rmi $(docker images -q)     # Supprimer toutes les images

# Registres
docker login [REGISTRE]            # Se connecter
docker logout [REGISTRE]           # Se déconnecter
docker search TERME                # Rechercher sur Docker Hub

# Export/Import
docker save -o file.tar IMAGE      # Sauvegarder
docker load -i file.tar            # Charger
```

---

## Prochaines étapes

Maintenant que vous maîtrisez les images, passez à:

- [**Conteneurs Docker**](./infos-docker-03-conteneurs.md) - Créer et gérer des conteneurs
- [**Dockerfile**](./infos-docker-07-dockerfile.md) - Créer vos propres images

---

[← Introduction](./infos-docker-01-introduction-installation.md) | [Index](./infos-docker-00-index.md) | [Conteneurs →](./infos-docker-03-conteneurs.md)
