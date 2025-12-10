# 📦 Conteneurs Docker

[← Images](./infos-docker-02-images.md) | [Index](./infos-docker-00-index.md) | [Volumes →](./infos-docker-04-volumes.md)

---

## Table des matières
- [Qu'est-ce qu'un conteneur ?](#quest-ce-quun-conteneur)
- [Cycle de vie d'un conteneur](#cycle-de-vie-dun-conteneur)
- [Créer et exécuter des conteneurs](#creer-et-executer-des-conteneurs)
- [Gérer les conteneurs](#gerer-les-conteneurs)
- [Interagir avec les conteneurs](#interagir-avec-les-conteneurs)
- [Logs et monitoring](#logs-et-monitoring)
- [Ressources et limites](#ressources-et-limites)
- [Variables d'environnement](#variables-denvironnement)
- [Conteneurs stateless vs stateful](#conteneurs-stateless-vs-stateful)

---

## Qu'est-ce qu'un conteneur ?

### Définition

Un **conteneur** est une **instance exécutable** d'une image Docker.

```
Image Docker = Modèle/Template (lecture seule)
           ↓
Conteneur = Instance en cours d'exécution (lecture/écriture)

Analogie:
Image    = Classe (en POO)
Conteneur = Objet/Instance de cette classe
```

### Conteneur vs Machine Virtuelle

```
┌─────────────────────────────┐  ┌─────────────────────────────┐
│   Machine Virtuelle (VM)    │  │     Conteneur Docker        │
├─────────────────────────────┤  ├─────────────────────────────┤
│   App A   │   App B         │  │   App A   │   App B         │
│   Bins    │   Bins          │  │   Bins    │   Bins          │
│   Guest OS│   Guest OS      │  ├─────────────────────────────┤
├─────────────────────────────┤  │     Docker Engine           │
│      Hypervisor             │  ├─────────────────────────────┤
├─────────────────────────────┤  │       Host OS               │
│       Host OS               │  ├─────────────────────────────┤
│       Hardware              │  │       Hardware              │
└─────────────────────────────┘  └─────────────────────────────┘

VM:                             Conteneur:
- OS complet par VM             - Partage le kernel de l'hôte
- Lourd (plusieurs Go)          - Léger (quelques Mo)
- Démarrage lent (minutes)      - Démarrage rapide (secondes)
- Isolation forte               - Isolation via namespaces
```

### Architecture d'un conteneur

```
┌───────────────────────────────────┐
│         Application               │  Votre code
├───────────────────────────────────┤
│      Bibliothèques/Dépendances    │  npm, pip, etc.
├───────────────────────────────────┤
│      Filesystem (Layer R/W)       │  Modifications du conteneur
├───────────────────────────────────┤
│      Image Layers (R/O)           │  Layers de l'image
├───────────────────────────────────┤
│      Docker Engine                │  Runtime
├───────────────────────────────────┤
│      Linux Kernel                 │  Kernel partagé
└───────────────────────────────────┘
```

---

## Cycle de vie d'un conteneur

### États d'un conteneur

```
       docker run
┌──────────────────►  RUNNING  ◄──────────┐
│                        │                 │
│                        │ docker stop     │ docker start
│                        ▼                 │
│                    STOPPED ──────────────┘
│                        │
│                        │ docker rm
Created ────────────────▼
                     REMOVED
```

### Commandes du cycle de vie

```bash
# 1. CREATED → RUNNING
docker run ubuntu echo "Hello"
# Crée ET démarre le conteneur

# 2. RUNNING → STOPPED
docker stop <container_id>
# Arrêt gracieux (SIGTERM puis SIGKILL après 10s)

docker kill <container_id>
# Arrêt immédiat (SIGKILL)

# 3. STOPPED → RUNNING
docker start <container_id>
# Redémarre un conteneur arrêté

# 4. RUNNING → PAUSED
docker pause <container_id>
# Suspend les processus (SIGSTOP)

docker unpause <container_id>
# Reprend les processus (SIGCONT)

# 5. STOPPED/RUNNING → REMOVED
docker rm <container_id>         # Si stopped
docker rm -f <container_id>      # Force remove (running)
```

---

## Créer et exécuter des conteneurs

### docker run - Syntaxe complète

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

# Exemple simple
docker run ubuntu echo "Hello Docker"

# Exemple avec options
docker run \
  --name mon-conteneur \          # Nom du conteneur
  -d \                            # Detached mode (arrière-plan)
  -p 8080:80 \                    # Port mapping (host:container)
  -v /host/data:/container/data \ # Volume mount
  -e ENV_VAR=value \              # Variable d'environnement
  --restart unless-stopped \      # Politique de redémarrage
  --memory="512m" \               # Limite mémoire
  --cpus="1.5" \                  # Limite CPU
  nginx:latest                    # Image à utiliser
```

### Mode interactif vs détaché

```bash
# ✅ Mode INTERACTIF (-it)
docker run -it ubuntu bash
# -i : interactive (garde STDIN ouvert)
# -t : tty (alloue un pseudo-terminal)
# Permet d'interagir avec le conteneur

# Exemple: Shell interactif
docker run -it --rm alpine sh
# --rm : supprime automatiquement à la sortie

# ✅ Mode DÉTACHÉ (-d)
docker run -d nginx
# Le conteneur tourne en arrière-plan
# Retourne l'ID du conteneur

# Voir les logs
docker logs <container_id>

# Attacher à un conteneur détaché
docker attach <container_id>
# Ctrl+P puis Ctrl+Q pour détacher sans arrêter
```

### Exemples pratiques

```bash
# 1. Serveur web Nginx
docker run -d \
  --name web-server \
  -p 8080:80 \
  nginx:alpine

# Tester: http://localhost:8080

# 2. Base de données PostgreSQL
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_USER=admin \
  -e POSTGRES_DB=mydb \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

# 3. Application Node.js
docker run -d \
  --name node-app \
  -p 3000:3000 \
  -v $(pwd):/app \
  -w /app \
  node:18 \
  npm start

# 4. Redis cache
docker run -d \
  --name redis-cache \
  -p 6379:6379 \
  --memory="256m" \
  redis:7-alpine

# 5. Commande ponctuelle
docker run --rm \
  -v $(pwd):/workspace \
  -w /workspace \
  node:18 \
  npm install
# --rm : supprime le conteneur après exécution
```

---

## Gérer les conteneurs

### Lister les conteneurs

```bash
# Conteneurs en cours d'exécution
docker ps
docker container ls

# Tous les conteneurs (running + stopped)
docker ps -a
docker container ls -a

# Derniers conteneurs créés
docker ps -n 5
# Affiche les 5 derniers

# Format personnalisé
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"

# Filtrer
docker ps --filter "status=running"
docker ps --filter "name=web"
docker ps --filter "ancestor=nginx"
```

### Démarrer et arrêter

```bash
# Démarrer
docker start <container_name_or_id>

# Démarrer et attacher
docker start -a <container>

# Démarrer plusieurs conteneurs
docker start container1 container2 container3

# Arrêter
docker stop <container>
# Timeout par défaut: 10 secondes

# Arrêter avec timeout personnalisé
docker stop -t 30 <container>

# Arrêt immédiat
docker kill <container>

# Redémarrer
docker restart <container>

# Arrêter tous les conteneurs
docker stop $(docker ps -q)
```

### Supprimer des conteneurs

```bash
# Supprimer un conteneur arrêté
docker rm <container>

# Forcer la suppression (même en running)
docker rm -f <container>

# Supprimer plusieurs conteneurs
docker rm container1 container2

# Supprimer tous les conteneurs arrêtés
docker container prune

# Supprimer TOUS les conteneurs (⚠️ ATTENTION)
docker rm -f $(docker ps -aq)

# Supprimer avec filtre
docker ps -a --filter "status=exited" -q | xargs docker rm
```

### Renommer et mettre à jour

```bash
# Renommer
docker rename old-name new-name

# Mettre à jour les ressources
docker update --memory="1g" --cpus="2" <container>

# Changer la politique de redémarrage
docker update --restart=always <container>
```

---

## Interagir avec les conteneurs

### Exécuter des commandes

```bash
# Exécuter une commande dans un conteneur running
docker exec <container> <command>

# Exemples:
docker exec web-server ls /usr/share/nginx/html
docker exec postgres-db psql -U admin -d mydb -c "SELECT version();"

# Shell interactif
docker exec -it <container> bash
docker exec -it <container> sh      # Pour Alpine

# En tant qu'utilisateur spécifique
docker exec -u root -it <container> bash

# Avec variables d'environnement
docker exec -e VAR=value <container> env

# Avec working directory
docker exec -w /app <container> ls -la
```

### Copier des fichiers

```bash
# Copier du host vers le conteneur
docker cp /host/path/file.txt <container>:/container/path/

# Exemples:
docker cp index.html web-server:/usr/share/nginx/html/
docker cp config.json node-app:/app/config/

# Copier du conteneur vers le host
docker cp <container>:/container/path/file.txt /host/path/

# Exemples:
docker cp web-server:/var/log/nginx/access.log ./logs/
docker cp postgres-db:/var/lib/postgresql/data/pg_hba.conf ./backup/

# Copier un dossier
docker cp /host/folder <container>:/container/folder
docker cp <container>:/container/folder ./backup/

# Utilisation avec tar
docker cp <container>:/app - | tar -x -C ./backup/
```

### Inspecter un conteneur

```bash
# Informations complètes (JSON)
docker inspect <container>

# Récupérer une valeur spécifique
docker inspect --format='{{.State.Status}}' <container>
docker inspect --format='{{.NetworkSettings.IPAddress}}' <container>
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container>

# Plusieurs conteneurs
docker inspect container1 container2

# Exemples pratiques:
# IP du conteneur
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web-server

# Volumes montés
docker inspect -f '{{.Mounts}}' <container>

# Variables d'environnement
docker inspect -f '{{.Config.Env}}' <container>

# Commande de démarrage
docker inspect -f '{{.Config.Cmd}}' <container>
```

---

## Logs et monitoring

### Voir les logs

```bash
# Afficher les logs
docker logs <container>

# Suivre les logs en temps réel (like tail -f)
docker logs -f <container>

# Dernières lignes
docker logs --tail 100 <container>

# Logs depuis un timestamp
docker logs --since 2024-01-01 <container>
docker logs --since 1h <container>
docker logs --since 30m <container>

# Logs jusqu'à un timestamp
docker logs --until 2024-01-02 <container>

# Avec timestamps
docker logs -t <container>

# Exemples combinés:
docker logs -f --tail 50 web-server
docker logs --since 1h --until 30m web-server
```

### Statistiques des conteneurs

```bash
# Stats en temps réel
docker stats

# Stats d'un conteneur spécifique
docker stats <container>

# Sans streaming (snapshot)
docker stats --no-stream

# Format personnalisé
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Sortie:
CONTAINER ID   NAME          CPU %     MEM USAGE / LIMIT     MEM %
abc123         web-server    0.50%     50MiB / 512MiB       9.77%
def456         postgres-db   2.00%     200MiB / 1GiB        19.53%
```

### Événements Docker

```bash
# Suivre les événements Docker
docker events

# Filtrer par type
docker events --filter type=container

# Filtrer par action
docker events --filter event=start
docker events --filter event=stop
docker events --filter event=die

# Filtrer par conteneur
docker events --filter container=web-server

# Depuis un timestamp
docker events --since 1h
```

### Processus dans un conteneur

```bash
# Lister les processus
docker top <container>

# Avec format ps
docker top <container> aux
docker top <container> -ef

# Exemple:
docker top web-server
# UID   PID    PPID   C   STIME   TTY   TIME      CMD
# root  1234   1220   0   10:00   ?     00:00:01  nginx: master
# nginx 1235   1234   0   10:00   ?     00:00:00  nginx: worker
```

---

## Ressources et limites

### Limiter la mémoire

```bash
# Limite mémoire
docker run -d --memory="512m" nginx
docker run -d -m 512m nginx           # Alias

# Limite mémoire + swap
docker run -d --memory="512m" --memory-swap="1g" nginx

# Sans swap (memory-swap = memory)
docker run -d --memory="512m" --memory-swap="512m" nginx

# Réservation mémoire (soft limit)
docker run -d --memory-reservation="256m" nginx

# OOM (Out Of Memory) killer
docker run -d --oom-kill-disable nginx  # ⚠️ Dangereux

# Mettre à jour un conteneur existant
docker update --memory="1g" <container>
```

### Limiter le CPU

```bash
# Limiter le nombre de CPUs
docker run -d --cpus="1.5" nginx
# Utilise au maximum 1.5 CPU

# CPU shares (poids relatif)
docker run -d --cpu-shares=512 nginx
# Par défaut: 1024
# Un conteneur avec 512 aura la moitié de la priorité

# Épingler sur des CPUs spécifiques
docker run -d --cpuset-cpus="0,1" nginx
# Utilise uniquement les CPU 0 et 1

# Quota CPU (microseconds)
docker run -d --cpu-period=100000 --cpu-quota=50000 nginx
# Limite à 50% d'un CPU

# Mettre à jour
docker update --cpus="2" <container>
```

### Limiter les I/O

```bash
# Limite lecture/écriture (bytes par seconde)
docker run -d \
  --device-read-bps=/dev/sda:10mb \
  --device-write-bps=/dev/sda:5mb \
  nginx

# Limite IOPS
docker run -d \
  --device-read-iops=/dev/sda:1000 \
  --device-write-iops=/dev/sda:500 \
  nginx

# Poids I/O (relatif, 10-1000)
docker run -d --blkio-weight=500 nginx
```

### Limiter les PID

```bash
# Limite le nombre de processus
docker run -d --pids-limit=100 nginx

# Illimité
docker run -d --pids-limit=-1 nginx
```

### Exemple complet avec limites

```bash
docker run -d \
  --name production-app \
  --memory="2g" \
  --memory-swap="2g" \
  --cpus="2" \
  --pids-limit=200 \
  --restart=always \
  -p 8080:8080 \
  my-app:latest
```

---

## Variables d'environnement

### Passer des variables

```bash
# Une variable
docker run -d -e NODE_ENV=production node-app

# Plusieurs variables
docker run -d \
  -e NODE_ENV=production \
  -e PORT=3000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/mydb \
  node-app

# Depuis un fichier .env
# Fichier .env:
# NODE_ENV=production
# PORT=3000
# API_KEY=secret123

docker run -d --env-file .env node-app

# Variable sans valeur (hérite du host)
docker run -d -e HOME node-app
```

### Voir les variables

```bash
# Variables d'un conteneur
docker exec <container> env

# Ou via inspect
docker inspect -f '{{.Config.Env}}' <container>

# Filtrer une variable spécifique
docker exec <container> printenv NODE_ENV
```

### Best practices

```bash
# ❌ MAUVAIS: Secrets en clair
docker run -d -e PASSWORD=secret123 app

# ✅ BON: Utiliser Docker Secrets (Swarm)
echo "secret123" | docker secret create db_password -
docker service create --secret db_password app

# ✅ BON: Fichier .env avec .gitignore
# .env
PASSWORD=secret123

# .gitignore
.env

# ✅ BON: Variables depuis le host
docker run -d -e PASSWORD="${DB_PASSWORD}" app

# ✅ BON: Utiliser un secret manager
docker run -d -e PASSWORD="$(aws secretsmanager get-secret-value --secret-id db-pass)" app
```

---

## Conteneurs stateless vs stateful

### Conteneurs stateless

**Caractéristiques:**
- Aucune donnée persistante
- Facilement remplaçables
- Scalabilité horizontale simple
- Parfait pour applications sans état

```bash
# Exemple: API REST stateless
docker run -d \
  --name api-server \
  -p 8080:8080 \
  --restart=always \
  my-api:latest

# Peut être supprimé et recréé sans perte de données
docker rm -f api-server
docker run -d --name api-server -p 8080:8080 my-api:latest
```

### Conteneurs stateful

**Caractéristiques:**
- Stockent des données importantes
- Nécessitent des volumes
- Plus complexes à gérer
- Backup requis

```bash
# Exemple: Base de données PostgreSQL
docker run -d \
  --name postgres-db \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \  # ✅ Volume persistant
  -v /backup:/backup \                         # ✅ Backup location
  -p 5432:5432 \
  --restart=always \
  postgres:15

# Les données survivent à la suppression du conteneur
docker rm -f postgres-db
docker run -d \
  --name postgres-db \
  -v postgres-data:/var/lib/postgresql/data \  # Même volume
  postgres:15
# ✅ Données toujours présentes
```

### Politiques de redémarrage

```bash
# no (défaut): Ne redémarre jamais
docker run -d --restart=no nginx

# on-failure: Redémarre uniquement en cas d'erreur
docker run -d --restart=on-failure nginx
docker run -d --restart=on-failure:5 nginx  # Max 5 tentatives

# always: Toujours redémarrer
docker run -d --restart=always nginx

# unless-stopped: Comme always, sauf si manuellement arrêté
docker run -d --restart=unless-stopped nginx

# Changer la politique
docker update --restart=always <container>
```

---

## Nettoyage et maintenance

### Nettoyer les conteneurs

```bash
# Supprimer les conteneurs arrêtés
docker container prune

# Avec confirmation
docker container prune -f

# Supprimer selon un filtre
docker container prune --filter "until=24h"
```

### Libérer de l'espace

```bash
# Nettoyer tout (conteneurs, images, volumes, networks)
docker system prune

# Agressif (inclut images non utilisées)
docker system prune -a

# Inclure les volumes
docker system prune -a --volumes

# Voir l'espace utilisé
docker system df

# Détails par type
docker system df -v
```

---

## Commandes de référence rapide

```bash
# Cycle de vie
docker run [options] image              # Créer et démarrer
docker start <container>                # Démarrer
docker stop <container>                 # Arrêter
docker restart <container>              # Redémarrer
docker pause <container>                # Suspendre
docker unpause <container>              # Reprendre
docker rm <container>                   # Supprimer

# Lister et inspecter
docker ps                               # Conteneurs running
docker ps -a                            # Tous les conteneurs
docker inspect <container>              # Infos détaillées
docker logs -f <container>              # Logs en temps réel
docker stats                            # Statistiques

# Interaction
docker exec -it <container> bash        # Shell interactif
docker cp file <container>:/path        # Copier fichier

# Ressources
docker run --memory="512m" image        # Limite mémoire
docker run --cpus="1.5" image           # Limite CPU
docker update --memory="1g" container   # Mettre à jour

# Nettoyage
docker container prune                  # Supprimer stopped
docker system prune -a                  # Nettoyer tout
```

---

[← Images](./infos-docker-02-images.md) | [Index](./infos-docker-00-index.md) | [Volumes →](./infos-docker-04-volumes.md)
