# 🧹 Maintenance Docker

[← Registres et CI/CD](./infos-docker-08-registres-cicd.md) | [Index](./infos-docker-00-index.md) | [Debug et monitoring →](./infos-docker-10-debug-monitoring.md)

---

## Table des matières
- [Nettoyage des ressources](#nettoyage-des-ressources)
- [Gestion de l'espace disque](#gestion-de-lespace-disque)
- [Mises à jour](#mises-a-jour)
- [Sauvegardes](#sauvegardes)
- [Monitoring des ressources](#monitoring-des-ressources)
- [Automatisation de la maintenance](#automatisation-de-la-maintenance)

---

## Nettoyage des ressources

### Vue d'ensemble de l'espace

```bash
# Voir l'utilisation de l'espace
docker system df

# Résultat:
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          15        5         2.5GB     1.8GB (72%)
Containers      10        2         500MB     300MB (60%)
Local Volumes   5         3         1GB       500MB (50%)
Build Cache     50        0         3GB       3GB (100%)

# Vue détaillée
docker system df -v
```

### Nettoyer tout

```bash
# Nettoyage global (⚠️ ATTENTION)
docker system prune

# Supprime:
# - Conteneurs arrêtés
# - Réseaux non utilisés
# - Images pendantes (dangling)
# - Cache de build

# Mode agressif (supprime TOUT ce qui n'est pas utilisé)
docker system prune -a

# Inclure les volumes
docker system prune -a --volumes

# Sans confirmation
docker system prune -f

# Avec filtre temporel
docker system prune --filter "until=24h"
docker system prune --filter "until=168h"  # 7 jours
```

### Nettoyer les conteneurs

```bash
# Supprimer les conteneurs arrêtés
docker container prune

# Avec force
docker container prune -f

# Supprimer selon un filtre
docker container prune --filter "until=24h"
docker container prune --filter "label=temporary=true"

# Supprimer tous les conteneurs arrêtés (méthode alternative)
docker rm $(docker ps -aq -f status=exited)

# Forcer la suppression de TOUS les conteneurs (⚠️ DANGEREUX)
docker rm -f $(docker ps -aq)

# Supprimer les conteneurs créés il y a plus de X heures
docker ps -a --filter "status=exited" --filter "status=created" | \
  awk 'NR>1 {print $1}' | xargs docker rm
```

### Nettoyer les images

```bash
# Supprimer les images pendantes (dangling)
docker image prune

# Supprimer TOUTES les images non utilisées
docker image prune -a

# Avec force
docker image prune -af

# Avec filtre
docker image prune --filter "until=720h"  # 30 jours

# Supprimer une image spécifique
docker rmi image:tag

# Forcer la suppression
docker rmi -f image:tag

# Supprimer plusieurs images
docker rmi image1:tag image2:tag image3:tag

# Supprimer toutes les images d'un repository
docker rmi $(docker images 'myapp' -q)

# Supprimer toutes les images sans tag
docker rmi $(docker images -f "dangling=true" -q)
```

### Nettoyer les volumes

```bash
# Supprimer les volumes non utilisés
docker volume prune

# Avec force
docker volume prune -f

# Avec filtre
docker volume prune --filter "label=temporary=true"

# Supprimer un volume spécifique
docker volume rm volume-name

# Forcer la suppression
docker volume rm -f volume-name

# Supprimer plusieurs volumes
docker volume rm volume1 volume2 volume3

# Supprimer TOUS les volumes non utilisés (⚠️ ATTENTION)
docker volume rm $(docker volume ls -q)
```

### Nettoyer les réseaux

```bash
# Supprimer les réseaux non utilisés
docker network prune

# Avec force
docker network prune -f

# Avec filtre
docker network prune --filter "until=24h"

# Supprimer un réseau spécifique
docker network rm network-name

# Supprimer plusieurs réseaux
docker network rm network1 network2
```

### Nettoyer le cache de build

```bash
# Voir le cache de build
docker buildx du

# Supprimer le cache de build
docker builder prune

# Mode agressif (tout le cache)
docker builder prune -a

# Avec force
docker builder prune -af

# Avec filtre
docker builder prune --filter "until=24h"

# Garder seulement X Go de cache
docker builder prune --keep-storage 10GB
```

---

## Gestion de l'espace disque

### Analyser l'utilisation

```bash
# Vue globale
docker system df

# Détails complets
docker system df -v

# Taille des images
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Trier par taille
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | sort -k3 -h

# Historique d'une image (layers)
docker history image:tag

# Avec tailles
docker history --no-trunc image:tag

# Inspecter une image
docker inspect image:tag | grep Size
```

### Identifier les gros consommateurs

```bash
# Images les plus volumineuses
docker images --format '{{.Size}}\t{{.Repository}}:{{.Tag}}' | sort -h -r | head -20

# Conteneurs utilisant le plus d'espace
docker ps -as --format "table {{.Names}}\t{{.Size}}"

# Volumes par taille
docker volume ls -q | xargs docker volume inspect | \
  grep -A 5 Mountpoint | grep Mountpoint | \
  awk '{print $2}' | xargs du -sh | sort -h -r

# Build cache
docker buildx du
```

### Libérer de l'espace rapidement

```bash
# Script de nettoyage complet
#!/bin/bash

echo "🧹 Nettoyage Docker..."

echo "📦 Suppression des conteneurs arrêtés..."
docker container prune -f

echo "🖼️  Suppression des images non utilisées..."
docker image prune -a -f

echo "💾 Suppression des volumes non utilisés..."
docker volume prune -f

echo "🌐 Suppression des réseaux non utilisés..."
docker network prune -f

echo "🔨 Suppression du cache de build..."
docker builder prune -a -f

echo "✅ Nettoyage terminé!"
docker system df
```

---

## Mises à jour

### Mettre à jour Docker Engine

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get upgrade docker-ce docker-ce-cli containerd.io

# CentOS/RHEL
sudo yum update docker-ce docker-ce-cli containerd.io

# Vérifier la version
docker version

# Docker Desktop (Windows/Mac)
# Vérifie automatiquement les mises à jour
# Ou manuellement: Check for updates
```

### Mettre à jour les images

```bash
# Pull la dernière version d'une image
docker pull nginx:latest

# Mettre à jour toutes les images
docker images --format "{{.Repository}}:{{.Tag}}" | \
  grep -v "<none>" | \
  xargs -L1 docker pull

# Avec Docker Compose
docker compose pull

# Puis recréer les conteneurs
docker compose up -d

# Recréer seulement si l'image a changé
docker compose up -d --force-recreate
```

### Mettre à jour les conteneurs

```bash
# Stratégie 1: Stop, remove, run nouveau
docker stop mon-conteneur
docker rm mon-conteneur
docker pull image:latest
docker run -d --name mon-conteneur ... image:latest

# Stratégie 2: Avec Docker Compose
docker compose pull
docker compose up -d

# Stratégie 3: Rolling update (Swarm)
docker service update --image image:new-version service-name
```

### Automatiser les mises à jour

```bash
# Watchtower: Met à jour automatiquement les conteneurs
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 3600  # Vérifie toutes les heures

# Avec options
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --cleanup \          # Supprime les anciennes images
  --interval 86400 \   # Une fois par jour
  --include-stopped \  # Aussi les conteneurs arrêtés
  conteneur1 conteneur2  # Seulement ces conteneurs
```

---

## Sauvegardes

### Sauvegarder les images

```bash
# Sauvegarder une image
docker save -o myimage.tar myimage:latest

# Avec compression
docker save myimage:latest | gzip > myimage.tar.gz

# Sauvegarder plusieurs images
docker save -o images-backup.tar image1:latest image2:latest

# Restaurer une image
docker load -i myimage.tar
docker load < myimage.tar.gz
```

### Sauvegarder les conteneurs

```bash
# Export d'un conteneur (filesystem seulement)
docker export mon-conteneur > conteneur-backup.tar

# Import
docker import conteneur-backup.tar myimage:restored

# Commit un conteneur en image
docker commit mon-conteneur myimage:snapshot

# Avec métadonnées
docker commit \
  --author "Admin <admin@example.com>" \
  --message "Backup avant migration" \
  mon-conteneur \
  myimage:backup-20240101
```

### Sauvegarder les volumes

```bash
# Backup d'un volume
docker run --rm \
  -v mon-volume:/source:ro \
  -v $(pwd):/backup \
  alpine \
  tar czf /backup/mon-volume-backup.tar.gz -C /source .

# Restaurer un volume
docker run --rm \
  -v mon-volume:/target \
  -v $(pwd):/backup \
  alpine \
  tar xzf /backup/mon-volume-backup.tar.gz -C /target

# Script de backup automatique
#!/bin/bash
BACKUP_DIR="/backup/docker-volumes"
DATE=$(date +%Y%m%d-%H%M%S)

for volume in $(docker volume ls -q); do
    echo "Sauvegarde de $volume..."
    docker run --rm \
        -v "$volume:/source:ro" \
        -v "$BACKUP_DIR:/backup" \
        alpine \
        tar czf "/backup/${volume}-${DATE}.tar.gz" -C /source .
done

echo "✅ Sauvegardes terminées dans $BACKUP_DIR"
```

### Sauvegarder la configuration

```bash
# docker-compose.yml
cp docker-compose.yml docker-compose.yml.backup

# Variables d'environnement
cp .env .env.backup

# Toute la configuration d'un projet
tar czf project-backup-$(date +%Y%m%d).tar.gz \
  docker-compose.yml \
  .env \
  nginx.conf \
  Dockerfile

# Exporter la configuration Docker
docker inspect mon-conteneur > mon-conteneur-config.json
```

---

## Monitoring des ressources

### Utilisation CPU et mémoire

```bash
# Stats en temps réel
docker stats

# Un seul conteneur
docker stats mon-conteneur

# Sans streaming (snapshot)
docker stats --no-stream

# Format personnalisé
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Tous les conteneurs (y compris arrêtés)
docker stats --all
```

### Limites de ressources

```bash
# Définir des limites au démarrage
docker run -d \
  --name app \
  --memory="512m" \
  --memory-swap="1g" \
  --cpus="1.5" \
  --pids-limit=100 \
  myapp:latest

# Modifier les limites d'un conteneur existant
docker update --memory="1g" --cpus="2" mon-conteneur

# Voir les limites actuelles
docker inspect mon-conteneur | grep -A 10 HostConfig
```

### Logs

```bash
# Taille des logs
docker inspect --format='{{.LogPath}}' mon-conteneur | xargs du -h

# Nettoyer les logs (⚠️ Arrête le conteneur)
truncate -s 0 $(docker inspect --format='{{.LogPath}}' mon-conteneur)

# Configurer la rotation des logs
docker run -d \
  --name app \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myapp:latest

# Daemon configuration (/etc/docker/daemon.json)
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "5"
  }
}
```

---

## Automatisation de la maintenance

### Cron job de nettoyage

```bash
# Créer un script de maintenance
sudo nano /usr/local/bin/docker-cleanup.sh
```

```bash
#!/bin/bash
# docker-cleanup.sh

LOG_FILE="/var/log/docker-cleanup.log"

echo "$(date): Début du nettoyage Docker" >> $LOG_FILE

# Nettoyer les conteneurs arrêtés depuis plus de 24h
docker container prune -f --filter "until=24h" >> $LOG_FILE 2>&1

# Nettoyer les images non utilisées depuis plus de 7 jours
docker image prune -a -f --filter "until=168h" >> $LOG_FILE 2>&1

# Nettoyer les volumes non utilisés
docker volume prune -f >> $LOG_FILE 2>&1

# Nettoyer le cache de build
docker builder prune -f --keep-storage=5GB >> $LOG_FILE 2>&1

echo "$(date): Nettoyage terminé" >> $LOG_FILE
echo "---" >> $LOG_FILE

# Afficher l'espace libéré
docker system df >> $LOG_FILE
```

```bash
# Rendre exécutable
sudo chmod +x /usr/local/bin/docker-cleanup.sh

# Ajouter au crontab
sudo crontab -e

# Exécuter tous les dimanches à 3h du matin
0 3 * * 0 /usr/local/bin/docker-cleanup.sh

# Ou tous les jours à 2h
0 2 * * * /usr/local/bin/docker-cleanup.sh
```

### Script de backup automatique

```bash
#!/bin/bash
# docker-backup.sh

BACKUP_ROOT="/backup/docker"
DATE=$(date +%Y%m%d-%H%M%S)
RETENTION_DAYS=30

# Créer le dossier de backup
mkdir -p "$BACKUP_ROOT"/{images,volumes,configs}

# 1. Backup des images importantes
echo "🖼️  Backup des images..."
for image in $(docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>"); do
    filename=$(echo $image | tr '/:' '-')
    echo "  - $image"
    docker save $image | gzip > "$BACKUP_ROOT/images/${filename}-${DATE}.tar.gz"
done

# 2. Backup des volumes
echo "💾 Backup des volumes..."
for volume in $(docker volume ls -q); do
    echo "  - $volume"
    docker run --rm \
        -v "$volume:/source:ro" \
        -v "$BACKUP_ROOT/volumes:/backup" \
        alpine \
        tar czf "/backup/${volume}-${DATE}.tar.gz" -C /source .
done

# 3. Backup des configurations
echo "📝 Backup des configurations..."
cp -r /etc/docker "$BACKUP_ROOT/configs/docker-${DATE}"

# 4. Nettoyer les anciens backups
echo "🧹 Nettoyage des anciens backups (>$RETENTION_DAYS jours)..."
find "$BACKUP_ROOT" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup terminé: $BACKUP_ROOT"
```

### Monitoring avec alertes

```bash
# Script de monitoring
#!/bin/bash
# docker-monitor.sh

THRESHOLD_DISK=80  # Alerte si > 80% utilisé
THRESHOLD_MEM=90   # Alerte si > 90% mémoire

# Vérifier l'espace disque Docker
DISK_USAGE=$(docker system df --format "{{.Type}}\t{{.Size}}\t{{.Reclaimable}}" | \
  awk '/Images/ {print $2}' | sed 's/GB//')

if (( $(echo "$DISK_USAGE > 100" | bc -l) )); then
    echo "⚠️  ALERTE: Espace disque Docker > 100GB"
    # Envoyer une notification (email, Slack, etc.)
fi

# Vérifier la mémoire des conteneurs
docker stats --no-stream --format "table {{.Name}}\t{{.MemPerc}}" | \
  awk 'NR>1 {gsub("%","",$2); if($2>90) print "⚠️  "$1" utilise "$2"% de mémoire"}'

# Vérifier les conteneurs unhealthy
UNHEALTHY=$(docker ps --filter health=unhealthy --format "{{.Names}}")
if [ ! -z "$UNHEALTHY" ]; then
    echo "⚠️  ALERTE: Conteneurs unhealthy: $UNHEALTHY"
fi
```

### Healthchecks automatiques

```bash
# Vérifier et redémarrer les conteneurs problématiques
#!/bin/bash
# docker-health-check.sh

for container in $(docker ps --format "{{.Names}}"); do
    status=$(docker inspect --format='{{.State.Health.Status}}' $container 2>/dev/null)

    if [ "$status" = "unhealthy" ]; then
        echo "⚠️  $container est unhealthy, redémarrage..."
        docker restart $container

        # Attendre 30s et vérifier
        sleep 30
        new_status=$(docker inspect --format='{{.State.Health.Status}}' $container)

        if [ "$new_status" != "healthy" ]; then
            echo "❌ $container toujours problématique après redémarrage"
            # Alerte
        else
            echo "✅ $container rétabli"
        fi
    fi
done
```

---

## Best practices

```bash
# ✅ Nettoyage régulier (automatisé)
# Cron job quotidien ou hebdomadaire

# ✅ Rotation des logs
# Configurer dans daemon.json

# ✅ Limites de ressources
docker run --memory="512m" --cpus="1" app

# ✅ Healthchecks
# Dans Dockerfile ou docker-compose.yml

# ✅ Backups réguliers
# Volumes et configurations importantes

# ✅ Monitoring
# Stats, logs, alertes

# ✅ Politique de rétention
# Images: garder les 5 dernières versions
# Backups: garder 30 jours
# Logs: rotation tous les 10MB

# ✅ Documentation
# Garder une trace des configurations et procédures

# ✅ Tests de restauration
# Tester régulièrement les backups
```

---

## Commandes de référence rapide

```bash
# Nettoyage
docker system prune -af --volumes         # Tout nettoyer
docker container prune -f                 # Conteneurs arrêtés
docker image prune -af                    # Images non utilisées
docker volume prune -f                    # Volumes non utilisés
docker builder prune -af                  # Cache de build

# Espace
docker system df                          # Vue d'ensemble
docker system df -v                       # Détails

# Backup/Restore
docker save image > image.tar             # Sauvegarder image
docker load < image.tar                   # Restaurer image
docker export container > container.tar   # Exporter conteneur

# Monitoring
docker stats                              # Statistiques temps réel
docker logs -f container                  # Logs en direct
```

---

[← Registres et CI/CD](./infos-docker-08-registres-cicd.md) | [Index](./infos-docker-00-index.md) | [Debug et monitoring →](./infos-docker-10-debug-monitoring.md)
