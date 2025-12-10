# ⚡ Performances avancées

[← Index et optimisation](./infos-postgresql-06-index-optimisation.md) | [Index](./infos-postgresql-00-index.md) | [Backup et restore →](./infos-postgresql-08-backup-restore.md)

## Configuration mémoire

```conf
# postgresql.conf

# Shared Buffers (cache PostgreSQL)
# 25% de la RAM pour serveur dédié
shared_buffers = 2GB

# Effective Cache Size (cache total OS + PostgreSQL)
# 75% de la RAM
effective_cache_size = 6GB

# Work Mem (mémoire par opération de tri/hash)
# RAM / (max_connections * 2-3)
work_mem = 16MB

# Maintenance Work Mem (VACUUM, CREATE INDEX, ALTER TABLE)
# 5-10% de la RAM
maintenance_work_mem = 512MB

# Temp Buffers (tables temporaires)
temp_buffers = 16MB

# WAL Buffers
wal_buffers = 16MB
```

```bash
# Calculer pour 16GB RAM
shared_buffers = 4GB                    # 25%
effective_cache_size = 12GB             # 75%
work_mem = 32MB                         # 16GB / (100 * 5)
maintenance_work_mem = 1GB              # 6%
```

## Configuration connexions

```conf
# Connexions maximales
max_connections = 100

# Connexions réservées pour superuser
superuser_reserved_connections = 3

# Statement timeout (timeout requête)
statement_timeout = 30000               # 30s

# Lock timeout
lock_timeout = 5000                     # 5s

# Idle in transaction timeout
idle_in_transaction_session_timeout = 60000  # 60s
```

## Connection Pooling avec PgBouncer

```bash
# Installer PgBouncer
sudo apt install pgbouncer

# Configuration /etc/pgbouncer/pgbouncer.ini
```

```ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Mode pooling
pool_mode = transaction             # transaction, session, statement
max_client_conn = 1000              # Connexions client max
default_pool_size = 25              # Connexions vers PostgreSQL
reserve_pool_size = 5
reserve_pool_timeout = 5

# Logs
log_connections = 1
log_disconnections = 1
```

```bash
# userlist.txt
"myuser" "md5xyz123..."

# Démarrer
sudo systemctl start pgbouncer
sudo systemctl enable pgbouncer

# Se connecter via PgBouncer
psql -h localhost -p 6432 -U myuser -d mydb
```

## Partitionnement

```sql
-- Partitionnement par plage (RANGE)
CREATE TABLE orders (
    id BIGSERIAL,
    user_id INTEGER,
    total DECIMAL(10,2),
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Créer les partitions
CREATE TABLE orders_2023 PARTITION OF orders
    FOR VALUES FROM ('2023-01-01') TO ('2024-01-01');

CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE orders_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Partitionnement par liste (LIST)
CREATE TABLE users (
    id SERIAL,
    username VARCHAR(100),
    country VARCHAR(2) NOT NULL,
    PRIMARY KEY (id, country)
) PARTITION BY LIST (country);

CREATE TABLE users_fr PARTITION OF users FOR VALUES IN ('FR');
CREATE TABLE users_us PARTITION OF users FOR VALUES IN ('US');
CREATE TABLE users_other PARTITION OF users DEFAULT;

-- Partitionnement par hash (HASH)
CREATE TABLE logs (
    id BIGSERIAL,
    message TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (id)
) PARTITION BY HASH (id);

CREATE TABLE logs_0 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE logs_1 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 1);
CREATE TABLE logs_2 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 2);
CREATE TABLE logs_3 PARTITION OF logs FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- Index sur partitions
CREATE INDEX idx_orders_2024_user ON orders_2024(user_id);
CREATE INDEX idx_orders_2025_user ON orders_2025(user_id);

-- Lister les partitions
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE tablename LIKE 'orders_%'
ORDER BY tablename;
```

## Parallélisation des requêtes

```conf
# postgresql.conf
max_worker_processes = 8
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
parallel_setup_cost = 1000
parallel_tuple_cost = 0.1
min_parallel_table_scan_size = 8MB
```

```sql
-- Voir si une requête est parallélisée
EXPLAIN SELECT COUNT(*) FROM large_table;
-- Si vous voyez "Parallel Seq Scan", c'est parallélisé

-- Forcer la parallélisation (test)
SET max_parallel_workers_per_gather = 4;
SET parallel_setup_cost = 0;

-- Désactiver (debug)
SET max_parallel_workers_per_gather = 0;
```

## Table partitioning automatique avec pg_partman

```sql
-- Installer extension
CREATE EXTENSION pg_partman;

-- Créer table mère
CREATE TABLE logs (
    id BIGSERIAL,
    message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Configurer pg_partman
SELECT partman.create_parent(
    p_parent_table => 'public.logs',
    p_control => 'created_at',
    p_type => 'native',
    p_interval => 'monthly',
    p_premake => 3
);

-- Créer les partitions futures automatiquement
SELECT partman.run_maintenance('public.logs');

-- Automatiser avec cron
-- Ajouter dans crontab:
-- 0 0 * * * psql -c "SELECT partman.run_maintenance()"
```

## Optimisation des écritures

```conf
# postgresql.conf

# WAL (Write-Ahead Logging)
wal_level = replica
wal_buffers = 16MB
min_wal_size = 1GB
max_wal_size = 4GB

# Checkpoints
checkpoint_timeout = 15min
checkpoint_completion_target = 0.9

# Commit delay (grouper les commits)
commit_delay = 10                       # microseconds
commit_siblings = 5

# Synchronous commit
synchronous_commit = on                 # on, off, remote_apply, remote_write, local
```

```sql
-- Désactiver temporairement pour import massif
BEGIN;
SET synchronous_commit = off;
SET maintenance_work_mem = '1GB';

COPY large_table FROM '/path/to/data.csv' WITH CSV;

COMMIT;
```

## Bulk Insert optimisé

```sql
-- ❌ Lent: INSERT un par un
INSERT INTO users (email, username) VALUES ('user1@example.com', 'user1');
INSERT INTO users (email, username) VALUES ('user2@example.com', 'user2');
-- ...

-- ✅ Rapide: INSERT multiple
INSERT INTO users (email, username) VALUES
    ('user1@example.com', 'user1'),
    ('user2@example.com', 'user2'),
    ('user3@example.com', 'user3');

-- ✅ Très rapide: COPY
COPY users (email, username) FROM '/tmp/users.csv' WITH CSV HEADER;

-- ✅ Import optimisé
BEGIN;

-- Désactiver les triggers
ALTER TABLE users DISABLE TRIGGER ALL;

-- Supprimer les index (sauf PK)
DROP INDEX IF EXISTS idx_users_email;
DROP INDEX IF EXISTS idx_users_country;

-- Import
COPY users FROM '/tmp/users.csv' WITH CSV HEADER;

-- Recréer les index
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_country ON users(country);

-- Réactiver les triggers
ALTER TABLE users ENABLE TRIGGER ALL;

-- Analyser
ANALYZE users;

COMMIT;
```

## UNLOGGED tables (super rapide mais pas durable)

```sql
-- Table UNLOGGED (pas de WAL, perdue en cas de crash)
CREATE UNLOGGED TABLE temp_data (
    id SERIAL PRIMARY KEY,
    data TEXT
);

-- Utilisation: données temporaires, cache, sessions
-- ⚠️ Ne pas utiliser pour données importantes

-- Convertir en table normale
ALTER TABLE temp_data SET LOGGED;

-- Convertir en UNLOGGED
ALTER TABLE temp_data SET UNLOGGED;
```

## Materialized Views (cache de requêtes complexes)

```sql
-- Créer une vue matérialisée
CREATE MATERIALIZED VIEW user_stats AS
SELECT
    u.id,
    u.username,
    COUNT(o.id) as order_count,
    SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.username;

-- Créer un index
CREATE INDEX idx_user_stats_order_count ON user_stats(order_count DESC);

-- Utiliser
SELECT * FROM user_stats WHERE order_count > 10;

-- Rafraîchir les données
REFRESH MATERIALIZED VIEW user_stats;

-- Rafraîchir sans bloquer les lectures
REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats;

-- Automatiser le rafraîchissement (cron ou pg_cron)
CREATE EXTENSION pg_cron;
SELECT cron.schedule('refresh-user-stats', '0 * * * *',
    $$REFRESH MATERIALIZED VIEW CONCURRENTLY user_stats$$);
```

## Prepared Statements

```sql
-- Préparer une requête
PREPARE get_user_orders (INTEGER) AS
    SELECT * FROM orders WHERE user_id = $1;

-- Exécuter
EXECUTE get_user_orders(123);

-- Voir les prepared statements
SELECT name, statement, parameter_types FROM pg_prepared_statements;

-- Supprimer
DEALLOCATE get_user_orders;
```

## Monitoring en temps réel

```sql
-- Connexions actives
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query,
    NOW() - query_start as duration
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Requêtes longues
SELECT
    pid,
    NOW() - query_start as duration,
    query,
    state
FROM pg_stat_activity
WHERE state != 'idle'
    AND NOW() - query_start > interval '5 seconds'
ORDER BY duration DESC;

-- Bloquer/tuer une requête
SELECT pg_cancel_backend(pid);      -- Cancel graceful
SELECT pg_terminate_backend(pid);   -- Kill

-- Locks
SELECT
    l.pid,
    l.mode,
    l.granted,
    a.query
FROM pg_locks l
JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted;

-- Taille des tables
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) -
                   pg_relation_size(schemaname||'.'||tablename)) as indexes_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Cache hit ratio (devrait être > 99%)
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit)  as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as cache_hit_ratio
FROM pg_statio_user_tables;
```

## pg_stat_statements

```sql
-- Installer
CREATE EXTENSION pg_stat_statements;

-- Top 10 requêtes lentes
SELECT
    round(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    round(mean_exec_time::numeric, 2) as avg_time_ms,
    round((100 * total_exec_time / sum(total_exec_time) OVER())::numeric, 2) as percentage,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Requêtes avec plus de lectures disque
SELECT
    calls,
    shared_blks_read + shared_blks_written as total_io,
    query
FROM pg_stat_statements
ORDER BY shared_blks_read + shared_blks_written DESC
LIMIT 10;

-- Reset des stats
SELECT pg_stat_statements_reset();
```

## Configuration SSD vs HDD

```conf
# Pour SSD
random_page_cost = 1.1
effective_io_concurrency = 200
maintenance_work_mem = 1GB

# Pour HDD
random_page_cost = 4.0
effective_io_concurrency = 2
maintenance_work_mem = 256MB
```

## Cas pratique: Optimiser une application

```sql
-- 1. Activer pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- 2. Laisser tourner l'application pendant quelques heures

-- 3. Identifier les requêtes lentes
SELECT
    round(total_exec_time::numeric, 2) as total_ms,
    calls,
    round(mean_exec_time::numeric, 2) as avg_ms,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- 4. Analyser chaque requête lente
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;

-- 5. Créer les index manquants
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- 6. Vérifier l'amélioration
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123;

-- 7. Mettre à jour les stats
ANALYZE orders;

-- 8. Vérifier le cache hit ratio
SELECT
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as cache_hit_ratio
FROM pg_statio_user_tables;
-- Si < 99%, augmenter shared_buffers

-- 9. Vérifier les connexions
SELECT COUNT(*) FROM pg_stat_activity;
-- Si proche de max_connections, utiliser PgBouncer
```

## Benchmarking

```bash
# pgbench (outil de benchmark PostgreSQL)
# Initialiser
pgbench -i -s 50 mydb

# Lancer le benchmark
pgbench -c 10 -j 2 -t 1000 mydb
# -c : nombre de clients
# -j : nombre de threads
# -t : nombre de transactions par client

# Résultat exemple:
# tps = 1234.56 (including connections establishing)
# tps = 1245.67 (excluding connections establishing)
```

[← Index et optimisation](./infos-postgresql-06-index-optimisation.md) | [Index](./infos-postgresql-00-index.md) | [Backup et restore →](./infos-postgresql-08-backup-restore.md)
