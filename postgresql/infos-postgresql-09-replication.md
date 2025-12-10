# 🔄 Réplication

[← Backup et restore](./infos-postgresql-08-backup-restore.md) | [Index](./infos-postgresql-00-index.md) | [Monitoring →](./infos-postgresql-10-monitoring.md)

## Types de réplication

```
📊 Types de réplication PostgreSQL:

1. Streaming Replication (asynchrone/synchrone)
   - Réplication physique (binaire)
   - Réplica en lecture seule (read-only)
   - Haute disponibilité et load balancing lectures

2. Logical Replication
   - Réplication logique (niveau ligne)
   - Permet modifications sur réplica
   - Réplication sélective (tables spécifiques)
   - Migration entre versions

3. Synchronous vs Asynchronous
   - Sync: commit attend confirmation réplica
   - Async: commit immédiat, réplication différée
```

## Streaming Replication - Configuration Primary

```conf
# postgresql.conf sur le serveur PRIMARY

# WAL
wal_level = replica                     # replica ou logical
max_wal_senders = 5                     # Nombre de réplicas max
wal_keep_size = 1GB                     # Garder les WAL pour réplicas
max_replication_slots = 5               # Slots de réplication

# Synchronous (optionnel)
synchronous_commit = on
synchronous_standby_names = 'replica1,replica2'

# Archive (optionnel mais recommandé)
archive_mode = on
archive_command = 'cp %p /archive/wal/%f'
```

```sql
-- Créer un utilisateur de réplication
CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'secret';
```

```conf
# pg_hba.conf sur le PRIMARY
# Autoriser la réplication

# TYPE  DATABASE        USER            ADDRESS                 METHOD
host    replication     replicator      192.168.1.0/24          md5
host    replication     replicator      10.0.0.0/8              md5
```

```bash
# Redémarrer PostgreSQL
sudo systemctl restart postgresql
```

## Streaming Replication - Configuration Replica

```bash
# Sur le serveur REPLICA

# 1. Arrêter PostgreSQL (si démarré)
sudo systemctl stop postgresql

# 2. Vider le data directory
sudo rm -rf /var/lib/postgresql/15/main/*

# 3. Créer un base backup depuis le primary
sudo -u postgres pg_basebackup \
    -h primary-server.local \
    -U replicator \
    -D /var/lib/postgresql/15/main \
    -P \
    -X stream \
    -c fast

# 4. Créer le fichier standby.signal
sudo -u postgres touch /var/lib/postgresql/15/main/standby.signal

# 5. Configurer la connexion au primary
sudo -u postgres cat >> /var/lib/postgresql/15/main/postgresql.auto.conf << EOF
primary_conninfo = 'host=primary-server.local port=5432 user=replicator password=secret'
EOF

# 6. Démarrer le replica
sudo systemctl start postgresql

# 7. Vérifier le statut
sudo -u postgres psql -c "SELECT * FROM pg_stat_wal_receiver;"
```

## Vérifier la réplication

```sql
-- Sur le PRIMARY
-- Voir les réplicas connectés
SELECT
    client_addr,
    state,
    sync_state,
    replay_lsn,
    write_lag,
    flush_lag,
    replay_lag
FROM pg_stat_replication;

-- Voir les slots de réplication
SELECT * FROM pg_replication_slots;

-- Sur le REPLICA
-- Vérifier le mode recovery
SELECT pg_is_in_recovery();  -- true si replica

-- Voir le lag de réplication
SELECT
    NOW() - pg_last_xact_replay_timestamp() AS replication_lag;

-- Statut du receiver
SELECT * FROM pg_stat_wal_receiver;
```

## Synchronous Replication

```conf
# postgresql.conf sur le PRIMARY
synchronous_commit = on
synchronous_standby_names = 'replica1'      # Un replica
# Ou
synchronous_standby_names = 'FIRST 1 (replica1, replica2)'  # Le premier disponible
# Ou
synchronous_standby_names = 'ANY 1 (replica1, replica2)'    # N'importe lequel
```

```sql
-- Vérifier la réplication synchrone
SELECT
    application_name,
    client_addr,
    state,
    sync_state,  -- sync, async, potential, quorum
    replay_lag
FROM pg_stat_replication;
```

## Replication Slots

```sql
-- Sur le PRIMARY
-- Créer un slot de réplication
SELECT * FROM pg_create_physical_replication_slot('replica1_slot');

-- Lister les slots
SELECT * FROM pg_replication_slots;

-- Supprimer un slot
SELECT pg_drop_replication_slot('replica1_slot');

-- Sur le REPLICA, utiliser le slot
-- Dans postgresql.auto.conf ou postgresql.conf:
primary_slot_name = 'replica1_slot'
```

## Promouvoir un Replica en Primary

```bash
# En cas de failover (primary down)

# 1. Sur le REPLICA, promouvoir en primary
sudo -u postgres pg_ctl promote -D /var/lib/postgresql/15/main

# Ou avec systemctl (PostgreSQL 12+)
sudo -u postgres psql -c "SELECT pg_promote();"

# 2. Vérifier qu'il n'est plus en recovery
psql -c "SELECT pg_is_in_recovery();"  -- false

# 3. Les applications peuvent maintenant écrire sur ce serveur

# 4. Reconfigurer l'ancien primary comme replica (quand il revient)
# Suivre les étapes "Configuration Replica" ci-dessus
```

## Logical Replication

```conf
# postgresql.conf sur le PRIMARY et REPLICA
wal_level = logical
max_replication_slots = 5
max_wal_senders = 5
```

```sql
-- Sur le PRIMARY
-- 1. Créer une publication
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- Ou pour des tables spécifiques
CREATE PUBLICATION my_publication FOR TABLE users, orders;

-- Ou avec filtre
CREATE PUBLICATION active_users FOR TABLE users WHERE (is_active = true);

-- Lister les publications
\dRp
SELECT * FROM pg_publication;

-- Sur le REPLICA
-- 2. Créer les mêmes tables (schema)
CREATE TABLE users (...);
CREATE TABLE orders (...);

-- 3. Créer une souscription
CREATE SUBSCRIPTION my_subscription
    CONNECTION 'host=primary.local dbname=mydb user=replicator password=secret'
    PUBLICATION my_publication;

-- Lister les souscriptions
\dRs
SELECT * FROM pg_subscription;

-- Vérifier l'état
SELECT * FROM pg_stat_subscription;
```

## Gérer la réplication logique

```sql
-- Ajouter des tables à une publication
ALTER PUBLICATION my_publication ADD TABLE products;

-- Retirer des tables
ALTER PUBLICATION my_publication DROP TABLE products;

-- Désactiver temporairement une souscription
ALTER SUBSCRIPTION my_subscription DISABLE;

-- Réactiver
ALTER SUBSCRIPTION my_subscription ENABLE;

-- Rafraîchir une souscription (resynchroniser)
ALTER SUBSCRIPTION my_subscription REFRESH PUBLICATION;

-- Supprimer une souscription
DROP SUBSCRIPTION my_subscription;

-- Supprimer une publication
DROP PUBLICATION my_publication;
```

## Load Balancing avec HAProxy

```bash
# Installer HAProxy
sudo apt install haproxy
```

```conf
# /etc/haproxy/haproxy.cfg

global
    maxconn 4096
    log /dev/log local0

defaults
    mode tcp
    timeout connect 5s
    timeout client 30s
    timeout server 30s
    log global

# Frontend pour les écritures (vers primary)
frontend postgres_write
    bind *:5432
    default_backend postgres_primary

# Backend primary (écritures)
backend postgres_primary
    option pgsql-check user health_check
    server primary1 192.168.1.10:5432 check

# Frontend pour les lectures (load balancing)
frontend postgres_read
    bind *:5433
    default_backend postgres_replicas

# Backend replicas (lectures)
backend postgres_replicas
    balance roundrobin
    option pgsql-check user health_check
    server replica1 192.168.1.11:5432 check
    server replica2 192.168.1.12:5432 check
    server replica3 192.168.1.13:5432 check

# Stats
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
```

```bash
# Créer l'utilisateur health_check
# Sur tous les serveurs PostgreSQL
psql -c "CREATE USER health_check WITH PASSWORD 'secret';"

# Redémarrer HAProxy
sudo systemctl restart haproxy
sudo systemctl enable haproxy

# Connexions:
# Écritures: psql -h haproxy.local -p 5432
# Lectures:  psql -h haproxy.local -p 5433
```

## High Availability avec Patroni

```bash
# Installer Patroni
sudo apt install patroni

# Configuration /etc/patroni/patroni.yml
```

```yaml
scope: postgres-cluster
namespace: /service/
name: postgres1

restapi:
  listen: 0.0.0.0:8008
  connect_address: 192.168.1.10:8008

etcd:
  hosts: 192.168.1.20:2379,192.168.1.21:2379,192.168.1.22:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      parameters:
        wal_level: replica
        hot_standby: "on"
        max_wal_senders: 10
        max_replication_slots: 10

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 192.168.1.10:5432
  data_dir: /var/lib/postgresql/15/main
  pgpass: /tmp/pgpass
  authentication:
    replication:
      username: replicator
      password: secret
    superuser:
      username: postgres
      password: supersecret
  parameters:
    unix_socket_directories: '/var/run/postgresql'

tags:
    nofailover: false
    noloadbalance: false
    clonefrom: false
    nosync: false
```

```bash
# Démarrer Patroni
sudo systemctl start patroni
sudo systemctl enable patroni

# Vérifier le cluster
patronictl -c /etc/patroni/patroni.yml list

# Basculer manuellement
patronictl -c /etc/patroni/patroni.yml switchover
```

## Monitoring de la réplication

```sql
-- Sur le PRIMARY
-- Lag par replica
SELECT
    client_addr,
    application_name,
    state,
    sync_state,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS replay_lag_bytes,
    EXTRACT(EPOCH FROM (NOW() - reply_time)) AS seconds_since_last_reply
FROM pg_stat_replication;

-- Taille des WAL
SELECT pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0'));

-- Sur le REPLICA
-- Lag de réplication
SELECT
    EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp()))::INT AS lag_seconds;

-- Bytes en retard
SELECT pg_wal_lsn_diff(
    pg_last_wal_receive_lsn(),
    pg_last_wal_replay_lsn()
) AS replay_lag_bytes;
```

```bash
#!/bin/bash
# check_replication_lag.sh
# Script de monitoring

THRESHOLD=10  # secondes

LAG=$(psql -h replica.local -U postgres -t -c "
    SELECT EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp()))::INT;
")

if [ $LAG -gt $THRESHOLD ]; then
    echo "⚠️  ALERTE: Lag de réplication = ${LAG}s"
    # Envoyer alerte (email, Slack, etc.)
else
    echo "✅ Réplication OK: lag = ${LAG}s"
fi
```

## Cascade Replication

```
PRIMARY → REPLICA1 → REPLICA2
```

```bash
# Sur REPLICA1
# postgresql.conf ou postgresql.auto.conf
hot_standby = on
max_wal_senders = 5
wal_level = replica

# REPLICA1 peut maintenant servir de source pour REPLICA2

# Sur REPLICA2, pointer vers REPLICA1
primary_conninfo = 'host=replica1.local port=5432 user=replicator password=secret'
```

## Troubleshooting

```sql
-- Réplication en retard
-- Voir le lag
SELECT
    client_addr,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes
FROM pg_stat_replication;

-- Si lag élevé, vérifier:
-- 1. Charge du replica
-- 2. Réseau entre primary et replica
-- 3. Disk I/O du replica

-- Slot de réplication plein
SELECT
    slot_name,
    pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained_wal
FROM pg_replication_slots;

-- Si trop gros, supprimer le slot
SELECT pg_drop_replication_slot('slot_name');

-- Replica out of sync
-- Sur le replica, vérifier les erreurs
tail -f /var/log/postgresql/postgresql-15-main.log

-- Resynchroniser
sudo systemctl stop postgresql
sudo rm -rf /var/lib/postgresql/15/main/*
sudo -u postgres pg_basebackup -h primary.local -U replicator \
    -D /var/lib/postgresql/15/main -P -X stream
sudo -u postgres touch /var/lib/postgresql/15/main/standby.signal
sudo systemctl start postgresql

-- Replica ne peut pas être promu
-- Vérifier standby.signal existe
ls -la /var/lib/postgresql/15/main/standby.signal

-- Promouvoir
sudo -u postgres pg_ctl promote -D /var/lib/postgresql/15/main
```

[← Backup et restore](./infos-postgresql-08-backup-restore.md) | [Index](./infos-postgresql-00-index.md) | [Monitoring →](./infos-postgresql-10-monitoring.md)
