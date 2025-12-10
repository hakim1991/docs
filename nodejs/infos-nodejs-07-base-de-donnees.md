# 💾 Base de données

[← Express](./infos-nodejs-06-express-serveur-web.md) | [Index](./infos-nodejs-00-index.md) | [Sécurité →](./infos-nodejs-08-securite.md)

## MongoDB avec Mongoose

### Installation

```bash
npm install mongoose
```

### Connexion

```javascript
const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/mydb', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB error:', err));
```

### Schéma et modèle

```javascript
const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  age: {
    type: Number,
    min: 0,
    max: 120
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

const User = mongoose.model('User', userSchema);

module.exports = User;
```

### CRUD opérations

```javascript
const User = require('./models/User');

// CREATE
const newUser = new User({
  name: 'Alice',
  email: 'alice@example.com',
  age: 30
});

await newUser.save();

// ou
await User.create({
  name: 'Bob',
  email: 'bob@example.com'
});

// READ
const users = await User.find();
const user = await User.findById(id);
const alice = await User.findOne({ name: 'Alice' });

// UPDATE
await User.findByIdAndUpdate(id, { age: 31 });
await User.updateOne({ name: 'Alice' }, { age: 31 });
await User.updateMany({ age: { $lt: 18 } }, { verified: false });

// DELETE
await User.findByIdAndDelete(id);
await User.deleteOne({ name: 'Alice' });
await User.deleteMany({ age: { $lt: 18 } });
```

### Query avancées

```javascript
// Where
const users = await User.find({ age: { $gte: 18 } });

// Select fields
const users = await User.find().select('name email');

// Sort
const users = await User.find().sort({ createdAt: -1 });

// Limit & Skip
const users = await User.find().limit(10).skip(20);

// Count
const count = await User.countDocuments({ age: { $gte: 18 } });

// Exists
const exists = await User.exists({ email: 'alice@example.com' });
```

## PostgreSQL

### Installation

```bash
npm install pg
```

### Connexion

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'postgres',
  password: 'password'
});

module.exports = pool;
```

### Requêtes

```javascript
const pool = require('./db');

// Query simple
const result = await pool.query('SELECT * FROM users');
console.log(result.rows);

// Query avec paramètres
const result = await pool.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]
);

// Insert
const result = await pool.query(
  'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
  ['Alice', 'alice@example.com']
);

// Update
await pool.query(
  'UPDATE users SET age = $1 WHERE id = $2',
  [31, userId]
);

// Delete
await pool.query('DELETE FROM users WHERE id = $1', [userId]);

// Transaction
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('INSERT INTO users ...');
  await client.query('UPDATE accounts ...');
  await client.query('COMMIT');
} catch (err) {
  await client.query('ROLLBACK');
  throw err;
} finally {
  client.release();
}
```

## MySQL

### Installation

```bash
npm install mysql2
```

### Connexion

```javascript
const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb',
  waitForConnections: true,
  connectionLimit: 10
});

module.exports = pool;
```

### Requêtes

```javascript
const pool = require('./db');

// Query
const [rows] = await pool.query('SELECT * FROM users');
console.log(rows);

// Avec paramètres
const [rows] = await pool.query(
  'SELECT * FROM users WHERE id = ?',
  [userId]
);

// Insert
const [result] = await pool.query(
  'INSERT INTO users (name, email) VALUES (?, ?)',
  ['Alice', 'alice@example.com']
);
console.log('Insert ID:', result.insertId);

// Update
await pool.query('UPDATE users SET age = ? WHERE id = ?', [31, userId]);

// Delete
await pool.query('DELETE FROM users WHERE id = ?', [userId]);
```

## Prisma ORM

### Installation

```bash
npm install prisma @prisma/client
npx prisma init
```

### Schema

```prisma
// prisma/schema.prisma

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

### Migration

```bash
# Créer migration
npx prisma migrate dev --name init

# Appliquer migrations
npx prisma migrate deploy

# Générer client
npx prisma generate
```

### Utilisation

```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// Create
const user = await prisma.user.create({
  data: {
    email: 'alice@example.com',
    name: 'Alice'
  }
});

// Read
const users = await prisma.user.findMany();
const user = await prisma.user.findUnique({
  where: { id: 1 }
});

// With relations
const userWithPosts = await prisma.user.findUnique({
  where: { id: 1 },
  include: { posts: true }
});

// Update
const updated = await prisma.user.update({
  where: { id: 1 },
  data: { name: 'Alice Updated' }
});

// Delete
await prisma.user.delete({
  where: { id: 1 }
});

// Disconnect
await prisma.$disconnect();
```

## TypeORM

### Installation

```bash
npm install typeorm reflect-metadata
npm install pg  # ou mysql2, sqlite3, etc.
```

### Configuration

```typescript
// ormconfig.json
{
  "type": "postgres",
  "host": "localhost",
  "port": 5432,
  "username": "postgres",
  "password": "password",
  "database": "mydb",
  "synchronize": true,
  "entities": ["src/entity/**/*.ts"]
}
```

### Entity

```typescript
// src/entity/User.ts
import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column({ unique: true })
  email: string;

  @Column({ nullable: true })
  age: number;
}
```

### Utilisation

```typescript
import { createConnection } from 'typeorm';
import { User } from './entity/User';

const connection = await createConnection();
const userRepository = connection.getRepository(User);

// Create
const user = new User();
user.name = 'Alice';
user.email = 'alice@example.com';
await userRepository.save(user);

// Read
const users = await userRepository.find();
const user = await userRepository.findOne(1);

// Update
await userRepository.update(1, { age: 31 });

// Delete
await userRepository.delete(1);
```

## Redis

### Installation

```bash
npm install redis
```

### Connexion

```javascript
const redis = require('redis');
const client = redis.createClient({
  host: 'localhost',
  port: 6379
});

client.on('error', (err) => console.error('Redis error:', err));
client.on('connect', () => console.log('Redis connected'));

await client.connect();
```

### Opérations

```javascript
// Set / Get
await client.set('key', 'value');
const value = await client.get('key');

// Set avec expiration
await client.setEx('key', 3600, 'value'); // 1 hour

// Set si n'existe pas
await client.setNX('key', 'value');

// Delete
await client.del('key');

// Exists
const exists = await client.exists('key');

// Incr / Decr
await client.incr('counter');
await client.decr('counter');

// Hash
await client.hSet('user:1', 'name', 'Alice');
await client.hSet('user:1', 'email', 'alice@example.com');
const user = await client.hGetAll('user:1');

// List
await client.rPush('list', 'item1');
await client.rPush('list', 'item2');
const items = await client.lRange('list', 0, -1);

// Set (ensemble)
await client.sAdd('set', 'member1');
await client.sAdd('set', 'member2');
const members = await client.sMembers('set');

// Disconnect
await client.quit();
```

## Exemple complet Express + MongoDB

```javascript
// app.js
const express = require('express');
const mongoose = require('mongoose');
const app = express();

app.use(express.json());

// Connect MongoDB
mongoose.connect('mongodb://localhost:27017/myapp')
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB error:', err));

// Model
const User = mongoose.model('User', {
  name: String,
  email: { type: String, unique: true },
  age: Number
});

// Routes
app.get('/api/users', async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/api/users/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/users', async (req, res) => {
  try {
    const user = await User.create(req.body);
    res.status(201).json(user);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.put('/api/users/:id', async (req, res) => {
  try {
    const user = await User.findByIdAndUpdate(
      req.params.id,
      req.body,
      { new: true }
    );
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.delete('/api/users/:id', async (req, res) => {
  try {
    const user = await User.findByIdAndDelete(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.status(204).send();
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

[← Express](./infos-nodejs-06-express-serveur-web.md) | [Index](./infos-nodejs-00-index.md) | [Sécurité →](./infos-nodejs-08-securite.md)
