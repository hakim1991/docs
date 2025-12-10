# 🗄️ Bases de données

[← Django](./infos-python-09-django.md) | [Index](./infos-python-00-index.md) | [Testing →](./infos-python-11-testing.md)

## SQLite (intégré)

```python
import sqlite3

# Connexion
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Créer table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    )
""")

# Insert
cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
               ("Alice", "alice@example.com", 25))
conn.commit()

# Select
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Select avec paramètres
cursor.execute("SELECT * FROM users WHERE age > ?", (18,))
rows = cursor.fetchall()

# Update
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Alice"))
conn.commit()

# Delete
cursor.execute("DELETE FROM users WHERE id = ?", (1,))
conn.commit()

# Fermer
conn.close()

# Context manager
with sqlite3.connect("database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
```

## PostgreSQL (psycopg2)

```bash
pip install psycopg2-binary
```

```python
import psycopg2
from psycopg2.extras import RealDictCursor

# Connexion
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="mydb",
    user="postgres",
    password="password"
)

cursor = conn.cursor(cursor_factory=RealDictCursor)

# Créer table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# Insert
cursor.execute(
    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
    ("Alice", "alice@example.com")
)
user_id = cursor.fetchone()["id"]
conn.commit()

# Select
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(user["name"], user["email"])

# Close
cursor.close()
conn.close()
```

## MySQL

```bash
pip install mysql-connector-python
```

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="mydb"
)

cursor = conn.cursor(dictionary=True)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE
    )
""")

cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)",
               ("Alice", "alice@example.com"))
conn.commit()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

cursor.close()
conn.close()
```

## SQLAlchemy (ORM)

```bash
pip install sqlalchemy
```

### Core

```python
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

# Engine
engine = create_engine("sqlite:///database.db")

# Metadata
metadata = MetaData()

# Table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("email", String(100), unique=True)
)

# Créer tables
metadata.create_all(engine)

# Insert
with engine.connect() as conn:
    conn.execute(users.insert().values(name="Alice", email="alice@example.com"))
    conn.commit()

    # Select
    result = conn.execute(users.select())
    for row in result:
        print(row.name, row.email)
```

### ORM

```python
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Engine et Session
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Modèles
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User(name={self.name})>"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

# Créer tables
Base.metadata.create_all(engine)

# Create
user = User(name="Alice", email="alice@example.com")
session.add(user)
session.commit()

# Query
users = session.query(User).all()
user = session.query(User).filter_by(name="Alice").first()
user = session.query(User).filter(User.id == 1).first()

# Update
user = session.query(User).filter_by(name="Alice").first()
user.email = "newemail@example.com"
session.commit()

# Delete
user = session.query(User).filter_by(name="Alice").first()
session.delete(user)
session.commit()

# Relations
post = Post(title="Mon article", content="Contenu", author=user)
session.add(post)
session.commit()

# Charger avec relations
user = session.query(User).filter_by(name="Alice").first()
for post in user.posts:
    print(post.title)

# Close
session.close()
```

## MongoDB (PyMongo)

```bash
pip install pymongo
```

```python
from pymongo import MongoClient
from datetime import datetime

# Connexion
client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["users"]

# Insert
user = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "created_at": datetime.now()
}
result = collection.insert_one(user)
print(f"Inserted ID: {result.inserted_id}")

# Insert many
users = [
    {"name": "Bob", "email": "bob@example.com"},
    {"name": "Charlie", "email": "charlie@example.com"}
]
collection.insert_many(users)

# Find
users = collection.find()
for user in users:
    print(user)

# Find one
user = collection.find_one({"name": "Alice"})

# Find with query
users = collection.find({"age": {"$gt": 18}})

# Update
collection.update_one(
    {"name": "Alice"},
    {"$set": {"age": 26}}
)

# Update many
collection.update_many(
    {"age": {"$lt": 18}},
    {"$set": {"minor": True}}
)

# Delete
collection.delete_one({"name": "Alice"})
collection.delete_many({"age": {"$lt": 18}})

# Count
count = collection.count_documents({"age": {"$gt": 18}})

# Sort
users = collection.find().sort("name", 1)  # 1 = ascending, -1 = descending

# Limit
users = collection.find().limit(10)

# Close
client.close()
```

## Redis

```bash
pip install redis
```

```python
import redis

# Connexion
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# String
r.set("name", "Alice")
name = r.get("name")

# Expiration
r.setex("session", 3600, "value")  # Expire dans 1h

# Hash
r.hset("user:1", "name", "Alice")
r.hset("user:1", "email", "alice@example.com")
name = r.hget("user:1", "name")
user = r.hgetall("user:1")

# List
r.lpush("tasks", "task1", "task2")
r.rpush("tasks", "task3")
tasks = r.lrange("tasks", 0, -1)

# Set
r.sadd("tags", "python", "flask", "django")
tags = r.smembers("tags")
r.srem("tags", "flask")

# Sorted Set
r.zadd("scores", {"alice": 100, "bob": 90, "charlie": 95})
scores = r.zrange("scores", 0, -1, withscores=True)

# Pub/Sub
pubsub = r.pubsub()
pubsub.subscribe("channel")

# Publish
r.publish("channel", "message")

# Close
r.close()
```

## Connection pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

## Migrations (Alembic)

```bash
pip install alembic
```

```bash
# Initialiser
alembic init alembic

# Créer migration
alembic revision --autogenerate -m "create users table"

# Appliquer migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

```python
# alembic/env.py
from myapp.models import Base
target_metadata = Base.metadata
```

## Bonnes pratiques

```python
# ✅ Utiliser context manager
with engine.connect() as conn:
    result = conn.execute(query)

# ✅ Paramètres (éviter SQL injection)
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ❌ Concaténation (dangereux)
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# ✅ Transaction
with session.begin():
    session.add(user)
    session.add(post)

# ✅ Try/except
try:
    session.add(user)
    session.commit()
except IntegrityError:
    session.rollback()
    print("User already exists")

# ✅ Connection pool
engine = create_engine("...", pool_size=10)

# ✅ Index pour performance
Index("idx_user_email", User.email)
```

[← Django](./infos-python-09-django.md) | [Index](./infos-python-00-index.md) | [Testing →](./infos-python-11-testing.md)
