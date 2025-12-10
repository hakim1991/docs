# 🔍 Requêtes SQL

[← Users](./infos-postgresql-04-users-permissions.md) | [Index](./infos-postgresql-00-index.md) | [Index et optimisation →](./infos-postgresql-06-index-optimisation.md)

## SELECT de base

```sql
-- Sélectionner tout
SELECT * FROM users;

-- Colonnes spécifiques
SELECT id, email, username FROM users;

-- Avec alias
SELECT email AS user_email, created_at AS registered_date FROM users;

-- DISTINCT
SELECT DISTINCT country FROM users;

-- LIMIT et OFFSET
SELECT * FROM users LIMIT 10 OFFSET 20;
```

## WHERE - Filtrer

```sql
-- Égalité
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE country = 'FR';

-- Comparaison
SELECT * FROM products WHERE price > 100;
SELECT * FROM products WHERE stock <= 0;

-- LIKE (pattern matching)
SELECT * FROM users WHERE email LIKE '%@gmail.com';
SELECT * FROM products WHERE name ILIKE '%phone%';  -- Case insensitive

-- IN
SELECT * FROM users WHERE country IN ('FR', 'BE', 'CH');

-- BETWEEN
SELECT * FROM orders WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';

-- IS NULL
SELECT * FROM users WHERE phone IS NULL;
SELECT * FROM users WHERE phone IS NOT NULL;

-- Opérateurs logiques
SELECT * FROM users WHERE country = 'FR' AND age >= 18;
SELECT * FROM products WHERE price < 50 OR stock > 100;
```

## ORDER BY - Trier

```sql
-- Ascendant (par défaut)
SELECT * FROM users ORDER BY created_at;
SELECT * FROM users ORDER BY created_at ASC;

-- Descendant
SELECT * FROM users ORDER BY created_at DESC;

-- Multiple colonnes
SELECT * FROM users ORDER BY country, age DESC;

-- NULLS FIRST/LAST
SELECT * FROM users ORDER BY phone NULLS LAST;
```

## JOIN - Joindre des tables

```sql
-- INNER JOIN
SELECT users.username, orders.total
FROM users
INNER JOIN orders ON users.id = orders.user_id;

-- LEFT JOIN (tous les users, même sans orders)
SELECT users.username, orders.total
FROM users
LEFT JOIN orders ON users.id = orders.user_id;

-- RIGHT JOIN
SELECT users.username, orders.total
FROM users
RIGHT JOIN orders ON users.id = orders.user_id;

-- FULL OUTER JOIN
SELECT users.username, orders.total
FROM users
FULL OUTER JOIN orders ON users.id = orders.user_id;

-- Multiple JOINs
SELECT u.username, o.total, p.name, oi.quantity
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

## Fonctions d'agrégation

```sql
-- COUNT
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT country) FROM users;

-- SUM, AVG, MIN, MAX
SELECT SUM(total) FROM orders;
SELECT AVG(price) FROM products;
SELECT MIN(price), MAX(price) FROM products;

-- GROUP BY
SELECT country, COUNT(*) as user_count
FROM users
GROUP BY country;

-- HAVING (filtre après GROUP BY)
SELECT country, COUNT(*) as user_count
FROM users
GROUP BY country
HAVING COUNT(*) > 10;
```

## INSERT

```sql
-- Insert simple
INSERT INTO users (email, username) VALUES ('test@example.com', 'testuser');

-- Insert multiple
INSERT INTO users (email, username) VALUES
    ('user1@example.com', 'user1'),
    ('user2@example.com', 'user2'),
    ('user3@example.com', 'user3');

-- Insert avec RETURNING
INSERT INTO users (email, username)
VALUES ('new@example.com', 'newuser')
RETURNING id, created_at;
```

## UPDATE

```sql
-- Update simple
UPDATE users SET country = 'FR' WHERE id = 1;

-- Update multiple colonnes
UPDATE users
SET country = 'FR', updated_at = NOW()
WHERE id = 1;

-- Update avec condition
UPDATE products
SET stock = stock - 1
WHERE id = 123 AND stock > 0;

-- Update avec RETURNING
UPDATE users SET is_active = true WHERE id = 1 RETURNING *;
```

## DELETE

```sql
-- Delete avec condition
DELETE FROM users WHERE id = 1;

-- Delete multiple
DELETE FROM users WHERE created_at < '2020-01-01';

-- Delete avec RETURNING
DELETE FROM users WHERE id = 1 RETURNING *;

-- TRUNCATE (plus rapide, vide toute la table)
TRUNCATE TABLE logs;
```

## Sous-requêtes

```sql
-- Dans WHERE
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

-- Dans SELECT
SELECT username,
       (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count
FROM users;

-- EXISTS
SELECT * FROM users u
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

## CTE (Common Table Expressions)

```sql
-- CTE simple
WITH active_users AS (
    SELECT * FROM users WHERE is_active = true
)
SELECT * FROM active_users WHERE country = 'FR';

-- CTE multiple
WITH
    french_users AS (SELECT * FROM users WHERE country = 'FR'),
    recent_orders AS (SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days')
SELECT u.username, COUNT(o.id) as order_count
FROM french_users u
LEFT JOIN recent_orders o ON u.id = o.user_id
GROUP BY u.username;
```

## Window Functions

```sql
-- ROW_NUMBER
SELECT username, email,
       ROW_NUMBER() OVER (ORDER BY created_at) as row_num
FROM users;

-- RANK
SELECT name, price,
       RANK() OVER (ORDER BY price DESC) as price_rank
FROM products;

-- Partition
SELECT category, name, price,
       AVG(price) OVER (PARTITION BY category) as avg_category_price
FROM products;
```

[← Users](./infos-postgresql-04-users-permissions.md) | [Index](./infos-postgresql-00-index.md) | [Index et optimisation →](./infos-postgresql-06-index-optimisation.md)
