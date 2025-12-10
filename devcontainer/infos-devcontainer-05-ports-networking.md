# 🌐 Ports et Networking

[← Extensions](./infos-devcontainer-04-extensions-vscode.md) | [Index](./infos-devcontainer-00-index.md) | [Volumes →](./infos-devcontainer-06-volumes-persistence.md)

## Port Forwarding

### forwardPorts

Transférer des ports du container vers l'hôte.

```json
{
  "forwardPorts": [3000]
}
```

```json
{
  "forwardPorts": [3000, 5000, 8080]
}
```

### Accès

Une fois le port forwardé, accéder via :
- `http://localhost:3000`
- VS Code affiche une notification avec le lien

## portsAttributes

Configurer les ports individuellement.

```json
{
  "forwardPorts": [3000, 5000],
  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "notify"
    },
    "5000": {
      "label": "Backend API",
      "onAutoForward": "silent"
    }
  }
}
```

### Propriétés

#### label

Nom du port affiché dans VS Code.

```json
{
  "portsAttributes": {
    "3000": {
      "label": "React App"
    }
  }
}
```

#### onAutoForward

Action lors du forward automatique :
- `notify` : notification
- `openBrowser` : ouvrir navigateur
- `openPreview` : ouvrir dans VS Code
- `silent` : aucune action
- `ignore` : ne pas forwarder

```json
{
  "portsAttributes": {
    "3000": {
      "onAutoForward": "openBrowser"
    }
  }
}
```

#### protocol

Protocole du port (http ou https).

```json
{
  "portsAttributes": {
    "3000": {
      "protocol": "https"
    }
  }
}
```

## Port automatique

VS Code détecte automatiquement les ports ouverts dans le container.

### Désactiver auto-forward

```json
{
  "portsAttributes": {
    "5432": {
      "onAutoForward": "ignore"
    }
  }
}
```

## Exemple complet

```json
{
  "name": "Full Stack App",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18",

  "forwardPorts": [3000, 5000, 5432],

  "portsAttributes": {
    "3000": {
      "label": "Frontend (React)",
      "onAutoForward": "openBrowser",
      "protocol": "http"
    },
    "5000": {
      "label": "Backend API (Express)",
      "onAutoForward": "notify",
      "protocol": "http"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "ignore"
    }
  }
}
```

## Networking

### Network mode

```json
{
  "runArgs": ["--network=host"]
}
```

Modes disponibles :
- `bridge` (défaut)
- `host`
- `none`
- Custom network

### Host network

Partager le réseau de l'hôte.

```json
{
  "runArgs": ["--network=host"]
}
```

Avantage : accès direct à localhost de l'hôte.

### Custom network

```json
{
  "runArgs": ["--network=my-network"]
}
```

## Docker Compose networking

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    networks:
      - app-network

  db:
    image: postgres:15
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

```json
// devcontainer.json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app"
}
```

Communication entre services via nom du service :

```javascript
// Dans le container app
const db = new Client({
  host: 'db', // Nom du service
  port: 5432,
  user: 'postgres',
  password: 'postgres',
  database: 'mydb',
});
```

## Ports avec Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "3000:3000"
      - "5000:5000"

  db:
    image: postgres:15
    ports:
      - "5432:5432"
```

```json
// devcontainer.json
{
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "forwardPorts": [3000, 5000, 5432]
}
```

## Exemple Multi-services

### Fichier docker-compose.yml

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
    networks:
      - app-network

  api:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ../api:/app
    command: npm run dev
    ports:
      - "5000:5000"
    networks:
      - app-network
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/mydb

  db:
    image: postgres:15-alpine
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - app-network
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: mydb

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    networks:
      - app-network

volumes:
  postgres-data:

networks:
  app-network:
    driver: bridge
```

### Fichier devcontainer.json

```json
{
  "name": "Full Stack Multi-services",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "forwardPorts": [3000, 5000, 5432, 6379],

  "portsAttributes": {
    "3000": {
      "label": "Frontend",
      "onAutoForward": "openBrowser"
    },
    "5000": {
      "label": "API",
      "onAutoForward": "notify"
    },
    "5432": {
      "label": "PostgreSQL",
      "onAutoForward": "ignore"
    },
    "6379": {
      "label": "Redis",
      "onAutoForward": "ignore"
    }
  },

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "cweijan.vscode-postgresql-client2"
      ]
    }
  }
}
```

### Connexion entre services

```javascript
// Frontend → API
const API_URL = 'http://localhost:5000';
fetch(`${API_URL}/api/users`);

// API → Database (dans le container)
const db = new Client({
  host: 'db', // Nom du service Docker
  port: 5432,
  user: 'postgres',
  password: 'postgres',
  database: 'mydb',
});

// API → Redis (dans le container)
const redis = new Redis({
  host: 'redis',
  port: 6379,
});
```

## Accès depuis l'hôte

### Container → Hôte

Utiliser `host.docker.internal` (Windows/Mac) :

```javascript
const API_URL = 'http://host.docker.internal:8000';
```

Linux : utiliser `--network=host` ou l'IP de l'hôte.

### Hôte → Container

Utiliser `localhost:PORT` où PORT est forwardé.

## DNS et résolution de noms

Dans Docker Compose, les services sont accessibles par leur nom :

```yaml
services:
  app:
    # Accessible via 'app'
  db:
    # Accessible via 'db'
  redis:
    # Accessible via 'redis'
```

```bash
# Depuis le container app
ping db
curl http://redis:6379
psql -h db -U postgres
```

## Variables d'environnement réseau

```json
{
  "containerEnv": {
    "DATABASE_HOST": "db",
    "DATABASE_PORT": "5432",
    "REDIS_HOST": "redis",
    "REDIS_PORT": "6379",
    "API_URL": "http://localhost:5000"
  }
}
```

## Troubleshooting

### Port déjà utilisé

```bash
# Vérifier les ports utilisés
docker ps
netstat -tulpn | grep :3000

# Changer le port
# Dans devcontainer.json
{
  "forwardPorts": [3001]
}
```

### Service non accessible

```bash
# Vérifier les networks
docker network ls
docker network inspect devcontainer_app-network

# Vérifier les services
docker-compose ps

# Logs
docker-compose logs db
```

### Firewall

Vérifier que le firewall autorise les ports.

```bash
# Linux
sudo ufw allow 3000

# Windows
# Firewall settings
```

## Sécurité

### Ne pas exposer les ports sensibles

```json
{
  "forwardPorts": [3000],
  // Ne PAS forwarder 5432, 6379, etc. en production
}
```

### Utiliser des variables d'environnement

```json
{
  "containerEnv": {
    "DATABASE_URL": "${localEnv:DATABASE_URL}"
  }
}
```

### Restreindre l'accès

```yaml
# docker-compose.yml
services:
  db:
    # Ne pas exposer le port publiquement
    # ports:
    #   - "5432:5432"
    expose:
      - "5432"
```

## Commandes utiles

```bash
# Voir les ports forwardés
docker port <container-id>

# Tester la connectivité
ping db
telnet db 5432
curl http://api:5000/health

# Voir les networks
docker network ls
docker network inspect <network-name>
```

## Bonnes pratiques

1. **Forwarder uniquement les ports nécessaires** : sécurité
2. **Utiliser des labels clairs** : facilite le dev
3. **Configurer onAutoForward** : meilleure UX
4. **Ne pas exposer les DB en production** : sécurité
5. **Utiliser Docker networks** : isolation
6. **Documenter les ports** : dans README.md

[← Extensions](./infos-devcontainer-04-extensions-vscode.md) | [Index](./infos-devcontainer-00-index.md) | [Volumes →](./infos-devcontainer-06-volumes-persistence.md)
