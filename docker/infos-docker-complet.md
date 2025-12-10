# Guide Complet Docker - Linux & Windows

## Table des Matières
1. [Introduction et Installation](#introduction)
2. [Images Docker](#images)
3. [Conteneurs Docker](#conteneurs)
4. [Volumes et Persistance](#volumes)
5. [Réseaux Docker](#reseaux)
6. [Docker Compose](#docker-compose)
7. [Dockerfile](#dockerfile)
8. [Registres et CI/CD](#registres)
9. [Maintenance et Nettoyage](#maintenance)
10. [Debug et Monitoring](#debug)
11. [Backup et Restauration](#backup)
12. [Différences Linux vs Windows](#differences)
13. [Cas Pratiques (Odoo, Next.js, FastAPI, PostgreSQL, MinIO)](#cas-pratiques)

---

## 1. Introduction et Installation {#introduction}

### Qu'est-ce que Docker ?
Docker est une plateforme de containerisation qui permet d'empaqueter des applications et leurs dépendances dans des conteneurs légers et portables. Contrairement aux machines virtuelles, Docker utilise le noyau de l'OS hôte, ce qui le rend beaucoup plus rapide et léger.

### Installation sur Linux

#### Ubuntu/Debian
```bash
# Mise à jour des paquets
sudo apt update

# Installation des dépendances
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Ajout de la clé GPG officielle de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Ajout du repository Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installation de Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Ajouter votre utilisateur au groupe docker (pour ne pas avoir à utiliser sudo)
sudo usermod -aG docker $USER

# Redémarrer la session pour appliquer les changements
# Ou exécuter : newgrp docker
```

#### CentOS/RHEL/Fedora
```bash
# Installation du repository Docker
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Installation de Docker
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
```

### Installation sur Windows

#### Windows avec WSL2 (Recommandé)
1. **Installer WSL2**
```powershell
# Exécuter dans PowerShell en tant qu'administrateur
wsl --install
# Redémarrer votre ordinateur
```

2. **Télécharger et installer Docker Desktop**
   - Télécharger depuis: https://www.docker.com/products/docker-desktop/
   - Installer en suivant l'assistant
   - Docker Desktop utilise WSL2 comme backend par défaut

3. **Configuration WSL2**
```bash
# Dans WSL2, vérifier que Docker fonctionne
docker --version
docker compose version
```

#### Différences importantes Windows vs Linux
- **Chemins de fichiers**: Windows utilise `\` (ex: `C:\Users\...`), Linux utilise `/` (ex: `/home/user/...`)
- **Montage de volumes**: Sur Windows avec WSL2, préférer les chemins WSL: `/mnt/c/Users/...` ou directement les volumes Docker
- **Performance**: Les volumes Docker natifs sont plus rapides que les bind mounts Windows dans WSL2
- **Line endings**: Attention aux CRLF (Windows) vs LF (Linux) dans les scripts

### Vérification de l'installation
```bash
# Vérifier la version de Docker
docker --version
# Résultat attendu: Docker version 24.x.x, build ...

# Vérifier Docker Compose
docker compose version
# Résultat attendu: Docker Compose version v2.x.x

# Tester Docker avec un conteneur Hello World
docker run hello-world
# Si tout fonctionne, vous verrez un message de confirmation

# Vérifier les informations système Docker
docker info
# Affiche: version, nombre de conteneurs, images, configuration réseau, etc.
```

---

## 2. Images Docker {#images}

### Qu'est-ce qu'une image Docker ?
Une image Docker est un template immuable qui contient tout ce dont une application a besoin pour s'exécuter : code, runtime, librairies, variables d'environnement et fichiers de configuration. Les images sont construites en couches (layers), ce qui permet de réutiliser les couches communes et d'économiser de l'espace disque.

### Gestion des Images

#### Lister les images
```bash
# Lister toutes les images locales
docker images
# ou
docker image ls

# Afficher avec plus de détails (taille, ID complet, etc.)
docker image ls --all --no-trunc

# Filtrer les images
docker images --filter "dangling=true"  # Images sans tag (orphelines)
docker images --filter "reference=postgres:*"  # Toutes les versions de postgres
```

#### Télécharger une image (Pull)
```bash
# Télécharger une image depuis Docker Hub
docker pull nginx
# Par défaut, télécharge la version "latest"

# Télécharger une version spécifique
docker pull nginx:1.25.3
# Toujours spécifier la version en production pour éviter les surprises !

# Télécharger depuis un registre privé
docker pull registry.gitlab.com/mon-projet/mon-app:latest

# Télécharger toutes les versions d'une image
docker pull --all-tags ubuntu
# Attention: peut télécharger plusieurs Go de données !
```

#### Construire une image (Build)
```bash
# Construire depuis un Dockerfile dans le répertoire courant
docker build -t mon-app:1.0 .
# -t : tag (nom) de l'image
# . : contexte de build (répertoire contenant le Dockerfile)

# Construire avec un Dockerfile différent
docker build -f Dockerfile.dev -t mon-app:dev .

# Construire sans utiliser le cache
docker build --no-cache -t mon-app:1.0 .
# Utile quand on veut forcer le téléchargement de nouvelles dépendances

# Construire avec des arguments
docker build --build-arg NODE_VERSION=18 -t mon-app:1.0 .
# Les ARG définis dans le Dockerfile peuvent être passés ainsi

# Construire pour une architecture différente (multi-platform)
docker buildx build --platform linux/amd64,linux/arm64 -t mon-app:1.0 .
# Utile pour les M1/M2 Mac ou les serveurs ARM
```

#### Tagger une image
```bash
# Créer un nouveau tag pour une image existante
docker tag mon-app:1.0 mon-app:latest
# Cela ne duplique pas l'image, juste crée un nouveau pointeur

# Tagger pour un registre privé
docker tag mon-app:1.0 registry.gitlab.com/mon-user/mon-app:1.0

# Convention de nommage recommandée
# registry.example.com/project/app:version
# Exemple: registry.gitlab.com/mycompany/backend:v2.3.1
```

#### Pousser une image vers un registre (Push)
```bash
# Se connecter à un registre
docker login registry.gitlab.com
# Entrer username et password/token

# Pousser l'image
docker push registry.gitlab.com/mon-user/mon-app:1.0

# Pousser toutes les versions d'une image
docker push --all-tags registry.gitlab.com/mon-user/mon-app
```

#### Inspecter une image
```bash
# Voir les détails d'une image
docker image inspect nginx:latest
# Affiche: layers, taille, date de création, commandes, etc.

# Voir l'historique des layers
docker history nginx:latest
# Utile pour comprendre comment l'image a été construite

# Voir uniquement la taille
docker image inspect nginx:latest --format='{{.Size}}'
```

#### Sauvegarder et charger des images
```bash
# Sauvegarder une image dans un fichier tar
docker save -o mon-app.tar mon-app:1.0
# Utile pour transférer des images sans registre

# Sauvegarder plusieurs images
docker save -o mes-images.tar mon-app:1.0 postgres:15 nginx:latest

# Charger une image depuis un fichier tar
docker load -i mon-app.tar
# Restaure l'image avec son tag d'origine

# Export vs Save
# save: garde l'historique et les layers (recommandé)
# export: créé un snapshot d'un conteneur (perte de l'historique)
```

#### Supprimer des images
```bash
# Supprimer une image spécifique
docker rmi mon-app:1.0
# ou
docker image rm mon-app:1.0

# Supprimer plusieurs images
docker rmi mon-app:1.0 mon-app:2.0

# Supprimer toutes les images non utilisées
docker image prune
# Supprime les images sans tag et non utilisées par des conteneurs

# Supprimer TOUTES les images non utilisées (même avec tag)
docker image prune -a
# ATTENTION: Supprime toutes les images non liées à un conteneur existant

# Forcer la suppression (même si l'image est utilisée)
docker rmi -f mon-app:1.0
# À éviter, préférer arrêter/supprimer le conteneur d'abord
```

### Optimisation des Images

#### Bonnes pratiques
```dockerfile
# ❌ MAUVAIS: Image lourde avec beaucoup de layers
FROM ubuntu:latest
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install flask
COPY . /app

# ✅ BON: Image optimisée
FROM python:3.11-slim  # Image de base plus légère
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*  # Nettoyer le cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt  # Pas de cache pip
COPY . /app
WORKDIR /app
```

#### Multi-stage builds
```dockerfile
# Stage 1: Build
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci  # Installion reproductible
COPY . .
RUN npm run build

# Stage 2: Production (image finale légère)
FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .
CMD ["node", "dist/index.js"]

# L'image finale ne contient que le nécessaire, pas les outils de build !
```

---

## 3. Conteneurs Docker {#conteneurs}

### Qu'est-ce qu'un conteneur ?
Un conteneur est une instance d'exécution d'une image Docker. C'est un processus isolé qui tourne sur votre machine avec son propre système de fichiers, réseau et espace de processus. Contrairement aux images (immuables), les conteneurs sont éphémères et modifiables.

### Création et Gestion des Conteneurs

#### Créer et lancer un conteneur (run)
```bash
# Lancer un conteneur basique
docker run nginx
# Lance nginx en avant-plan (bloque le terminal)

# Lancer en arrière-plan (mode détaché)
docker run -d nginx
# Retourne l'ID du conteneur

# Lancer avec un nom personnalisé
docker run -d --name mon-nginx nginx
# Beaucoup plus pratique que d'utiliser l'ID !

# Lancer avec mapping de ports
docker run -d -p 8080:80 nginx
# Format: -p PORT_HÔTE:PORT_CONTENEUR
# Accès: http://localhost:8080

# Lancer avec plusieurs ports
docker run -d -p 8080:80 -p 8443:443 nginx

# Publier tous les ports exposés aléatoirement
docker run -d -P nginx
# Docker choisit automatiquement des ports disponibles

# Lancer avec des variables d'environnement
docker run -d -e POSTGRES_PASSWORD=monmdp postgres:15
# -e : définir une variable d'environnement

# Charger les variables depuis un fichier
docker run -d --env-file .env postgres:15

# Lancer avec un volume
docker run -d -v /mon/chemin/local:/chemin/conteneur nginx
# Bind mount: lie un répertoire de l'hôte au conteneur

# Lancer avec un volume Docker nommé
docker run -d -v mes-donnees:/var/lib/postgresql/data postgres:15
# Volume nommé: géré par Docker (recommandé)

# Lancer avec un réseau personnalisé
docker run -d --network mon-reseau --name db postgres:15

# Lancer en mode interactif
docker run -it ubuntu bash
# -i: interactif (garde stdin ouvert)
# -t: alloue un pseudo-terminal
# Lance bash dans le conteneur

# Lancer et supprimer automatiquement à l'arrêt
docker run --rm -it ubuntu bash
# --rm: supprime le conteneur quand il s'arrête
# Utile pour les tests

# Lancer avec des limites de ressources
docker run -d --memory="512m" --cpus="1.5" nginx
# Limite la RAM à 512 Mo et 1.5 CPU cores

# Lancer avec une politique de redémarrage
docker run -d --restart=always nginx
# always: redémarre toujours le conteneur
# unless-stopped: redémarre sauf si arrêté manuellement
# on-failure: redémarre uniquement en cas d'erreur

# Lancer en lecture seule
docker run -d --read-only nginx
# Le système de fichiers du conteneur est en lecture seule
# Utile pour la sécurité

# Exemple complet pour PostgreSQL
docker run -d \
  --name postgres-dev \
  --restart=unless-stopped \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret123 \
  -e POSTGRES_DB=mabase \
  -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:15
```

#### Lister les conteneurs
```bash
# Lister les conteneurs en cours d'exécution
docker ps

# Lister TOUS les conteneurs (même arrêtés)
docker ps -a

# Afficher uniquement les IDs
docker ps -q

# Afficher avec un format personnalisé
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

# Filtrer les conteneurs
docker ps -a --filter "status=exited"  # Conteneurs arrêtés
docker ps --filter "name=postgres"     # Conteneurs avec "postgres" dans le nom
docker ps --filter "ancestor=nginx"    # Conteneurs créés depuis l'image nginx

# Voir la taille des conteneurs
docker ps -s
# Affiche la taille du layer en écriture
```

#### Arrêter et démarrer des conteneurs
```bash
# Arrêter un conteneur (graceful shutdown)
docker stop mon-conteneur
# Envoie SIGTERM, puis SIGKILL après 10 secondes

# Arrêter avec un timeout personnalisé
docker stop -t 30 mon-conteneur
# Attend 30 secondes avant le SIGKILL

# Arrêter immédiatement (force)
docker kill mon-conteneur
# Envoie directement SIGKILL (brutal)

# Démarrer un conteneur arrêté
docker start mon-conteneur

# Redémarrer un conteneur
docker restart mon-conteneur

# Arrêter tous les conteneurs
docker stop $(docker ps -q)

# Démarrer tous les conteneurs arrêtés
docker start $(docker ps -aq)
```

#### Supprimer des conteneurs
```bash
# Supprimer un conteneur arrêté
docker rm mon-conteneur

# Forcer la suppression (même en cours d'exécution)
docker rm -f mon-conteneur

# Supprimer plusieurs conteneurs
docker rm conteneur1 conteneur2 conteneur3

# Supprimer tous les conteneurs arrêtés
docker container prune
# Demande confirmation avant suppression

# Supprimer sans confirmation
docker container prune -f

# Supprimer tous les conteneurs (même en cours d'exécution)
docker rm -f $(docker ps -aq)
# ATTENTION: très destructif !
```

#### Logs et monitoring
```bash
# Voir les logs d'un conteneur
docker logs mon-conteneur

# Suivre les logs en temps réel (comme tail -f)
docker logs -f mon-conteneur

# Afficher les 100 dernières lignes
docker logs --tail 100 mon-conteneur

# Afficher les logs depuis une date
docker logs --since 2024-01-01 mon-conteneur

# Afficher avec les timestamps
docker logs -t mon-conteneur

# Logs des 5 dernières minutes
docker logs --since 5m mon-conteneur

# Statistiques en temps réel
docker stats
# Affiche CPU, RAM, I/O réseau pour tous les conteneurs

# Stats d'un conteneur spécifique
docker stats mon-conteneur

# Stats sans streaming (une seule fois)
docker stats --no-stream
```

#### Exécuter des commandes dans un conteneur
```bash
# Exécuter une commande dans un conteneur en cours
docker exec mon-conteneur ls -la /app

# Ouvrir un shell interactif
docker exec -it mon-conteneur bash
# Si bash n'est pas disponible, essayer sh
docker exec -it mon-conteneur sh

# Exécuter en tant qu'un autre utilisateur
docker exec -u root -it mon-conteneur bash

# Exécuter avec des variables d'environnement
docker exec -e VAR=value mon-conteneur env

# Exemple: se connecter à PostgreSQL dans le conteneur
docker exec -it postgres-dev psql -U admin -d mabase

# Exemple: voir les processus dans le conteneur
docker exec mon-conteneur ps aux

# Exemple: lire un fichier de log
docker exec mon-conteneur cat /var/log/app.log
```

#### Copier des fichiers
```bash
# Copier un fichier depuis l'hôte vers le conteneur
docker cp ./mon-fichier.txt mon-conteneur:/app/

# Copier un répertoire
docker cp ./mon-dossier mon-conteneur:/app/

# Copier depuis le conteneur vers l'hôte
docker cp mon-conteneur:/app/logs ./logs-backup

# Copier avec conservation des permissions
docker cp -a ./data mon-conteneur:/app/

# Exemple: backup d'une base de données
docker exec postgres-dev pg_dump -U admin mabase > backup.sql
# Ou en utilisant docker cp
docker cp postgres-dev:/tmp/backup.sql ./backup.sql
```

#### Inspecter un conteneur
```bash
# Voir toutes les informations d'un conteneur
docker inspect mon-conteneur
# Retourne un JSON avec configuration, réseau, volumes, etc.

# Extraire une information spécifique
docker inspect mon-conteneur --format='{{.State.Status}}'
docker inspect mon-conteneur --format='{{.NetworkSettings.IPAddress}}'
docker inspect mon-conteneur --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'

# Voir les variables d'environnement
docker inspect mon-conteneur --format='{{.Config.Env}}'

# Voir les volumes montés
docker inspect mon-conteneur --format='{{.Mounts}}'

# Voir les ports mappés
docker inspect mon-conteneur --format='{{.NetworkSettings.Ports}}'

# Voir la commande de démarrage
docker inspect mon-conteneur --format='{{.Config.Cmd}}'
```

#### Pause et unpause
```bash
# Mettre en pause un conteneur (freeze les processus)
docker pause mon-conteneur
# Le conteneur reste en mémoire mais ne consomme plus de CPU

# Reprendre un conteneur en pause
docker unpause mon-conteneur

# Utile pour prendre un snapshot ou sauvegarder l'état
```

#### Voir les processus d'un conteneur
```bash
# Lister les processus dans un conteneur
docker top mon-conteneur

# Avec format personnalisé
docker top mon-conteneur aux
```

#### Voir les changements dans le système de fichiers
```bash
# Voir les fichiers modifiés/ajoutés/supprimés dans le conteneur
docker diff mon-conteneur
# A: ajouté, C: modifié, D: supprimé
# Utile pour debug
```

---

## 4. Volumes et Persistance {#volumes}

### Pourquoi les volumes ?
Les conteneurs sont éphémères: quand ils sont supprimés, toutes leurs données disparaissent. Les volumes permettent de persister les données en dehors du cycle de vie du conteneur. Il existe 3 types de montage:
- **Volumes**: gérés par Docker (recommandé)
- **Bind mounts**: lie un répertoire de l'hôte
- **tmpfs**: stockage temporaire en RAM (Linux uniquement)

### Volumes Docker

#### Créer et gérer des volumes
```bash
# Créer un volume
docker volume create mon-volume
# Docker créé le volume dans /var/lib/docker/volumes/ (Linux)

# Lister les volumes
docker volume ls

# Inspecter un volume
docker volume inspect mon-volume
# Affiche: chemin, driver, date de création, etc.

# Exemple de résultat
# "Mountpoint": "/var/lib/docker/volumes/mon-volume/_data"
# C'est là que Docker stocke les données

# Créer un volume avec des options
docker volume create --driver local \
  --opt type=nfs \
  --opt o=addr=192.168.1.100,rw \
  --opt device=:/path/to/dir \
  mon-volume-nfs
# Permet d'utiliser NFS, CIFS, etc.
```

#### Utiliser des volumes
```bash
# Monter un volume dans un conteneur
docker run -d -v mon-volume:/app/data nginx
# Format: VOLUME_NAME:PATH_IN_CONTAINER

# Monter en lecture seule
docker run -d -v mon-volume:/app/data:ro nginx
# :ro = read-only

# Exemple avec PostgreSQL
docker run -d \
  --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:15
# Les données de la base survivront à la suppression du conteneur

# Monter plusieurs volumes
docker run -d \
  -v app-data:/app/data \
  -v app-logs:/app/logs \
  -v app-config:/app/config \
  mon-app:latest
```

#### Partager des volumes entre conteneurs
```bash
# Conteneur 1 créé le volume
docker run -d --name app1 -v shared-data:/data alpine sleep 3600

# Conteneur 2 utilise le même volume
docker run -d --name app2 -v shared-data:/data alpine sleep 3600

# Les deux conteneurs voient les mêmes données dans /data

# Utiliser les volumes d'un autre conteneur
docker run -d --name app3 --volumes-from app1 alpine sleep 3600
# app3 monte tous les volumes de app1
```

#### Sauvegarder et restaurer des volumes
```bash
# Sauvegarder un volume dans un tar
docker run --rm \
  -v mon-volume:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/backup.tar.gz /data
# Créé un conteneur temporaire qui archive le volume

# Version Windows (PowerShell)
docker run --rm `
  -v mon-volume:/data `
  -v ${PWD}:/backup `
  ubuntu tar czf /backup/backup.tar.gz /data

# Restaurer un volume depuis un tar
docker run --rm \
  -v mon-volume:/data \
  -v $(pwd):/backup \
  ubuntu tar xzf /backup/backup.tar.gz -C /
# Extrait l'archive dans le volume

# Backup PostgreSQL (méthode recommandée)
docker exec postgres-dev pg_dump -U admin mabase > backup.sql

# Restore PostgreSQL
docker exec -i postgres-dev psql -U admin mabase < backup.sql
```

#### Copier des données entre volumes
```bash
# Copier d'un volume à un autre
docker run --rm \
  -v volume-source:/source \
  -v volume-destination:/destination \
  ubuntu cp -r /source/. /destination/
```

#### Supprimer des volumes
```bash
# Supprimer un volume
docker volume rm mon-volume
# Ne fonctionne que si le volume n'est pas utilisé

# Supprimer tous les volumes non utilisés
docker volume prune
# Demande confirmation

# Supprimer sans confirmation
docker volume prune -f

# ATTENTION: vérifier d'abord les volumes avant de les supprimer !
docker volume ls
```

### Bind Mounts (montage direct)

```bash
# Monter un répertoire de l'hôte dans le conteneur
docker run -d -v /chemin/absolu/local:/chemin/conteneur nginx
# IMPORTANT: Le chemin doit être absolu !

# Exemple Linux
docker run -d -v /home/user/mon-site:/usr/share/nginx/html nginx

# Exemple Windows (CMD)
docker run -d -v C:\Users\Maste\mon-site:/usr/share/nginx/html nginx

# Exemple Windows (PowerShell)
docker run -d -v ${PWD}/mon-site:/usr/share/nginx/html nginx

# Exemple WSL2 (accès aux fichiers Windows depuis Linux)
docker run -d -v /mnt/c/Users/Maste/mon-site:/usr/share/nginx/html nginx

# Monter en lecture seule
docker run -d -v /chemin/local:/chemin/conteneur:ro nginx

# Monter le répertoire courant
docker run -d -v $(pwd):/app mon-app
# Très utile pour le développement

# Windows PowerShell
docker run -d -v ${PWD}:/app mon-app
```

#### Quand utiliser bind mounts vs volumes ?
- **Volumes**: Production, données importantes, portabilité, performance
- **Bind mounts**: Développement, configuration, fichiers sources
```bash
# Développement: bind mount pour hot-reload
docker run -v $(pwd)/src:/app/src mon-app

# Production: volume pour les données
docker run -v app-data:/app/data mon-app
```

### tmpfs (stockage temporaire en RAM)

```bash
# Monter un tmpfs (Linux uniquement)
docker run -d --tmpfs /app/cache:rw,size=100m nginx
# Les données sont en RAM et disparaissent à l'arrêt du conteneur

# Exemple avec plusieurs tmpfs
docker run -d \
  --tmpfs /tmp:rw,size=100m,mode=1777 \
  --tmpfs /app/cache:rw,size=50m \
  mon-app

# Utile pour:
# - Fichiers temporaires
# - Cache éphémère
# - Performance maximale
# - Données sensibles qui ne doivent pas être écrites sur disque
```

### Bonnes Pratiques

```yaml
# Dans docker-compose.yml

services:
  # ✅ BON: Volume nommé pour les données de production
  postgres:
    image: postgres:15
    volumes:
      - postgres-data:/var/lib/postgresql/data

  # ✅ BON: Bind mount pour le développement
  app:
    image: mon-app
    volumes:
      - ./src:/app/src  # Hot-reload
      - app-data:/app/data  # Données persistantes
      - /app/node_modules  # Volume anonyme pour exclure node_modules

  # ✅ BON: Read-only pour les configurations
  nginx:
    image: nginx
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro

volumes:
  postgres-data:  # Volume géré par Docker
    driver: local
  app-data:
    driver: local
```

#### Permissions et ownership
```bash
# Problème courant: permissions refusées dans le conteneur

# Solution 1: Créer un utilisateur avec le même UID dans le conteneur
# Dans le Dockerfile
RUN useradd -u 1000 appuser
USER appuser

# Solution 2: Changer les permissions sur l'hôte
sudo chown -R 1000:1000 ./data

# Solution 3: Utiliser un volume Docker (recommandé)
# Docker gère les permissions automatiquement

# Vérifier les permissions dans un volume
docker run --rm -v mon-volume:/data ubuntu ls -la /data
```

---

## 5. Réseaux Docker {#reseaux}

### Concepts des réseaux Docker
Docker crée un réseau virtuel isolé pour les conteneurs. Par défaut, les conteneurs peuvent communiquer entre eux via leurs noms de conteneurs comme noms d'hôtes (DNS automatique). Docker supporte plusieurs drivers réseau.

### Types de réseaux (Drivers)

1. **bridge** (par défaut): Réseau privé sur l'hôte
2. **host**: Le conteneur utilise directement le réseau de l'hôte
3. **none**: Pas de réseau
4. **overlay**: Réseau multi-hôtes (Docker Swarm)
5. **macvlan**: Attribue une adresse MAC au conteneur

### Gestion des réseaux

#### Lister les réseaux
```bash
# Lister tous les réseaux
docker network ls

# Réseaux par défaut:
# - bridge: réseau par défaut
# - host: réseau de l'hôte
# - none: pas de réseau
```

#### Créer un réseau
```bash
# Créer un réseau bridge
docker network create mon-reseau

# Créer avec un subnet personnalisé
docker network create --subnet=172.20.0.0/16 mon-reseau

# Créer avec gateway
docker network create \
  --subnet=172.20.0.0/16 \
  --gateway=172.20.0.1 \
  mon-reseau

# Créer un réseau avec IPv6
docker network create --ipv6 mon-reseau-v6

# Créer un réseau overlay (pour Swarm)
docker network create --driver overlay mon-reseau-swarm
```

#### Inspecter un réseau
```bash
# Voir les détails d'un réseau
docker network inspect mon-reseau
# Affiche: conteneurs connectés, subnet, gateway, etc.

# Voir les conteneurs sur un réseau
docker network inspect mon-reseau --format='{{range .Containers}}{{.Name}} {{end}}'
```

#### Connecter des conteneurs à un réseau
```bash
# Lancer un conteneur sur un réseau spécifique
docker run -d --name web --network mon-reseau nginx

# Connecter un conteneur existant à un réseau
docker network connect mon-reseau mon-conteneur

# Déconnecter un conteneur d'un réseau
docker network disconnect mon-reseau mon-conteneur

# Connecter avec un alias
docker network connect --alias web-alias mon-reseau mon-conteneur
# Le conteneur sera accessible via "web-alias" sur ce réseau
```

#### Communication entre conteneurs
```bash
# Créer un réseau
docker network create app-network

# Lancer une base de données
docker run -d \
  --name postgres \
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# Lancer une application qui se connecte à la DB
docker run -d \
  --name app \
  --network app-network \
  -e DB_HOST=postgres \
  -e DB_PORT=5432 \
  mon-app:latest
# L'app peut se connecter à "postgres" comme hostname !

# Test de connectivité
docker run --rm --network app-network alpine ping postgres
# Doit répondre si le réseau fonctionne

# Test avec curl
docker run --rm --network app-network curlimages/curl curl http://web
```

#### Réseau host
```bash
# Utiliser le réseau de l'hôte directement
docker run -d --network host nginx
# nginx sera accessible sur http://localhost:80
# Pas besoin de mapping de ports (-p)
# Moins d'isolation, à éviter en général

# Utile pour:
# - Performance maximale (pas de NAT)
# - Accès aux services locaux de l'hôte
# - Debugging réseau
```

#### Réseau none
```bash
# Aucun réseau (conteneur isolé)
docker run -d --network none alpine sleep 3600
# Aucune connectivité réseau
# Utile pour tests ou sécurité maximale
```

#### Supprimer des réseaux
```bash
# Supprimer un réseau
docker network rm mon-reseau
# Ne fonctionne que si aucun conteneur n'est connecté

# Supprimer tous les réseaux non utilisés
docker network prune

# Supprimer sans confirmation
docker network prune -f
```

### Exposition de ports

```bash
# Mapper un port de l'hôte vers le conteneur
docker run -d -p 8080:80 nginx
# Format: -p HOST_PORT:CONTAINER_PORT
# Accès: http://localhost:8080

# Mapper sur une interface spécifique
docker run -d -p 127.0.0.1:8080:80 nginx
# Accessible uniquement depuis localhost

# Mapper sur une interface et IPv6
docker run -d -p [::1]:8080:80 nginx

# Mapper plusieurs ports
docker run -d -p 8080:80 -p 8443:443 nginx

# Mapper un port UDP
docker run -d -p 8080:80/udp mon-app

# Mapper un port TCP et UDP
docker run -d -p 8080:80/tcp -p 8080:80/udp mon-app

# Publier tous les ports exposés (EXPOSE dans Dockerfile)
docker run -d -P nginx
# Docker attribue automatiquement des ports aléatoires

# Voir les ports mappés
docker port mon-conteneur
```

### DNS et résolution de noms

```bash
# Docker fournit un DNS interne automatique
# Les conteneurs sur le même réseau peuvent se résoudre par leur nom

# Exemple
docker network create app-net
docker run -d --name db --network app-net postgres:15
docker run -d --name web --network app-net nginx

# Depuis "web", on peut ping "db"
docker exec web ping db

# Ajouter des entrées DNS personnalisées
docker run -d --add-host=api.local:192.168.1.100 nginx
# Ajoute "192.168.1.100 api.local" dans /etc/hosts

# Changer le DNS resolver
docker run -d --dns=8.8.8.8 --dns=8.8.4.4 nginx

# Définir le domaine de recherche
docker run -d --dns-search=example.com nginx
```

### Liens entre conteneurs (Legacy)

```bash
# Ancienne méthode (deprecated, utiliser les réseaux à la place)
docker run -d --name db postgres:15
docker run -d --name app --link db:database mon-app
# Créé une variable d'environnement DATABASE_HOST dans "app"

# Mais préférez les réseaux personnalisés !
```

### Isolation et sécurité réseau

```bash
# Par défaut, les conteneurs sur le même réseau peuvent communiquer

# Pour isoler complètement
docker network create --internal mon-reseau-isole
# Les conteneurs peuvent communiquer entre eux mais pas avec l'extérieur

# Exemple: base de données isolée
docker run -d --name db --network mon-reseau-isole postgres:15
# La DB ne peut pas accéder à Internet

# Pour donner accès à Internet, connecter à un autre réseau
docker network connect bridge db
```

### Cas pratique: Architecture multi-tiers

```bash
# Créer les réseaux
docker network create frontend-net
docker network create backend-net

# Base de données (uniquement sur backend)
docker run -d \
  --name postgres \
  --network backend-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# API (sur frontend ET backend)
docker run -d \
  --name api \
  --network backend-net \
  -e DB_HOST=postgres \
  mon-api:latest
docker network connect frontend-net api

# Frontend (uniquement sur frontend)
docker run -d \
  --name web \
  --network frontend-net \
  -p 80:80 \
  nginx

# Résultat:
# - web peut communiquer avec api
# - api peut communiquer avec postgres
# - web NE peut PAS communiquer avec postgres (isolation)
```

---

## 6. Docker Compose {#docker-compose}

### Qu'est-ce que Docker Compose ?
Docker Compose est un outil pour définir et gérer des applications multi-conteneurs. Au lieu de lancer chaque conteneur manuellement avec `docker run`, vous définissez toute votre stack dans un fichier YAML (`docker-compose.yml` ou `compose.yml`) et lancez tout avec une seule commande.

### Installation

```bash
# Sur Linux (si non inclus avec Docker)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Vérifier l'installation
docker compose version
# ou (ancienne syntaxe)
docker-compose --version

# Note: "docker compose" (sans tiret) est la nouvelle syntaxe recommandée
# "docker-compose" (avec tiret) est l'ancienne syntaxe (encore supportée)
```

### Structure de base d'un docker-compose.yml

```yaml
# Version du format Compose (optionnelle depuis Compose V2)
version: '3.8'

# Définition des services (conteneurs)
services:
  # Nom du service
  web:
    # Image à utiliser
    image: nginx:latest
    # Ou build depuis un Dockerfile
    # build: ./web

    # Ports à mapper
    ports:
      - "8080:80"

    # Variables d'environnement
    environment:
      - NODE_ENV=production

    # Volumes
    volumes:
      - ./html:/usr/share/nginx/html

    # Réseaux
    networks:
      - frontend

    # Dépendances (démarrage ordonné)
    depends_on:
      - api

    # Politique de redémarrage
    restart: unless-stopped

  api:
    image: mon-api:latest
    environment:
      - DB_HOST=postgres
    networks:
      - frontend
      - backend
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend

# Définition des volumes
volumes:
  postgres-data:
    driver: local

# Définition des réseaux
networks:
  frontend:
  backend:
```

### Commandes Docker Compose

#### Démarrer les services
```bash
# Démarrer tous les services (en arrière-plan)
docker compose up -d
# -d: mode détaché (background)

# Démarrer en avant-plan (voir les logs)
docker compose up

# Démarrer des services spécifiques
docker compose up -d web api
# Ne démarre que "web" et "api"

# Forcer la reconstruction des images
docker compose up -d --build
# Rebuild avant de démarrer

# Reconstruire sans cache
docker compose build --no-cache
docker compose up -d

# Reconstruire un service spécifique
docker compose up -d --build web
```

#### Arrêter et supprimer
```bash
# Arrêter les services (garde les conteneurs)
docker compose stop

# Démarrer les services arrêtés
docker compose start

# Redémarrer les services
docker compose restart

# Arrêter et supprimer les conteneurs
docker compose down
# Garde les volumes et images

# Supprimer avec les volumes
docker compose down --volumes
# ⚠️ ATTENTION: Supprime toutes les données !

# Supprimer avec les images
docker compose down --rmi all
# Supprime aussi les images

# Tout supprimer (conteneurs, volumes, images, réseaux)
docker compose down --volumes --rmi all
```

#### Gérer les services
```bash
# Lister les services en cours
docker compose ps

# Lister tous les conteneurs (même arrêtés)
docker compose ps -a

# Voir les logs
docker compose logs

# Suivre les logs en temps réel
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f web

# Logs de plusieurs services
docker compose logs -f web api

# Logs avec timestamps
docker compose logs -t

# Dernières 100 lignes
docker compose logs --tail=100

# Exécuter une commande dans un service
docker compose exec web bash
# Ouvre un shell dans le conteneur "web"

# Exécuter en une fois (sans -it)
docker compose exec web ls -la

# Exécuter un service one-off
docker compose run --rm web npm install
# Lance un nouveau conteneur, exécute la commande, puis supprime le conteneur
```

#### Scaling et réplication
```bash
# Lancer plusieurs instances d'un service
docker compose up -d --scale web=3
# Lance 3 instances du service "web"

# Note: les ports doivent être dynamiques
# Dans le docker-compose.yml:
# ports:
#   - "8080-8082:80"  # Plage de ports
```

#### Rebuild et mise à jour
```bash
# Reconstruire les images
docker compose build

# Rebuild un service spécifique
docker compose build web

# Rebuild sans cache
docker compose build --no-cache

# Pull les dernières images
docker compose pull

# Redémarrer avec les nouvelles images
docker compose up -d --force-recreate
# Force la recréation des conteneurs même si rien n'a changé
```

#### Configuration et validation
```bash
# Valider le fichier compose
docker compose config
# Affiche la configuration résolue et détecte les erreurs

# Valider sans résoudre les variables
docker compose config --quiet

# Voir les services définis
docker compose config --services

# Voir les volumes définis
docker compose config --volumes
```

### Fichier docker-compose.yml avancé

```yaml
version: '3.8'

services:
  # Frontend Next.js
  nextjs:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      # Arguments de build
      args:
        - NODE_VERSION=18
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://api:8000
      # Ou depuis un fichier .env
      - NEXT_PUBLIC_API_URL=${API_URL}
    volumes:
      # Bind mount pour hot-reload en développement
      - ./frontend/src:/app/src
      # Volume anonyme pour node_modules
      - /app/node_modules
    networks:
      - frontend
    depends_on:
      api:
        # Attendre que le service soit "healthy"
        condition: service_healthy
    restart: unless-stopped
    # Limites de ressources
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M

  # API FastAPI
  api:
    build:
      context: ./backend
      # Multi-stage build pour production
      target: production
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/dbname
      - REDIS_URL=redis://redis:6379
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ACCESS_KEY=${MINIO_ACCESS_KEY}
      - MINIO_SECRET_KEY=${MINIO_SECRET_KEY}
    env_file:
      # Charger depuis un fichier .env
      - .env
    volumes:
      - ./backend/app:/app
      - api-uploads:/app/uploads
    networks:
      - frontend
      - backend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    # Healthcheck
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=dbname
      # Optimisations PostgreSQL
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --locale=C
    volumes:
      # Données persistantes
      - postgres-data:/var/lib/postgresql/data
      # Scripts d'initialisation
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    # Commande personnalisée
    command: postgres -c max_connections=100 -c shared_buffers=256MB

  # Redis
  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - backend
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    restart: unless-stopped

  # MinIO (stockage S3)
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"  # API
      - "9001:9001"  # Console
    environment:
      - MINIO_ROOT_USER=${MINIO_ACCESS_KEY}
      - MINIO_ROOT_PASSWORD=${MINIO_SECRET_KEY}
    volumes:
      - minio-data:/data
    networks:
      - backend
    command: server /data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
    restart: unless-stopped

  # Odoo
  odoo:
    image: odoo:16
    ports:
      - "8069:8069"
    environment:
      - HOST=postgres
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
      - ./config:/etc/odoo
    networks:
      - frontend
      - backend
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  # Nginx (reverse proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - nginx-cache:/var/cache/nginx
    networks:
      - frontend
    depends_on:
      - nextjs
      - api
      - odoo
    restart: unless-stopped

# Volumes nommés
volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
  minio-data:
    driver: local
  odoo-web-data:
    driver: local
  api-uploads:
    driver: local
  nginx-cache:
    driver: local

# Réseaux personnalisés
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    # Isolation du réseau backend
    internal: true
```

### Variables d'environnement

#### Fichier .env
```bash
# .env à la racine du projet (à côté de docker-compose.yml)

# PostgreSQL
POSTGRES_USER=admin
POSTGRES_PASSWORD=super_secret_password
POSTGRES_DB=mydb

# Redis
REDIS_PASSWORD=redis_secret

# MinIO
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin_secret

# API
API_SECRET_KEY=my_api_secret_key
JWT_SECRET=jwt_secret_key

# URLs
API_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

#### Utilisation dans compose
```yaml
services:
  app:
    image: mon-app
    environment:
      # Utiliser une variable du .env
      - DB_PASSWORD=${POSTGRES_PASSWORD}
      # Avec valeur par défaut
      - DB_HOST=${DB_HOST:-postgres}
      # Variable obligatoire (erreur si non définie)
      - API_KEY=${API_KEY:?API_KEY must be set}
    # Ou charger tout le fichier
    env_file:
      - .env
      - .env.local  # Surcharge
```

### Profils (environments multiples)

```yaml
services:
  web:
    image: nginx
    # Ce service appartient au profil "frontend"
    profiles: ["frontend"]

  db:
    image: postgres
    # Ce service est toujours actif (pas de profil)

  debug:
    image: mon-app-debug
    profiles: ["debug"]

# Lancer uniquement le profil "frontend"
# docker compose --profile frontend up -d

# Lancer plusieurs profils
# docker compose --profile frontend --profile debug up -d
```

### Override files

```bash
# docker-compose.yml: configuration de base
# docker-compose.override.yml: surcharge automatiquement appliquée
# docker-compose.prod.yml: pour la production

# Utiliser un fichier de surcharge spécifique
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Exemple: docker-compose.override.yml (développement)
version: '3.8'
services:
  web:
    volumes:
      - ./src:/app/src  # Hot-reload
    environment:
      - DEBUG=true

# Exemple: docker-compose.prod.yml (production)
version: '3.8'
services:
  web:
    restart: always
    deploy:
      replicas: 3
```

### Extends (réutiliser des configurations)

```yaml
# common-services.yml
version: '3.8'
services:
  base-service:
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

# docker-compose.yml
version: '3.8'
services:
  web:
    extends:
      file: common-services.yml
      service: base-service
    image: nginx
```

---

## 7. Dockerfile {#dockerfile}

### Qu'est-ce qu'un Dockerfile ?
Un Dockerfile est un fichier texte contenant une série d'instructions pour construire une image Docker. Chaque instruction crée une nouvelle couche (layer) dans l'image.

### Instructions de base

#### FROM - Image de base
```dockerfile
# Image de base officielle
FROM ubuntu:22.04

# Image Alpine (très légère ~5MB)
FROM alpine:3.18

# Image Node.js officielle
FROM node:18

# Version spécifique avec digest (pour reproductibilité)
FROM node:18@sha256:abc123...

# Multi-stage: nommer un stage
FROM node:18 AS builder

# Image de base vide (pour les binaires statiques)
FROM scratch
```

#### WORKDIR - Répertoire de travail
```dockerfile
# Définir le répertoire de travail
WORKDIR /app
# Créé le répertoire s'il n'existe pas
# Tous les RUN, COPY, ADD suivants se feront dans /app

# Exemple complet
FROM node:18
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
```

#### COPY vs ADD
```dockerfile
# COPY: copier des fichiers/dossiers (recommandé)
COPY package.json /app/
COPY ./src /app/src/
COPY . /app/

# Copier avec changement d'owner
COPY --chown=appuser:appgroup file.txt /app/

# ADD: comme COPY mais avec fonctionnalités supplémentaires
ADD https://example.com/file.tar.gz /app/  # Télécharge depuis URL
ADD archive.tar.gz /app/  # Extrait automatiquement les archives

# ⚠️ Utiliser COPY sauf si vous avez besoin des features de ADD
```

#### RUN - Exécuter des commandes
```dockerfile
# Exécuter une commande shell
RUN apt-get update && apt-get install -y curl

# ❌ MAUVAIS: Plusieurs RUN créent plusieurs layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

# ✅ BON: Combiner en une seule commande
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*
# && rm -rf /var/lib/apt/lists/* : nettoyer le cache apt

# Forme exec (pas de shell)
RUN ["apt-get", "install", "-y", "curl"]
```

#### ENV - Variables d'environnement
```dockerfile
# Définir une variable d'environnement
ENV NODE_ENV=production
ENV PORT=3000
ENV PATH="/app/bin:${PATH}"

# Plusieurs variables
ENV NODE_ENV=production \
    PORT=3000 \
    DEBUG=false

# Les variables sont disponibles à la build ET au runtime
```

#### ARG - Arguments de build
```dockerfile
# Définir un argument (uniquement pour le build)
ARG NODE_VERSION=18

# Utiliser l'argument
FROM node:${NODE_VERSION}

# Avec valeur par défaut
ARG ENVIRONMENT=development

# Utiliser dans RUN
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y nginx

# Passer l'argument au build
# docker build --build-arg NODE_VERSION=20 .
```

#### EXPOSE - Documenter les ports
```dockerfile
# Indiquer quel port l'app écoute (documentation uniquement)
EXPOSE 8080

# Plusieurs ports
EXPOSE 8080 8443

# Port UDP
EXPOSE 8080/udp

# ⚠️ EXPOSE ne publie pas réellement le port !
# Il faut utiliser -p au runtime: docker run -p 8080:8080
```

#### CMD vs ENTRYPOINT

##### CMD - Commande par défaut
```dockerfile
# Forme shell
CMD npm start

# Forme exec (recommandée)
CMD ["npm", "start"]

# CMD peut être surchargée au runtime
# docker run mon-image echo "hello"  # Remplace CMD
```

##### ENTRYPOINT - Point d'entrée
```dockerfile
# Forme exec (recommandée)
ENTRYPOINT ["python", "app.py"]

# Forme shell
ENTRYPOINT python app.py

# ENTRYPOINT n'est pas surchargée, les arguments sont ajoutés
# docker run mon-image --debug  # Execute: python app.py --debug
```

##### Combiner ENTRYPOINT et CMD
```dockerfile
# ENTRYPOINT: commande fixe
ENTRYPOINT ["python", "app.py"]

# CMD: arguments par défaut
CMD ["--port", "8000"]

# Résultat: python app.py --port 8000

# Au runtime, on peut surcharger CMD
# docker run mon-image --port 9000
# Execute: python app.py --port 9000
```

#### USER - Changer d'utilisateur
```dockerfile
# Par défaut, les conteneurs s'exécutent en root (⚠️ risque de sécurité)

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser

# Changer d'utilisateur
USER appuser

# Tout ce qui suit s'exécutera en tant que "appuser"

# Exemple complet
FROM node:18
RUN useradd -m -u 1000 nodeuser
WORKDIR /app
COPY --chown=nodeuser:nodeuser . .
USER nodeuser
CMD ["node", "index.js"]
```

#### VOLUME - Points de montage
```dockerfile
# Déclarer un volume
VOLUME /app/data

# Plusieurs volumes
VOLUME ["/app/data", "/app/logs"]

# Au runtime, Docker créera un volume anonyme si non spécifié
# Mieux: spécifier le volume au runtime
# docker run -v my-data:/app/data mon-image
```

#### HEALTHCHECK - Vérification de santé
```dockerfile
# Définir un healthcheck
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Options:
# --interval: fréquence de vérification
# --timeout: timeout de la commande
# --retries: nombre d'échecs avant "unhealthy"
# --start-period: délai avant le premier check

# Désactiver le healthcheck
HEALTHCHECK NONE
```

#### LABEL - Métadonnées
```dockerfile
# Ajouter des métadonnées
LABEL maintainer="you@example.com"
LABEL version="1.0"
LABEL description="Mon application"

# Plusieurs labels
LABEL org.opencontainers.image.authors="you@example.com" \
      org.opencontainers.image.version="1.0" \
      org.opencontainers.image.description="Mon app"
```

### Exemples complets

#### Dockerfile Node.js (production)
```dockerfile
# Multi-stage build pour optimiser la taille

# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances (y compris dev)
RUN npm ci

# Copier le code source
COPY . .

# Build de l'application
RUN npm run build

# Stage 2: Production
FROM node:18-alpine
WORKDIR /app

# Créer un utilisateur non-root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copier uniquement les fichiers nécessaires depuis le stage builder
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

# Variables d'environnement
ENV NODE_ENV=production
ENV PORT=3000

# Exposer le port
EXPOSE 3000

# Changer d'utilisateur
USER nodejs

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Commande de démarrage
CMD ["node", "dist/index.js"]
```

#### Dockerfile Python FastAPI
```dockerfile
# Multi-stage build

# Stage 1: Builder
FROM python:3.11-slim AS builder
WORKDIR /app

# Installer les dépendances système pour la compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .

# Installer dans un virtualenv (pour copier facilement)
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app

# Copier le virtualenv depuis le builder
COPY --from=builder /opt/venv /opt/venv

# Créer utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Variables d'environnement
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copier le code
COPY --chown=appuser:appuser . .

# Changer d'utilisateur
USER appuser

# Exposer le port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Dockerfile Next.js
```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app

# Copier package files
COPY package.json package-lock.json ./

# Installer les dépendances
RUN npm ci

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app

# Copier les dépendances depuis deps
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build Next.js
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Stage 3: Runner (production)
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Créer utilisateur
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copier les fichiers nécessaires
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json

# Copier le build avec les permissions
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
```

### .dockerignore

```bash
# Fichier .dockerignore (comme .gitignore)
# Exclut des fichiers du contexte de build

# Node
node_modules
npm-debug.log

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.egg-info
venv/
.venv/

# Git
.git
.gitignore
.gitattributes

# IDE
.vscode
.idea
*.swp
*.swo

# Tests
tests/
*.test.js
*.spec.js
coverage/

# Documentation
README.md
docs/
*.md

# CI/CD
.github/
.gitlab-ci.yml
Jenkinsfile

# Docker
Dockerfile*
docker-compose*.yml
.dockerignore

# Environnement
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Builds locaux
dist/
build/
```

### Optimisations avancées

#### Layer caching
```dockerfile
# ❌ MAUVAIS: Invalide le cache à chaque modification de code
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# ✅ BON: Séparer les layers pour optimiser le cache
FROM node:18
WORKDIR /app

# Layer 1: Copier uniquement package.json (cache si pas de changement)
COPY package*.json ./

# Layer 2: Installer les dépendances (cache si package.json n'a pas changé)
RUN npm ci

# Layer 3: Copier le code (invalidé à chaque changement, mais layers 1-2 en cache)
COPY . .

# Layer 4: Build
RUN npm run build
```

#### Multi-platform builds
```dockerfile
# Build pour plusieurs architectures (AMD64, ARM64)

# Utiliser buildx
# docker buildx build --platform linux/amd64,linux/arm64 -t mon-app:latest .

# Dans le Dockerfile, détecter l'architecture
ARG TARGETPLATFORM
ARG BUILDPLATFORM

RUN echo "Building on $BUILDPLATFORM for $TARGETPLATFORM"

# Installer des dépendances spécifiques à l'architecture
RUN if [ "$TARGETPLATFORM" = "linux/arm64" ]; then \
      apt-get install -y arm-specific-package; \
    fi
```

---

## 8. Registres et CI/CD {#registres}

### Registres Docker

#### Docker Hub (registre public)
```bash
# Login
docker login
# Entrer username et password

# Tagger pour Docker Hub
docker tag mon-app:latest username/mon-app:latest

# Push
docker push username/mon-app:latest

# Pull
docker pull username/mon-app:latest

# Logout
docker logout
```

#### GitLab Container Registry
```bash
# Login avec token personnel
docker login registry.gitlab.com -u username -p ACCESS_TOKEN

# Tagger
docker tag mon-app:latest registry.gitlab.com/username/project/mon-app:latest

# Push
docker push registry.gitlab.com/username/project/mon-app:latest
```

#### GitHub Container Registry (ghcr.io)
```bash
# Login avec token GitHub
echo $GITHUB_TOKEN | docker login ghcr.io -u username --password-stdin

# Tagger
docker tag mon-app:latest ghcr.io/username/mon-app:latest

# Push
docker push ghcr.io/username/mon-app:latest
```

#### Azure Container Registry
```bash
# Login
docker login myregistry.azurecr.io -u username -p password

# Tagger et push
docker tag mon-app:latest myregistry.azurecr.io/mon-app:latest
docker push myregistry.azurecr.io/mon-app:latest
```

#### Registre privé auto-hébergé
```bash
# Lancer un registre local
docker run -d -p 5000:5000 --name registry registry:2

# Tagger
docker tag mon-app:latest localhost:5000/mon-app:latest

# Push
docker push localhost:5000/mon-app:latest

# Avec authentification et volumes
docker run -d \
  -p 5000:5000 \
  --name registry \
  -v registry-data:/var/lib/registry \
  -v $(pwd)/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  registry:2
```

### CI/CD avec Docker

#### GitLab CI (.gitlab-ci.yml)
```yaml
# .gitlab-ci.yml

stages:
  - build
  - test
  - deploy

variables:
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  LATEST_TAG: $CI_REGISTRY_IMAGE:latest

# Build de l'image
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker tag $IMAGE_TAG $LATEST_TAG
    - docker push $IMAGE_TAG
    - docker push $LATEST_TAG
  only:
    - main

# Tests
test:
  stage: test
  image: $IMAGE_TAG
  script:
    - npm test
  only:
    - main

# Déploiement
deploy:
  stage: deploy
  image: docker:24
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    # SSH vers le serveur de prod et pull la nouvelle image
    - ssh user@prod-server "docker pull $IMAGE_TAG"
    - ssh user@prod-server "docker-compose up -d"
  only:
    - main
  when: manual  # Déploiement manuel
```

#### GitHub Actions
```yaml
# .github/workflows/docker.yml

name: Docker Build and Push

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Login to GitHub Container Registry
      uses: docker/login-action@v2
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ghcr.io/${{ github.repository }}:latest
          ghcr.io/${{ github.repository }}:${{ github.sha }}
        cache-from: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache
        cache-to: type=registry,ref=ghcr.io/${{ github.repository }}:buildcache,mode=max
```

---

## 9. Maintenance et Nettoyage {#maintenance}

### Voir l'utilisation disque

```bash
# Voir l'espace disque utilisé par Docker
docker system df

# Avec plus de détails
docker system df -v
# Affiche: images, conteneurs, volumes, build cache

# Exemple de sortie:
# TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
# Images          25        5         4.2GB     3.1GB (73%)
# Containers      10        2         100MB     50MB (50%)
# Local Volumes   8         3         2GB       1GB (50%)
# Build Cache     30        0         1GB       1GB (100%)
```

### Nettoyage

#### Nettoyer tout (⚠️ destructif)
```bash
# Nettoyer TOUT (images, conteneurs, volumes, réseaux, cache)
docker system prune -a --volumes
# ATTENTION: Supprime TOUT ce qui n'est pas en cours d'utilisation !

# Sans les volumes
docker system prune -a

# Avec confirmation automatique
docker system prune -a -f
```

#### Nettoyer les images
```bash
# Supprimer les images "dangling" (sans tag)
docker image prune

# Supprimer toutes les images non utilisées
docker image prune -a

# Supprimer sans confirmation
docker image prune -a -f

# Supprimer les images de plus de 7 jours
docker image prune -a --filter "until=168h"
```

#### Nettoyer les conteneurs
```bash
# Supprimer tous les conteneurs arrêtés
docker container prune

# Sans confirmation
docker container prune -f

# Supprimer tous les conteneurs (même en cours)
docker rm -f $(docker ps -aq)
```

#### Nettoyer les volumes
```bash
# Supprimer les volumes non utilisés
docker volume prune

# ⚠️ ATTENTION: Cela supprime les données !
# Toujours vérifier avant
docker volume ls

# Supprimer un volume spécifique
docker volume rm mon-volume

# Supprimer sans confirmation
docker volume prune -f
```

#### Nettoyer les réseaux
```bash
# Supprimer les réseaux non utilisés
docker network prune

# Sans confirmation
docker network prune -f
```

#### Nettoyer le build cache
```bash
# Voir le cache de build
docker buildx du

# Supprimer tout le cache
docker builder prune

# Supprimer le cache de plus de 7 jours
docker builder prune --filter until=168h

# Nettoyer le cache BuildKit
docker buildx prune
```

### Scripts de maintenance

#### Script de nettoyage automatique (Linux/Mac)
```bash
#!/bin/bash
# cleanup-docker.sh

echo "🧹 Nettoyage Docker..."

# Arrêter les conteneurs de plus de 24h
echo "Arrêt des conteneurs anciens..."
docker ps -a --filter "status=exited" --filter "status=created" --format "{{.ID}}" | xargs -r docker rm

# Supprimer les images non utilisées de plus de 7 jours
echo "Suppression des images anciennes..."
docker image prune -a --filter "until=168h" -f

# Supprimer les volumes orphelins
echo "Suppression des volumes non utilisés..."
docker volume prune -f

# Supprimer les réseaux non utilisés
echo "Suppression des réseaux non utilisés..."
docker network prune -f

# Supprimer le build cache de plus de 7 jours
echo "Nettoyage du cache de build..."
docker builder prune --filter until=168h -f

echo "✅ Nettoyage terminé !"
docker system df
```

#### Cron job pour nettoyage automatique
```bash
# Ajouter au crontab (crontab -e)
# Nettoyer tous les dimanches à 3h du matin
0 3 * * 0 /path/to/cleanup-docker.sh >> /var/log/docker-cleanup.log 2>&1
```

#### Windows PowerShell
```powershell
# cleanup-docker.ps1

Write-Host "Nettoyage Docker..." -ForegroundColor Green

# Conteneurs arrêtés
Write-Host "Suppression des conteneurs arrêtés..."
docker container prune -f

# Images non utilisées
Write-Host "Suppression des images non utilisées..."
docker image prune -a -f

# Volumes non utilisés
Write-Host "Suppression des volumes non utilisés..."
docker volume prune -f

# Réseaux
Write-Host "Suppression des réseaux non utilisés..."
docker network prune -f

Write-Host "Nettoyage terminé !" -ForegroundColor Green
docker system df
```

### Monitoring de l'espace disque

```bash
# Surveiller la taille des volumes
docker volume ls -q | xargs docker volume inspect --format '{{.Name}}: {{.Mountpoint}}' | while read line; do
  name=$(echo $line | cut -d: -f1)
  path=$(echo $line | cut -d: -f2)
  size=$(sudo du -sh $path 2>/dev/null | cut -f1)
  echo "$name: $size"
done | sort -k2 -hr

# Surveiller la taille des images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | sort -k3 -hr
```

---

## 10. Debug et Monitoring {#debug}

### Logs

```bash
# Voir les logs d'un conteneur
docker logs mon-conteneur

# Suivre les logs en temps réel
docker logs -f mon-conteneur

# Dernières 100 lignes
docker logs --tail 100 mon-conteneur

# Avec timestamps
docker logs -t mon-conteneur

# Depuis une date
docker logs --since "2024-01-01T00:00:00" mon-conteneur
docker logs --since 1h mon-conteneur
docker logs --since 30m mon-conteneur

# Entre deux dates
docker logs --since "2024-01-01" --until "2024-01-02" mon-conteneur

# Logs de tous les conteneurs
for container in $(docker ps -q); do
  echo "=== Logs de $(docker ps --filter id=$container --format '{{.Names}}') ==="
  docker logs --tail 50 $container
done
```

### Stats et monitoring

```bash
# Statistiques en temps réel
docker stats
# Affiche: CPU, RAM, I/O réseau, I/O disque

# Stats d'un conteneur spécifique
docker stats mon-conteneur

# Stats sans streaming (une seule fois)
docker stats --no-stream

# Format personnalisé
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Export des stats en JSON
docker stats --no-stream --format json

# Limiter les ressources au runtime
docker run -d \
  --memory="512m" \
  --memory-swap="1g" \
  --cpus="1.5" \
  --cpu-shares=1024 \
  nginx
```

### Inspection et debug

```bash
# Inspecter un conteneur
docker inspect mon-conteneur

# Extraire une info spécifique
docker inspect mon-conteneur --format='{{.State.Status}}'
docker inspect mon-conteneur --format='{{.NetworkSettings.IPAddress}}'
docker inspect mon-conteneur --format='{{range .Mounts}}{{.Source}}:{{.Destination}}{{"\n"}}{{end}}'

# Voir les processus dans un conteneur
docker top mon-conteneur

# Voir les ports
docker port mon-conteneur

# Voir les changements dans le filesystem
docker diff mon-conteneur

# Exporter le filesystem
docker export mon-conteneur > conteneur.tar

# Copier le filesystem modifié
docker cp mon-conteneur:/app/logs ./backup-logs
```

### Debug interactif

```bash
# Ouvrir un shell dans un conteneur en cours
docker exec -it mon-conteneur bash
# ou sh si bash n'est pas disponible
docker exec -it mon-conteneur sh

# Exécuter en tant que root
docker exec -u root -it mon-conteneur bash

# Débugger un conteneur qui crash au démarrage
# 1. Surcharger l'entrypoint
docker run -it --entrypoint /bin/sh mon-app

# 2. Ou avec bash
docker run -it --entrypoint /bin/bash mon-app

# 3. Inspecter sans démarrer
docker create --name debug mon-app
docker cp debug:/app/config ./config-backup
docker rm debug
```

### Healthchecks

```bash
# Voir le statut de santé
docker ps
# Colonne STATUS affiche "healthy" ou "unhealthy"

# Inspecter le healthcheck
docker inspect mon-conteneur --format='{{.State.Health.Status}}'

# Voir l'historique des healthchecks
docker inspect mon-conteneur --format='{{json .State.Health}}' | jq

# Définir un healthcheck dans Dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# Définir dans docker-compose.yml
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Troubleshooting commun

#### Conteneur qui crash immédiatement
```bash
# Voir les logs
docker logs mon-conteneur

# Voir l'exit code
docker inspect mon-conteneur --format='{{.State.ExitCode}}'

# Exit codes courants:
# 0: OK
# 1: Erreur application
# 137: Tué par OOM (Out of Memory)
# 139: Segmentation fault
# 143: SIGTERM (arrêt gracieux)

# Débugger en overridant l'entrypoint
docker run -it --entrypoint sh mon-app
```

#### Problèmes réseau
```bash
# Ping entre conteneurs
docker exec conteneur1 ping conteneur2

# Vérifier la résolution DNS
docker exec mon-conteneur nslookup autre-conteneur

# Voir les interfaces réseau
docker exec mon-conteneur ip addr

# Voir les routes
docker exec mon-conteneur ip route

# Test de connectivité HTTP
docker exec mon-conteneur curl -v http://autre-conteneur:8080
```

#### Problèmes de permissions
```bash
# Voir les permissions dans le conteneur
docker exec mon-conteneur ls -la /app

# Voir l'utilisateur du processus
docker exec mon-conteneur whoami
docker exec mon-conteneur id

# Changer le owner des fichiers
docker exec -u root mon-conteneur chown -R appuser:appuser /app
```

#### Performance lente
```bash
# Vérifier l'utilisation des ressources
docker stats mon-conteneur

# Voir les limites de ressources
docker inspect mon-conteneur --format='{{.HostConfig.Memory}}'
docker inspect mon-conteneur --format='{{.HostConfig.CpuShares}}'

# Augmenter les limites
docker update --memory=1g --cpus=2 mon-conteneur
```

### Outils de monitoring avancés

#### cAdvisor (Container Advisor)
```bash
# Lancer cAdvisor
docker run -d \
  --name=cadvisor \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:ro \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --publish=8080:8080 \
  --detach=true \
  google/cadvisor:latest

# Interface web: http://localhost:8080
```

#### Portainer (UI pour Docker)
```bash
# Lancer Portainer
docker run -d \
  -p 9000:9000 \
  --name=portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer-data:/data \
  portainer/portainer-ce

# Interface web: http://localhost:9000
```

---

## 11. Backup et Restauration {#backup}

### Sauvegarder des volumes

#### Méthode 1: Tar archive
```bash
# Sauvegarder un volume dans un tar
docker run --rm \
  -v mon-volume:/data \
  -v $(pwd):/backup \
  ubuntu tar czf /backup/volume-backup-$(date +%Y%m%d).tar.gz /data

# Windows PowerShell
docker run --rm `
  -v mon-volume:/data `
  -v ${PWD}:/backup `
  ubuntu tar czf /backup/volume-backup.tar.gz /data

# Restaurer depuis le tar
docker run --rm \
  -v mon-volume:/data \
  -v $(pwd):/backup \
  ubuntu bash -c "cd /data && tar xzf /backup/volume-backup.tar.gz --strip 1"
```

#### Méthode 2: Docker cp (pour conteneurs en cours)
```bash
# Backup
docker cp mon-conteneur:/app/data ./backup-data

# Restore
docker cp ./backup-data/. mon-conteneur:/app/data
```

### Sauvegarder des bases de données

#### PostgreSQL
```bash
# Dump de la base
docker exec postgres-container pg_dump -U username dbname > backup.sql

# Avec compression
docker exec postgres-container pg_dump -U username dbname | gzip > backup.sql.gz

# Dump de toutes les bases
docker exec postgres-container pg_dumpall -U postgres > backup-all.sql

# Restore
docker exec -i postgres-container psql -U username dbname < backup.sql

# Ou avec gunzip
gunzip < backup.sql.gz | docker exec -i postgres-container psql -U username dbname

# Backup automatique avec cron
#!/bin/bash
# backup-postgres.sh
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

docker exec postgres-container pg_dump -U username dbname | gzip > "$BACKUP_DIR/backup-$DATE.sql.gz"

# Garder seulement les 7 derniers backups
ls -t $BACKUP_DIR/backup-*.sql.gz | tail -n +8 | xargs rm -f
```

#### MySQL/MariaDB
```bash
# Dump
docker exec mysql-container mysqldump -u root -pPASSWORD dbname > backup.sql

# Avec compression
docker exec mysql-container mysqldump -u root -pPASSWORD dbname | gzip > backup.sql.gz

# Restore
docker exec -i mysql-container mysql -u root -pPASSWORD dbname < backup.sql

# Backup toutes les bases
docker exec mysql-container mysqldump -u root -pPASSWORD --all-databases > backup-all.sql
```

#### MongoDB
```bash
# Dump
docker exec mongo-container mongodump --out /backup
docker cp mongo-container:/backup ./mongo-backup

# Restore
docker cp ./mongo-backup mongo-container:/backup
docker exec mongo-container mongorestore /backup
```

### Sauvegarder des images

```bash
# Sauvegarder une image
docker save -o mon-app.tar mon-app:latest

# Sauvegarder plusieurs images
docker save -o mes-images.tar mon-app:latest postgres:15 redis:7

# Avec compression
docker save mon-app:latest | gzip > mon-app.tar.gz

# Charger une image
docker load -i mon-app.tar

# Ou avec gunzip
gunzip < mon-app.tar.gz | docker load
```

### Sauvegarder des conteneurs (snapshot)

```bash
# Créer une image depuis un conteneur en cours
docker commit mon-conteneur mon-image-snapshot:$(date +%Y%m%d)

# Avec un message
docker commit -m "Snapshot avant mise à jour" mon-conteneur mon-image-snapshot

# Sauvegarder le snapshot
docker save -o snapshot.tar mon-image-snapshot

# Restaurer
docker load -i snapshot.tar
docker run -d mon-image-snapshot
```

### Stratégie de backup complète

#### Script de backup complet
```bash
#!/bin/bash
# docker-full-backup.sh

BACKUP_DIR="/backups/docker"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_PATH="$BACKUP_DIR/$DATE"

mkdir -p "$BACKUP_PATH"

echo "🔄 Backup Docker complet - $DATE"

# 1. Sauvegarder les volumes
echo "📦 Backup des volumes..."
for volume in $(docker volume ls -q); do
  echo "  - $volume"
  docker run --rm \
    -v $volume:/data \
    -v $BACKUP_PATH:/backup \
    ubuntu tar czf /backup/volume-$volume.tar.gz /data
done

# 2. Sauvegarder PostgreSQL
echo "🗄️  Backup PostgreSQL..."
docker exec postgres pg_dumpall -U postgres | gzip > "$BACKUP_PATH/postgres-all.sql.gz"

# 3. Sauvegarder les images custom
echo "🖼️  Backup des images..."
for image in $(docker images --filter "reference=mon-projet/*" --format "{{.Repository}}:{{.Tag}}"); do
  image_name=$(echo $image | tr '/:' '-')
  echo "  - $image"
  docker save $image | gzip > "$BACKUP_PATH/image-$image_name.tar.gz"
done

# 4. Sauvegarder les configurations
echo "⚙️  Backup des configurations..."
cp docker-compose.yml "$BACKUP_PATH/"
cp .env "$BACKUP_PATH/" 2>/dev/null || true
cp -r ./config "$BACKUP_PATH/" 2>/dev/null || true

# 5. Créer un index
echo "📝 Création de l'index..."
cat > "$BACKUP_PATH/README.md" << EOF
# Backup Docker - $DATE

## Conteneurs actifs
$(docker ps --format "- {{.Names}} ({{.Image}})")

## Volumes sauvegardés
$(ls $BACKUP_PATH/volume-*.tar.gz | xargs -n1 basename)

## Images sauvegardées
$(ls $BACKUP_PATH/image-*.tar.gz | xargs -n1 basename)

## Commandes de restauration

### Volumes
\`\`\`bash
docker volume create mon-volume
docker run --rm -v mon-volume:/data -v \$(pwd):/backup ubuntu tar xzf /backup/volume-mon-volume.tar.gz -C /data --strip 1
\`\`\`

### PostgreSQL
\`\`\`bash
gunzip < postgres-all.sql.gz | docker exec -i postgres psql -U postgres
\`\`\`

### Images
\`\`\`bash
gunzip < image-XXX.tar.gz | docker load
\`\`\`
EOF

echo "✅ Backup terminé: $BACKUP_PATH"

# Nettoyer les vieux backups (garder 7 jours)
find $BACKUP_DIR -type d -mtime +7 -exec rm -rf {} +

echo "🧹 Anciens backups nettoyés"
```

#### Restauration complète
```bash
#!/bin/bash
# docker-restore.sh

BACKUP_PATH=$1

if [ -z "$BACKUP_PATH" ]; then
  echo "Usage: ./docker-restore.sh /path/to/backup"
  exit 1
fi

echo "🔄 Restauration Docker depuis $BACKUP_PATH"

# 1. Arrêter tous les conteneurs
echo "⏹️  Arrêt des conteneurs..."
docker-compose down

# 2. Restaurer les volumes
echo "📦 Restauration des volumes..."
for volume_backup in $BACKUP_PATH/volume-*.tar.gz; do
  volume_name=$(basename $volume_backup | sed 's/volume-\(.*\).tar.gz/\1/')
  echo "  - $volume_name"

  # Créer le volume s'il n'existe pas
  docker volume create $volume_name

  # Restaurer les données
  docker run --rm \
    -v $volume_name:/data \
    -v $BACKUP_PATH:/backup \
    ubuntu bash -c "cd /data && tar xzf /backup/$(basename $volume_backup) --strip 1"
done

# 3. Restaurer les images
echo "🖼️  Restauration des images..."
for image_backup in $BACKUP_PATH/image-*.tar.gz; do
  echo "  - $(basename $image_backup)"
  gunzip < $image_backup | docker load
done

# 4. Restaurer PostgreSQL
echo "🗄️  Restauration PostgreSQL..."
docker-compose up -d postgres
sleep 10  # Attendre que PostgreSQL soit prêt
gunzip < $BACKUP_PATH/postgres-all.sql.gz | docker exec -i postgres psql -U postgres

# 5. Redémarrer tous les services
echo "▶️  Redémarrage des services..."
docker-compose up -d

echo "✅ Restauration terminée !"
```

### Backup vers le cloud

#### AWS S3
```bash
# Installer AWS CLI
pip install awscli

# Configurer
aws configure

# Backup vers S3
docker run --rm \
  -v mon-volume:/data \
  -v ~/.aws:/root/.aws \
  amazon/aws-cli s3 sync /data s3://mon-bucket/backups/$(date +%Y%m%d)/

# Restore depuis S3
docker run --rm \
  -v mon-volume:/data \
  -v ~/.aws:/root/.aws \
  amazon/aws-cli s3 sync s3://mon-bucket/backups/latest/ /data
```

---

## 12. Différences Linux vs Windows {#differences}

### Chemins de fichiers

```bash
# Linux/Mac
docker run -v /home/user/data:/app/data nginx

# Windows CMD
docker run -v C:\Users\user\data:/app/data nginx

# Windows PowerShell
docker run -v ${PWD}/data:/app/data nginx

# WSL2 (accès aux fichiers Windows)
docker run -v /mnt/c/Users/user/data:/app/data nginx
```

### Line endings (CRLF vs LF)

```bash
# Problème: scripts avec CRLF ne fonctionnent pas sur Linux

# Solution 1: .gitattributes
* text=auto
*.sh text eol=lf
*.py text eol=lf

# Solution 2: Convertir avec dos2unix dans le Dockerfile
RUN apt-get update && apt-get install -y dos2unix
COPY script.sh /app/
RUN dos2unix /app/script.sh

# Solution 3: VSCode setting
# "files.eol": "\n"
```

### Performance

```bash
# Sur Windows avec WSL2:
# ✅ BON: Volumes Docker natifs (rapides)
docker run -v mon-volume:/app/data nginx

# ❌ LENT: Bind mounts Windows -> WSL2 (lent à cause du layer de traduction)
docker run -v /mnt/c/Users/data:/app/data nginx

# ✅ MEILLEUR: Fichiers dans WSL2
# Stocker les projets dans \\wsl$\Ubuntu\home\user\projects
docker run -v ~/projects/data:/app/data nginx
```

### Réseau

```bash
# Linux: localhost fonctionne directement
curl http://localhost:8080

# Windows Docker Desktop: localhost fonctionne aussi
curl http://localhost:8080

# Mais en WSL2, parfois besoin de l'IP de l'hôte
# Obtenir l'IP de l'hôte Windows depuis WSL2
grep nameserver /etc/resolv.conf | awk '{print $2}'
```

### Docker Desktop vs Docker Engine

```yaml
# Docker Desktop (Windows/Mac):
# - Interface graphique
# - Kubernetes intégré
# - Gestion automatique des ressources
# - Mise à jour automatique

# Docker Engine (Linux):
# - Ligne de commande uniquement
# - Plus léger
# - Contrôle total des ressources
# - Installation manuelle des outils
```

### Scripts cross-platform

```bash
# Utiliser des variables pour les chemins

# Linux/Mac
DATA_PATH="$(pwd)/data"

# Windows PowerShell
$DATA_PATH = "${PWD}/data"

# Docker run
docker run -v "${DATA_PATH}:/app/data" nginx
```

---

## 13. Cas Pratiques {#cas-pratiques}

### Stack complète Odoo + PostgreSQL

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=odoo
      - POSTGRES_PASSWORD=odoo_password
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - odoo-db-data:/var/lib/postgresql/data/pgdata
    networks:
      - odoo-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U odoo"]
      interval: 10s
      timeout: 5s
      retries: 5

  odoo:
    image: odoo:17
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "8069:8069"
    environment:
      - HOST=postgres
      - USER=odoo
      - PASSWORD=odoo_password
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
      - ./config:/etc/odoo
    networks:
      - odoo-network
    restart: unless-stopped

volumes:
  odoo-web-data:
  odoo-db-data:

networks:
  odoo-network:
    driver: bridge
```

### Stack Next.js + FastAPI + PostgreSQL + Redis + MinIO

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Frontend Next.js
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - /app/node_modules
      - /app/.next
    networks:
      - frontend-net
    depends_on:
      - backend
    restart: unless-stopped

  # Backend FastAPI
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@postgres:5432/mydb
      - REDIS_URL=redis://redis:6379/0
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ACCESS_KEY=minioadmin
      - MINIO_SECRET_KEY=minioadmin123
      - JWT_SECRET=${JWT_SECRET}
    env_file:
      - .env
    volumes:
      - ./backend/app:/app/app
      - backend-uploads:/app/uploads
    networks:
      - frontend-net
      - backend-net
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
      minio:
        condition: service_healthy
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - backend-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    networks:
      - backend-net
    restart: unless-stopped

  # MinIO (S3-compatible)
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=minioadmin
      - MINIO_ROOT_PASSWORD=minioadmin123
    volumes:
      - minio-data:/data
    networks:
      - backend-net
    command: server /data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
    restart: unless-stopped

  # Nginx (reverse proxy + SSL)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    networks:
      - frontend-net
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres-data:
  redis-data:
  minio-data:
  backend-uploads:

networks:
  frontend-net:
  backend-net:
    internal: true  # Pas d'accès Internet direct
```

### Configuration Nginx
```nginx
# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream backend {
        server backend:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # API
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

### Commandes de gestion

```bash
# Démarrer toute la stack
docker compose up -d

# Voir les logs
docker compose logs -f

# Rebuild un service
docker compose up -d --build backend

# Restart un service
docker compose restart backend

# Shell dans un service
docker compose exec backend bash

# Exécuter des migrations
docker compose exec backend python manage.py migrate

# Backup PostgreSQL
docker compose exec postgres pg_dump -U user mydb > backup.sql

# Arrêter tout
docker compose down

# Arrêter et supprimer les données
docker compose down --volumes
```

---

## Ressources supplémentaires

### Documentation officielle
- Docker: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Dockerfile reference: https://docs.docker.com/engine/reference/builder/

### Best practices
- Docker best practices: https://docs.docker.com/develop/dev-best-practices/
- Security: https://docs.docker.com/engine/security/
- Multi-stage builds: https://docs.docker.com/build/building/multi-stage/

### Commandes de référence rapide

```bash
# Images
docker images                          # Lister
docker pull IMAGE                      # Télécharger
docker build -t NAME .                 # Construire
docker rmi IMAGE                       # Supprimer

# Conteneurs
docker ps                              # Lister (actifs)
docker ps -a                           # Lister (tous)
docker run IMAGE                       # Créer et lancer
docker start CONTAINER                 # Démarrer
docker stop CONTAINER                  # Arrêter
docker rm CONTAINER                    # Supprimer

# Volumes
docker volume ls                       # Lister
docker volume create NAME              # Créer
docker volume rm NAME                  # Supprimer

# Réseaux
docker network ls                      # Lister
docker network create NAME             # Créer
docker network rm NAME                 # Supprimer

# Compose
docker compose up -d                   # Démarrer
docker compose down                    # Arrêter
docker compose logs -f                 # Logs
docker compose exec SERVICE bash       # Shell

# Nettoyage
docker system prune                    # Nettoyer tout
docker image prune -a                  # Nettoyer images
docker volume prune                    # Nettoyer volumes

# Debug
docker logs CONTAINER                  # Logs
docker exec -it CONTAINER bash         # Shell
docker inspect CONTAINER               # Détails
docker stats                           # Stats
```

---

**Dernière mise à jour**: Décembre 2025
