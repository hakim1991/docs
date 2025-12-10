# ⚙️ Configuration PostgreSQL

[← Installation](./infos-postgresql-01-introduction-installation.md) | [Index](./infos-postgresql-00-index.md) | [Databases et schémas →](./infos-postgresql-03-databases-schemas.md)

## Fichiers de configuration

```
/etc/postgresql/15/main/
├── postgresql.conf      # Configuration principale
├── pg_hba.conf         # Authentification
├── pg_ident.conf       # Mapping des utilisateurs
└── environment         # Variables d'environnement
```

## postgresql.conf

```conf
# Connexions
listen_addresses = '*'           # Écouter sur toutes les interfaces
port = 5432                      # Port par défaut
max_connections = 100            # Connexions max simultanées

# Mémoire
shared_buffers = 256MB           # RAM pour le cache
effective_cache_size = 1GB       # Cache total disponible
work_mem = 4MB                   # RAM par opération de tri
maintenance_work_mem = 64MB      # RAM pour maintenance (VACUUM, CREATE INDEX)

# WAL (Write-Ahead Logging)
wal_level = replica              # Level pour réplication
wal_buffers = 16MB              # Buffers WAL
checkpoint_timeout = 5min        # Temps entre checkpoints
max_wal_size = 1GB              # Taille max WAL avant checkpoint

# Logging
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 10MB
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '
log_min_duration_statement = 1000  # Log requêtes > 1s

# Performance
random_page_cost = 1.1           # SSD: 1.1, HDD: 4.0
effective_io_concurrency = 200   # Nombre de I/O simultanées
max_worker_processes = 4
max_parallel_workers_per_gather = 2
```

## pg_hba.conf (Host-Based Authentication)

```conf
# TYPE  DATABASE  USER      ADDRESS          METHOD

# Local connections
local   all       postgres                   peer
local   all       all                        md5

# IPv4 local connections
host    all       all       127.0.0.1/32     md5

# IPv6 local connections
host    all       all       ::1/128          md5

# Réseau local
host    all       all       192.168.1.0/24   md5

# Connexions SSL
hostssl all       all       0.0.0.0/0        md5

# Méthodes d'authentification:
# trust  - Pas de mot de passe (⚠️ DANGEREUX)
# md5    - Mot de passe MD5 (recommandé)
# scram-sha-256 - Plus sécurisé que MD5
# peer   - Utilisateur système (local only)
# ident  - Serveur ident
```

## Memory tuning

```bash
# Calculer les paramètres optimaux
# Pour un serveur dédié avec 4GB RAM:

shared_buffers = 1GB                # 25% de la RAM
effective_cache_size = 3GB          # 75% de la RAM
work_mem = 10MB                     # RAM / max_connections
maintenance_work_mem = 256MB        # 5-10% de la RAM
```

```conf
# Configuration optimale pour 8GB RAM
shared_buffers = 2GB
effective_cache_size = 6GB
maintenance_work_mem = 512MB
work_mem = 20MB
```

## Recharger la configuration

```bash
# Recharger sans redémarrer
sudo systemctl reload postgresql

# Ou depuis psql
SELECT pg_reload_conf();

# Voir les paramètres actuels
SHOW all;
SHOW shared_buffers;
SHOW max_connections;

# Voir les paramètres modifiés
SELECT name, setting, source
FROM pg_settings
WHERE source != 'default';
```

## Configuration pour Docker

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    command:
      - "postgres"
      - "-c"
      - "shared_buffers=256MB"
      - "-c"
      - "max_connections=200"
      - "-c"
      - "work_mem=4MB"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./postgresql.conf:/etc/postgresql/postgresql.conf
```

[← Installation](./infos-postgresql-01-introduction-installation.md) | [Index](./infos-postgresql-00-index.md) | [Databases et schémas →](./infos-postgresql-03-databases-schemas.md)
