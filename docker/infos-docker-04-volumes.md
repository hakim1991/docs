# 💾 Volumes Docker

[← Conteneurs](./infos-docker-03-conteneurs.md) | [Index](./infos-docker-00-index.md) | [Réseaux →](./infos-docker-05-reseaux.md)

---

## Table des matières
- [Qu'est-ce qu'un volume ?](#quest-ce-quun-volume)
- [Types de stockage](#types-de-stockage)
- [Volumes nommés](#volumes-nommes)
- [Bind mounts](#bind-mounts)
- [tmpfs mounts](#tmpfs-mounts)
- [Partager des volumes](#partager-des-volumes)
- [Backup et restauration](#backup-et-restauration)
- [Best practices](#best-practices)

---

## Qu'est-ce qu'un volume ?

### Le problème de la persistance

```
Conteneur sans volume:
┌─────────────────────┐
│   Application       │
│   ↓                 │
│   Données           │  ← Écrit dans le conteneur
└─────────────────────┘
         ↓
    docker rm
         ↓
    ❌ DONNÉES PERDUES

Conteneur avec volume:
┌─────────────────────┐     ┌──────────────┐
│   Application       │     │              │
│   ↓                 │ ←→  │   Volume     │  ← Persistant
│   Données           │     │  (Host disk) │
└─────────────────────┘     └──────────────┘
         ↓
    docker rm
         ↓
    ✅ DONNÉES CONSERVÉES
```

### Pourquoi des volumes ?

```bash
# ❌ SANS volume
docker run -d --name postgres postgres:15
# Créer des données...
docker rm -f postgres
docker run -d --name postgres postgres:15
# ❌ Toutes les données perdues !

# ✅ AVEC volume
docker run -d --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:15
# Créer des données...
docker rm -f postgres
docker run -d --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  postgres:15
# ✅ Données toujours présentes !
```

---

## Types de stockage

Docker propose **3 types** de stockage:

```
1. VOLUMES (Recommandé)
   /var/lib/docker/volumes/
   ├── volume1/
   ├── volume2/
   └── volume3/

   ✅ Géré par Docker
   ✅ Portable
   ✅ Backup facile
   ✅ Performance optimale

2. BIND MOUNTS
   Montage direct d'un dossier host
   /home/user/data → /container/data

   ✅ Accès direct aux fichiers
   ⚠️ Dépend du filesystem host
   ⚠️ Permissions complexes

3. TMPFS MOUNTS
   Stockage en RAM (temporaire)

   ✅ Très rapide
   ⚠️ Non persistant
   ⚠️ Limité par la RAM
```

### Comparaison

| Type | Localisation | Persistance | Gestion | Performance |
|------|-------------|-------------|---------|-------------|
| **Volume** | Géré par Docker | ✅ Oui | Docker | ⚡ Excellente |
| **Bind mount** | Choix libre | ✅ Oui | Utilisateur | ⚡ Bonne |
| **tmpfs** | RAM | ❌ Non | Docker | ⚡⚡ Très rapide |

---

## Volumes nommés

### Créer des volumes

```bash
# Créer un volume
docker volume create mon-volume

# Créer avec driver spécifique
docker volume create --driver local mon-volume

# Créer avec labels
docker volume create \
  --label project=myapp \
  --label env=production \
  mon-volume

# Créer avec options
docker volume create \
  --opt type=nfs \
  --opt o=addr=192.168.1.1,rw \
  --opt device=:/path/to/dir \
  nfs-volume
```

### Utiliser des volumes

```bash
# Utiliser un volume avec -v
docker run -d \
  --name web \
  -v mon-volume:/app/data \
  nginx

# Utiliser un volume avec --mount (syntaxe explicite)
docker run -d \
  --name web \
  --mount source=mon-volume,target=/app/data \
  nginx

# Volume en lecture seule
docker run -d \
  -v mon-volume:/app/data:ro \
  nginx

# Ou avec --mount
docker run -d \
  --mount source=mon-volume,target=/app/data,readonly \
  nginx

# Créer le volume automatiquement
docker run -d \
  -v auto-volume:/app/data \  # Créé si n'existe pas
  nginx
```

### Lister et inspecter

```bash
# Lister tous les volumes
docker volume ls

# Filtrer par nom
docker volume ls --filter name=mon

# Filtrer par label
docker volume ls --filter label=project=myapp

# Filtrer les volumes orphelins (non utilisés)
docker volume ls --filter dangling=true

# Inspecter un volume
docker volume inspect mon-volume

# Format JSON complet
docker volume inspect mon-volume

# Obtenir une propriété spécifique
docker volume inspect --format '{{.Mountpoint}}' mon-volume
# Retourne: /var/lib/docker/volumes/mon-volume/_data
```

### Exemples pratiques

```bash
# 1. PostgreSQL avec volume
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

# 2. MongoDB avec volume
docker run -d \
  --name mongodb \
  -v mongo-data:/data/db \
  -v mongo-config:/data/configdb \
  -p 27017:27017 \
  mongo:7

# 3. Redis avec volume
docker run -d \
  --name redis \
  -v redis-data:/data \
  -p 6379:6379 \
  redis:7 redis-server --appendonly yes

# 4. Nginx avec volumes multiples
docker run -d \
  --name nginx \
  -v nginx-html:/usr/share/nginx/html \
  -v nginx-config:/etc/nginx \
  -v nginx-logs:/var/log/nginx \
  -p 80:80 \
  nginx:alpine

# 5. Application Node.js
docker run -d \
  --name node-app \
  -v app-data:/app/data \
  -v app-logs:/app/logs \
  -v app-uploads:/app/uploads \
  -p 3000:3000 \
  node-app:latest
```

---

## Bind mounts

### Qu'est-ce qu'un bind mount ?

**Bind mount** = Monter un dossier/fichier du host directement dans le conteneur.

```
Host                    Conteneur
/home/user/project  →   /app
├── src/            →   ├── src/
├── public/         →   ├── public/
└── package.json    →   └── package.json

Modifications en temps réel des deux côtés !
```

### Utiliser des bind mounts

```bash
# Syntaxe -v
docker run -d \
  -v /host/path:/container/path \
  image

# Syntaxe --mount (recommandée, plus explicite)
docker run -d \
  --mount type=bind,source=/host/path,target=/container/path \
  image

# Exemple: Développement Node.js
docker run -d \
  --name node-dev \
  -v $(pwd):/app \
  -w /app \
  -p 3000:3000 \
  node:18 \
  npm run dev

# Windows (PowerShell)
docker run -d `
  --name node-dev `
  -v ${PWD}:/app `
  -w /app `
  -p 3000:3000 `
  node:18 `
  npm run dev

# Windows (cmd)
docker run -d ^
  --name node-dev ^
  -v %cd%:/app ^
  -w /app ^
  -p 3000:3000 ^
  node:18 ^
  npm run dev
```

### Bind mounts en lecture seule

```bash
# Lecture seule avec :ro
docker run -d \
  -v /host/config:/app/config:ro \
  nginx

# Avec --mount
docker run -d \
  --mount type=bind,source=/host/config,target=/app/config,readonly \
  nginx

# Cas d'usage: Configuration en lecture seule
docker run -d \
  --name web \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  -p 80:80 \
  nginx
```

### Exemples pratiques bind mounts

```bash
# 1. Développement React
docker run -d \
  --name react-dev \
  -v $(pwd):/app \
  -w /app \
  -p 3000:3000 \
  node:18 \
  npm start
# Le code modifié sur le host = hot-reload dans le conteneur

# 2. Développement Python/FastAPI
docker run -d \
  --name fastapi-dev \
  -v $(pwd):/app \
  -w /app \
  -p 8000:8000 \
  python:3.11 \
  uvicorn main:app --reload --host 0.0.0.0

# 3. Nginx avec config custom
docker run -d \
  --name nginx \
  -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  -v $(pwd)/logs:/var/log/nginx \
  -p 80:80 \
  nginx:alpine

# 4. PostgreSQL avec init scripts
docker run -d \
  --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  -v $(pwd)/init-scripts:/docker-entrypoint-initdb.d:ro \
  -e POSTGRES_PASSWORD=secret \
  postgres:15

# 5. Partager le socket Docker (Docker-in-Docker)
docker run -d \
  --name dind \
  -v /var/run/docker.sock:/var/run/docker.sock \
  docker:latest
```

---

## tmpfs mounts

### Qu'est-ce qu'un tmpfs ?

**tmpfs** = Stockage temporaire en **RAM** (non persistant).

```
Conteneur
┌─────────────────┐
│  Application    │
│  ↓              │
│  /tmp (RAM)     │  ← Très rapide, mais volatile
└─────────────────┘

Redémarrage → Données perdues
```

### Utiliser tmpfs

```bash
# Syntaxe --tmpfs
docker run -d \
  --tmpfs /app/cache \
  nginx

# Syntaxe --mount (recommandée)
docker run -d \
  --mount type=tmpfs,target=/app/cache \
  nginx

# Avec taille limite
docker run -d \
  --mount type=tmpfs,target=/app/cache,tmpfs-size=100m \
  nginx

# Avec mode (permissions)
docker run -d \
  --mount type=tmpfs,target=/app/cache,tmpfs-mode=1770 \
  nginx
```

### Cas d'usage tmpfs

```bash
# 1. Cache temporaire
docker run -d \
  --name app \
  --mount type=tmpfs,target=/app/cache,tmpfs-size=500m \
  my-app

# 2. Fichiers temporaires sensibles
docker run -d \
  --name secure-app \
  --mount type=tmpfs,target=/tmp/secrets,tmpfs-mode=700 \
  secure-app

# 3. Build temporaire
docker run --rm \
  --mount type=tmpfs,target=/tmp/build,tmpfs-size=2g \
  build-tool

# 4. Session storage
docker run -d \
  --name web-app \
  --mount type=tmpfs,target=/app/sessions,tmpfs-size=200m \
  web-app
```

---

## Partager des volumes

### Entre conteneurs

```bash
# Créer un conteneur avec volume
docker run -d \
  --name producer \
  -v shared-data:/data \
  producer-app

# Partager le même volume avec un autre conteneur
docker run -d \
  --name consumer \
  -v shared-data:/data:ro \  # Lecture seule
  consumer-app

# Ou utiliser --volumes-from
docker run -d \
  --name consumer2 \
  --volumes-from producer \
  consumer-app
```

### Pattern data container

```bash
# 1. Créer un conteneur de données (ne tourne pas)
docker create \
  --name data-container \
  -v /data \
  busybox

# 2. Utiliser ce conteneur comme source de volumes
docker run -d \
  --name app1 \
  --volumes-from data-container \
  app-image

docker run -d \
  --name app2 \
  --volumes-from data-container \
  app-image

# Les deux conteneurs partagent le même volume
```

### Exemple: Application + Base de données

```bash
# Volume partagé pour backup
docker volume create backup-vol

# PostgreSQL
docker run -d \
  --name postgres \
  -v postgres-data:/var/lib/postgresql/data \
  -v backup-vol:/backup \
  postgres:15

# Application avec accès au backup
docker run -d \
  --name backup-service \
  -v backup-vol:/backup \
  backup-app

# Backup manuel
docker exec postgres \
  pg_dump -U postgres mydb > /backup/dump.sql
```

---

## Backup et restauration

### Backup d'un volume

```bash
# Méthode 1: Copie avec conteneur temporaire
docker run --rm \
  -v mon-volume:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar czf /backup/backup.tar.gz /data

# Méthode 2: Via conteneur existant
docker exec -it postgres \
  tar czf /backup/db-backup.tar.gz /var/lib/postgresql/data

# Méthode 3: Copier tout le volume
docker run --rm \
  -v mon-volume:/source:ro \
  -v $(pwd):/backup \
  alpine \
  sh -c "cd /source && tar czf /backup/volume-backup.tar.gz ."

# Backup PostgreSQL
docker exec postgres \
  pg_dump -U postgres -d mydb -F c -f /backup/mydb.dump

# Backup MySQL
docker exec mysql \
  mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" --all-databases > backup.sql

# Backup MongoDB
docker exec mongodb \
  mongodump --out /backup/mongo-backup
```

### Restauration d'un volume

```bash
# Méthode 1: Extraction du tar
docker run --rm \
  -v mon-volume:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar xzf /backup/backup.tar.gz -C /

# Méthode 2: Créer nouveau volume et restaurer
docker volume create mon-volume-restored

docker run --rm \
  -v mon-volume-restored:/data \
  -v $(pwd):/backup \
  ubuntu \
  tar xzf /backup/backup.tar.gz -C /data --strip-components=1

# Restauration PostgreSQL
docker exec -i postgres \
  pg_restore -U postgres -d mydb -F c < backup/mydb.dump

# Restauration MySQL
docker exec -i mysql \
  mysql -u root -p"$MYSQL_ROOT_PASSWORD" < backup.sql

# Restauration MongoDB
docker cp backup/mongo-backup mongodb:/backup
docker exec mongodb \
  mongorestore /backup/mongo-backup
```

### Script de backup automatique

```bash
#!/bin/bash
# backup-docker-volumes.sh

BACKUP_DIR="/backup/docker-volumes"
DATE=$(date +%Y%m%d-%H%M%S)

# Créer le dossier de backup
mkdir -p "$BACKUP_DIR"

# Lister tous les volumes
for volume in $(docker volume ls -q); do
    echo "Backing up volume: $volume"

    docker run --rm \
        -v "$volume:/source:ro" \
        -v "$BACKUP_DIR:/backup" \
        alpine \
        tar czf "/backup/${volume}-${DATE}.tar.gz" -C /source .

    echo "✅ Backup saved: ${volume}-${DATE}.tar.gz"
done

# Nettoyer les backups > 7 jours
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup completed"
```

### Automatiser avec cron

```bash
# Ajouter au crontab
crontab -e

# Backup quotidien à 2h du matin
0 2 * * * /path/to/backup-docker-volumes.sh >> /var/log/docker-backup.log 2>&1

# Backup toutes les 6 heures
0 */6 * * * /path/to/backup-docker-volumes.sh >> /var/log/docker-backup.log 2>&1
```

---

## Gestion des volumes

### Supprimer des volumes

```bash
# Supprimer un volume
docker volume rm mon-volume

# Supprimer plusieurs volumes
docker volume rm volume1 volume2 volume3

# Supprimer les volumes non utilisés
docker volume prune

# Avec force
docker volume prune -f

# Supprimer volumes selon filtre
docker volume prune --filter "label=temporary=true"

# ⚠️ Supprimer TOUS les volumes non utilisés
docker volume prune -a
```

### Copier/Cloner un volume

```bash
# Cloner un volume
# 1. Créer le nouveau volume
docker volume create volume-copy

# 2. Copier les données
docker run --rm \
  -v original-volume:/source:ro \
  -v volume-copy:/dest \
  alpine \
  sh -c "cp -a /source/. /dest/"

# Méthode alternative avec tar
docker run --rm \
  -v original-volume:/source:ro \
  -v volume-copy:/dest \
  alpine \
  sh -c "cd /source && tar cf - . | (cd /dest && tar xf -)"
```

### Migrer un volume

```bash
# Migrer vers un autre host

# Sur le host source:
docker run --rm \
  -v mon-volume:/data:ro \
  alpine \
  tar czf - -C /data . > volume-backup.tar.gz

# Transférer le fichier vers le nouveau host
scp volume-backup.tar.gz user@new-host:/tmp/

# Sur le nouveau host:
docker volume create mon-volume

docker run --rm \
  -v mon-volume:/data \
  -i alpine \
  tar xzf - -C /data < /tmp/volume-backup.tar.gz
```

---

## Best practices

### Recommandations

```bash
# ✅ BON: Utiliser des volumes nommés pour données importantes
docker run -d -v postgres-data:/var/lib/postgresql/data postgres

# ❌ MAUVAIS: Stocker dans le conteneur
docker run -d postgres  # Données perdues à chaque rm !

# ✅ BON: Bind mounts pour développement
docker run -v $(pwd):/app node npm run dev

# ❌ MAUVAIS: Bind mounts en production
# Dépendance au filesystem host

# ✅ BON: tmpfs pour données temporaires sensibles
docker run --mount type=tmpfs,target=/tmp/secrets app

# ❌ MAUVAIS: Stocker secrets dans volume persistant
docker run -v secrets:/secrets app

# ✅ BON: Labels pour organisation
docker volume create --label env=prod --label app=web web-data

# ✅ BON: Backup réguliers
# Script cron pour backup automatique

# ✅ BON: Lecture seule quand possible
docker run -v config:/app/config:ro app
```

### Permissions et sécurité

```bash
# Problème: Fichiers créés par root dans bind mount
docker run -v $(pwd):/app alpine touch /app/file.txt
# file.txt appartient à root !

# Solution 1: Spécifier l'utilisateur
docker run --user $(id -u):$(id -g) -v $(pwd):/app alpine touch /app/file.txt

# Solution 2: Dans le Dockerfile
# USER node
# Ou créer un utilisateur non-root

# Volumes en lecture seule pour sécurité
docker run -v sensitive-config:/config:ro app

# Utiliser tmpfs pour données sensibles non persistantes
docker run --tmpfs /tmp/secrets:rw,noexec,nosuid,size=100m app
```

### Performance

```bash
# ✅ Utiliser volumes (pas bind mounts) en production
# Meilleure performance, surtout sur Mac/Windows

# ✅ tmpfs pour performances I/O maximales
docker run --tmpfs /app/cache:size=1g app

# ✅ Volumes avec options de montage
docker run \
  --mount type=volume,source=data,target=/data,volume-opt=type=nfs \
  app

# ⚠️ Attention aux bind mounts sur Mac/Windows
# Peuvent être lents (Docker Desktop + filesystem translation)
```

---

## Commandes de référence rapide

```bash
# Volumes nommés
docker volume create vol               # Créer
docker volume ls                       # Lister
docker volume inspect vol              # Inspecter
docker volume rm vol                   # Supprimer
docker volume prune                    # Nettoyer

# Utilisation
docker run -v vol:/path image          # Volume nommé
docker run -v /host:/container image   # Bind mount
docker run --tmpfs /path image         # tmpfs

# Options
-v vol:/path:ro                        # Lecture seule
-v vol:/path:rw                        # Lecture/écriture (défaut)

# Backup/Restauration
docker run --rm -v vol:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz /data
docker run --rm -v vol:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /

# Partage
docker run --volumes-from container1 image2

# Informations
docker system df -v                    # Espace utilisé
```

---

[← Conteneurs](./infos-docker-03-conteneurs.md) | [Index](./infos-docker-00-index.md) | [Réseaux →](./infos-docker-05-reseaux.md)
