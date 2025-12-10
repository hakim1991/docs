# 👥 Users et Permissions

[← Databases](./infos-postgresql-03-databases-schemas.md) | [Index](./infos-postgresql-00-index.md) | [Requêtes SQL →](./infos-postgresql-05-requetes-sql.md)

## Créer des utilisateurs

```sql
-- Créer un utilisateur simple
CREATE USER myuser WITH PASSWORD 'secret';

-- Avec options
CREATE USER admin WITH
    PASSWORD 'supersecret'
    CREATEDB
    CREATEROLE
    LOGIN
    VALID UNTIL '2025-12-31';

-- Créer un rôle (groupe)
CREATE ROLE readonly;
CREATE ROLE readwrite;
```

```bash
# Depuis le shell
createuser myuser
createuser -P myuser  # Avec prompt password
```

## Lister les utilisateurs

```sql
-- Lister les rôles/users
\du

SELECT usename, usesuper, usecreatedb
FROM pg_user;

-- Voir les attributs
SELECT rolname, rolsuper, rolinherit, rolcreaterole, rolcreatedb
FROM pg_roles;
```

## Modifier un utilisateur

```sql
-- Changer le mot de passe
ALTER USER myuser WITH PASSWORD 'newpassword';

-- Donner des privilèges
ALTER USER myuser WITH CREATEDB;
ALTER USER myuser WITH SUPERUSER;

-- Retirer des privilèges
ALTER USER myuser WITH NOCREATEDB;

-- Renommer
ALTER USER oldname RENAME TO newname;

-- Définir une expiration
ALTER USER myuser VALID UNTIL '2025-12-31';
```

## GRANT - Donner des permissions

```sql
-- Database
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
GRANT CONNECT ON DATABASE mydb TO readonly;

-- Schema
GRANT USAGE ON SCHEMA public TO myuser;
GRANT ALL ON SCHEMA sales TO myuser;

-- Tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;
GRANT SELECT, INSERT, UPDATE, DELETE ON users TO myuser;
GRANT ALL PRIVILEGES ON users TO myuser;

-- Permissions futures
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO readonly;

-- Séquences (pour SERIAL)
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO myuser;
```

## REVOKE - Retirer des permissions

```sql
-- Retirer toutes les permissions
REVOKE ALL PRIVILEGES ON DATABASE mydb FROM myuser;
REVOKE ALL ON users FROM myuser;

-- Retirer des permissions spécifiques
REVOKE INSERT, UPDATE, DELETE ON users FROM readonly;
```

## Rôles (groupes)

```sql
-- Créer des rôles
CREATE ROLE readonly;
CREATE ROLE readwrite;
CREATE ROLE admin;

-- Donner des permissions aux rôles
GRANT CONNECT ON DATABASE mydb TO readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;

GRANT CONNECT ON DATABASE mydb TO readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO readwrite;

-- Assigner des utilisateurs aux rôles
GRANT readonly TO user1;
GRANT readwrite TO user2;
GRANT admin TO user3;

-- Retirer un utilisateur d'un rôle
REVOKE readonly FROM user1;
```

## Configuration typique

```sql
-- 1. Créer la database
CREATE DATABASE myapp;

-- 2. Créer les rôles
CREATE ROLE app_readonly;
CREATE ROLE app_readwrite;
CREATE ROLE app_admin;

-- 3. Permissions readonly
GRANT CONNECT ON DATABASE myapp TO app_readonly;
\c myapp
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO app_readonly;

-- 4. Permissions readwrite
GRANT CONNECT ON DATABASE myapp TO app_readwrite;
GRANT USAGE, CREATE ON SCHEMA public TO app_readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_readwrite;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO app_readwrite;

-- 5. Créer les utilisateurs
CREATE USER app_user WITH PASSWORD 'userpass';
CREATE USER app_service WITH PASSWORD 'servicepass';
CREATE USER app_manager WITH PASSWORD 'managerpass';

-- 6. Assigner les rôles
GRANT app_readonly TO app_user;
GRANT app_readwrite TO app_service;
GRANT app_admin TO app_manager;
```

## Vérifier les permissions

```sql
-- Permissions sur une table
\dp users
SELECT grantee, privilege_type
FROM information_schema.table_privileges
WHERE table_name = 'users';

-- Permissions d'un utilisateur
\du myuser

-- Tables accessibles par un utilisateur
SELECT table_schema, table_name, privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'myuser';
```

## Supprimer un utilisateur

```sql
-- Supprimer un utilisateur
DROP USER myuser;

-- Si l'utilisateur possède des objets
REASSIGN OWNED BY myuser TO postgres;
DROP OWNED BY myuser;
DROP USER myuser;
```

## Row Level Security (RLS)

```sql
-- Activer RLS sur une table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Politique: les users ne voient que leurs documents
CREATE POLICY user_documents ON documents
    FOR SELECT
    USING (user_id = current_user_id());

-- Politique: admin voit tout
CREATE POLICY admin_all ON documents
    FOR ALL
    TO admin_role
    USING (true);
```

[← Databases](./infos-postgresql-03-databases-schemas.md) | [Index](./infos-postgresql-00-index.md) | [Requêtes SQL →](./infos-postgresql-05-requetes-sql.md)
