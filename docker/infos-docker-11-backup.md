# 💾 Backup et Restauration

[← Debug et monitoring](./infos-docker-10-debug-monitoring.md) | [Index](./infos-docker-00-index.md) | [Différences Linux/Windows →](./infos-docker-12-differences-linux-windows.md)

---

## Table des matières
- [Stratégies de backup](#strategies-de-backup)
- [Backup des images](#backup-des-images)
- [Backup des conteneurs](#backup-des-conteneurs)
- [Backup des volumes](#backup-des-volumes)
- [Backup des configurations](#backup-des-configurations)
- [Automatisation](#automatisation)
- [Restauration](#restauration)

---

## Stratégies de backup

### Ce qu'il faut sauvegarder

```
📦 Images Docker
   ├─ Images personnalisées
   └─ Tags spécifiques

📂 Volumes
   ├─ Données applicatives
   ├─ Bases de données
   └─ Fichiers uploads

⚙️  Configurations
   ├─ docker-compose.yml
   ├─ .env
   ├─ Dockerfiles
   └─ Configs (nginx.conf, etc.)

🔐 Secrets & Credentials
   ├─ Certificats SSL
   ├─ Clés API
   └─ Tokens (en sécurité!)
```

### Fréquence recommandée

```
🔴 CRITIQUE (Quotidien)
   - Bases de données
   - Données utilisateurs
   - Fichiers transactionnels

🟡 IMPORTANT (Hebdomadaire)
   - Volumes applicatifs
   - Configurations
   - Images personnalisées

🟢 NORMAL (Mensuel)
   - Archives
   - Logs historiques
   - Données de référence
```

---

## Backup des images

### Sauvegarder une image

```bash
# Sauvegarder une seule image
docker save -o mon-image.tar mon-image:latest

# Avec compression gzip
docker save mon-image:latest | gzip > mon-image.tar.gz

# Avec compression bzip2 (meilleur ratio)
docker save mon-image:latest | bzip2 > mon-image.tar.bz2

# Sauvegarder avec plusieurs tags
docker save -o mon-image.tar mon-image:latest mon-image:1.0.0

# Voir la taille
ls -lh mon-image.tar.gz
```

### Sauvegarder plusieurs images

```bash
# Toutes les images d'un repository
docker save -o myapp-images.tar \
  $(docker images myapp --format "{{.Repository}}:{{.Tag}}")

# Toutes les images personnalisées (non officielles)
docker images --filter "reference=*/*" --format "{{.Repository}}:{{.Tag}}" | \
  xargs docker save -o custom-images.tar

# Script pour sauvegarder toutes les images
#!/bin/bash
BACKUP_DIR="/backup/docker-images"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR"

docker images --format "{{.Repository}}:{{.Tag}}" | \
  grep -v "<none>" | \
  while read image; do
    filename=$(echo $image | tr '/:' '-')
    echo "Sauvegarde de $image..."
    docker save "$image" | gzip > "$BACKUP_DIR/${filename}-${DATE}.tar.gz"
  done

echo "✅ Backup terminé dans $BACKUP_DIR"
```

### Restaurer une image

```bash
# Restaurer depuis un fichier tar
docker load -i mon-image.tar

# Depuis tar.gz
docker load < mon-image.tar.gz
gunzip -c mon-image.tar.gz | docker load

# Depuis bz2
bunzip2 -c mon-image.tar.bz2 | docker load

# Vérifier
docker images | grep mon-image
```

---

## Backup des conteneurs

### Export d'un conteneur

```bash
# Exporter le filesystem d'un conteneur
docker export mon-conteneur > conteneur-backup.tar

# Avec compression
docker export mon-conteneur | gzip > conteneur-backup.tar.gz

# Export avec métadonnées (via commit)
docker commit mon-conteneur mon-image:backup
docker save -o mon-image-backup.tar mon-image:backup
```

### Commit un conteneur en image

```bash
# Créer une image depuis un conteneur
docker commit mon-conteneur mon-image:snapshot

# Avec message et auteur
docker commit \
  --author "Admin <admin@example.com>" \
  --message "Backup avant mise à jour" \
  mon-conteneur \
  mon-image:backup-$(date +%Y%m%d)

# Avec pause (arrête temporairement le conteneur)
docker commit --pause mon-conteneur mon-image:snapshot

# Sans pause (risque d'incohérence)
docker commit --pause=false mon-conteneur mon-image:snapshot
```

### Restaurer un conteneur

```bash
# Depuis un export
docker import conteneur-backup.tar mon-image:restored

# Depuis une image commitée
docker run -d --name mon-conteneur-restored mon-image:backup

# Import avec configuration
docker import \
  --change "ENV DEBUG=false" \
  --change "EXPOSE 80" \
  conteneur-backup.tar \
  mon-image:restored
```

---

## Backup des volumes

### Backup manuel d'un volume

```bash
# Méthode 1: Tar dans un conteneur temporaire
docker run --rm \
  -v mon-volume:/source:ro \
  -v $(pwd):/backup \
  alpine \
  tar czf /backup/mon-volume-backup.tar.gz -C /source .

# Méthode 2: Avec timestamp
docker run --rm \
  -v mon-volume:/source:ro \
  -v $(pwd):/backup \
  alpine \
  tar czf /backup/mon-volume-$(date +%Y%m%d-%H%M%S).tar.gz -C /source .

# Méthode 3: Backup incrémental avec rsync
docker run --rm \
  -v mon-volume:/source:ro \
  -v $(pwd)/backup:/backup \
  alpine \
  sh -c "apk add rsync && rsync -av /source/ /backup/"
```

### Backup de bases de données

```bash
# PostgreSQL
docker exec postgres-db \
  pg_dump -U postgres -d mydb -F c -f /backup/mydb-$(date +%Y%m%d).dump

# Ou directement vers le host
docker exec postgres-db \
  pg_dump -U postgres -d mydb -F c > mydb-$(date +%Y%m%d).dump

# MySQL
docker exec mysql-db \
  mysqldump -u root -p"$MYSQL_ROOT_PASSWORD" --all-databases \
  > mysql-backup-$(date +%Y%m%d).sql

# MongoDB
docker exec mongodb \
  mongodump --out=/backup/mongo-$(date +%Y%m%d)

# Extraire le backup
docker cp mongodb:/backup/mongo-$(date +%Y%m%d) ./backups/

# Redis
docker exec redis redis-cli SAVE
docker exec redis cat /data/dump.rdb > redis-backup-$(date +%Y%m%d).rdb
```

### Backup de tous les volumes

```bash
#!/bin/bash
# backup-all-volumes.sh

BACKUP_DIR="/backup/docker-volumes"
DATE=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"

echo "🔍 Recherche des volumes..."
volumes=$(docker volume ls -q)

if [ -z "$volumes" ]; then
    echo "❌ Aucun volume trouvé"
    exit 0
fi

for volume in $volumes; do
    echo "💾 Backup de $volume..."

    docker run --rm \
        -v "$volume:/source:ro" \
        -v "$BACKUP_DIR:/backup" \
        alpine \
        tar czf "/backup/${volume}-${DATE}.tar.gz" -C /source . 2>/dev/null

    if [ $? -eq 0 ]; then
        size=$(du -h "$BACKUP_DIR/${volume}-${DATE}.tar.gz" | cut -f1)
        echo "  ✅ ${volume}: ${size}"
    else
        echo "  ❌ ${volume}: Échec"
    fi
done

echo ""
echo "📊 Résumé:"
echo "  Volumes sauvegardés: $(ls -1 $BACKUP_DIR/*${DATE}*.tar.gz | wc -l)"
echo "  Espace total: $(du -sh $BACKUP_DIR | cut -f1)"
echo "  Emplacement: $BACKUP_DIR"

# Nettoyer les backups > 30 jours
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +30 -delete
echo "  Nettoyage: Backups > 30 jours supprimés"
```

### Restaurer un volume

```bash
# Méthode 1: Créer le volume et restaurer
docker volume create mon-volume-restored

docker run --rm \
  -v mon-volume-restored:/target \
  -v $(pwd):/backup \
  alpine \
  tar xzf /backup/mon-volume-backup.tar.gz -C /target

# Méthode 2: Restaurer dans un volume existant (⚠️ écrase le contenu)
docker run --rm \
  -v mon-volume:/target \
  -v $(pwd):/backup \
  alpine \
  sh -c "rm -rf /target/* /target/..?* /target/.[!.]* 2>/dev/null; \
         tar xzf /backup/mon-volume-backup.tar.gz -C /target"

# Méthode 3: Restaurer une base de données PostgreSQL
docker exec -i postgres-db \
  pg_restore -U postgres -d mydb -c < mydb-backup.dump

# MySQL
docker exec -i mysql-db \
  mysql -u root -p"$MYSQL_ROOT_PASSWORD" < mysql-backup.sql

# MongoDB
docker cp mongo-backup mongodb:/backup
docker exec mongodb mongorestore /backup/mongo-backup
```

---

## Backup des configurations

### Docker Compose

```bash
# Backup simple
cp docker-compose.yml docker-compose.yml.backup

# Avec timestamp
cp docker-compose.yml docker-compose.yml.$(date +%Y%m%d)

# Backup de tout le projet
tar czf project-backup-$(date +%Y%m%d).tar.gz \
  docker-compose.yml \
  .env \
  Dockerfile \
  nginx.conf \
  configs/

# Exclure certains fichiers
tar czf project-backup-$(date +%Y%m%d).tar.gz \
  --exclude='node_modules' \
  --exclude='.git' \
  --exclude='*.log' \
  .
```

### Configuration Docker daemon

```bash
# Backup de /etc/docker/daemon.json
sudo cp /etc/docker/daemon.json /backup/daemon.json.$(date +%Y%m%d)

# Backup complet de la config Docker
sudo tar czf docker-config-$(date +%Y%m%d).tar.gz \
  /etc/docker/ \
  /etc/systemd/system/docker.service.d/ 2>/dev/null

# Exporter les configurations des conteneurs
for container in $(docker ps -q); do
    name=$(docker inspect --format='{{.Name}}' $container | sed 's/\///')
    docker inspect $container > "config-${name}.json"
done
```

### Secrets et certificats

```bash
# ⚠️ SÉCURITÉ: Chiffrer les backups contenant des secrets

# Backup chiffré avec GPG
tar czf - secrets/ | gpg --symmetric --cipher-algo AES256 -o secrets-backup-$(date +%Y%m%d).tar.gz.gpg

# Backup chiffré avec OpenSSL
tar czf - secrets/ | openssl enc -aes-256-cbc -salt -out secrets-backup-$(date +%Y%m%d).tar.gz.enc

# Déchiffrer avec GPG
gpg --decrypt secrets-backup.tar.gz.gpg | tar xzf -

# Déchiffrer avec OpenSSL
openssl enc -aes-256-cbc -d -in secrets-backup.tar.gz.enc | tar xzf -
```

---

## Automatisation

### Script de backup complet

```bash
#!/bin/bash
# docker-full-backup.sh

set -e

BACKUP_ROOT="/backup/docker"
DATE=$(date +%Y%m%d-%H%M%S)
RETENTION_DAYS=30
LOG_FILE="/var/log/docker-backup.log"

# Créer les dossiers
mkdir -p "$BACKUP_ROOT"/{images,volumes,configs}

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🚀 Début du backup Docker"

# 1. Backup des images
log "📦 Backup des images..."
for image in $(docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>"); do
    filename=$(echo $image | tr '/:' '-')
    log "  - $image"
    docker save "$image" | gzip > "$BACKUP_ROOT/images/${filename}-${DATE}.tar.gz" 2>> "$LOG_FILE"
done

# 2. Backup des volumes
log "💾 Backup des volumes..."
for volume in $(docker volume ls -q); do
    log "  - $volume"
    docker run --rm \
        -v "$volume:/source:ro" \
        -v "$BACKUP_ROOT/volumes:/backup" \
        alpine \
        tar czf "/backup/${volume}-${DATE}.tar.gz" -C /source . 2>> "$LOG_FILE"
done

# 3. Backup des bases de données
log "🗄️  Backup des bases de données..."

# PostgreSQL
if docker ps --format '{{.Names}}' | grep -q postgres; then
    postgres_container=$(docker ps --format '{{.Names}}' | grep postgres | head -1)
    log "  - PostgreSQL ($postgres_container)"
    docker exec "$postgres_container" \
        pg_dumpall -U postgres | gzip > "$BACKUP_ROOT/postgres-${DATE}.sql.gz" 2>> "$LOG_FILE"
fi

# MySQL
if docker ps --format '{{.Names}}' | grep -q mysql; then
    mysql_container=$(docker ps --format '{{.Names}}' | grep mysql | head -1)
    log "  - MySQL ($mysql_container)"
    docker exec "$mysql_container" \
        mysqldump -u root -p"${MYSQL_ROOT_PASSWORD}" --all-databases | \
        gzip > "$BACKUP_ROOT/mysql-${DATE}.sql.gz" 2>> "$LOG_FILE"
fi

# 4. Backup des configurations
log "⚙️  Backup des configurations..."
cp -r /etc/docker "$BACKUP_ROOT/configs/docker-${DATE}" 2>> "$LOG_FILE"

# 5. Export de la liste des conteneurs
log "📋 Export de la configuration des conteneurs..."
docker ps -a --format '{{json .}}' > "$BACKUP_ROOT/configs/containers-${DATE}.json"

# 6. Nettoyer les anciens backups
log "🧹 Nettoyage des backups > $RETENTION_DAYS jours..."
find "$BACKUP_ROOT" -name "*-*.tar.gz" -mtime +$RETENTION_DAYS -delete 2>> "$LOG_FILE"
find "$BACKUP_ROOT" -name "*-*.sql.gz" -mtime +$RETENTION_DAYS -delete 2>> "$LOG_FILE"

# 7. Statistiques
log "📊 Statistiques:"
log "  Total: $(du -sh $BACKUP_ROOT | cut -f1)"
log "  Images: $(ls -1 $BACKUP_ROOT/images/*${DATE}*.tar.gz 2>/dev/null | wc -l)"
log "  Volumes: $(ls -1 $BACKUP_ROOT/volumes/*${DATE}*.tar.gz 2>/dev/null | wc -l)"

log "✅ Backup terminé avec succès"
```

### Crontab pour automatisation

```bash
# Ouvrir crontab
sudo crontab -e

# Backup quotidien à 2h du matin
0 2 * * * /usr/local/bin/docker-full-backup.sh

# Backup hebdomadaire le dimanche à 3h
0 3 * * 0 /usr/local/bin/docker-full-backup.sh

# Backup mensuel le 1er à 4h
0 4 1 * * /usr/local/bin/docker-full-backup.sh

# Backup avec notification par email
0 2 * * * /usr/local/bin/docker-full-backup.sh && echo "Backup OK" | mail -s "Docker Backup" admin@example.com
```

### Systemd timer (alternative à cron)

```ini
# /etc/systemd/system/docker-backup.service
[Unit]
Description=Docker Backup Service
After=docker.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/docker-full-backup.sh
User=root

[Install]
WantedBy=multi-user.target
```

```ini
# /etc/systemd/system/docker-backup.timer
[Unit]
Description=Docker Backup Timer
Requires=docker-backup.service

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# Activer le timer
sudo systemctl enable docker-backup.timer
sudo systemctl start docker-backup.timer

# Vérifier le statut
sudo systemctl status docker-backup.timer
sudo systemctl list-timers | grep docker-backup
```

---

## Restauration

### Plan de restauration

```
1️⃣ Préparer l'environnement
   - Installer Docker
   - Vérifier l'espace disque
   - Créer les réseaux nécessaires

2️⃣ Restaurer les images
   - Charger les images Docker
   - Vérifier les tags

3️⃣ Restaurer les volumes
   - Créer les volumes
   - Extraire les données

4️⃣ Restaurer les configurations
   - docker-compose.yml
   - .env et variables
   - Configs applicatives

5️⃣ Démarrer les services
   - Dans le bon ordre
   - Vérifier les healthchecks

6️⃣ Vérifier l'intégrité
   - Tester les services
   - Vérifier les données
   - Valider les connexions
```

### Script de restauration

```bash
#!/bin/bash
# docker-restore.sh

set -e

BACKUP_DIR="/backup/docker"
RESTORE_DATE=${1:-$(ls -1 $BACKUP_DIR/volumes/*.tar.gz | tail -1 | grep -oP '\d{8}-\d{6}')}

if [ -z "$RESTORE_DATE" ]; then
    echo "❌ Aucun backup trouvé"
    exit 1
fi

echo "📦 Restauration du backup: $RESTORE_DATE"

# 1. Restaurer les images
echo "🖼️  Restauration des images..."
for image_tar in $BACKUP_DIR/images/*-${RESTORE_DATE}.tar.gz; do
    if [ -f "$image_tar" ]; then
        echo "  - $(basename $image_tar)"
        gunzip -c "$image_tar" | docker load
    fi
done

# 2. Restaurer les volumes
echo "💾 Restauration des volumes..."
for volume_tar in $BACKUP_DIR/volumes/*-${RESTORE_DATE}.tar.gz; do
    if [ -f "$volume_tar" ]; then
        volume_name=$(basename "$volume_tar" | sed "s/-${RESTORE_DATE}.tar.gz//")
        echo "  - $volume_name"

        # Créer le volume s'il n'existe pas
        docker volume create "$volume_name" >/dev/null 2>&1 || true

        # Restaurer les données
        docker run --rm \
            -v "$volume_name:/target" \
            -v "$BACKUP_DIR/volumes:/backup" \
            alpine \
            tar xzf "/backup/$(basename $volume_tar)" -C /target
    fi
done

# 3. Restaurer les bases de données
if [ -f "$BACKUP_DIR/postgres-${RESTORE_DATE}.sql.gz" ]; then
    echo "🗄️  Restauration PostgreSQL..."
    # Démarrer PostgreSQL si nécessaire
    docker compose up -d postgres
    sleep 5
    gunzip -c "$BACKUP_DIR/postgres-${RESTORE_DATE}.sql.gz" | \
        docker exec -i postgres psql -U postgres
fi

if [ -f "$BACKUP_DIR/mysql-${RESTORE_DATE}.sql.gz" ]; then
    echo "🗄️  Restauration MySQL..."
    docker compose up -d mysql
    sleep 5
    gunzip -c "$BACKUP_DIR/mysql-${RESTORE_DATE}.sql.gz" | \
        docker exec -i mysql mysql -u root -p"${MYSQL_ROOT_PASSWORD}"
fi

echo "✅ Restauration terminée"
echo ""
echo "📋 Prochaines étapes:"
echo "  1. Vérifier les configurations"
echo "  2. Démarrer les services: docker compose up -d"
echo "  3. Vérifier les logs: docker compose logs -f"
echo "  4. Tester les applications"
```

### Test de restauration

```bash
# Tester régulièrement la restauration !

#!/bin/bash
# test-restore.sh

TEST_DIR="/tmp/docker-restore-test"
BACKUP_DIR="/backup/docker"

echo "🧪 Test de restauration Docker"

# Créer un environnement de test
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Restaurer un volume de test
latest_volume_backup=$(ls -t $BACKUP_DIR/volumes/*.tar.gz | head -1)

if [ -f "$latest_volume_backup" ]; then
    volume_name="test-restore-$(date +%s)"

    echo "📦 Test avec: $(basename $latest_volume_backup)"

    # Créer et restaurer
    docker volume create "$volume_name"
    docker run --rm \
        -v "$volume_name:/target" \
        -v "$BACKUP_DIR/volumes:/backup" \
        alpine \
        tar xzf "/backup/$(basename $latest_volume_backup)" -C /target

    # Vérifier le contenu
    file_count=$(docker run --rm -v "$volume_name:/data" alpine sh -c "find /data -type f | wc -l")

    echo "📊 Résultat: $file_count fichiers restaurés"

    # Nettoyer
    docker volume rm "$volume_name"

    if [ "$file_count" -gt 0 ]; then
        echo "✅ Test réussi"
        exit 0
    else
        echo "❌ Test échoué: aucun fichier trouvé"
        exit 1
    fi
else
    echo "❌ Aucun backup trouvé"
    exit 1
fi
```

---

## Best practices

```bash
# ✅ Backup régulier et automatisé
# Cron ou systemd timer

# ✅ Plusieurs emplacements
# Local + Remote (NAS, Cloud)

# ✅ Test de restauration
# Au moins une fois par mois

# ✅ Rotation des backups
# Conserver: 7 jours quotidiens + 4 semaines + 12 mois

# ✅ Chiffrement des backups sensibles
# GPG ou OpenSSL pour secrets et données

# ✅ Monitoring
# Alertes si backup échoue

# ✅ Documentation
# Procédures de restauration à jour

# ✅ Versionning
# Git pour docker-compose.yml et configs

# ✅ Backup avant changements majeurs
# Migrations, mises à jour, etc.

# ✅ Compression
# Économiser l'espace disque
```

---

## Commandes de référence rapide

```bash
# Images
docker save image > image.tar                # Sauvegarder
docker load < image.tar                      # Restaurer

# Conteneurs
docker export container > container.tar      # Exporter
docker import container.tar image:tag        # Importer
docker commit container image:tag            # Commit en image

# Volumes
docker run --rm -v vol:/src:ro -v $(pwd):/backup alpine tar czf /backup/vol.tar.gz -C /src .
docker run --rm -v vol:/target -v $(pwd):/backup alpine tar xzf /backup/vol.tar.gz -C /target

# Bases de données
docker exec postgres pg_dump ... > backup.sql
docker exec -i postgres psql < backup.sql
```

---

[← Debug et monitoring](./infos-docker-10-debug-monitoring.md) | [Index](./infos-docker-00-index.md) | [Différences Linux/Windows →](./infos-docker-12-differences-linux-windows.md)
