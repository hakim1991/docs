# 📊 Monitoring

[← Réplication](./infos-postgresql-09-replication.md) | [Index](./infos-postgresql-00-index.md) | [Maintenance →](./infos-postgresql-11-maintenance.md)

## Vues système essentielles

```sql
-- Connexions actives
SELECT
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    NOW() - query_start AS duration,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- Nombre de connexions par database
SELECT
    datname,
    COUNT(*) as connections
FROM pg_stat_activity
GROUP BY datname
ORDER BY connections DESC;

-- Connexions par user
SELECT
    usename,
    COUNT(*) as connections
FROM pg_stat_activity
GROUP BY usename;

-- Connexions par state
SELECT
    state,
    COUNT(*) as count
FROM pg_stat_activity
GROUP BY state;
```

## Statistiques de tables

```sql
-- Tables les plus utilisées
SELECT
    schemaname,
    tablename,
    seq_scan,                           -- Sequential scans
    seq_tup_read,                       -- Lignes lues par seq scan
    idx_scan,                           -- Index scans
    idx_tup_fetch,                      -- Lignes lues par index
    n_tup_ins,                          -- Insertions
    n_tup_upd,                          -- Updates
    n_tup_del,                          -- Deletes
    n_live_tup,                         -- Lignes vivantes
    n_dead_tup                          -- Lignes mortes
FROM pg_stat_user_tables
ORDER BY seq_scan + idx_scan DESC
LIMIT 20;

-- Tables avec beaucoup de dead tuples
SELECT
    schemaname,
    tablename,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Dernière analyse/vacuum
SELECT
    schemaname,
    tablename,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY last_autovacuum NULLS FIRST;
```

## Statistiques d'index

```sql
-- Index utilisés
SELECT
    schemaname,
    tablename,
    indexrelname,
    idx_scan,                           -- Nombre de scans
    idx_tup_read,                       -- Lignes lues
    idx_tup_fetch                       -- Lignes retournées
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Index jamais utilisés
SELECT
    schemaname,
    tablename,
    indexrelname,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND indexrelid NOT IN (
        SELECT indexrelid FROM pg_index WHERE indisunique OR indisprimary
    )
ORDER BY pg_relation_size(indexrelid) DESC;

-- Cache hit ratio des index
SELECT
    schemaname,
    tablename,
    indexrelname,
    idx_blks_hit,
    idx_blks_read,
    CASE
        WHEN idx_blks_hit + idx_blks_read = 0 THEN NULL
        ELSE ROUND(idx_blks_hit * 100.0 / (idx_blks_hit + idx_blks_read), 2)
    END AS cache_hit_ratio
FROM pg_statio_user_indexes
ORDER BY cache_hit_ratio NULLS LAST;
```

## Taille des objets

```sql
-- Taille des databases
SELECT
    datname,
    pg_size_pretty(pg_database_size(datname)) as size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- Taille des tables (avec index et toast)
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) -
                   pg_relation_size(schemaname||'.'||tablename)) as external_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Top 20 plus grosses tables
SELECT
    n.nspname as schema,
    c.relname as table,
    pg_size_pretty(pg_total_relation_size(c.oid)) as total_size,
    pg_size_pretty(pg_relation_size(c.oid)) as table_size,
    pg_size_pretty(pg_indexes_size(c.oid)) as indexes_size
FROM pg_class c
LEFT JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind = 'r'
    AND n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(c.oid) DESC
LIMIT 20;

-- Taille totale par schéma
SELECT
    schemaname,
    pg_size_pretty(SUM(pg_total_relation_size(schemaname||'.'||tablename))::BIGINT) as total_size
FROM pg_tables
GROUP BY schemaname
ORDER BY SUM(pg_total_relation_size(schemaname||'.'||tablename)) DESC;
```

## Performance des requêtes

```sql
-- pg_stat_statements (nécessite l'extension)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 requêtes les plus lentes (temps total)
SELECT
    queryid,
    ROUND(total_exec_time::numeric, 2) as total_time_ms,
    calls,
    ROUND(mean_exec_time::numeric, 2) as avg_time_ms,
    ROUND(max_exec_time::numeric, 2) as max_time_ms,
    ROUND((100 * total_exec_time / SUM(total_exec_time) OVER())::numeric, 2) as percentage,
    query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Requêtes avec temps moyen élevé
SELECT
    queryid,
    calls,
    ROUND(mean_exec_time::numeric, 2) as avg_time_ms,
    ROUND(stddev_exec_time::numeric, 2) as stddev_time_ms,
    query
FROM pg_stat_statements
WHERE calls > 10
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Requêtes avec le plus d'I/O
SELECT
    queryid,
    calls,
    shared_blks_read + shared_blks_written as total_io,
    shared_blks_hit,
    query
FROM pg_stat_statements
ORDER BY shared_blks_read + shared_blks_written DESC
LIMIT 10;

-- Cache hit ratio par requête
SELECT
    queryid,
    calls,
    shared_blks_hit,
    shared_blks_read,
    CASE
        WHEN shared_blks_hit + shared_blks_read = 0 THEN NULL
        ELSE ROUND(shared_blks_hit * 100.0 / (shared_blks_hit + shared_blks_read), 2)
    END as cache_hit_ratio,
    query
FROM pg_stat_statements
WHERE shared_blks_hit + shared_blks_read > 0
ORDER BY cache_hit_ratio NULLS LAST
LIMIT 20;
```

## Cache et I/O

```sql
-- Cache hit ratio global (devrait être > 99%)
SELECT
    SUM(heap_blks_read) as heap_read,
    SUM(heap_blks_hit) as heap_hit,
    ROUND(SUM(heap_blks_hit) * 100.0 / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2) as cache_hit_ratio
FROM pg_statio_user_tables;

-- Cache hit ratio par table
SELECT
    schemaname,
    tablename,
    heap_blks_read,
    heap_blks_hit,
    ROUND(heap_blks_hit * 100.0 / NULLIF(heap_blks_hit + heap_blks_read, 0), 2) as cache_hit_ratio
FROM pg_statio_user_tables
WHERE heap_blks_read + heap_blks_hit > 0
ORDER BY cache_hit_ratio
LIMIT 20;

-- Statistiques I/O par backend
SELECT
    backend_type,
    COUNT(*) as count
FROM pg_stat_io
GROUP BY backend_type;
```

## Locks et blocages

```sql
-- Locks actifs
SELECT
    l.locktype,
    l.database,
    l.relation::regclass as table,
    l.page,
    l.tuple,
    l.virtualxid,
    l.transactionid,
    l.mode,
    l.granted,
    a.usename,
    a.query,
    a.query_start
FROM pg_locks l
LEFT JOIN pg_stat_activity a ON l.pid = a.pid
WHERE NOT l.granted
ORDER BY a.query_start;

-- Queries en attente de lock
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement,
    blocked_activity.application_name AS blocked_application
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

## Transactions longues

```sql
-- Transactions actives depuis plus de 5 minutes
SELECT
    pid,
    NOW() - xact_start AS duration,
    usename,
    query,
    state
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
    AND NOW() - xact_start > interval '5 minutes'
ORDER BY xact_start;

-- Oldest transaction
SELECT
    pid,
    NOW() - xact_start AS duration,
    usename,
    query
FROM pg_stat_activity
WHERE xact_start IS NOT NULL
ORDER BY xact_start
LIMIT 1;
```

## Replication monitoring

```sql
-- Statut des replicas (sur le primary)
SELECT
    client_addr,
    application_name,
    state,
    sync_state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) AS send_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) AS write_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) AS flush_lag_bytes,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS replay_lag_bytes,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;

-- Lag de réplication (sur le replica)
SELECT
    NOW() - pg_last_xact_replay_timestamp() AS replication_lag;
```

## Scripts de monitoring

```bash
#!/bin/bash
# monitor_postgres.sh

# Configuration
DB_NAME="mydb"
THRESHOLD_CONNECTIONS=80
THRESHOLD_SLOW_QUERIES=5

# Nombre de connexions
CONNECTIONS=$(psql -t -c "SELECT COUNT(*) FROM pg_stat_activity;")
echo "🔌 Connexions: $CONNECTIONS"

if [ $CONNECTIONS -gt $THRESHOLD_CONNECTIONS ]; then
    echo "⚠️  ALERTE: Trop de connexions ($CONNECTIONS)"
fi

# Requêtes lentes
SLOW_QUERIES=$(psql -t -c "
    SELECT COUNT(*)
    FROM pg_stat_activity
    WHERE state != 'idle'
        AND NOW() - query_start > interval '$THRESHOLD_SLOW_QUERIES seconds';
")
echo "🐌 Requêtes lentes (>5s): $SLOW_QUERIES"

# Cache hit ratio
CACHE_RATIO=$(psql -t -c "
    SELECT ROUND(SUM(heap_blks_hit) * 100.0 / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0), 2)
    FROM pg_statio_user_tables;
")
echo "💾 Cache hit ratio: ${CACHE_RATIO}%"

if (( $(echo "$CACHE_RATIO < 99" | bc -l) )); then
    echo "⚠️  ALERTE: Cache hit ratio faible"
fi

# Taille de la database
DB_SIZE=$(psql -t -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME'));")
echo "📊 Taille DB: $DB_SIZE"

# Dead tuples
DEAD_TUPLES=$(psql -t -c "
    SELECT SUM(n_dead_tup) FROM pg_stat_user_tables;
")
echo "💀 Dead tuples: $DEAD_TUPLES"
```

## Monitoring avec Prometheus + postgres_exporter

```bash
# Installer postgres_exporter
wget https://github.com/prometheus-community/postgres_exporter/releases/download/v0.15.0/postgres_exporter-0.15.0.linux-amd64.tar.gz
tar xzf postgres_exporter-0.15.0.linux-amd64.tar.gz
cd postgres_exporter-0.15.0.linux-amd64

# Configuration
export DATA_SOURCE_NAME="postgresql://postgres:secret@localhost:5432/mydb?sslmode=disable"

# Démarrer
./postgres_exporter

# Ou avec systemd
sudo cat > /etc/systemd/system/postgres_exporter.service << EOF
[Unit]
Description=PostgreSQL Prometheus Exporter
After=network.target

[Service]
Type=simple
User=postgres
Environment=DATA_SOURCE_NAME=postgresql://postgres:secret@localhost:5432/mydb?sslmode=disable
ExecStart=/usr/local/bin/postgres_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start postgres_exporter
sudo systemctl enable postgres_exporter

# Métriques disponibles sur http://localhost:9187/metrics
```

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'postgresql'
    static_configs:
      - targets: ['localhost:9187']
        labels:
          instance: 'postgres-prod'
```

## Monitoring avec Grafana

```yaml
# docker-compose.yml pour stack monitoring
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"

  postgres_exporter:
    image: prometheuscommunity/postgres-exporter
    environment:
      DATA_SOURCE_NAME: "postgresql://postgres:secret@postgres:5432/postgres?sslmode=disable"
    ports:
      - "9187:9187"
    depends_on:
      - postgres

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  prometheus-data:
  grafana-data:
```

## Alertes importantes

```sql
-- Créer une fonction pour les alertes
CREATE OR REPLACE FUNCTION check_database_health()
RETURNS TABLE (
    check_name TEXT,
    status TEXT,
    details TEXT
) AS $$
BEGIN
    -- Vérifier les connexions
    RETURN QUERY
    SELECT
        'Connections'::TEXT,
        CASE WHEN COUNT(*) > 80 THEN 'WARNING' ELSE 'OK' END,
        'Connexions actives: ' || COUNT(*)::TEXT
    FROM pg_stat_activity;

    -- Vérifier le cache hit ratio
    RETURN QUERY
    SELECT
        'Cache Hit Ratio'::TEXT,
        CASE
            WHEN cache_ratio < 99 THEN 'WARNING'
            ELSE 'OK'
        END,
        'Cache hit: ' || ROUND(cache_ratio, 2)::TEXT || '%'
    FROM (
        SELECT SUM(heap_blks_hit) * 100.0 / NULLIF(SUM(heap_blks_hit) + SUM(heap_blks_read), 0) as cache_ratio
        FROM pg_statio_user_tables
    ) t;

    -- Vérifier les dead tuples
    RETURN QUERY
    SELECT
        'Dead Tuples'::TEXT,
        CASE WHEN SUM(n_dead_tup) > 10000 THEN 'WARNING' ELSE 'OK' END,
        'Dead tuples: ' || SUM(n_dead_tup)::TEXT
    FROM pg_stat_user_tables;

    -- Vérifier les requêtes longues
    RETURN QUERY
    SELECT
        'Long Queries'::TEXT,
        CASE WHEN COUNT(*) > 0 THEN 'WARNING' ELSE 'OK' END,
        'Requêtes > 5min: ' || COUNT(*)::TEXT
    FROM pg_stat_activity
    WHERE state != 'idle'
        AND NOW() - query_start > interval '5 minutes';

END;
$$ LANGUAGE plpgsql;

-- Utiliser
SELECT * FROM check_database_health();
```

## Logs analysis

```bash
# Activer le logging des requêtes lentes
# Dans postgresql.conf:
log_min_duration_statement = 1000  # Log requêtes > 1s

# Analyser les logs avec pgBadger
sudo apt install pgbadger

# Générer un rapport
pgbadger /var/log/postgresql/postgresql-15-main.log -o report.html

# Avec plusieurs fichiers
pgbadger /var/log/postgresql/*.log -o report.html

# Format incrémental (pour cron)
pgbadger /var/log/postgresql/*.log -o /var/www/html/pg_report.html -I
```

[← Réplication](./infos-postgresql-09-replication.md) | [Index](./infos-postgresql-00-index.md) | [Maintenance →](./infos-postgresql-11-maintenance.md)
