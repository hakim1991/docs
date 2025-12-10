# 🐋 Docker Compose

[← Volumes](./infos-devcontainer-06-volumes-persistence.md) | [Index](./infos-devcontainer-00-index.md) | [Templates →](./infos-devcontainer-08-templates-exemples.md)

## Pourquoi Docker Compose ?

Docker Compose permet de gérer plusieurs containers :
- App + Database
- Frontend + Backend + Database
- Microservices
- Services auxiliaires (Redis, etc.)

## Configuration de base

### devcontainer.json

```json
{
  "name": "Mon Projet",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace"
}
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: postgres
```

## Exemple : Node.js + PostgreSQL

### Structure

```
projet/
├── .devcontainer/
│   ├── devcontainer.json
│   ├── docker-compose.yml
│   └── Dockerfile
├── src/
├── package.json
└── README.md
```

### devcontainer.json

```json
{
  "name": "Node.js + PostgreSQL",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "cweijan.vscode-postgresql-client2"
      ]
    }
  },

  "forwardPorts": [3000, 5432],

  "postCreateCommand": "npm install",

  "remoteUser": "node"
}
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
      args:
        NODE_VERSION: 18
    volumes:
      - ..:/workspace:cached
      - node-modules:/workspace/node_modules
    command: sleep infinity
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/mydb
      NODE_ENV: development
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  node-modules:
  postgres-data:
```

### Dockerfile

```dockerfile
FROM node:18

# Installer PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

USER node
```

## Exemple : Full Stack (React + Express + PostgreSQL)

### docker-compose.yml

```yaml
version: '3.8'

services:
  # Dev Container
  devcontainer:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
      - node-modules-frontend:/workspace/frontend/node_modules
      - node-modules-backend:/workspace/backend/node_modules
    command: sleep infinity
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/mydb
      REDIS_URL: redis://redis:6379

  # PostgreSQL
  db:
    image: postgres:15-alpine
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"

  # Redis
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"

  # pgAdmin (optionnel)
  pgadmin:
    image: dpage/pgadmin4:latest
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - db

volumes:
  node-modules-frontend:
  node-modules-backend:
  postgres-data:
  redis-data:
```

### devcontainer.json

```json
{
  "name": "Full Stack App",
  "dockerComposeFile": "docker-compose.yml",
  "service": "devcontainer",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "dsznajder.es7-react-js-snippets",
        "bradlc.vscode-tailwindcss",
        "cweijan.vscode-postgresql-client2"
      ]
    }
  },

  "forwardPorts": [3000, 5000, 5432, 6379, 5050],

  "portsAttributes": {
    "3000": { "label": "Frontend" },
    "5000": { "label": "Backend API" },
    "5432": { "label": "PostgreSQL", "onAutoForward": "ignore" },
    "6379": { "label": "Redis", "onAutoForward": "ignore" },
    "5050": { "label": "pgAdmin", "onAutoForward": "silent" }
  },

  "postCreateCommand": "cd frontend && npm install && cd ../backend && npm install",

  "remoteUser": "node"
}
```

## Exemple : Python + MongoDB

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    environment:
      MONGODB_URL: mongodb://mongo:27017/mydb
      PYTHONUNBUFFERED: 1
    depends_on:
      - mongo

  mongo:
    image: mongo:7
    restart: unless-stopped
    volumes:
      - mongo-data:/data/db
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin

  mongo-express:
    image: mongo-express:latest
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin
      ME_CONFIG_MONGODB_URL: mongodb://admin:admin@mongo:27017/
    depends_on:
      - mongo

volumes:
  mongo-data:
```

## Microservices

### docker-compose.yml

```yaml
version: '3.8'

services:
  # Dev Container
  devcontainer:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    networks:
      - microservices

  # Frontend
  frontend:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ../frontend:/app
    command: npm run dev
    ports:
      - "3000:3000"
    networks:
      - microservices

  # Auth Service
  auth-service:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ../services/auth:/app
    command: npm run dev
    ports:
      - "5001:5001"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/auth
    depends_on:
      - db
    networks:
      - microservices

  # User Service
  user-service:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ../services/user:/app
    command: npm run dev
    ports:
      - "5002:5002"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/users
    depends_on:
      - db
    networks:
      - microservices

  # Database
  db:
    image: postgres:15-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    networks:
      - microservices

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - microservices

volumes:
  postgres-data:

networks:
  microservices:
    driver: bridge
```

## runServices

Démarrer des services supplémentaires automatiquement.

```json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "runServices": ["db", "redis"]
}
```

## shutdownAction

Action lors de la fermeture de VS Code.

```json
{
  "shutdownAction": "stopCompose"
}
```

Options :
- `none` : ne rien faire
- `stopCompose` : arrêter tous les services
- `stopContainer` : arrêter uniquement le container app

## Variables d'environnement

### Fichier .env

```bash
# .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mydb
API_KEY=secret
```

```yaml
# docker-compose.yml
services:
  app:
    env_file:
      - .env
```

### Variables dans devcontainer.json

```json
{
  "containerEnv": {
    "DATABASE_URL": "postgresql://postgres:postgres@db:5432/mydb"
  }
}
```

## Healthchecks

Attendre que les services soient prêts.

```yaml
services:
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    depends_on:
      db:
        condition: service_healthy
```

## Init containers

Exécuter des scripts d'initialisation.

```yaml
services:
  db:
    image: postgres:15-alpine
    volumes:
      - ./init-db:/docker-entrypoint-initdb.d
```

```sql
-- init-db/01-schema.sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255)
);
```

## Build arguments

```yaml
services:
  app:
    build:
      context: ..
      dockerfile: .devcontainer/Dockerfile
      args:
        NODE_VERSION: 18
        PYTHON_VERSION: 3.11
```

```dockerfile
ARG NODE_VERSION=18
FROM node:${NODE_VERSION}

ARG PYTHON_VERSION=3.11
RUN apt-get update && apt-get install -y python${PYTHON_VERSION}
```

## Override files

Surcharger la config pour dev/prod.

```yaml
# docker-compose.yml (base)
services:
  app:
    image: myapp:latest

# docker-compose.override.yml (auto-chargé)
services:
  app:
    build: .
    volumes:
      - .:/app
```

```json
{
  "dockerComposeFile": [
    "docker-compose.yml",
    "docker-compose.dev.yml"
  ]
}
```

## Troubleshooting

### Services ne démarrent pas

```bash
# Vérifier les logs
docker-compose logs db

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose restart db
```

### Permission denied

```yaml
services:
  app:
    user: "${UID}:${GID}"
```

### Network issues

```bash
# Vérifier les networks
docker network ls
docker network inspect devcontainer_default

# Tester connectivité
docker exec -it <container> ping db
```

## Commandes utiles

```bash
# Démarrer services
docker-compose up -d

# Arrêter services
docker-compose down

# Rebuild
docker-compose build

# Logs
docker-compose logs -f

# Exec commande
docker-compose exec app npm install

# Lister services
docker-compose ps
```

## Bonnes pratiques

1. **Utiliser healthchecks** : attendre que services soient prêts
2. **Named volumes pour data** : persistence
3. **Networks explicites** : isolation
4. **Variables d'environnement** : configuration flexible
5. **depends_on avec condition** : ordre de démarrage
6. **Documenter services** : dans README.md

[← Volumes](./infos-devcontainer-06-volumes-persistence.md) | [Index](./infos-devcontainer-00-index.md) | [Templates →](./infos-devcontainer-08-templates-exemples.md)
