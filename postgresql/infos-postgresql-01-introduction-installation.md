# 🚀 Introduction et Installation PostgreSQL

[Index](./infos-postgresql-00-index.md) | [Configuration →](./infos-postgresql-02-configuration.md)

## Qu'est-ce que PostgreSQL ?

**PostgreSQL** est un système de gestion de base de données relationnelle (SGBD) open-source, puissant et conforme aux standards SQL.

### Caractéristiques principales

```
✅ Open source et gratuit
✅ Conforme ACID
✅ Support avancé de SQL
✅ Types de données riches (JSON, XML, Arrays, etc.)
✅ Extensions (PostGIS, pgcrypto, etc.)
✅ Réplication et haute disponibilité
✅ Performance et scalabilité
✅ Communauté active
```

## Installation sur Linux

### Ubuntu / Debian

```bash
# Installer PostgreSQL
sudo apt update
sudo apt install -y postgresql postgresql-contrib

# Vérifier l'installation
psql --version

# Démarrer PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Statut
sudo systemctl status postgresql
```

### Installation version spécifique

```bash
# Ajouter le dépôt officiel PostgreSQL
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget -qO- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/pgdg.asc &>/dev/null

# Installer PostgreSQL 15
sudo apt update
sudo apt install -y postgresql-15 postgresql-contrib-15
```

### CentOS / RHEL

```bash
# Installer le dépôt
sudo yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-$(rpm -E %{rhel})-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Installer PostgreSQL 15
sudo yum install -y postgresql15-server postgresql15-contrib

# Initialiser la base de données
sudo /usr/pgsql-15/bin/postgresql-15-setup initdb

# Démarrer et activer
sudo systemctl start postgresql-15
sudo systemctl enable postgresql-15
```

## Installation sur Windows

```powershell
# Télécharger depuis https://www.postgresql.org/download/windows/
# Ou avec Chocolatey
choco install postgresql

# Démarrer le service
net start postgresql-x64-15
```

## Installation avec Docker

```bash
# Démarrer PostgreSQL
docker run -d \
    --name postgres \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_USER=admin \
    -e POSTGRES_DB=mydb \
    -p 5432:5432 \
    -v postgres-data:/var/lib/postgresql/data \
    postgres:15-alpine

# Se connecter
docker exec -it postgres psql -U admin -d mydb
```

## Première connexion

```bash
# Se connecter en tant que postgres (superuser)
sudo -u postgres psql

# Ou directement
sudo -i -u postgres
psql
```

```sql
-- Afficher la version
SELECT version();

-- Lister les bases de données
\l

-- Lister les utilisateurs
\du

-- Quitter
\q
```

## Créer un utilisateur et une database

```bash
# Créer un utilisateur
sudo -u postgres createuser --interactive

# Créer une base de données
sudo -u postgres createdb mydb

# Ou en SQL
sudo -u postgres psql
```

```sql
-- Créer un utilisateur
CREATE USER myuser WITH PASSWORD 'secret';

-- Créer une database
CREATE DATABASE mydb OWNER myuser;

-- Donner tous les privilèges
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

-- Se connecter à la nouvelle database
\c mydb
```

## Configuration d'accès

```bash
# Éditer pg_hba.conf
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

```conf
# Autoriser les connexions locales avec mot de passe
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5

# Autoriser depuis le réseau local
host    all             all             192.168.1.0/24          md5
```

```bash
# Redémarrer PostgreSQL
sudo systemctl restart postgresql
```

## Connexion depuis un client

```bash
# psql
psql -h localhost -U myuser -d mydb

# Avec URL
psql postgresql://myuser:secret@localhost:5432/mydb

# Variables d'environnement
export PGHOST=localhost
export PGUSER=myuser
export PGPASSWORD=secret
export PGDATABASE=mydb
psql
```

## Commandes psql essentielles

```sql
-- Bases de données
\l                  -- Lister les databases
\c database         -- Se connecter à une database

-- Tables
\dt                 -- Lister les tables
\d table            -- Décrire une table
\d+ table           -- Description détaillée

-- Utilisateurs et permissions
\du                 -- Lister les rôles/users
\dp                 -- Lister les permissions

-- Schémas
\dn                 -- Lister les schémas

-- Aide
\?                  -- Aide sur les commandes psql
\h                  -- Aide sur les commandes SQL
\h CREATE TABLE     -- Aide sur une commande spécifique

-- Quitter
\q
```

## Vérification de l'installation

```bash
# Test de connexion
psql -U postgres -c "SELECT version();"

# Voir les processus PostgreSQL
ps aux | grep postgres

# Port d'écoute
sudo netstat -tulpn | grep 5432
sudo ss -tulpn | grep 5432

# Logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

## Firewall

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 5432/tcp

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=5432/tcp
sudo firewall-cmd --reload
```

## Troubleshooting installation

```bash
# PostgreSQL ne démarre pas
sudo systemctl status postgresql
sudo journalctl -u postgresql -n 50

# Problème de permissions
ls -la /var/lib/postgresql/15/main/
sudo chown -R postgres:postgres /var/lib/postgresql/

# Réinitialiser le mot de passe postgres
sudo -u postgres psql
ALTER USER postgres WITH PASSWORD 'newpassword';
```

[Index](./infos-postgresql-00-index.md) | [Configuration →](./infos-postgresql-02-configuration.md)
