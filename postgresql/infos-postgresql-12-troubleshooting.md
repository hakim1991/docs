# 🔧 Troubleshooting

[← Maintenance](./infos-postgresql-11-maintenance.md) | [Index](./infos-postgresql-00-index.md)

## Problèmes de connexion

```bash
# Erreur: "connection refused"
# Solution: Vérifier que PostgreSQL est démarré
sudo systemctl status postgresql
sudo systemctl start postgresql

# Vérifier le port
sudo netstat -tulpn | grep 5432
sudo ss -tulpn | grep 5432

# Erreur: "could not connect to server: Connection timed out"
# Solution: Vérifier le firewall
sudo ufw status
sudo ufw allow 5432/tcp

# CentOS/RHEL
sudo firewall-cmd --list-all
sudo firewall-cmd --permanent --add-port=5432/tcp
sudo firewall-cmd --reload

# Erreur: "FATAL: password authentication failed"
# Solution: Vérifier pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf
# Changer 'peer' en 'md5' pour les connexions locales

# Réinitialiser le mot de passe
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'newpassword';

# Erreur: "FATAL: role does not exist"
# Solution: Créer l'utilisateur
sudo -u postgres createuser myuser
# Ou:
sudo -u postgres psql -c "CREATE USER myuser WITH PASSWORD 'secret';"

# Erreur: "FATAL: database does not exist"
# Solution: Créer la database
sudo -u postgres createdb mydb
```

## Erreurs "too many connections"

```sql
-- Voir le nombre de connexions max
SHOW max_connections;

-- Voir les connexions actives
SELECT COUNT(*) FROM pg_stat_activity;

-- Voir les connexions par database
SELECT
    datname,
    COUNT(*) as connections
FROM pg_stat_activity
GROUP BY datname;

-- Tuer les connexions idle
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
    AND NOW() - state_change > interval '10 minutes';

-- Solutions:
-- 1. Augmenter max_connections (postgresql.conf)
max_connections = 200

-- 2. Utiliser un connection pooler (PgBouncer)
-- 3. Fermer les connexions inutilisées dans l'application
-- 4. Configurer des timeouts
idle_in_transaction_session_timeout = 60000  -- 60s
```

## Requêtes lentes

```sql
-- Identifier les requêtes lentes
SELECT
    pid,
    NOW() - query_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE state != 'idle'
    AND NOW() - query_start > interval '5 seconds'
ORDER BY duration DESC;

-- Tuer une requête lente
SELECT pg_cancel_backend(pid);       -- Cancel graceful
SELECT pg_terminate_backend(pid);    -- Kill forcé

-- Activer le logging des requêtes lentes
-- Dans postgresql.conf:
log_min_duration_statement = 1000    -- Log requêtes > 1s

-- Analyser une requête lente
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;

-- Solutions:
-- 1. Créer des index
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- 2. Optimiser la requête
-- 3. Augmenter work_mem si beaucoup de sorts
SET work_mem = '64MB';

-- 4. Mettre à jour les statistiques
ANALYZE orders;
```

## Problèmes de locks

```sql
-- Voir les locks actifs
SELECT
    l.locktype,
    l.database,
    l.relation::regclass as table,
    l.mode,
    l.granted,
    a.pid,
    a.usename,
    a.query,
    a.state,
    NOW() - a.query_start as duration
FROM pg_locks l
LEFT JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted
ORDER BY a.query_start;

-- Voir qui bloque qui
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- Tuer la requête qui bloque
SELECT pg_terminate_backend(blocking_pid);

-- Solutions:
-- 1. Optimiser les transactions (les garder courtes)
-- 2. Configurer des timeouts
lock_timeout = 5000                  -- 5s
statement_timeout = 30000            -- 30s
idle_in_transaction_session_timeout = 60000
```

## Erreurs de disque plein

```bash
# Vérifier l'espace disque
df -h

# Voir la taille de PostgreSQL
sudo du -sh /var/lib/postgresql/

# Voir la taille par database
psql -c "
    SELECT
        datname,
        pg_size_pretty(pg_database_size(datname)) as size
    FROM pg_database
    ORDER BY pg_database_size(datname) DESC;
"

# Solutions:
# 1. Supprimer les vieux logs
find /var/log/postgresql -name "*.log" -mtime +30 -delete

# 2. Nettoyer les WAL
# Vérifier les slots de réplication
psql -c "SELECT * FROM pg_replication_slots;"
# Supprimer les slots inutilisés
psql -c "SELECT pg_drop_replication_slot('slot_name');"

# 3. VACUUM FULL (libère l'espace disque)
psql mydb -c "VACUUM FULL;"

# 4. Archiver/supprimer les vieilles données
psql mydb -c "DELETE FROM logs WHERE created_at < NOW() - interval '90 days';"

# 5. Déplacer le tablespace
# Créer nouveau tablespace sur autre disque
psql -c "CREATE TABLESPACE new_space LOCATION '/mnt/postgres';"
# Déplacer une table
psql -c "ALTER TABLE large_table SET TABLESPACE new_space;"
```

## Problèmes de performance

```sql
-- Cache hit ratio faible (< 99%)
SELECT
    SUM(heap_blks_hit) as heap_hit,
    SUM(heap_blks_read) as heap_read,
    ROUND(SUM(heap_blks_hit) * 100.0 / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2) as cache_hit_ratio
FROM pg_statio_user_tables;

-- Solution: Augmenter shared_buffers
-- Dans postgresql.conf:
shared_buffers = 2GB                 -- 25% de la RAM

-- Index non utilisés
SELECT
    schemaname,
    tablename,
    indexrelname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND indexrelid NOT IN (SELECT indexrelid FROM pg_index WHERE indisunique)
ORDER BY pg_relation_size(indexrelid) DESC;

-- Solution: Supprimer les index inutilisés
DROP INDEX idx_unused;

-- Tables avec beaucoup de dead tuples
SELECT
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC;

-- Solution: VACUUM
VACUUM ANALYZE tablename;

-- Ou configurer autovacuum plus agressif
ALTER TABLE tablename SET (
    autovacuum_vacuum_scale_factor = 0.05,
    autovacuum_analyze_scale_factor = 0.02
);
```

## PostgreSQL ne démarre pas

```bash
# Vérifier les logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
sudo journalctl -u postgresql -n 50

# Erreurs communes:

# 1. "Invalid command error" ou syntaxe erreur dans postgresql.conf
# Solution: Vérifier la configuration
sudo -u postgres postgres -C config_file
sudo -u postgres postgres --check

# 2. "data directory has wrong ownership"
# Solution: Changer le propriétaire
sudo chown -R postgres:postgres /var/lib/postgresql/15/main

# 3. "port 5432 already in use"
# Solution: Tuer le processus
sudo lsof -i :5432
sudo kill -9 PID

# 4. "could not create shared memory segment"
# Solution: Augmenter kernel.shmmax
sudo sysctl -w kernel.shmmax=17179869184
sudo sysctl -w kernel.shmall=4194304

# 5. Corruption de données
# Solution: Essayer pg_resetwal (DANGEREUX, dernier recours)
sudo -u postgres pg_resetwal /var/lib/postgresql/15/main
```

## Erreurs de réplication

```sql
-- Sur le PRIMARY
-- Vérifier les replicas
SELECT
    client_addr,
    state,
    sync_state,
    replay_lag
FROM pg_stat_replication;

-- Aucun replica connecté
-- Vérifier pg_hba.conf permet la réplication
-- host    replication     replicator      192.168.1.0/24          md5

-- Sur le REPLICA
-- Vérifier si en recovery mode
SELECT pg_is_in_recovery();  -- Devrait être true

-- Voir le lag
SELECT
    NOW() - pg_last_xact_replay_timestamp() AS replication_lag;

-- Replica trop en retard
-- Vérifier les WAL sur le primary
SELECT
    slot_name,
    pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) as retained_wal
FROM pg_replication_slots;

-- Solution: Reconstruire le replica
-- 1. Sur replica:
sudo systemctl stop postgresql
sudo rm -rf /var/lib/postgresql/15/main/*
sudo -u postgres pg_basebackup -h primary.local -U replicator \
    -D /var/lib/postgresql/15/main -P -X stream
sudo -u postgres touch /var/lib/postgresql/15/main/standby.signal
sudo systemctl start postgresql
```

## Corruption de base de données

```sql
-- Vérifier l'intégrité d'une table
-- Installer extension
CREATE EXTENSION IF NOT EXISTS amcheck;

-- Vérifier un index
SELECT bt_index_check('idx_users_email');

-- Vérifier tous les index d'une table
SELECT bt_index_check(c.oid), c.relname
FROM pg_index i
JOIN pg_class c ON i.indexrelid = c.oid
WHERE i.indrelid = 'users'::regclass;

-- Si corruption détectée:
-- 1. REINDEX
REINDEX INDEX idx_users_email;
REINDEX TABLE users;

-- 2. Si ça ne marche pas, dump/restore
pg_dump mydb > backup.sql
dropdb mydb
createdb mydb
psql mydb < backup.sql
```

## Problèmes de backup/restore

```bash
# Erreur: "permission denied"
# Solution: Utiliser un répertoire accessible
pg_dump mydb > /tmp/backup.sql

# Erreur: "out of memory"
# Solution: Utiliser format custom avec compression
pg_dump -Fc mydb > backup.dump

# Erreur lors du restore: "role does not exist"
# Solution: Ne pas restaurer ownership
pg_restore --no-owner --no-acl -d mydb backup.dump

# Erreur: "database already exists"
# Solution: Clean avant restore
pg_restore --clean --if-exists -d mydb backup.dump

# Restore très lent
# Solution: Paralléliser
pg_restore -j 4 -d mydb backup.dump
```

## Erreurs de migration

```bash
# Erreur lors d'un ALTER TABLE sur grosse table
# Solution: Utiliser CONCURRENTLY si possible
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

# Pour les index:
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);

# Erreur: "tuple concurrently updated"
# Solution: Retry la transaction

# Erreur lors d'ajout de NOT NULL
# Solution: Ajouter en plusieurs étapes
-- 1. Ajouter la colonne
ALTER TABLE users ADD COLUMN email VARCHAR(255);
-- 2. Remplir avec des valeurs
UPDATE users SET email = 'default@example.com' WHERE email IS NULL;
-- 3. Ajouter la contrainte
ALTER TABLE users ALTER COLUMN email SET NOT NULL;
```

## Diagnostic général

```sql
-- Script de diagnostic complet
SELECT 'Connexions actives' as check,
       COUNT(*)::TEXT as value
FROM pg_stat_activity
UNION ALL
SELECT 'Cache hit ratio',
       ROUND(SUM(heap_blks_hit) * 100.0 / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2)::TEXT || '%'
FROM pg_statio_user_tables
UNION ALL
SELECT 'Taille DB',
       pg_size_pretty(pg_database_size(current_database()))
UNION ALL
SELECT 'Tables avec dead tuples > 10000',
       COUNT(*)::TEXT
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
UNION ALL
SELECT 'Index inutilisés',
       COUNT(*)::TEXT
FROM pg_stat_user_indexes
WHERE idx_scan = 0
UNION ALL
SELECT 'Requêtes longues (>5min)',
       COUNT(*)::TEXT
FROM pg_stat_activity
WHERE state != 'idle'
    AND NOW() - query_start > interval '5 minutes'
UNION ALL
SELECT 'Locks en attente',
       COUNT(*)::TEXT
FROM pg_locks
WHERE NOT granted;
```

## Outils de diagnostic

```bash
# pg_top (like htop for PostgreSQL)
sudo apt install ptop
pg_top -d mydb

# pgBadger (analyse des logs)
sudo apt install pgbadger
pgbadger /var/log/postgresql/*.log -o report.html

# pg_activity (monitoring en temps réel)
pip install pg_activity
pg_activity -h localhost -U postgres

# pgcli (CLI amélioré avec auto-completion)
pip install pgcli
pgcli postgresql://postgres@localhost/mydb
```

## Checklist troubleshooting

```
🔍 Checklist diagnostic:

☐ 1. PostgreSQL est-il démarré?
     sudo systemctl status postgresql

☐ 2. Peut-on se connecter localement?
     sudo -u postgres psql

☐ 3. Espace disque suffisant?
     df -h

☐ 4. Vérifier les logs
     tail -f /var/log/postgresql/postgresql-15-main.log

☐ 5. Connexions actives
     psql -c "SELECT COUNT(*) FROM pg_stat_activity;"

☐ 6. Requêtes longues?
     psql -c "SELECT pid, query FROM pg_stat_activity WHERE NOW() - query_start > interval '1 minute';"

☐ 7. Locks?
     psql -c "SELECT COUNT(*) FROM pg_locks WHERE NOT granted;"

☐ 8. Cache hit ratio > 99%?
     psql -c "SELECT ROUND(SUM(heap_blks_hit) * 100.0 / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2) FROM pg_statio_user_tables;"

☐ 9. Dead tuples élevés?
     psql -c "SELECT tablename, n_dead_tup FROM pg_stat_user_tables WHERE n_dead_tup > 10000;"

☐ 10. Réplication OK? (si applicable)
      psql -c "SELECT * FROM pg_stat_replication;"
```

## Ressources utiles

```
📚 Documentation et aide:

- Documentation officielle: https://www.postgresql.org/docs/
- Wiki PostgreSQL: https://wiki.postgresql.org/
- Mailing lists: https://www.postgresql.org/list/
- Stack Overflow: https://stackoverflow.com/questions/tagged/postgresql
- Reddit: r/PostgreSQL
- Slack: https://postgres-slack.herokuapp.com/

🛠️ Outils:
- pgAdmin: Interface graphique
- DBeaver: Client SQL universel
- DataGrip: IDE JetBrains
- Postico (Mac): Client PostgreSQL
- pgcli: CLI avec auto-completion
- pg_activity: Monitoring temps réel

📊 Monitoring:
- Prometheus + postgres_exporter
- Grafana
- pgBadger
- pg_stat_statements
```

[← Maintenance](./infos-postgresql-11-maintenance.md) | [Index](./infos-postgresql-00-index.md)
