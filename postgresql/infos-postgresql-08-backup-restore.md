# 💾 Backup et Restore

[← Performances avancées](./infos-postgresql-07-performances-avancees.md) | [Index](./infos-postgresql-00-index.md) | [Réplication →](./infos-postgresql-09-replication.md)

## pg_dump - Backup logique

```bash
# Backup d'une database (format SQL)
pg_dump mydb > mydb_backup.sql
pg_dump -U postgres mydb > mydb_backup.sql

# Format custom (compressé, plus rapide pour restore)
pg_dump -Fc mydb > mydb_backup.dump

# Format directory (parallélisé)
pg_dump -Fd mydb -f mydb_backup_dir -j 4

# Format tar
pg_dump -Ft mydb > mydb_backup.tar

# Avec compression gzip
pg_dump mydb | gzip > mydb_backup.sql.gz

# Backup d'une table spécifique
pg_dump -t users mydb > users_backup.sql
pg_dump -t 'schema.table' mydb > table_backup.sql

# Backup de plusieurs tables
pg_dump -t users -t orders mydb > tables_backup.sql

# Exclure des tables
pg_dump --exclude-table=logs mydb > mydb_backup.sql

# Schema uniquement (sans données)
pg_dump --schema-only mydb > schema.sql

# Données uniquement (sans schema)
pg_dump --data-only mydb > data.sql

# Avec options avancées
pg_dump \
    -h localhost \
    -U postgres \
    -Fc \
    --verbose \
    --no-owner \
    --no-acl \
    mydb > mydb_backup.dump
```

## pg_dumpall - Backup complet du serveur

```bash
# Backup de toutes les databases
pg_dumpall > all_databases.sql

# Backup des rôles/users seulement
pg_dumpall --roles-only > roles.sql

# Backup des tablespaces seulement
pg_dumpall --tablespaces-only > tablespaces.sql

# Backup globals (roles + tablespaces)
pg_dumpall --globals-only > globals.sql

# Backup complet (recommandé)
pg_dumpall --clean --if-exists > full_backup.sql
```

## Restore

```bash
# Restore format SQL
psql mydb < mydb_backup.sql

# Restore format custom
pg_restore -d mydb mydb_backup.dump

# Restore avec parallélisme
pg_restore -d mydb -j 4 mydb_backup.dump

# Restore format directory
pg_restore -d mydb mydb_backup_dir -j 4

# Créer la DB avant restore
createdb mydb
pg_restore -d mydb mydb_backup.dump

# Ou avec --create (crée la DB)
pg_restore --create -d postgres mydb_backup.dump

# Restore avec options
pg_restore \
    -h localhost \
    -U postgres \
    -d mydb \
    --verbose \
    --clean \
    --if-exists \
    --no-owner \
    --no-acl \
    mydb_backup.dump

# Restore une table spécifique
pg_restore -d mydb -t users mydb_backup.dump

# Restore schema seulement
pg_restore -d mydb --schema-only mydb_backup.dump

# Restore données seulement
pg_restore -d mydb --data-only mydb_backup.dump
```

## Backup automatisé

```bash
#!/bin/bash
# backup_postgres.sh

# Configuration
DB_NAME="mydb"
DB_USER="postgres"
BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.dump"
RETENTION_DAYS=7

# Créer le répertoire si nécessaire
mkdir -p $BACKUP_DIR

# Backup
pg_dump -U $DB_USER -Fc $DB_NAME > $BACKUP_FILE

# Vérifier le succès
if [ $? -eq 0 ]; then
    echo "✅ Backup réussi: $BACKUP_FILE"

    # Compression supplémentaire (optionnel)
    # gzip $BACKUP_FILE

    # Supprimer les anciens backups
    find $BACKUP_DIR -name "${DB_NAME}_*.dump" -mtime +$RETENTION_DAYS -delete

    # Upload vers S3 (optionnel)
    # aws s3 cp $BACKUP_FILE s3://my-bucket/backups/
else
    echo "❌ Échec du backup"
    exit 1
fi
```

```bash
# Rendre exécutable
chmod +x backup_postgres.sh

# Tester
./backup_postgres.sh

# Automatiser avec cron
crontab -e
```

```cron
# Backup tous les jours à 2h du matin
0 2 * * * /path/to/backup_postgres.sh >> /var/log/postgres_backup.log 2>&1

# Backup toutes les 6 heures
0 */6 * * * /path/to/backup_postgres.sh

# Backup hebdomadaire (dimanche à 3h)
0 3 * * 0 /path/to/backup_postgres_weekly.sh
```

## Backup physique avec pg_basebackup

```bash
# Backup physique complet
pg_basebackup -h localhost -U postgres -D /backup/base -Ft -z -P

# Options:
# -D : répertoire destination
# -Ft : format tar
# -z : compression gzip
# -P : afficher la progression
# -X stream : inclure les WAL

# Backup physique avec WAL streaming
pg_basebackup \
    -h localhost \
    -U replicator \
    -D /backup/base \
    -Ft \
    -z \
    -P \
    -X stream \
    -c fast

# Restore d'un backup physique
# 1. Arrêter PostgreSQL
sudo systemctl stop postgresql

# 2. Vider le data directory
rm -rf /var/lib/postgresql/15/main/*

# 3. Extraire le backup
cd /var/lib/postgresql/15/main
tar xzf /backup/base/base.tar.gz
tar xzf /backup/base/pg_wal.tar.gz -C pg_wal

# 4. Permissions
chown -R postgres:postgres /var/lib/postgresql/15/main

# 5. Redémarrer
sudo systemctl start postgresql
```

## Point-in-Time Recovery (PITR)

```conf
# 1. Configurer postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/wal_archive/%f'
max_wal_senders = 3
```

```bash
# 2. Redémarrer PostgreSQL
sudo systemctl restart postgresql

# 3. Créer un base backup
pg_basebackup -D /backup/pitr_base -Ft -z -P -X stream

# 4. Les WAL sont archivés automatiquement dans /backup/wal_archive/

# 5. En cas de besoin de restauration à un point dans le temps:

# Arrêter PostgreSQL
sudo systemctl stop postgresql

# Vider le data directory
rm -rf /var/lib/postgresql/15/main/*

# Restaurer le base backup
cd /var/lib/postgresql/15/main
tar xzf /backup/pitr_base/base.tar.gz

# Créer recovery.signal
touch recovery.signal

# Configurer postgresql.conf ou postgresql.auto.conf
restore_command = 'cp /backup/wal_archive/%f %p'
recovery_target_time = '2024-12-01 14:30:00'
# Ou recovery_target_xid = '12345'
# Ou recovery_target_name = 'before_disaster'

# Permissions
chown -R postgres:postgres /var/lib/postgresql/15/main

# Démarrer
sudo systemctl start postgresql

# PostgreSQL va rejouer les WAL jusqu'au point demandé
# Surveiller les logs
tail -f /var/log/postgresql/postgresql-15-main.log
```

## Backup avec Docker

```bash
# Backup d'un container PostgreSQL
docker exec postgres-container pg_dump -U postgres mydb > backup.sql

# Backup avec timestamp
docker exec postgres-container pg_dump -U postgres mydb > mydb_$(date +%Y%m%d).sql

# Backup format custom
docker exec postgres-container pg_dump -U postgres -Fc mydb > backup.dump

# Restore
docker exec -i postgres-container psql -U postgres mydb < backup.sql

# Ou avec pg_restore
cat backup.dump | docker exec -i postgres-container pg_restore -U postgres -d mydb

# Script automatisé Docker
#!/bin/bash
CONTAINER="postgres-container"
DB_NAME="mydb"
BACKUP_DIR="/backup/docker"
DATE=$(date +%Y%m%d_%H%M%S)

docker exec $CONTAINER pg_dump -U postgres -Fc $DB_NAME > \
    $BACKUP_DIR/${DB_NAME}_${DATE}.dump
```

## Backup vers cloud (AWS S3)

```bash
#!/bin/bash
# backup_to_s3.sh

DB_NAME="mydb"
BACKUP_FILE="/tmp/${DB_NAME}_$(date +%Y%m%d_%H%M%S).dump"
S3_BUCKET="s3://my-backups/postgresql"

# Backup
pg_dump -Fc $DB_NAME > $BACKUP_FILE

# Upload vers S3
aws s3 cp $BACKUP_FILE $S3_BUCKET/

# Supprimer le fichier local
rm $BACKUP_FILE

# Supprimer les backups de plus de 30 jours sur S3
aws s3 ls $S3_BUCKET/ | while read -r line; do
    createDate=$(echo $line | awk {'print $1" "$2'})
    createDate=$(date -d "$createDate" +%s)
    olderThan=$(date -d "30 days ago" +%s)
    if [[ $createDate -lt $olderThan ]]; then
        fileName=$(echo $line | awk {'print $4'})
        aws s3 rm $S3_BUCKET/$fileName
    fi
done
```

## Backup incrémentiels avec pgBackRest

```bash
# Installer pgBackRest
sudo apt install pgbackrest

# Configuration /etc/pgbackrest.conf
```

```ini
[global]
repo1-path=/backup/pgbackrest
repo1-retention-full=2
repo1-retention-diff=4

[mydb]
pg1-path=/var/lib/postgresql/15/main
```

```bash
# Créer le stanza
pgbackrest --stanza=mydb stanza-create

# Backup complet
pgbackrest --stanza=mydb backup --type=full

# Backup différentiel
pgbackrest --stanza=mydb backup --type=diff

# Backup incrémentiel
pgbackrest --stanza=mydb backup --type=incr

# Lister les backups
pgbackrest --stanza=mydb info

# Restore
pgbackrest --stanza=mydb restore

# Restore à un point dans le temps
pgbackrest --stanza=mydb \
    --type=time \
    --target="2024-12-01 14:30:00" \
    restore
```

## Stratégies de backup

```
📅 Stratégie recommandée:

1. Backup complet hebdomadaire (dimanche)
2. Backup incrémentiel quotidien
3. Archivage des WAL continu (PITR)
4. Rétention: 7 jours local + 30 jours cloud

Exemple:
- Dimanche 3h: Full backup + upload S3
- Lundi-Samedi 2h: Incrémental backup
- Continu: Archive WAL
- Mensuel: Full backup conservé 1 an
```

```bash
#!/bin/bash
# backup_strategy.sh

DAY=$(date +%u)  # 1-7 (lundi-dimanche)
BACKUP_DIR="/backup/postgresql"
DB_NAME="mydb"

if [ $DAY -eq 7 ]; then
    # Dimanche: Full backup
    echo "Full backup"
    pg_dump -Fc $DB_NAME > $BACKUP_DIR/full_$(date +%Y%m%d).dump

    # Upload vers S3
    aws s3 cp $BACKUP_DIR/full_$(date +%Y%m%d).dump s3://my-backups/weekly/
else
    # Lundi-Samedi: Backup quotidien
    echo "Daily backup"
    pg_dump -Fc $DB_NAME > $BACKUP_DIR/daily_$(date +%Y%m%d).dump
fi

# Nettoyer les anciens backups locaux (> 7 jours)
find $BACKUP_DIR -name "*.dump" -mtime +7 -delete
```

## Vérification des backups

```bash
# Tester un backup SQL
psql -d testdb -f backup.sql --single-transaction --set ON_ERROR_STOP=on

# Tester un backup dump
pg_restore --list backup.dump

# Restaurer dans une DB de test
createdb test_restore
pg_restore -d test_restore backup.dump

# Vérifier les données
psql test_restore -c "SELECT COUNT(*) FROM users;"

# Nettoyer
dropdb test_restore
```

```bash
#!/bin/bash
# verify_backup.sh

BACKUP_FILE=$1
TEST_DB="test_restore_$(date +%s)"

echo "🔍 Vérification du backup: $BACKUP_FILE"

# Créer DB test
createdb $TEST_DB

# Restore
pg_restore -d $TEST_DB $BACKUP_FILE 2>&1 | tee restore.log

if [ $? -eq 0 ]; then
    echo "✅ Restore réussi"

    # Vérifier quelques tables
    psql $TEST_DB -c "\dt" | tee tables.log

    # Nettoyer
    dropdb $TEST_DB
    echo "✅ Backup valide"
else
    echo "❌ Échec du restore"
    dropdb $TEST_DB
    exit 1
fi
```

## Export/Import données avec COPY

```sql
-- Export vers CSV
COPY users TO '/tmp/users.csv' WITH CSV HEADER;
COPY (SELECT * FROM users WHERE country = 'FR') TO '/tmp/users_fr.csv' WITH CSV;

-- Import depuis CSV
COPY users FROM '/tmp/users.csv' WITH CSV HEADER;

-- Options avancées
COPY users TO '/tmp/users.csv' WITH (
    FORMAT CSV,
    HEADER true,
    DELIMITER ',',
    QUOTE '"',
    ENCODING 'UTF8'
);
```

```bash
# Export via psql
psql -c "COPY users TO STDOUT WITH CSV HEADER" > users.csv

# Import via psql
psql -c "COPY users FROM STDIN WITH CSV HEADER" < users.csv
```

## Troubleshooting

```bash
# Backup échoue: permission denied
# Solution: utiliser un répertoire accessible
pg_dump mydb > /tmp/backup.sql

# Restore échoue: database exists
# Solution: drop ou --clean
dropdb mydb
createdb mydb
pg_restore -d mydb backup.dump

# Ou:
pg_restore --clean --if-exists -d mydb backup.dump

# Backup trop gros
# Solution: compression + exclude tables
pg_dump -Fc --exclude-table=logs mydb | gzip > backup.dump.gz

# Restore lent
# Solution: parallélisme + désactiver triggers
pg_restore -d mydb -j 4 backup.dump

# Espace disque insuffisant
# Solution: backup vers NFS/cloud directement
pg_dump mydb | aws s3 cp - s3://bucket/backup.sql

# Vérifier la taille avant backup
psql -c "SELECT pg_size_pretty(pg_database_size('mydb'));"
```

[← Performances avancées](./infos-postgresql-07-performances-avancees.md) | [Index](./infos-postgresql-00-index.md) | [Réplication →](./infos-postgresql-09-replication.md)
