# 💾 Databases et Schémas

[← Configuration](./infos-postgresql-02-configuration.md) | [Index](./infos-postgresql-00-index.md) | [Users et permissions →](./infos-postgresql-04-users-permissions.md)

## Créer une database

```sql
-- Syntaxe simple
CREATE DATABASE mydb;

-- Avec options
CREATE DATABASE mydb
    OWNER = myuser
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Se connecter
\c mydb
```

```bash
# Depuis le shell
createdb mydb
createdb -O myuser mydb
```

## Lister et supprimer databases

```sql
-- Lister les databases
\l
SELECT datname FROM pg_database;

-- Supprimer une database
DROP DATABASE mydb;

-- Supprimer si existe
DROP DATABASE IF EXISTS mydb;
```

## Schémas

```sql
-- Créer un schéma
CREATE SCHEMA sales;
CREATE SCHEMA IF NOT EXISTS inventory;

-- Schéma avec propriétaire
CREATE SCHEMA hr AUTHORIZATION hruser;

-- Lister les schémas
\dn
SELECT schema_name FROM information_schema.schemata;

-- Supprimer un schéma
DROP SCHEMA sales;
DROP SCHEMA sales CASCADE;  -- Supprime aussi les objets
```

## Tables

```sql
-- Créer une table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table avec schéma
CREATE TABLE sales.orders (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
);

-- Lister les tables
\dt
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
```

## Types de colonnes

```sql
CREATE TABLE examples (
    -- Entiers
    small_num SMALLINT,          -- -32768 à 32767
    normal_num INTEGER,           -- -2 milliards à 2 milliards
    big_num BIGINT,              -- Très grand nombre
    auto_id SERIAL,              -- Auto-increment
    big_auto_id BIGSERIAL,       -- BIGINT auto-increment

    -- Décimaux
    price DECIMAL(10,2),         -- Précision fixe
    score NUMERIC(5,2),          -- Alias de DECIMAL
    ratio REAL,                  -- Float 4 bytes
    precise DOUBLE PRECISION,    -- Float 8 bytes

    -- Texte
    code CHAR(10),               -- Longueur fixe
    name VARCHAR(255),           -- Longueur variable
    description TEXT,            -- Texte illimité

    -- Booléen
    is_active BOOLEAN,

    -- Date et heure
    birth_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMPTZ,      -- Avec timezone
    duration INTERVAL,

    -- JSON
    settings JSON,
    metadata JSONB,              -- JSON binaire (indexable)

    -- Autres
    tags TEXT[],                 -- Array
    coordinates POINT,           -- Géométrie
    ip_address INET,            -- Adresse IP
    mac_address MACADDR,        -- Adresse MAC
    uuid_col UUID               -- UUID
);
```

## Contraintes

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) CHECK (price > 0),
    category_id INTEGER REFERENCES categories(id),
    sku VARCHAR(50) UNIQUE,
    stock INTEGER DEFAULT 0,
    CONSTRAINT price_positive CHECK (price > 0)
);

-- Clé primaire composite
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

## Modifier une table

```sql
-- Ajouter une colonne
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- Supprimer une colonne
ALTER TABLE users DROP COLUMN phone;

-- Modifier une colonne
ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(300);
ALTER TABLE users ALTER COLUMN username SET NOT NULL;
ALTER TABLE users ALTER COLUMN created_at SET DEFAULT NOW();

-- Renommer
ALTER TABLE users RENAME COLUMN username TO user_name;
ALTER TABLE users RENAME TO app_users;

-- Contraintes
ALTER TABLE users ADD CONSTRAINT email_check CHECK (email LIKE '%@%');
ALTER TABLE users DROP CONSTRAINT email_check;
```

[← Configuration](./infos-postgresql-02-configuration.md) | [Index](./infos-postgresql-00-index.md) | [Users et permissions →](./infos-postgresql-04-users-permissions.md)
