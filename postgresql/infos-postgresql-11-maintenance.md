# 🔧 Maintenance

[← Monitoring](./infos-postgresql-10-monitoring.md) | [Index](./infos-postgresql-00-index.md) | [Troubleshooting →](./infos-postgresql-12-troubleshooting.md)

## VACUUM

```sql
-- VACUUM simple (nettoie les lignes mortes)
VACUUM users;

-- VACUUM avec VERBOSE (affiche les détails)
VACUUM VERBOSE users;

-- VACUUM ANALYZE (nettoie + met à jour les stats)
VACUUM ANALYZE users;

-- VACUUM toute la database
VACUUM;

-- VACUUM FULL (réorganise complètement, bloque la table)
VACUUM FULL users;
-- ⚠️ Nécessite un lock exclusif, à faire en maintenance

-- VACUUM avec options
VACUUM (VERBOSE, ANALYZE, DISABLE_PAGE_SKIPPING) users;

-- Voir les tables qui ont besoin de VACUUM
SELECT
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_ratio,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

## Autovacuum

```conf
# postgresql.conf

# Activer autovacuum (par défaut: on)
autovacuum = on
autovacuum_max_workers = 3
autovacuum_naptime = 1min

# Seuils de déclenchement
autovacuum_vacuum_threshold = 50
autovacuum_vacuum_scale_factor = 0.2
# Déclenché quand: dead_tuples > threshold + (scale_factor * total_tuples)
# Exemple: table de 10000 lignes
# Seuil = 50 + (0.2 * 10000) = 2050 dead tuples

autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.1

# Coût et délai
autovacuum_vacuum_cost_delay = 2ms
autovacuum_vacuum_cost_limit = 200

# Logs
log_autovacuum_min_duration = 0     # Log tous les autovacuum
```

```sql
-- Voir l'activité autovacuum
SELECT
    schemaname,
    tablename,
    last_autovacuum,
    last_autoanalyze,
    n_dead_tup
FROM pg_stat_user_tables
ORDER BY last_autovacuum DESC NULLS LAST;

-- Désactiver autovacuum sur une table (déconseillé)
ALTER TABLE logs SET (autovacuum_enabled = false);

-- Réactiver
ALTER TABLE logs SET (autovacuum_enabled = true);

-- Personnaliser pour une table
ALTER TABLE large_table SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_analyze_scale_factor = 0.02
);
```

## ANALYZE

```sql
-- Mettre à jour les statistiques d'une table
ANALYZE users;

-- Colonnes spécifiques
ANALYZE users (email, country);

-- Toute la database
ANALYZE;

-- Avec VERBOSE
ANALYZE VERBOSE users;

-- Voir la dernière analyse
SELECT
    schemaname,
    tablename,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY last_analyze DESC NULLS LAST;

-- Statistiques d'une colonne
SELECT * FROM pg_stats
WHERE tablename = 'users' AND attname = 'email';
```

## REINDEX

```sql
-- Reconstruire un index
REINDEX INDEX idx_users_email;

-- Reconstruire tous les index d'une table
REINDEX TABLE users;

-- Reconstruire tous les index d'une database
REINDEX DATABASE mydb;

-- Avec CONCURRENTLY (ne bloque pas)
REINDEX INDEX CONCURRENTLY idx_users_email;

-- Reconstruire les index système
REINDEX SYSTEM mydb;

-- Voir les index à reconstruire (bloat)
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;
```

## Nettoyage des logs

```sql
-- Voir les paramètres de logging
SHOW log_directory;
SHOW log_filename;
SHOW log_rotation_age;
SHOW log_rotation_size;

-- Configurer la rotation
-- Dans postgresql.conf:
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d          # Rotation quotidienne
log_rotation_size = 100MB      # Rotation si > 100MB
log_truncate_on_rotation = off

-- Supprimer les vieux logs
-- Dans postgresql.conf:
log_file_mode = 0600
```

```bash
# Script de nettoyage des logs
#!/bin/bash
# cleanup_postgres_logs.sh

LOG_DIR="/var/log/postgresql"
RETENTION_DAYS=30

# Supprimer les logs de plus de 30 jours
find $LOG_DIR -name "*.log" -mtime +$RETENTION_DAYS -delete

# Compresser les logs de plus de 7 jours
find $LOG_DIR -name "*.log" -mtime +7 -exec gzip {} \;

echo "✅ Nettoyage des logs terminé"
```

```cron
# Automatiser avec cron
0 2 * * * /path/to/cleanup_postgres_logs.sh
```

## Maintenance des WAL

```sql
-- Voir les paramètres WAL
SHOW wal_level;
SHOW max_wal_size;
SHOW min_wal_size;
SHOW wal_keep_size;

-- Voir la taille des WAL
SELECT
    pg_size_pretty(
        pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0')
    ) as wal_size;

-- Forcer un checkpoint (écrire les WAL sur disque)
CHECKPOINT;

-- Voir les slots de réplication (gardent les WAL)
SELECT
    slot_name,
    slot_type,
    active,
    pg_size_pretty(
        pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)
    ) as retained_wal
FROM pg_replication_slots;

-- Supprimer un slot inutilisé
SELECT pg_drop_replication_slot('old_slot');
```

```bash
# Nettoyer les WAL archives (si archive_mode = on)
#!/bin/bash
# cleanup_wal_archive.sh

ARCHIVE_DIR="/backup/wal_archive"
RETENTION_DAYS=7

# Supprimer les WAL de plus de 7 jours
find $ARCHIVE_DIR -name "*.wal" -mtime +$RETENTION_DAYS -delete

echo "✅ Nettoyage des WAL terminé"
```

## Bloat (tables et index gonflés)

```sql
-- Détecter le bloat des tables
CREATE EXTENSION IF NOT EXISTS pgstattuple;

-- Analyser une table
SELECT * FROM pgstattuple('users');

-- Bloat ratio
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as size,
    ROUND((
        100 * (pg_relation_size(schemaname||'.'||tablename)::NUMERIC -
               pgstattuple(schemaname||'.'||tablename).tuple_len) /
        NULLIF(pg_relation_size(schemaname||'.'||tablename), 0)
    ), 2) as bloat_ratio
FROM pg_tables
WHERE schemaname = 'public'
    AND pg_relation_size(schemaname||'.'||tablename) > 1048576  -- > 1MB
ORDER BY bloat_ratio DESC;

-- Réduire le bloat
-- Option 1: VACUUM FULL (bloque la table)
VACUUM FULL users;

-- Option 2: pg_repack (sans bloquer, nécessite extension)
CREATE EXTENSION pg_repack;
-- Utiliser en ligne de commande:
-- pg_repack -d mydb -t users
```

## pg_repack (réorganiser sans bloquer)

```bash
# Installer pg_repack
sudo apt install postgresql-15-repack

# Installer l'extension
psql -c "CREATE EXTENSION pg_repack;"

# Réorganiser une table
pg_repack -d mydb -t users

# Réorganiser toutes les tables
pg_repack -d mydb

# Dry-run (test)
pg_repack -d mydb -t users --dry-run

# Avec plusieurs workers (plus rapide)
pg_repack -d mydb -j 4

# Exclure des tables
pg_repack -d mydb -x logs
```

## Maintenance régulière

```sql
-- Script de maintenance hebdomadaire
DO $$
DECLARE
    r RECORD;
BEGIN
    -- 1. VACUUM ANALYZE toutes les tables
    FOR r IN SELECT schemaname, tablename FROM pg_tables WHERE schemaname = 'public'
    LOOP
        EXECUTE 'VACUUM ANALYZE ' || quote_ident(r.schemaname) || '.' || quote_ident(r.tablename);
        RAISE NOTICE 'VACUUM ANALYZE %', r.tablename;
    END LOOP;

    -- 2. REINDEX tables avec beaucoup de dead tuples
    FOR r IN
        SELECT schemaname, tablename
        FROM pg_stat_user_tables
        WHERE n_dead_tup > 10000
    LOOP
        EXECUTE 'REINDEX TABLE ' || quote_ident(r.schemaname) || '.' || quote_ident(r.tablename);
        RAISE NOTICE 'REINDEX %', r.tablename;
    END LOOP;

    RAISE NOTICE 'Maintenance terminée';
END $$;
```

```bash
#!/bin/bash
# maintenance_hebdomadaire.sh

DB_NAME="mydb"
LOG_FILE="/var/log/postgres_maintenance.log"

echo "=== Maintenance $(date) ===" >> $LOG_FILE

# 1. VACUUM ANALYZE
echo "VACUUM ANALYZE..." >> $LOG_FILE
psql $DB_NAME -c "VACUUM ANALYZE;" >> $LOG_FILE 2>&1

# 2. Nettoyer les logs > 30 jours
echo "Nettoyage logs..." >> $LOG_FILE
find /var/log/postgresql -name "*.log" -mtime +30 -delete

# 3. Nettoyer les WAL archives > 7 jours
echo "Nettoyage WAL..." >> $LOG_FILE
find /backup/wal_archive -name "*.wal" -mtime +7 -delete

# 4. Vérifier les tables avec bloat
echo "Vérification bloat..." >> $LOG_FILE
psql $DB_NAME -c "
    SELECT tablename, n_dead_tup
    FROM pg_stat_user_tables
    WHERE n_dead_tup > 10000
    ORDER BY n_dead_tup DESC;
" >> $LOG_FILE

# 5. Statistiques
echo "Statistiques..." >> $LOG_FILE
psql $DB_NAME -c "
    SELECT
        pg_size_pretty(pg_database_size('$DB_NAME')) as db_size,
        (SELECT COUNT(*) FROM pg_stat_activity) as connections;
" >> $LOG_FILE

echo "✅ Maintenance terminée" >> $LOG_FILE
echo "" >> $LOG_FILE
```

```cron
# Exécuter tous les dimanches à 3h
0 3 * * 0 /path/to/maintenance_hebdomadaire.sh
```

## Maintenance quotidienne

```bash
#!/bin/bash
# maintenance_quotidienne.sh

DB_NAME="mydb"

# 1. Vérifier les connexions
CONNECTIONS=$(psql -t -c "SELECT COUNT(*) FROM pg_stat_activity;")
echo "🔌 Connexions actives: $CONNECTIONS"

# 2. Vérifier les requêtes longues
LONG_QUERIES=$(psql -t -c "
    SELECT COUNT(*)
    FROM pg_stat_activity
    WHERE state != 'idle'
        AND NOW() - query_start > interval '1 hour';
")
if [ $LONG_QUERIES -gt 0 ]; then
    echo "⚠️  Requêtes longues (>1h): $LONG_QUERIES"
fi

# 3. Vérifier les locks
LOCKS=$(psql -t -c "
    SELECT COUNT(*) FROM pg_locks WHERE NOT granted;
")
if [ $LOCKS -gt 0 ]; then
    echo "⚠️  Locks en attente: $LOCKS"
fi

# 4. Vérifier le cache hit ratio
CACHE_RATIO=$(psql -t -c "
    SELECT ROUND(SUM(heap_blks_hit) * 100.0 / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2)
    FROM pg_statio_user_tables;
")
echo "💾 Cache hit ratio: ${CACHE_RATIO}%"

# 5. Taille de la database
DB_SIZE=$(psql -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));")
echo "📊 Taille DB: $DB_SIZE"

# 6. ANALYZE sur tables modifiées
psql -c "
    SELECT schemaname || '.' || tablename as table
    FROM pg_stat_user_tables
    WHERE last_autoanalyze < NOW() - interval '1 day'
        OR last_autoanalyze IS NULL;
" | while read table; do
    if [ -n "$table" ]; then
        echo "📊 ANALYZE $table"
        psql -c "ANALYZE $table;"
    fi
done
```

```cron
# Exécuter tous les jours à 2h
0 2 * * * /path/to/maintenance_quotidienne.sh
```

## pg_cron (planifier des tâches)

```sql
-- Installer extension
CREATE EXTENSION pg_cron;

-- Planifier un VACUUM quotidien à 2h
SELECT cron.schedule('vacuum-daily', '0 2 * * *', 'VACUUM ANALYZE;');

-- Planifier nettoyage des vieilles données
SELECT cron.schedule('cleanup-logs', '0 3 * * *',
    $$DELETE FROM logs WHERE created_at < NOW() - interval '30 days'$$);

-- Planifier refresh d'une materialized view
SELECT cron.schedule('refresh-stats', '0 * * * *',
    $$REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats$$);

-- Lister les tâches
SELECT * FROM cron.job;

-- Supprimer une tâche
SELECT cron.unschedule(1);  -- job_id

-- Voir l'historique
SELECT * FROM cron.job_run_details ORDER BY start_time DESC LIMIT 20;
```

## Archivage des vieilles données

```sql
-- Créer une table d'archive
CREATE TABLE orders_archive (LIKE orders INCLUDING ALL);

-- Archiver les données de plus d'un an
WITH archived AS (
    DELETE FROM orders
    WHERE created_at < NOW() - interval '1 year'
    RETURNING *
)
INSERT INTO orders_archive SELECT * FROM archived;

-- Automatiser avec pg_cron
SELECT cron.schedule('archive-orders', '0 0 1 * *',  -- 1er de chaque mois
    $$
    WITH archived AS (
        DELETE FROM orders
        WHERE created_at < NOW() - interval '1 year'
        RETURNING *
    )
    INSERT INTO orders_archive SELECT * FROM archived;
    $$
);
```

## Checklist maintenance

```
📋 Maintenance quotidienne:
  ☐ Vérifier les connexions actives
  ☐ Vérifier les requêtes longues
  ☐ Vérifier les locks
  ☐ Vérifier le cache hit ratio
  ☐ Vérifier la taille de la database
  ☐ Vérifier les logs d'erreurs

📋 Maintenance hebdomadaire:
  ☐ VACUUM ANALYZE toutes les tables
  ☐ Vérifier le bloat
  ☐ REINDEX si nécessaire
  ☐ Nettoyer les logs > 30 jours
  ☐ Vérifier les backups
  ☐ Tester une restauration

📋 Maintenance mensuelle:
  ☐ Analyser pg_stat_statements
  ☐ Archiver les vieilles données
  ☐ Vérifier la réplication
  ☐ Audit des permissions
  ☐ Vérifier les mises à jour PostgreSQL
  ☐ Réviser les index inutilisés
```

[← Monitoring](./infos-postgresql-10-monitoring.md) | [Index](./infos-postgresql-00-index.md) | [Troubleshooting →](./infos-postgresql-12-troubleshooting.md)
