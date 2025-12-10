# 🚀 Index et Optimisation

[← Requêtes SQL](./infos-postgresql-05-requetes-sql.md) | [Index](./infos-postgresql-00-index.md) | [Performances avancées →](./infos-postgresql-07-performances-avancees.md)

## Types d'index

```sql
-- B-tree (par défaut, pour la plupart des cas)
CREATE INDEX idx_users_email ON users(email);

-- Index unique
CREATE UNIQUE INDEX idx_users_username ON users(username);

-- Index composite (multi-colonnes)
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at);

-- Index partiel (avec condition)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Index sur expression
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Hash (pour égalité uniquement)
CREATE INDEX idx_users_country_hash ON users USING HASH (country);

-- GiST (pour types géométriques, full-text search)
CREATE INDEX idx_locations_gist ON locations USING GIST (coordinates);

-- GIN (pour JSONB, arrays, full-text)
CREATE INDEX idx_products_tags ON products USING GIN (tags);
CREATE INDEX idx_data_jsonb ON documents USING GIN (data);

-- BRIN (pour très grandes tables avec données séquentielles)
CREATE INDEX idx_logs_created_brin ON logs USING BRIN (created_at);
```

## Créer et gérer les index

```sql
-- Créer un index
CREATE INDEX idx_orders_total ON orders(total);

-- Créer index en parallèle (ne bloque pas les écritures)
CREATE INDEX CONCURRENTLY idx_products_price ON products(price);

-- Index avec options
CREATE INDEX idx_users_email ON users(email)
    WITH (fillfactor = 70);

-- Lister les index
\di
SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public';

-- Voir les index d'une table
\d users
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users';

-- Supprimer un index
DROP INDEX idx_users_email;
DROP INDEX CONCURRENTLY idx_users_email;  -- Sans bloquer
```

## EXPLAIN - Analyser les requêtes

```sql
-- Voir le plan d'exécution
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- Avec coûts détaillés
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders
WHERE user_id = 123;

-- Format JSON
EXPLAIN (FORMAT JSON)
SELECT * FROM products WHERE price > 100;

-- Voir les statistiques réelles
EXPLAIN ANALYZE
SELECT u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.username;
```

## Interpréter EXPLAIN

```sql
-- Exemple de sortie EXPLAIN
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

/*
Résultat:
  Seq Scan on orders  (cost=0.00..1234.56 rows=10 width=50)
    Filter: (user_id = 123)

Explication:
- Seq Scan : Parcours séquentiel (pas d'index utilisé)
- cost=0.00..1234.56 : Coût estimé (startup..total)
- rows=10 : Nombre de lignes estimées
- width=50 : Taille moyenne d'une ligne (bytes)
*/

-- Avec index
CREATE INDEX idx_orders_user_id ON orders(user_id);

EXPLAIN SELECT * FROM orders WHERE user_id = 123;
/*
  Index Scan using idx_orders_user_id on orders
    (cost=0.29..45.12 rows=10 width=50)
    Index Cond: (user_id = 123)
*/
```

## Types de Scan

```sql
-- Sequential Scan (parcours complet de la table)
EXPLAIN SELECT * FROM users WHERE age > 18;
-- ⚠️ Lent sur grandes tables

-- Index Scan (utilise l'index)
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- ✅ Rapide

-- Index Only Scan (données dans l'index uniquement)
CREATE INDEX idx_users_email_country ON users(email, country);
EXPLAIN SELECT email, country FROM users WHERE email = 'test@example.com';
-- ✅ Très rapide

-- Bitmap Index Scan (pour plusieurs conditions)
EXPLAIN SELECT * FROM products
WHERE category = 'Electronics' AND price > 100;

-- Index Scan Backward (tri inversé)
EXPLAIN SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;
```

## ANALYZE - Mettre à jour les statistiques

```sql
-- Analyser toute la base
ANALYZE;

-- Analyser une table
ANALYZE users;

-- Analyser des colonnes spécifiques
ANALYZE users (email, country);

-- Voir les statistiques d'une table
SELECT * FROM pg_stats WHERE tablename = 'users';

-- Voir la dernière analyse
SELECT schemaname, relname, last_analyze, last_autoanalyze
FROM pg_stat_user_tables;
```

## Optimiser les requêtes

```sql
-- ❌ Mauvais: fonction sur colonne indexée
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- ✅ Bon: créer un index sur l'expression
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'test@example.com';

-- ❌ Mauvais: OR sur différentes colonnes
SELECT * FROM users WHERE country = 'FR' OR age > 65;

-- ✅ Bon: UNION de deux requêtes
SELECT * FROM users WHERE country = 'FR'
UNION
SELECT * FROM users WHERE age > 65;

-- ❌ Mauvais: SELECT *
SELECT * FROM orders WHERE user_id = 123;

-- ✅ Bon: sélectionner uniquement les colonnes nécessaires
SELECT id, total, created_at FROM orders WHERE user_id = 123;

-- ❌ Mauvais: LIKE avec %prefix%
SELECT * FROM users WHERE email LIKE '%gmail%';

-- ✅ Bon: LIKE prefix% (peut utiliser index)
SELECT * FROM users WHERE email LIKE 'john%';

-- ✅ Encore mieux: index GIN pour full-text search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_users_email_trgm ON users USING GIN (email gin_trgm_ops);
SELECT * FROM users WHERE email LIKE '%gmail%';
```

## Index et JOIN

```sql
-- Index sur les clés étrangères
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);

-- Analyser un JOIN
EXPLAIN ANALYZE
SELECT u.username, o.total, p.name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
WHERE u.country = 'FR';

-- Index composite pour les conditions fréquentes
CREATE INDEX idx_users_country_created ON users(country, created_at);
```

## Maintenance des index

```sql
-- Voir la taille des index
SELECT
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC;

-- Voir les index non utilisés
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND indexrelid NOT IN (
        SELECT indexrelid FROM pg_index WHERE indisunique
    );

-- Supprimer les index inutilisés
DROP INDEX idx_unused_index;

-- Reconstruire un index (si corrompu ou fragmenté)
REINDEX INDEX idx_users_email;
REINDEX TABLE users;
REINDEX DATABASE mydb;
```

## Stratégies d'indexation

```sql
-- Index pour les recherches fréquentes
CREATE INDEX idx_users_email ON users(email);

-- Index composite (ordre important!)
-- Bon pour: (country = 'FR') ou (country = 'FR' AND city = 'Paris')
CREATE INDEX idx_users_country_city ON users(country, city);

-- Pas bon pour: (city = 'Paris') seul
-- Il faut créer un index séparé:
CREATE INDEX idx_users_city ON users(city);

-- Index partiel pour sous-ensemble
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;
CREATE INDEX idx_pending_orders ON orders(created_at) WHERE status = 'pending';

-- Index pour tri fréquent
CREATE INDEX idx_products_price_desc ON products(price DESC);
CREATE INDEX idx_orders_created_desc ON orders(created_at DESC);

-- Index covering (inclut toutes les colonnes nécessaires)
CREATE INDEX idx_orders_user_covering
ON orders(user_id) INCLUDE (total, created_at);
-- Permet Index Only Scan
```

## VACUUM et maintenance

```sql
-- VACUUM (nettoyer les lignes mortes)
VACUUM users;
VACUUM VERBOSE users;
VACUUM ANALYZE users;  -- VACUUM + mise à jour stats

-- VACUUM FULL (réorganise la table, bloque les écritures)
VACUUM FULL users;

-- Voir les tables qui ont besoin de VACUUM
SELECT
    schemaname,
    relname,
    n_dead_tup,
    n_live_tup,
    round(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) as dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Autovacuum (automatique)
-- Voir la configuration
SHOW autovacuum;
SELECT * FROM pg_settings WHERE name LIKE 'autovacuum%';

-- Désactiver autovacuum sur une table (déconseillé)
ALTER TABLE logs SET (autovacuum_enabled = false);
```

## Paramètres de performance

```sql
-- Voir les paramètres actuels
SHOW shared_buffers;
SHOW work_mem;
SHOW maintenance_work_mem;
SHOW effective_cache_size;

-- work_mem : mémoire pour les tris
SET work_mem = '64MB';

-- maintenance_work_mem : pour VACUUM, CREATE INDEX
SET maintenance_work_mem = '256MB';

-- random_page_cost (SSD: 1.1, HDD: 4.0)
SET random_page_cost = 1.1;

-- effective_cache_size (cache OS)
SET effective_cache_size = '4GB';
```

## Outils d'analyse

```sql
-- pg_stat_statements (extension)
CREATE EXTENSION pg_stat_statements;

-- Requêtes les plus lentes
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Requêtes les plus fréquentes
SELECT
    query,
    calls,
    mean_exec_time
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 10;

-- Réinitialiser les statistiques
SELECT pg_stat_statements_reset();
```

## Cas pratiques

```sql
-- Optimiser une requête lente
-- 1. Analyser
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- 2. Créer un index composite
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 3. Vérifier l'amélioration
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = 123 AND status = 'pending';

-- Optimiser les recherches full-text
-- 1. Installer extension
CREATE EXTENSION pg_trgm;

-- 2. Créer index GIN
CREATE INDEX idx_products_name_trgm ON products USING GIN (name gin_trgm_ops);

-- 3. Utiliser
SELECT * FROM products WHERE name ILIKE '%phone%';

-- Index pour les données JSON
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    data JSONB
);

-- Index sur tout le JSON
CREATE INDEX idx_documents_data ON documents USING GIN (data);

-- Index sur un champ spécifique
CREATE INDEX idx_documents_status ON documents ((data->>'status'));

-- Requête
SELECT * FROM documents WHERE data->>'status' = 'active';
SELECT * FROM documents WHERE data @> '{"category": "tech"}';
```

## Troubleshooting

```sql
-- Index ne s'utilise pas
-- 1. Vérifier que les stats sont à jour
ANALYZE users;

-- 2. Vérifier le plan
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 3. Forcer l'utilisation d'index (debug uniquement)
SET enable_seqscan = off;

-- 4. Vérifier les stats
SELECT * FROM pg_stats WHERE tablename = 'users' AND attname = 'email';

-- Index corrompu
-- Reconstruire
REINDEX INDEX idx_users_email;

-- Table gonflée (bloat)
-- Voir le bloat
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Solution: VACUUM FULL (bloque la table)
VACUUM FULL users;
```

[← Requêtes SQL](./infos-postgresql-05-requetes-sql.md) | [Index](./infos-postgresql-00-index.md) | [Performances avancées →](./infos-postgresql-07-performances-avancees.md)
